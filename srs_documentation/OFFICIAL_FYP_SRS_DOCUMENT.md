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

In addition, this Software Requirements Specification (SRS) clearly describes the system’s functional requirements (what the system should do) and non-functional requirements (how well the system should perform). It also includes the use case models and the guidelines for designing artifacts that will be used while building the BioMechAI system. For the mid-evaluation stage, the project is divided into the following eight modules:
* **Module 1**: User Registration and Login
* **Module 2**: Real-time 3D Pose Detection
* **Module 3**: Exercise Recognition and Classification
* **Module 4**: Real-time Rep Counting and Form Validation
* **Module 5**: Posture Correctness (Four-Pattern Form Correction)
* **Module 6**: Body Measurement and Transformation Tracking
* **Module 7**: AI Injury Prediction
* **Module 8**: AI Workout Companion with Voice Conversation
* **Module 9**: Trainer Dashboard

---

## 2. Vision Document

### 2.1. Problem Statement
| Category | Description |
| :--- | :--- |
| **Problem** | • Personal training sessions are expensive, and many users cannot afford them, as a single session can cost a large amount of money.<br/>• Around 45% of people who go to the gym experience injuries because they perform exercises with the wrong form and there is no system to correct them instantly.<br/>• Most fitness applications only provide general workout plans. They are not personalized and do not give real-time 3D feedback about body movement during exercises. |
| **Affects** | • People of all fitness levels who want to exercise safely and improve their training.<br/>• The wider health and fitness community, including physiotherapists, fitness coaches, and sports medicine professionals. |
| **Impact** | • Leads to avoidable injuries, extra medical costs, and people training on their own without proper guidance.<br/>• Creates a gap in preventive health because there are very few affordable tools that combine movement analysis with personalized coaching. |
| **Solution** | An AI-powered personal fitness trainer that works on a smartphone and uses real-time movement analysis. The system will:<br/>• Provide real-time 3D pose correction and recognize the exercise being performed.<br/>• Automatically count repetitions while checking if the exercise form is correct.<br/>• Analyze movement patterns during workouts to predict possible injury risks.<br/>• Include an AI voice companion that can talk with the user and give personalized workout guidance.<br/>• Work completely on normal smartphones so users do not need expensive or specialized equipment. |

### 2.2. Business Opportunities
BioMechAI aims to solve an important problem in accessible personal fitness while also creating a strong business opportunity. The system can support a premium subscription model for users and also allow partnerships with rehabilitation clinics, sports academies, and corporate wellness programs. Through these partnerships, this application can provide scalable AI-based coaching that analyzes body movement and exercise form.

### 2.3. Objectives
Following are the objectives of BioMechAI:
* Develop a real-time 3D pose detection system that can run smoothly on normal smartphones and accurately track the user’s body movements.
* Implement automatic exercise recognition so the system can identify different workouts without the user needing to select them manually.
* Provide a form validation system that checks movement patterns to make sure exercises are performed safely, with correct posture, and flags movements that may cause injury.
* Allow users to monitor their physical progress through a body measurement and transformation tracking feature that uses 3D body modeling.
* Build an AI-based injury prediction system that studies movement changes over time and warns users about possible injury risks before they happen.
* Introduce a conversational AI voice companion that gives users real-time coaching, motivation, and feedback while they are exercising.
* Provide certified personal trainers with a dedicated dashboard so they can manage, review, and guide their remote clients using AI-supported workout videos.
* Use optimization methods so that all AI models run efficiently and respond in real time on mid-range smartphones, ensuring a smooth experience.

### 2.4. Scope
The scope of BioMechAI includes developing a complete personal fitness platform that focuses on real-time 3D body movement analysis, exercise recognition with form checking, AI-based injury prediction, and conversational coaching. In the beginning, the system will be designed to run on both web and mobile platforms.

### 2.5. Constraints
* All AI processing must finish within 100ms on mid-range devices (equivalent to Snapdragon 720G or better).
* AI model sizes must stay under 50MB on the device after INT8 quantization to comply with app store limits.
* During academic testing, the Firebase free tier restricts the number of concurrent users to about 50-100 active users.
* LLaVA-1.5-7B runs in the cloud on Google Colab, which can cause 500ms-1s delays for complex AI companion responses.
* The accuracy of body measurement depends on the quality of 2D images, lighting conditions, and the user’s clothing.
* Injury prediction requires at least 30 workout sessions before it can provide reliable risk assessments.

### 2.6. Stakeholder and User Description

#### 2.6.1. Market Demographics
The primary target market for this app includes fitness-conscious individuals aged 16 to 45 who exercise on their own, either at home or in gyms, without regular access to personal trainers. Secondary markets include certified fitness trainers who want AI-assisted tools to manage and monitor clients, physiotherapists who use movement analysis for rehabilitation, and sports academies focused on tracking athletes’ form and performance. In Pakistan and South Asia, BioMechAI’s smartphone-based approach makes professional fitness guidance more affordable, helping users overcome economic barriers.

#### 2.6.2. User Environment
End users interact with BioMechAI through the Flutter mobile app on Android or iOS smartphones. They perform workouts in different settings such as homes, gyms, or outdoor spaces, with the phone placed 1.5-3 metres away on a stand or flat surface. Trainers access the system using web portal on desktop browsers like Chrome, Firefox, or Safari. Most AI processing happens directly on the device, while cloud services like LLaVA and Firebase need a stable internet connection. If the connection is weak, the system continues to work by disabling cloud-based voice features and relying on on-device models for essential functionality.

#### 2.6.3. Stakeholder Profiles
* **Supervisor Team**: Mr. Mughees Ismail, Dr. Muhammad Usama (Academic direction, review, project progress).
* **Development Team**: Muhammad Abdullah, Muhammad Abdul Hanan Nadeem, Zainab Haider (Full SDLC, model training, mobile/web app).
* **End Users**: General public, fitness enthusiasts (Real-time form tracking, feedback).
* **Certified Trainers**: Professional fitness coaches (Client management, video reviews, training plans).
* **Admin**: Backend management, Firebase/cloud monitoring, user account control.

---

## 3. System Requirements Specification

### 3.1. System Features
* **Real-time 3D Pose Detection**: Detects 33 body landmarks in real time at around 30 FPS with skeleton overlay using MediaPipe Pose Lite.
* **Exercise Recognition**: Automatically identifies more than 60 types of exercises using PoseConv3D on short movement clips with ~85% confidence.
* **Rep Counting and Form Validation**: Counts repetitions only when correct movement patterns are detected via motion peaks and valleys with safety checks.
* **Posture Correctness (Four-Pattern Engine)**: Checks posture using sports science rules, machine learning quality scoring, time-based movement analysis, and user body proportions.
* **Body Measurement Tracking**: Creates a simple 3D body model from user photos using SMPL methods and standard formulas to track physical changes.
* **AI Injury Prediction**: Studies workout data across 30+ sessions using LSTM and Isolation Forest models to predict injury risks and suggest preventive steps.
* **AI Voice Companion**: Continuous voice guidance and motivation during workouts using AI vision-language understanding, speech recognition, and text-to-speech.
* **Trainer Dashboard**: React-based web portal allowing trainers to review AI-annotated workout videos, client data, and generate PDF reports.

### 3.2. Functional Requirements

#### 3.2.1. Real-time 3D Pose Detection
* Video capture at minimum 30 FPS.
* Detect 33 body points with X, Y, Z coordinates using MediaPipe Pose Lite.
* Skeleton overlay using OpenGL with total delay below 100ms.
* Ring buffer of 90 frames for movement analysis.
* On LiDAR-supported iPhones, use ARKit depth information.

#### 3.2.2. Exercise Recognition and Classification
* Automatically recognize exercises without manual input.
* Support recognition of at least 60 different exercises (strength, cardio, core, yoga).
* 3-second sliding window with PoseConv3D model.
* Confirmation when confidence reaches 85% for two continuous seconds.
* Display exercise name and load exercise-specific movement rules.

#### 3.2.3. Real-time Rep Counting and Form Validation
* Track primary joint movements (e.g. hip in squats, elbow in pushups).
* Peak and valley detection in joint movement data.
* Validate repetitions against safety limits before incrementing count.
* Reject unsafe/incomplete reps with visual warnings.
* Real-time display of rep count, speed, and form quality score.

#### 3.2.4. Posture Correctness
* Joint angles and body posture checked against sports science limits.
* Use AQMN model for quality score (0–100) and mistake detection.
* Evaluate movement smoothness, sudden changes, rhythm, and left-right balance.
* Dynamic limit adjustment based on user onboarding body proportions.
* Visual correction arrows and colored skeleton (red = mistake, green = correct) + voice feedback.

#### 3.2.5. Body Measurement and Transformation Tracking
* Front and side photos to construct body model.
* MediaPipe Pose 2D keypoints + SMPL 3D body mesh reconstruction.
* Height-adjusted estimation of chest, waist, hips, arms, and thighs.
* Firestore storage and side-by-side historical comparison.
* Color-based delta visuals (e.g., blue = waist reduction, green = muscle gain).

#### 3.2.6. AI Injury Prediction
* Movement data analysis across 30+ workout sessions via LSTM neural network.
* Isolation Forest for anomaly detection vs. historical user baseline.
* Integration with sports medicine reference database.
* Push notifications for injury risk > 60% (Low, Medium, High).
* Automated suggestion of corrective exercises and rest days.

#### 3.2.7. AI Workout Companion with Voice Conversation
* Continuous two-way voice communication via live speech recognition.
* Auditory rep counting, motivational feedback, and workout Q&A.
* Context retention (exercise, completed reps, corrections, fatigue signs).
* Latency: < 500ms on-device, < 1.5s for cloud queries.
* Adaptive workout intensity based on user fatigue voice input.

#### 3.2.8. Trainer Dashboard
* React-based web application with Firebase Authentication.
* Client roster display with activity status, form quality scores, and history.
* Video playback with AI skeleton overlay and time-based error tags.
* Time-specific written coaching feedback directly on workout videos.
* Automated monthly PDF client progress reports via jsPDF.

### 3.3. Non-Functional Requirements
* **Performance**: End-to-end feedback delay $\le 100\text{ms}$; exercise confirmation in 3–5 seconds; 30 FPS camera processing without drops.
* **Usability**: Onboarding complete in $\le 5$ minutes; icon- and color-based overlays understandable without reading text.
* **Reliability**: On-device pose detection, rep counting, and form validation work 100% offline; resume within 2s after phone call interruption.
* **Security & Privacy**: TLS 1.3 encryption in transit; Firestore encrypted at rest; workout videos not stored without user consent; OAuth 2.0 / Firebase Auth.
* **Compatibility**: Android 8.0+ / iOS 14.0+; Desktop Chrome 90+, Firefox 88+, Safari 14+; min 3GB RAM on Snapdragon 660 or equivalent.

---

## 4. Project Artefacts

### 4.1. Use Case Model
* **UC-01**: Register and Login User (End User, Module 1)
* **UC-02**: Track Body Measurements (End User, Module 1)
* **UC-03**: Detect Real Time 3D Pose (AI System, Module 2)
* **UC-04**: Recognize Exercise (AI System, Module 2)
* **UC-05**: Assist Via Voice (End User, Module 3 / Module 8)
* **UC-06**: Provide Posture Correction and Feedback (End User, Module 3 / Module 5)
* **UC-07**: Count Reps and Validate Form (End User, Module 3 / Module 4)
* **UC-08**: Predict Injury (Certified Trainer, Module 4 / Module 7)
* **UC-09**: Manage Users (Admin, Module 5)
* **UC-10**: View Reports (Admin, Module 5)
* **UC-11**: Access Trainer Dashboard (Certified Trainer, Module 5 / Module 9)

### 4.2. Structural Design
* **Domain Model (Figure 12)**: Entities include `Trainer`, `User`, `ProgressReport`, `BodyTransformationRecord`, `InjuryAlert`, `WorkoutSession`, `Repetition`, `ExerciseType`, `FormAnalysisResult`, `InjuryPrediction`.
* **Class Diagram (Figure 13)**: Class hierarchies for `PoseDetector`, `ExerciseRecognizer`, `RepCounter`, `PostureCorrection`, `InjuryPredictor`, `VoiceCompanion`, `BodyMeasurementTracker`.
* **Component Diagram (Figure 14)**:
  - Mobile: Flutter App (Camera, UI, Pose Engine, Form Analysis Engine).
  - On-Device AI: MediaPipe Pose Lite (`.tflite`), PoseConvo3D (`.tflite`), AQMN (`.tflite`).
  - Cloud AI Services: LLaVA-1.5-7B (Google Colab), Google Speech-to-Text API, ElevenLabs TTS API.
  - Backend: Firebase (Database, Auth, Storage, Cloud Functions).
  - Web: Trainer Dashboard (Client Management, AI Video Player, jsPDF).

### 4.3. Behavioral Design
* **Data Flow Diagrams (DFD Level 0 & 1, Figures 15 & 16)**: Pipeline data flow from user video/voice to AI system, data store, and trainer.
* **State Machine Diagram (Figure 17)**: States from `IdleSystem` $\to$ `Register/Login` $\to$ `CameraInitializing` $\to$ `DetectingExercise` $\to$ `ExerciseActive` $\to$ `ValidatingForm` $\to$ `RepCounted` $\to$ `SessionSaving`.
* **Sequence Diagram (Figure 18)**: End-to-end interactions across User, Mobile App, Pose Detector, Exercise Recognizer, Rep Counter, Posture Correction, Voice Companion, Firebase.

### 4.4. Maintenance Phase & Deployment
* **Deployment Diagram (Figure 19)**:
  - User Smartphone: Flutter App, MediaPipe, PoseConvo3D, AQMN, SQLite Local DB.
  - External APIs: Google Speech-to-Text, ElevenLabs TTS.
  - Cloud AI Server: LLaVA-1.5-7B (4-bit), Python Server.
  - Firebase Cloud & Trainer Browser.
