# BioMechAI Models Directory

## Overview
This directory organizes all trained machine learning and deep learning models for the BioMechAI Exercise Classifier.

---

## Subdirectories

```
models/
├── posec3d_v5/                   # [PRIMARY] Final Fine-Tuned Deep Learning Model (PoseC3D)
│   ├── README.md                 # Architecture, weights, metrics, and inference code
│   ├── best_acc_top1_epoch_18.pth# Peak validation model (49.77% Top-1, 87.39% Top-5)
│   ├── epoch_24.pth              # Final 24-epoch checkpoint with optimizer buffers
│   └── posec3d_biomechai.py      # MMAction2 configuration file
│
└── random_forest_baselines/      # [BASELINES] Historical Tabular Random Forest Models
    ├── README.md                 # Documentation of tabular models (v1 through v5)
    ├── exercise_classifier_v4.pkl# Final 599-video Random Forest model (52.91% LOVO-CV)
    ├── exercise_classifier.pkl   # Earlier baseline model (v2/v3)
    ├── scaler_v4.pkl / scaler.pkl# Fitted StandardScalers
    ├── label_encoder_v4.pkl      # Fitted LabelEncoders
    └── confusion_matrix.png      # Baseline confusion matrix plot
```

---

## Recommended Deployment Model

For production deployment and presentation, use:
- **`models/posec3d_v5/best_acc_top1_epoch_18.pth`**
- Config: **`models/posec3d_v5/posec3d_biomechai.py`**
- Evaluated on: **444 clips across 115 unseen video folds (zero subject overlap)**.
