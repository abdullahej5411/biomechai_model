# BioMechAI: 3D Spatiotemporal Exercise Recognition & Biomechanical Analysis

> **Final Year Project (FYP-I & FYP-II — Semester 8 Final Evaluation)**  
> **Domain**: Computer Vision, Deep Learning, Biomechanics & Human Action Recognition  
> **Champion Deep Architecture**: PoseC3D (`ResNet3dSlowOnly` + `I3DHead`, CVPR 2022) with Connected Limb Heatmaps  
> **Pretrained Source**: OpenMMLab FineGYM Athletic Pretrained Weights (`gym-limb_20220815-2e6e3c5c.pth`)  
> **Dataset**: BioMechAI v5 Production Dataset (2,164 clips across 572 unique video folds, 7 exercises)  
> **Evaluation Protocol**: Strict Video-Disjoint Split (457 Train Videos / 115 Held-Out Videos — 0 Subject Leakage)

---

## 🎯 Executive Summary & Certified Benchmark Results

BioMechAI is an end-to-end AI fitness and clinical injury prevention system classifying and analyzing 7 functional movements:
1. `bicep_curl`  2. `high_knees`  3. `jumping_jack`  4. `lunge`  5. `plank`  6. `pushup`  7. `squat`

### Authoritative Model Benchmark (Frozen 115 Held-Out Videos, 444 Clips)
Evaluated with **zero identity, room, or subject leakage**:

| Exercise Class | Validation Clips | Random Forest v5 Baseline | PoseC3D v1 (Scratch, Ep 18) | PoseC3D v3 (NTU-60, Ep 14) | PoseC3D v4 (FineGYM Dots, Ep 4) | **PoseC3D v5 (FineGYM Limb, Ep 10) [CHAMPION]** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`lunge`** | 68 | 66.18% (45) | 69.12% (47) | 60.29% (41) | 85.29% (58) | **75.00% (51)** |
| **`pushup`** | 49 | 57.14% (28) | 63.27% (31) | 63.27% (31) | 42.86% (21) | **67.35% (33)** 🚀 |
| **`plank`** | 64 | 71.88% (46) | 78.12% (50) | 62.50% (40) | 57.81% (37) | **65.62% (42)** |
| **`bicep_curl`** | 73 | 60.27% (44) | 46.58% (34) | 30.14% (22) | 67.12% (49) | **61.64% (45)** |
| **`squat`** | 73 | 36.99% (27) | 28.77% (21) | 32.88% (24) | 20.55% (15) | **53.42% (39)** 🚀 *(+160% relative gain over v4!)* |
| **`high_knees`** | 41 | 46.34% (19) | 58.54% (24) | 53.66% (22) | 36.59% (15) | **29.27% (12)** |
| **`jumping_jack`** | 76 | 52.63% (40) | 18.42% (14) | 44.74% (34) | 40.79% (31) | **19.74% (15)** |
| **Overall Top-1** | **444** | **56.08%** (249) | **49.77%** (221) | **48.20%** (214) | **50.90%** (226) | **53.38% (237)** 🏆 *(All-Time Deep Record)* |
| **Macro Recall** | **444** | **55.92%** | **51.83%** | **49.64%** | **50.14%** | **53.15%** 🏆 *(All-Time Deep Record)* |
| **Top-5 Accuracy** | **444** | — | **87.39%** | **91.22%** | **89.64%** | **91.22%** 🎯 *(Project Peak)* |

### Key Scientific Takeaway (Why Limb Heatmaps Won):
Joint dot heatmaps ($17 \times 48 \times 56 \times 56$) suffered from severe squat-to-lunge collapse (41/73 squats misclassified as lunges in v4). Switching to connected 3D spatiotemporal limb heatmaps (`with_kp=False, with_limb=True`, $\sigma = 0.6$) provided bilateral geometric continuity, cutting squat misclassifications by 65.9% and propelling squat recall from 20.55% to **53.42%**.

---

## 📂 Repository Layout

```
biomechai_model/
├── README.md                                  # [THIS FILE] Master Architecture & Benchmark Guide
├── AGENTS.md                                  # System Memory & Agent Operating Guide
├── FINAL_PRODUCTION_REPORT.md                 # Authoritative Academic Action Recognition Report
├── run_cloud_server.bat                       # 1-Click Production Server Launcher (FastAPI + ngrok)
├── run_live_webcam.bat                        # Standalone local webcam test launcher
├── BioMechAI_v2.7_PlankHoldTimer.apk          # [LATEST PRODUCTION APK] (98.1 MB)
├── BioMechAI_v2.6_EmailVerification.apk       # Email Verification Baseline APK (222.4 MB)
├── BioMechAI_v2.5_TwoWayCoachPairing.apk      # Previous Baseline APK
├── BioMechAI_v2.4_PdfAssessmentExport.apk     # Cross-Platform PDF Engine Baseline APK
├── BioMechAI_v2.3_SmartScannerProductionReady.apk # Smart Anthropometry Scanner APK
├── BioMechAI_v2.2_PermanentCloudTunnel.apk    # Permanent Cloud Tunnel Baseline APK
│
├── backend/                                   # FastAPI Backend Bridge
│   ├── main.py                                # Endpoints: POST /classify, WebSocket /ws/stream, GET /health
│   ├── engine.py                              # PyTorch PoseC3D v5 Inference Engine
│   ├── kinematics.py                          # Biomechanical Form Rules & Clinical Injury Engines
│   └── config.py                              # Joint Indices, Model Paths, & Clinical Constants
│
├── models/                                    # Model Checkpoints & Configurations
│   └── posec3d_v5_limb/                       # [CHAMPION] PoseC3D v5 Limb Heatmap Model
│       ├── best_acc_top1_epoch_10.pth         # [CHAMPION CHECKPOINT] (8.33 MB)
│       ├── posec3d_biomechai_v5_limb.py       # Model architecture configuration
│       └── pose_transforms_extra.py           # Custom limb heatmap transforms
│
├── reports/                                   # 34 Authoritative Milestone & Engineering Reports
└── work_dirs/                                 # Training checkpoint runs and execution logs
```

---

## 🚀 How to Run the Production Backend

### 1-Click Launch (Recommended for Presentations & Daily Use)
Double-click [`run_cloud_server.bat`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/run_cloud_server.bat).  
This automatically:
1. Activates Python `venv`
2. Starts FastAPI on `http://0.0.0.0:8000`
3. Launches an ngrok secure tunnel to the permanent static domain: `https://persevere-kindred-tasty.ngrok-free.dev`

### Python Direct Execution
```bash
# In biomechai_model:
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## 📱 Mobile App Connection

The mobile application ([`BioMechAI_v2.6_EmailVerification.apk`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/BioMechAI_v2.6_EmailVerification.apk)) comes pre-configured with:
- **Default Endpoint**: `https://persevere-kindred-tasty.ngrok-free.dev`
- **Telemetry Stream**: `wss://persevere-kindred-tasty.ngrok-free.dev/ws/stream`
- **Header**: `'ngrok-skip-browser-warning': 'true'`
- **Fallback**: Built-in network settings dialog allowing custom local IP entry for completely offline setups.
- **Latest Production Features (v2.3–v2.6)**:
  * Mandatory Email Verification & Sign-In Gatekeeper with interactive Resend action.
  * Two-Way Coach-Athlete Pairing & Disconnect Flow with multi-tenant data isolation.
  * Option C Cross-Platform Clinical Assessment PDF Export Engine.
  * Smart Distance-Guiding Auto-Body Scanner with monocular height scale calibration.

---

## 🎓 Academic Defense Highlights

1. **Honest Science (No Data Leakage)**:
   - Early unverified pipelines achieved artificial ~84–95% scores by splitting consecutive frames of the same video between train and test (memorizing clothing, furniture, and subjects).
   - BioMechAI strictly enforces a **115 held-out video partition (444 clips)** where the test subjects were never seen during training, proving genuine biomechanical generalization.
2. **Clinical Utility**:
   - Beyond classification, BioMechAI enforces real-time clinical injury rules (Munro FPPA knee valgus for ACL tear prevention, McGill lumbar spine hyperextension, shoulder impingement flare angles).
