"""
BioMechAI - Incremental Batch Expansion & Landmark Extraction Pipeline (Phase v7)
- Downloads targeted exercise videos safely in modular batches (High Knees, Jumping Jacks, Squats).
- Extracts 17 COCO spatiotemporal landmarks using MediaPipe PoseLandmarker.
- Filters out occluded / corrupted frames and packages clips into PoseC3D MMAction2 format.
- Strictly protects production files.
"""

import os
import sys
import glob
import json
import pickle
import argparse
import numpy as np
import cv2

# Set base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_B3_DIR = os.path.join(BASE_DIR, 'data', 'raw_videos_batch3')
EXTRACTED_PKL = os.path.join(BASE_DIR, 'data', 'batch3_extracted_clips.pkl')
MODEL_ASSET = os.path.join(BASE_DIR, 'tools_and_utilities', 'pose_landmarker_lite.task')

TARGET_EXERCISES = ['squat', 'high_knees', 'jumping_jack']

LABEL_MAP = {
    'bicep_curl': 0,
    'high_knees': 1,
    'jumping_jack': 2,
    'lunge': 3,
    'plank': 4,
    'pushup': 5,
    'squat': 6
}

# 17 COCO landmarks mapped from 33 MediaPipe landmarks
COCO_MP_MAP = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

SEARCH_QUERIES = {
    'squat': [
        'bodyweight squat exercise form demonstration',
        'how to do squats proper form tutorial',
        'perfect squat reps home workout front view',
        'squats workout full body visible demonstration',
        'air squat exercise tutorial proper technique',
        'squat reps exercise side angle view'
    ],
    'high_knees': [
        'high knees exercise proper form tutorial',
        'how to do high knees correctly home workout',
        'high knees cardio exercise demonstration',
        'high knee running in place full body workout',
        'high knees exercise technique fitness guide',
        'high knees reps cardio drill front view'
    ],
    'jumping_jack': [
        'jumping jacks exercise proper form tutorial',
        'how to do jumping jacks correctly full body',
        'jumping jack cardio exercise demonstration',
        'jumping jacks reps workout fitness guide',
        'jumping jacks technique demonstration workout',
        'standard jumping jacks cardio exercise'
    ]
}

def ensure_dirs():
    os.makedirs(RAW_B3_DIR, exist_ok=True)
    for ex in TARGET_EXERCISES:
        os.makedirs(os.path.join(RAW_B3_DIR, ex), exist_ok=True)

def download_batch(per_exercise_count=15):
    """Downloads a batch of videos for targeted exercises without requiring ffmpeg."""
    import yt_dlp
    ensure_dirs()
    print("=" * 65)
    print(f"BATCH DOWNLOAD INITIATED: {per_exercise_count} videos per exercise")
    print("=" * 65)

    for ex in TARGET_EXERCISES:
        out_dir = os.path.join(RAW_B3_DIR, ex)
        existing = glob.glob(os.path.join(out_dir, "*.mp4"))
        print(f"\n[TARGET: {ex.upper()}] Existing videos: {len(existing)}")
        
        queries = SEARCH_QUERIES.get(ex, [])
        vids_downloaded = 0
        
        for q in queries:
            if vids_downloaded >= per_exercise_count:
                break
            needed = per_exercise_count - vids_downloaded
            search_str = f"ytsearch{min(needed, 5)}:{q}"
            
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]/bestvideo/best',
                'outtmpl': os.path.join(out_dir, f"{ex}_b3_%(id)s.%(ext)s"),
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'max_downloads': needed
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([search_str])
            except Exception as e:
                print(f"   Notice during query '{q}': {e}")
            
            current_total = len(glob.glob(os.path.join(out_dir, "*.mp4")))
            vids_downloaded = current_total - len(existing)
            print(f"   Query '{q}' finished -> Total downloaded for {ex}: {vids_downloaded}/{per_exercise_count}")

def extract_landmarks_from_video(video_path, exercise_name):
    """
    Extracts 90-frame clips evenly spaced across exercise duration.
    Instantiates a fresh MediaPipe session per video to guarantee monotonic timestamps.
    """
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    
    # Must have at least 150 frames (~5-6 seconds)
    if total_frames < 150:
        cap.release()
        return []

    base_options = python.BaseOptions(model_asset_path=MODEL_ASSET)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False,
        running_mode=vision.RunningMode.VIDEO
    )

    # Distribute 4 clip starting positions across 15% to 80% of video duration (skipping intro/outro)
    start_ratio_range = (0.15, 0.80)
    start_frame_min = int(total_frames * start_ratio_range[0])
    start_frame_max = max(start_frame_min + 90, int(total_frames * start_ratio_range[1]) - 90)
    
    num_sample_clips = 4
    if start_frame_max > start_frame_min:
        sample_starts = np.linspace(start_frame_min, start_frame_max, num_sample_clips, dtype=int)
    else:
        sample_starts = [start_frame_min]

    clips = []
    vid_basename = os.path.splitext(os.path.basename(video_path))[0]
    clip_idx = 1
    
    # Process with fresh landmarker
    try:
        with vision.PoseLandmarker.create_from_options(options) as landmarker:
            for s_frame in sample_starts:
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(s_frame))
                clip_kps = []
                clip_scores = []
                valid_pose_count = 0
                
                for f_rel in range(90):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                    # Timestamp relative to clip start (monotonic within this clip)
                    t_ms = int(f_rel * 1000 / fps)
                    
                    try:
                        res = landmarker.detect_for_video(mp_img, t_ms)
                        if res.pose_landmarks and len(res.pose_landmarks) > 0:
                            lms = res.pose_landmarks[0]
                            kps = []
                            scs = []
                            for p_idx in COCO_MP_MAP:
                                lm = lms[p_idx]
                                kps.append([lm.x * 1000.0, lm.y * 1000.0])
                                scs.append(getattr(lm, 'visibility', 0.9))
                            clip_kps.append(kps)
                            clip_scores.append(scs)
                            valid_pose_count += 1
                        else:
                            if clip_kps:
                                clip_kps.append(clip_kps[-1])
                                clip_scores.append([s * 0.5 for s in clip_scores[-1]])
                            else:
                                clip_kps.append([[500.0, 500.0]] * 17)
                                clip_scores.append([0.0] * 17)
                    except Exception:
                        pass
                        
                # QA filtering: Must have valid human pose in at least 60 of the 90 frames (67%)
                # and standard deviation of joint positions > 5.0 (real movement, not static image)
                if len(clip_kps) == 90 and valid_pose_count >= 60:
                    arr_kp = np.array(clip_kps, dtype=np.float32)
                    if np.std(arr_kp) >= 5.0:
                        arr_sc = np.array(clip_scores, dtype=np.float32)
                        clip_dict = {
                            'frame_dir': f"{vid_basename}_clip{clip_idx:02d}",
                            'video_id': vid_basename,
                            'label': LABEL_MAP[exercise_name],
                            'exercise': exercise_name,
                            'img_shape': (1000, 1000),
                            'original_shape': (1000, 1000),
                            'total_frames': 90,
                            'num_clips': 1,
                            'keypoint': np.expand_dims(arr_kp, axis=0),
                            'keypoint_score': np.expand_dims(arr_sc, axis=0)
                        }
                        clips.append(clip_dict)
                        clip_idx += 1
    except Exception as e:
        pass
        
    cap.release()
    return clips

def extract_all():
    """Runs landmark extraction across all videos in raw_videos_batch3."""
    ensure_dirs()
    print("=" * 65)
    print("LANDMARK EXTRACTION & QA FILTERING (BATCH 3)")
    print("=" * 65)
    
    if not os.path.exists(MODEL_ASSET):
        print(f"[ERROR] Model asset not found at {MODEL_ASSET}")
        return
        
    accumulated_clips = []
    if os.path.exists(EXTRACTED_PKL):
        try:
            with open(EXTRACTED_PKL, 'rb') as f:
                accumulated_clips = pickle.load(f)
            print(f"Loaded existing pool of {len(accumulated_clips)} clips from {EXTRACTED_PKL}")
        except Exception:
            accumulated_clips = []
            
    processed_video_ids = set(x['video_id'] for x in accumulated_clips)
    new_clips_total = 0
    
    for ex in TARGET_EXERCISES:
        ex_dir = os.path.join(RAW_B3_DIR, ex)
        mp4_files = sorted(glob.glob(os.path.join(ex_dir, "*.mp4")))
        print(f"\nProcessing {ex.upper()} ({len(mp4_files)} files on disk)...")
        
        ex_clips = 0
        for vid_f in mp4_files:
            v_id = os.path.splitext(os.path.basename(vid_f))[0]
            if v_id in processed_video_ids:
                continue
                
            clips = extract_landmarks_from_video(vid_f, ex)
            if clips:
                accumulated_clips.extend(clips)
                processed_video_ids.add(v_id)
                ex_clips += len(clips)
                new_clips_total += len(clips)
                print(f"   [+ {len(clips):2d} clips] {os.path.basename(vid_f)}")
                
        print(f"-> Extracted {ex_clips} new clips for {ex}")
        
    with open(EXTRACTED_PKL, 'wb') as f:
        pickle.dump(accumulated_clips, f)
        
    print("\n" + "=" * 65)
    print(f"[SUCCESS] BATCH 3 EXTRACTION COMPLETE!")
    print(f"   New clips added in this run:  {new_clips_total}")
    print(f"   Total clips in Batch 3 pool:  {len(accumulated_clips)}")
    print(f"   Saved to: {EXTRACTED_PKL}")
    print("=" * 65)

def print_status():
    """Prints current inventory of Batch 3 videos and extracted clips."""
    ensure_dirs()
    print("=" * 65)
    print("BATCH 3 DATASET EXPANSION INVENTORY")
    print("=" * 65)
    for ex in TARGET_EXERCISES:
        ex_dir = os.path.join(RAW_B3_DIR, ex)
        count = len(glob.glob(os.path.join(ex_dir, "*.mp4")))
        print(f"   * {ex:<15}: {count} raw videos")
        
    if os.path.exists(EXTRACTED_PKL):
        with open(EXTRACTED_PKL, 'rb') as f:
            clips = pickle.load(f)
        from collections import Counter
        counts = Counter(x['exercise'] for x in clips)
        print("\nExtracted Batch 3 Clips in Pool:")
        for ex in TARGET_EXERCISES:
            print(f"   * {ex:<15}: {counts.get(ex, 0)} clips")
        print(f"Total Extracted Clips: {len(clips)}")
    else:
        print("\nNo extracted clips yet. Run --extract after downloading.")
    print("=" * 65)

def merge_and_export_v7():
    """Merges Batch 3 with baseline dataset, applies zero-leakage split, and exports v7 pickles."""
    baseline_train_path = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'posec3d_data', 'Files to upload to kaggle', 'custom_dataset_train.pkl')
    baseline_val_path = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'posec3d_data', 'Files to upload to kaggle', 'custom_dataset_val.pkl')
    
    out_dir = os.path.join(BASE_DIR, 'model_training', 'experiments_v7_expansion')
    os.makedirs(out_dir, exist_ok=True)
    
    if not os.path.exists(EXTRACTED_PKL):
        print(f"[ERROR] {EXTRACTED_PKL} not found. Run --extract first.")
        return
        
    with open(EXTRACTED_PKL, 'rb') as f:
        b3_clips = pickle.load(f)
        
    with open(baseline_train_path, 'rb') as f:
        base_train = pickle.load(f)
        
    with open(baseline_val_path, 'rb') as f:
        base_val = pickle.load(f)
        
    print(f"Baseline Train Clips: {len(base_train)}")
    print(f"Baseline Val Clips:   {len(base_val)}")
    print(f"Batch 3 New Clips:    {len(b3_clips)}")
    
    # Split Batch 3 using 80/20 video-disjoint GroupKFold
    b3_vids = np.array([x['video_id'] for x in b3_clips])
    unique_vids = np.unique(b3_vids)
    
    # Deterministic split: 80% train, 20% val
    rng = np.random.RandomState(42)
    shuffled_vids = unique_vids.copy()
    rng.shuffle(shuffled_vids)
    
    split_idx = int(0.8 * len(shuffled_vids))
    train_vids_set = set(shuffled_vids[:split_idx])
    val_vids_set = set(shuffled_vids[split_idx:])
    
    b3_train = [x for x in b3_clips if x['video_id'] in train_vids_set]
    b3_val = [x for x in b3_clips if x['video_id'] in val_vids_set]
    
    final_train = base_train + b3_train
    final_val = base_val + b3_val
    
    # Export v7 pickles
    out_train_path = os.path.join(out_dir, 'custom_dataset_train_v7.pkl')
    out_val_path = os.path.join(out_dir, 'custom_dataset_val_v7.pkl')
    
    with open(out_train_path, 'wb') as f:
        pickle.dump(final_train, f)
    with open(out_val_path, 'wb') as f:
        pickle.dump(final_val, f)
        
    print("\n" + "=" * 65)
    print("[SUCCESS] PHASE v7 DATASET CONSOLIDATION COMPLETE (ZERO LEAKAGE)!")
    print("=" * 65)
    print(f"Total v7 Training Clips:   {len(final_train):5d}  ({os.path.getsize(out_train_path)/1024**2:.2f} MB)")
    print(f"Total v7 Validation Clips: {len(final_val):5d}  ({os.path.getsize(out_val_path)/1024**2:.2f} MB)")
    print(f"Saved to: {out_dir}")
    print("=" * 65)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="BioMechAI Incremental Dataset Expansion")
    parser.add_argument('--download', action='store_true', help="Download batch of videos")
    parser.add_argument('--count', type=int, default=15, help="Number of videos per exercise to download")
    parser.add_argument('--extract', action='store_true', help="Extract landmarks from Batch 3 videos")
    parser.add_argument('--status', action='store_true', help="Show Batch 3 status")
    parser.add_argument('--merge-v7', action='store_true', help="Consolidate and export v7 training datasets")
    
    args = parser.parse_args()
    
    if args.download:
        download_batch(args.count)
    elif args.extract:
        extract_all()
    elif args.merge_v7:
        merge_and_export_v7()
    else:
        print_status()
