"""
Check whether squat and lunge training videos are predominantly frontal-camera shots
(which would explain the persistent squat<->lunge confusion across every RF experiment
so far -- see notes above this script).

Heuristic: shoulder-width / torso-height ratio, per video (averaged across its clips).
  - Frontal view: shoulders spread wide in x relative to torso height -> HIGH ratio
  - Side/profile view: shoulders nearly overlap in x (one behind the other from camera's
    perspective) -> LOW ratio

This is read-only. Does not modify anything.
"""
import os
import json
import numpy as np

BASE_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
LM_DIR = os.path.join(BASE_DIR, 'data', 'landmarks')
LM_BATCH2_DIR = os.path.join(BASE_DIR, 'data', 'landmarks_batch2')
LM_BACKLOG_DIR = os.path.join(BASE_DIR, 'data', 'landmarks_backlog')

# MediaPipe landmark indices
L_SHOULDER, R_SHOULDER = 11, 12
L_HIP, R_HIP = 23, 24

def shoulder_width_torso_ratio(landmarks):
    lm = np.array(landmarks)
    shoulder_width = np.abs(lm[:, L_SHOULDER, 0] - lm[:, R_SHOULDER, 0])
    shoulder_y = (lm[:, L_SHOULDER, 1] + lm[:, R_SHOULDER, 1]) / 2
    hip_y = (lm[:, L_HIP, 1] + lm[:, R_HIP, 1]) / 2
    torso_height = np.abs(hip_y - shoulder_y)
    torso_height = np.where(torso_height < 1e-6, 1e-6, torso_height)  # avoid div by zero
    ratio = shoulder_width / torso_height
    return float(np.mean(ratio))

def scan_exercise(exercise, base_dirs):
    video_clips = {}
    for base in base_dirs:
        ex_path = os.path.join(base, exercise)
        if not os.path.isdir(ex_path):
            continue
        for f in os.listdir(ex_path):
            if not f.endswith('.json'):
                continue
            parts = f.rsplit('_clip', 1)
            if len(parts) != 2:
                video_id = f.replace('.json', '')
            else:
                video_id = parts[0]
            with open(os.path.join(ex_path, f)) as fh:
                data = json.load(fh)
            ratio = shoulder_width_torso_ratio(data['landmarks'])
            video_clips.setdefault(video_id, []).append(ratio)

    results = []
    for video_id, ratios in video_clips.items():
        results.append((video_id, float(np.mean(ratios)), len(ratios)))
    return results

for exercise in ['squat', 'lunge', 'pushup', 'plank']:  # pushup/plank included as a control comparison
    results = scan_exercise(exercise, [LM_DIR, LM_BATCH2_DIR, LM_BACKLOG_DIR])
    if not results:
        print(f"{exercise}: no landmark files found (check paths)")
        continue
    ratios = [r[1] for r in results]
    ratios_sorted = sorted(results, key=lambda x: x[1])

    print(f"\n=== {exercise.upper()} ({len(results)} unique videos) ===")
    print(f"  Mean ratio: {np.mean(ratios):.3f}  |  Median: {np.median(ratios):.3f}  |  "
          f"Min: {min(ratios):.3f}  |  Max: {max(ratios):.3f}")

    # Rough bucketing -- thresholds are a starting heuristic, not calibrated ground truth
    likely_side = [r for r in results if r[1] < 0.3]
    likely_oblique = [r for r in results if 0.3 <= r[1] < 0.6]
    likely_frontal = [r for r in results if r[1] >= 0.6]
    print(f"  Likely SIDE/profile (<0.3):    {len(likely_side):2d}/{len(results)} "
          f"({100*len(likely_side)/len(results):5.1f}%)")
    print(f"  Likely OBLIQUE (0.3-0.6):      {len(likely_oblique):2d}/{len(results)} "
          f"({100*len(likely_oblique)/len(results):5.1f}%)")
    print(f"  Likely FRONTAL (>=0.6):        {len(likely_frontal):2d}/{len(results)} "
          f"({100*len(likely_frontal)/len(results):5.1f}%)")
    print(f"  5 lowest-ratio (most side-on) videos: {[r[0] for r in ratios_sorted[:5]]}")
    print(f"  5 highest-ratio (most frontal) videos: {[r[0] for r in ratios_sorted[-5:]]}")
