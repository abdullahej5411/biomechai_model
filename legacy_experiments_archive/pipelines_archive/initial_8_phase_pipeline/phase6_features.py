"""
Phase 6 of 8 — Merge and Rebuild the Feature Matrix
- Loads accepted clips from Phase 5 (model_training/cleanup_v2/accepted_clips.json)
- Computes exact 50-feature vectors using extract_features & angle functions from train_model.py
- Validates shapes, NaNs, and Infs
- Saves merged dataset with features to model_training/cleanup_v2/merged_dataset.json
"""
import os, sys, json, re
import numpy as np

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
CLEANUP_DIR     = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2')
ACC_FILE        = os.path.join(CLEANUP_DIR, 'accepted_clips.json')
OUT_MERGED_FILE = os.path.join(CLEANUP_DIR, 'merged_dataset.json')

EXERCISES = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']
ORDER     = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']

# 1. Prerequisite verification
if not os.path.exists(ACC_FILE):
    print("ERROR: accepted_clips.json from Phase 5 is missing!")
    sys.exit(1)

with open(ACC_FILE, 'r') as f:
    accepted_by_ex = json.load(f)

print("Prerequisite verified: accepted_clips.json found.\n")

# 2. Exact feature extraction functions from train_model.py
def angle(lm, a, b, c):
    ba = lm[:, a, :2] - lm[:, b, :2]
    bc = lm[:, c, :2] - lm[:, b, :2]
    cos = np.sum(ba*bc, axis=1) / (
        np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1) + 1e-9)
    return np.degrees(np.arccos(np.clip(cos, -1, 1)))

def extract_features(landmarks):
    lm = np.array(landmarks)
    features = []
    angle_seqs = {
        'knee_l':     angle(lm, 23, 25, 27), 'knee_r':     angle(lm, 24, 26, 28),
        'elbow_l':    angle(lm, 11, 13, 15), 'elbow_r':    angle(lm, 12, 14, 16),
        'hip_l':      angle(lm, 11, 23, 25), 'hip_r':      angle(lm, 12, 24, 26),
        'shoulder_l': angle(lm, 13, 11, 23), 'shoulder_r': angle(lm, 14, 12, 24),
    }
    for seq in angle_seqs.values():
        features.extend([np.mean(seq), np.std(seq), np.min(seq), np.max(seq),
                          np.max(seq) - np.min(seq)])
    for seq in angle_seqs.values():
        features.append(np.mean(np.abs(np.diff(seq))))
    features.append(np.mean(np.abs(angle_seqs['knee_l'] - angle_seqs['knee_r'])))
    features.append(np.mean(np.abs(angle_seqs['shoulder_l'] - angle_seqs['shoulder_r'])))
    return np.array(features)

# 3. Process all accepted clips and build merged dataset
merged_data = []
summary_table = []

for exercise in ORDER:
    clips = accepted_by_ex.get(exercise, [])
    unique_vids = set()
    feature_list = []
    
    for c in clips:
        fpath = c['filepath']
        fname = c['filename']
        source = c['source']
        
        # Determine unique video identifier
        # baseline: e.g. squat_01, squat_02
        # batch2: e.g. squat_b2_01, squat_b2_02
        m_base = re.match(rf'^{exercise}_(\w+)_clip\d+\.json$', fname)
        m_b2   = re.match(rf'^{exercise}_b2_(\w+)_clip\d+\.json$', fname)
        
        if source == 'baseline' and m_base:
            vid_id = f"{exercise}_{m_base.group(1)}"
        elif source == 'batch2' and m_b2:
            vid_id = f"{exercise}_b2_{m_b2.group(1)}"
        else:
            # Fallback
            parts = fname[:-5].split('_')
            vid_id = f"{exercise}_{source}_{parts[-2]}"
            
        unique_vids.add(vid_id)

        with open(fpath, 'r') as jf:
            cdata = json.load(jf)
            landmarks = cdata['landmarks']

        feat = extract_features(landmarks)
        assert feat.shape == (50,), f"Expected 50 features, got {feat.shape} on {fname}"
        assert not np.isnan(feat).any(), f"NaN found in features on {fname}"
        assert not np.isinf(feat).any(), f"Inf found in features on {fname}"

        feature_list.append(feat)
        merged_data.append({
            'exercise': exercise,
            'video_id': vid_id,
            'source': source,
            'filename': fname,
            'features': feat.tolist()
        })

    summary_table.append({
        'exercise': exercise,
        'total_clips': len(clips),
        'unique_videos': len(unique_vids)
    })
    print(f"[{exercise:<15}] {len(clips):2d} clips across {len(unique_vids):2d} unique videos (Features computed: 50 dims)")

# 4. Save merged dataset
with open(OUT_MERGED_FILE, 'w') as f:
    json.dump(merged_data, f)
print(f"\nMerged dataset saved to: {OUT_MERGED_FILE} ({len(merged_data)} total samples)")

# 5. Required output format
print("\n" + "=" * 70)
print("PHASE 6 REQUIRED OUTPUT TABLE")
print("=" * 70)
print(f"| {'Exercise':<15} | {'Total Clips':<15} | {'Total Unique Videos':<22} |")
print(f"|{'-'*17}|{'-'*17}|{'-'*24}|")

for row in summary_table:
    print(f"| {row['exercise']:<15} | {row['total_clips']:<15} | {row['unique_videos']:<22} |")
