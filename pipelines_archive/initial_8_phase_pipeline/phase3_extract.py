"""
Phase 3 of 8 — Extract landmarks from candidate videos in data/raw_videos_batch2/
- MediaPipe PoseLandmarker (pose_landmarker_lite.task)
- Extracts 5 clips of 90 frames evenly distributed across each video
- Mandatory motion-sanity filter: computes baseline median motion per exercise from data/landmarks/
  and discards any clip below 20% of that median.
- Saves valid clips to data/landmarks_batch2/{exercise}/
"""
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os, sys, json

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
RAW_BATCH2_DIR  = os.path.join(BASE_DIR, 'data', 'raw_videos_batch2')
LANDMARKS_B2    = os.path.join(BASE_DIR, 'data', 'landmarks_batch2')
ORIG_LANDMARKS  = os.path.join(BASE_DIR, 'data', 'landmarks')
MODEL_ASSET     = os.path.join(BASE_DIR, 'pose_landmarker_lite.task')
LOG_FILE        = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'phase3_extraction_log.json')

EXERCISES = ['squat', 'pushup', 'jumping_jack', 'bicep_curl', 'lunge', 'plank', 'high_knees']
ORDER     = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']

FRAMES_PER_CLIP = 90
CLIPS_PER_VIDEO = 5

def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    diffs = np.diff(lm, axis=0)
    disp = np.linalg.norm(diffs, axis=2)
    return float(disp.mean())

# ---------------------------------------------------------------------------
# Step 1: Compute baseline motion medians from existing data/landmarks/
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 1: Calculating baseline motion medians from data/landmarks/")
print("=" * 60)

baseline_medians = {}
baseline_thresholds = {}

for ex in EXERCISES:
    ex_dir = os.path.join(ORIG_LANDMARKS, ex)
    motions = []
    if os.path.isdir(ex_dir):
        for fname in sorted(os.listdir(ex_dir)):
            if fname.endswith('.json'):
                fpath = os.path.join(ex_dir, fname)
                try:
                    with open(fpath, 'r') as f:
                        data = json.load(f)
                    lm = data.get('landmarks')
                    if lm and len(lm) >= 90:
                        m = overall_motion(lm)
                        motions.append(m)
                except Exception:
                    pass
    if motions:
        med = float(np.median(motions))
        thresh = 0.20 * med
    else:
        med = 0.005
        thresh = 0.001
    baseline_medians[ex] = med
    baseline_thresholds[ex] = thresh
    print(f"  {ex:<15}: median motion = {med:.5f} | 20% filter threshold = {thresh:.5f} (from {len(motions)} clips)")

# ---------------------------------------------------------------------------
# Step 2: Per-clip Landmark Extraction
# ---------------------------------------------------------------------------
base_options = python.BaseOptions(model_asset_path=MODEL_ASSET)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=False,
    running_mode=vision.RunningMode.VIDEO
)

def extract_5_clips_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    if total_frames < FRAMES_PER_CLIP:
        cap.release()
        return None

    step = (total_frames - FRAMES_PER_CLIP) // CLIPS_PER_VIDEO
    clips = []

    for i in range(CLIPS_PER_VIDEO):
        start_frame = i * step
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        clip_landmarks = []
        with vision.PoseLandmarker.create_from_options(options) as lm:
            for frame_idx in range(FRAMES_PER_CLIP):
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                timestamp_ms = int((frame_idx * 1000) / 30.0)
                
                try:
                    result = lm.detect_for_video(mp_image, timestamp_ms)
                    if result.pose_landmarks and len(result.pose_landmarks) > 0:
                        lms = [[p.x, p.y, p.z] for p in result.pose_landmarks[0]]
                        clip_landmarks.append(lms)
                    else:
                        if clip_landmarks:
                            clip_landmarks.append(clip_landmarks[-1])
                        else:
                            clip_landmarks.append([[0.0, 0.0, 0.0] for _ in range(33)])
                except Exception:
                    if clip_landmarks:
                        clip_landmarks.append(clip_landmarks[-1])
                    else:
                        clip_landmarks.append([[0.0, 0.0, 0.0] for _ in range(33)])

        if len(clip_landmarks) == FRAMES_PER_CLIP:
            clips.append(clip_landmarks)

    cap.release()
    return clips

# ---------------------------------------------------------------------------
# Step 3: Process batch2 videos with motion filtering
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Step 2: Extracting landmarks from raw_videos_batch2/ with motion filtering")
print("=" * 60)

summary_results = {}

for exercise in ORDER:
    raw_dir = os.path.join(RAW_BATCH2_DIR, exercise)
    out_dir = os.path.join(LANDMARKS_B2, exercise)
    os.makedirs(out_dir, exist_ok=True)

    med = baseline_medians[exercise]
    thresh = baseline_thresholds[exercise]

    if not os.path.exists(raw_dir):
        print(f"No folder for {exercise}")
        continue

    video_files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.mp4')])
    print(f"\nProcessing {exercise}: {len(video_files)} videos (Threshold: {thresh:.5f})")

    extracted_clips = []
    skipped_clips = []

    for vidx, vfile in enumerate(video_files):
        vpath = os.path.join(raw_dir, vfile)
        vbase = os.path.splitext(vfile)[0]

        try:
            clips = extract_5_clips_from_video(vpath)

            if not clips:
                skipped_clips.append({
                    'video': vfile,
                    'clip_filename': 'N/A',
                    'clip_index': -1,
                    'reason': 'insufficient frames (< 90 frames)',
                    'motion': 0.0
                })
                continue

            for j, clip in enumerate(clips):
                clip_motion = overall_motion(clip)
                clip_fname = f"{vbase}_clip{j:02d}.json"
                clip_fpath = os.path.join(out_dir, clip_fname)

                if clip_motion >= thresh:
                    with open(clip_fpath, 'w') as f:
                        json.dump({
                            'exercise': exercise,
                            'landmarks': clip,
                            'frames': len(clip),
                            'motion': clip_motion
                        }, f)
                    extracted_clips.append({
                        'video': vfile,
                        'clip_filename': clip_fname,
                        'clip_index': j,
                        'motion': clip_motion
                    })
                else:
                    pct = (clip_motion / med) * 100 if med > 0 else 0
                    skipped_clips.append({
                        'video': vfile,
                        'clip_filename': clip_fname,
                        'clip_index': j,
                        'motion': clip_motion,
                        'reason': f'motion {clip_motion:.5f} ({pct:.1f}% of median) < 20% threshold {thresh:.5f}'
                    })

            print(f"  [{vidx+1}/{len(video_files)}] {vfile}: {len(clips)} clips evaluated")

        except Exception as e:
            print(f"  Error on {vfile}: {e}")
            skipped_clips.append({
                'video': vfile,
                'clip_filename': 'N/A',
                'clip_index': -1,
                'reason': f'extraction error: {str(e)}',
                'motion': 0.0
            })

    summary_results[exercise] = {
        'videos_processed': len(video_files),
        'clips_extracted': len(extracted_clips),
        'clips_skipped': len(skipped_clips),
        'median_motion': med,
        'threshold': thresh,
        'extracted_list': extracted_clips,
        'skipped_list': skipped_clips
    }
    print(f"  -> {exercise}: {len(extracted_clips)} clips extracted, {len(skipped_clips)} clips skipped by motion filter")

# Save log
with open(LOG_FILE, 'w') as f:
    json.dump(summary_results, f, indent=2)
print("\nExtraction log saved to:", LOG_FILE)

# ---------------------------------------------------------------------------
# Step 4: Print required output table
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 3 REQUIRED OUTPUT TABLE")
print("=" * 70)
print(f"| {'Exercise':<15} | {'Videos Processed':<18} | {'Clips Extracted':<16} | {'Clips Skipped (Motion Filter)':<35} |")
print(f"|{'-'*17}|{'-'*20}|{'-'*18}|{'-'*37}|")

for ex in ORDER:
    res = summary_results.get(ex, {})
    v_proc = res.get('videos_processed', 0)
    c_ext  = res.get('clips_extracted', 0)
    c_skip = res.get('clips_skipped', 0)
    med    = res.get('median_motion', 0.0)
    thresh = res.get('threshold', 0.0)
    skip_reason = f"{c_skip} skipped (<20% of med {med:.5f})" if c_skip > 0 else "0 skipped"
    print(f"| {ex:<15} | {v_proc:<18} | {c_ext:<16} | {skip_reason:<35} |")
