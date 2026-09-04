"""
BioMechAI Backlog Extraction — PHASE 4 of 5
- Full landmark extraction for remaining 5 exercises: bicep_curl, high_knees, jumping_jack, plank, pushup
- Candidates source: backlog_clean_deduped_candidates.json
- Duration-aware clip count: max(3, min(15, round(duration_seconds / 90)))
- 90 frames per clip (3 seconds at 30 FPS)
- Motion filter: 20% of v3 class median per exercise
- Saves extracted clips in data/landmarks_backlog/{exercise}/
- Logs extraction metrics in backlog_phase4_extraction_log.json
"""
import os, sys, json, cv2, warnings
warnings.filterwarnings('ignore')

import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
CANDIDATES_FILE = os.path.join(BASE_DIR, 'backlog_clean_deduped_candidates.json')
OUT_LM_DIR      = os.path.join(BASE_DIR, 'data', 'landmarks_backlog')
LOG_OUT_FILE    = os.path.join(BASE_DIR, 'backlog_phase4_extraction_log.json')
MODEL_PATH      = os.path.join(BASE_DIR, 'pose_landmarker_lite.task')

if not os.path.exists(CANDIDATES_FILE):
    print("ERROR: backlog_clean_deduped_candidates.json from Phase 1 is missing!")
    sys.exit(1)

with open(CANDIDATES_FILE, 'r') as f:
    cand_data = json.load(f)

EXERCISES_P4 = ['bicep_curl', 'high_knees', 'jumping_jack', 'plank', 'pushup']

THRESHOLDS = {
    'bicep_curl': 0.0017986392884140837,
    'high_knees': 0.003117979691455129,
    'jumping_jack': 0.003853549991256588,
    'plank': 0.0009178165969680682,
    'pushup': 0.001563309412493966
}

FRAMES_PER_CLIP = 90

def clip_count_for_duration(duration_seconds):
    return max(3, min(15, round(duration_seconds / 90.0)))

def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    diffs = np.diff(lm, axis=0)
    disp = np.linalg.norm(diffs, axis=2)
    return float(disp.mean())

def extract_clip_landmarks(cap, start_frame, frames_count=90, fps=30.0):
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False,
        running_mode=vision.RunningMode.VIDEO
    )
    
    clip_landmarks = []
    with vision.PoseLandmarker.create_from_options(options) as landmarker:
        for f_idx in range(frames_count):
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            timestamp_ms = int((f_idx * 1000) / fps)
            result = landmarker.detect_for_video(mp_image, timestamp_ms)
            
            if result.pose_landmarks and len(result.pose_landmarks) > 0:
                lms = [[lm.x, lm.y, lm.z] for lm in result.pose_landmarks[0]]
                clip_landmarks.append(lms)
            else:
                if clip_landmarks:
                    clip_landmarks.append(clip_landmarks[-1])
                else:
                    clip_landmarks.append([[0.0, 0.0, 0.0] for _ in range(33)])

    return clip_landmarks

print("Starting Phase 4 Landmark Extraction for remaining 5 exercises...\n")

extraction_results = {}
summary_totals = {}

for ex in EXERCISES_P4:
    ex_out_dir = os.path.join(OUT_LM_DIR, ex)
    os.makedirs(ex_out_dir, exist_ok=True)
    
    candidates = cand_data[ex]['unique_candidates']
    thresh = THRESHOLDS[ex]
    print(f"=== Processing {ex.upper()} ({len(candidates)} candidate videos, threshold={thresh:.6f}) ===")
    
    video_logs = []
    total_clips_extracted = 0
    total_clips_discarded = 0
    
    for idx, cand in enumerate(candidates, 1):
        v_file = cand['filename']
        v_path = cand['filepath']
        stem = v_file.replace('.mp4', '')
        
        cap = cv2.VideoCapture(v_path)
        if not cap.isOpened():
            print(f"  [{idx}/{len(candidates)}] {v_file}: Failed to open video!")
            continue
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        if fps <= 0 or fps > 120:
            fps = 30.0
        duration_s = total_frames / fps if total_frames > 0 else 0.0
        
        target_clips = clip_count_for_duration(duration_s)
        
        # Calculate start frames
        if total_frames < FRAMES_PER_CLIP:
            start_frames = [0]
            target_clips = 1
        else:
            step = (total_frames - FRAMES_PER_CLIP) // target_clips if target_clips > 1 else 0
            start_frames = [i * step for i in range(target_clips)]
            
        v_extracted = 0
        v_discarded = 0
        
        for c_idx, start_f in enumerate(start_frames):
            clip_lms = extract_clip_landmarks(cap, start_f, frames_count=FRAMES_PER_CLIP, fps=fps)
            if len(clip_lms) < FRAMES_PER_CLIP:
                while len(clip_lms) < FRAMES_PER_CLIP:
                    clip_lms.append(clip_lms[-1] if clip_lms else [[0.0, 0.0, 0.0] for _ in range(33)])
            
            motion_val = overall_motion(clip_lms)
            
            if motion_val >= thresh:
                v_extracted += 1
                clip_fname = f"{stem}_clip{c_idx:02d}.json"
                clip_out_path = os.path.join(ex_out_dir, clip_fname)
                with open(clip_out_path, 'w') as f:
                    json.dump({
                        'exercise': ex,
                        'video_id': stem,
                        'clip_index': c_idx,
                        'landmarks': clip_lms,
                        'frames': len(clip_lms),
                        'motion': motion_val
                    }, f)
            else:
                v_discarded += 1
                
        cap.release()
        
        total_clips_extracted += v_extracted
        total_clips_discarded += v_discarded
        
        v_log = {
            'filename': v_file,
            'duration_seconds': round(duration_s, 2),
            'target_clips': target_clips,
            'clips_extracted': v_extracted,
            'clips_discarded': v_discarded
        }
        video_logs.append(v_log)
        
        if idx % 15 == 0 or idx == len(candidates):
            print(f"  Processed {idx}/{len(candidates)} videos (Extracted: {total_clips_extracted}, Discarded: {total_clips_discarded})...")
            
    extraction_results[ex] = video_logs
    summary_totals[ex] = {
        'candidates_processed': len(video_logs),
        'total_clips_extracted': total_clips_extracted,
        'total_clips_discarded': total_clips_discarded
    }
    print(f"Done {ex}: {len(video_logs)} videos -> {total_clips_extracted} clips accepted, {total_clips_discarded} clips discarded.\n")

# Save extraction log
with open(LOG_OUT_FILE, 'w') as f:
    json.dump({
        'summary': summary_totals,
        'details': extraction_results
    }, f, indent=2)

print(f"Extraction log saved to: {LOG_OUT_FILE}\n")

# Print Summary Totals
print("=" * 90)
print("PHASE 4 REQUIRED OUTPUT: PER-EXERCISE TOTALS")
print("=" * 90)
print(f"| {'Exercise':<15} | {'Candidates Processed':<22} | {'Total Clips Extracted':<23} | {'Total Clips Discarded':<23} |")
print(f"|{'-'*17}|{'-'*24}|{'-'*25}|{'-'*25}|")
for ex in EXERCISES_P4:
    tot = summary_totals[ex]
    print(f"| {ex:<15} | {tot['candidates_processed']:>20d}   | {tot['total_clips_extracted']:>21d}   | {tot['total_clips_discarded']:>21d}   |")

tot_proc = sum(s['candidates_processed'] for s in summary_totals.values())
tot_ext = sum(s['total_clips_extracted'] for s in summary_totals.values())
tot_disc = sum(s['total_clips_discarded'] for s in summary_totals.values())

print(f"|{'-'*17}|{'-'*24}|{'-'*25}|{'-'*25}|")
print(f"| {'TOTAL':<15} | {tot_proc:>20d}   | {tot_ext:>21d}   | {tot_disc:>21d}   |")
