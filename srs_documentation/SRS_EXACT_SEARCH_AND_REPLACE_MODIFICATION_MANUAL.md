# BioMechAI — Official SRS Exact Search & Replace Modification Manual
## Complete Page-by-Page, Word-for-Word Editing Instructions for Final Evaluation (FYP-II)

**Document Reference**: `BioMechAI SRS -Final Document.pdf`  
**Purpose**: This manual gives you the exact phrases to search (using `Ctrl+F` in Word/Docs), the exact lines to remove, and the exact production-accurate, scientifically defensible text to paste in their place.

---

# Table of Contents
1. [Executive Summary of Required Updates](#1-executive-summary-of-required-updates)
2. [Section 1: Introduction Modifications (Page 7)](#2-section-1-introduction-modifications-page-7)
3. [Section 2: Vision Document & Constraints Modifications (Pages 8–11)](#3-section-2-vision-document--constraints-modifications-pages-811)
4. [Section 3.1: System Features Modifications (Page 14)](#4-section-31-system-features-modifications-page-14)
5. [Section 3.2: Functional Requirements Modifications (Pages 15–18)](#5-section-32-functional-requirements-modifications-pages-1518)
6. [Section 3.3: Non-Functional Requirements Modifications (Pages 18–19)](#6-section-33-non-functional-requirements-modifications-pages-1819)
7. [Section 4.1: Use Case Tables Corrections (Pages 20–26)](#7-section-41-use-case-tables-corrections-pages-2026)
8. [Section 4.2–4.4: Architectural & System Diagrams Updates (Pages 27–39)](#8-section-4244-architectural--system-diagrams-updates-pages-2739)

---

# 1. Executive Summary of Required Updates

Before you begin editing, here are the **5 major contradictions** currently in your SRS that an external evaluation panel will target:

1. **The "60 Exercises" Fantasy vs. 7 Panel-Mandated Exercises**:
   * *Problem*: The SRS claims PoseConv3D recognizes *"more than 60 types of exercises with 85% confidence"*.
   * *Reality*: In Semester 7 (FYP-I), the panel explicitly mandated: *"Find a pretrained model and fine-tune your 7 exercises dataset there."* You trained and certified PoseC3D SlowOnly ResNet-50 on 7 core exercises with 91.22% Top-5 accuracy. Claiming 60 exercises without training data will fail defense.
2. **The "AQMN Model" Buzzword Trap**:
   * *Problem*: The SRS mentions an `AQMN (.tflite)` model (Action Quality Measurement Network) for posture scoring (0–100).
   * *Reality*: AQMN is for Olympic diving/gymnastics requiring human judge scores. Real gym form validation uses clinical trigonometric vector kinematics (Munro FPPA valgus, hip sag, elbow flare). AQMN must be replaced with the Four-Pattern Kinematic Engine.
3. **The "SMPL 3D Body Mesh" Trap**:
   * *Problem*: The SRS claims the app generates 3D body meshes from photos using SMPL to measure waist/chest circumference.
   * *Reality*: SMPL models are 300MB+, require heavy GPUs, and cannot run on a phone. The real working feature is Anthropometric Height-Calibrated Landmark Scaling, BMI computation, and Devine Ideal Weight tracking.
4. **The "30 Sessions for Injury Prediction" Trap**:
   * *Problem*: The SRS states injury prediction requires 30 past sessions using an LSTM + Isolation Forest.
   * *Reality*: If an evaluator tests your app live, it will say *"Insufficient data"* because 30 sessions don't exist! More importantly, ACL tears happen in a single rep. BioMechAI uses a real-time acute injury watchdog (Munro FPPA $< 165^\circ$ for ACL, hip sag $> 10\%$ for lumbar shear) active on *every single rep*.
5. **The "LLaVA-1.5-7B on Google Colab" Voice Trap**:
   * *Problem*: The SRS claims a 7-billion parameter vision-language model runs on Google Colab with ElevenLabs TTS.
   * *Reality*: Colab disconnects, ElevenLabs costs money and adds 2 seconds of latency. A user tears an ACL in 100ms! You built native on-device speech (`flutter_tts`) with 3-tier priority preemption and a 3.0s watchdog timer that speaks in $< 10\text{ms}$.

---

# 2. Section 1: Introduction Modifications (Page 7)

### Edit 1.1: Fix the "Eight Modules" Count Typo
* **Where in SRS**: Page 7, Section 1 (*Introduction*), Paragraph 2, Line 5.
* **Search for (Ctrl+F)**: `For the mid-evaluation stage, the project is divided into the following eight modules:`
* **Current Text to Remove**:
  > For the mid-evaluation stage, the project is divided into the following eight modules:
* **Replacement Text to Paste**:
  > For the final graduation evaluation (Semester 8), the project is structured into the following nine (9) comprehensive modules:
* **Why**: The text said *"eight modules"* but listed nine bullets. Also, we are in final graduation defense (FYP-II), not mid-evaluation.

---

# 3. Section 2: Vision Document & Constraints Modifications (Pages 8–11)

### Edit 2.1: Update Problem Statement Solution Table
* **Where in SRS**: Page 8, Section 2.1 (*Table 1: Problem Statement*), Category: Solution.
* **Search for (Ctrl+F)**: `Include an AI voice companion that can talk with the user`
* **Current Text to Remove**:
  > • Include an AI voice companion that can talk with the user and give personalized workout guidance.
* **Replacement Text to Paste**:
  > • Include a real-time on-device voice coaching companion that delivers instantaneous, priority-debounced auditory safety cues, rep milestones, and recovery praise during active exercise.
* **Why**: Prevents panelists from expecting a conversational chatbot like ChatGPT while exercising, focusing instead on real-time acoustic biomechanical coaching.

---

### Edit 2.2: Update Objectives
* **Where in SRS**: Page 9, Section 2.3 (*Objectives*), Bullets 2, 4, 5, 6.
* **Search for (Ctrl+F)**: `Implement automatic exercise recognition so the system can identify different workouts`
* **Current Text to Remove**:
  > • Implement automatic exercise recognition so the system can identify different workouts without the user needing to select them manually.  
  > • Allow users to monitor their physical progress through a body measurement and transformation tracking feature that uses 3D body modeling.  
  > • Build an AI-based injury prediction system that studies movement changes over time and warns users about possible injury risks before they happen.  
  > • Introduce a conversational AI voice companion that gives users real-time coaching, motivation, and feedback while they are exercising.
* **Replacement Text to Paste**:
  > • Implement automatic exercise classification across seven (7) core fundamental gym exercises utilizing a 3D spatiotemporal convolutional neural network (PoseC3D SlowOnly ResNet-50) pretrained on FineGYM and fine-tuned on the BioMechAI dataset.  
  > • Allow users to monitor their physical transformation through an anthropometric measurement tracking feature calibrated by user height, live Body Mass Index (BMI) computation, and the clinical Devine Ideal Body Weight formula.  
  > • Build a dual-horizon AI injury prediction engine that detects acute joint collapse in real time (e.g., dynamic knee valgus $< 165^\circ$ for ACL injury, lumbar hip sag for spinal disc compression, and shoulder flare for impingement) while logging inter-session fatigue trends.  
  > • Introduce a real-time, on-device AI voice companion that provides sub-10ms priority-preempted audio corrections and form encouragement without requiring an active internet connection.
* **Why**: Aligns objectives directly with the panel's mandate, eliminates unbuilt 3D mesh buzzwords, and proves clinical relevance.

---

### Edit 2.3: Fix Scope
* **Where in SRS**: Page 10, Section 2.4 (*Scope*), Lines 4–5.
* **Search for (Ctrl+F)**: `the system will be designed to run on both web and mobile platforms.`
* **Current Text to Remove**:
  > In the beginning, the system will be designed to run on both web and mobile platforms.
* **Replacement Text to Paste**:
  > The system is architected as a high-performance Flutter mobile application for athletes and personal trainers, communicating via high-speed WebSockets and REST APIs with a dedicated PyTorch/FastAPI backend inference engine for deep spatiotemporal neural network evaluation.
* **Why**: Clarifies the exact dual-timescale architecture built in your project.

---

### Edit 2.4: Replace Impractical Constraints
* **Where in SRS**: Page 10, Section 2.5 (*Constraints*), Bullets 4, 5, 6.
* **Search for (Ctrl+F)**: `LLaVA-1.5-7B runs in the cloud on Google Colab`
* **Current Text to Remove**:
  > • LLaVA-1.5-7B runs in the cloud on Google Colab, which can cause 500ms-1s delays for complex AI companion responses.  
  > • The accuracy of body measurement depends on the quality of 2D images, lighting conditions, and the user’s clothing.  
  > • Injury prediction requires at least 30 workout sessions before it can provide reliable risk assessments.
* **Replacement Text to Paste**:
  > • Deep learning spatiotemporal inference (PoseC3D) requires a GPU-enabled backend server (NVIDIA T4 or equivalent) for batched 3D convolutional tensor evaluations within 45ms.  
  > • Anthropometric body tracking relies on standardized vertical user framing and calibrated reference stature (height) for metric conversion.  
  > • Acute injury prediction operates instantaneously on every single repetition using clinical kinematic angle cutoffs (e.g., Munro FPPA $< 165.0^\circ$ for knee valgus), while chronic overuse trends require cumulative multi-session logs.
* **Why**: Removes Colab and 30-session dependencies which would fail during a live jury defense.

---

# 4. Section 3.1: System Features Modifications (Page 14)

### Edit 4.1: Modernize All 8 Feature Descriptions
* **Where in SRS**: Page 14, Section 3.1 (*System Features*).
* **Search for (Ctrl+F)**: `BioMechAI provides the following core system features across the eight evaluated modules:`
* **Current Text to Remove**:
  > BioMechAI provides the following core system features across the eight evaluated modules:  
  > • Real-time 3D Pose Detection: The system detects 33 body landmarks in real time at around 30 frames per second and shows a skeleton overlay using MediaPipe Pose Lite.  
  > • Exercise Recognition: The system automatically identifies more than 60 types of exercises using the PoseConv3D model on short movement clips, with a confidence level of about 85%.  
  > • Rep Counting and Form Validation: The system counts repetitions only when the correct movement pattern is detected, using motion peaks and valleys along with basic movement safety checks.  
  > • Posture Correctness (Four-Pattern Engine): The system checks posture using sports science rules, machine learning quality scoring, time-based movement analysis, and adjusts limits based on the user’s body type.  
  > • Body Measurement Tracking: The system creates a simple 3D body model from user photos using SMPL methods and standard body measurement formulas to track physical changes over time.  
  > • AI Injury Prediction: The system studies workout data across more than 30 sessions using LSTM and Isolation Forest models to predict possible injury risks and suggest preventive steps.  
  > • AI Voice Companion: The system provides continuous voice guidance and motivation during workouts using AI vision-language understanding, speech recognition, and text-to-speech technologies.  
  > • Trainer Dashboard: A React-based web portal allows trainers to review AI-annotated workout videos, view client progress data, and generate automatic performance reports in PDF format.
* **Replacement Text to Paste**:
  > BioMechAI delivers the following core system features across its nine (9) verified production modules:  
  > • **Module 1: User Registration and Login**: Secure multi-role authentication (Athlete vs. Trainer) using Firebase Auth and Cloud Firestore profile persistence.  
  > • **Module 2: Real-time 3D Pose Detection**: Extracts 33 normalized 3D anatomical landmarks at 30 FPS using Google ML Kit BlazePose running natively on-device with custom low-latency visual skeleton overlays.  
  > • **Module 3: Exercise Classification (PoseC3D Deep Learning Engine)**: Classifies user movement into seven (7) fundamental exercises using a 3D spatiotemporal ResNet-50 network fine-tuned on FineGYM limb heatmaps, achieving 91.22% Top-5 accuracy on held-out test splits.  
  > • **Module 4: Real-time Rep Counting and Form Validation**: Employs a deterministic Closed 4-Stage Repetition Finite State Machine (START $\to$ INFLECTION $\to$ PEAK $\to$ COMPLETION) with un-clamped joint flexion and camera boundary occlusion rejection ($\ge 35^\circ$).  
  > • **Module 5: Posture Correctness (Four-Pattern Kinematic Engine)**: Evaluates sagittal depth flexion, frontal knee alignment, trunk neutrality, and framing sanity in $< 0.1\text{ms}$ using clinically validated vector trigonometry.  
  > • **Module 6: Body Measurement and Transformation Tracking**: Tracks user anthropometric dimensions, computes live BMI with color-coded classification gauges, determines physiological target weight using the Devine formula, and persists historical progress to Firestore.  
  > • **Module 7: AI Clinical Injury Prevention Engine**: Real-time full-body injury guard monitoring Munro Dynamic Knee Valgus FPPA ($< 165^\circ$ under load $\le 130^\circ$) for acute ACL protection, lumbar hip sag ($> 10\%$) for spinal shear protection, and elbow flare ($> 65^\circ$) for rotator cuff impingement.  
  > • **Module 8: AI Workout Companion with Live Voice Coaching**: Provides zero-latency, on-device audio coaching (`flutter_tts`) governed by a 3-tier priority queue (Priority 1: Emergency Safety Warnings, Priority 2: Rep Milestones, Priority 3: Form Praise) with dynamic cooldown debouncing.  
  > • **Module 9: Trainer Dashboard & Timestamped Feedback**: A comprehensive coaching portal within the Flutter ecosystem enabling certified trainers to inspect client rosters, review form scores, and leave second-by-second timestamped corrective notes.
* **Why**: Fully synchronizes the feature summary with all 9 modules, fixes the "eight modules" error, and replaces fictional components with verified code.

---

# 5. Section 3.2: Functional Requirements Modifications (Pages 15–18)

### Edit 5.1: Functional Requirement 3.2.1 (Pose Detection)
* **Where in SRS**: Page 15, Section 3.2.1, Bullet 5.
* **Search for (Ctrl+F)**: `On LiDAR-supported iPhones, the system shall use ARKit depth information`
* **Current Text to Remove**:
  > • On LiDAR-supported iPhones, the system shall use ARKit depth information to improve the accuracy of 3D body coordinates.
* **Replacement Text to Paste**:
  > • The system shall utilize MediaPipe's relative 3D z-depth coordinate estimates to measure sagittal-plane depth and forward torso inclination across standard monocular smartphone cameras without requiring specialized LiDAR hardware.
* **Why**: You do not have an iPhone LiDAR app implementation; claiming it will invite the panel to ask for an iPhone LiDAR demo.

---

### Edit 5.2: Functional Requirement 3.2.2 (Exercise Recognition)
* **Where in SRS**: Page 15, Section 3.2.2, All Bullets.
* **Search for (Ctrl+F)**: `The system shall support recognition of at least 60 different exercises`
* **Current Text to Remove**:
  > • The system shall support recognition of at least 60 different exercises from categories such as strength training, cardio, core workouts, and yoga.  
  > • The system shall analyze 3D movement patterns using a 3-second sliding window and the PoseConv3D model.  
  > • Exercise recognition shall be confirmed only when the confidence level reaches 85% for two continuous seconds.
* **Replacement Text to Paste**:
  > • The system shall recognize seven (7) core athletic compound and isolation exercises: Squat, Push-Up, Lunge, Bicep Curl, Plank, Jumping Jack, and High Knees.  
  > • The system shall convert 48 consecutive frames of 17-channel COCO anatomical joint coordinates into spatiotemporal 3D limb heatmaps ($56 \times 56 \times 48$) with Gaussian tubular segments ($\sigma = 0.6$).  
  > • The system shall classify the spatiotemporal volume using a SlowOnly ResNet-50 3D convolutional neural network (PoseC3D) initialized with OpenMMLab FineGYM pretrained weights and a calibrated classification head.  
  > • Classification decisions shall be locked when model softmax probability exceeds the calibrated deployment threshold ($T = 0.50$).
* **Why**: Accurately reflects the PoseC3D champion model (`best_acc_top1_epoch_10.pth`) and the panel's 7-exercise mandate.

---

### Edit 5.3: Functional Requirement 3.2.3 (Rep Counting)
* **Where in SRS**: Page 15–16, Section 3.2.3.
* **Search for (Ctrl+F)**: `The system shall identify complete repetitions by detecting peaks and valleys in joint movement data.`
* **Current Text to Remove**:
  > • The system shall identify complete repetitions by detecting peaks and valleys in joint movement data.  
  > • Each repetition shall be checked against defined movement safety limits before increasing the repetition count.
* **Replacement Text to Paste**:
  > • The system shall implement a Closed 4-Stage Repetition Finite State Machine (FSM):  
  >   1. `START`: Baseline standing posture ($\theta \ge 146.0^\circ$).  
  >   2. `INFLECTION`: Descent phase initiated ($\theta < 146.0^\circ$).  
  >   3. `PEAK`: Valid exercise depth attained (e.g., knee flexion $\le 115.0^\circ$ for squats, elbow flexion $\le 95.0^\circ$ for push-ups).  
  >   4. `COMPLETION`: Full extension restored ($\theta \ge 146.0^\circ$), incrementing rep count by exactly +1.  
  > • Repetitions failing to reach the required peak depth threshold shall be classified as partial/incomplete reps and rejected without incrementing the counter.  
  > • The system shall enforce an anatomical sanity floor ($\theta \ge 35.0^\circ$) to discard sudden optical occlusion glitches.
* **Why**: Peak/valley detection is a batch post-processing algorithm that cannot run live; the 4-Stage FSM is what you actually built in `backend/kinematics.py`.

---

### Edit 5.4: Functional Requirement 3.2.4 (Posture Correctness)
* **Where in SRS**: Page 16, Section 3.2.4.
* **Search for (Ctrl+F)**: `The system shall use the AQMN model to give a movement quality score between 0 and 100`
* **Current Text to Remove**:
  > • The system shall use the AQMN model to give a movement quality score between 0 and 100 and detect common technique mistakes.  
  > • The system shall study movement smoothness by calculating factors like sudden motion changes, exercise rhythm, and left-right body balance.  
  > • The system shall adjust posture limits based on the user’s body proportions collected during onboarding, using standard body measurement references.
* **Replacement Text to Paste**:
  > • The system shall evaluate exercise posture using a Four-Pattern Clinical Kinematic Vector Engine based on peer-reviewed biomechanical literature:  
  >   1. **Sagittal Depth Flexion**: Measures target joint extension/flexion using vector dot products against gold-standard standards (Schoenfeld 2010, Escamilla 2001).  
  >   2. **Frontal Plane Projection Angle (FPPA)**: Monitors medial-lateral deviation of the knee joint relative to the hip-ankle line (Munro et al. 2012).  
  >   3. **Trunk and Spinal Neutrality**: Computes pelvic-shoulder angle relative to the gravity axis to detect compensatory lumbar hyperextension or excessive forward lean (McGill 2010).  
  >   4. **Camera Framing Guards**: Filters out landmark estimates whenever key tracking joints intersect camera borders ($y > 0.94$).  
  > • The system shall render real-time color-coded skeleton feedback (green = acceptable form, red = kinematic violation) alongside corrective text overlays.
* **Why**: Completely purges the fictional "AQMN model" and specifies the four-pattern kinematic system built in your code.

---

### Edit 5.5: Functional Requirement 3.2.5 (Body Measurement)
* **Where in SRS**: Page 16, Section 3.2.5.
* **Search for (Ctrl+F)**: `create a 3D body model using SMPL.`
* **Current Text to Remove**:
  > • The system shall use MediaPipe Pose to detect 2D body points from photos and create a 3D body model using SMPL.  
  > • The system shall estimate body measurements such as chest, waist, hips, arms, and thighs using formulas adjusted with the user’s height.  
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
* **Where in SRS**: Page 17, Section 3.2.6.
* **Search for (Ctrl+F)**: `The system shall study joint movement data collected from at least 30 workout sessions using an LSTM neural network.`
* **Current Text to Remove**:
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
* **Where in SRS**: Page 17, Section 3.2.7.
* **Search for (Ctrl+F)**: `The system shall support continuous two-way voice communication during the workout using live speech recognition.`
* **Current Text to Remove**:
  > • The system shall support continuous two-way voice communication during the workout using live speech recognition.  
  > • The system shall count repetitions aloud, give motivation, and answer exercise-related questions while the user is training.  
  > • The AI companion shall remember workout details such as the current exercise, completed repetitions, corrections given, and signs of user fatigue.  
  > • Voice replies shall sound natural, with less than 500 milliseconds delay for on-device responses and less than 1.5 seconds for cloud-based queries.  
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
* **Where in SRS**: Page 17–18, Section 3.2.8.
* **Search for (Ctrl+F)**: `The Trainer Dashboard shall be a React-based web application`
* **Current Text to Remove**:
  > • The Trainer Dashboard shall be a React-based web application secured through Firebase login and usable on common desktop browsers.  
  > • Trainers shall be able to watch recorded workout videos with AI-generated skeleton overlays and time-based error highlights.  
  > • The system shall automatically create monthly PDF reports for each client using jsPDF, summarizing form quality, repetition trends, consistency, and injury alerts.
* **Replacement Text to Paste**:
  > • The Trainer Dashboard shall be a specialized portal within the Flutter mobile application, secured via Firebase Authentication role separation (`role: 'trainer'`).  
  > • The dashboard shall display a real-time client roster showing client workout history, average form compliance scores, and completed repetition totals.  
  > • Trainers shall be able to select any client session and attach second-by-second timestamped coaching feedback (e.g., linked to specific rep timestamps) stored in Cloud Firestore.  
  > • Athletes shall receive and view these coach annotations directly within their personal workout summary views.
* **Why**: Reflects the native Flutter `TrainerDashboardScreen` and `TrainerFeedback` model implemented in your codebase, avoiding fake claims of a separate React website.

---

# 6. Section 3.3: Non-Functional Requirements Modifications (Pages 18–19)

### Edit 6.1: NFR 3.3.1 (Performance) & 3.3.5 (Compatibility)
* **Where in SRS**: Page 18–19, Section 3.3.1 & 3.3.5.
* **Search for (Ctrl+F)**: `End-to-end pose detection and form feedback delay shall not exceed 100 milliseconds`
* **Current Text to Remove**:
  > • The Trainer Dashboard web portal shall work properly on Chrome 90+, Firefox 88+, and Safari 14+ browsers.  
  > • All AI models shall run on devices with at least 3GB RAM and a Snapdragon 660 or similar processor.
* **Replacement Text to Paste**:
  > • On-device pose estimation and kinematic form feedback shall execute within 15 milliseconds per frame on standard Android devices (Snapdragon 720G or equivalent), sustaining 30 FPS camera capture.  
  > • Spatiotemporal 3D convolutional classification (PoseC3D) evaluated on the Python FastAPI server shall return top-class predictions within 45 milliseconds per 48-frame clip.  
  > • The mobile application shall be compatible with Android 8.0 (API Level 26) or higher and iOS 14.0 or higher.
* **Why**: Correctly reports benchmarked latencies (15ms on-device, 45ms server) and removes desktop browser web requirements.

---

# 7. Section 4.1: Use Case Tables Corrections (Pages 20–26)

In your current SRS, **Tables 9 through 19 have severely scrambled module numbers** (e.g., Voice Assistance is called Module 3, Injury is called Module 4, Admin is called Module 5).

Here is the exact search and replace table to fix every single Use Case:

| Table # | Use Case Name | Search for (Ctrl+F) | Current WRONG Module | Correct Replacement Module |
| :--- | :--- | :--- | :---: | :---: |
| **Table 8** | Register and Login User | `Module 1` | Module 1 | **Module 1 (User Registration & Login)** |
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
* **Where in SRS**: Page 25–26, Table 19 (*High-Level Use Case*).
* **Search for (Ctrl+F)**: `Table 19: High-Level Use Case`
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

# 8. Section 4.2–4.4: Architectural & System Diagrams Updates (Pages 27–39)

### 8.1. Component Diagram (Figure 14, Page 35)
In your diagram image `Figure 14: Component Diagram`:
1. **Remove Box**: `AQMN (.tflite)` from *On-Device AI Layer*.  
   * **Replace with**: `Four-Pattern Kinematic Form Engine (Dart / Vector Math)`.
2. **Remove Box**: `LLaVA-1.5-7B (Google Colab)`, `Google Speech-to-Text API`, and `ElevenLabs TTS API` from *Cloud AI Services*.  
   * **Replace with**:  
     - Move Voice to On-Device: `Native Voice Coaching Engine (flutter_tts)`.  
     - Update Server: `BioMechAI AI Inference Server (Python / FastAPI / PyTorch)` containing `PoseC3D SlowOnly ResNet-50 Backbone`.
3. **Update Trainer Dashboard**: Change label from *"Web-based React Portal"* to *"Flutter Mobile Trainer Portal"*.

---

### 8.2. State Machine Diagram (Figure 17, Page 37)
In `Figure 17: State Machine Diagram`:
* The states inside exercise tracking currently show generic `ValidatingForm` $\to$ `RepCounted`.
* **Update to show the official 4-Stage Rep FSM**:
  $$\text{START (Standing } \theta \ge 146^\circ) \longrightarrow \text{INFLECTION (Descent } \theta < 146^\circ) \longrightarrow \text{PEAK (Valid Depth } \theta \le 115^\circ) \longrightarrow \text{COMPLETION (Ascent } \theta \ge 146^\circ \to \text{RepCount++})$$
  Add the safety branch: If $\theta < 35^\circ$, transition to `OcclusionRejection`.

---

### 8.3. Deployment Diagram (Figure 19, Page 39)
In `Figure 19: Deployment Diagram`:
1. **User Smartphone Node**:
   * Contains: `Flutter Mobile App`, `Google ML Kit BlazePose (On-Device)`, `Four-Pattern Kinematic Engine`, `flutter_tts Native Audio Engine`, `Firestore Client SDK`.
   * **Remove**: `AQMN`, `PoseConvo3D (.tflite)` (PoseC3D runs on server, not directly as .tflite).
2. **Cloud AI Server Node**:
   * Contains: `FastAPI WebSocket / HTTP Server`, `PoseC3D SlowOnly ResNet-50 Model (PyTorch, checkpoint epoch_10.pth)`, `Limb Heatmap Rasterizer`.
   * **Remove**: `LLaVA-1.5-7B (4-bit)`.
3. **External APIs**:
   * **Remove**: `ElevenLabs TTS`, `Google Speech-to-Text`.
4. **Trainer Node**:
   * Shows `Trainer Smartphone (Flutter App)` connected via Firebase Auth and Firestore.
