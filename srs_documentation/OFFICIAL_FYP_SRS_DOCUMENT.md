# BioMechAI — Official Software Requirements Specification (SRS)
## Full Academic Transcript & Repository Copy

**University**: FAST – National University of Computer & Emerging Sciences, Chiniot-Faisalabad Campus  
**Department**: Department of Computer Science  
**Academic Year**: 2026 (Semester 8 — Final Year Project)  
**Project Title**: BioMechAI  
**Document Type**: Software Requirement Specification (SRS)  

### FYP Team
1. **Muhammad Abdullah** (Roll No: 22F-3444)
2. **Muhammad Abdul Hanan Nadeem** (Roll No: 22F-8762)
3. **Zainab Haider** (Roll No: 22F-8818)

### Supervision
* **Supervisor**: Mr. Mughees Ismail
* **Co-Supervisor**: Dr. Muhammad Usama

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Vision Document](#2-vision-document)
   - 2.1. Problem Statement
   - 2.2. Business Opportunities
   - 2.3. Objectives
   - 2.4. Scope
   - 2.5. Constraints
   - 2.6. Stakeholder and User Description
     - 2.6.1. Market Demographics
     - 2.6.2. User Environment
     - 2.6.3. Stakeholder Profiles
     - 2.6.4. Stakeholder Summary
3. [System Requirements Specification](#3-system-requirements-specification)
   - 3.1. System Features
   - 3.2. Functional Requirements
     - 3.2.1. Real-time 3D Pose Detection
     - 3.2.2. Exercise Recognition and Classification
     - 3.2.3. Real-time Rep Counting and Form Validation
     - 3.2.4. Posture Correctness
     - 3.2.5. Body Measurement and Transformation Tracking
     - 3.2.6. AI Injury Prediction
     - 3.2.7. AI Workout Companion with Voice Conversation
     - 3.2.8. Trainer Dashboard
   - 3.3. Non-Functional Requirements
     - 3.3.1. Performance
     - 3.3.2. Usability
     - 3.3.3. Reliability
     - 3.3.4. Security and Privacy
     - 3.3.5. Compatibility
4. [Project Artefacts](#4-project-artefacts)
   - 4.1. Use Case Models
   - 4.2. Structural Design (Domain Model, Class Diagram, Component Diagram)
   - 4.3. Behavioral Design (DFD Level 0/1, State Machine, Sequence Diagram)
   - 4.4. Maintenance Phase (Deployment Diagram)

---

## 1. Introduction
BioMechAI is created to solve an important problem in personal fitness: many people do not have an easy way to check whether they are performing exercises with the correct form in real time, which can increase the chances of workout-related injuries. This section introduces the main goals and reasons behind developing this system.

In addition, this Software Requirements Specification (SRS) clearly describes the system’s functional requirements (what the system should do) and non-functional requirements (how well the system should perform). It also includes the use case models and the guidelines for designing artifacts that will be used while building the BioMechAI system. For the final graduation evaluation (Semester 8), the project is structured into the following nine (9) comprehensive modules:
* **Module 1**: User Registration and Login
* **Module 2**: Real-time 3D Pose Detection
* **Module 3**: Exercise Recognition and Classification (PoseC3D Deep Learning Engine)
* **Module 4**: Real-time Rep Counting and Form Validation (Closed 4-Stage Rep FSM)
* **Module 5**: Posture Correctness (Four-Pattern Kinematic Form Engine)
* **Module 6**: Body Measurement and Transformation Tracking
* **Module 7**: AI Clinical Injury Prevention Engine
* **Module 8**: AI Workout Companion with Live Voice Coaching
* **Module 9**: Trainer Dashboard & Timestamped Feedback

---

## 2. Vision Document

### 2.1. Problem Statement
| Category | Description |
| :--- | :--- |
| **Problem** | • Personal training sessions are expensive, and many users cannot afford them, as a single session can cost a large amount of money.<br/>• Around 45% of people who go to the gym experience injuries because they perform exercises with the wrong form and there is no system to correct them instantly.<br/>• Most fitness applications only provide general workout plans. They are not personalized and do not give real-time 3D feedback about body movement during exercises. |
| **Affects** | • People of all fitness levels who want to exercise safely and improve their training.<br/>• The wider health and fitness community, including physiotherapists, fitness coaches, and sports medicine professionals. |
| **Impact** | • Leads to avoidable injuries, extra medical costs, and people training on their own without proper guidance.<br/>• Creates a gap in preventive health because there are very few affordable tools that combine movement analysis with personalized coaching. |
| **Solution** | An AI-powered personal fitness trainer that works on a smartphone and uses real-time movement analysis. The system will:<br/>• Provide real-time 3D pose correction and recognize the exercise being performed.<br/>• Automatically count repetitions while checking if the exercise form is correct using a 4-stage state machine.<br/>• Analyze movement patterns during workouts to predict acute and chronic injury risks in real time.<br/>• Include a real-time, on-device AI voice companion that delivers priority-preempted audio safety cues.<br/>• Work completely on normal smartphones so users do not need expensive or specialized equipment. |

### 2.2. Business Opportunities
BioMechAI aims to solve an important problem in accessible personal fitness while also creating a strong business opportunity. The system can support a premium subscription model for users and also allow partnerships with rehabilitation clinics, sports academies, and corporate wellness programs. Through these partnerships, this application can provide scalable AI-based coaching that analyzes body movement and exercise form.

### 2.3. Objectives
Following are the objectives of BioMechAI:
* Develop a real-time 3D pose detection system that runs smoothly on standard smartphones and accurately tracks user body landmarks at 30 FPS.
* Implement automatic exercise classification across seven (7) core gym exercises using a 3D spatiotemporal convolutional neural network (PoseC3D SlowOnly ResNet-50) pretrained on FineGYM and fine-tuned on the BioMechAI dataset.
* Provide a deterministic form validation system that evaluates movement patterns using vector kinematics against sports science literature, flagging movements that cause injury.
* Allow users to monitor physical transformation through an anthropometric measurement tracking feature, live Body Mass Index (BMI) computation, and the clinical Devine Ideal Body Weight formula.
* Build an AI-based clinical injury prevention system that detects acute kinetic failure in real time (e.g. Munro dynamic knee valgus $< 165^\circ$ for ACL risk, lumbar hip sag for spinal disc compression, and shoulder flare for impingement) while logging inter-session fatigue trends.
* Introduce an on-device AI voice companion that delivers sub-10ms priority-debounced audio coaching, rep announcements, and recovery encouragement.
* Provide certified personal trainers with a dedicated mobile dashboard to inspect client progress, review form compliance scores, and attach second-by-second timestamped coaching feedback.
* Utilize optimization methods so that pose estimation and form feedback execute in under 15 milliseconds on mid-range smartphones.

### 2.4. Scope
The scope of BioMechAI includes developing a complete personal fitness platform focusing on real-time 3D body movement analysis, deep learning exercise classification, clinical injury prevention, and on-device voice coaching. The system is architected as a high-performance Flutter mobile application communicating with a dedicated PyTorch/FastAPI backend server for spatiotemporal neural network evaluation.

### 2.5. Constraints
* All on-device AI processing (pose estimation, rep counting, kinematic form checking) must execute within 15ms per frame on mid-range devices (Snapdragon 720G or equivalent) to sustain 30 FPS.
* Deep learning spatiotemporal inference (PoseC3D) requires a GPU-enabled backend server (NVIDIA T4 or equivalent) for batched 3D convolutional tensor evaluations within 45ms.
* During academic testing, the Firebase free tier restricts the number of concurrent users to about 50-100 active users.
* Anthropometric body tracking relies on standardized vertical user camera framing and calibrated reference stature (height) for metric conversion.
* Acute injury prediction operates instantaneously on every single repetition using clinical kinematic angle cutoffs (e.g., Munro FPPA $< 165.0^\circ$ for knee valgus), while chronic overuse trends require cumulative multi-session logs.

### 2.6. Stakeholder and User Description

#### 2.6.1. Market Demographics
The primary target market for this app includes fitness-conscious individuals aged 16 to 45 who exercise on their own, either at home or in gyms, without regular access to personal trainers. Secondary markets include certified fitness trainers who want AI-assisted tools to manage and monitor clients, physiotherapists who use movement analysis for rehabilitation, and sports academies focused on tracking athletes’ form and performance. In Pakistan and South Asia, BioMechAI’s smartphone-based approach makes professional fitness guidance more affordable, helping users overcome economic barriers.

#### 2.6.2. User Environment
End users interact with BioMechAI through the Flutter mobile app on Android or iOS smartphones. They perform workouts in different settings such as homes, gyms, or outdoor spaces, with the phone placed 1.5-3 metres away on a stand or flat surface. Trainers access the system using the mobile Trainer Dashboard. Most AI processing happens directly on the device, while deep learning spatiotemporal classification uses local Wi-Fi or mobile data to communicate with the FastAPI server. If the internet connection is weak, the system continues to work by running all on-device pose estimation, rep counting, and form correction models offline.

#### 2.6.3. Stakeholder Profiles
* **Supervisor Team**: Mr. Mughees Ismail, Dr. Muhammad Usama (Academic direction, review, project progress).
* **Development Team**: Muhammad Abdullah, Muhammad Abdul Hanan Nadeem, Zainab Haider (Full SDLC, model training, mobile app, backend server).
* **End Users**: General public, fitness enthusiasts (Real-time form tracking, feedback).
* **Certified Trainers**: Professional fitness coaches (Client management, workout reviews, timestamped coaching).
* **Admin**: Backend management, Firebase/cloud monitoring, user account control.

---

## 3. System Requirements Specification

### 3.1. System Features
BioMechAI delivers the following core system features across its nine (9) verified production modules:
* **Module 1: User Registration and Login**: Multi-role authentication (Athlete vs. Trainer) using Firebase Auth and Cloud Firestore profile persistence.
* **Module 2: Real-time 3D Pose Detection**: Extracts 33 normalized 3D anatomical landmarks at 30 FPS using Google ML Kit BlazePose running natively on-device with custom low-latency visual skeleton overlays.
* **Module 3: Exercise Classification (PoseC3D Deep Learning Engine)**: Classifies user movement into seven (7) fundamental exercises using a 3D spatiotemporal ResNet-50 network fine-tuned on FineGYM limb heatmaps, achieving 91.22% Top-5 accuracy on held-out test splits.
* **Module 4: Real-time Rep Counting and Form Validation**: Employs a deterministic Closed 4-Stage Repetition Finite State Machine (START $\to$ INFLECTION $\to$ PEAK $\to$ COMPLETION) with un-clamped joint flexion and camera boundary occlusion rejection ($\ge 35^\circ$).
* **Module 5: Posture Correctness (Four-Pattern Kinematic Engine)**: Evaluates sagittal depth flexion, frontal knee alignment, trunk neutrality, and framing sanity in $< 0.1\text{ms}$ using clinically validated vector trigonometry.
* **Module 6: Body Measurement and Transformation Tracking**: Tracks user anthropometric dimensions, computes live BMI with color-coded classification gauges, determines physiological target weight using the Devine formula, and persists historical progress to Firestore.
* **Module 7: AI Clinical Injury Prevention Engine**: Real-time full-body injury guard monitoring Munro Dynamic Knee Valgus FPPA ($< 165^\circ$ under load $\le 130^\circ$) for acute ACL protection, lumbar hip sag ($> 10\%$) for spinal shear protection, and elbow flare ($> 65^\circ$) for rotator cuff impingement.
* **Module 8: AI Workout Companion with Live Voice Coaching**: Provides zero-latency, on-device audio coaching (`flutter_tts`) governed by a 3-tier priority queue (Priority 1: Emergency Safety Warnings, Priority 2: Rep Milestones, Priority 3: Form Praise) with dynamic cooldown debouncing.
* **Module 9: Trainer Dashboard & Timestamped Feedback**: A comprehensive coaching portal within the Flutter mobile app enabling certified trainers to inspect client rosters, review form scores, and leave second-by-second timestamped corrective notes.

### 3.2. Functional Requirements

#### 3.2.1. Real-time 3D Pose Detection
* Video capture at minimum 30 FPS via standard device camera.
* Detect 33 body landmarks with $(x, y, z)$ coordinates using Google ML Kit BlazePose.
* Render real-time neon skeleton overlay on the camera preview keeping total processing delay below 15ms.
* Temporal buffer of 48 frames for spatiotemporal movement classification.
* Utilize MediaPipe's relative z-depth coordinate estimates to measure sagittal-plane depth and forward torso inclination across standard monocular smartphone cameras.

#### 3.2.2. Exercise Recognition and Classification
* Automatically recognize seven (7) core athletic compound and isolation exercises: Squat, Push-Up, Lunge, Bicep Curl, Plank, Jumping Jack, and High Knees.
* Convert 48 consecutive frames of 17-channel COCO anatomical joint coordinates into spatiotemporal 3D limb heatmaps ($56 \times 56 \times 48$) with Gaussian tubular segments ($\sigma = 0.6$).
* Classify the spatiotemporal volume using a SlowOnly ResNet-50 3D convolutional neural network (PoseC3D) initialized with OpenMMLab FineGYM pretrained weights.
* Lock classification decisions when model softmax probability exceeds the calibrated deployment threshold ($T = 0.50$).
* Display the detected exercise name and dynamically activate exercise-specific kinematic rules.

#### 3.2.3. Real-time Rep Counting and Form Validation
* Implement a Closed 4-Stage Repetition Finite State Machine (FSM):
  1. `START`: Baseline standing posture ($\theta \ge 146.0^\circ$).
  2. `INFLECTION`: Descent phase initiated ($\theta < 146.0^\circ$).
  3. `PEAK`: Valid exercise depth attained (e.g., knee flexion $\le 115.0^\circ$ for squats, elbow flexion $\le 95.0^\circ$ for push-ups).
  4. `COMPLETION`: Full extension restored ($\theta \ge 146.0^\circ$), incrementing rep count by exactly +1.
* Repetitions failing to reach the required peak depth threshold shall be classified as partial/incomplete reps and rejected without incrementing the counter.
* Enforce an anatomical sanity floor ($\theta \ge 35.0^\circ$) to discard sudden optical occlusion glitches.
* Real-time on-screen display of completed repetition count, movement phase, and form compliance status.

#### 3.2.4. Posture Correctness (Four-Pattern Kinematic Engine)
* Evaluate exercise posture using a Four-Pattern Clinical Kinematic Vector Engine based on peer-reviewed biomechanical literature:
  1. **Sagittal Depth Flexion**: Measures target joint extension/flexion using vector dot products against gold-standard standards (Schoenfeld 2010, Escamilla 2001).
  2. **Frontal Plane Projection Angle (FPPA)**: Monitors medial-lateral deviation of the knee joint relative to the hip-ankle line (Munro et al. 2012).
  3. **Trunk and Spinal Neutrality**: Computes pelvic-shoulder angle relative to the gravity axis to detect compensatory lumbar hyperextension or excessive forward lean (McGill 2010).
  4. **Camera Framing Guards**: Filters out landmark estimates whenever key tracking joints intersect camera borders ($y > 0.94$).
* Render real-time color-coded skeleton feedback (green = acceptable form, red = kinematic violation) alongside corrective text overlays.

#### 3.2.5. Body Measurement and Transformation Tracking
* Provide an Anthropometric Body Measurement and Transformation Tracking interface.
* Calculate Body Mass Index (BMI) dynamically from recorded weight and height using the World Health Organization (WHO TRS 854) standard: $\text{BMI} = \text{weight (kg)} / (\text{height (m)})^2$.
* Render an interactive color-coded BMI gauge with medical classification bands: Underweight ($<18.5$, blue), Normal ($18.5\text{--}24.9$, green), Overweight ($25.0\text{--}29.9$, yellow), and Obese ($\ge 30.0$, red).
* Compute the user's physiological Ideal Body Weight (IBW) baseline using the clinical Devine Formula: $\text{IBW} = 50.0\text{ kg} + 2.3 \times (\text{height in inches} - 60) \pm 5.0\text{ kg}$.
* Persist longitudinal transformation logs in Cloud Firestore (`/users/{uid}/body_measurements`) and plot historical weight trends over time.

#### 3.2.6. AI Clinical Injury Prevention Engine
* Implement a Dual-Horizon AI Clinical Injury Prevention Engine protecting upper body, core/spine, and lower body joints across all 7 exercises:
  1. **Acute Knee Valgus / ACL Tear Risk (Squats & Lunges)**: Continuously evaluates Munro Frontal Plane Projection Angle ($\text{FPPA} = \arccos(\frac{\vec{u}_{HK} \cdot \vec{v}_{AK}}{\|\vec{u}\| \|\vec{v}\|})$). An acute alert is triggered when $\text{FPPA} < 165.0^\circ$ under active flexion load ($\le 130.0^\circ$), preventing non-contact ACL rupture (Munro 2012, Hewett 2005).
  2. **Lumbar Disc Shear & Compression Risk (Push-Ups & Planks)**: Calculates perpendicular orthogonal distance from hip joint to shoulder-ankle axis. Sagging exceeding $10\%$ of body length triggers an immediate spinal safety alert (McGill 2010).
  3. **Subacromial Shoulder Impingement Risk (Push-Ups)**: Measures humeral abduction angle relative to torso axis. Elbow flare exceeding $65.0^\circ$ triggers an acute warning to prevent supraspinatus tendon pinching (Flatow 1994, Cogley 2005).
  4. **Bicipital Tendon & Lumbar Strain Risk (Bicep Curls)**: Flags forward elbow drift $> 30.0^\circ$ and backward torso swing $> 20.0^\circ$.
  5. **Iliopsoas & Lower Back Compensation (High Knees)**: Flags excessive forward trunk lean $> 15.0^\circ$.
* Log cumulative repetitions performed with hazardous kinematics to assess longitudinal joint fatigue trends.

#### 3.2.7. AI Workout Companion with Live Voice Coaching
* Provide an on-device AI Voice Coaching Engine powered by `flutter_tts` operating completely offline with sub-10 millisecond latency.
* Audio cues shall be dispatched using a strict 3-tier Priority Preemption Queue:
  - **Priority 1 (Emergency Safety Alerts)**: Immediate voice override for acute injury risks (*"Push your knees out!"*, *"Lift your hips!"*, *"Tuck your elbows!"*).
  - **Priority 2 (Repetition Milestones)**: Auditory rep count announcements (*"Rep 5 completed"*).
  - **Priority 3 (Form Praise & Recovery)**: Positive encouragement when safe form is maintained or restored (*"Great depth, keep going!"*).
* Implement dynamic cooldown debouncing (minimum 2.5 seconds between duplicate cues) to prevent auditory flooding.
* Asynchronous 3.0-second hardware watchdog timer to monitor audio speech completion and prevent mobile audio channel deadlocks.

#### 3.2.8. Trainer Dashboard & Timestamped Feedback
* Specialized coaching portal within the Flutter mobile application, secured via Firebase Authentication role separation (`role: 'trainer'`).
* Display real-time client roster showing client workout history, average form compliance scores, and completed repetition totals.
* Enable trainers to select any client session and attach second-by-second timestamped coaching feedback stored in Cloud Firestore.
* Athletes shall receive and view coach annotations directly within their personal workout summary views.

### 3.3. Non-Functional Requirements
* **Performance**: On-device pose estimation and form feedback delay $\le 15\text{ms}$ (30 FPS); server spatiotemporal classification $\le 45\text{ms}$ per clip.
* **Usability**: New users complete onboarding in $\le 5$ minutes; color-coded skeleton and icon overlays understandable without reading text.
* **Reliability**: Main on-device features (pose detection, rep counting, form validation, voice coaching) operate 100% offline without internet; auto-recovery within 2 seconds after phone call interruption.
* **Security & Privacy**: TLS 1.3 encryption in transit; Cloud Firestore security rules with authenticated user UID isolation; raw workout video frames are processed transiently in RAM and never stored on remote servers without explicit user consent.
* **Compatibility**: Native Android 8.0 (API Level 26) or higher and iOS 14.0 or higher; minimum 3GB RAM on Snapdragon 660 or equivalent.

---

## 4. Project Artefacts

### 4.1. Use Case Model

| UC ID | Use Case Name | Primary Actor | Official Module | Verified Function Description |
| :---: | :--- | :---: | :---: | :--- |
| **UC-01** | Register and Login User | End User | **Module 1** | User authenticates via email/password, sets up profile with body metrics, and loads saved data via Firebase. |
| **UC-02** | Track Body Measurements | End User | **Module 6** | User logs height/weight, views live BMI gauge with WHO color coding, calculates Devine Ideal Body Weight, and views transformation history. |
| **UC-03** | Detect Real Time 3D Pose | AI System | **Module 2** | Camera captures video at 30 FPS; on-device Google ML Kit extracts 33 $(x,y,z)$ coordinates and renders neon skeleton overlay in $<15\text{ms}$. |
| **UC-04** | Recognize Exercise | AI System | **Module 3** | Server-side PoseC3D SlowOnly ResNet-50 classifies 48-frame 3D limb heatmaps across 7 exercises with 91.22% Top-5 accuracy. |
| **UC-05** | Assist Via Voice | End User | **Module 8** | On-device `flutter_tts` delivers real-time Priority 1 safety warnings, rep counts, and recovery encouragement with dynamic cooldowns. |
| **UC-06** | Provide Posture Correction | End User | **Module 5** | Four-Pattern Kinematic Engine checks joint flexion, knee valgus, spine neutrality, and camera boundaries, rendering visual corrections. |
| **UC-07** | Count Reps and Validate Form | End User | **Module 4** | Closed 4-Stage Rep FSM (START $\to$ INFLECTION $\to$ PEAK $\to$ COMPLETION) tracks un-clamped joint angles and increments count only on valid depth. |
| **UC-08** | Predict Injury | End User / Trainer | **Module 7** | Real-time clinical watchdog flags Munro FPPA knee valgus ($<165^\circ$ under load $\le 130^\circ$), lumbar hip sag ($>10\%$), and shoulder elbow flare ($>65^\circ$). |
| **UC-09** | Manage User Profile | Admin / User | **Module 1** | System validates account status, manages role-based permissions (Athlete vs. Trainer), and handles secure password operations. |
| **UC-10** | View Reports | Athlete / Trainer | **Module 9** | System compiles session histories, rep completion counts, and form compliance scores for review. |
| **UC-11** | Access Trainer Dashboard | Certified Trainer | **Module 9** | Trainer reviews assigned client lists, inspects exercise logs, and attaches timestamped written coaching advice to client sessions. |

### 4.2. Structural Design
* **Domain Model (Figure 12)**: Entities include `Trainer`, `User`, `ProgressReport`, `BodyTransformationRecord`, `InjuryAlert`, `WorkoutSession`, `Repetition`, `ExerciseType`, `FormAnalysisResult`, `InjuryPrediction`.
* **Class Diagram (Figure 13)**: Class hierarchies for `PoseDetector`, `ExerciseRecognizer`, `RepCounter`, `PostureCorrection`, `InjuryPredictor`, `VoiceCompanion`, `BodyMeasurementTracker`.
* **Component Diagram (Figure 14)**:
  - Mobile: Flutter App (Camera Module, UI Layer, Pose Detection Engine, Four-Pattern Form Analysis Engine).
  - On-Device AI: MediaPipe Pose Lite (`.tflite`), Native Audio Coaching Engine (`flutter_tts`).
  - Backend AI Services: Python FastAPI Server hosting PoseC3D SlowOnly ResNet-50 PyTorch Model with 3D Limb Heatmap Rasterizer.
  - Backend Persistence: Cloud Firestore (User Profiles, Subcollections for Body Measurements, Workout History, and Trainer Feedback).
  - Mobile Trainer Portal: Flutter Trainer Dashboard View with Timestamped Annotation Support.

### 4.3. Behavioral Design
* **Data Flow Diagrams (DFD Level 0 & 1, Figures 15 & 16)**: Pipeline data flow from user video/pose stream to on-device kinematic engine, WebSocket transmission of 17-joint coordinates to PoseC3D AI server, and Firestore synchronization.
* **State Machine Diagram (Figure 17)**: States from `IdleSystem` $\to$ `Register/Login` $\to$ `CameraInitializing` $\to$ `DetectingExercise` $\to$ `ExerciseActive` $\to$ `4-Stage Rep FSM (START -> INFLECTION -> PEAK -> COMPLETION)` $\to$ `SessionSaving`.
* **Sequence Diagram (Figure 18)**: End-to-end interactions across User, Mobile App, Pose Detector, Exercise Recognizer, Rep Counter, Posture Correction, Voice Companion, Firebase.

### 4.4. Maintenance Phase & Deployment
* **Deployment Diagram (Figure 19)**:
  - User Smartphone: Flutter Mobile App, MediaPipe Pose Lite (On-Device), Four-Pattern Kinematic Engine, `flutter_tts` Audio Engine, SQLite/Hive Local Cache, Cloud Firestore Client SDK.
  - AI Inference Server: FastAPI WebSocket/HTTP Server, PoseC3D SlowOnly ResNet-50 PyTorch Model (`epoch_10.pth`), GPU Tensor Runtime.
  - Cloud Backend: Firebase Authentication, Cloud Firestore Database, Cloud Storage.
  - Trainer Smartphone: Flutter Mobile App with Trainer Profile Role Access.

