# BioMechAI Operational & Accuracy Fix Guides

This directory contains all technical operational guides, phase specifications, and execution instructions for training, fixing, and evaluating the BioMechAI models.

---

## Directory Structure

```
guides/
├── README.md                          # This directory guide
├── accuracy_fix_phases/               # Step-by-step 5-phase accuracy fix specifications
│   ├── FIX_PHASE_1_of_5.md           # Phase 1: Environment & Pipeline Diagnostics
│   ├── FIX_PHASE_2_of_5.md           # Phase 2: PoseC3D Baseline Audit & JJ Error Detection
│   ├── FIX_PHASE_3_of_5.md           # Phase 3: Regularization Ablation (Dropout 0.70)
│   ├── FIX_PHASE_4_of_5.md           # Phase 4: PoseC3D v3 Configuration & Rotation Augmentation
│   └── FIX_PHASE_5_of_5.md           # Phase 5: Verification & Full Held-Out Evaluation
│
└── kaggle_training/                  # Operational training and execution manuals
    ├── KAGGLE_POSEC3D_V3_TRAIN_AND_EVAL.md # End-to-end Python script & instructions for Kaggle v3 training
    ├── KAGGLE_SESSION_SETUP.md             # GPU session setup, dependencies, and environment configuration
    └── PRODUCTION_TRAINING_GUIDE.md        # Comprehensive manual for production training & troubleshooting
```
