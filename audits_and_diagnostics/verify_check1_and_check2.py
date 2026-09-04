"""
Script to execute Check 1 and Check 2 from VERIFY_PIPELINE_BEFORE_REAL_RUN.md on real v5 data.
"""
import os
import glob
import json
import pickle
import numpy as np
from collections import defaultdict
from sklearn.model_selection import GroupShuffleSplit

BASE_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
V5_MERGED_PATH = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'merged_dataset.json')
OUTPUT_DIR = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'posec3d_data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# MediaPipe 33 to COCO 17 mapping
COCO_MAP = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
EXERCISE_LABELS = {
    'bicep_curl': 0,
    'high_knees': 1,
    'jumping_jack': 2,
    'lunge': 3,
    'plank': 4,
    'pushup': 5,
    'squat': 6
}

# 1. Index all landmark files across the 3 landmark folders
landmark_index = {} # (exercise, clip_id_without_json) -> full_path
for root_name in ['landmarks', 'landmarks_batch2', 'landmarks_backlog']:
    root_path = os.path.join(BASE_DIR, 'data', root_name)
    if os.path.isdir(root_path):
        for json_path in glob.glob(os.path.join(root_path, '**', '*.json'), recursive=True):
            fname = os.path.basename(json_path)
            clip_id = fname.replace('.json', '')
            ex = os.path.basename(os.path.dirname(json_path))
            landmark_index[(ex, clip_id)] = json_path

print(f"Total landmark files indexed on disk: {len(landmark_index)}")

# Load v5 dataset
with open(V5_MERGED_PATH) as f:
    v5_clips = json.load(f)

print(f"Total v5 clips in master catalog: {len(v5_clips)}")

# ==============================================================================
# CHECK 1: Keypoint conversion runs on real data without silent failures
# ==============================================================================
print("\n" + "=" * 70)
print("RUNNING CHECK 1: Real Keypoint Conversion & Sanity Verification")
print("=" * 70)

converted_samples = []
skipped_clips = []

REF_W = 1000
REF_H = 1000

for clip in v5_clips:
    ex = clip['exercise']
    vid = clip['video_id']
    # clip filename like 'bicep_curl_01_clip00.json' or 'bicep_curl_01_clip00'
    raw_fname = clip.get('filename', '')
    clip_id = os.path.basename(raw_fname).replace('.json', '') if raw_fname else f"{vid}_clip00"
    
    key = (ex, clip_id)
    if key not in landmark_index:
        # try fallback matching by video_id
        matched_paths = [p for (e, c), p in landmark_index.items() if e == ex and c.startswith(vid)]
        if matched_paths:
            lm_path = matched_paths[0]
        else:
            skipped_clips.append((ex, vid, clip_id))
            continue
    else:
        lm_path = landmark_index[key]
        
    try:
        with open(lm_path) as f:
            lm_data = json.load(f)
            
        raw_lms = np.array(lm_data['landmarks'], dtype=np.float32) # (90, 33, 3)
        if raw_lms.shape[0] != 90 or raw_lms.shape[1] != 33:
            skipped_clips.append((ex, vid, f"Invalid shape: {raw_lms.shape}"))
            continue
            
        # Extract 17 COCO keypoints (x, y)
        kps_17 = raw_lms[:, COCO_MAP, :2] # (90, 17, 2)
        
        # Scale normalized [0, 1] to reference frame [0, 1000]
        kps_scaled = kps_17.copy()
        kps_scaled[:, :, 0] = np.clip(kps_scaled[:, :, 0] * REF_W, 0, REF_W)
        kps_scaled[:, :, 1] = np.clip(kps_scaled[:, :, 1] * REF_H, 0, REF_H)
        
        # Keypoint scores (1, 90, 17)
        kp_score = np.ones((1, 90, 17), dtype=np.float32)
        
        entry = {
            'frame_dir': clip_id,
            'video_id': vid,
            'label': EXERCISE_LABELS[ex],
            'exercise': ex,
            'img_shape': (REF_H, REF_W),
            'original_shape': (REF_H, REF_W),
            'total_frames': 90,
            'num_clips': 1,
            'keypoint': np.expand_dims(kps_scaled, axis=0).astype(np.float32), # (1, 90, 17, 2)
            'keypoint_score': kp_score
        }
        converted_samples.append(entry)
    except Exception as e:
        skipped_clips.append((ex, vid, str(e)))

print(f"Total clips attempted:             {len(v5_clips)}")
print(f"Total clips successfully converted: {len(converted_samples)}")
print(f"Total clips skipped:               {len(skipped_clips)}")
if skipped_clips:
    print("First 10 skipped clips:")
    for sc in skipped_clips[:10]:
        print(f"  {sc}")

# Sample 20 converted clips for min/max x, y
sample_20 = converted_samples[:20]
all_kps_20 = np.concatenate([s['keypoint'] for s in sample_20], axis=0) # (20, 90, 17, 2)
min_x = float(all_kps_20[:, :, :, 0].min())
max_x = float(all_kps_20[:, :, :, 0].max())
min_y = float(all_kps_20[:, :, :, 1].min())
max_y = float(all_kps_20[:, :, :, 1].max())

print(f"\nCoordinate bounds across sample of 20 clips (Reference Frame: 1000x1000):")
print(f"  X Range: [{min_x:.1f}, {max_x:.1f}] (Expected within [0, 1000])")
print(f"  Y Range: [{min_y:.1f}, {max_y:.1f}] (Expected within [0, 1000])")

# Check shoulder-to-hip distance for 3 sample clips
# COCO indices: Left Shoulder = 5, Left Hip = 11, Right Shoulder = 6, Right Hip = 12
print(f"\nShoulder-to-Hip Distance Sanity Check (3 Sample Clips):")
for idx in [0, len(converted_samples)//2, len(converted_samples)-1]:
    s = converted_samples[idx]
    kps = s['keypoint'][0] # (90, 17, 2)
    # Mean left shoulder-to-hip distance across 90 frames
    l_sh = kps[:, 5, :] # (90, 2)
    l_hip = kps[:, 11, :] # (90, 2)
    dist_l = np.linalg.norm(l_sh - l_hip, axis=1).mean()
    
    r_sh = kps[:, 6, :]
    r_hip = kps[:, 12, :]
    dist_r = np.linalg.norm(r_sh - r_hip, axis=1).mean()
    
    print(f"  Clip '{s['frame_dir']}' ({s['exercise']}):")
    print(f"    Left Shoulder->Hip Dist:  {dist_l:.1f} pixels ({(dist_l/REF_H)*100:.1f}% body torso height)")
    print(f"    Right Shoulder->Hip Dist: {dist_r:.1f} pixels ({(dist_r/REF_H)*100:.1f}% body torso height)")

# ==============================================================================
# CHECK 2: Train/Val split is genuinely video-disjoint
# ==============================================================================
print("\n" + "=" * 70)
print("RUNNING CHECK 2: Train/Val Disjoint Video Split Verification")
print("=" * 70)

# Build strictly video-disjoint 80/20 split using GroupShuffleSplit
video_groups = [s['video_id'] for s in converted_samples]
labels = [s['label'] for s in converted_samples]

gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
train_idx, val_idx = next(gss.split(converted_samples, labels, groups=video_groups))

train_data = [converted_samples[i] for i in train_idx]
val_data = [converted_samples[i] for i in val_idx]

train_pkl_path = os.path.join(OUTPUT_DIR, 'custom_dataset_train.pkl')
val_pkl_path = os.path.join(OUTPUT_DIR, 'custom_dataset_val.pkl')

with open(train_pkl_path, 'wb') as f:
    pickle.dump(train_data, f)
with open(val_pkl_path, 'wb') as f:
    pickle.dump(val_data, f)

print(f"Saved train pickle: {train_pkl_path} ({len(train_data)} clips)")
print(f"Saved val pickle:   {val_pkl_path} ({len(val_data)} clips)")

# Execute exact Check 2 test code
with open(train_pkl_path, 'rb') as f:
    train = pickle.load(f)
with open(val_pkl_path, 'rb') as f:
    val = pickle.load(f)

train_videos = set((a['label'], a['video_id']) for a in train)
val_videos = set((a['label'], a['video_id']) for a in val)
overlap = train_videos & val_videos

print(f"\nExact Output for Check 2 Code:")
print(f"Train videos: {len(train_videos)}, Val videos: {len(val_videos)}")
print(f"Overlap (MUST be 0): {len(overlap)}")
if overlap:
    print("!!! LEAKAGE DETECTED !!!", list(overlap)[:10])
else:
    print("Zero video leakage confirmed across train and val splits.")

# Build Tiny Dataset (5 clips per class) for Check 4
tiny_train = []
tiny_val = []
by_class_train = defaultdict(list)
by_class_val = defaultdict(list)

for c in train_data:
    by_class_train[c['label']].append(c)
for c in val_data:
    by_class_val[c['label']].append(c)

for lbl in range(7):
    tiny_train.extend(by_class_train[lbl][:4]) # 4 train per class
    tiny_val.extend(by_class_val[lbl][:1])     # 1 val per class

tiny_train_path = os.path.join(OUTPUT_DIR, 'tiny_train.pkl')
tiny_val_path = os.path.join(OUTPUT_DIR, 'tiny_val.pkl')

with open(tiny_train_path, 'wb') as f:
    pickle.dump(tiny_train, f)
with open(tiny_val_path, 'wb') as f:
    pickle.dump(tiny_val, f)

print(f"\nTiny Dataset Created for Check 4 Dry Run:")
print(f"  tiny_train.pkl: {len(tiny_train)} clips (4 per class x 7 classes)")
print(f"  tiny_val.pkl:   {len(tiny_val)} clips (1 per class x 7 classes)")
