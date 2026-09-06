# BioMechAI Models Directory

## Overview
This directory organizes all trained machine learning and deep learning models for the BioMechAI Exercise Classifier across all evolutionary stages.

---

## Subdirectories

```
models/
├── posec3d_v4/                   # [CHAMPION] FineGYM Transfer Learning Deep Learning Model
│   ├── README.md                 # Architecture, FineGYM base, metrics, and evaluation matrix
│   ├── best_acc_top1_epoch_4.pth # Peak model (50.90% Top-1, 85.29% Lunge, 67.12% Bicep Curl)
│   ├── phase4_v4_result.pkl      # 444-clip held-out evaluation output
│   ├── posec3d_biomechai_v4.py   # MMAction2 configuration file
│   └── pose_transforms_extra.py  # Camera viewpoint tilt jitter transform
│
├── posec3d_v3/                   # [STAGE 3] NTU-60 Pretrained Transfer Learning Model
│   ├── README.md                 # Documentation and NTU-60 benchmark analysis
│   ├── best_acc_top1_epoch_14.pth# Peak checkpoint (48.20% Top-1, 49.64% Macro Recall)
│   ├── phase4_v3_result.pkl      # 444-clip evaluation dumps
│   ├── posec3d_biomechai_v3.py   # MMAction2 configuration file
│   └── pose_transforms_extra.py  # Transform module
│
├── posec3d_v1/                   # [STAGE 1] Original Scratch Baseline Model (formerly posec3d_v5)
│   ├── README.md                 # Documentation of scratch training
│   ├── best_acc_top1_epoch_18.pth# Peak checkpoint from scratch (49.77% Top-1, 51.83% Recall)
│   ├── epoch_24.pth              # Final 24-epoch checkpoint with optimizer momentum
│   └── posec3d_biomechai.py      # MMAction2 configuration file
│
├── random_forest_baselines/      # [GEOMETRIC BASELINES] Tabular Random Forest Models
│   ├── README.md                 # Documentation of tabular models (v1 through v5: 56.08% LOVO)
│   ├── exercise_classifier_v4.pkl# Final 599-video Random Forest model
│   └── confusion_matrix.png      # Baseline confusion matrix plot
│
└── mediapipe/                    # [FEATURE EXTRACTOR] Landmark Extraction Task Model
    └── pose_landmarker_lite.task # MediaPipe pose landmark detector
```

---

## Recommended Deployment Model

For production deployment and presentation:
* **Primary Deep Learning Champion**: **`models/posec3d_v4/best_acc_top1_epoch_4.pth`**
* Config: **`models/posec3d_v4/posec3d_biomechai_v4.py`**
* Peak Highlights: **50.90% Overall Top-1**, **85.29% Lunge Recall**, **67.12% Bicep Curl Recall** on 115 held-out subject videos.
