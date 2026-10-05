# BioMechAI — SRS Final Production Updates & Additions Manual
## Complete Step-by-Step Guide for Updating the SRS Word Document to the Final Semester 8 Production Baseline

- **Target Document**: `BioMechAI SRS -FYP-II Mid Evaluation Document.docx` (or your Google Docs working copy)  
- **Context**: This manual builds directly upon the previous manual (`27_2026-09-30_SRS_PartnerExactSearchAndReplaceManual.md`). Assuming all edits from that previous manual have already been applied, this document contains **every single new feature, security rule, and refined specification** developed since then.
- **Goal for Partner**: Give this file to your partner. She can simply press `Ctrl+F`, find the target location in Word, and paste the exact production-accurate text without breaking any formatting or document structure.

---

# 🚀 Quick Partner Checklist & Overview of New Additions

Tell your partner: *"We have added several production-certified features (Email Verification Security, Two-Way Coach Pairing, Smart Distance-Guiding Body Scanner, Plank Hold Timer, and Unread Feedback Badge). Use the table below to find each section and paste the new text."*

| Edit # | Target SRS Section | Fail-Safe Search (`Ctrl+F`) | Feature / Update Summary | Status |
| :---: | :--- | :--- | :--- | :---: |
| **New 1.1** | Section 1 (Document Purpose & Scope) | `final evaluation` or `Semester 8` | Clarify Final Graduation Baseline (FYP-II Final Defense) | [ ] |
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
| **New 6.1** | Section 4.1 (Use Case Tables - Table 19) | `Table 19:` | Update Use Case Table 19 with Coach Invitation Acceptance & Feedback Badge | [ ] |

---

# Part 1: Final Graduation Context (Semester 8 Defense)

### Edit New 1.1: Final Graduation Baseline Finality
* **Where in Word**: Section 1 (*Introduction*), under Document Purpose or Scope.
* **Fail-Safe Search (`Ctrl+F`)**: `mid-evaluation stage of FYP-II` or `Semester 8`
* **Text to Inspect / Update**:
  If the text says *"For the mid-evaluation stage of FYP-II..."*, replace it with the final graduation statement:
* **Replacement Text to Paste**:
  > This Software Requirements Specification (SRS) establishes the definitive, production-validated requirements for **BioMechAI** at the **FYP-II Final Graduation Defense (Semester 8)**. All nine (9) core modules have been fully implemented, hardened, and verified through both rigorous computational benchmarks and real-time physical athletic trials.
* **Why**: Ensures no outdated "planned for next semester" or "mid-evaluation" phrases remain in your final graduation document.

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

# Part 5: Section 4.1 — Use Case Table 19 Update

In **Section 4.1 (Use Case Tables)**, verify that **Table 19** includes the Two-Way Pairing and Notification Badge interactions:

### Edit New 6.1: Table 19 (Two-Way Coach Pairing & Notification Feedback Hub)
* **Where in Word**: Section 4.1, Table 19 (*UC-09: Coach Dashboard & Client Management*).
* **Fail-Safe Search (`Ctrl+F`)**: `Table 19:` or `UC-09`
* **Update the "Main Flow of Events" section in Table 19**:
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

## Final Quality Assurance Check for Partner

Before saving and submitting the Word document, have your partner perform these quick checks:
1. **Search for `Colab`**: Should return **0 results**.
2. **Search for `LLaVA`**: Should return **0 results**.
3. **Search for `SMPL`**: Should return **0 results**.
4. **Search for `AQMN`**: Should return **0 results**.
5. **Search for `60 different exercises`**: Should return **0 results** (Only **7 exercises**).
6. **Search for `30 workout sessions`** (for injury prediction): Should return **0 results** (Injury prediction runs on **every single rep**).
7. **Search for `eight modules`**: Should return **0 results** (Always **nine (9) modules**).
8. **Search for `50.90%` or `48.20%`**: Should return **0 results** (Active champion PoseC3D v5 is **53.38% Top-1 / 91.22% Top-5**).

---
*Created for BioMechAI FYP-II Final Graduation System Memory & SRS Word Synchronization.*
