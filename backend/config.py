"""
BioMechAI Backend Configuration
Holds all validated biomechanical constants, model paths, and class mappings.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Strict Biomechanical Coded Constants (No ambiguous ranges)
BOTTOM_DEPTH_THRESHOLD     = 115.0  # Deg: Biomechanically parallel squat depth (femur parallel to floor)
TOP_RETURN_THRESHOLD        = 146.0  # Deg: Natural upright standing extension (registers immediately upon return)
VALGUS_LOAD_THRESHOLD       = 130.0  # Deg: Dynamic knee valgus evaluated only when joint is loaded
VALGUS_FPPA_THRESHOLD       = 165.0  # Deg: Munro et al. 2012 clinical diagnostic cutoff for knee valgus
KNEE_FLEXION_SANITY_FLOOR   = 35.0   # Deg: Anatomical limit of human knee flexion; rejects 2D occlusion glitches

# Model Weights & Config Paths
# Active model version:
#   'rf' -> Random Forest Baseline (Original FYP-I 84% tabular model)
#   'v6' -> Phase v6 (Threshold 80, 54.05% Top-1 / 53.82% Macro Recall on 444 frozen benchmark)
#   'v7' -> Phase v7 (63.54% Top-1 on distinct unique clips)
#   'v5' -> Champion v5 baseline (53.38% Top-1 / 91.22% Top-5)
ACTIVE_MODEL_VERSION = "v7"

RF_MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_baselines", "exercise_classifier.pkl")
RF_SCALER_PATH = os.path.join(BASE_DIR, "models", "random_forest_baselines", "scaler.pkl")
RF_LE_PATH = os.path.join(BASE_DIR, "models", "random_forest_baselines", "label_encoder.pkl")

if ACTIVE_MODEL_VERSION == "v6":
    POSEC3D_CONFIG = os.path.join(BASE_DIR, "models", "posec3d_v6_thr80", "posec3d_biomechai_v6_thr80.py")
    POSEC3D_CHECKPOINT = os.path.join(BASE_DIR, "models", "posec3d_v6_thr80", "best_acc_top1_epoch_46.pth")
elif ACTIVE_MODEL_VERSION == "v7":
    POSEC3D_CONFIG = os.path.join(BASE_DIR, "models", "posec3d_v7_dedup", "posec3d_biomechai_v7_dedup.py")
    POSEC3D_CHECKPOINT = os.path.join(BASE_DIR, "models", "posec3d_v7_dedup", "best_acc_top1_epoch_10.pth")
else:
    POSEC3D_CONFIG = os.path.join(BASE_DIR, "models", "posec3d_v5_limb", "posec3d_biomechai_v5_limb.py")
    POSEC3D_CHECKPOINT = os.path.join(BASE_DIR, "models", "posec3d_v5_limb", "best_acc_top1_epoch_10.pth")

MEDIAPIPE_TASK = os.path.join(BASE_DIR, "models", "mediapipe", "pose_landmarker_lite.task")

# 7 Exercise Classes
CLASSES = ["bicep_curl", "high_knees", "jumping_jack", "lunge", "plank", "pushup", "squat"]

# Display mapping for mobile Flutter UI
CLASS_DISPLAY_NAMES = {
    "bicep_curl": "Bicep Curl",
    "high_knees": "High Knees",
    "jumping_jack": "Jumping Jack",
    "lunge": "Lunge",
    "plank": "Plank",
    "pushup": "Push-Up",
    "squat": "Squat",
}

# MediaPipe (33 joints) to COCO-17 Mapping for PoseC3D input
COCO_MP_MAP = [
    0,   # 0: nose
    2,   # 1: left_eye (MP 2)
    5,   # 2: right_eye (MP 5)
    7,   # 3: left_ear (MP 7)
    8,   # 4: right_ear (MP 8)
    11,  # 5: left_shoulder (MP 11)
    12,  # 6: right_shoulder (MP 12)
    13,  # 7: left_elbow (MP 13)
    14,  # 8: right_elbow (MP 14)
    15,  # 9: left_wrist (MP 15)
    16,  # 10: right_wrist (MP 16)
    23,  # 11: left_hip (MP 23)
    24,  # 12: right_hip (MP 24)
    25,  # 13: left_knee (MP 25)
    26,  # 14: right_knee (MP 26)
    27,  # 15: left_ankle (MP 27)
    28,  # 16: right_ankle (MP 28)
]
