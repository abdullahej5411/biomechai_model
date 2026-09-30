# BioMechAI — Official SRS Exact Search & Replace Modification Manual
## Complete Page-by-Page, Word-for-Word Editing Instructions for FYP-II Mid-Evaluation (Semester 8)

**Document Reference**: `BioMechAI SRS -Final Document.pdf` (Total 39 Pages)  
**Target Document**: Word / Google Docs source of your official SRS  
**Purpose**: This manual gives your FYP team member the exact `Ctrl+F` search terms, the exact lines to delete, and the exact production-accurate, scientifically defensible text to paste in their place.

> ⚠️ **STRICT EDITING RULE FOR PARTNER**:
> 1. **DO NOT ADD ANY NEW SECTIONS OR HEADINGS**: Keep the exact same section numbers and document structure as the original SRS.
> 2. **DO NOT CHANGE THE DOCUMENT FORMATTING**: Preserve all existing font styles, sizes, line spacings, and table layouts.
> 3. **ONLY REPLACE THE IDENTIFIED TEXT**: Use `Ctrl+F` to locate the exact outdated phrase, delete only that specific text or bullet block, and paste the replacement text in its exact location.

---

# 🚀 Quick Partner Cheat Sheet & Editing Checklist

Tell your partner: *"Open our SRS in Word or Google Docs, press `Ctrl+F`, type the fail-safe keyword from the table below, delete the old text, and paste the replacement. Do not add any new sections."*

| Edit # | SRS Page (Word vs PDF) | SRS Section | Fail-Safe Search Keyword (`Ctrl+F`) | Summary of Fix | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **Edit 1.1** | Word P1 (PDF P7) | Section 1 (Introduction) | `eight modules` | Fix "eight modules" count $\to$ Nine (9) comprehensive modules (FYP-II Mid-Eval) | [ ] |
| **Edit 2.1** | Word P2 (PDF P8) | Section 2.1 (Problem Statement) | `Include an AI voice companion` | Replace chatbot $\to$ Real-time priority-debounced voice coaching | [ ] |
| **Edit 2.2** | Word P3 (PDF P9) | Section 2.3 (Objectives) | `Implement automatic exercise recognition` | Replace 60 exercises, 3D mesh & 30-session claims $\to$ 7 PoseC3D classes & acute injury | [ ] |
| **Edit 2.3** | Word P4 (PDF P10) | Section 2.4 (Scope) | `both web and mobile platforms` | Clarify Flutter mobile app + PyTorch FastAPI dual-timescale architecture | [ ] |
| **Edit 2.4** | Word P4 (PDF P10) | Section 2.5 (Constraints) | `LLaVA-1.5-7B` or `Google Colab` | Remove Colab / 30-session traps $\to$ GPU inference & single-rep acute checks | [ ] |
| **Edit 2.5** | Word P5–6 (PDF P11–12) | Section 2.6.2 & Table 5 | `cloud services like LLaVA` or `User Environment` | Remove LLaVA / desktop web portal $\to$ Flutter Mobile Trainer Portal & offline AI | [ ] |
| **Edit 4.1** | Word P8 (PDF P14) | Section 3.1 (System Features) | `eight evaluated modules` | Replace all 8 feature bullets with the 9 verified FYP-II production modules | [ ] |
| **Edit 5.1** | Word P9 (PDF P15) | Section 3.2.1 (Pose Detection) | `LiDAR` or `ARKit depth` | Remove iPhone LiDAR & OpenGL (<100ms) $\to$ Monocular z-depth & Flutter (<15ms) | [ ] |
| **Edit 5.2** | Word P9 (PDF P15) | Section 3.2.2 (Exercise Recognition) | `at least 60 different exercises` | Replace 60 exercises $\to$ 7 PoseC3D classes (91.22% Top-5, 53.38% Top-1, $T=0.50$) | [ ] |
| **Edit 5.3** | Word P9–10 (PDF P15–16) | Section 3.2.3 (Rep Counting) | `peaks and valleys` | Replace post-processing peaks/valleys $\to$ Closed 4-Stage Rep FSM ($\ge 35^\circ$ floor) | [ ] |
| **Edit 5.4** | Word P10 (PDF P16) | Section 3.2.4 (Posture Correctness) | `AQMN model` or `AQMN` | Remove fictional AQMN model $\to$ Four-Pattern Kinematic Vector Engine | [ ] |
| **Edit 5.5** | Word P10–11 (PDF P16–17) | Section 3.2.5 (Body Measurement) | `SMPL` or `3D body model using SMPL` | Remove SMPL 3D mesh $\to$ Anthropometric scaling, live WHO BMI & Devine formula | [ ] |
| **Edit 5.6** | Word P11 (PDF P17) | Section 3.2.6 (AI Injury Prediction) | `at least 30 workout sessions` | Remove 30-session LSTM $\to$ Dual-Horizon Acute Engine (Munro FPPA $< 165^\circ$, hip sag, flare) | [ ] |
| **Edit 5.7** | Word P11 (PDF P17) | Section 3.2.7 (Voice Companion) | `speech recognition` or `voice communication` | Remove Colab/ElevenLabs chatbot $\to$ Native on-device `flutter_tts` 3-tier queue | [ ] |
| **Edit 5.8** | Word P11–12 (PDF P17–18) | Section 3.2.8 (Trainer Dashboard) | `React-based` or `React -based` | Remove React web portal $\to$ Flutter Mobile Trainer Portal & Firestore feedback | [ ] |
| **Edit 6.1** | Word P12 (PDF P18) | Section 3.3.1 (Performance) | `End-to-end pose detection` | Update latency specs $\to$ 15ms on-device (30 FPS) & 45ms server PoseC3D | [ ] |
| **Edit 6.2** | Word P12–13 (PDF P18–19) | Section 3.3.5 (Compatibility) | `Chrome 90+` or `Safari 14+` | Remove web browsers $\to$ Android 8.0+ / iOS 14.0+ and 3GB RAM mobile specs | [ ] |
| **Section 7** | Word P14–19 (PDF P20–25) | Section 4.1 (Use Case Tables) | `Table 9:` to `Table 19:` | Fix scrambled module numbers in Tables 9–18 & paste new Table 19 | [ ] |
| **Section 8** | Word P13, 21–33 (PDF P19, 27–39) | Section 4.2–4.4 (Diagrams) | `Figure 14`, `Figure 17`, `Figure 19` | Master 19-Diagram Guide: Keep 13 safe diagrams, update 3 critical diagrams (Figures 14, 17, 19) | [ ] |

---

# 1. Executive Summary of Required Updates

Before you begin editing, here are the **5 major contradictions** currently in your SRS that an external evaluation panel will target:

1. **The "60 Exercises" Fantasy vs. 7 Panel-Mandated Exercises**:
   * *Problem*: The SRS claims PoseConv3D recognizes *"more than 60 types of exercises with 85% confidence"*.
   * *Reality*: In Semester 7 (FYP-I), the panel explicitly mandated: *"Find a pretrained model and fine-tune your 7 exercises dataset there."* You trained and certified PoseC3D SlowOnly ResNet-50 across 7 core exercises (Squat, Push-Up, Lunge, Bicep Curl, Plank, Jumping Jack, High Knees) on the 0-leakage held-out test split (91.22% Top-5 accuracy, 53.38% Top-1 record). Claiming 60 exercises without training data will fail evaluation.
2. **The "AQMN Model" Buzzword Trap**:
   * *Problem*: The SRS mentions an `AQMN (.tflite)` model (Action Quality Measurement Network) for posture scoring (0–100).
   * *Reality*: AQMN is an academic model for Olympic diving/gymnastics requiring subjective judge scores. Real gym form validation uses clinical vector trigonometry (Munro FPPA knee valgus, lumbar hip sag, elbow flare). AQMN must be replaced with the Four-Pattern Kinematic Engine.
3. **The "SMPL 3D Body Mesh" Trap**:
   * *Problem*: The SRS claims the app generates 3D body meshes from photos using SMPL to measure waist/chest circumference.
   * *Reality*: SMPL models are 300MB+, require heavy GPUs, and cannot run on a smartphone. The real working feature is Anthropometric Height-Calibrated Landmark Scaling, live WHO Body Mass Index (BMI) computation, and the clinical Devine Ideal Body Weight formula.
4. **The "30 Sessions for Injury Prediction" Trap**:
   * *Problem*: The SRS states injury prediction requires 30 past workout sessions using an LSTM + Isolation Forest.
   * *Reality*: If an evaluator tests your app live, it will say *"Insufficient data"* because 30 sessions don't exist! More importantly, ACL tears happen in a single rep. BioMechAI uses a real-time acute injury watchdog (Munro FPPA $< 165^\circ$ for ACL, hip sag $> 10\%$ for lumbar shear, elbow flare $> 65^\circ$ for shoulder impingement) active on *every single rep*.
5. **The "LLaVA-1.5-7B on Google Colab" Voice Trap**:
   * *Problem*: The SRS claims a 7-billion parameter vision-language model runs on Google Colab with ElevenLabs TTS.
   * *Reality*: Colab disconnects, ElevenLabs costs money and adds 2 seconds of latency. A user tears an ACL in 100ms! You built native on-device speech (`flutter_tts`) with 3-tier priority preemption and a 3.0s watchdog timer that speaks in $< 10\text{ms}$.

---

# 2. Section 1: Introduction Modifications (Word Page 1 / PDF Page 7)

### Edit 1.1: Fix the "Eight Modules" Count Typo
* **Where in SRS**: Word Page 1 (PDF Page 7), Section 1 (*Introduction*), Paragraph 2, Line 5.
* **Fail-Safe Search (Ctrl+F)**: `eight modules`  
  *(Exact full phrase: `For the mid-evaluation stage, the project is divided into the following eight modules:`)*
* **Current Text to Remove**:
  > For the mid-evaluation stage, the project is divided into the following eight modules:
* **Replacement Text to Paste**:
  > For the mid-evaluation stage of FYP-II (Semester 8), the project is structured into the following nine (9) comprehensive modules:
* **Why**: The text said *"eight modules"* but listed nine bullets. This fixes the count to nine (9) comprehensive modules while keeping the correct FYP-II mid-evaluation milestone.

---

# 3. Section 2: Vision Document & Constraints Modifications (Word Pages 2–6 / PDF Pages 8–12)

### Edit 2.1: Update Problem Statement Solution Table
* **Where in SRS**: Word Page 2 (PDF Page 8), Section 2.1 (*Table 1: Problem Statement*), Category: Solution, Bullet 4.
* **Fail-Safe Search (Ctrl+F)**: `Include an AI voice companion that can talk with the user`
* **Current Text to Remove**:
  > • Include an AI voice companion that can talk with the user and give personalized workout guidance.
* **Replacement Text to Paste**:
  > • Include a real-time on-device voice coaching companion that delivers instantaneous, priority-debounced auditory safety cues, rep milestones, and recovery praise during active exercise.
* **Why**: Prevents panelists from expecting a conversational chatbot like ChatGPT while exercising, focusing instead on real-time acoustic biomechanical coaching.

---

### Edit 2.2: Update Objectives
* **Where in SRS**: Word Page 3 (PDF Page 9), Section 2.3 (*Objectives*), Bullets 2, 4, 5, 6.
* **Fail-Safe Search (Ctrl+F)**: `Implement automatic exercise recognition so the system can identify different workouts`
* **Current Text to Remove**:
  > • Implement automatic exercise recognition so the system can identify different workouts without the user needing to select them manually.  
  > • Allow users to monitor their physical progress through a body measurement and transformation tracking feature that uses 3D body modeling.  
  > • Build an AI-based injury prediction system that studies movement changes over time and warns users about possible injury risks before they happen.  
  > • Introduce a conversational AI voice companion that gives users real-time coaching, motivation, and feedback while they are exercising.
* **Replacement Text to Paste**:
  > • Implement automatic exercise classification across seven (7) core fundamental gym exercises utilizing a 3D spatiotemporal convolutional neural network (PoseC3D SlowOnly ResNet-50) pretrained on athletic video datasets (NTU RGB+D / FineGYM) and fine-tuned on the BioMechAI dataset.  
  > • Allow users to monitor their physical transformation through an anthropometric measurement tracking feature calibrated by user height, live Body Mass Index (BMI) computation, and the clinical Devine Ideal Body Weight formula.  
  > • Build a dual-horizon AI injury prediction engine that detects acute joint collapse in real time (e.g., dynamic knee valgus $< 165^\circ$ for ACL injury, lumbar hip sag for spinal disc compression, and shoulder flare for impingement) while logging inter-session fatigue trends.  
  > • Introduce a real-time, on-device AI voice companion that provides sub-10ms priority-preempted audio corrections and form encouragement without requiring an active internet connection.
* **Why**: Aligns objectives directly with the panel's mandate, eliminates unbuilt 3D mesh buzzwords, and proves clinical relevance.

---

### Edit 2.3: Fix Scope
* **Where in SRS**: Word Page 4 (PDF Page 10), Section 2.4 (*Scope*), Lines 4–5.
* **Fail-Safe Search (Ctrl+F)**: `both web and mobile platforms`
* **Current Text to Remove**:
  > In the beginning, the system will be designed to run on both web and mobile platforms.
* **Replacement Text to Paste**:
  > The system is architected as a high-performance Flutter mobile application for athletes and personal trainers, communicating via high-speed WebSockets and REST APIs with a dedicated PyTorch/FastAPI backend inference engine for deep spatiotemporal neural network evaluation.
* **Why**: Clarifies the exact dual-timescale mobile client and GPU server architecture built in your project.

---

### Edit 2.4: Replace Impractical Constraints
* **Where in SRS**: Word Page 4 (PDF Page 10), Section 2.5 (*Constraints*), Bullets 1, 4, 5, 6.
* **Fail-Safe Search (Ctrl+F)**: `LLaVA-1.5-7B` or `Google Colab`
* **Current Text to Remove**:
  > • All AI processing must finish within 100ms on mid -range devices (equivalent to Snapdragon 720G or better).  
  > • LLaVA-1.5-7B runs in the cloud on Google Colab, which can cause 500ms-1s delays for complex AI companion responses.  
  > • The accuracy of body measurement depends on the quality of 2D images, lighting conditions, and the user’s clothing.  
  > • Injury prediction requires at least 30 workout sessions before it can provide reliable risk assessments.
* **Replacement Text to Paste**:
  > • On-device AI processing (pose estimation, rep counting, kinematic form validation) must execute within 15ms per frame on mid-range devices (Snapdragon 720G or equivalent) to sustain 30 FPS camera capture.  
  > • Deep learning spatiotemporal inference (PoseC3D) requires a GPU-enabled backend server (NVIDIA T4 or equivalent) for batched 3D convolutional tensor evaluations within 45ms.  
  > • Anthropometric body tracking relies on standardized vertical user framing and calibrated reference stature (height) for metric conversion.  
  > • Acute injury prediction operates instantaneously on every single repetition using clinical kinematic angle cutoffs (e.g., Munro FPPA $< 165.0^\circ$ for knee valgus), while chronic overuse trends require cumulative multi-session logs.
* **Why**: Removes Colab and 30-session dependencies which would fail during a live jury evaluation, and reflects actual benchmarked latencies.

---

### Edit 2.5: Fix User Environment & Trainer Stakeholder Profile
* **Where in SRS**: Word Pages 5–6 (PDF Pages 11–12), Section 2.6.2 (*User Environment*) and Section 2.6.3.4 (*Table 5: Certified Trainers*).
* **Fail-Safe Search (Ctrl+F)**: `cloud services like LLaVA` or `2.6.2. User Environment`
* **Current Text to Remove in 2.6.2 (Page 11)**:
  > Trainers access the system using web portal on desktop browsers like Chrome, Firefox, or Safari. Most AI processing happens directly on the device, while cloud services like LLaVA and Firebase need a stable internet connection. If the connection is weak, the system continues to work by disabling cloud-based voice features and relying on on-device models for essential functionality.
* **Replacement Text to Paste in 2.6.2**:
  > Trainers access the system through a dedicated Flutter Mobile Trainer Portal. On-device AI processing (Google ML Kit pose detection, Closed 4-Stage Rep FSM, Four-Pattern Kinematics, and flutter_tts voice coaching) operates fully autonomously with sub-15ms frame latency without requiring an active internet connection. Dedicated GPU cloud inference (PoseC3D spatiotemporal model on FastAPI) and Firebase Firestore synchronization activate when network connectivity is available, providing seamless offline-first capability.
* **Current Text to Remove in Table 5 (Page 12)**:
  > Description: Fitness professionals using the web -based Trainer Dashboard to remotely manage clients  
  > Involvement: 1. Beta testing of the web portal
* **Replacement Text to Paste in Table 5**:
  > Description: Fitness professionals using the dedicated Flutter Mobile Trainer Portal to remotely manage clients  
  > Involvement: 1. Field testing of the mobile trainer portal
* **Why**: Completely purges the last remaining mention of LLaVA and false claims of a desktop web portal from the stakeholder environment.

---

# 4. Section 3.1: System Features Modifications (Word Page 8 / PDF Page 14)

### Edit 4.1: Modernize All 8 Feature Descriptions
* **Where in SRS**: Word Page 8 (PDF Page 14), Section 3.1 (*System Features*).
* **Fail-Safe Search (Ctrl+F)**: `eight evaluated modules`  
  *(Exact phrase: `BioMechAI provides the following core system features across the eight evaluated modules:`)*
* **Current Text to Remove**:
  > BioMechAI provides the following core system features across the eight evaluated modules:  
  > • Real-time 3D Pose Detection: The system detects 33 body landmarks in real time at around 30 frames per second and shows a skeleton overlay using MediaPipe Pose Lite.  
  > • Exercise Recognition: The system automatically identifies more than 60 types of exercises using the PoseConv3D model on short movement clips, with a confidence level of about 85%.  
  > • Rep Counting and Form Validation: The system counts repetitions only when the correct movement pattern is detected, using motion peaks and valleys along with basic movement safety checks.  
  > • Posture Correctness (Four -Pattern Engine): The system checks posture using sports science rules, machine learning quality scoring, time-based movement analysis, and adjusts limits based on the user’s body type.  
  > • Body Measurement Tracking: The system creates a simple 3D body model from user photos using SMPL methods and standard body measurement formulas to track physical changes over time.  
  > • AI Injury Prediction: The system studies workout data across more than 30 sessions using LSTM and Isolation Forest models to predict possible injury risks and suggest preventive steps.  
  > • AI Voice Companion: The system provides continuous voice guidance and motivation during workouts using AI vision -language understanding, speech recognition, and text-to-speech technologies.  
  > • Trainer Dashboard: A React-based web portal allows trainers to review AI-annotated workout videos, view client progress data, and generate automatic performance reports in PDF format.
* **Replacement Text to Paste**:
  > BioMechAI delivers the following core system features across its nine (9) verified production modules:  
  > • **Module 1: User Registration and Login**: Secure multi-role authentication (Athlete vs. Trainer) using Firebase Auth and Cloud Firestore profile persistence.  
  > • **Module 2: Real-time 3D Pose Detection**: Extracts 33 normalized 3D anatomical landmarks at 30 FPS using Google ML Kit BlazePose running natively on-device with custom low-latency visual skeleton overlays.  
  > • **Module 3: Exercise Classification (PoseC3D Deep Learning Engine)**: Classifies user movement into seven (7) fundamental exercises using a 3D spatiotemporal ResNet-50 network fine-tuned on athletic limb heatmaps, achieving 91.22% Top-5 accuracy on held-out test splits.  
  > • **Module 4: Real-time Rep Counting and Form Validation**: Employs a deterministic Closed 4-Stage Repetition Finite State Machine (START $\to$ INFLECTION $\to$ PEAK $\to$ COMPLETION) with un-clamped joint flexion and camera boundary occlusion rejection ($\ge 35^\circ$).  
  > • **Module 5: Posture Correctness (Four-Pattern Kinematic Engine)**: Evaluates sagittal depth flexion, frontal knee alignment, trunk neutrality, and framing sanity in $< 0.1\text{ms}$ using clinically validated vector trigonometry.  
  > • **Module 6: Body Measurement and Transformation Tracking**: Tracks user anthropometric dimensions, computes live BMI with color-coded classification gauges, determines physiological target weight using the Devine formula, and persists historical progress to Firestore.  
  > • **Module 7: AI Clinical Injury Prevention Engine**: Real-time full-body injury guard monitoring Munro Dynamic Knee Valgus FPPA ($< 165^\circ$ under load $\le 130^\circ$) for acute ACL protection, lumbar hip sag ($> 10\%$) for spinal shear protection, and elbow flare ($> 65^\circ$) for rotator cuff impingement.  
  > • **Module 8: AI Workout Companion with Live Voice Coaching**: Provides zero-latency, on-device audio coaching (`flutter_tts`) governed by a 3-tier priority queue (Priority 1: Emergency Safety Warnings, Priority 2: Rep Milestones, Priority 3: Form Praise) with dynamic cooldown debouncing.  
  > • **Module 9: Trainer Dashboard & Timestamped Feedback**: A comprehensive coaching portal within the Flutter ecosystem enabling certified trainers to inspect client rosters, review form scores, and leave second-by-second timestamped corrective notes.
* **Why**: Fully synchronizes the feature summary with all 9 modules, fixes the "eight modules" error, and replaces fictional components with verified code.

---

# 5. Section 3.2: Functional Requirements Modifications (Word Pages 9–12 / PDF Pages 15–18)

### Edit 5.1: Functional Requirement 3.2.1 (Pose Detection)
* **Where in SRS**: Word Page 9 (PDF Page 15), Section 3.2.1, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `LiDAR` or `ARKit depth`  
  *(Exact phrase in PDF: `On LiDAR -supported iPhones, the system shall use ARKit depth`)*
* **Current Text to Remove (All 5 Bullets under 3.2.1)**:
  > • The system shall capture workout video using the device camera at a minimum speed of 30 frames per second.  
  > • The system shall detect 33 body points with X, Y, and Z coordinates in real time using MediaPipe Pose Lite.  
  > • The system shall show a skeleton overlay on the live camera feed using OpenGL, keeping total delay below 100 milliseconds.  
  > • The system shall temporarily store joint position data in a ring buffer of 90 frames for further movement analysis.  
  > • On LiDAR -supported iPhones, the system shall use ARKit depth information to improve the accuracy of 3D body coordinates.
* **Replacement Text to Paste**:
  > • The system shall capture live workout frames from the front/back mobile camera at 30 frames per second.  
  > • The system shall detect 33 normalized 3D anatomical body landmarks $(x, y, z)$ in real time using Google ML Kit BlazePose executing natively on-device.  
  > • The system shall render a color-coded kinematic skeleton overlay on the live camera feed using Flutter CustomPainter, keeping rendering latency below 15 milliseconds.  
  > • The system shall buffer joint coordinate streams in a 48-frame rolling spatiotemporal window for deep convolutional exercise classification.  
  > • The system shall utilize MediaPipe's relative 3D z-depth coordinate estimates to measure sagittal-plane depth and forward torso inclination across standard monocular smartphone cameras without requiring specialized LiDAR hardware.
* **Why**: Replaces OpenGL/100ms claims with Flutter CustomPainter (<15ms) and removes unbuilt iPhone LiDAR hardware claims.

---

### Edit 5.2: Functional Requirement 3.2.2 (Exercise Recognition)
* **Where in SRS**: Word Page 9 (PDF Page 15), Section 3.2.2, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `at least 60 different exercises` or `60 different exercises`
* **Current Text to Remove (All 5 Bullets under 3.2.2)**:
  > • The system shall automatically recognize the exercise being performed without requiring manual input from the user.  
  > • The system shall support recognition of at least 60 different exercises from categories such as strength training, cardio, core workouts, and yoga.  
  > • The system shall analyze 3D movement patterns using a 3 -second sliding window and the PoseConv3D model.  
  > • Exercise recognition shall be confirmed only when the confidence level reaches 85% for two continuous seconds.  
  > • After recognition, the system shall load exercise -specific movement rules and display the exercise name on the screen.
* **Replacement Text to Paste**:
  > • The system shall recognize seven (7) core athletic compound and isolation exercises: Squat, Push-Up, Lunge, Bicep Curl, Plank, Jumping Jack, and High Knees.  
  > • The system shall convert 48 consecutive frames of 17-channel COCO anatomical joint coordinates into spatiotemporal 3D limb heatmaps ($56 \times 56 \times 48$) with Gaussian tubular segments ($\sigma = 0.6$).  
  > • The system shall classify the spatiotemporal volume using a SlowOnly ResNet-50 3D convolutional neural network (PoseC3D) initialized with pretrained athletic weights (NTU RGB+D / FineGYM) and fine-tuned on the BioMechAI dataset (91.22% Top-5 accuracy, 53.38% Top-1 record on held-out test splits).  
  > • Classification decisions shall be locked when model softmax probability exceeds the calibrated deployment threshold ($T = 0.50$).  
  > • After recognition, the system shall dynamically switch kinematic form validation rules and audio coaching prompts specific to the recognized exercise.
* **Why**: Accurately reflects the PoseC3D champion model (`best_acc_top1_epoch_10.pth` loaded in backend) and the panel's 7-exercise mandate.

---

### Edit 5.3: Functional Requirement 3.2.3 (Rep Counting)
* **Where in SRS**: Word Pages 9–10 (PDF Pages 15–16), Section 3.2.3, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `peaks and valleys` or `3.2.3. Real-time Rep Counting`
* **Current Text to Remove (All 5 Bullets under 3.2.3)**:
  > • The system shall track the main joint movement related to each exercise, such as hip movement during squats or elbow angle during push-ups.  
  > • The system shall identify complete repetitions by detecting peaks and valleys in joint movement data.  
  > • Each repetition shall be checked against defined movement safety limits before increasing the repetition count.  
  > • Repetitions performed with unsafe or incomplete form shall be rejected and a visual warning shall be shown.  
  > • During workouts, the system shall display the current repetition count, exercise speed, and form quality score in real time.
* **Replacement Text to Paste**:
  > • The system shall track primary biomechanical joint articulations in real time (knee flexion for squats/lunges, elbow flexion for push-ups/curls, hip height for planks).  
  > • The system shall implement a deterministic Closed 4-Stage Repetition Finite State Machine (FSM):  
  >   1. `START`: Baseline standing posture ($\theta \ge 146.0^\circ$).  
  >   2. `INFLECTION`: Descent phase initiated ($\theta < 146.0^\circ$).  
  >   3. `PEAK`: Valid exercise depth attained (e.g., knee flexion $\le 115.0^\circ$ for squats, elbow flexion $\le 95.0^\circ$ for push-ups).  
  >   4. `COMPLETION`: Full extension restored ($\theta \ge 146.0^\circ$), incrementing rep count by exactly +1.  
  > • Repetitions failing to reach the required peak depth threshold shall be classified as partial/incomplete reps and rejected without incrementing the counter.  
  > • The system shall enforce an anatomical sanity floor ($\theta \ge 35.0^\circ$) to discard sudden optical occlusion glitches.  
  > • During workouts, the system shall display the validated repetition count, real-time joint angles, and active form status flags.
* **Why**: Peak/valley detection is a batch post-processing algorithm that cannot run live; the 4-Stage FSM is what you actually built in `backend/kinematics.py`.

---

### Edit 5.4: Functional Requirement 3.2.4 (Posture Correctness)
* **Where in SRS**: Word Page 10 (PDF Page 16), Section 3.2.4, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `AQMN model` or `AQMN`
* **Current Text to Remove (All 5 Bullets under 3.2.4)**:
  > • The system shall check joint angles and overall body posture using basic sports science safety limits for each exercise.  
  > • The system shall use the AQMN model to give a movement quality score between 0 and 100 and detect common technique mistakes.  
  > • The system shall study movement smoothness by calculating factors like sudden motion changes, exercise rhythm, and left-right body balance.  
  > • The system shall adjust posture limits based on the user’s body proportions collected during onboarding, using standard body measurement references.  
  > • The system shall show visual correction arrows and highlight the skeleton (red for mistakes, green for correct posture), along with voice feedback during workouts.
* **Replacement Text to Paste**:
  > • The system shall evaluate exercise posture using a Four-Pattern Clinical Kinematic Vector Engine based on peer-reviewed biomechanical literature:  
  >   1. **Sagittal Depth Flexion**: Measures target joint extension/flexion using vector dot products against gold-standard standards (Schoenfeld 2010, Escamilla 2001).  
  >   2. **Frontal Plane Projection Angle (FPPA)**: Monitors medial-lateral deviation of the knee joint relative to the hip-ankle line (Munro et al. 2012).  
  >   3. **Trunk and Spinal Neutrality**: Computes pelvic-shoulder angle relative to the gravity axis to detect compensatory lumbar hyperextension or excessive forward lean (McGill 2010).  
  >   4. **Camera Framing Guards**: Filters out landmark estimates whenever key tracking joints intersect camera borders ($y > 0.94$).  
  > • The system shall render real-time color-coded skeleton feedback (green = acceptable form, red = kinematic violation) alongside corrective text overlays and priority audio coaching cues.
* **Why**: Completely purges the fictional "AQMN model" and specifies the four-pattern kinematic system built in your code.

---

### Edit 5.5: Functional Requirement 3.2.5 (Body Measurement)
* **Where in SRS**: Word Pages 10–11 (PDF Pages 16–17), Section 3.2.5, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `SMPL` or `3D body model using SMPL`
* **Current Text to Remove (All 5 Bullets under 3.2.5)**:
  > • The system shall allow users to take standard front and side photos to build a body model.  
  > • The system shall use MediaPipe Pose to detect 2D body points from photos and create a 3D body model using SMPL.  
  > • The system shall estimate body measurements such as chest, waist, hips, arms, and thighs using formulas adjusted with the user’s height.  
  > • The system shall store initial and later measurements in Firestore and show side-by-side comparisons of body changes.  
  > • The system shall use color-based visuals to show measurement changes, such as waist reduction in blue or muscle gain in green.
* **Replacement Text to Paste**:
  > • The system shall provide an Anthropometric Body Measurement and Transformation Tracking interface.  
  > • The system shall calculate Body Mass Index (BMI) dynamically from recorded weight and height using the World Health Organization (WHO TRS 854) standard: $\text{BMI} = \text{weight (kg)} / (\text{height (m)})^2$.  
  > • The system shall render an interactive color-coded BMI gauge with medical classification bands: Underweight ($<18.5$, blue), Normal ($18.5\text{--}24.9$, green), Overweight ($25.0\text{--}29.9$, yellow), and Obese ($\ge 30.0$, red).  
  > • The system shall compute the user's physiological Ideal Body Weight (IBW) baseline using the clinical Devine Formula: $\text{IBW} = 50.0\text{ kg} + 2.3 \times (\text{height in inches} - 60) \pm 5.0\text{ kg}$.  
  > • The system shall persist longitudinal transformation logs in Cloud Firestore (`/users/{uid}/body_measurements`) and plot historical weight trends over time.
* **Why**: Replaces the unfeasible SMPL 3D mesh claim with the actual fully working Body Measurement Screen (`lib/screens/body_measurement_screen.dart`).

---

### Edit 5.6: Functional Requirement 3.2.6 (AI Injury Prediction)
* **Where in SRS**: Word Page 11 (PDF Page 17), Section 3.2.6, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `at least 30 workout sessions` or `LSTM neural network`
* **Current Text to Remove (All 5 Bullets under 3.2.6)**:
  > • The system shall study joint movement data collected from at least 30 workout sessions using an LSTM neural network.  
  > • The system shall use Isolation Forest to detect unusual movement patterns compared to the user’s normal performance.  
  > • The system shall connect detected movement issues with possible injury risks using a sports medicine reference database.  
  > • The system shall send push notifications when injury risk goes above 60%, labeling it as Low, Medium, or High.  
  > • When high risk is detected, the system shall suggest corrective exercises and automatically add rest days to the workout plan.
* **Replacement Text to Paste**:
  > • The system shall implement a Dual-Horizon AI Clinical Injury Prevention Engine protecting upper body, core/spine, and lower body joints across all 7 exercises:  
  >   1. **Acute Knee Valgus / ACL Tear Risk (Squats & Lunges)**: Continuously evaluates Munro Frontal Plane Projection Angle ($\text{FPPA} = \arccos(\frac{\vec{u}_{HK} \cdot \vec{v}_{AK}}{\|\vec{u}\| \|\vec{v}\|})$). An acute alert is triggered when $\text{FPPA} < 165.0^\circ$ under active flexion load ($\le 130.0^\circ$), preventing non-contact ACL rupture (Munro 2012, Hewett 2005).  
  >   2. **Lumbar Disc Shear & Compression Risk (Push-Ups & Planks)**: Calculates perpendicular orthogonal distance from hip joint to shoulder-ankle axis. Sagging exceeding $10\%$ of body length triggers an immediate spinal safety alert (McGill 2010).  
  >   3. **Subacromial Shoulder Impingement Risk (Push-Ups)**: Measures humeral abduction angle relative to torso axis. Elbow flare exceeding $65.0^\circ$ triggers an acute warning to prevent supraspinatus tendon pinching (Flatow 1994, Cogley 2005).  
  >   4. **Bicipital Tendon & Lumbar Strain Risk (Bicep Curls)**: Flags forward elbow drift $> 30.0^\circ$ and backward torso swing $> 20.0^\circ$.  
  >   5. **Iliopsoas & Lower Back Compensation (High Knees)**: Flags excessive forward trunk lean $> 15.0^\circ$.  
  > • The system shall log cumulative repetitions performed with hazardous kinematics to assess longitudinal joint fatigue trends.
* **Why**: Replaces the "30 sessions" demo trap with the multi-joint clinical injury prevention engine verified in `backend/kinematics.py`.

---

### Edit 5.7: Functional Requirement 3.2.7 (Voice Companion)
* **Where in SRS**: Word Page 11 (PDF Page 17), Section 3.2.7, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `speech recognition` or `voice communication`  
  *(Exact phrase in PDF: `continuous two -way voice communication`)*
* **Current Text to Remove (All 5 Bullets under 3.2.7)**:
  > • The system shall support continuous two -way voice communication during the workout using live speech recognition.  
  > • The system shall count repetitions aloud, give motivation, and answer exercise -related questions while the user is training.  
  > • The AI companion shall remember workout details such as the current exercise, completed repetitions, corrections given, and signs of user fatigue.  
  > • Voice replies shall sound natural, with less than 500 milliseconds delay for on -device responses and less than 1.5 seconds for cloud-based queries.  
  > • The companion shall change workout intensity based on user voice feedback, such as suggesting rest when the user feels tired.
* **Replacement Text to Paste**:
  > • The system shall provide an on-device AI Voice Coaching Engine powered by `flutter_tts` operating completely offline with sub-10 millisecond latency.  
  > • Audio cues shall be dispatched using a strict 3-tier Priority Preemption Queue:  
  >   - **Priority 1 (Emergency Safety Alerts)**: Immediate voice override for acute injury risks (*"Push your knees out!"*, *"Lift your hips!"*, *"Tuck your elbows!"*).  
  >   - **Priority 2 (Repetition Milestones)**: Auditory rep count announcements (*"Rep 5 completed"*).  
  >   - **Priority 3 (Form Praise & Recovery)**: Positive encouragement when safe form is maintained or restored (*"Great depth, keep going!"*).  
  > • The engine shall implement dynamic cooldown debouncing (minimum 2.5 seconds between duplicate cues) to prevent auditory flooding.  
  > • An asynchronous 3.0-second hardware watchdog timer shall monitor audio speech completion to prevent mobile audio channel deadlocks.
* **Why**: Completely aligns with the verified `VoiceCoachingService` and `VoiceCuePriority` implementation in your Flutter app.

---

### Edit 5.8: Functional Requirement 3.2.8 (Trainer Dashboard)
* **Where in SRS**: Word Pages 11–12 (PDF Pages 17–18), Section 3.2.8, All Bullets.
* **Fail-Safe Search (Ctrl+F)**: `React-based` or `React -based`  
  *(Exact phrase in PDF: `The Trainer Dashboard shall be a React -based web application`)*
* **Current Text to Remove (All 5 Bullets across Pages 17–18)**:
  > • The Trainer Dashboard shall be a React -based web application secured through Firebase login and usable on common desktop browsers.  
  > • The system shall show all connected clients along with their activity status, form quality scores, and workout history.  
  > • Trainers shall be able to watch recorded workout videos with AI-generated skeleton overlays and time-based error highlights.  
  > • Trainers shall be able to leave time -specific written feedback directly on client workout videos.  
  > • The system shall automatically create monthly PDF reports for each client using jsPDF, summarizing form quality, repetition trends, consistency, and injury alerts.
* **Replacement Text to Paste**:
  > • The Trainer Dashboard shall be a specialized portal within the Flutter mobile application, secured via Firebase Authentication role separation (`role: 'trainer'`).  
  > • The dashboard shall display a real-time client roster showing client workout history, average form compliance scores, and completed repetition totals.  
  > • Trainers shall be able to select any client session and attach second-by-second timestamped coaching feedback (e.g., linked to specific rep timestamps) stored in Cloud Firestore.  
  > • Athletes shall receive and view these coach annotations directly within their personal workout summary views.
* **Why**: Reflects the native Flutter `TrainerDashboardScreen` and `TrainerFeedback` model implemented in your codebase, avoiding fake claims of a separate React website.

---

# 6. Section 3.3: Non-Functional Requirements Modifications (Word Pages 12–13 / PDF Pages 18–19)

### Edit 6.1: NFR 3.3.1 (Performance)
* **Where in SRS**: Word Page 12 (PDF Page 18), Section 3.3.1 (*Performance*).
* **Fail-Safe Search (Ctrl+F)**: `End-to-end pose detection` or `3.3.1. Performance`
* **Current Text to Remove (All 3 Bullets under 3.3.1)**:
  > • End-to-end pose detection and form feedback delay shall not exceed 100 milliseconds on devices with Snapdragon 720G or similar performance.  
  > • Exercise recognition shall provide a confirmed result within 3 to 5 seconds after the user starts moving.  
  > • The app shall maintain smooth camera processing at 30 frames per second without frame drops during workouts.
* **Replacement Text to Paste**:
  > • On-device pose estimation and kinematic form feedback shall execute within 15 milliseconds per frame on standard Android devices (Snapdragon 720G or equivalent), sustaining 30 FPS camera capture without frame drops.  
  > • Spatiotemporal 3D convolutional classification (PoseC3D) evaluated on the Python FastAPI inference server shall return top-class predictions within 45 milliseconds per 48-frame clip.  
  > • Exercise recognition shall establish confirmed exercise lock within 2.0 seconds of steady motion using a 48-frame rolling buffer.
* **Why**: Correctly reports benchmarked latencies (15ms on-device, 45ms server) and 30 FPS performance.

---

### Edit 6.2: NFR 3.3.5 (Compatibility)
* **Where in SRS**: Word Pages 12–13 (PDF Pages 18–19), Section 3.3.5 (*Compatibility*).
* **Fail-Safe Search (Ctrl+F)**: `Chrome 90+` or `Safari 14+` or `3.3.5. Compatibility`
* **Current Text to Remove (All 3 Bullets under 3.3.5 across Pages 18–19)**:
  > • The mobile app shall support devices running Android 8.0 or higher and iOS 14.0 or higher.  
  > • The Trainer Dashboard web portal shall work properly on Chrome 90+, Firefox 88+, and Safari 14+ browsers.  
  > • All AI models shall run on devices with at least 3GB RAM and a Snapdragon 660 or similar processor.
* **Replacement Text to Paste**:
  > • The mobile application (both Athlete and Trainer modes) shall support devices running Android 8.0 (API Level 26) or higher and iOS 14.0 or higher.  
  > • All on-device AI modules (Google ML Kit pose detection, Closed 4-Stage Rep FSM, Four-Pattern Kinematics, flutter_tts Voice Coaching) shall run efficiently on devices with at least 3GB RAM and Snapdragon 660 or higher without thermal throttling.  
  > • The dedicated PyTorch backend service shall run on any Linux or Windows environment equipped with Python 3.10+ and CUDA-capable GPU acceleration (or CPU fallback).
* **Why**: Removes desktop web browser requirements and accurately documents the mobile and backend execution environments.

---

# 7. Section 4.1: Use Case Tables Corrections (Word Pages 14–19 / PDF Pages 20–26)

In your current SRS, **Tables 9 through 19 have severely scrambled module numbers** (e.g., Voice Assistance is called Module 3, Injury is called Module 4, Admin is called Module 5).

Here is the exact search and replace table to fix every single Use Case:

| Table # | Use Case Name | Fail-Safe Search (Ctrl+F) | Current WRONG Module | Correct Replacement Module |
| :--- | :--- | :--- | :---: | :---: |
| **Table 8** | Register and Login User | `Table 8: Register and Login User` | Module 1 | **Module 1 (User Registration & Login)** |
| **Table 9** | Track Body Measurements | `Table 9: Track Body Measurements` | **Module 1** ❌ | **Module 6 (Body Measurement & Tracking)** ✅ |
| **Table 10** | Detect Real-Time 3D Pose | `Table 10: Detect Real-Time 3D Pose` | Module 2 | **Module 2 (Real-Time 3D Pose Detection)** |
| **Table 11** | Recognize Exercise | `Table 11: Recognize Exercise` | **Module 2** ❌ | **Module 3 (Exercise Classification - PoseC3D)** ✅ |
| **Table 12** | Assist Via Voice | `Table 12: Assist Via Voice` | **Module 3** ❌ | **Module 8 (AI Workout Companion - Voice)** ✅ |
| **Table 13** | Provide Posture Correction | `Table 13: Provide Posture Correction` | **Module 3** ❌ | **Module 5 (Posture Correctness Engine)** ✅ |
| **Table 14** | Count Reps and Validate Form | `Table 14: Count Reps and Validate Form` | **Module 3** ❌ | **Module 4 (Real-Time Rep Counting FSM)** ✅ |
| **Table 15** | Predict Injury | `Table 15: Predict Injury` | **Module 4** ❌ | **Module 7 (AI Clinical Injury Prevention)** ✅ |
| **Table 16** | Manage User | `Table 16: Manage User` | **Module 5** ❌ | **Module 1 (Administration & Profile Control)** ✅ |
| **Table 17** | View Reports | `Table 17: View Reports` | **Module 5** ❌ | **Module 9 (Trainer & Admin Analytics)** ✅ |
| **Table 18** | Access Trainer Dashboard | `Table 18: Access Trainer Dashboard` | **Module 5** ❌ | **Module 9 (Trainer Dashboard & Feedback)** ✅ |

---

### Edit 7.1: Replace Table 19 (High-Level Use Case Summary Table)
* **Where in SRS**: Word Page 19 (PDF Pages 25–26), Table 19 (*High-Level Use Case*).
* **Fail-Safe Search (Ctrl+F)**: `Table 19: High-Level Use Case`
* **Current Table to Replace**: Entire Table 19 rows.
* **Replacement Content to Paste**:

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

---

# 8. Master Architectural & System Diagrams Modification Guide (Figures 1 to 19)
## Complete Step-by-Step Diagram Guide for Word Document Pages 13 & 21–33 (PDF Pages 19 & 27–39)

> 💡 **MESSAGE FOR PARTNER ABOUT DIAGRAMS**:
> * We extracted and visually verified **all 19 diagrams** directly from the official SRS document.
> * **13 diagrams are 100% SAFE**: You do **NOT** need to redraw or change them. Leave them exactly as they are.
> * **3 diagrams have MINOR FLOWS (Figures 2, 11, 18)**: They depict high-level conversational flow from FYP-I. They are **harmless for the mid-evaluation** unless you are already redrawing diagrams.
> * **3 diagrams are CRITICAL FIXES (Figures 14, 17, 19)**: They contain dangerous outdated buzzwords (`AQMN .tflite`, `LLaVA-1.5-7B on Google Colab`, `ElevenLabs TTS`, `Confidence >85% for 2s`, and typos like `.apl` and `Forebase`). **These 3 diagrams must be updated or re-exported** to ensure a bulletproof defense before the panel.

---

### 8.0. Master Diagram Inventory & Health Status Table (All 19 Figures)

| Figure # | Diagram Name | Word Doc Page | PDF Page | Health Category | Action Required |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **Figure 1** | Use Case Diagram | **Page 13** | Page 19 | 🟢 **100% Safe** | **No action needed.** Leave as-is. Matches Table 19 perfectly. |
| **Figure 2** | Swimlane Activity Diagram | **Page 21** | Page 27 | 🟡 **Minor Note** | Safe for mid-eval. (Optional: update voice query branch to audio cue dispatch). |
| **Figure 3** | SSD 01: Body Measurement Tracking | **Page 22** | Page 28 | 🟢 **100% Safe** | **No action needed.** Generic system calls (`continueBodyScan`, `analyzeBody`). |
| **Figure 4** | SSD 02: Exercise Recognition | **Page 22** | Page 28 | 🟢 **100% Safe** | **No action needed.** Generic system calls (`capturePose`, `classifyExercise`). |
| **Figure 5** | SSD 03: Injury Prediction | **Page 23** | Page 29 | 🟢 **100% Safe** | **No action needed.** Generic calls (`repHistory`, `analyzeInjuryRisk`). |
| **Figure 6** | SSD 04: Pose Detection | **Page 23** | Page 29 | 🟢 **100% Safe** | **No action needed.** Generic calls (`activateCamera`, `detectLandmarks`). |
| **Figure 7** | SSD 05: Posture Correction | **Page 24** | Page 30 | 🟢 **100% Safe** | **No action needed.** Generic calls (`analyzePosture`, `correctionAdvice`). |
| **Figure 8** | SSD 06: Rep Counter | **Page 24** | Page 30 | 🟢 **100% Safe** | **No action needed.** Generic calls (`detectMovementCycle`, `validateForm`). |
| **Figure 9** | SSD 07: Trainer Dashboard | **Page 25** | Page 31 | 🟢 **100% Safe** | **No action needed.** Generic calls (`authenticateTrainer`, `requestsReports`). |
| **Figure 10** | SSD 08: User Registration and Login | **Page 25** | Page 31 | 🟢 **100% Safe** | **No action needed.** Standard authentication sequence. |
| **Figure 11** | SSD 09: Voice Companion | **Page 26** | Page 32 | 🟡 **Minor Note** | Safe for mid-eval. High-level sequence (`askQuestion`, `playAudio`). |
| **Figure 12** | Domain Model | **Page 27** | Page 33 | 🟢 **100% Safe** | **No action needed.** Matches Firestore schema and domain logic exactly. |
| **Figure 13** | Class Diagram | **Page 28** | Page 34 | 🟢 **100% Safe** | **No action needed.** Contains `height`, `weight`, `bmi`, `CalculateBMI()` in User class. |
| **Figure 14** | Component Diagram | **Page 29** | Page 35 | 🔴 **CRITICAL FIX** | **MUST UPDATE IMAGE**: Remove AQMN, PoseConvo3D, LLaVA Colab, ElevenLabs. Fix typos. |
| **Figure 15** | DFD Level 0 (Context Diagram) | **Page 30** | Page 36 | 🟢 **100% Safe** | **No action needed.** Clean top-level data flow. |
| **Figure 16** | DFD Level 1 | **Page 30** | Page 36 | 🟢 **100% Safe** | **No action needed.** Clean 6-process decomposition. |
| **Figure 17** | State Machine Diagram | **Page 31** | Page 37 | 🔴 **CRITICAL FIX** | **MUST UPDATE IMAGE**: Change `Confidence >85%` $\to$ $T \ge 0.50$, add 4-Stage Rep FSM. |
| **Figure 18** | Sequence Diagram | **Page 32** | Page 38 | 🟡 **Minor Note** | Safe for mid-eval. Full workout lifecycle sequence. |
| **Figure 19** | Deployment Diagram | **Page 33** | Page 39 | 🔴 **CRITICAL FIX** | **MUST UPDATE IMAGE**: Remove AQMN, LLaVA Colab, ElevenLabs. Fix `BioMechAI.apl` typo. |

---

### 8.1. Figure-by-Figure Detailed Audit (Figures 1 to 19)

#### Figure 1: Use Case Diagram (Word Page 13 / PDF Page 19)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Shows 4 actors: `Admin`, `Certified Trainer`, `End User`, and `AI System`. Shows 11 clean use case ovals: `Manage Users`, `View Reports`, `Register and Login User`, `Predict Injury`, `Access Trainer Dashboard`, `Assist Via Voice`, `Track Body Measurements`, `Provide Posture Correction and Feedback`, `Count Reps and Validate Form`, `Recognize Exercise`, `Detect Real Time 3D Pose`. 
* **Defense Verdict**: 100% aligned with our updated Table 19. No buzzwords, no fictional models mentioned. Leave as is.

#### Figure 2: Swimlane Activity Diagram (Word Page 21 / PDF Page 27)
* **Status**: 🟡 **MINOR NOTE — SAFE AS-IS FOR MID-EVALUATION**
* **Detailed Audit**: Features 5 swimlanes: `User`, `Mobile App`, `Trainer`, `Admin`, `Cloud`. The workout loop is technically sound (Initialize Camera $\to$ 30 FPS Capture $\to$ Detect 3D Landmarks $\to$ Exercise Recognized $\to$ Joint Trajectory $\to$ Form Valid check $\to$ Increment Rep / Warning). Near the bottom, there is a branch: `Ask Voice Question` $\to$ `Speech to Text` $\to$ `AI Response Generation` $\to$ `Convert Response to Speech`.
* **Defense Verdict**: While our production implementation uses priority-debounced audio coaching cues rather than conversational speech queries, panels routinely accept this high-level activity swimlane. If you are not redrawing diagrams, leave it as is. If redrawing, change `Ask Voice Question` to `Audio Biomechanical Coaching Dispatch`.

#### Figure 3: SSD 01 — Body Measurement Tracking (Word Page 22 / PDF Page 28)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Pose Detector`, `Firebase`. Method calls: `continueBodyScan()`, `analyzeBody()`, `measurements`, `storeMeasurements()`, `saved`, `showBodyStats`.
* **Defense Verdict**: Completely generic and correct. Aligns with our anthropometric measurement tracking engine. Leave as is.

#### Figure 4: SSD 02 — Exercise Recognition (Word Page 22 / PDF Page 28)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Pose Detector`, `Exercise recognizer`. Method calls: `capturePose()`, `bodyLandmarks`, `classifyExercise()`, `exerciseType`, `showSkeletonOverlay`.
* **Defense Verdict**: Clean and generic. Aligns with PoseC3D inference pipeline. Leave as is.

#### Figure 5: SSD 03 — Injury Prediction (Word Page 23 / PDF Page 29)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Rep Counter`, `Posture Correction`, `Firebase`. Method calls: `repHistory()`, `postureMetrics()`, `riskData`, `analyzeInjuryRisk()`, `injuryAlert`, `showWarnng`.
* **Defense Verdict**: Fully aligns with Module 7 injury watchdog logic. (Note: contains a harmless minor typo `showWarnng`, but the sequence logic is sound). Leave as is.

#### Figure 6: SSD 04 — Pose Detection (Word Page 23 / PDF Page 29)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Pose Detector`, `Exercise recognizer`. Method calls: `startWorkout()`, `activateCamera()`, `detectLandmarks`, `bodyLandmarks`, `showSkeletonOverlay`.
* **Defense Verdict**: 100% standard and accurate for Module 2 Google ML Kit BlazePose. Leave as is.

#### Figure 7: SSD 05 — Posture Correction (Word Page 24 / PDF Page 30)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Posture Correction`. Method calls: `continueWorkout()`, `analyzePosture()`, `correctionAdvice`, `showSkeletonOverlay`.
* **Defense Verdict**: 100% standard and accurate for Module 5 kinematic posture engine. Leave as is.

#### Figure 8: SSD 06 — Rep Counter (Word Page 24 / PDF Page 30)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Exercise Recognizer`, `Rep Counter`, `Posture Correction`. Method calls: `PerformExercise()`, `movementData()`, `detectMovementCycle()`, `validateForm()`, alt `validRep` / `incrementRep()` / `showRepCount`, alt `correctionFeedback` / `showWarnng`.
* **Defense Verdict**: Clean alt-block sequence showing valid vs invalid reps. 100% accurate. Leave as is.

#### Figure 9: SSD 07 — Trainer Dashboard (Word Page 25 / PDF Page 31)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `Trainer`, `Trainer Dashboard`, `Firebase`. Method calls: `login()`, `authenticateTrainer()`, `accessGranted`, `requestsReports()`, `fetchAnalytics()`, `analyticsData`, `showReports`.
* **Defense Verdict**: 100% clean and generic. Aligns with Module 9 trainer portal. Leave as is.

#### Figure 10: SSD 08 — User Registration and Login (Word Page 25 / PDF Page 31)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAi`, `FireBase`. Method calls: `enterRegistrationDetails()`, `validateUserData`, `storeUserData`, `registrationSuccess`, `login(email, password)`, `authenticateUser`, `loginResult`.
* **Defense Verdict**: Standard Firebase authentication flow. 100% accurate. Leave as is.

#### Figure 11: SSD 09 — Voice Companion (Word Page 26 / PDF Page 32)
* **Status**: 🟡 **MINOR NOTE — SAFE AS-IS FOR MID-EVALUATION**
* **Detailed Audit**: Lifelines: `End User`, `BioMechAI`, `Voice Companion`, `Firebase`. Method calls: `askQuestion()`, `voiceInput()`, `processQuery()`, `response`, `voiceResponse`, `playAudio`.
* **Defense Verdict**: Generic conversational sequence. While our production companion triggers auditory alerts autonomously via kinematics without requiring user voice input, this sequence is harmless at mid-evaluation. If redrawing, change `askQuestion()` to `triggerFormCheck()` and `voiceResponse` to `speakCoachingCue()`.

#### Figure 12: Domain Model (Word Page 27 / PDF Page 33)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Entities: `Trainer`, `User`, `ProgressReport`, `InjuryAlert`, `BodyTransformationRecord`, `Workout Session`, `Repetition`, `ExerciseType`, `InjuryPrediction`, `FormAnalysisResult`. Cardinalities: User to Workout Session (1 to 0..\*), Workout Session to Repetition (1 to 1..\*), Repetition to FormAnalysisResult (1 to 1), Workout Session to InjuryPrediction (1 to 0..1), User to BodyTransformationRecord (1 to 1).
* **Defense Verdict**: Matches our actual Firestore data models and clinical parameters almost 1:1. Zero buzzwords. Completely safe.

#### Figure 13: Class Diagram (Word Page 28 / PDF Page 34)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Classes: `Trainer`, `TrainerDashboard`, `User`, `WorkoutSession`, `BodyMeasurementTracker`, `VoiceCompanion`, `PoseDetector`, `ExerciseRecognizer`, `RepCounter`, `PostureCorrection`, `InjuryPredictor`. 
* **Defense Verdict**: Excellent UML class diagram. Notably, the `User` class already contains `-height: double`, `-weight: double`, `-bmi: double`, and `+CalculateBMI()`, perfectly matching our working anthropometric implementation. Leave as is.

#### Figure 14: Component Diagram (Word Page 29 / PDF Page 35)
* **Status**: 🔴 **CRITICAL ACTION REQUIRED — MUST UPDATE IMAGE**
* **Detailed Audit**: Contains fatal buzzwords and typos that directly contradict our codebase:
  1. Mentions `AQMN (.tflite)` (academic diving model that does not exist in gym biomechanics).
  2. Mentions `PoseConvo3D (.tflite)` on-device (PoseC3D is a PyTorch server model, not a mobile .tflite).
  3. Mentions `LLaVA-1.5-7B (Google Colab)`, `Google Speech-to-Text API`, and `ElevenLabs TTS API`.
  4. Contains embarrassing typos: `"Pose Detection Enginer"` and `"Forebase Database"`.
* **Action**: Follow the step-by-step blueprint in **Section 8.2** below to update this diagram.

#### Figure 15: DFD Level 0 — Context Diagram (Word Page 30 / PDF Page 36)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: Process 0: `BioMech AI System`. External entities: `End User`, `Data Store`, `AI Services`, `Trainer`. Data flows: `video input, voice input`, `rep count, corrections, injury alerts`, `Store workout data`, `user data`, `Query Data`, `AI Analysis`, `client analytics, reports`, `feedback`.
* **Defense Verdict**: Standard, clean context diagram. Completely safe.

#### Figure 16: DFD Level 1 (Word Page 30 / PDF Page 36)
* **Status**: 🟢 **100% SAFE — NO EDIT REQUIRED**
* **Detailed Audit**: 6 sub-processes: `1. Capture and Detect Pose`, `2. Recognize Exercise`, `3. Count Reps and validate Forms`, `4. Analyze Injury Risk`, `5. Voice Companion`, `6. Trainer Analytics`. Data store: `Data Store`.
* **Defense Verdict**: Clean functional decomposition matching our 9 modules. Completely safe.

#### Figure 17: State Machine Diagram (Word Page 31 / PDF Page 37)
* **Status**: 🔴 **CRITICAL ACTION REQUIRED — MUST UPDATE IMAGE**
* **Detailed Audit**: Contains three major technical flaws:
  1. Transition from `Detecting Exercise` to `ExersizeActive` says `Confidence >85% for 2s`. In reality, our calibrated production threshold is $T = 0.50$ (50% Softmax probability) over 48 frames.
  2. Typo: spelled `ExersizeActive` instead of `ExerciseActive`.
  3. Rep loop shows generic `ValidatingForm` $\to$ `RepCounted`, completely missing our scientifically certified Closed 4-Stage Rep FSM and occlusion rejection floor ($\ge 35^\circ$).
  4. Shows voice companion as a query-response loop (`user speaks query` $\to$ `VoiceCompanionActive` $\to$ `response given`).
* **Action**: Follow the step-by-step blueprint in **Section 8.2** below to update this diagram.

#### Figure 18: Sequence Diagram (Word Page 32 / PDF Page 38)
* **Status**: 🟡 **MINOR NOTE — SAFE AS-IS FOR MID-EVALUATION**
* **Detailed Audit**: Lifelines: `User`, `Mobile App`, `Pose Detector`, `Exercise recognizer`, `Rep Counter`, `Posture Correction`, `Voice Companion`, `Firebase Cloud`. Shows complete session lifecycle: auth $\to$ camera feed $\to$ landmark detection $\to$ classification $\to$ rep counting & form validation loop $\to$ voice response $\to$ session persistence.
* **Defense Verdict**: Standard UML sequence diagram. Safe for mid-evaluation as-is.

#### Figure 19: Deployment Diagram (Word Page 33 / PDF Page 39)
* **Status**: 🔴 **CRITICAL ACTION REQUIRED — MUST UPDATE IMAGE**
* **Detailed Audit**: Contains fatal deployment contradictions:
  1. `User Smartphone` node lists `AQMN`, `PoseConvo3D`, and typo `BioMechAI.apl`.
  2. `Cloud AI Server` node lists `LLaVA-1.5-7B (4-bit)`.
  3. `External APIs` node lists `Google Speech-to-Text` and `ElevenLabs TTS`.
  4. Lists `Trainer Browser` instead of the mobile trainer app.
* **Action**: Follow the step-by-step blueprint in **Section 8.2** below to update this diagram.

---

### 8.2. Detailed Re-Engineering Blueprints for the 3 Critical Diagrams

If you have access to the original diagram files (draw.io, Lucidchart, or PowerPoint), make the exact changes below and re-export the images into your Word document.

```
========================================================================================
BLUEPRINT 1: FIGURE 14 — COMPONENT DIAGRAM (Word Page 29 / PDF Page 35)
========================================================================================
```

#### Box-by-Box Exact Changes:
1. **Component Box 1: `On-Device AI Layer`**:
   * ❌ **DELETE**: `AQMN (.tflite)`
   * ❌ **DELETE**: `PoseConvo3D (.tflite)`
   * ✅ **CHANGE / ADD**:
     - `Google ML Kit BlazePose (On-Device 30 FPS)`
     - `Four-Pattern Kinematic Engine (Dart / Vector Math)`
     - `Closed 4-Stage Repetition FSM`
     - `Native Voice Coaching Engine (flutter_tts)`
2. **Component Box 2: `Flutter Mobile App`**:
   * ❌ **FIX TYPO**: Change `"Pose Detection Enginer"` to `"Pose Detection Engine"`.
   * ✅ **KEEP**: `Camera Module`, `UI Layer`, `Form Analysis Engine`.
3. **Component Box 3: `Cloud AI Services`**:
   * ❌ **DELETE**: `LLaVA-1.5-7B (Google Colab)`
   * ❌ **DELETE**: `Google Speech-to-Text API`
   * ❌ **DELETE**: `ElevenLabs TTS API`
   * ✅ **RENAME BOX TO**: `BioMechAI AI Inference Server (Python / FastAPI / PyTorch)`
   * ✅ **INSIDE BOX, WRITE**:
     - `PoseC3D SlowOnly ResNet-50 Backbone`
     - `Spatiotemporal 3D Limb Heatmap Rasterizer`
     - `Calibrated Classification Head (T = 0.50)`
4. **Component Box 4: `Firebase Backend`**:
   * ❌ **FIX TYPO**: Change `"Forebase Database"` to `"Firebase Firestore"`.
   * ✅ **KEEP**: `Firebase Auth`, `Firebase Storage`, `Cloud Functions`.
5. **Component Box 5: `Trainer Dashboard`**:
   * ❌ **DELETE**: `Report Generator (jsPDF)`
   * ✅ **RENAME COMPONENT TO**: `Flutter Mobile Trainer Portal`
   * ✅ **INSIDE BOX, WRITE**:
     - `Client Management Roster`
     - `Video Playback & Timestamped Feedback Engine`

#### Updated Visual Layout for Figure 14:
```
+---------------------------------------------------------------------------------+
|                                 BioMechAI SRS                                    |
|                         Figure 14: Component Diagram                            |
+---------------------------------------------------------------------------------+

                      +---------------------------------------+
                      |       <<component>>                   |
                      |     Flutter Mobile App                |
                      |---------------------------------------|
                      | - Camera Module                       |
                      | - UI & Skeleton Overlay Layer         |
                      | - Pose Detection Engine               |
                      | - Form Analysis Engine                |
                      +-------------------+-------------------+
                                          |
                   +----------------------+----------------------+
                   | (Uses On-Device)     | (HTTPS Reads/Writes) | (WebSocket/REST)
                   v                      v                      v
+-------------------------------+  +--------------------+  +----------------------+
|        <<component>>          |  |   <<component>>    |  |    <<component>>     |
|      On-Device AI Layer       |  |  Firebase Backend  |  | Cloud AI Inference   |
|-------------------------------|  |--------------------|  | (FastAPI / PyTorch)  |
| - Google ML Kit BlazePose     |  | - Firestore DB     |  |----------------------|
| - Four-Pattern Kinematics     |  | - Firebase Auth    |  | - PoseC3D SlowOnly   |
| - Closed 4-Stage Rep FSM      |  | - Cloud Storage    |  |   ResNet-50 Model    |
| - On-Device TTS Engine        |  | - Cloud Functions  |  | - 3D Heatmap Engine  |
+-------------------------------+  +---------+----------+  | - Softmax Head       |
                                             ^             |   (T = 0.50)         |
                                             |             +----------------------+
                                             | (Firestore SDK)
                               +-------------+-------------+
                               |       <<component>>       |
                               | Mobile Trainer Portal     |
                               |---------------------------|
                               | - Client Management Roster|
                               | - Timestamped Feedback    |
                               +---------------------------+
```

---

```
========================================================================================
BLUEPRINT 2: FIGURE 17 — STATE MACHINE DIAGRAM (Word Page 31 / PDF Page 37)
========================================================================================
```

#### Step-by-Step Exact Changes:
1. **Fix Exercise Recognition Transition**:
   * ❌ **REMOVE**: `Confidence >85% for 2s`
   * ✅ **REPLACE WITH**: `PoseC3D Softmax Score >= 0.50 (Locked)`
2. **Fix Typo in Active State**:
   * ❌ **FIX**: Change `ExersizeActive` to `ExerciseActive`.
3. **Incorporate the 4-Stage Rep FSM Inside ExerciseActive**:
   * Replace the vague `ValidatingForm` $\to$ `RepCounted` loop with our 4-state cycle:
     - `START`: Standing neutral joint angle ($\theta \ge 146^\circ$).
     - `INFLECTION`: Descent begins ($\theta < 146^\circ$).
     - `PEAK`: Valid depth achieved ($\theta \le 115^\circ$).
     - `COMPLETION`: Ascent returns to start ($\theta \ge 146^\circ$) $\to$ `RepCount++`.
4. **Add Occlusion Safety Guard**:
   * Branch: `If joint angle < 35°` $\to$ `OcclusionRejection (Do Not Count Rep)`.
5. **Fix Voice Companion Transition**:
   * ❌ **REMOVE**: `user speaks query` $\to$ `VoiceCompanionActive` $\to$ `response given`.
   * ✅ **REPLACE WITH**: `Kinematic Deviation Detected` $\to$ `Priority Voice Cue Dispatched (flutter_tts, <10ms)`.

#### Updated Visual Layout for Figure 17:
```
+---------------------------------------------------------------------------------+
|                                 BioMechAI SRS                                    |
|                       Figure 17: State Machine Diagram                          |
+---------------------------------------------------------------------------------+

     (●) Start
      |
      v
+-------------+      user opens workout      +--------------------+
| IdleSystem  | ---------------------------> | CameraInitializing |
+-------------+                              +---------+----------+
      ^                                                | camera ready
      |                                                v
      | session saved                        +--------------------+
+-----+--------+                             | Detecting Exercise |
|SessionSaving | <----+                      +---------+----------+
+--------------+      |                                |
                      | user ends session              | PoseC3D Score >= 0.50 (Locked)
                      |                                v
           +----------+--------------------------------------------------+
           |                       ExerciseActive                        |
           |                                                             |
           |   +--------+   descent (θ < 146°)   +------------+          |
           |   | START  | ---------------------> | INFLECTION |          |
           |   +--------+                        +-----+------+          |
           |       ^                                   |                 |
           |       | ascent (θ >= 146°)                | valid depth     |
           |       | [RepCount++]                      | (θ <= 115°)     |
           |       |                                   v                 |
           |   +---+--------+                     +----+----+            |
           |   | COMPLETION | <------------------ |  PEAK   |            |
           |   +------------+                     +----+----+            |
           |                                           |                 |
           |                                           | θ < 35°         |
           |                                           v                 |
           |                               +-----------------------+     |
           |                               | OcclusionRejection    |     |
           |                               | (Ignore Glitch)       |     |
           |                               +-----------------------+     |
           |                                                             |
           |   * Kinematic Fault Detected ---> Dispatches Voice Cue      |
           |                                   (flutter_tts, <10ms)      |
           +-------------------------------------------------------------+
```

---

```
========================================================================================
BLUEPRINT 3: FIGURE 19 — DEPLOYMENT DIAGRAM (Word Page 33 / PDF Page 39)
========================================================================================
```

#### Node-by-Node Exact Changes:
1. **In Node `User Smartphone (Android / iOS)`**:
   * ❌ **FIX TYPO**: Change `BioMechAI.apl` to `BioMechAI.apk`.
   * ❌ **DELETE**: `AQMN`
   * ❌ **DELETE**: `PoseConvo3D`
   * ✅ **KEEP / ADD**:
     - `<<artifact>> BioMechAI.apk`
     - `<<artifact>> Google ML Kit BlazePose (On-Device)`
     - `<<artifact>> Four-Pattern Kinematic Engine`
     - `<<artifact>> flutter_tts Native Audio Engine`
     - `<<artifact>> Firestore Client SDK`
2. **In Node `Cloud AI Server`**:
   * ❌ **DELETE**: `LLaVA-1.5-7B (4-bit)`
   * ✅ **RENAME / ADD**:
     - `<<artifact>> FastAPI PyTorch Server`
     - `<<artifact>> PoseC3D SlowOnly ResNet-50 (best_acc_top1_epoch_10.pth)`
3. **In Node `External APIs`**:
   * ❌ **DELETE ENTIRELY**: `ElevenLabs TTS` and `Google Speech-to-Text`.
   * (You do NOT use external cloud speech APIs; TTS is 100% on-device and free).
4. **In Node `Trainer Workstation`**:
   * ❌ **CHANGE**: `Trainer Browser (React Web Dashboard)` $\to$ ✅ `Trainer Smartphone (Flutter Mobile App)`.

#### Updated Visual Layout for Figure 19:
```
+---------------------------------------------------------------------------------+
|                                 BioMechAI SRS                                    |
|                        Figure 19: Deployment Diagram                            |
+---------------------------------------------------------------------------------+

+-----------------------------------------+
|     Node: User Smartphone               |
|         (Android / iOS)                 |
|-----------------------------------------|
| <<artifact>> BioMechAI.apk              |
| <<artifact>> Google ML Kit BlazePose    |
| <<artifact>> Kinematic Form Engine      |
| <<artifact>> flutter_tts Native Audio   |
| <<artifact>> Firestore Client SDK       |
+--------------------+--------------------+
                     |
                     | HTTPS / WebSocket
                     v
+-----------------------------------------+       Firestore SDK       +----------------------+
|       Node: Cloud AI Server             | <-----------------------> | Node: Firebase Cloud |
|          (GPU / Ubuntu)                 |                           |----------------------|
|-----------------------------------------|                           | <<artifact>>         |
| <<artifact>> FastAPI PyTorch Server     |                           | Firebase Auth        |
| <<artifact>> PoseC3D ResNet-50 Model    |                           | <<artifact>>         |
|              (best_acc_top1_epoch_10)   |                           | Firestore Database   |
+-----------------------------------------+                           | <<artifact>>         |
                                                                      | Cloud Storage        |
+-----------------------------------------+                           +----------+-----------+
|     Node: Trainer Smartphone            |                                      ^
|         (Android / iOS)                 |                                      |
|-----------------------------------------|                                      |
| <<artifact>> BioMechAI Trainer App      | <------------------------------------+
| <<artifact>> Firestore Client SDK       |            Firestore SDK
+-----------------------------------------+
```

---

### 8.3. Practical Options for Your Partner to Apply Diagram Changes

1. **Option A (Best & Cleanest — If You Have draw.io / Lucidchart Source Files)**:
   * Open your diagram source files.
   * Update the text boxes in **Figure 14**, **Figure 17**, and **Figure 19** using the exact blueprints above.
   * Export as high-resolution PNGs and right-click $\to$ "Change Picture" in Word.

2. **Option B (Fast & Direct — Editing Directly Inside Microsoft Word)**:
   * If you don't have the original draw.io file, open your Word document.
   * Go to **Figure 14, 17, and 19**.
   * Insert small white rectangles (Shape: Rectangle, Fill: White, Outline: None) over the outdated labels (`AQMN`, `LLaVA-1.5-7B`, `ElevenLabs`, `.apl`).
   * Insert clean text boxes with the correct labels (`Google ML Kit`, `PoseC3D Server`, `flutter_tts`, `.apk`) directly over them, and group the shapes.

3. **Option C (Defensive Backup — Text-Only Alignment)**:
   * If your partner is unable to edit the images before the deadline, **the text updates in Sections 1 through 7 already protect you 100%**.
   * If an evaluator points to Figure 14 or 19 and asks: *"Is AQMN or LLaVA running here?"*, your defense is:
     > *"Sir, that diagram represents our initial conceptual architecture from FYP-I. During Semester 8 FYP-II implementation, as detailed in Section 3.2 of this document, we replaced AQMN with deterministic kinematic vector trigonometry (Munro FPPA knee valgus and lumbar shear) and fine-tuned PoseC3D SlowOnly ResNet-50 on FastAPI, achieving 91.22% Top-5 accuracy and sub-15ms on-device latency."*


