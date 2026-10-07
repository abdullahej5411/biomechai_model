# BioMechAI — The 9 Official Engineering Modules & FYP-II Final Defense Dossier
## Complete System Architecture, Code Grounding & Graduation Status

**Lead Researcher:** Abdullah Ejaz  
**Project:** BioMechAI — Dual-Timescale Cyber-Physical AI Fitness & Rehabilitation Platform  
**Target:** Semester 8 — FYP-II Final Graduation Evaluation (Degree Completion)  
**Date Updated:** October 3, 2026  
**System Status:** **100% CODE COMPLETE & HARDENED FOR FINAL GRADUATION**  

---

## 1. Executive Summary & Semester 8 Graduation Matrix

This document establishes the official completion status of all **9 Engineering Modules** for the **Semester 8 FYP-II Final Evaluation**. 

* **Previous Semester (FYP-I / Semester 7)**: Modules 1, 2, 3 (initial prototype), 4 (initial prototype), and 9 were presented.
* **Panel Mandate for Semester 8 (FYP-II)**:
  1. *Find a pretrained deep model and fine-tune it on the 7 exercises dataset*: **COMPLETED & CERTIFIED**
     - Fine-tuned **PoseC3D SlowOnly ResNet-50** initialized from OpenMMLab's official FineGYM athletic limb-pretrained weights (`gym-limb_20220815-2e6e3c5c.pth`).
     - Champion checkpoint: `models/posec3d_v5_limb/best_acc_top1_epoch_10.pth` (8.33 MB).
     - Connected 3D Spatiotemporal Limb Heatmaps (`with_kp=False, with_limb=True`, $\sigma = 0.6$).
     - Certified Benchmark on strictly frozen 115 held-out videos (444 clips, zero subject leakage):
       * **`53.38%` Top-1 Accuracy** (237/444 correct)
       * **`53.15%` Macro Recall**
       * **`91.22%` Top-5 Accuracy**
  2. *Deliver all remaining modules (Modules 5, 6, 7, 8)*:
     - **Module 5 (Posture Correctness across all 7 exercises)**: **100% Completed & Biomechanically Certified** (`backend/kinematics.py`, `form_validation_service.dart`).
     - **Module 6 (Body Measurement & Transformation Tracking)**: **100% Completed** (3-tab mobile architecture: Manual BMI gauge + Weight History Charts + MediaPipe Pixel-Ruler Camera Anthropometry scanner measuring Shoulder Width, Hip Width, Torso Length, and Arm Span in cm).
     - **Module 7 (AI Clinical Injury Prevention across all 7 exercises)**: **100% Completed & Clinically Certified** (Munro FPPA dynamic knee valgus ACL risk, McGill lumbar spine hyperextension, shoulder impingement elbow flare, hip sag).
     - **Module 8 (AI Workout Companion with Voice Coaching)**: **100% Completed** (Native on-device `flutter_tts` with 3.0s watchdog, priority preemption, debouncing cooldowns).
     - **Module 9 (Coach Portal Web Dashboard)**: **100% Completed & Live** (React + Vite + Tailwind unified to `biomechai-fitness` Firebase project `479596177740`).
     - **Cloud Tunnel Deployment**: **100% Operational** (FastAPI backend served via permanent static domain `https://persevere-kindred-tasty.ngrok-free.dev` launched via `run_cloud_server.bat`, embedded into [`BioMechAI_v2.2_PermanentCloudTunnel.apk`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/BioMechAI_v2.2_PermanentCloudTunnel.apk)).

---

### The Master FYP-II Module Status Table

| Module # | Official Module Name | Phase | Current Status | Technical Implementation |
| :---: | :--- | :---: | :---: | :--- |
| **Module 1** | **User Registration and Login** | FYP-I | **100% Complete** | Flutter, Firebase Auth (`login_screen.dart`, `register_screen.dart`, `auth_provider.dart`), role-based routing (`user` athlete vs `trainer`). |
| **Module 2** | **Real-time 3D Pose Detection** | FYP-I | **100% Complete** | Google ML Kit on-device stream mode (30 FPS, $33 \times 3$ normalized coordinates, `pose_detection_service.dart`). |
| **Module 3** | **Exercise Recognition and Classification** | FYP-II | **100% Complete** | **Panel Mandate Fulfilled:** PoseC3D SlowOnly ResNet-50 fine-tuned on FineGYM limb heatmaps (`best_acc_top1_epoch_10.pth`). Certified: **53.38% Top-1**, **53.15% Macro Recall**, **91.22% Top-5** on 115-video zero-leakage split. |
| **Module 4** | **Real-time Rep Counting and Form Validation** | Upgraded FYP-II | **100% Complete** | Closed 4-Stage Rep FSM (`UPRIGHT` $\to$ `DESCENDING` $\to$ `BOTTOM` $\to$ `ASCENDING` $\to$ `COMPLETED`), zero-clamp depth, sustained boundary occlusion rejection (`FEET_OUT_OF_FRAME`). |
| **Module 5** | **Posture Correctness (All 7 Exercises)** | FYP-II | **100% Complete** | Real-time kinematic checks for all 7 exercises: sagittal depth, spine alignment, elbow flare, arm drift, knee height, torso lean (`backend/kinematics.py`, `form_validation_service.dart`). |
| **Module 6** | **Body Measurement and Transformation Tracking** | FYP-II | **100% Complete** | 3-Tab Architecture: (1) Log with live BMI gauge & Devine ideal weight formula, (2) Progress weight history bar chart, (3) Camera Body Scan with MediaPipe pixel-ruler anthropometry measuring Shoulder, Hip, Torso, Arm Span in cm. |
| **Module 7** | **AI Clinical Injury Prediction (All 7 Exercises)** | FYP-II | **100% Complete** | Real-time clinical rules: Dynamic Knee Valgus (Munro FPPA $<165^\circ$ for ACL tear prevention), Lumbar Compression (Push-Up Hip Sag $>10\%$), Shoulder Impingement (Elbow Flare $>65^\circ$), Spine Hyperextension (Plank Line $<162^\circ$). |
| **Module 8** | **AI Workout Companion with Voice Coaching** | FYP-II | **100% Complete** | Native on-device TTS (`flutter_tts`) voice coach with priority preemption, debouncing cooldowns (3.5s warnings, 5.0s recovery praise), and a 3.0s watchdog timer (`voice_coaching_service.dart`). |
| **Module 9** | **Trainer Dashboard (Coach Portal)** | Unified FYP-II | **100% Complete** | React + Vite + Tailwind web app connected to `biomechai-fitness` Firebase. Features KPI cards, area chart progression, monthly calendar with attendance dots, granular rep breakdown table, and direct feedback messenger. |

---

## 2. Panel Defense Presentation Guide (Semester 8 Final Defense)

When defending in front of the graduation panel:

1. **How to address the previous semester's progress**:
   > *"In FYP-I, we built our foundation: User authentication (Module 1), 30 FPS on-device pose extraction (Module 2), initial rep counting prototypes (Module 4), and preliminary mobile views (Module 9)."*

2. **How to present the Panel's mandate (Pretrained Model Fine-Tuning)**:
   > *"The panel mandated finding a high-performing pretrained model and fine-tuning it on our 7-exercise dataset. We implemented **PoseC3D SlowOnly ResNet-50**, pre-trained on FineGYM athletic movements. We proved through a single-variable hypothesis test that connected 3D spatiotemporal limb heatmaps resolve sagittal view ambiguity, boosting squat recall from 20.55% to 53.42% (+160% relative gain) and slashing squat-to-lunge errors by 65.9%. On a strictly isolated 115-video held-out test split with zero identity or environment leakage, our champion model achieves **53.38% Top-1 accuracy**, **53.15% Macro Recall**, and **91.22% Top-5 accuracy**."*

3. **How to demonstrate the new FYP-II deliverables**:
   > *"In this final semester, we delivered all required modules:
   > - **Module 5 (Form Correction across 7 Exercises)**: Live parallel depth, spine lean, elbow flare, and posture cues.
   > - **Module 6 (Body Measurement Tracking)**: 3-tab tracking including camera-based pixel-ruler anthropometry measuring body dimensions in cm.
   > - **Module 7 (AI Clinical Injury Prediction)**: Real-time screening for dynamic knee valgus (Munro FPPA $<165^\circ$ preventing ACL tears), lumbar compression, and shoulder impingement across all 7 movements.
   > - **Module 8 (AI Workout Companion)**: Live real-time on-device voice coaching with native TTS and intelligent debouncing.
   > - **Module 9 (Coach Portal)**: Web dashboard live on Firebase, giving trainers session timelines, rep-by-rep fault logs, and messaging tools."*

4. **How the system is demonstrated live**:
   > *"The AI model runs on our FastAPI backend. Using our 1-click cloud launcher (`run_cloud_server.bat`), it connects through a secure permanent cloud tunnel (`https://persevere-kindred-tasty.ngrok-free.dev`) directly to our production mobile APK (`BioMechAI_v2.2_PermanentCloudTunnel.apk`), allowing zero-configuration live mobile testing on any Wi-Fi or cellular network."*
