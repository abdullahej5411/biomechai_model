# BioMechAI — Report #28: Final Graduation Handover & Permanent Cloud Architecture (v2.2)
## Complete FYP-II System State, Cloud Tunnel Infrastructure & Viva Demonstration Guide

**Document ID:** `28_2026-10-03_SYSTEM_FinalGraduationHandoverAndCloudArchitectureV2_2.md`  
**Date:** October 3, 2026  
**Target:** Semester 8 — FYP-II Final Graduation Evaluation (Degree Completion)  
**Author:** Abdullah Ejaz (Lead FYP Researcher) & Antigravity AI  
**Current Baseline APK:** [`BioMechAI_v2.2_PermanentCloudTunnel.apk`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/BioMechAI_v2.2_PermanentCloudTunnel.apk) (215.10 MB)  
**Active Production Model:** PoseC3D v5 Limb Heatmaps (`best_acc_top1_epoch_10.pth`, 8.33 MB)  
**Active Firebase Project:** `biomechai-fitness` (Project Number `479596177740`, Owner: `aejshah@gmail.com`)  
**Permanent Cloud Domain:** `https://persevere-kindred-tasty.ngrok-free.dev`  

---

## 1. Executive Summary & Purpose

This report marks the **official completion of all engineering, scientific, and deployment milestones** for the BioMechAI Final Year Project (FYP-II).

Every requirement set forth by the graduation panel and university evaluation guidelines has been fulfilled, verified with empirical evidence, and packaged for immediate live demonstration:
1. **Model Accuracy & Integrity**: The panel's mandate to implement and fine-tune a pretrained deep action recognition architecture has been achieved with **PoseC3D SlowOnly-R50 v5 (Limb Heatmaps)**, reaching **`53.38%` Top-1 Accuracy**, **`53.15%` Macro Recall**, and **`91.22%` Top-5 Accuracy** on a strictly frozen 115 held-out videos zero-leakage test set.
2. **All 9 Modules Code Complete**: From authentication and 3D pose detection to on-device voice coaching, body anthropometry scanning, clinical injury prevention across all 7 movements, and a synchronized React coach portal.
3. **Zero-Config Remote Connectivity**: Eliminated manual Wi-Fi IP configuration through a permanent, static cloud tunnel (`persevere-kindred-tasty.ngrok-free.dev`) paired with a 1-click launcher (`run_cloud_server.bat`) and compiled into the production baseline APK (`BioMechAI_v2.2_PermanentCloudTunnel.apk`).

---

## 2. Definitive Status of the 9 FYP Modules

| Module # | Module Name | Deliverable Status | Verification Evidence |
|:---:|---|:---:|---|
| **Module 1** | **User Registration & Login** | **100% Complete** | Flutter Firebase Auth with role routing (`user` vs `trainer`), forgot password, password toggle. |
| **Module 2** | **Real-time 3D Pose Detection** | **100% Complete** | Google ML Kit on-device at 30 FPS producing 33 normalized landmark coordinates. |
| **Module 3** | **Exercise Recognition & Classification** | **100% Complete** | PoseC3D SlowOnly-R50 fine-tuned on FineGYM athletic limb weights. Certified: **53.38% Top-1**, **53.15% Macro Recall**, **91.22% Top-5** (444 clips / 115 held-out videos). |
| **Module 4** | **Real-time Rep Counting & Validation** | **100% Complete** | Closed 4-Stage Rep FSM (`UPRIGHT` $\to$ `DESCENDING` $\to$ `BOTTOM` $\to$ `ASCENDING` $\to$ `COMPLETED`), zero-clamp depth, boundary occlusion rejection. |
| **Module 5** | **Posture Correctness (7 Exercises)** | **100% Complete** | Real-time kinematic checks across all 7 exercises (squat depth, lunge stride, push-up depth, plank line, bicep curl drift, high knees height, jumping jack stability). |
| **Module 6** | **Body Measurement & Transformation** | **100% Complete** | 3-Tab Architecture: Manual Log + BMI gauge, Progress weight history bar chart, and Camera Body Scan with MediaPipe pixel-ruler anthropometry measuring Shoulder, Hip, Torso, and Arm Span in cm. |
| **Module 7** | **AI Clinical Injury Prevention (7 Exercises)**| **100% Complete** | Evaluates dynamic knee valgus (Munro FPPA $<165^\circ$ for ACL tear risk), lumbar compression (push-up hip sag $>10\%$), rotator cuff impingement (elbow flare $>65^\circ$), lumbar hyperextension (plank line $<162^\circ$). |
| **Module 8** | **AI Workout Companion with Voice** | **100% Complete** | Native on-device TTS (`flutter_tts`) with 3.0s watchdog, priority preemption, debouncing cooldowns (3.5s warnings, 5.0s recovery praise). |
| **Module 9** | **Trainer Dashboard (Coach Portal)** | **100% Complete** | React + Vite + Tailwind web app unified to `biomechai-fitness` Firebase. Features KPI cards, area chart progression, monthly attendance calendar, rep fault log, and instant athlete messenger. |

---

## 3. Permanent Cloud Architecture & Deployment (v2.2)

### 3.1 Why Permanent Cloud Tunnel Replaced Prior Approaches
1. **Render Free Tier Limitations**: Render's free tier has a 512 MB RAM ceiling, causing PyTorch PoseC3D models to trigger Out-Of-Memory (OOM) fatal kills.
2. **Hugging Face Spaces Compute Paywall**: Hugging Face recently restricted Docker/Gradio compute hardware spaces to paid plans, preventing free deployment.
3. **Local Wi-Fi IP Fragility**: Hardcoding local IPv4 addresses (e.g., `192.168.1.192`) fails whenever the laptop joins university Wi-Fi or changes routers, requiring manual IP lookup and re-compiling.
4. **The Verified Permanent Solution**: A permanent static domain on ngrok (`persevere-kindred-tasty.ngrok-free.dev`) tunnelled directly to local FastAPI port 8000 via [`run_cloud_server.bat`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/run_cloud_server.bat).

### 3.2 Technical Implementation Details
- **FastAPI Backend (`backend/main.py`)**:
  - Serves dual timescales: REST (`POST /classify`) for exercise recognition and WebSockets (`/ws/stream`) for 30 Hz repetition and clinical telemetry streaming.
  - Automatically loads PoseC3D v5 Limb Heatmaps (`best_acc_top1_epoch_10.pth`).
- **Dynamic Mobile Routing (`server_config.dart`)**:
  - Automatically routes `https://persevere-kindred-tasty.ngrok-free.dev` for REST endpoints and `wss://persevere-kindred-tasty.ngrok-free.dev/ws/stream` for WebSocket streaming.
  - Automatically migrates existing installs from legacy `192.168.1.192` caches.
  - Retains in-app settings dialog for manual local Wi-Fi entry if running in airplane/offline mode.
- **ngrok Interstitial Bypass**:
  - Injected `'ngrok-skip-browser-warning': 'true'` header on all HTTP calls (`/classify` POST and `/health` GET pings) to ensure requests pass directly to the AI engine without browser warning interstitials.

---

## 4. Academic Defense & Viva Demonstration Playbook

### Step 1: Start the Backend (Laptop)
1. Double-click [`run_cloud_server.bat`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/run_cloud_server.bat).
2. The batch script activates Python virtual environment `venv`, starts FastAPI on port 8000, and connects ngrok to `persevere-kindred-tasty.ngrok-free.dev`.
3. In a browser or terminal, verify health:
   `curl https://persevere-kindred-tasty.ngrok-free.dev/health` $\to$ Returns `{"status": "healthy", "model": "PoseC3D-v5-SlowOnly-R50"}`.

### Step 2: Run the Mobile Application (Phone)
1. Install [`BioMechAI_v2.2_PermanentCloudTunnel.apk`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/BioMechAI_v2.2_PermanentCloudTunnel.apk) on the Android phone.
2. Open the app — it connects automatically to the cloud tunnel without requiring any IP configuration.
3. **Demonstrating Modules 3, 4, 5, 7, 8 (Live Workout)**:
   - Select Squat (or Push-up, Bicep Curl).
   - Perform reps in front of the camera:
     * Watch the real-time repetition state machine (`UPRIGHT` $\to$ `DESCENDING` $\to$ `BOTTOM` $\to$ `ASCENDING` $\to$ `COMPLETED`).
     * Purposefully cave knees inward to trigger the dynamic knee valgus ACL warning (Munro FPPA $<165^\circ$).
     * Listen to the real-time native TTS voice coach: *"Push your knees outward!"*
4. **Demonstrating Module 6 (Body Measurement Tracking)**:
   - Navigate to the Body Measurements screen.
   - Show Tab 1: Enter height and weight to view real-time BMI gauge and Devine ideal weight formula.
   - Show Tab 2: View historical weight progression bar chart.
   - Show Tab 3: Perform a Camera Body Scan to demonstrate MediaPipe pixel-ruler anthropometry measuring Shoulder Width, Hip Width, Torso Length, and Arm Span in cm.
5. **Demonstrating Module 9 (Coach Portal)**:
   - Open the web dashboard at `https://biomechai-fitness.web.app` (or run locally in `web_dashboard/`).
   - Log in as trainer. Show the athlete's workout session appearing instantly in Firestore with rep-by-rep fault logs and form score progression.

---

## 5. Artifact & Repository Verification Manifest

- **Model Weights**: `models/posec3d_v5_limb/best_acc_top1_epoch_10.pth` (8.33 MB)
- **Model Config**: `models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py`
- **1-Click Startup Launcher**: `biomechai_model/run_cloud_server.bat`
- **Current Baseline APK**: `biomechai_model/BioMechAI_v2.2_PermanentCloudTunnel.apk` (~215.1 MB)
- **Model Git Repository**: `https://github.com/abdullahej5411/biomechai_model.git` (`main` branch)
- **Flutter & Dashboard Git Repository**: `https://github.com/abdullahej5411/BioMechAI.git` (`master` branch)
- **Firebase Project**: `biomechai-fitness` (Project Number `479596177740`)
