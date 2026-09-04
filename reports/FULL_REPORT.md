# CLAUDE.md — BioMechAI Project Context & Architecture Guide

> **Purpose**: This file serves as the definitive reference for Claude AI (and other agents) to immediately understand the entire codebase, directory structure, data cleanup history, video collection pipeline, evaluation metrics, and current model artifacts.

---

## 1. Project Overview

* **Project Name**: BioMechAI — Biomechanical Exercise Recognition & Form Analysis (Module 3)
* **Goal**: Real-time classification and kinematic analysis of 7 human exercises from video streams:
  1. `bicep_curl`
  2. `high_knees`
  3. `jumping_jack`
  4. `lunge`
  5. `plank`
  6. `pushup`
  7. `squat`
* **Core Technology Stack**:
  * **Pose Estimation**: Google MediaPipe Pose Landmarker (`pose_landmarker_lite.task` — 33 3D landmarks)
  * **Video Processing**: OpenCV (`cv2` 5.0.0)
  * **Feature Engineering**: 50 biomechanical kinematic features (joint angles + angular velocities + bilateral asymmetries)
  * **Classifier**: Scikit-Learn `RandomForestClassifier` (200 trees, `max_depth=15`, `min_samples_leaf=2`, `random_state=42`)
  * **Validation Protocol**: **Leave-One-Video-Out Cross-Validation (LOVO-CV)** — the only honest metric for human activity recognition across unseen subjects.

---

## 2. Directory Structure & File Map

```
biomechai_model/
├── CLAUDE.md                                  # <-- THIS FILE (Master Agent Guide)
├── pose_landmarker_lite.task                  # MediaPipe Pose Landmarker model asset
├── BIOMECHAI_MODULE3_DATA_CLEANUP_AGENT_INSTRUCTIONS.md # Original cleanup specification
├── PHASE_1_of_8.md to PHASE_8_of_8.md        # 8-phase operational instruction guides
│
├── data/
│   ├── raw_videos/                            # ORIGINAL downloaded MP4 videos (1,054 files, untouched)
│   ├── landmarks/                             # ORIGINAL extracted landmark JSON clips (335 files, untouched)
│   ├── raw_videos_batch2/                     # BATCH 2 newly downloaded diverse MP4 videos (78 files)
│   │   ├── bicep_curl/                        # 11 videos
│   │   ├── high_knees/                        # 9 videos
│   │   ├── jumping_jack/                      # 14 videos
│   │   ├── lunge/                             # 12 videos
│   │   ├── plank/                             # 12 videos
│   │   ├── pushup/                            # 11 videos
│   │   └── squat/                             # 9 videos
│   └── landmarks_batch2/                      # BATCH 2 extracted & motion-filtered landmark clips (329 JSON files)
│       └── [7 exercise subdirectories]
│
├── model_training/
│   ├── cleanup_v2/                            # INITIAL DATA CLEANUP & BASELINE LOGS
│   │   ├── REPORT.md                          # Initial audit report (LOVO-CV: 35.71%)
│   │   ├── baseline_videos.json               # Phase 1: 42 clean accepted baseline video signatures
│   │   ├── excluded_duplicates.json           # 25 duplicate videos identified in original data
│   │   ├── excluded_corrupted.json            # 2 corrupted landmark clips
│   │   ├── excluded_static.json               # 26 zero-motion / static clips
│   │   ├── phase2_download_log.json           # Phase 2 download log
│   │   ├── phase3_extraction_log.json         # Phase 3 landmark extraction log
│   │   ├── batch2_duplicates.json             # Phase 4 deduplication log (0 duplicates)
│   │   ├── phase5_motion_filter_log.json      # Phase 5 combined motion filter log
│   │   ├── accepted_clips.json                # Phase 5 final accepted clip metadata (495 clips)
│   │   ├── merged_dataset.json                # Phase 6 merged 50-feature matrix (495 samples)
│   │   ├── phase7_lovo_results.json           # Phase 7 119-fold LOVO-CV evaluation results
│   │   ├── exercise_classifier_CLEANED.pkl    # Initial baseline model (35.71% LOVO-CV)
│   │   ├── scaler_CLEANED.pkl                 # Initial baseline scaler
│   │   └── label_encoder_CLEANED.pkl          # Initial baseline label encoder
│   │
│   └── cleanup_v3/                            # FINAL UNIFIED PRODUCTION ARTIFACTS & REPORT
│       ├── REPORT.md                          # Master Report: Collection, Validation & Evaluation
│       ├── baseline_videos.json               # Baseline video records
│       ├── batch2_downloads.json              # Batch 2 download metadata & channels
│       ├── batch2_duplicates.json             # Deduplication log
│       ├── batch2_static_excluded.json        # Filtered low-motion clip records
│       ├── merged_lovo_cv_results.json        # 119-fold LOVO-CV cross-validation data & confusion matrix
│       ├── exercise_classifier_v3.pkl         # FINAL TRAINED MODEL (Trained on all 495 clean merged clips)
│       ├── scaler_v3.pkl                      # FINAL FITTED STANDARD SCALER (50 features)
│       └── label_encoder_v3.pkl               # FINAL LABEL ENCODER (7 classes)
│
├── models/                                    # Original legacy model artifacts
│   ├── exercise_classifier.pkl                # Original uncleaned model (inflated 82% clip split)
│   ├── scaler.pkl
│   └── label_encoder.pkl
│
└── [Execution Scripts]
    ├── extract_landmarks.py                   # Original landmark extractor
    ├── train_model.py                         # Original training script
    ├── cleanup_pipeline.py                    # Cleanup v2 pipeline script
    ├── phase1_baseline.py                     # Phase 1: Baseline builder
    ├── phase2_download.py                     # Phase 2: yt-dlp downloader with mobile client & channel caps
    ├── phase3_extract.py                      # Phase 3: MediaPipe 90-frame extractor & 20% motion filter
    ├── phase4_deduplicate.py                  # Phase 4: Exact 4-decimal signature deduplication
    ├── phase5_final_filter.py                 # Phase 5: Shifted combined median motion filter
    ├── phase6_features.py                     # Phase 6: 50-feature kinematic matrix computation
    ├── phase7_evaluate.py                     # Phase 7: 119-fold LOVO-CV cross-validation
    └── phase8_finalize.py                     # Phase 8: v3 directory packager and report writer
```

---

## 3. The Core Journey: Why and How the Dataset was Rebuilt

### Step 1: The Initial Discovery (Module 3 Cleanup)
* **The Flaw**: The original repo reported ~82% accuracy, but it was split at the **clip level** (random 80/20 train/test split). Clips from the same video were in both train and test sets, allowing the model to memorize the person/background.
* **The Audit**: Out of 67 original videos (335 clips), **25 videos were exact duplicate re-downloads**, 2 were corrupted, and 26 were completely static.
* **The Reality**: Only **42 unique videos** existed across all 7 exercises (4–8 per exercise).
* **The Real Baseline**: Honest Leave-One-Video-Out CV accuracy was only **35.71%**, and **`lunge` was completely broken at 0.00% F1**.

### Step 2: The 8-Phase Collection & Retraining Pipeline
To solve the data bottleneck honestly without synthetic inflation:
1. **Phase 1 (Baseline Locking)**: Extracted and stored 4-decimal landmark signatures for the 42 clean baseline videos into `baseline_videos.json`.
2. **Phase 2 (Candidate Video Collection)**: Downloaded 78 new diverse YouTube videos into `data/raw_videos_batch2/`, capping channel representation to $\le 2$ videos per channel to ensure subject diversity.
3. **Phase 3 (Landmark Extraction & Motion Sanity)**: Extracted 5 clips of 90 frames per video (390 candidate clips) using MediaPipe, automatically discarding 61 static/sub-threshold clips ($<20\%$ of exercise motion median).
4. **Phase 4 (Deduplication Check)**: Tested all new videos against baseline videos and each other using exact 4-decimal landmark signatures. Result: **0 duplicates** (all 77 surviving candidate videos were confirmed genuinely unique).
5. **Phase 5 (Combined Motion Re-Filter)**: Merged the 182 clean baseline clips + 329 Batch 2 clips (511 total) and filtered them against the updated combined motion distribution. **495 clean clips across 119 unique videos** were finally accepted.
6. **Phase 6 (Feature Matrix Rebuild)**: Extracted 50 biomechanical joint-angle features per clip (verified 0 NaNs, 0 Infs).
7. **Phase 7 (Honest 119-Fold LOVO-CV Evaluation)**: Re-evaluated with strict Leave-One-Video-Out cross-validation across all 119 unique videos.
8. **Phase 8 (Final Packaging)**: Serialized all artifacts into `model_training/cleanup_v3/` and documented findings in `REPORT.md`.

---

## 4. Evaluation Results: Old Baseline vs. Merged v3

### Overall Leave-One-Video-Out Cross-Validation (LOVO-CV)
| Metric | Cleanup v2 Baseline (42 videos, 182 clips) | Merged v3 Model (119 videos, 495 clips) | Absolute Change |
|---|---|---|---|
| **Honest LOVO-CV Accuracy** | **35.71%** | **56.36%** | **+20.65%** |

### Per-Class Metrics Breakdown (Side-by-Side)
| Exercise | Old Precision | New Precision | Old Recall | New Recall | Old F1 | New F1 | F1 Change |
|---|---|---|---|---|---|---|---|
| **bicep_curl** | 0.35 | **0.41** | 0.32 | **0.49** | 0.33 | **0.44** | +0.11 |
| **high_knees** | 0.42 | **0.77** | 0.49 | **0.69** | 0.45 | **0.72** | +0.27 |
| **jumping_jack** | 0.46 | **0.62** | 0.67 | **0.69** | 0.55 | **0.65** | +0.10 |
| **lunge** | **0.00** | **0.49** | **0.00** | **0.47** | **0.00** | **0.48** | **+0.48** |
| **plank** | 0.44 | **0.65** | 0.33 | **0.63** | 0.38 | **0.64** | +0.26 |
| **pushup** | 0.33 | **0.63** | 0.39 | **0.67** | 0.36 | **0.65** | +0.29 |
| **squat** | 0.36 | **0.39** | 0.30 | **0.30** | 0.33 | **0.34** | +0.01 |

### Confusion Matrix (119 Folds, 495 Clips)
```
True \ Pred      bicep_curl  high_knees  jumping_jack  lunge  plank  pushup  squat
bicep_curl            34           6            4         8      2       9      7
high_knees             5          46            7         8      0       0      1
jumping_jack           5           3           53         4      5       3      4
lunge                 14           2           10        37      3       5      8
plank                  8           1            1         3     41       7      4
pushup                 4           1            2         4      7      49      6
squat                 13           1            9        12      5       5     19
```

---

## 5. Feature Engineering Specification (50 Dimensions)

Features are extracted from a 90-frame landmark clip sequence of shape `(90, 33, 3)` using `extract_features(landmarks)`:

```python
import numpy as np

def angle(lm, a, b, c):
    ba = lm[:, a, :2] - lm[:, b, :2]
    bc = lm[:, c, :2] - lm[:, b, :2]
    cos = np.sum(ba * bc, axis=1) / (
        np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1) + 1e-9)
    return np.degrees(np.arccos(np.clip(cos, -1, 1)))

def extract_features(landmarks):
    lm = np.array(landmarks)
    features = []
    angle_seqs = {
        'knee_l':     angle(lm, 23, 25, 27), # left hip-knee-ankle
        'knee_r':     angle(lm, 24, 26, 28), # right hip-knee-ankle
        'elbow_l':    angle(lm, 11, 13, 15), # left shoulder-elbow-wrist
        'elbow_r':    angle(lm, 12, 14, 16), # right shoulder-elbow-wrist
        'hip_l':      angle(lm, 11, 23, 25), # left shoulder-hip-knee
        'hip_r':      angle(lm, 12, 24, 26), # right shoulder-hip-knee
        'shoulder_l': angle(lm, 13, 11, 23), # left elbow-shoulder-hip
        'shoulder_r': angle(lm, 14, 12, 24), # right elbow-shoulder-hip
    }
    # 5 summary statistics per joint angle (8 * 5 = 40 features):
    for seq in angle_seqs.values():
        features.extend([np.mean(seq), np.std(seq), np.min(seq), np.max(seq), np.max(seq) - np.min(seq)])
    # Angular velocity approximation (8 features):
    for seq in angle_seqs.values():
        features.append(np.mean(np.abs(np.diff(seq))))
    # Bilateral asymmetries (2 features):
    features.append(np.mean(np.abs(angle_seqs['knee_l'] - angle_seqs['knee_r'])))
    features.append(np.mean(np.abs(angle_seqs['shoulder_l'] - angle_seqs['shoulder_r'])))
    return np.array(features) # Shape: (50,)
```

---

## 6. How to Load and Run Inference with the v3 Model

```python
import joblib, json, numpy as np

# 1. Load production v3 artifacts
MODEL_DIR = r"model_training/cleanup_v3"
clf = joblib.load(f"{MODEL_DIR}/exercise_classifier_v3.pkl")
scaler = joblib.load(f"{MODEL_DIR}/scaler_v3.pkl")
label_encoder = joblib.load(f"{MODEL_DIR}/label_encoder_v3.pkl")

# 2. Extract 50 features from 90-frame MediaPipe pose landmarks (shape: 90, 33, 3)
features = extract_features(clip_landmarks) # shape (50,)

# 3. Scale and predict
scaled_features = scaler.transform([features])
pred_idx = clf.predict(scaled_features)[0]
pred_class = label_encoder.inverse_transform([pred_idx])[0]
probabilities = clf.predict_proba(scaled_features)[0]

print(f"Predicted Exercise: {pred_class} (Confidence: {probabilities[pred_idx]*100:.1f}%)")
```

---

## 7. Roadmap to Reach 85%+ LOVO-CV Accuracy

1. **Torso & Orientation Features**: Add torso angle relative to horizontal ground (`angle_between_torso_and_vertical`). This eliminates confusion between horizontal exercises (`plank`, `pushup`) and upright exercises (`squat`, `bicep_curl`).
2. **Keypoint Displacement Features**: Add vertical displacement of wrists relative to shoulders (`y_wrist - y_shoulder`) and vertical travel of hips (`y_hip_max - y_hip_min`). This instantly separates `bicep_curl` from `squat`.
3. **Temporal Deep Learning Model**: Replace static summary Random Forest with a **1D-CNN + Bi-LSTM / GRU** operating directly on the 90-frame temporal trajectory to capture repetition phases and movement rhythm.
4. **Targeted Side-View Video Collection**: Collect 10–15 side-profile videos for `squat` and `lunge` to eliminate frontal perspective ambiguity.
5. **Scale**: Target ~30–35 unique video sources per class (200–250 total).
