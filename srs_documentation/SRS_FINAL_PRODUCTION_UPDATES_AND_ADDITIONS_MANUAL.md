# BioMechAI — SRS Final Production Updates & Additions Manual
## Complete Step-by-Step Guide for Updating the SRS Word Document for FYP-II Mid Evaluation (Semester 8)

- **Target Document**: `BioMechAI SRS -FYP-II Mid Evaluation Document.docx` (or your Google Docs working copy)  
- **Context**: This manual builds directly upon the previous manual (`27_2026-09-30_SRS_PartnerExactSearchAndReplaceManual.md`). Assuming all edits from that previous manual have already been applied, this document contains **every single new feature, security rule, table update, and diagram blueprint** developed since then.
- **Goal for Partner**: Give this file to your partner. She can simply press `Ctrl+F`, find each target location in Word, and paste the exact production-accurate text, tables, and diagram descriptions without breaking any formatting or document structure.

---

# 🚀 Quick Partner Checklist & Master Index

Tell your partner: *"We have added production-certified upgrades (Email Verification Security, Two-Way Coach Pairing, Smart Distance-Guiding Body Scanner, Plank Hold Timer, and Unread Feedback Badge). Use this checklist to update each section, table, and diagram."*

| Edit # | Target SRS Section | Fail-Safe Search (`Ctrl+F`) | Feature / Update Summary | Status |
| :---: | :--- | :--- | :--- | :---: |
| **New 1.1** | Section 1 (Document Purpose & Scope) | `mid-evaluation` or `Semester 8` | Clarify FYP-II Mid Evaluation Scope & System Maturity | [ ] |
| **New 2.1** | Section 2.3 (Objectives - Security) | `Secure multi-role authentication` | Add Mandatory Email Verification & Sign-In Gatekeeper | [ ] |
| **New 3.1** | Section 3.1 (System Features - Module 1) | `Module 1: User Registration` | Update Module 1 with Email Verification & Auto-Login Session Persistence | [ ] |
| **New 3.4** | Section 3.1 (System Features - Module 4) | `Module 4: Real-time Rep Counting` | Add Posture-Gated Isometric Plank Hold Timer & Continuous Scoring | [ ] |
| **New 3.6** | Section 3.1 (System Features - Module 6) | `Module 6: Body Measurement` | Add Smart Distance-Guiding Auto-Body Scanner & Cross-Platform PDF Export | [ ] |
| **New 3.7** | Section 3.1 (System Features - Module 7) | `Module 7: AI Clinical Injury` | Document Edge-Cloud Hybrid Fallback with Zero-Fail Offline Kinematics | [ ] |
| **New 3.9** | Section 3.1 (System Features - Module 9) | `Module 9: Trainer Dashboard` | Add Two-Way Coach Pairing, Bell Notification Badge & 1-Tap Deep Linking | [ ] |
| **New 4.1** | Section 3.2.1 (Functional Req - Module 1) | `3.2.1` or `User Registration and Login` | Add FR-1.4 (Email Verification Gatekeeper) & FR-1.5 (Session Persistence) | [ ] |
| **New 4.4** | Section 3.2.3 (Functional Req - Module 4) | `Closed 4-Stage Repetition` | Add FR-4.6 (Posture-Gated Isometric Plank Timer: 150°–195° standard) | [ ] |
| **New 4.6** | Section 3.2.5 (Functional Req - Module 6) | `Devine Ideal Body Weight` | Add FR-6.5 (Smart Distance Scanner 0.65–0.85 span) & FR-6.6 (PDF Export) | [ ] |
| **New 4.7** | Section 3.2.6 (Functional Req - Module 7) | `Dynamic Knee Valgus` | Add FR-7.5 (Edge-Cloud Hybrid Zero-Fail Offline Fallback Architecture) | [ ] |
| **New 4.9** | Section 3.2.8 (Functional Req - Module 9) | `Module 9` or `Trainer Dashboard` | Add FR-9.5 (Two-Way Pairing Sovereign Unlink) & FR-9.6 (Unread Badge Count) | [ ] |
| **New 5.1** | Section 3.3.1 (Performance Requirements) | `PoseC3D` or `latency` | Ensure Champion PoseC3D v5 Benchmark Accuracy (53.38% Top-1, 91.22% Top-5) | [ ] |
| **New 6.1** | Section 4.1 (Use Case Tables - Table 9) | `Table 9:` or `UC-01` | Update Table 9 with Email Verification Sign-In Gatekeeper Flow | [ ] |
| **New 6.4** | Section 4.1 (Use Case Tables - Table 12) | `Table 12:` or `UC-04` | Update Table 12 with Posture-Gated Isometric Plank Hold Timer Flow | [ ] |
| **New 6.6** | Section 4.1 (Use Case Tables - Table 14) | `Table 14:` or `UC-06` | Update Table 14 with Smart Camera Scanner & PDF Assessment Export | [ ] |
| **New 6.7** | Section 4.1 (Use Case Tables - Table 15) | `Table 15:` or `UC-07` | Update Table 15 with Clinical Injury Prevention & Hybrid Offline Fallback | [ ] |
| **New 6.9** | Section 4.1 (Use Case Tables - Table 19) | `Table 19:` or `UC-09` | Update Table 19 with Coach Pairing, Notification Badge & Deep Linking | [ ] |
| **New 7.1** | Section 4.2 (Diagram - Figure 14) | `Figure 14` | Update Sequence Diagram: Authentication & Email Verification Gatekeeper | [ ] |
| **New 7.2** | Section 4.3 (Diagram - Figure 17) | `Figure 17` | Update Activity Diagram: Dual-Branch Rep FSM vs Plank Hold Timer | [ ] |
| **New 7.3** | Section 4.4 (Diagram - Figure 19) | `Figure 19` | Update Deployment Diagram: 4-Node Mobile + Web Dashboard + GPU Backend | [ ] |

---

# Part 1: FYP-II Mid Evaluation Scope & System Maturity (Semester 8)

### Edit New 1.1: FYP-II Mid Evaluation Scope & Baseline Alignment
* **Where in Word**: Section 1 (*Introduction*), under Document Purpose or Scope.
* **Fail-Safe Search (`Ctrl+F`)**: `mid-evaluation stage of FYP-II` or `Semester 8`
* **Text to Inspect / Update**:
  Verify that the text formally frames the comprehensive implementation presented for the FYP-II Mid Evaluation:
* **Replacement Text to Paste**:
  > This Software Requirements Specification (SRS) establishes the definitive, production-validated requirements for **BioMechAI** presented at the **FYP-II Mid Evaluation (Semester 8)**. All nine (9) core modules have been fully implemented, integrated, and verified through empirical benchmarks and physical athletic trials.
* **Why**: Aligns the document precisely with the official **FYP-II Mid Evaluation milestone**, demonstrating that all 9 modules are actively working and verified.

---

# Part 2: Section 3.1 — Core System Features Updates

Navigate to **Section 3.1 (System Features)** in your Word document. Find each module bullet and update it with the new production capabilities:

### Edit New 3.1: Module 1 (Authentication, Security Gatekeeper & Session Persistence)
* **Where in Word**: Section 3.1, under `Module 1: User Registration and Login`.
* **Fail-Safe Search (`Ctrl+F`)**: `Module 1: User Registration and Login`
* **Current Text**:
  > • **Module 1: User Registration and Login**: Secure multi-role authentication (Athlete vs. Trainer) using Firebase Auth and Cloud Firestore profile persistence.
* **Replacement Text to Paste**:
  > • **Module 1: User Registration and Login (Security Gatekeeper & Persistent Session)**: Implements hardened role-based authentication partitioning Athletes and Certified Trainers across Mobile and Web (`biomechai-fitness`). Enforces a mandatory **Email Verification Security Gatekeeper** where registration triggers native email verification links and immediately terminates unverified sessions. Integrates an automatic **Session Persistence Engine** with a 3.0s background watchdog, allowing verified users to stay logged in across app restarts without retyping credentials.

---

### Edit New 3.4: Module 4 (Posture-Gated Isometric Plank Hold Timer)
* **Where in Word**: Section 3.1, under `Module 4: Real-time Rep Counting`.
* **Fail-Safe Search (`Ctrl+F`)**: `Module 4: Real-time Rep Counting`
* **Current Text**:
  > • **Module 4: Real-time Rep Counting and Form Validation**: Employs a deterministic Closed 4-Stage Repetition Finite State Machine (START $\to$ INFLECTION $\to$ PEAK $\to$ COMPLETION) with un-clamped joint flexion and camera boundary occlusion rejection ($\ge 35^\circ$).
* **Replacement Text to Paste**:
  > • **Module 4: Real-time Rep Counting & Isometric Hold Timer**: Employs a deterministic Closed 4-Stage Repetition Finite State Machine (START $\to$ INFLECTION $\to$ PEAK $\to$ COMPLETION) with camera boundary occlusion rejection ($\ge 35^\circ$) for dynamic exercises. For static holds (Plank), features a **Posture-Gated Isometric Hold Timer** adhering to the McGill (2010) clinical spine standard (150°–195° body line angle), automatically pausing the timer and illuminating a red skeleton on hip sag or pike, and calculating posture-weighted continuous scores ($Score = \frac{\text{validHoldTime}}{\text{totalTime}} \times 100$).

---

### Edit New 3.6: Module 6 (Smart Distance-Guiding Auto-Body Scanner & PDF Export)
* **Where in Word**: Section 3.1, under `Module 6: Body Measurement`.
* **Fail-Safe Search (`Ctrl+F`)**: `Module 6: Body Measurement`
* **Current Text**:
  > • **Module 6: Body Measurement and Transformation Tracking**: Tracks user anthropometric dimensions, computes live BMI with color-coded classification gauges, determines physiological target weight using the Devine formula, and persists historical progress to Firestore.
* **Replacement Text to Paste**:
  > • **Module 6: Smart Anthropometric Scanner & Assessment PDF Engine**: Monocular photogrammetry engine utilizing the user's entered stature as a calibration anchor ($scale = heightCm / bodyPx$). Integrates a **Smart Distance-Guiding Auto-Scanner** with real-time video stream processing at 30 FPS, dynamic color-coded framing cues (Red: $<0.55$ too far, $>0.92$ too close; Green: $0.65-0.85$ ideal zone), a 3-second hold countdown, and instant Euclidean joint span extraction (Shoulder Width, Hip Width, Torso Length, Arm Reach). Includes **Cross-Platform Assessment PDF Generation** providing branded clinical progress reports on mobile and web.

---

### Edit New 3.7: Module 7 (Clinical Injury Engine & Zero-Fail Hybrid Fallback)
* **Where in Word**: Section 3.1, under `Module 7: AI Clinical Injury Prevention`.
* **Fail-Safe Search (`Ctrl+F`)**: `Module 7: AI Clinical Injury Prevention`
* **Current Text**:
  > • **Module 7: AI Clinical Injury Prevention Engine**: Real-time full-body injury guard monitoring Munro Dynamic Knee Valgus FPPA ($< 165^\circ$ under load $\le 130^\circ$) for acute ACL protection, lumbar hip sag ($> 10\%$) for spinal shear protection, and elbow flare ($> 65^\circ$) for rotator cuff impingement.
* **Replacement Text to Paste**:
  > • **Module 7: AI Clinical Injury Prevention & Edge-Cloud Hybrid Fallback**: Real-time multi-joint clinical injury prevention engine covering all 7 exercises: Munro Dynamic Knee Valgus FPPA ($< 165.0^\circ$) for acute ACL risk (Squat/Lunge), lumbar hip sag ($> 10\%$ below line) for spinal compression (Push-Up/Plank), and elbow flare ($> 65.0^\circ$) for shoulder impingement (Push-Up). Backed by an **Edge-Cloud Zero-Fail Hybrid Fallback Shield**: if cloud connectivity drops, the local mobile kinematic engine instantly assumes full responsibility, turning the skeleton Crimson Red (`#F85149`) and firing priority-preempted audio safety warnings offline without frame drops.

---

### Edit New 3.9: Module 9 (Two-Way Pairing, Bell Badge & Direct Session Navigation)
* **Where in Word**: Section 3.1, under `Module 9: Trainer Dashboard`.
* **Fail-Safe Search (`Ctrl+F`)**: `Module 9: Trainer Dashboard`
* **Current Text**:
  > • **Module 9: Trainer Dashboard & Timestamped Feedback**: A comprehensive coaching portal within the Flutter ecosystem enabling certified trainers to inspect client rosters, review form scores, and leave second-by-second timestamped corrective notes.
* **Replacement Text to Paste**:
  > • **Module 9: Trainer Dashboard, Two-Way Pairing & Feedback Hub**: A unified multi-tenant coaching platform connecting the Flutter mobile app and React Web Portal (`biomechai-fitness`). Implements **Two-Way Sovereign Pairing** where coaches invite athletes by email, athletes accept/decline via in-app invitation cards, and either party can unlink at any time with multi-coach data isolation. Features an active **Unread Feedback Bell Badge** lighting up with unread counts (`1`, `2`) on the mobile home screen, paired with **1-Tap Direct Session Navigation** that deep-links directly from notifications into the exact workout session details screen.

---

# Part 3: Section 3.2 — Functional Requirements Detailed Additions

In **Section 3.2 (Specific Functional Requirements)**, add the following sub-bullets to their respective requirement blocks:

### Edit New 4.1: Additions to 3.2.1 (User Authentication & Security)
* **Where in Word**: Section 3.2.1, after the last existing bullet.
* **Fail-Safe Search (`Ctrl+F`)**: `3.2.1` or `User Registration and Login`
* **New Bullets to Add at the bottom of 3.2.1**:
  > • **FR-1.4 (Mandatory Email Verification Gatekeeper)**: The system shall enforce mandatory email verification upon account registration by automatically dispatching a native Google verification email, forcing session sign-out, and blocking login attempts until the link is verified.  
  > • **FR-1.5 (Automatic Session Persistence)**: The system shall maintain authenticated user sessions across mobile application terminations and restarts by asynchronously verifying local authentication state during the splash screen, utilizing a 3.0-second safety watchdog to prevent UI freezing under adverse network conditions.

---

### Edit New 4.4: Additions to 3.2.3 (Rep Counting & Plank Isometric Timer)
* **Where in Word**: Section 3.2.3, after the last existing bullet.
* **Fail-Safe Search (`Ctrl+F`)**: `3.2.3` or `Real-time Rep Counting`
* **New Bullets to Add at the bottom of 3.2.3**:
  > • **FR-4.6 (Posture-Gated Isometric Hold Timer)**: For static isometric exercises (Plank), the system shall track continuous hold duration, gating the active timer to valid spinal posture (body line angle between $150.0^\circ$ and $195.0^\circ$). The timer shall pause immediately when posture deviates into hip sag ($<150.0^\circ$) or hip pike ($>195.0^\circ$), and calculate final session scores weighted by valid hold percentage.  
  > • **FR-4.7 (Multi-Exercise Timeline Recording)**: The system shall record distinct exercise blocks chronologically within a single workout session, logging start times, end times, individual rep counts, hold durations, and separate form scores for post-workout timeline inspection.

---

### Edit New 4.6: Additions to 3.2.5 (Body Measurement & Scanner)
* **Where in Word**: Section 3.2.5, after the last existing bullet.
* **Fail-Safe Search (`Ctrl+F`)**: `3.2.5` or `Body Measurement Tracking`
* **New Bullets to Add at the bottom of 3.2.5**:
  > • **FR-6.5 (Smart Distance-Guiding Auto-Scanner)**: The system shall process live camera frames at 30 FPS to calculate vertical body span ($span = |y_{ankle} - y_{nose}| / H_{frame}$) and provide real-time color-coded framing cues (Red: $<0.55$ or $>0.92$; Green: $0.65-0.85$ ideal zone). Upon detecting 3.0 seconds of stable ideal framing, the system shall capture landmark coordinates with zero shutter lag.  
  > • **FR-6.6 (Euclidean Anthropometric Extraction)**: The system shall calculate real-world physical dimensions (Shoulder Width, Hip Width, Torso Length, and Arm Span) in centimeters using the user's calibrated height ratio ($scale = heightCm / bodyPx$).  
  > • **FR-6.7 (Cross-Platform Assessment PDF Export)**: The system shall generate comprehensive clinical fitness assessment reports in PDF format on both mobile (`PdfReportService`) and web (`jsPDF`), detailing anthropometric levers, vitals, BMI classification, and chronological workout metrics.

---

### Edit New 4.7: Additions to 3.2.6 (Clinical Injury Prevention)
* **Where in Word**: Section 3.2.6, after the last existing bullet.
* **Fail-Safe Search (`Ctrl+F`)**: `3.2.6` or `AI Injury Prediction`
* **New Bullets to Add at the bottom of 3.2.6**:
  > • **FR-7.5 (Edge-Cloud Hybrid Zero-Fail Fallback)**: The system shall maintain an edge-cloud hybrid kinematics pipeline. If the cloud inference server or network tunnel becomes unreachable, the on-device kinematic engine shall autonomously handle real-time form validation, illuminating the skeleton Crimson Red (`#F85149`) on detected faults and outputting local text-to-speech audio warnings without latency degradation.

---

### Edit New 4.9: Additions to 3.2.8 (Trainer Dashboard & Communication Hub)
* **Where in Word**: Section 3.2.8, after the last existing bullet.
* **Fail-Safe Search (`Ctrl+F`)**: `3.2.8` or `Trainer Dashboard`
* **New Bullets to Add at the bottom of 3.2.8**:
  > • **FR-9.5 (Two-Way Sovereign Coach-Athlete Pairing)**: The system shall enforce two-way pairing consent: coaches dispatch email invitations via the web dashboard, athletes receive interactive in-app invitation cards with [Accept] and [Decline] actions, and either party can disconnect at any time to preserve client autonomy and multi-tenant data isolation.  
  > • **FR-9.6 (Real-Time Unread Feedback Bell Badge & Deep Linking)**: The mobile application shall maintain an unread trainer feedback counter in local device storage, dynamically rendering a numeric badge (`1`, `2`) over the home screen notification bell icon upon receiving new coach feedback. Selecting a feedback item shall deep-link directly to that specific workout session's details screen with the highlighted coach feedback card.

---

# Part 4: Section 3.3 — Performance & Benchmark Accuracy Updates

### Edit New 5.1: PoseC3D Champion Model Benchmark Certification
* **Where in Word**: Section 3.3.1 (*Performance Requirements*) or Section 3.2.2.
* **Fail-Safe Search (`Ctrl+F`)**: `PoseC3D` or `91.22%`
* **Text to Inspect / Update**:
  Verify that the official benchmark accuracy for PoseC3D is stated as follows:
* **Replacement / Confirmation Text to Paste**:
  > The active production action recognition model is **PoseC3D v5 (SlowOnly ResNet-50 with 3D Spatiotemporal Connected Limb Heatmaps)** fine-tuned from FineGYM athletic weights. Evaluated under strict zero-leakage conditions on 115 held-out videos (444 clips), the champion model achieves:  
  > • **Top-1 Accuracy**: **53.38%** (237/444 clips)  
  > • **Top-5 Accuracy**: **91.22%** (405/444 clips)  
  > • **Macro Recall**: **53.15%** across all 7 exercise classes  
  > • **Per-Class Top-1 Accuracy**: Lunge 75.00%, Push-Up 67.35%, Plank 65.62%, Bicep Curl 61.64%, Squat 53.42%, High Knees 29.27%, Jumping Jack 19.74%.  
  > • **Inference Latency**: $\le 45\text{ms}$ on dedicated GPU backend server; on-device kinematics execute in $\le 15\text{ms}$ (30 FPS).
* **Why**: Establishes the exact scientific truth certified in the production benchmarks, eliminating any confusion with legacy experiments.

---

# Part 5: Section 4.1 — Use Case Tables Modernization

In **Section 4.1 (Use Case Tables)**, verify and update the following tables to reflect the newest flows:

### Edit New 6.1: Table 9 (UC-01: User Registration & Security Gatekeeper)
* **Where in Word**: Table 9 (`UC-01`).
* **Fail-Safe Search (`Ctrl+F`)**: `Table 9:` or `UC-01`
* **Update the Main Flow & Exceptions**:
  > **Main Flow**:
  > 1. User enters name, email, password, height, weight, age, and selects role (Athlete vs Trainer).
  > 2. System validates input formats and creates an authentication record in Firebase Auth.
  > 3. System automatically dispatches a verification link to the user's email inbox via `sendEmailVerification()`.
  > 4. System immediately terminates the unverified session and redirects to the Login screen with an alert: *"Verification email sent. Please verify before signing in."*
  > 5. User clicks the verification link in their email client.
  > 6. User enters credentials on the Login screen; System reloads user profile, verifies `emailVerified == true`, and grants access to the dashboard.
  >
  > **Exceptions**:
  > * **3a. User attempts login without verifying email**: System intercepts the attempt, denies login, terminates session, and displays an interactive *"Resend Verification Link"* button.
  > * **3b. Session persistence verification**: On application relaunch, system verifies cached token in background with a 3.0s watchdog, bypassing credentials input for verified users.

---

### Edit New 6.4: Table 12 (UC-04: Rep Counting & Isometric Hold Timer)
* **Where in Word**: Table 12 (`UC-04`).
* **Fail-Safe Search (`Ctrl+F`)**: `Table 12:` or `UC-04`
* **Update the Main Flow**:
  > **Main Flow**:
  > 1. Athlete enters camera frame; System locks active exercise (e.g. Squat or Plank).
  > 2. **For Dynamic Exercises**: Closed 4-Stage Rep FSM monitors primary joint angles. As athlete reaches peak depth (e.g., knee flexion $\le 115^\circ$) and ascends fully ($\ge 146^\circ$), valid rep count increments by +1.
  > 3. **For Isometric Plank**: Posture-Gated Hold Timer monitors body line angle ($150^\circ - 195^\circ$). As long as alignment is straight, timer ticks continuously second-by-second.
  > 4. **Exception (Plank Sag / Pike)**: If athlete's hips sag below $150^\circ$ or pike above $195^\circ$, skeleton turns Crimson Red and the timer immediately pauses until posture is corrected.
  > 5. System writes exercise timeline blocks to memory upon exercise transition or session completion.

---

### Edit New 6.6: Table 14 (UC-06: Smart Camera Body Scanner & PDF Export)
* **Where in Word**: Table 14 (`UC-06`).
* **Fail-Safe Search (`Ctrl+F`)**: `Table 14:` or `UC-06`
* **Update the Main Flow**:
  > **Main Flow**:
  > 1. Athlete navigates to Body Measurement screen and selects the Camera Scanner tab.
  > 2. Athlete stands in front of camera; live video stream tracks vertical body span fraction ($span = |y_{ankle} - y_{nose}| / H$).
  > 3. Viewfinder HUD provides dynamic color-coded guidance: Red if too close ($>0.92$) or too far ($<0.55$), Yellow if near, and Green when within ideal framing ($0.65 - 0.85$).
  > 4. Once stable in the green zone, a 3-second hold countdown initiates.
  > 5. Upon countdown completion, the system instantly captures live landmarks (`_latestPose`) without shutter lag.
  > 6. Euclidean anthropometric engine calculates Shoulder Width, Hip Width, Torso Length, and Arm Span in centimeters calibrated by user stature.
  > 7. User taps "Export Assessment PDF" to generate a clinical PDF report via `PdfReportService`.

---

### Edit New 6.7: Table 15 (UC-07: Clinical Injury Prevention & Hybrid Fallback)
* **Where in Word**: Table 15 (`UC-07`).
* **Fail-Safe Search (`Ctrl+F`)**: `Table 15:` or `UC-07`
* **Update the Main Flow & Edge-Cloud Hybrid Failover**:
  > **Main Flow**:
  > 1. Kinematics engine continuously inspects live 3D joint landmarks across every single rep.
  > 2. Evaluates specific clinical rules: Munro Dynamic Knee Valgus ($<165^\circ$) for Squats/Lunges, Lumbar Hip Sag ($>10\%$) for Push-Ups/Planks, and Elbow Flare ($>65^\circ$) for Push-Ups.
  > 3. If an injury threshold is breached: Skeleton turns Crimson Red (`#F85149`), a red alert card appears, and priority-preempted audio safety cue is spoken aloud.
  > 4. **Edge-Cloud Hybrid Failover (Zero-Fail Guarantee)**: If network connectivity or cloud backend is disconnected, the local on-device `FormValidationService` seamlessly assumes 100% of injury evaluation and rep counting with zero frame drops or latency spikes.

---

### Edit New 6.9: Table 19 (UC-09: Coach Web Portal, Two-Way Pairing & Notification Hub)
* **Where in Word**: Table 19 (`UC-09`).
* **Fail-Safe Search (`Ctrl+F`)**: `Table 19:` or `UC-09`
* **Update the Main Flow**:
  > **Main Flow**:  
  > 1. Trainer logs into the Web Dashboard (`https://biomechai-fitness.web.app`) and navigates to the Client Management page.  
  > 2. Trainer enters an athlete's registered email to send a coaching invitation.  
  > 3. The athlete receives a real-time invitation card on their mobile home screen and profile screen with [Accept] and [Decline] options.  
  > 4. Upon athlete acceptance, bidirectional pairing is established in Firestore (`users/{uid}/trainerId`), granting the coach read-access to the athlete's workout telemetry.  
  > 5. Trainer inspects the athlete's chronological area charts, monthly calendar dots, and rep-by-rep fault logs.  
  > 6. Trainer enters clinical corrective feedback for a workout session and submits it.  
  > 7. The athlete's mobile application detects the new feedback, increments the unread count badge (`1`) on the home notification bell, and displays a push notification.  
  > 8. The athlete taps the bell icon, views the feedback card, and taps it to deep-link directly into the full Session Details screen.  
  > 9. The athlete or trainer can download the complete Assessment PDF report at any time.

---

# Part 6: Master Diagram Modernization Blueprints

Use these visual blueprints if updating your diagram images or Word drawings:

---

### Blueprint 1: Figure 14 — Sequence Diagram (Authentication & Security Gatekeeper)
* **Where in Word**: Figure 14 (or your Authentication Sequence Diagram).
* **Exact Flow to Represent**:

```
Athlete / Trainer            Mobile / Web App              Firebase Auth              Cloud Firestore
      |                             |                            |                            |
      |--- 1. Submit Registration ->|                            |                            |
      |    (email, password, role)  |--- 2. createUserWithEmail->|                            |
      |                             |<-- 3. Returns User Cred ---|                            |
      |                             |--- 4. sendEmailVerification---------------------------->|
      |                             |--- 5. Force signOut() ---->|                            |
      |<-- 6. Show "Verify Email" --|                            |                            |
      |                             |                            |                            |
      |=== 7. User Clicks Verification Link in Email Inbox ===================================|
      |                             |                            |                            |
      |--- 8. Submit Login -------->|                            |                            |
      |                             |--- 9. signInWithPassword ->|                            |
      |                             |--- 10. user.reload() ----->|                            |
      |                             |<-- 11. emailVerified: true |                            |
      |                             |--- 12. getUserData(uid) ------------------------------->|
      |                             |<-- 13. Return Profile Data -----------------------------|
      |<-- 14. Access Granted ------|
```

---

### Blueprint 2: Figure 17 — Activity Diagram (Dual-Branch Workout State Machine)
* **Where in Word**: Figure 17 (Workout State Machine Activity Diagram).
* **Exact Logic to Represent**:

```
                             [ User Enters Frame ]
                                       │
                                       ▼
                         [ Exercise Locked / Auto-Detected ]
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        [ Dynamic Repetition Mode ]               [ Isometric Plank Mode ]
       (Squat, Push-Up, Lunge, etc.)                      │
                    │                                     ▼
                    ▼                          [ Check Body Line Angle θ ]
           ┌─────────────────┐                 (McGill Standard: 150°–195°)
           │  START (θ≥146°) │                            │
           └────────┬────────┘                   ┌────────┴────────┐
                    │ Descent                    ▼                 ▼
                    ▼                       [ θ in Range ]   [ θ out of Range ]
         ┌─────────────────────┐             (150°–195°)      (<150° or >195°)
         │ INFLECTION (θ<146°) │                 │                 │
         └──────────┬──────────┘                 ▼                 ▼
                    │ Valid Depth            [ Green Skeleton ] [ Red Skeleton ]
                    ▼                        [ Timer Ticking  ] [ Timer Paused ]
           ┌─────────────────┐               [ Audio: Praise  ] [ Audio: Alert ]
           │  PEAK (θ≤115°)  │                   │                 │
           └────────┬────────┘                   └────────┬────────┘
                    │ Full Ascent                         ▼
                    ▼                           [ End Hold Session ]
           ┌─────────────────┐                            │
           │   COMPLETION    │                            ▼
           │  [RepCount++]   │                   [ Posture-Weighted ]
           └─────────────────┘                   [ Continuous Score ]
```

---

### Blueprint 3: Figure 19 — Deployment Diagram (Accurate 4-Node Architecture)
* **Where in Word**: Figure 19 (Deployment Diagram, Word Page 33 / PDF Page 39).
* **Exact Node-by-Node Layout**:

```
+-----------------------------------------------------------------------------------------------+
|                                BioMechAI SRS — Figure 19: Deployment Diagram                  |
+-----------------------------------------------------------------------------------------------+

+-----------------------------------------+                 +-----------------------------------------+
|     Node: Athlete Smartphone            |                 |     Node: Trainer Workstation           |
|         (Android / iOS)                 |                 |     (Chrome / Safari / Edge Browser)    |
|-----------------------------------------|                 |-----------------------------------------|
| <<artifact>> BioMechAI.apk (v3.1)       |                 | <<artifact>> React + Vite Web Portal    |
| <<artifact>> Google ML Kit BlazePose    |                 | <<artifact>> Tailwind + Recharts UI     |
| <<artifact>> Closed 4-Stage Rep FSM     |                 | <<artifact>> jsPDF Assessment Engine    |
| <<artifact>> Plank Hold Timer           |                 | <<artifact>> Firebase Web SDK           |
| <<artifact>> flutter_tts Audio Engine   |                 +--------------------+--------------------+
| <<artifact>> Smart Distance Scanner     |                                      |
| <<artifact>> Firestore Client SDK       |                                      | HTTPS
+--------------------+--------------------+                                      |
                     |                                                           |
                     | HTTPS / WSS (Cloud Tunnel)                                |
                     v                                                           |
+-----------------------------------------+                                      |
|       Node: Cloud AI Server             |                                      |
|     (GPU / FastAPI / Ubuntu 22.04)      |                                      |
|-----------------------------------------|                                      |
| <<artifact>> FastAPI PyTorch App        |                                      |
| <<artifact>> PoseC3D v5 Limb Model      |                                      |
|              (best_acc_top1_epoch_10)   |                                      |
| <<artifact>> ngrok Permanent Tunnel     |                                      |
|   (persevere-kindred-tasty.ngrok-free)  |                                      |
+--------------------+--------------------+                                      |
                     |                                                           |
                     | Cloud Telemetry                                           |
                     v                                                           v
+-----------------------------------------------------------------------------------------------+
|                               Node: Google Firebase Cloud (`biomechai-fitness`)               |
|-----------------------------------------------------------------------------------------------|
| <<artifact>> Firebase Authentication (Mandatory Email Verification & Role Gatekeeper)         |
| <<artifact>> Cloud Firestore Database (Real-Time Workouts, Two-Way Pairing, Feedback)        |
| <<artifact>> Firebase Hosting (Web Portal: `https://biomechai-fitness.web.app`)               |
+-----------------------------------------------------------------------------------------------+
```

---

### Blueprint 4: Smart Camera Body Scanner State Machine Diagram
* **Where to Include**: Section 3.2.5 (or Module 6 documentation).

```
[ Idle / Tab Opened ]
         │
         ▼
[ Camera Active ] ──► Continuous 30 FPS Stream
         │            Tracks: Span = |y_ankle - y_nose| / H_frame
         ▼
[ Real-Time Framing Check ]
         ├── If Span < 0.55 (Red) ──► CUE: "Move closer - too far away!"
         ├── If Span > 0.92 (Red) ──► CUE: "Step back - too close!"
         ├── If 0.55–0.65 or 0.85–0.92 (Yellow) ──► CUE: "Adjust slightly..."
         └── If 0.65–0.85 (Green) ──► CUE: "Perfect! Hold still."
                                           │
                                           ▼
                                 [ 3-Second Hold Countdown ]
                                 (3... 2... 1...)
                                           │
                                           ▼
                                 [ Zero-Lag Live Capture ]
                                 (Read Verified Landmark Buffer)
                                           │
                                           ▼
                                 [ Anthropometric Engine ]
                                 (Shoulder, Hip, Torso, Arm reach in cm)
                                           │
                                           ▼
                                 [ Save to Firestore & Export PDF ]
```

---

# Part 7: Final 8-Point Quality Assurance Check for Partner

Before saving and submitting the Word document, have your partner perform these quick `Ctrl+F` checks:

1. **Search for `Colab`**: Should return **0 results**.
2. **Search for `LLaVA`**: Should return **0 results**.
3. **Search for `SMPL`**: Should return **0 results**.
4. **Search for `AQMN`**: Should return **0 results**.
5. **Search for `60 different exercises`**: Should return **0 results** (Only **7 exercises**).
6. **Search for `30 workout sessions`** (for injury prediction): Should return **0 results** (Injury prediction runs on **every single rep**).
7. **Search for `eight modules`**: Should return **0 results** (Always **nine (9) modules**).
8. **Search for `50.90%` or `48.20%`**: Should return **0 results** (Active champion PoseC3D v5 is **53.38% Top-1 / 91.22% Top-5**).

---
*Created for BioMechAI FYP-II Mid Evaluation System Memory & SRS Word Synchronization.*
