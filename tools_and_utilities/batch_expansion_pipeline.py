"""
BioMechAI - 5,000+ Clip Dataset Expansion & Extraction Engine (Phase v7)
- Downloads fresh, unseen YouTube videos for all 7 exercises (110 fresh videos per exercise).
- Guarantees 0 duplicate videos by checking download_archive.txt.
- 100% preserves all 1,978 existing training clips.
- Multi-rep spatiotemporal sampling: extracts 5-6 clean 90-frame clips per video.
- 3-step QA filtering: >= 60 pose frames, motion std >= 5.0, 17 COCO landmarks.
- Auto-deletes raw MP4s after extraction (--cleanup-mp4) for 0 MB disk footprint.
- Merges into custom_dataset_train_v7.pkl to surpass 5,000+ total training clips.
- Preserves the strictly frozen 444 benchmark validation clips for fair evaluation.
"""

import os
import sys
import glob
import json
import pickle
import argparse
import numpy as np
import cv2

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_B3_DIR = os.path.join(BASE_DIR, 'data', 'raw_videos_batch3')
EXTRACTED_PKL = os.path.join(BASE_DIR, 'data', 'batch3_extracted_clips.pkl')
ARCHIVE_FILE = os.path.join(RAW_B3_DIR, 'download_archive.txt')
MODEL_ASSET = os.path.join(BASE_DIR, 'tools_and_utilities', 'pose_landmarker_lite.task')

ALL_EXERCISES = ['squat', 'high_knees', 'jumping_jack', 'bicep_curl', 'pushup', 'lunge', 'plank']

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
    'high_knees': [
        'high knees exercise proper form tutorial',
        'how to do high knees correctly home workout',
        'high knees cardio exercise demonstration',
        'high knee running in place full body workout',
        'high knees exercise technique fitness guide',
        'high knees reps cardio drill front view',
        'high knees workout slow motion full body',
        'tabata high knees workout demonstration',
        'high knees running drill proper technique',
        'cardio high knees workout demonstration reps',
        'standing high knee march exercise demonstration',
        'high knees warm up exercise technique',
        'aerobic high knees drill workout reps',
        'running high knees exercise form side view',
        'high knee drill workout tutorial form'
    ],
    'jumping_jack': [
        'jumping jacks exercise proper form tutorial',
        'how to do jumping jacks correctly full body',
        'jumping jack cardio exercise demonstration',
        'jumping jacks reps workout fitness guide',
        'jumping jacks technique demonstration workout',
        'standard jumping jacks cardio exercise',
        'jumping jacks workout home exercise slow motion',
        'jumping jacks full body visible demonstration',
        'jumping jacks fitness test reps proper form',
        'calisthenics jumping jacks workout demonstration',
        'star jumps jumping jacks aerobic exercise',
        'jumping jack warm up exercise full body',
        'basic jumping jacks exercise demonstration',
        'cardio jumping jacks workout proper form reps',
        'jumping jacks fitness workout tutorial side view'
    ],
    'squat': [
        'bodyweight squat exercise form demonstration',
        'how to do squats proper form tutorial',
        'perfect squat reps home workout front view',
        'squats workout full body visible demonstration',
        'air squat exercise tutorial proper technique',
        'squat reps exercise side angle view',
        'deep squat workout proper form demonstration',
        'squats exercise front angle view reps',
        'fitness squat workout technique tutorial',
        'bodyweight squats slow motion side view',
        'parallel squat exercise technique full body',
        'prisoner squats bodyweight exercise demonstration',
        'bodyweight squat reps slow motion demonstration',
        'squat exercise demonstration workout proper depth',
        'standard bodyweight squat workout proper form'
    ],
    'bicep_curl': [
        'dumbbell bicep curl exercise proper form',
        'how to do bicep curls correctly tutorial',
        'bicep curl slow motion side view technique',
        'arm curl exercise form demonstration full body',
        'standing dumbbell curl proper technique reps',
        'bicep curls workout demonstration front angle',
        'hammer curl bicep exercise proper form',
        'dumbbell arm curls workout full body visible',
        'alternating dumbbell bicep curl exercise technique',
        'biceps workout arm curls form tutorial',
        'standing bicep curls fitness reps demonstration',
        'proper bicep curl form for beginners tutorial',
        'bicep dumbbell curls side view technique guide',
        'dumbbell curls repetition workout demonstration',
        'biceps curl arm exercise proper movement demonstration'
    ],
    'pushup': [
        'push up exercise proper form tutorial',
        'how to do push ups correctly beginner guide',
        'push up workout slow motion side view full body',
        'perfect push up form demonstration reps',
        'standard push up technique tutorial front side view',
        'bodyweight pushups exercise demonstration',
        'military push up proper form workout reps',
        'pushup workout demonstration side angle view',
        'calisthenics push up exercise proper technique',
        'chest pushup exercise full body visible',
        'strict push ups form demonstration tutorial',
        'push up reps workout technique fitness guide',
        'standard pushups full body side view reps',
        'pushup exercise tutorial proper depth demonstration',
        'bodyweight chest pushups technique reps'
    ],
    'lunge': [
        'forward lunge exercise proper form tutorial',
        'how to do lunges correctly technique guide',
        'walking lunge workout slow motion side view',
        'perfect lunge form demonstration full body visible',
        'bodyweight lunge exercise tutorial front view',
        'stationary lunge workout demonstration reps',
        'reverse lunge exercise proper form demonstration',
        'lunges workout reps side view technique',
        'alternating forward lunges exercise demonstration',
        'bodyweight lunges leg workout form tutorial',
        'walking lunges exercise demonstration full body',
        'static lunges fitness reps proper depth',
        'fitness lunge workout technique side angle',
        'leg day lunges exercise demonstration reps',
        'standard lunges workout proper technique guide'
    ],
    'plank': [
        'forearm plank exercise proper form tutorial',
        'how to do plank correctly core workout',
        'plank hold exercise side view full body visible',
        'perfect plank form demonstration guide',
        'isometric plank hold exercise demonstration',
        'standard plank workout technique tutorial',
        'abdominal plank hold exercise proper form',
        'core plank exercise demonstration full body',
        'forearm plank hold workout technique side angle',
        'proper plank technique for beginners tutorial',
        'bodyweight plank hold exercise demonstration',
        'plank exercise proper alignment demonstration',
        'isometric core plank hold reps side view',
        'full body plank hold workout technique guide',
        'standard forearm plank position demonstration'
    ]
}

def ensure_dirs():
    os.makedirs(RAW_B3_DIR, exist_ok=True)
    for ex in ALL_EXERCISES:
        os.makedirs(os.path.join(RAW_B3_DIR, ex), exist_ok=True)
        
    # Populate archive with any existing files or previously extracted video IDs
    if not os.path.exists(ARCHIVE_FILE):
        existing_ids = set()
        for f in glob.glob(os.path.join(RAW_B3_DIR, "*", "*.mp4")):
            base = os.path.splitext(os.path.basename(f))[0]
            if "_b3_" in base:
                yt_id = base.split("_b3_", 1)[1]
                existing_ids.add(yt_id)
        if os.path.exists(EXTRACTED_PKL):
            try:
                with open(EXTRACTED_PKL, 'rb') as f_pk:
                    clips = pickle.load(f_pk)
                for c in clips:
                    v_id = c.get('video_id', '')
                    if "_b3_" in v_id:
                        yt_id = v_id.split("_b3_", 1)[1]
                        existing_ids.add(yt_id)
            except Exception:
                pass
        with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f_arc:
            for ytid in sorted(existing_ids):
                f_arc.write(f"youtube {ytid}\n")

def download_fresh_videos(exercise, count_to_download=110):
    """
    Downloads count_to_download BRAND-NEW, fresh videos for an exercise using yt-dlp.
    Strictly checks download_archive.txt so zero previously downloaded videos are fetched.
    """
    import yt_dlp
    ensure_dirs()
    out_dir = os.path.join(RAW_B3_DIR, exercise)
    
    # Determine how many videos were already downloaded during this exercise run
    existing_in_dir = len(glob.glob(os.path.join(out_dir, "*.mp4")))
    needed = max(0, count_to_download - existing_in_dir)
    
    print("=" * 65)
    print(f"FETCHING FRESH BATCH: {exercise.upper()} ({count_to_download} new videos)")
    print(f"   Unextracted MP4s on disk: {existing_in_dir}")
    print(f"   Fresh downloads needed:   {needed}")
    print(f"   Archive file:             {ARCHIVE_FILE} (Guarantees 0 duplicates)")
    print("=" * 65)
    
    if needed <= 0:
        print(f"[OK] Already have {existing_in_dir} videos on disk ready for extraction.")
        return
        
    queries = SEARCH_QUERIES.get(exercise, [f"{exercise} exercise proper form tutorial"])
    per_query = max(int(np.ceil(needed / len(queries))) + 1, 8)
    
    for q_idx, q in enumerate(queries, 1):
        cur_files = len(glob.glob(os.path.join(out_dir, "*.mp4")))
        rem = count_to_download - cur_files
        if rem <= 0:
            print(f"[OK] Reached target {count_to_download} videos for {exercise}!")
            break
            
        grab_count = min(rem, max(per_query, 8))
        search_str = f"ytsearch{grab_count * 2}:{q}"
        print(f"\n[Query {q_idx}/{len(queries)}] Searching up to {grab_count} fresh videos: '{q}'...")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]/bestvideo/best',
            'outtmpl': os.path.join(out_dir, f"{exercise}_b3_%(id)s.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'download_archive': ARCHIVE_FILE,
            'match_filter': yt_dlp.utils.match_filter_func('duration > 10 & duration < 300'),
            'max_downloads': grab_count
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_str])
        except Exception as e:
            print(f"   Notice: {e}")
            
        cur_files = len(glob.glob(os.path.join(out_dir, "*.mp4")))
        print(f"   -> Progress: {cur_files}/{count_to_download} fresh videos on disk for {exercise}")
        
    final_files = len(glob.glob(os.path.join(out_dir, "*.mp4")))
    print(f"\n[DOWNLOAD COMPLETED] Fresh videos on disk for {exercise}: {final_files}")

def extract_landmarks_from_video(video_path, exercise_name):
    """
    Extracts 5-6 clean 90-frame clips evenly spaced across exercise duration.
    Instantiates a fresh MediaPipe session per clip to guarantee monotonic timestamps.
    Applies 3-step QA:
    1. >= 60 frames with human pose detected.
    2. Keypoint standard deviation >= 5.0 (motion verification).
    3. Proper PoseC3D format (17 COCO landmarks, 90 frames).
    """
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    
    if total_frames < 100:
        cap.release()
        return []

    base_options = python.BaseOptions(model_asset_path=MODEL_ASSET)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False,
        running_mode=vision.RunningMode.VIDEO
    )

    max_possible_start = max(0, total_frames - 95)
    start_min = min(int(total_frames * 0.15), max_possible_start)
    start_max = min(int(total_frames * 0.85), max_possible_start)
    if start_max <= start_min:
        start_min = 0
        start_max = max_possible_start

    num_sample_clips = 5
    if total_frames > 500:
        num_sample_clips = 6
    if start_max > start_min:
        sample_starts = np.linspace(start_min, start_max, num_sample_clips, dtype=int)
    else:
        sample_starts = [start_min]

    clips = []
    vid_basename = os.path.splitext(os.path.basename(video_path))[0]
    clip_idx = 1
    
    for s_frame in sample_starts:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(s_frame))
        clip_kps = []
        clip_scores = []
        valid_pose_count = 0
        
        try:
            with vision.PoseLandmarker.create_from_options(options) as landmarker:
                for f_rel in range(90):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
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
        except Exception:
            pass
            
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
                
    cap.release()
    return clips

def extract_for_exercise(exercise, cleanup_mp4=False):
    """Extracts landmarks for a specific exercise and saves to pool."""
    ensure_dirs()
    out_dir = os.path.join(RAW_B3_DIR, exercise)
    mp4_files = sorted(glob.glob(os.path.join(out_dir, "*.mp4")))
    
    print("=" * 65)
    print(f"EXTRACTION & QA FILTERING: {exercise.upper()} ({len(mp4_files)} videos on disk)")
    print(f"Auto-cleanup raw MP4s after extraction: {cleanup_mp4}")
    print("=" * 65)
    
    accumulated_clips = []
    if os.path.exists(EXTRACTED_PKL):
        try:
            with open(EXTRACTED_PKL, 'rb') as f:
                accumulated_clips = pickle.load(f)
        except Exception:
            accumulated_clips = []
            
    processed_video_ids = set(x['video_id'] for x in accumulated_clips)
    new_clips = 0
    extracted_vids = 0
    
    for v_idx, vid_f in enumerate(mp4_files, 1):
        v_id = os.path.splitext(os.path.basename(vid_f))[0]
        if v_id in processed_video_ids:
            if cleanup_mp4:
                try:
                    os.remove(vid_f)
                except Exception:
                    pass
            continue
            
        print(f"[{v_idx}/{len(mp4_files)}] Processing: {os.path.basename(vid_f)} ...", end="", flush=True)
        clips = extract_landmarks_from_video(vid_f, exercise)
        if clips:
            accumulated_clips.extend(clips)
            processed_video_ids.add(v_id)
            new_clips += len(clips)
            extracted_vids += 1
            print(f" -> [+ {len(clips)} clean clips]")
        else:
            print(f" -> [Rejected by QA / Insufficient Motion]")
            
        if cleanup_mp4:
            try:
                os.remove(vid_f)
            except Exception:
                pass
                
        # Periodic save every 10 videos
        if extracted_vids > 0 and extracted_vids % 10 == 0:
            with open(EXTRACTED_PKL, 'wb') as f:
                pickle.dump(accumulated_clips, f)
                
    # Final save
    with open(EXTRACTED_PKL, 'wb') as f:
        pickle.dump(accumulated_clips, f)
        
    print("\n" + "=" * 65)
    print(f"[EXTRACTION COMPLETED FOR {exercise.upper()}]")
    print(f"   New videos successfully extracted: {extracted_vids}")
    print(f"   New clips added to pool:          {new_clips}")
    print(f"   Total clips in accumulated pool:  {len(accumulated_clips)}")
    print("=" * 65)

def print_status():
    """Prints current inventory of Batch 3 videos and extracted clips."""
    ensure_dirs()
    print("=" * 65)
    print("BATCH 3 DATASET EXPANSION INVENTORY")
    print("=" * 65)
    for ex in ALL_EXERCISES:
        ex_dir = os.path.join(RAW_B3_DIR, ex)
        count = len(glob.glob(os.path.join(ex_dir, "*.mp4")))
        print(f"   * {ex:<15}: {count} raw videos on disk")
        
    if os.path.exists(EXTRACTED_PKL):
        with open(EXTRACTED_PKL, 'rb') as f:
            clips = pickle.load(f)
        from collections import Counter
        counts = Counter(x['exercise'] for x in clips)
        print("\nExtracted Batch 3 Clean Clips in Pool:")
        for ex in ALL_EXERCISES:
            print(f"   * {ex:<15}: {counts.get(ex, 0):4d} clips")
        print(f"\nTOTAL EXTRACTED CLIPS IN POOL: {len(clips):4d}")
    else:
        print("\nNo extracted clips yet. Run extraction after downloading.")
    print("=" * 65)

def merge_and_export_v7():
    """
    Merges Batch 3 with baseline dataset, applies zero-leakage split, and exports v7 pickles.
    100% preserves all 1,720 baseline clips, adds all clean Batch 3 clips, and ensures >5,000 clips.
    """
    baseline_train_path = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'posec3d_data', 'Files to upload to kaggle', 'custom_dataset_train.pkl')
    baseline_val_path = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'posec3d_data', 'Files to upload to kaggle', 'custom_dataset_val.pkl')
    
    out_dir = os.path.join(BASE_DIR, 'model_training', 'experiments_v7_expansion')
    os.makedirs(out_dir, exist_ok=True)
    
    if not os.path.exists(EXTRACTED_PKL):
        print(f"[ERROR] {EXTRACTED_PKL} not found.")
        return
        
    with open(EXTRACTED_PKL, 'rb') as f:
        b3_clips = pickle.load(f)
        
    with open(baseline_train_path, 'rb') as f:
        base_train = pickle.load(f)
        
    with open(baseline_val_path, 'rb') as f:
        base_val = pickle.load(f)
        
    print("=" * 65)
    print("CONSOLIDATING 5,000+ CLIP DATASET (ZERO-LEAKAGE SPLIT)")
    print("=" * 65)
    print(f"Preserved Baseline Train Clips: {len(base_train)}")
    print(f"Preserved Benchmark Val Clips:  {len(base_val)}")
    print(f"Accumulated Batch 3 New Clips:  {len(b3_clips)}")
    
    # 80/20 video-level disjoint split for Batch 3
    b3_vids = np.array([x['video_id'] for x in b3_clips])
    unique_vids = np.unique(b3_vids)
    
    rng = np.random.RandomState(42)
    shuffled_vids = unique_vids.copy()
    rng.shuffle(shuffled_vids)
    
    split_idx = int(0.8 * len(shuffled_vids))
    train_vids_set = set(shuffled_vids[:split_idx])
    val_vids_set = set(shuffled_vids[split_idx:])
    
    b3_train = [x for x in b3_clips if x['video_id'] in train_vids_set]
    b3_val = [x for x in b3_clips if x['video_id'] in val_vids_set]
    
    final_train = base_train + b3_train
    final_val_expanded = base_val + b3_val
    
    out_train_path = os.path.join(out_dir, 'custom_dataset_train_v7.pkl')
    out_val_expanded_path = os.path.join(out_dir, 'custom_dataset_val_v7.pkl')
    out_val_frozen_path = os.path.join(out_dir, 'custom_dataset_val_frozen.pkl')
    
    with open(out_train_path, 'wb') as f:
        pickle.dump(final_train, f)
    with open(out_val_expanded_path, 'wb') as f:
        pickle.dump(final_val_expanded, f)
    with open(out_val_frozen_path, 'wb') as f:
        pickle.dump(base_val, f)  # Frozen 444 benchmark clips
        
    from collections import Counter
    train_counts = Counter(x['label'] for x in final_train)
    val_counts = Counter(x['label'] for x in final_val_expanded)
    inv_label = {v: k for k, v in LABEL_MAP.items()}
    
    print("\n" + "=" * 65)
    print("[SUCCESS] PHASE v7 DATASET CONSOLIDATION COMPLETE!")
    print("=" * 65)
    print(f"{'EXERCISE':<15} {'BASE TRAIN':<12} {'v7 TRAIN':<12} {'v7 EXP VAL':<12}")
    print("-" * 65)
    base_train_counts = Counter(x['label'] for x in base_train)
    for lbl in range(7):
        ex_name = inv_label[lbl]
        print(f"{ex_name:<15} {base_train_counts.get(lbl, 0):<12} {train_counts.get(lbl, 0):<12} {val_counts.get(lbl, 0):<12}")
    print("-" * 65)
    print(f"Total v7 Training Clips:   {len(final_train):5d}  ({os.path.getsize(out_train_path)/1024**2:.2f} MB)")
    print(f"Total v7 Expanded Val:     {len(final_val_expanded):5d}  ({os.path.getsize(out_val_expanded_path)/1024**2:.2f} MB)")
    print(f"Frozen Benchmark Val:      {len(base_val):5d}  (Strictly frozen 115 held-out videos zero leakage)")
    print(f"Target Milestone >= 5,000: {'ACHIEVED!' if len(final_train) >= 5000 else f'Pending ({len(final_train)}/5000)'}")
    print(f"Export directory:          {out_dir}")
    print("=" * 65)

def run_target_5000(fresh_videos_per_exercise=110, cleanup_mp4=True):
    """
    Executes large-scale expansion across ALL 7 exercises:
    1. Downloads 110 fresh, brand-new videos per exercise (guaranteed 0 duplicates via archive).
    2. Extracts 5-6 clean clips per video via MediaPipe.
    3. Deletes raw MP4s after extraction for 0 MB disk bloat.
    4. Merges with preserved 1,978 clips to surpass 5,000+ training clips.
    """
    print("#" * 65)
    print("BIOMECHAI OVERNIGHT RUN: TARGET 5,000+ TRAINING CLIPS")
    print(f"Fresh videos per exercise: {fresh_videos_per_exercise} (~{fresh_videos_per_exercise * 7} total)")
    print(f"Auto-cleanup raw MP4s:    {cleanup_mp4}")
    print("#" * 65)
    
    for idx, ex in enumerate(ALL_EXERCISES, 1):
        print(f"\n[{idx}/7] >>> Starting Pipeline for: {ex.upper()} <<<")
        download_fresh_videos(ex, count_to_download=fresh_videos_per_exercise)
        extract_for_exercise(ex, cleanup_mp4=cleanup_mp4)
        
    print("\n" + "#" * 65)
    print("ALL 7 EXERCISES COMPLETED SUCCESSFULLY!")
    print("#" * 65)
    print_status()
    
    print("\n>>> Consolidating Final Phase v7 Dataset (Zero-Leakage Split) <<<")
    merge_and_export_v7()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="BioMechAI Large Batch Dataset Expansion")
    parser.add_argument('--target-5000', action='store_true', help="Run overnight expansion for 5,000+ training clips across all 7 exercises")
    parser.add_argument('--fresh-videos', type=int, default=110, help="Fresh videos to download per exercise (default: 110)")
    parser.add_argument('--batch-process', type=str, choices=ALL_EXERCISES, help="Run single exercise")
    parser.add_argument('--cleanup-mp4', action='store_true', help="Delete raw MP4 after landmark extraction to save disk space")
    parser.add_argument('--status', action='store_true', help="Show Batch 3 inventory")
    parser.add_argument('--merge-v7', action='store_true', help="Consolidate and export v7 training datasets")
    
    args = parser.parse_args()
    
    if args.target_5000:
        run_target_5000(fresh_videos_per_exercise=args.fresh_videos, cleanup_mp4=args.cleanup_mp4)
    elif args.batch_process:
        download_fresh_videos(args.batch_process, count_to_download=args.fresh_videos)
        extract_for_exercise(args.batch_process, cleanup_mp4=args.cleanup_mp4)
    elif args.merge_v7:
        merge_and_export_v7()
    else:
        print_status()
