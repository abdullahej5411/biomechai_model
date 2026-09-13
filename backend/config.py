"""
BioMechAI Backend Configuration
Holds all validated biomechanical constants, model paths, and class mappings.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Strict Biomechanical Coded Constants (No ambiguous ranges)
BOTTOM_DEPTH_THRESHOLD     = 100.0  # Deg: Knee flexion must drop below this to register valid bottom
TOP_RETURN_THRESHOLD        = 155.0  # Deg: Knee flexion must return above this single exact threshold
VALGUS_LOAD_THRESHOLD       = 130.0  # Deg: Dynamic knee valgus evaluated only when joint is loaded
VALGUS_FPPA_THRESHOLD       = 165.0  # Deg: Munro et al. 2012 clinical diagnostic cutoff for knee valgus
KNEE_FLEXION_SANITY_FLOOR   = 35.0   # Deg: Anatomical limit of human knee flexion; rejects 2D occlusion glitches

# Model Weights & Config Paths
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
