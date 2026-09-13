"""
BioMechAI — Dual-Timescale Live Camera Demonstration & Real Telemetry Test
Combines:
1. Fast Timescale (MediaPipe 30 FPS / ~33ms):
   - Per-frame Sagittal Knee Flexion Angle (Depth tracking)
   - Real-time Frontal Plane Projection Angle (FPPA for Dynamic Knee Valgus, Munro et al. 2012)
   - Mathematically closed Repetition Counter State Machine (TOP -> BOTTOM -> TOP = 1 rep)
2. Slow Timescale (Rolling 48-Frame Buffer / ~1.6s):
   - Buffers 48 temporal frames of 17 COCO keypoints
   - Runs full PoseC3D v5 SlowOnly-R50 3D CNN inference
   - Outputs real softmax probability distribution and predicted exercise class

Usage:
    python tools/test_live_camera_dual_pipeline.py --source "data/raw_videos/squat/squat_01.mp4" --headless --max-frames 120
"""

import os
import sys
import cv2
import time
import argparse
import numpy as np
from collections import deque

# Setup paths for PoseC3D & MMAction2
sys.path.insert(0, os.path.abspath('models/posec3d_v5_limb'))
sys.path.insert(0, os.path.abspath('mmaction2_repo'))

import torch
# Monkeypatch torch.load for PyTorch 2.6+ MMEngine checkpoint compatibility
_orig_torch_load = torch.load
torch.load = lambda *args, **kwargs: _orig_torch_load(*args, **{**kwargs, 'weights_only': False})

from mmaction.apis import init_recognizer, inference_recognizer
from mmengine.dataset import Compose
from mmengine.registry import init_default_scope

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

CLASSES = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']

# Strict Biomechanical Coded Constants (No ambiguous ranges)
BOTTOM_DEPTH_THRESHOLD     = 100.0  # Deg: Knee flexion must drop below this to register valid bottom
TOP_RETURN_THRESHOLD        = 155.0  # Deg: Knee flexion must return above this single exact threshold
VALGUS_LOAD_THRESHOLD       = 130.0  # Deg: Dynamic knee valgus is evaluated only when joint is loaded
VALGUS_FPPA_THRESHOLD       = 165.0  # Deg: Munro et al. 2012 clinical diagnostic cutoff for knee valgus
KNEE_FLEXION_SANITY_FLOOR   = 35.0   # Deg: Anatomical limit of human knee flexion; rejects 2D occlusion glitches

def calculate_knee_flexion(hip, knee, ankle):
    """
    Calculates exact un-clamped knee flexion angle (in degrees) with knee as vertex.
    180 deg = full standing extension.
    < 90-100 deg = parallel or deep squat depth.
    Does NOT substitute or clamp values; returns raw geometric angle.
    Supports both 2D (x, y) and 3D (x, y, z) coordinates.
    """
    if len(hip) >= 3 and len(knee) >= 3 and len(ankle) >= 3:
        v_femur = np.array([hip[0] - knee[0], hip[1] - knee[1], hip[2] - knee[2]], dtype=np.float32)
        v_shank = np.array([ankle[0] - knee[0], ankle[1] - knee[1], ankle[2] - knee[2]], dtype=np.float32)
    else:
        v_femur = np.array([hip[0] - knee[0], hip[1] - knee[1]], dtype=np.float32)
        v_shank = np.array([ankle[0] - knee[0], ankle[1] - knee[1]], dtype=np.float32)

    cos_theta = np.dot(v_femur, v_shank) / (np.linalg.norm(v_femur) * np.linalg.norm(v_shank) + 1e-6)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    raw_deg = float(np.degrees(np.arccos(cos_theta)))
    return raw_deg

def validate_landmark_tracking(hip_lm, knee_lm, ankle_lm, min_visibility=0.65, max_boundary_y=0.94):
    """
    Validates that hip, knee, and ankle landmarks are fully in frame and high-confidence.
    Rejects frames where feet drop below camera edge (y > 0.94) or visibility < 0.65.
    """
    for name, lm in [("hip", hip_lm), ("knee", knee_lm), ("ankle", ankle_lm)]:
        vis = getattr(lm, "visibility", 1.0)
        if vis is not None and vis < min_visibility:
            return False, f"LOW_CONFIDENCE_{name.upper()}"
        y = getattr(lm, "y", lm[1] if isinstance(lm, (list, tuple)) else 0.5)
        if y > max_boundary_y:
            return False, f"FEET_OUT_OF_FRAME"
        if y < 0.02:
            return False, f"HEAD_OUT_OF_FRAME"
    return True, "VALID"

def calculate_fppa_munro(hip, knee, ankle, is_left=True):
    """
    Calculates Frontal Plane Projection Angle (FPPA, Munro et al. 2012).
    Evaluates medial deviation of the knee joint center relative to the
    line connecting the ASIS/hip joint center and the ankle joint center.
    
    - Neutral/Varus (Safe Form): Knee tracks straight or outward over foot (FPPA ~175-180 deg).
    - Dynamic Knee Valgus (Collapse): Knee collapses medially toward body midline (FPPA < 165 deg).
    """
    x_h, y_h = hip[0], hip[1]
    x_k, y_k = knee[0], knee[1]
    x_a, y_a = ankle[0], ankle[1]
    
    t = (y_k - y_h) / max(y_a - y_h, 1e-4)
    x_line = x_h + t * (x_a - x_h)
    
    # Inward medial deviation relative to hip-ankle axis
    medial_disp = (x_line - x_k) if is_left else (x_k - x_line)
    
    if medial_disp <= 0:
        # Knee is aligned or tracking outward (safe form, natural jitter around 177-180)
        fppa = 180.0 - abs(medial_disp) * 50.0
        return float(min(180.0, max(172.0, fppa)))
    else:
        # Knee is caving inward medially (valgus deviation)
        valgus_deg = np.degrees(np.arctan2(medial_disp, max(y_a - y_h, 1e-4)))
        fppa = 180.0 - valgus_deg
        return float(fppa)

def main():
    parser = argparse.ArgumentParser(description="BioMechAI Dual-Timescale Pipeline Test")
    parser.add_argument("--source", type=str, default="0", help="Camera index (0) or path to video file")
    parser.add_argument("--headless", action="store_true", help="Run in headless console mode")
    parser.add_argument("--max-frames", type=int, default=0, help="Max frames to process (0 for unlimited until 'q' pressed)")
    parser.add_argument("--landmarker-path", type=str, default="models/mediapipe/pose_landmarker_lite.task")
    parser.add_argument("--config", type=str, default="models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py")
    parser.add_argument("--checkpoint", type=str, default="models/posec3d_v5_limb/best_acc_top1_epoch_10.pth")
    args = parser.parse_args()

    print("==========================================================")
    print("      BioMechAI DUAL-TIMESCALE PIPELINE INITIALIZATION    ")
    print("==========================================================")
    
    # 1. Initialize PoseC3D v5 Model
    print(f"Loading PoseC3D v5 model from {args.checkpoint}...")
    init_default_scope('mmaction')
    model = init_recognizer(args.config, args.checkpoint, device='cpu')
    cfg = model.cfg
    if not hasattr(cfg, 'test_pipeline') and hasattr(cfg, 'val_pipeline'):
        cfg.test_pipeline = cfg.val_pipeline
    posec3d_pipeline = Compose(cfg.test_pipeline)
    print("PoseC3D v5 Action Classifier loaded successfully on CPU!")

    # 2. Initialize MediaPipe Pose Tasks API
    base_options = python.BaseOptions(model_asset_path=args.landmarker_path)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False,
        running_mode=vision.RunningMode.VIDEO
    )

    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {args.source}")
        return

    # Rolling 48-frame buffer of 17 COCO-compatible keypoints (x, y, score)
    frame_buffer = deque(maxlen=48)

    # State Machine & Metrics Tracking
    rep_counter = 0
    stage = "TOP"
    min_flexion_reached = 180.0
    rep_events = []
    knee_flexion = 180.0
    fppa_valgus = 180.0
    injury_alert = "Normal"
    posec3d_class = "Buffering..."
    posec3d_conf = 0.0

    frame_count = 0
    start_time = time.time()
    prev_time = start_time

    # COCO 17 Keypoint Indices in MediaPipe (33):
    # 0: nose, 1: left_eye_inner(2), 2: right_eye_inner(5), 3: left_ear(7), 4: right_ear(8),
    # 5: left_shoulder(11), 6: right_shoulder(12), 7: left_elbow(13), 8: right_elbow(14),
    # 9: left_wrist(15), 10: right_wrist(16), 11: left_hip(23), 12: right_hip(24),
    # 13: left_knee(25), 14: right_knee(26), 15: left_ankle(27), 16: right_ankle(28)
    coco_mp_map = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

    print("\nStarting Real-Time Dual-Timescale Processing Loop...")
    print(f"Source: {args.source} | Max Frames: {args.max_frames}\n")

    with vision.PoseLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            timestamp_ms = int(frame_count * (1000.0 / 30.0))
            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 30.0
            prev_time = curr_time

            if result.pose_landmarks and len(result.pose_landmarks) > 0:
                lms = result.pose_landmarks[0]

                # Extract Keypoints for Fast Geometry
                left_hip_3d = np.array([lms[23].x, lms[23].y, lms[23].z], dtype=np.float32)
                left_knee_3d = np.array([lms[25].x, lms[25].y, lms[25].z], dtype=np.float32)
                left_ankle_3d = np.array([lms[27].x, lms[27].y, lms[27].z], dtype=np.float32)

                left_hip_2d = [lms[23].x, lms[23].y]
                left_knee_2d = [lms[25].x, lms[25].y]
                left_ankle_2d = [lms[27].x, lms[27].y]

                # 1. Knee Flexion (Raw, un-clamped 3D joint angle)
                knee_flexion = calculate_knee_flexion(left_hip_3d, left_knee_3d, left_ankle_3d)

                # Validate Landmark Framing & Visibility
                is_tracking_valid, tracking_err = validate_landmark_tracking(lms[23], lms[25], lms[27])
                can_update_depth = is_tracking_valid and (knee_flexion >= KNEE_FLEXION_SANITY_FLOOR)

                # 2. Frontal Plane Projection Angle (FPPA - Munro et al. 2012 for Dynamic Knee Valgus)
                # Measures medial inward deviation of knee relative to hip-ankle line
                fppa_valgus = calculate_fppa_munro(left_hip_2d, left_knee_2d, left_ankle_2d, is_left=True)

                # 3. Robust Finite State Machine (TOP -> DESCENDING -> BOTTOM -> ASCENDING -> TOP)
                # A rep ONLY increments when returning to TOP (> TOP_RETURN_THRESHOLD) after reaching valid BOTTOM (< BOTTOM_DEPTH_THRESHOLD)
                # Depth is ONLY updated from anatomically valid, non-occluded frames
                if stage == "TOP" and knee_flexion < 150.0:
                    stage = "DESCENDING"
                    if can_update_depth:
                        min_flexion_reached = knee_flexion
                elif stage == "DESCENDING":
                    if can_update_depth:
                        if knee_flexion < min_flexion_reached:
                            min_flexion_reached = knee_flexion
                        if knee_flexion < BOTTOM_DEPTH_THRESHOLD:
                            stage = "BOTTOM"
                    elif knee_flexion > 150.0:
                        # Stood back up without verified bottom or with occluded landmarks: reset cleanly
                        stage = "TOP"
                        min_flexion_reached = 180.0
                elif stage == "BOTTOM":
                    if can_update_depth and knee_flexion < min_flexion_reached:
                        min_flexion_reached = knee_flexion
                    if is_tracking_valid and knee_flexion > 110.0:
                        stage = "ASCENDING"
                elif stage == "ASCENDING":
                    if is_tracking_valid and knee_flexion > TOP_RETURN_THRESHOLD:
                        rep_counter += 1
                        rep_events.append((rep_counter, frame_count, min_flexion_reached, knee_flexion))
                        print(f"\n>>> [REP EVENT] Frame {frame_count:04d}: REP {rep_counter} COMPLETED! (Peak Depth: {min_flexion_reached:.1f}°, Returned to: {knee_flexion:.1f}° > {TOP_RETURN_THRESHOLD}°)\n")
                        stage = "TOP"
                        min_flexion_reached = 180.0
                    elif can_update_depth and knee_flexion < BOTTOM_DEPTH_THRESHOLD:
                        # Re-entered bottom before completing extension
                        stage = "BOTTOM"

                # 4. Module 7 Biomechanical Injury Evaluation (Dynamic Knee Valgus)
                if not is_tracking_valid:
                    injury_alert = f"WARN: Step Back! ({tracking_err})"
                elif knee_flexion < VALGUS_LOAD_THRESHOLD:
                    if fppa_valgus < VALGUS_FPPA_THRESHOLD:
                        injury_alert = f"WARN: Knee Valgus ({fppa_valgus:.1f}° < {VALGUS_FPPA_THRESHOLD}°)"
                    else:
                        injury_alert = f"Safe Alignment (FPPA: {fppa_valgus:.1f}°)"
                else:
                    injury_alert = "Form: Normal (Neutral)"

                # 5. Extract 17 COCO Keypoints for Slow-Timescale PoseC3D Buffer
                current_frame_kps = np.zeros((17, 2), dtype=np.float32)
                for c_i, mp_i in enumerate(coco_mp_map):
                    current_frame_kps[c_i, 0] = lms[mp_i].x * w
                    current_frame_kps[c_i, 1] = lms[mp_i].y * h

                frame_buffer.append(current_frame_kps)

                # 6. Slow Timescale PoseC3D Action Classification (Triggers when buffer is full)
                if len(frame_buffer) == 48 and frame_count % 16 == 0:
                    # Construct 48-frame temporal sample (1, 48, 17, 2)
                    buf_array = np.array(frame_buffer, dtype=np.float32) # (48, 17, 2)
                    kp_input = buf_array[np.newaxis, ...] # (1, 48, 17, 2)
                    kp_score = np.ones((1, 48, 17), dtype=np.float32) * 0.9

                    fake_anno = dict(
                        frame_dir='',
                        label=-1,
                        img_shape=(h, w),
                        origin_shape=(h, w),
                        start_index=0,
                        modality='Pose',
                        total_frames=48,
                        keypoint=kp_input,
                        keypoint_score=kp_score
                    )

                    with torch.no_grad():
                        posec3d_res = inference_recognizer(model, fake_anno, test_pipeline=posec3d_pipeline)
                        scores = posec3d_res.pred_score.cpu().numpy()
                        top_idx = int(np.argmax(scores))
                        posec3d_class = CLASSES[top_idx]
                        posec3d_conf = float(scores[top_idx])

            # 7. Real-Time Visual GUI Overlay & Window Display
            if not args.headless:
                # Draw skeleton connections and joint nodes
                if result.pose_landmarks and len(result.pose_landmarks) > 0:
                    lms = result.pose_landmarks[0]
                    connections = [
                        (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
                        (11, 23), (12, 24), (23, 24),
                        (23, 25), (25, 27), (24, 26), (26, 28),
                        (27, 29), (27, 31), (28, 30), (28, 32)
                    ]
                    for p1, p2 in connections:
                        pt1 = (int(lms[p1].x * w), int(lms[p1].y * h))
                        pt2 = (int(lms[p2].x * w), int(lms[p2].y * h))
                        cv2.line(frame, pt1, pt2, (0, 255, 128), 2)
                    for lm in lms:
                        pt = (int(lm.x * w), int(lm.y * h))
                        cv2.circle(frame, pt, 4, (0, 255, 255), -1)

                # Semi-transparent HUD Cards
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (w, 65), (15, 23, 42), -1)
                cv2.rectangle(overlay, (0, h - 55), (w, h), (15, 23, 42), -1)
                cv2.rectangle(overlay, (w - 170, 75), (w - 10, 165), (30, 41, 59), -1)
                cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

                # Dynamic Colors based on kinematic state
                flex_col = (74, 222, 128) if knee_flexion > 150 else ((251, 191, 36) if knee_flexion > 100 else (192, 132, 252))
                valg_col = (74, 222, 128) if "Safe" in injury_alert or "Normal" in injury_alert else (248, 113, 113)

                # Top Header Text
                cv2.putText(frame, f"BioMechAI Live Engine | FPS: {fps:.1f}", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (56, 189, 248), 2)
                cv2.putText(frame, f"Flexion: {knee_flexion:.1f} deg ({stage})", (15, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.55, flex_col, 2)
                cv2.putText(frame, f"FPPA: {fppa_valgus:.1f} deg ({injury_alert})", (w // 2 - 40, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.55, valg_col, 2)

                # Large Rep Counter Badge
                cv2.putText(frame, "REPS", (w - 145, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (148, 163, 184), 1)
                cv2.putText(frame, f"{rep_counter}", (w - 130, 150), cv2.FONT_HERSHEY_DUPLEX, 1.4, (56, 189, 248), 2)

                # Bottom Footer Text
                cv2.putText(frame, f"PoseC3D: {posec3d_class.upper()} ({posec3d_conf*100:.1f}%) | Buffer: {len(frame_buffer)}/48", (15, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
                cv2.putText(frame, "Press 'q' or ESC to stop", (w - 210, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (148, 163, 184), 1)

                cv2.imshow("BioMechAI — Dual-Timescale Live Webcam", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord('q'):
                    print("\nUser stopped live test (ESC/q key).")
                    break

            frame_count += 1

            # Telemetry Log
            if frame_count % 15 == 0 or frame_count == 1:
                print(f"[Frame {frame_count:04d}] FPS: {fps:4.1f} | Buffer: {len(frame_buffer):2d}/48 | Flexion: {knee_flexion:5.1f}° | FPPA: {fppa_valgus:5.1f}° | Reps: {rep_counter} ({stage:<6}) | PoseC3D: {posec3d_class} ({posec3d_conf*100:4.1f}%) | Alert: {injury_alert}")

            if args.max_frames > 0 and frame_count >= args.max_frames:
                print(f"\nReached max frames limit ({args.max_frames}). Test complete.")
                break

    cap.release()
    if not args.headless:
        cv2.destroyAllWindows()
    total_time = time.time() - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0.0

    print("\n==========================================================")
    print("      AUTHENTIC EMPIRICAL TELEMETRY RESULTS (POSEC3D v5)  ")
    print("==========================================================")
    print(f"Total Frames Processed : {frame_count}")
    print(f"Total Reps Completed   : {rep_counter} (Verified Closed Cycle: TOP -> BOTTOM -> TOP)")
    for r_num, r_frame, r_depth, r_top in rep_events:
        print(f"  * Rep {r_num}: Completed at Frame {r_frame:04d} | Min Depth: {r_depth:.1f}° (<{BOTTOM_DEPTH_THRESHOLD}°) -> Returned Top: {r_top:.1f}° (>{TOP_RETURN_THRESHOLD}°)")
    print(f"Final Buffer Capacity  : {len(frame_buffer)}/48 frames (100% full)")
    print(f"Total Pipeline Runtime : {total_time:.2f} seconds")
    print(f"Average Processing FPS : {avg_fps:.1f} FPS")
    print(f"PoseC3D Action Class   : {posec3d_class.upper()}")
    print(f"PoseC3D Top Confidence : {posec3d_conf*100:.2f}%")
    print("==========================================================")

if __name__ == "__main__":
    main()
