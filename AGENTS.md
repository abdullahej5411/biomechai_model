# BioMechAI — Official FYP-II Final Graduation System Memory

## CRITICAL PROJECT CONTEXT: SEMESTER 8 (FYP-II FINAL DEFENSE)
- **Current Phase**: **Semester 8 — Final Evaluation (FYP-II)**.
- **ABSOLUTE RULE 1**: **THERE IS NO NEXT SEMESTER**. This is the final graduation evaluation. We must NEVER say "reserved for FYP-II" or "planned for next semester" because we ARE in FYP-II right now.
- **ABSOLUTE RULE 2 (CHAMPION MODEL ACCURACY TRUTH)**:
  - **The Active Production Model is PoseC3D v5 (Limb Heatmaps)**.
  - Checkpoint: `models/posec3d_v5_limb/best_acc_top1_epoch_10.pth` (8.33 MB).
  - Config: `models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py`.
  - Loaded in: `backend/config.py` (lines 18–19) and `backend/engine.py`.
  - Pretrained Source: OpenMMLab official FineGYM athletic limb weights (`gym-limb_20220815-2e6e3c5c.pth`).
  - Heatmap Modality: Connected 3D Spatiotemporal Limb Heatmaps (`with_kp=False, with_limb=True`, $\sigma = 0.6$).
  - **TRUE BENCHMARK ACCURACY**:
    - **Top-1 Accuracy**: **`53.38%`** (237/444 clips on strictly frozen 115 held-out videos zero-leakage split).
    - **Macro Recall**: **`53.15%`**.
    - **Top-5 Accuracy**: **`91.22%`**.
  - **NEVER GET CONFUSED ABOUT OLD EXPERIMENTS**:
    - Do NOT say "accuracy is 50.90%" — that was the old v4 keypoints (dot heatmaps) model.
    - Do NOT propose "retrain with limb heatmaps" — limb heatmaps were ALREADY trained on Kaggle and produced this v5 champion!
    - Do NOT quote the old FYP-I 84% Random Forest number as current — that 84% was due to clip-level data leakage (memorizing subjects). Under honest video-disjoint evaluation, RF dropped to 56.08% and PoseC3D stands at 53.38% Top-1 / 91.22% Top-5.
- **ABSOLUTE RULE 3 (MODULE 7 IS NOT JUST ACL)**:
  - Module 7 covers **clinical injury prevention across ALL 7 exercises**, not just ACL.
  - Implemented in `backend/kinematics.py` and `form_validation_service.dart`.
- **ABSOLUTE RULE 4 (FIREBASE UNIFICATION)**:
  - Active Firebase Project: **`biomechai-fitness`** (Project Number `479596177740`, Owner: `aejshah@gmail.com` / `abdullahej5411`).
  - Both Flutter mobile app and Coach Web Dashboard (`web_dashboard/src/firebase.ts`) are unified to `biomechai-fitness`.

---

## THE 9 OFFICIAL FYP MODULES & CURRENT FYP-II STATUS

1. **Module 1: User Registration and Login** (Done in FYP-I)
   - Status: 100% Completed (Flutter, Firebase Auth, role-based routing for `user` vs `trainer`).
2. **Module 2: Real-time 3D Pose Detection** (Done in FYP-I)
   - Status: 100% Completed (Google ML Kit on-device, 30 FPS, $33 \times 3$ normalized coordinates).
3. **Module 3: Exercise Recognition and Classification** (FYP-II Deliverable per Panel Mandate)
   - Status: **100% Code Complete & Benchmark Certified**.
   - Model: PoseC3D SlowOnly ResNet-50 fine-tuned on FineGYM limb heatmaps (`models/posec3d_v5_limb/best_acc_top1_epoch_10.pth`).
   - Official Metrics: **`53.38%` Top-1 Accuracy**, **`53.15%` Macro Recall**, and **`91.22%` Top-5 Accuracy** on 115 held-out videos (444 clips, strictly zero leakage).
   - Per-Class Breakdown: Lunge 75.00%, Push-Up 67.35%, Plank 65.62%, Bicep Curl 61.64%, Squat 53.42%, High Knees 29.27%, Jumping Jack 19.74%.
   - Demo Strategy: Use the app's manual dropdown picker for seamless live demonstrations (Squat, Pushup, Curl) while citing the 91.22% Top-5 benchmark for Module 3.
4. **Module 4: Real-time Rep Counting and Form Validation** (Upgraded for FYP-II)
   - Status: **100% Code Complete & Validated**.
   - Closed 4-Stage Rep FSM (`UPRIGHT` $\rightarrow$ `DESCENDING` $\rightarrow$ `BOTTOM` $\rightarrow$ `ASCENDING` $\rightarrow$ `COMPLETED`), zero-clamping, sustained boundary occlusion rejection.
5. **Module 5: Posture Correctness (Form Correction Across 7 Exercises)** (FYP-II Deliverable)
   - Status: **100% Code Complete & Kinematics Certified**.
   - Real-time kinematic checks for all 7 exercises: sagittal depth, spine alignment, elbow flare, arm drift, knee height, torso lean.
6. **Module 6: Body Measurement and Transformation Tracking** (FYP-II Deliverable)
   - Status: **100% Completed**.
   - 3-Tab Architecture:
     1. *Log*: Manual weight/height entry, live color-coded BMI gauge, Devine Formula ideal weight range.
     2. *Progress*: Weight history bar chart + transformation delta tracking.
     3. *Camera Body Scan*: MediaPipe pixel-ruler anthropometry calculating Shoulder Width, Hip Width, Torso Length, and Arm Span in cm using entered height as the calibration anchor. Saves to Firestore `body_scan_measurements`.
7. **Module 7: AI Clinical Injury Prediction (All 7 Exercises)** (FYP-II Deliverable)
   - Status: **100% Operational & Biomechanically Certified**.
   - Matrix of Clinical Injury Rules:
     * **Squat & Lunge**: Dynamic Knee Valgus (Munro et al. 2012 FPPA $< 165.0^\circ$) $\rightarrow$ ACL tear & patellofemoral syndrome risk.
     * **Push-Up**: Hip Sag ($>10\%$ below line) $\rightarrow$ Lumbar compression risk; Elbow Flare ($>65.0^\circ$) $\rightarrow$ Shoulder impingement & rotator cuff tear risk.
     * **Plank**: Hip Sag (Body Line $<162.0^\circ$ McGill 2010 standard) $\rightarrow$ Lumbar spine hyperextension risk.
     * **Bicep Curl**: Upper Arm Drift ($>30.0^\circ$) $\rightarrow$ Anterior shoulder impingement; Torso Swing ($>20.0^\circ$) $\rightarrow$ Lumbar hyperextension strain.
     * **High Knees**: Forward Torso Lean ($>15.0^\circ$) $\rightarrow$ Hip flexor overload & spine strain.
     * **Jumping Jack**: Lateral Torso Lean ($>12.0^\circ$) $\rightarrow$ Asymmetric joint loading & lateral spine strain.
8. **Module 8: AI Workout Companion with Voice Coaching** (FYP-II Deliverable)
   - Status: **100% Operational & Architecture Hardened**.
   - Edge-triggered `VoiceCoachingEngine` with priority preemption, debouncing cooldowns (3.5s warnings, 5.0s recovery praise), and on-device native `flutter_tts` with 3.0s watchdog.
9. **Module 9: Trainer Dashboard (Coach Portal)** (Demonstrated in FYP-I, Unified in FYP-II)
   - Status: **100% Operational & Live on Firebase**.
   - Architecture:
     * Athlete Mobile App (`biomechai_flutter_latest`) sends telemetry to Firebase Firestore (`biomechai-fitness`).
     * Trainer Web Portal (`web_dashboard/`, React + Vite + Tailwind + Recharts) connects directly to `biomechai-fitness`.
     * Live Host: Deployable via `npx firebase-tools deploy --only hosting` to `https://biomechai-fitness.web.app` (previously on `biomechai.web.app`).
     * Coach Views:
       1. Overview KPI Cards (Total Workouts, Avg Form Score, Total Valid Reps).
       2. Form Progression Area Chart (`recharts`) tracking score trends across chronological sessions.
       3. Interactive Monthly Workout Calendar (`react-calendar`) with green attendance indicator dots.
       4. Granular Rep-by-Rep Fault Breakdown Table (Rep #, Valid/Invalid, Form Score, exact biomechanical fault detected).
       5. Direct Feedback Messenger: Coach writes notes and delivers instant feedback to the athlete's phone.

---

## BACKEND & DEPLOYMENT ARCHITECTURE

- **Backend Code Location**: `backend/`
  - `main.py`: FastAPI server (`POST /classify`, `GET /health`, `WebSocket /ws/stream`, `GET /pair`, `GET /latency_test`).
  - `engine.py`: `PoseC3DEngine` loading `best_acc_top1_epoch_10.pth` on PyTorch.
  - `kinematics.py`: Deterministic biomechanical physics and clinical injury detection.
  - `config.py`: Joint indices and clinical angle constants.
- **Hosting Options**:
  - Local Wi-Fi: `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000`.
  - Tunnel (Any Network): `cloudflared tunnel --url http://localhost:8000` (or `ngrok http 8000`).
  - 24/7 Cloud: Hugging Face Spaces (Docker, Basic CPU tier gives **16 GB RAM** free, preventing Render 512MB OOM crashes; kept awake with UptimeRobot ping to `/health`).

---

## MANDATORY APK SEQUENTIAL NAMING CONVENTION
- All newly compiled or updated APKs MUST follow strict semantic sequential naming:
  `BioMechAI_v<Major>.<Minor>_<FeatureTag>.apk`
  - Current baseline: `BioMechAI_v2.1_Module6CameraComplete.apk`
  - Previous baseline: `BioMechAI_v2.0_AllModulesComplete.apk`
  - Next update: `BioMechAI_v2.2_<FeatureTag>.apk`, then `v2.3`, etc.
- Never overwrite without leaving the clear sequential version tag so the user is never confused about which APK is latest.
