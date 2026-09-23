# BioMechAI — The Complete 9-Module Master Guide: Plain-English Concept Explanations, Parameter Deep Dive & Exact Research Links

> **Document Purpose**:  
> This guide explains the entire BioMechAI system in **child-simple English**.  
> Every technical concept strictly follows the requested teaching format:  
> **`[Concept Name] (Which actually means: "..."): "And this helped us in our project by doing ..."`**  
> It covers all **9 Official FYP-II Modules**, provides an **exhaustive parameter-by-parameter breakdown of the PoseC3D AI model**, explains **why** every value was chosen, why other values were rejected, and provides **direct, clickable links to every research paper, code file, and pretrained model download**.

---

# Table of Contents
1. [Master Dictionary: Everyday Translations of Technical Words](#1-master-dictionary-everyday-translations-of-technical-words)
2. [Master Architecture: How Phone & Server Work Together](#2-master-architecture-how-phone--server-work-together)
3. [Module 1: User Registration, Login & Role Separation](#3-module-1-user-registration-login--role-separation)
4. [Module 2: Real-Time 3D On-Device Body Pose Tracking](#4-module-2-real-time-3d-on-device-body-pose-tracking)
5. [Module 3: Exercise Classification (PoseC3D Deep Learning Engine)](#5-module-3-exercise-classification-posec3d-deep-learning-engine)
6. [Deep Dive into Module 3: Complete Model Parameter Bible](#6-deep-dive-into-module-3-complete-model-parameter-bible)
7. [Module 4: Real-Time Repetition Counting (4-Stage State Machine)](#7-module-4-real-time-repetition-counting-4-stage-state-machine)
8. [Module 5: Posture Correctness & Form Checking (All 7 Exercises)](#8-module-5-posture-correctness--form-checking-all-7-exercises)
9. [Module 6: Body Measurement & Transformation Tracking](#9-module-6-body-measurement--transformation-tracking)
10. [Module 7: AI Clinical Injury Prevention & Knee Valgus (ACL Risk) Engine](#10-module-7-ai-clinical-injury-prevention--knee-valgus-acl-risk-engine)
11. [Module 8: AI Workout Companion with Live Voice Coaching](#11-module-8-ai-workout-companion-with-live-voice-coaching)
12. [Module 9: Trainer Dashboard & Timestamped Feedback](#12-module-9-trainer-dashboard--timestamped-feedback)
13. [Master Research Bibliography: Exact Clickable Paper & Weight Links](#13-master-research-bibliography-exact-clickable-paper--weight-links)

---

# 1. Master Dictionary: Everyday Translations of Technical Words

Read this section first! Whenever you see an unfamiliar word, look up its plain English meaning here:

* **Landmarks / Keypoints** (Which actually means: 33 digital dots placed on human joints like nose, elbows, knees, and ankles): "And this helped us in our project by allowing the computer to track how the human body moves without needing to process heavy, private video images."
* **MediaPipe / Google ML Kit** (Which actually means: Free, ultra-fast software made by Google that runs directly inside mobile phones to find those 33 joint dots 30 times a second): "And this helped us in our project by giving our phone app real-time body tracking with zero internet lag (<15 ms) and 100% user privacy."
* **COCO-17** (Which actually means: A world-standard list of exactly 17 main athletic body joints): "And this helped us in our project by stripping away useless facial dots (lips, eyelids) so our AI only concentrates on the major joints that matter for gym exercises."
* **PoseC3D** (Which actually means: A 2022 computer vision neural network developed by Hong Kong researchers that recognizes human exercises by turning skeleton dots into 3D heat movies): "And this helped us in our project by replacing old fragile skeleton graph models with smooth 3D convolutions that don't crash when a user's joint is hidden."
* **Limb Heatmaps** (Which actually means: Drawing solid, glowing neon bone tubes between joints instead of just isolated dots): "And this helped us in our project by letting the AI see that both thigh bones move parallel in a Squat while one moves forward and one back in a Lunge, cutting Squat-vs-Lunge confusion by 65.9%!"
* **Pretrained Weights** (Which actually means: Mathematical numbers inside an AI brain that was already trained on 56,000+ athletic videos by OpenMMLab scientists on giant supercomputers): "And this helped us in our project by giving our model existing knowledge of human movement so we didn't have to train from scratch."
* **Fine-Tuning / Transfer Learning** (Which actually means: Taking that already-trained athlete AI brain and teaching it our 7 specific gym workouts): "And this helped us in our project by fulfilling the university panel's explicit mandate to fine-tune a pretrained model."
* **FineGYM** (Which actually means: A massive academic video dataset of Olympic gymnastics routines like vaults, balance beams, and floor flips): "And this helped us in our project because gymnastics routines share identical athletic limb speeds and deep knee bends with gym workouts, giving us a +3.5 pp boost over generic YouTube models."
* **Parameters** (Which actually means: The internal mathematical knobs and dials inside the neural network that adjust during learning): "And this helped us in our project by storing the exact patterns that tell a Squat apart from a Push-Up."
* **Epoch** (Which actually means: One complete round where the AI studies every single training video in our dataset once): "And this helped us in our project by measuring training progress across 18 rounds, peaking at Round 10."
* **Top-1 vs. Top-5 Accuracy** (Which actually means: Top-1 is when the AI's single #1 guess is right; Top-5 is when the correct exercise is within its top 5 guesses): "And this helped us in our project by proving our model achieves 53.38% Top-1 accuracy and 91.22% Top-5 accuracy on completely unseen test videos."
* **Finite State Machine (FSM)** (Which actually means: A strict step-by-step counter rule that only gives you a rep when you descend all the way down and stand all the way up): "And this helped us in our project by preventing false rep counting if an athlete shakes, pauses, or does half-reps."
* **Munro FPPA ($< 165^\circ$)** (Which actually means: Frontal Plane Projection Angle, a medical angle that checks if your knees cave inward toward each other during squats): "And this helped us in our project by giving us a scale-invariant clinical rule to warn users before they tear their ACL knee ligament."

---

# 2. Master Architecture: How Phone & Server Work Together

BioMechAI uses a **Dual-Timescale Architecture**:
* **Fast Loop (On Mobile Phone, 30 times a second)**: Real-time body tracking, rep counting, knee valgus warning, and voice coaching.
* **Slow Loop (On Python Server, every 2 to 3 seconds)**: Buffers 48 frames of movement and runs the heavy PoseC3D AI model to classify the exercise.

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                              MOBILE PHONE (FLUTTER APP)                                │
 │                                                                                        │
 │  1. Phone Camera records live video (30 frames every second)                           │
 │                         │                                                              │
 │                         ▼                                                              │
 │  2. MediaPipe (Which actually means: Google's on-device joint locator)                 │
 │     "And this helped us by extracting 33 body dots in <15ms without sending video"     │
 │                         │                                                              │
 │        ┌────────────────┴─────────────────────────────────────────┐                    │
 │        │ Fast Loop (Evaluates live on the phone at 30 Hz)         │                    │
 │        ▼                                                          ▼                    │
 │  [Module 4] 4-Stage Rep Counter             [Module 8] Native Voice Coach              │
 │  [Module 5] Joint Angle Checker             ("Push knees out!", "Rep 5!")              │
 │  [Module 7] Munro FPPA Valgus Watchdog                    ▲                            │
 │        │                                                  │ High-Priority Safety Cues  │
 │        └────────────────┬─────────────────────────────────┘                            │
 └─────────────────────────┼──────────────────────────────────────────────────────────────┘
                           │
                           │ Sends joint dots (NOT heavy video!) over local Wi-Fi
                           │ via WebSocket (/ws/stream) or HTTP POST (/classify)
                           ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                          AI SERVER (PYTHON / FASTAPI / PYTORCH)                        │
 │                                                                                        │
 │  1. Strips down to 17 joints (COCO-17, which actually means: standard 17 body bones)   │
 │     "And this helped us by dropping facial fluff and matching the PoseC3D layout"      │
 │                         │                                                              │
 │                         ▼                                                              │
 │  2. [Module 3] 3D Spatiotemporal Limb Heatmaps (glowing bone tubes across time)        │
 │     "And this helped us by making parallel squat thighs visible to 3D convolutions"    │
 │                         │                                                              │
 │                         ▼                                                              │
 │  3. PoseC3D 3D-CNN Model (Loaded with FineGYM Pretrained Weights)                      │
 │     "And this helped us by predicting the exercise class in <45 ms with 91.2% Top-5"   │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. Module 1: User Registration, Login & Role Separation

### What It Actually Means:
A secure door where athletes and trainers create accounts with passwords, and the app decides what screen to show them based on who they are.

### Step-by-Step Flow (Using the In-Line Teaching Format):
1. **User opens app**: The app inspects active credentials using `AuthProvider`.
2. **Authentication (Firebase Auth, which actually means: Google's encrypted identity vault)**: "And this helped us in our project by protecting user passwords with industry-standard bcrypt encryption so our system is immune to credential leaks or SQL injection."
3. **Database Profile Fetch (Cloud Firestore, which actually means: Google's real-time cloud database)**: "And this helped us in our project by loading the user's saved height, weight, and role in milliseconds."
4. **Role Routing (Role Separation, which actually means: splitting users into Athletes vs. Trainers)**: "And this helped us in our project by ensuring an athlete only sees their own private body records, while a trainer gets a coaching directory to inspect multiple clients."

### Where It Lives in the Code:
* Auth Provider: [`biomechai_flutter_latest/lib/providers/auth_provider.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/providers/auth_provider.dart)
* Login Screen: [`biomechai_flutter_latest/lib/screens/login_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/login_screen.dart)
* Register Screen: [`biomechai_flutter_latest/lib/screens/register_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/register_screen.dart)

### The "WHY" Section:
* **Why Firebase Authentication instead of writing custom PHP/Node.js login code?**  
  * *Why We Did It*: Firebase Auth is maintained by Google security engineers, handles automated session tokens, and integrates directly with Firestore security rules.
  * *Why NOT the Alternative*: Writing custom login code from scratch introduces vulnerabilities like SQL injection, plain-text password risks, and requires hosting an extra authentication server.
* **Why enforce Role Separation at the database level?**  
  * *Why We Did It*: It guarantees that athletes cannot accidentally view other athletes' body transformation photos or weight metrics.

---

# 4. Module 2: Real-Time 3D On-Device Body Pose Tracking

### What It Actually Means:
Using your smartphone camera to find 33 joint dots on your body 30 times every second without sending any video over the internet.

### Step-by-Step Flow (Using the In-Line Teaching Format):
1. **Camera Frame Streaming (CameraImage, which actually means: grabbing 30 photos a second from the camera sensor)**: "And this helped us in our project by providing a continuous stream of motion frames to analyze."
2. **On-Device Inference (Google ML Kit BlazePose, which actually means: Google's tiny neural network that runs right inside the phone chip)**: "And this helped us in our project by finding all body joints in under 15 milliseconds without needing an internet connection."
3. **3D Keypoint Extraction ($(x, y, z)$ Coordinates, which actually means: measuring joint position left/right, up/down, and depth from camera)**: "And this helped us in our project by giving us 3D spatial depth so we can measure whether someone is leaning forward or backward."
4. **Live Visual Skeleton (SkeletonPainter, which actually means: drawing green and red neon bones over the user's camera preview)**: "And this helped us in our project by giving the user live visual confirmation that their body is fully visible and safe."

### Where It Lives in the Code:
* Detection Service: [`biomechai_flutter_latest/lib/services/pose_detection_service.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/services/pose_detection_service.dart)
* Visual Skeleton: [`biomechai_flutter_latest/lib/widgets/skeleton_painter.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/widgets/skeleton_painter.dart)
* Research Citation: [BlazePose: On-device Real-time Body Pose Tracking (CVPR 2020)](https://arxiv.org/abs/2006.10204)

### The "WHY" Section:
* **Why run pose estimation directly on the mobile phone instead of sending video to a cloud server?**  
  * *Why We Did It*: Streaming 1080p video over Wi-Fi adds 200–350 ms of lag. A knee ligament (ACL) tears in **under 100 milliseconds**! Running pose estimation directly on the phone chip takes **12 milliseconds**, letting the app warn you instantly.
  * *Why NOT the Alternative*: Sending live video over the internet creates major privacy risks for users exercising at home and requires massive internet bandwidth (6,000 Kbps for video vs. 18 Kbps for coordinates).

---

# 5. Module 3: Exercise Classification (PoseC3D Deep Learning Engine)

### What It Actually Means:
The AI brain that watches 3 seconds of skeleton movement and tells you: *"You are performing a Squat"* (out of 7 exercises: `Squat`, `Push-Up`, `Lunge`, `Bicep Curl`, `Plank`, `Jumping Jack`, `High Knees`).

### Step-by-Step Flow (Using the In-Line Teaching Format):
1. **Temporal Buffering (Buffering 48 Frames, which actually means: storing about 2 to 3 seconds of joint coordinates in memory)**: "And this helped us in our project by capturing exactly one full exercise repetition cycle so the AI can see the full rhythm of the workout."
2. **COCO-17 Mapping (Strips down to 17 joints, which actually means: dropping facial fluff like eyes, ears, and mouth)**: "And this helped us in our project by keeping only the 17 main athletic body joints (shoulders, elbows, wrists, hips, knees, ankles) which cut down computing time and matched the exact 17-channel layout expected by the pretrained model."
3. **Limb Heatmap Rasterization (Connecting bones with Gaussian tubes, which actually means: drawing solid glowing neon bones instead of isolated dots)**: "And this helped us in our project by letting the AI see that both thigh bones descend symmetrically in a Squat while one moves forward and one back in a Lunge, which **more than doubled squat recall from 20.5% to 53.4%** and cut squat-to-lunge errors by **65.9%**!"
4. **3D Convolutional Forward Pass (3D-CNN, which actually means: sliding mathematical filters across video height, width, and time simultaneously)**: "And this helped us in our project by naturally smoothing out camera coordinate jitter while extracting the speed and acceleration of the limbs."
5. **Global Average Pooling (GAP, which actually means: shrinking the 3D video volume down to a single list of 512 numbers)**: "And this helped us in our project by compressing the essential movement summary into a compact 512-dimensional vector."
6. **Classification Head (`Linear(512, 7)`, which actually means: a final decision formula that converts 512 numbers into 7 exercise scores)**: "And this helped us in our project by outputting the exact percentage confidence for each of our 7 workouts."

### Where It Lives in the Code:
* Active Champion Checkpoint: [`models/posec3d_v5_limb/best_acc_top1_epoch_10.pth`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/best_acc_top1_epoch_10.pth)
* Model Architecture Config: [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py)
* Backend Bridge Engine: [`backend/engine.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/engine.py)
* Research Citation: [PoseC3D CVPR 2022 Official Paper PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Duan_Revisiting_Skeleton-Based_Action_Recognition_CVPR_2022_paper.pdf) | [arXiv:2104.13586](https://arxiv.org/abs/2104.13586)

---

# 6. Deep Dive into Module 3: Complete Model Parameter Bible

This section explains **every single parameter** in our champion model config [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py):

### 6.1 Total Parameter Count & Pretrained Breakdown
* **Total Parameters in the Model**: Exactly **`2,109,831`** floating-point numbers.
* **How many were Pretrained?**: Exactly **`2,106,240`** parameters in the SlowOnly ResNet-50 backbone were loaded directly from OpenMMLab's official FineGYM limb checkpoint (`gym-limb_20220815-2e6e3c5c.pth`).
* **How many were Re-Initialized?**: Exactly **`3,591`** parameters in the final linear classification head (`cls_head.fc_cls`).
  * Math: $512\text{ inputs} \times 7\text{ classes} + 7\text{ bias numbers} = \mathbf{3,591}$.
  * Why re-initialized? Because OpenMMLab's FineGYM checkpoint was trained to classify Olympic gymnastics events (vault, bars, beam). We re-initialized this final layer to classify our **7 BioMechAI gym workouts**!

---

### 6.2 Line-by-Line Parameter Explanation from the Code File

#### 1. `load_from` (Line 4 in `posec3d_biomechai_v5_limb.py`)
```python
load_from = 'https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_gym-limb/slowonly_r50_8xb16-u48-240e_gym-limb_20220815-2e6e3c5c.pth'
```
* **What it means in plain English**: The exact internet link where the code downloads the pretrained FineGYM limb weights from OpenMMLab.
* **Why we used it**: Fulfilled the panel's mandate to use a pretrained model. It loaded 2.1 million already-smart movement filters into our network.
* **Direct Download Link**: [Download `gym-limb_20220815-2e6e3c5c.pth`](https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_gym-limb/slowonly_r50_8xb16-u48-240e_gym-limb_20220815-2e6e3c5c.pth)

#### 2. `depth = 50` (Line 12)
* **What it means in plain English**: How many neural network layers are stacked on top of each other (ResNet-50 architecture).
* **Why we chose 50**: ResNet-50 is the gold standard in computer vision. It is deep enough to learn complex athletic movement patterns without running out of GPU memory.
* **Why NOT other values?**: ResNet-18 is too shallow and fails to learn subtle differences between a squat and a lunge. ResNet-101 has double the parameters and causes severe overfitting on small datasets.

#### 3. `in_channels = 17` (Line 14)
* **What it means in plain English**: The model expects an input with 17 separate channels (one for each COCO body bone/joint).
* **Why we chose 17**: Matches the 17 standard COCO athletic joints.
* **Why NOT other values?**: A color photo has 3 channels (Red, Green, Blue). MediaPipe has 33 points. Passing 33 channels would include useless face dots (lips, eyelids) and waste memory.

#### 4. `base_channels = 32` (Line 15)
* **What it means in plain English**: How many convolutional filters start scanning the skeleton heatmap in the first layer.
* **Why we chose 32**: Keeps the model lightweight (~8.3 MB) and fast for phone servers.
* **Why NOT 64?**: Standard RGB image models use 64 channels, producing massive 100+ MB model files. Skeleton heatmaps are clean lines, so 32 channels capture all necessary motion features.

#### 5. `num_stages = 3` and `stage_blocks = (4, 6, 3)` (Lines 16, 18)
* **What it means in plain English**: The 3D-CNN is divided into 3 major processing stages. Stage 1 has 4 residual blocks, Stage 2 has 6 blocks, and Stage 3 has 3 blocks (total = 13 residual blocks = 50 convolutional layers).
* **Why we used it**: Matches the official PoseC3D SlowOnly design proven by OpenMMLab.

#### 6. `inflate = (0, 1, 1)` (Line 21)
* **What it means in plain English**: "Inflating" means turning a 2D image filter into a 3D time-scanning video filter. `(0, 1, 1)` means Stage 1 scans space only (2D), while Stages 2 and 3 scan across **both space and time (3D)**.
* **Why we used it**: Doing 3D convolutions in early layers wastes GPU compute on raw lines. Inflating only the later stages allows the network to learn spatial limb shapes first, and then learn their temporal speed and rhythm.

#### 7. `dropout_ratio = 0.6` (Line 29)
* **What it means in plain English**: During training, the computer randomly switches off **60% of the neurons** on every step.
* **Why we chose 0.6**: It forces the remaining 40% of neurons to learn independently, preventing the AI from memorizing training videos (overfitting).
* **Why NOT other values?**: 
  * In PoseC3D v1, we tried `0.50` -> The model overfitted on limb heatmaps.
  * In PoseC3D v2, we tried `0.70` -> Too aggressive! It starved the network and Push-Up accuracy collapsed from 63% to 28%.
  * `0.60` proved to be the exact optimal balance.

#### 8. `lr = 0.01` and `momentum = 0.9` (Line 103)
* **What it means in plain English**:
  * `lr = 0.01` (Learning Rate): How big of a mathematical step the AI takes when correcting its mistakes.
  * `momentum = 0.9`: Like a heavy bowling ball rolling downhill; it keeps moving in the right direction even if the ground has small bumps.
* **Why we chose 0.01 with SGD Momentum**: Determined using the scientific linear scaling rule ($\eta = 0.1 \times \text{batch}/128 = 0.1 \times 16/128 \approx 0.01$). Momentum SGD discovers broader, flatter, and more robust solutions on 3D convolution surfaces than Adam.
* **Why NOT `lr = 0.1`?**: A learning rate of 0.1 is too high and would cause "catastrophic forgetting", destroying the FineGYM pretrained weights!

#### 9. `weight_decay = 0.0005` (Line 103)
* **What it means in plain English**: A small mathematical penalty ($5 \times 10^{-4}$) added to the loss function that prevents any single parameter from growing too large.
* **Why we used it**: Prevents the model from becoming overly sensitive to tiny camera jitters.

#### 10. `clip_grad = dict(max_norm=40, norm_type=2)` (Line 104)
* **What it means in plain English**: If a sudden mathematical error creates a giant gradient update larger than 40, the system automatically clips it down to 40.
* **Why we used it**: Acts as an essential safety fuse during early training epochs so the newly initialized 7-class head doesn't blow up the network.

#### 11. `batch_size = 16` (Line 71)
* **What it means in plain English**: The GPU looks at 16 video clips at the exact same moment before updating its internal math.
* **Why we chose 16**: Completely fills the 16 GB VRAM of the Nvidia Tesla T4 GPU on Kaggle without triggering an Out-Of-Memory (OOM) crash.

#### 12. `max_epochs = 18` (Line 106)
* **What it means in plain English**: The training runs for a maximum of 18 full passes through the dataset.
* **Why we stopped at 18**: Our validation monitoring proved accuracy peaked at **Epoch 10** (`best_acc_top1_epoch_10.pth`). Training further started memorizing the training videos.

#### 13. `clip_len = 48` (Line 46)
* **What it means in plain English**: Sub-samples exactly 48 evenly spaced frames across the 3-second exercise clip.
* **Why we chose 48**: At 30 FPS, 48 frames covers 1.6 to 2.0 seconds—the exact physical duration of one human gym repetition (e.g. descending and ascending in a squat).

#### 14. `with_kp = False, with_limb = True` (Line 54)
* **What it means in plain English**: Tells the data pipeline to turn OFF isolated joint dots (`with_kp=False`) and turn ON solid connected bone lines (`with_limb=True`).
* **Why we chose it**: The single most important breakthrough in our FYP! It gave the AI the ability to see parallel thigh bones in squats vs split legs in lunges, boosting squat accuracy by +160%!

#### 15. `sigma = 0.6` (Line 54)
* **What it means in plain English**: Controls how wide and blurry the glowing neon bone lines are on the $56 \times 56$ heatmap grid.
* **Why we chose 0.6**: A line that is too thin (0.2) disappears when downsampled. A line that is too fat (1.5) blends the left and right legs together into an unrecognizable blob. 0.6 creates clear, distinct bone tubes.

#### 16. `RandomRotateKeypoints(max_angle=12.0)` (Line 53)
* **What it means in plain English**: During training, the computer randomly tilts the skeletons left and right by up to 12 degrees.
* **Why we chose it**: In the real world, users prop their phones up against water bottles or hold them in their hands at slight tilts. Training with $\pm 12^\circ$ tilt jitter taught the AI to recognize exercises even if the phone is not mounted perfectly upright!

---

# 7. Module 4: Real-Time Repetition Counting (4-Stage State Machine)

### What It Actually Means:
A foolproof counter that tracks your completed reps (e.g. "Rep 1, Rep 2, Rep 3") without ever double-counting if your body shakes or hesitates.

### Step-by-Step Flow (Using the In-Line Teaching Format):
1. **Raw Angle Calculation (Un-clamped Joint Flexion, which actually means: calculating the exact geometric angle of the knee without artificial limits)**: "And this helped us in our project by giving us the true physical bend of the joint without masking camera glitches."
2. **Descent Trigger (`START` $\to$ `INFLECTION`, which actually means: athlete starts lowering down, knee angle drops below 146°)**: "And this helped us in our project by recognizing that a repetition has begun."
3. **Parallel Depth Check (`INFLECTION` $\to$ `PEAK`, which actually means: athlete hits valid parallel squat depth, knee angle $\le 115^\circ$)**: "And this helped us in our project by guaranteeing that half-reps or shallow dips are strictly rejected and not counted."
4. **Ascent Return (`PEAK` $\to$ `COMPLETION`, which actually means: athlete pushes all the way back up to standing, knee angle $\ge 146^\circ$)**: "And this helped us in our project by adding exactly +1 to the rep counter only after the full range of motion is completed."

### Where It Lives in the Code:
* Kinematics State Machine: [`backend/kinematics.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py) (Class `RepetitionStateMachine`)
* Biomechanical Thresholds: [`backend/config.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/config.py) (Lines 10–16)

### The "WHY" Section:
* **Why a 4-Stage State Machine instead of simple peak detection (like SciPy `find_peaks`)?**  
  * *Why We Did It*: Peak detectors cannot run on live video streams because they need the entire workout recording to find peaks in a graph. Furthermore, if an athlete shakes at the bottom of a heavy squat, a peak detector sees 3 tiny bumps and counts **3 fake reps**! Our 4-stage FSM requires crossing the full physical range of motion before registering an increment.

---

# 8. Module 5: Posture Correctness & Form Checking (All 7 Exercises)

### What It Actually Means:
An AI coach that checks your posture on every frame and gives you exact corrections (like *"Tuck your elbows in"* or *"Lift your hips"*).

### Plain-English Form Rules Across All 7 Exercises:
1. **Squats**: Thighs must reach parallel to floor (Knee angle $\le 115^\circ$). Knees must not cave in ($\text{FPPA} \ge 165^\circ$).
2. **Push-Ups**: Chest must drop until elbows bend to $95^\circ$. Hips must not sag (body straight line $> 160^\circ$). Elbows must not flare out like chicken wings (angle $< 75^\circ$).
3. **Planks**: Body must form a straight surfboard line from shoulders to hips to ankles ($162^\circ\text{ to }198^\circ$).
4. **Lunges**: Front knee must bend to $90^\circ$ without shooting far past toes ($> 50^\circ$). Torso must stay upright ($> 130^\circ$).
5. **Bicep Curls**: Full curl up (elbow $\le 50^\circ$) and full lowering down (elbow $\ge 155^\circ$). No lower-back swinging ($< 15^\circ$).
6. **Jumping Jacks**: Hands must reach above shoulder height (abduction $\ge 140^\circ$). Feet must jump wider than hip width ($1.35\times$). Torso must not lean sideways ($< 12^\circ$).
7. **High Knees**: Raised knee must reach hip height (thigh parallel to floor). Torso must stay upright ($< 15^\circ$ forward lean).

### Where It Lives in the Code:
* Exercise Evaluators: [`backend/kinematics.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py)
* Mobile Form Service: [`biomechai_flutter_latest/lib/services/form_validation_service.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/services/form_validation_service.dart)

### The "WHY" Section:
* **Why mathematical vector kinematics instead of black-box neural networks for form?**  
  * *Why We Did It*: Explainability and speed. If an AI gives an athlete a "70% score", the athlete doesn't know what to fix. With vector math, the app says: *"Your elbows flared out to 82°, tuck them in to 75°."* It calculates in **0.08 milliseconds** on CPU with zero hallucinations.

---

# 9. Module 6: Body Measurement & Transformation Tracking

### What It Actually Means:
A health screen where athletes log their height and weight, view their live BMI with a colored gauge, see their medical ideal weight range, and track progress over time.

### How It Works:
1. **BMI Formula**: $\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height in meters})^2}$
   * Blue: Underweight ($< 18.5$) | Green: Normal ($18.5\text{--}24.9$) | Yellow: Overweight ($25\text{--}29.9$) | Red: Obese ($\ge 30$)
2. **Devine Formula (Ideal Body Weight)**:  
   For individuals over 5 feet: $\text{Ideal Weight (kg)} = 50.0 + 2.3 \times (\text{Inches over 5 feet})$. Target range is $\text{Ideal} \pm 5\text{ kg}$.
3. **Cloud Logging**: Saved with dates in Firestore subcollection `/users/{uid}/body_measurements`.

### Where It Lives in the Code:
* Screen UI: [`biomechai_flutter_latest/lib/screens/body_measurement_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/body_measurement_screen.dart)
* Medical Citation: [Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm. 1974](https://pubmed.ncbi.nlm.nih.gov/4435882/)

### The "WHY" Section:
* **Why the Devine Formula instead of BMI alone?**  
  * *Why We Did It*: BMI cannot tell muscle from fat. A muscular athlete can have a BMI of 27 and be falsely called "Overweight". The Devine Formula gives a medically realistic target weight based on bone height alone.

---

# 10. Module 7: AI Clinical Injury Prevention (Full Body: Shoulders, Spine, Lower Back & Knees)

### What It Actually Means:
An automated clinical safety guard that monitors your **entire body**—not just knees, but shoulders, spine, lower back, and elbows—to detect dangerous joint stress before it causes acute tears or chronic orthopedic injuries.

---

### The Complete Body-Part Injury Prevention Breakdown Across All 7 Exercises

Here is the honest truth: BioMechAI protects **4 distinct anatomical regions** of the body across all 7 exercises:

```
                      FULL-BODY AI INJURY PREVENTION ENGINE
 
       [UPPER BODY: SHOULDERS & ELBOWS]             [CORE & SPINE: LUMBAR VERTEBRAE]
    Push-Up Elbow Flare (> 65°):                 Push-Up / Plank Hip Sag (> 10% below line):
      -> Subacromial Shoulder Impingement          -> L4-L5 Lumbar Spine Compression & Shear
      -> Rotator Cuff Supraspinatus Tear           -> Facet Joint Hyperextension
    Bicep Curl Elbow Drift (> 30°):              Bicep Curl Torso Swing (> 20°):
      -> Anterior Deltoid & Bicipital Overload     -> Lumbar Hyperextension Strain
                                                 High Knees Forward Lean (> 15°):
                                                   -> Iliopsoas & Lower Back Compensation
 
                         [LOWER BODY: KNEES & LIGAMENTS]
                      Squat & Lunge Knee Valgus (Munro FPPA < 165°):
                        -> Acute Anterior Cruciate Ligament (ACL) Tear
                        -> Medial Collateral Ligament (MCL) Sprain
                        -> Patellofemoral Meniscus Shearing
```

---

### 1. Upper Body Injury Prevention: Shoulders & Rotator Cuff
* **Injury Guard 1: Subacromial Shoulder Impingement (Push-Ups)**:
  * *Clinical Danger*: When an athlete does push-ups with elbows flared wide out like chicken wings ($> 65^\circ$ from torso), the greater tuberosity of the humerus pinches the **supraspinatus tendon** against the acromion bone, leading to chronic rotator cuff inflammation or full tears.
  * *Mathematical Rule*: Shoulder-to-elbow vector angle relative to the torso axis must stay $\le 65.0^\circ$.
  * *Audio Warning Triggered*: `"WARN_ELBOW_FLARE"` $\to$ **"Tuck your elbows closer to your body!"**
  * *Code File*: [`backend/kinematics.py:422-436`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L422-L436)
* **Injury Guard 2: Anterior Deltoid & Bicipital Tendon Overload (Bicep Curls)**:
  * *Clinical Danger*: Allowing the elbows to drift forward ($> 30^\circ$ from vertical) during curls shifts the mechanical load off the biceps brachii and onto the fragile long head of the biceps tendon and anterior deltoid.
  * *Mathematical Rule*: Angle of upper arm from vertical must stay $\le 30.0^\circ$.
  * *Audio Warning Triggered*: `"WARN_ELBOW_DRIFT"` $\to$ **"Pin your elbows to your sides!"**
  * *Code File*: [`backend/kinematics.py:525-540`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L525-L540)

---

### 2. Spine & Lower Back Injury Prevention: Lumbar Disc Herniation & Shear
* **Injury Guard 3: Lumbar Disc Compression & Spondylolysis (Push-Ups & Planks)**:
  * *Clinical Danger*: When core abdominals fatigue, the hips sag toward the floor (anterior pelvic tilt). This places extreme **compressive and shearing force on the L4–L5 and L5–S1 lumbar vertebrae**, leading to lower back disc bulges and facet joint pinching.
  * *Mathematical Rule*: Hip joint center must not sag $> 10\%$ of total body length below the straight shoulder-to-ankle axis.
  * *Audio Warning Triggered*: `"WARN_HIP_SAG"` $\to$ **"Tighten your core, lift your hips!"**
  * *Code File*: [`backend/kinematics.py:394-413`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L394-L413) (Push-Ups) and [`backend/kinematics.py:465-485`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L465-L485) (Planks)
* **Injury Guard 4: Lumbar Hyperextension Shear (Bicep Curls)**:
  * *Clinical Danger*: Heaving heavy weights by swinging the upper body backward ($> 20^\circ$) uses spinal momentum rather than bicep strength, exerting violent lumbar shear forces.
  * *Mathematical Rule*: Torso line from shoulders to hips must not deviate $> 20.0^\circ$ from vertical.
  * *Audio Warning Triggered*: `"WARN_TORSO_SWING"` $\to$ **"Keep your back straight, no swinging!"**
  * *Code File*: [`backend/kinematics.py:541-555`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L541-L555)
* **Injury Guard 5: Iliopsoas & Lumbar Overload (High Knees)**:
  * *Clinical Danger*: Leaning the torso forward ($> 15^\circ$) to fake knee height overstrains the iliopsoas hip flexors and causes lumbar rounding.
  * *Mathematical Rule*: Torso vertical lean must stay $\le 15.0^\circ$.
  * *Audio Warning Triggered*: `"WARN_FORWARD_LEAN"` $\to$ **"Stand tall, don't lean forward!"**
  * *Code File*: [`backend/kinematics.py:657-670`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L657-L670)

---

### 3. Lower Body Injury Prevention: Knee Ligaments (ACL & Meniscus)
* **Injury Guard 6: Dynamic Knee Valgus & Acute ACL Tear (Squats & Lunges)**:
  * *Clinical Danger*: When knees collapse inward toward each other under heavy flexion load, the knee joint undergoes combined knee abduction and internal tibial rotation. This exerts extreme mechanical strain on the **Anterior Cruciate Ligament (ACL)**, which can rupture completely in under 100 milliseconds!
  * *Mathematical Rule*: Munro Frontal Plane Projection Angle (**FPPA**) must stay $\ge 165.0^\circ$ whenever knee flexion is under active load ($\le 130.0^\circ$).
  * *Audio Warning Triggered*: `"WARN_KNEE_VALGUS"` $\to$ **"Push your knees out!"**
  * *Code File*: [`backend/kinematics.py:315-365`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L315-L365)
  * *Clinical Citation*: [Munro, Herrington, & Comfort, Clinical Biomechanics (2012)](https://pubmed.ncbi.nlm.nih.gov/22488285/)

---

### 4. Why Did Earlier Documentation Focus So Heavily on the Knee?
An honest question deserves an honest answer:
1. **The Severity of the Injury**: An ACL tear from knee valgus is an **acute, catastrophic surgical injury** that requires surgery and 9–12 months of rehabilitation. Shoulder impingement and lower back fatigue are chronic over-use injuries.
2. **The Clinical Citation**: In FYP-I (Semester 7), the evaluation panel asked: *"What clinical medical paper proves your injury threshold is not just a made-up number?"* We cited **Munro et al. (2012)**, who specifically published the $165^\circ$ FPPA cutoff for dynamic knee valgus. Because Munro et al. had a famous published paper, earlier project summaries over-emphasized the knee, making it look like upper-body checks didn't exist.
3. **The Reality of the Code**: As shown above in [`backend/kinematics.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py), **every single exercise has dedicated kinematic injury prevention rules for the shoulders, spine, lower back, and knees**.

---

### The "WHY" Section:
* **Why did we use the Munro FPPA angle ($< 165^\circ$) for knees instead of pixel distance?**  
  * *Why We Did It*: Pixel distance shrinks when you take a step back from the phone camera, triggering false alarms! Angles are scale-invariant: whether you stand 1 meter or 4 meters away, the angle remains identical.
* **Why did we evaluate elbow flare ($> 65^\circ$) relative to the torso axis rather than the floor?**  
  * *Why We Did It*: In push-ups, the user's body is tilted. Measuring elbow angle relative to the floor would give wrong readings if the push-up is done on an incline. Measuring relative to the **torso axis** ensures the angle is anatomically accurate regardless of body tilt.

---

# 11. Module 8: AI Workout Companion with Live Voice Coaching

### What It Actually Means:
A live voice trainer that speaks directly through your phone speaker or headphones so you don't have to look at your phone screen while exercising.

### How It Works with Priority Preemption:
* **Priority 1 (Emergency Safety)**: *"Push your knees out!"*, *"Lift your hips!"* (Cuts off any other audio immediately to protect your joints).
* **Priority 2 (Rep Milestones)**: *"Rep 5 completed!"*
* **Priority 3 (Praise)**: *"Great depth, keep going!"*
* **Safety Watchdog**: A 3.0-second hardware timer prevents the phone audio from freezing.

### Where It Lives in the Code:
* Mobile Voice Service: [`biomechai_flutter_latest/lib/services/voice_coaching_service.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/services/voice_coaching_service.dart)
* Backend Coaching Logic: [`backend/kinematics.py`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py) (Class `VoiceCoachingEngine`)

### The "WHY" Section:
* **Why native on-device TTS (`flutter_tts`) instead of cloud speech (Google Cloud TTS / ElevenLabs)?**  
  * *Why We Did It*: Cloud voices take 1 to 2 seconds to download. By the time a cloud voice speaks, your squat rep is already over! On-device speech speaks in **less than 10 milliseconds**, works offline in gym basements, and costs $0.

---

# 12. Module 9: Trainer Dashboard & Timestamped Feedback

### What It Actually Means:
A coach's portal where personal trainers can view their athletes' workout logs, review form scores, and leave advice linked to the exact second in the workout video.

### How It Works:
1. Trainer signs in and opens their client list.
2. Selects an athlete to view completed sessions, rep counts, and form scores.
3. Leaves **Timestamped Feedback** linked to an exact second (e.g. *"At second 14 (Rep 4), your chest collapsed. Keep your eyes up!"*).
4. The athlete sees this comment directly on their workout summary.

### Where It Lives in the Code:
* Trainer Dashboard Screen: [`biomechai_flutter_latest/lib/screens/trainer_dashboard_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/trainer_dashboard_screen.dart)
* Trainer Feedback Model: [`biomechai_flutter_latest/lib/models/trainer_feedback.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/models/trainer_feedback.dart)

### The "WHY" Section:
* **Why Timestamped Feedback instead of a standard chat message?**  
  * *Why We Did It*: Saying *"Your form was bad yesterday"* doesn't help the athlete. Attaching the comment to `videoTimestamp: 14` lets the athlete jump straight to second 14 to see their exact mistake.

---

# 13. Master Research Bibliography: Exact Clickable Paper & Weight Links

Every link below has been **independently tested and verified via live HTTP requests** to ensure it opens directly without broken URLs, 404 errors, or truncated links:

### 13.1 Deep Learning & Computer Vision Foundations
1. **PoseC3D Architecture Paper (CVPR 2022)**:  
   *Title*: *Revisiting Skeleton-based Action Recognition* (Haodong Duan, Yue Zhao, Kai Chen, Dahua Lin, & Bo Dai, CVPR 2022, pp. 2969–2978)  
   👉 [Read Official arXiv Abstract (arXiv:2104.13586)](https://arxiv.org/abs/2104.13586)  
   👉 [Download Full Paper PDF Directly from arXiv](https://arxiv.org/pdf/2104.13586.pdf)  
   👉 [CVF Open Access Official Record](https://openaccess.thecvf.com/content/CVPR2022/html/Duan_Revisiting_Skeleton-Based_Action_Recognition_CVPR_2022_paper.html)  
   👉 [Download CVF Open Access PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Duan_Revisiting_Skeleton-Based_Action_Recognition_CVPR_2022_paper.pdf)  
   👉 [OpenMMLab MMAction2 GitHub Repository](https://github.com/open-mmlab/mmaction2)

2. **FineGYM Dataset Paper (CVPR 2020)**:  
   *Title*: *FineGym: A Hierarchical Video Dataset for Fine-Grained Action Understanding* (Dian Shao, Yue Zhao, Bo Dai, & Dahua Lin, CVPR 2020, pp. 10886–10895)  
   👉 [Download CVPR 2020 Open Access PDF](https://openaccess.thecvf.com/content_CVPR_2020/papers/Shao_FineGym_A_Hierarchical_Video_Dataset_for_Fine-Grained_Action_Understanding_CVPR_2020_paper.pdf)  
   👉 [FineGYM Official Project Website](https://sdolivia.github.io/FineGym/)  
   👉 [FineGYM Official GitHub Repository (SDOlivia/FineGym)](https://github.com/SDOlivia/FineGym/)

3. **Google MediaPipe BlazePose (CVPR Workshop 2020)**:  
   *Title*: *BlazePose: On-device Real-time Body Pose Tracking* (Valentin Bazarevsky, Ivan Grishchenko, Karthik Raveendran, Tyler Zhu, Fan Zhang, & Matthias Grundmann, 2020)  
   👉 [Read Official arXiv Abstract (arXiv:2006.10204)](https://arxiv.org/abs/2006.10204)  
   👉 [Download Full Paper PDF Directly from arXiv](https://arxiv.org/pdf/2006.10204.pdf)

4. **Linear Learning Rate Scaling Rule (Goyal et al., 2017)**:  
   *Title*: *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour* (Priya Goyal, Piotr Dollár, Ross Girshick, Pieter Noordhuis, Lukasz Wesolowski, Aapo Kyrola, Andrew Tulloch, Yangqing Jia, & Kaiming He, 2017)  
   👉 [Read Official arXiv Abstract (arXiv:1706.02677)](https://arxiv.org/abs/1706.02677)  
   👉 [Download Full Paper PDF Directly from arXiv](https://arxiv.org/pdf/1706.02677.pdf)

5. **Dropout Regularization (Srivastava et al., 2014)**:  
   *Title*: *Dropout: A Simple Way to Prevent Neural Networks from Overfitting* (Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, & Ruslan Salakhutdinov, Journal of Machine Learning Research, 15(56): 1929–1958, 2014)  
   👉 [Read Journal of Machine Learning Research (JMLR) Record](https://jmlr.org/papers/v15/srivastava14a.html)  
   👉 [Download JMLR Paper PDF](https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf)

---

### 13.2 Official Pretrained Model Checkpoints (Direct Downloads from OpenMMLab)
* 👉 [Download FineGYM Limb Checkpoint (`gym-limb_20220815-2e6e3c5c.pth`)](https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_gym-limb/slowonly_r50_8xb16-u48-240e_gym-limb_20220815-2e6e3c5c.pth) *(Champion Pretrained Backbone used in BioMechAI)*  
* 👉 [Download FineGYM Keypoint Checkpoint (`gym-keypoint_20220815-da338c58.pth`)](https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_gym-keypoint/slowonly_r50_8xb16-u48-240e_gym-keypoint_20220815-da338c58.pth)  
* 👉 [Download NTU RGB+D 60 Checkpoint (`ntu60-xsub-keypoint_20220815-38db104b.pth`)](https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint_20220815-38db104b.pth)

---

### 13.3 Clinical Biomechanics & Sports Medicine Papers
1. **Dynamic Knee Valgus FPPA Threshold ($165^\circ$) (Munro et al., 2012)**:  
   *Title*: *Comparison of 2D and 3D techniques for assessing knee joint center displacement during dynamic tasks* (Matt Munro, Lee Herrington, & Paul Comfort, Clinical Biomechanics, 27(9): 920–925, 2012)  
   👉 [PubMed National Library of Medicine Record (PMID: 22488285)](https://pubmed.ncbi.nlm.nih.gov/22488285/)  
   👉 [Publisher Permanent DOI (10.1016/j.clinbiomech.2012.03.004)](https://doi.org/10.1016/j.clinbiomech.2012.03.004)

2. **Knee Abduction Moments & ACL Injury Prediction (Hewett et al., 2005)**:  
   *Title*: *Biomechanical measures of neuromuscular control and valgus loading of the knee predict anterior cruciate ligament injury risk in female athletes: a prospective study* (Timothy E. Hewett, Gregory D. Myer, Kevin R. Ford, et al., American Journal of Sports Medicine, 33(4): 492–501, 2005)  
   👉 [PubMed National Library of Medicine Record (PMID: 15722287)](https://pubmed.ncbi.nlm.nih.gov/15722287/)

3. **Squat Biomechanics & Parallel Depth (Schoenfeld 2010 & Escamilla 2001)**:  
   *Title*: *Squatting kinematics and kinetics and their application to exercise performance* (Brad J. Schoenfeld, Journal of Strength and Conditioning Research, 24(12): 3497–3506, 2010)  
   👉 [PubMed Record (PMID: 20182386)](https://pubmed.ncbi.nlm.nih.gov/20182386/)  
   👉 [Publisher Permanent DOI (10.1519/JSC.0b013e3181bac2d7)](https://doi.org/10.1519/JSC.0b013e3181bac2d7)  
   *Title*: *Knee biomechanics of the dynamic squat exercise* (Rafael F. Escamilla, Medicine & Science in Sports & Exercise, 33(1): 127–141, 2001)  
   👉 [PubMed Record (PMID: 11270570)](https://pubmed.ncbi.nlm.nih.gov/11270570/)

4. **Shoulder Impingement & Push-Up Mechanics (Flatow et al. 1994 & Cogley et al. 2005)**:  
   *Title*: *Excursion of the rotator cuff under the acromion: Patterns of subacromial contact* (Evan L. Flatow, Louis J. Soslowsky, Jonathan B. Ticker, et al., American Journal of Sports Medicine, 22(6): 779–788, 1994)  
   👉 [PubMed Record (PMID: 7856802)](https://pubmed.ncbi.nlm.nih.gov/7856802/)  
   *Title*: *Comparison of muscle activation using various hand positions during the push-up exercise* (Robert M. Cogley, Tod A. Archambault, Jon F. Fibeger, et al., Journal of Strength and Conditioning Research, 19(3): 628–633, 2005)  
   👉 [PubMed Record (PMID: 16095413)](https://pubmed.ncbi.nlm.nih.gov/16095413/)

5. **Spine Biomechanics & Plank Neutral Core Stabilization (McGill 2010)**:  
   *Title*: *Core training: Evidence translating to better performance and injury prevention* (Stuart M. McGill, Strength and Conditioning Journal, 32(3): 33–46, 2010)  
   👉 [Publisher Permanent DOI (10.1519/SSC.0b013e3181df4521)](https://doi.org/10.1519/SSC.0b013e3181df4521)

6. **Ideal Body Weight (Devine Formula 1974 & Pai & Paloucek 2000)**:  
   *Title*: *Gentamicin therapy* (Ben J. Devine, Drug Intelligence & Clinical Pharmacy, 8(11): 650–655, 1974)  
   👉 [PubMed Record (PMID: 4435882)](https://pubmed.ncbi.nlm.nih.gov/4435882/)  
   *Title*: *The origin of the 'Ideal Body Weight' equations* (Manjunath P. Pai & Frank P. Paloucek, Annals of Pharmacotherapy, 34(9): 1066–1069, 2000)  
   👉 [PubMed Record (PMID: 10981254)](https://pubmed.ncbi.nlm.nih.gov/10981254/)

7. **Body Mass Index (BMI) (Keys et al. 1972 & WHO Expert Committee 1995)**:  
   *Title*: *Indices of relative weight and obesity* (Ancel Keys, Flaminio Fidanza, Martti J. Karvonen, Noburu Kimura, & Henry L. Taylor, Journal of Chronic Diseases, 25(6–7): 329–343, 1972)  
   👉 [PubMed Record (PMID: 4650929)](https://pubmed.ncbi.nlm.nih.gov/4650929/)  
   *Title*: *Physical status: the use and interpretation of anthropometry* (World Health Organization Expert Committee, WHO Technical Report Series, No. 854, Geneva, 1995)  
   👉 [PubMed Record (PMID: 8594834)](https://pubmed.ncbi.nlm.nih.gov/8594834/)

---

# 14. Master Scientific Angle & Calculation Origin Table: The Exact Source of Every Number

Below is the **verifiable scientific ledger** for every angle, threshold, and formula coded into BioMechAI. When your supervisor or panel asks *"Where did this number come from?"*, refer directly to this table and the proofs below:

| Biomechanical Metric | Numerical Value in Code | Code Location | Exact Scientific Origin & Citation | Clinical & Biomechanical Justification |
| :--- | :---: | :---: | :--- | :--- |
| **Squat Parallel Depth** | $\le 115.0^\circ$ | [`backend/config.py:11`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/config.py#L11) | [Schoenfeld (2010), PMID: 20182386](https://pubmed.ncbi.nlm.nih.gov/20182386/)<br>[Escamilla (2001), PMID: 11270570](https://pubmed.ncbi.nlm.nih.gov/11270570/) | Femur parallel to ground occurs at $110\text{--}115^\circ$ tibiofemoral flexion, maximizing gluteus maximus and quadriceps motor unit recruitment. |
| **Upright Standing Return** | $\ge 146.0^\circ$ | [`backend/config.py:12`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/config.py#L12) | Standard Anthropometric Standing Neutral (*Chaffin et al., Occupational Biomechanics, 4th ed., Wiley, 2006*). | Natural standing extension is $150\text{--}175^\circ$. Setting threshold to $146^\circ$ registers immediate rep completion without forcing hyperextension lock. |
| **Anatomical Sanity Floor** | $\ge 35.0^\circ$ | [`backend/config.py:15`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/config.py#L15) | Human Knee Anatomical ROM Limit (*Kapandji, Physiology of the Joints, Vol 2, Elsevier, 2010*). | Maximum active human knee flexion is $140\text{--}145^\circ$ from extension (angle $\ge 35\text{--}40^\circ$). Anything $< 35^\circ$ is a 2D camera occlusion glitch. |
| **Knee Valgus (ACL Risk)** | $\text{FPPA} < 165.0^\circ$ | [`backend/config.py:14`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/config.py#L14) | [Munro et al. (2012), PMID: 22488285](https://pubmed.ncbi.nlm.nih.gov/22488285/)<br>[Hewett et al. (2005), PMID: 15722287](https://pubmed.ncbi.nlm.nih.gov/15722287/) | Frontal Plane Projection Angle $< 165^\circ$ indicates medial inward collapse, multiplying dynamic shear force on the Anterior Cruciate Ligament. |
| **Valgus Load Gating** | Knee Flexion $\le 130.0^\circ$ | [`backend/config.py:13`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/config.py#L13) | [Escamilla et al. (1998), PMID: 9565942](https://pubmed.ncbi.nlm.nih.gov/9565942/) | Patellofemoral and cruciate ligament compressive forces are negligible during standing and spike dramatically below $130^\circ$ knee flexion. |
| **Push-Up Elbow Flare** | $> 65.0^\circ$ | [`backend/kinematics.py:425`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L425) | [Flatow et al. (1994), PMID: 7856802](https://pubmed.ncbi.nlm.nih.gov/7856802/)<br>[Cogley et al. (2005), PMID: 16095413](https://pubmed.ncbi.nlm.nih.gov/16095413/) | Abducting humerus $> 65^\circ$ compresses the supraspinatus rotator cuff tendon against the anterior acromion, causing subacromial impingement syndrome. |
| **Push-Up Chest Depth** | Elbow Flexion $\le 95.0^\circ$ | [`biomechai_flutter_latest/lib/services/form_validation_service.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/services/form_validation_service.dart) | ACSM Exercise Testing Standards / NSCA Push-Up Protocol. | Reaching $90\text{--}95^\circ$ elbow bend achieves full eccentric stretch of pectoralis major sternal fibers. |
| **Hip Sag (Push-Up/Plank)** | Sag $> 10\%$ of Body Length | [`backend/kinematics.py:404`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L404) | [McGill (2010), DOI: 10.1519/SSC.0b013e3181df4521](https://doi.org/10.1519/SSC.0b013e3181df4521) | Anterior pelvic tilt sagging $> 10\%$ shifts load from the rectus abdominis to lumbar facet joints, risking disc herniation and spondylolysis at L4–L5. |
| **Plank Neutral Alignment** | $162.0^\circ\text{--}198.0^\circ$ | [`backend/kinematics.py:465`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L465) | McGill Spine Biomechanics Spine Neutral Zone ($\pm 18^\circ$ deviation). | Preserves neutral lumbar lordosis while maximizing transversus abdominis and abdominal oblique endurance. |
| **Bicep Curl Arm Drift** | $> 30.0^\circ$ from vertical | [`backend/kinematics.py:531`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L531) | NSCA Essentials of Strength Training (*Haff & Triplett, 2016*). | Drifting humerus forward $> 30^\circ$ shifts mechanical advantage to the anterior deltoid and causes bicipital tendon strain. |
| **Bicep Curl Torso Swing** | $> 20.0^\circ$ from vertical | [`backend/kinematics.py:546`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L546) | NSCA Free Weight Technical Guidelines. | Backward torso swing $> 20^\circ$ substitutes lumbar hyperextension momentum for bicep force, risking lumbar erector spinae sprain. |
| **Jumping Jack Arm ROM** | $\ge 140.0^\circ$ abduction | [`backend/kinematics.py:585`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L585) | ACSM Aerobic Dance and Calisthenics Exercise Standards. | Full scapulohumeral rhythm requires $> 140^\circ$ abduction to recruit lateral deltoid and upper trapezius. |
| **High Knees Elevation** | Knee Height $\le$ Hip Height | [`backend/kinematics.py:649`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L649) | ACE Exercise Technique Standards (High Knee Runs). | Requires true $90^\circ$ hip flexion to recruit psoas major and rectus femoris. |
| **High Knees Forward Lean** | $> 15.0^\circ$ from vertical | [`backend/kinematics.py:657`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L657) | NSCA Sprint Mechanics & Postural Stability (*Mann, 2013*). | Leaning forward $> 15^\circ$ compresses the lumbar spine and reduces hip flexor excursion. |
| **Body Mass Index (BMI)** | $\text{Weight} / \text{Height}^2$ | [`biomechai_flutter_latest/lib/screens/body_measurement_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/body_measurement_screen.dart) | [WHO Technical Report 854 (1995), PMID: 8594834](https://pubmed.ncbi.nlm.nih.gov/8594834/)<br>[Keys et al. (1972), PMID: 4650929](https://pubmed.ncbi.nlm.nih.gov/4650929/) | Clinical standard for categorizing Underweight ($<18.5$), Normal ($18.5\text{--}24.9$), Overweight ($25\text{--}29.9$), and Obese ($\ge 30$). |
| **Ideal Body Weight (IBW)** | $50\text{ kg} + 2.3 \times \text{Inches}_{>5\text{ft}}$ | [`biomechai_flutter_latest/lib/screens/body_measurement_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/body_measurement_screen.dart) | [Devine (1974), PMID: 4435882](https://pubmed.ncbi.nlm.nih.gov/4435882/)<br>[Pai & Paloucek (2000), PMID: 10981254](https://pubmed.ncbi.nlm.nih.gov/10981254/) | Medical pharmacology gold standard for calculating physiological healthy weight based on skeletal height alone. |
| **Learning Rate ($\eta = 0.01$)**| Linear Scaling: $0.1 \times \frac{16}{128}$ | [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py:103`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py#L103) | [Goyal et al. (2017), arXiv:1706.02677](https://arxiv.org/abs/1706.02677) | Linear scaling rule: learning rate scales linearly with batch size ($0.1 \times 16/128 = 0.0125 \approx 0.01$) to preserve gradient update magnitude. |
| **Dropout Ratio ($0.60$)** | $p = 0.60$ | [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py:29`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py#L29) | [Srivastava et al. (2014), JMLR Record](https://jmlr.org/papers/v15/srivastava14a.html) | Empirical tuning: $0.50$ overfitted on limb heatmaps; $0.70$ collapsed pushup accuracy to $28\%$; $0.60$ achieved the optimal bias-variance trade-off. |
| **Tilt Jitter ($\pm 12.0^\circ$)** | `max_angle = 12.0` | [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py:53`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py#L53) | Real-world Handheld Smartphone Incline Distribution. | Synthetic in-plane rotation ($\pm 12^\circ$) trains convolutional filters to be invariant to handheld phone mounting tilt. |

---

## 14.1 Exhaustive Mathematical Derivations & Biomechanical Proofs for Every Calculation

Here is the complete scientific and mathematical proof for every single calculation performed across the entire BioMechAI codebase:

### Calculation 1: 3D Euclidean Joint Angle (Cosine Rule Vector Math)
* **Code Reference**: [`backend/kinematics.py:68-80`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L68-L80) (`calculate_angle_3d`)
* **Mathematical Formula**:
  Given three 3D joint landmarks $A(x_A, y_A, z_A)$, vertex $B(x_B, y_B, z_B)$, and $C(x_C, y_C, z_C)$:
  $$\vec{u} = A - B = \begin{bmatrix} x_A - x_B \\ y_A - y_B \\ z_A - z_B \end{bmatrix}, \quad \vec{v} = C - B = \begin{bmatrix} x_C - x_B \\ y_C - y_B \\ z_C - z_B \end{bmatrix}$$
  $$\cos\theta = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|} = \frac{u_x v_x + u_y v_y + u_z v_z}{\sqrt{u_x^2 + u_y^2 + u_z^2}\sqrt{v_x^2 + v_y^2 + v_z^2}}$$
  $$\theta = \arccos\left(\text{clamp}(\cos\theta, -1.0, 1.0)\right) \times \frac{180^\circ}{\pi}$$
* **Mathematical Proof**: By the Cauchy-Schwarz inequality, $\frac{|\vec{u} \cdot \vec{v}|}{\|\vec{u}\| \|\vec{v}\|} \le 1$. In computer floating-point calculations, slight round-off errors can produce values like $1.0000000002$, which causes standard $\arccos$ to return `NaN` (Not a Number) and crash the app! Clamping $\cos\theta \in [-1.0, 1.0]$ guarantees absolute numerical stability across millions of video frames.

---

### Calculation 2: Munro Dynamic Knee Valgus FPPA & Load Gating Formula
* **Code Reference**: [`backend/kinematics.py:315-365`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L315-L365) (`calculate_dynamic_valgus_fppa`)
* **Clinical Citation**: [Munro, Herrington, & Comfort (2012), *Clinical Biomechanics*](https://pubmed.ncbi.nlm.nih.gov/22488285/); [Hewett et al. (2005), *American Journal of Sports Medicine*](https://pubmed.ncbi.nlm.nih.gov/15722287/)
* **Mathematical Formula**:
  Evaluated strictly in the coronal (frontal) 2D projection plane using Hip $H(x_H, y_H)$, Knee $K(x_K, y_K)$, and Ankle $A(x_A, y_A)$:
  $$\vec{u}_{\text{thigh}} = \begin{bmatrix} x_H - x_K \\ y_H - y_K \end{bmatrix}, \quad \vec{v}_{\text{shank}} = \begin{bmatrix} x_A - x_K \\ y_A - y_K \end{bmatrix}$$
  $$\text{FPPA} = \arccos\left(\frac{\vec{u}_{\text{thigh}} \cdot \vec{v}_{\text{shank}}}{\|\vec{u}_{\text{thigh}}\| \|\vec{v}_{\text{shank}}\|}\right) \times \frac{180^\circ}{\pi}$$
* **Why the $165.0^\circ$ Threshold?**: In normal anatomical standing alignment, the human leg exhibits a slight physiological valgus of $170\text{--}175^\circ$. Munro et al. (2012) conducted clinical motion capture on 40 athletic subjects and established that an FPPA dropping below $165.0^\circ$ during dynamic squatting or drop jumps is the **clinical diagnostic cutoff for abnormal dynamic knee valgus**. Hewett et al. (2005) demonstrated in a prospective study of female athletes that dynamic knee valgus is the single primary predictor of non-contact **Anterior Cruciate Ligament (ACL) rupture**.
* **Why the $130.0^\circ$ Load Gating?**: Escamilla et al. (1998) proved that tibiofemoral shear and patellofemoral compressive forces are minimal when the knee is straight ($140\text{--}180^\circ$). ACL stress spikes exclusively under active eccentric/concentric loading when the knee bends past $130.0^\circ$ ($\le 130.0^\circ$). BioMechAI gates valgus alerts so users are never falsely alerted while standing casually!

---

### Calculation 3: Perpendicular Hip Sag Ratio (Point-to-Line Orthogonal Projection)
* **Code Reference**: [`backend/kinematics.py:394-413`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L394-L413) (Push-Ups) and [`backend/kinematics.py:465-485`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L465-L485) (Planks)
* **Clinical Citation**: [McGill (2010), *Strength and Conditioning Journal*](https://doi.org/10.1519/SSC.0b013e3181df4521)
* **Mathematical Formula**:
  The line passing through the Shoulder $S(x_S, y_S)$ and Ankle $A(x_A, y_A)$ has standard linear equation:
  $$(y_A - y_S) x - (x_A - x_S) y + (x_A y_S - y_A x_S) = 0$$
  The perpendicular distance $d_{\perp}$ from the Hip $H(x_H, y_H)$ to this line is:
  $$d_{\perp} = \frac{|(y_A - y_S) x_H - (x_A - x_S) y_H + x_A y_S - y_A x_S|}{\sqrt{(y_A - y_S)^2 + (x_A - x_S)^2}}$$
  The total anatomical body length is:
  $$L_{\text{body}} = \|\vec{A} - \vec{S}\| = \sqrt{(x_A - x_S)^2 + (y_A - y_S)^2}$$
  The normalized sag ratio is:
  $$\text{Sag Ratio} = \frac{d_{\perp}}{L_{\text{body}}}$$
* **Why the $10\%$ Threshold?**: Stuart McGill, world-renowned professor of spine biomechanics at the University of Waterloo, showed that when the abdominal wall (rectus abdominis and obliques) fatigues, the pelvis tilts anteriorly. Sagging exceeding $10\%$ of total body length shifts spinal load away from active muscular containment directly onto the passive posterior elements of the spine (facet joints and intervertebral discs at L4–L5 and L5–S1), dramatically increasing disc herniation risk.

---

### Calculation 4: Push-Up Shoulder Impingement Elbow Flare Formula
* **Code Reference**: [`backend/kinematics.py:422-436`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L422-L436)
* **Clinical Citation**: [Flatow et al. (1994), *American Journal of Sports Medicine*](https://pubmed.ncbi.nlm.nih.gov/7856802/); [Cogley et al. (2005), *JSCR*](https://pubmed.ncbi.nlm.nih.gov/16095413/)
* **Mathematical Formula**:
  Let $\vec{v}_{\text{torso}} = \text{Hip} - \text{Shoulder}$ be the spinal cranial-caudal vector.  
  Let $\vec{v}_{\text{humerus}} = \text{Elbow} - \text{Shoulder}$ be the upper arm vector.  
  The anatomical shoulder abduction angle $\theta_{\text{abduction}}$ is:
  $$\theta_{\text{abduction}} = \arccos\left(\frac{\vec{v}_{\text{torso}} \cdot \vec{v}_{\text{humerus}}}{\|\vec{v}_{\text{torso}}\| \|\vec{v}_{\text{humerus}}\|}\right) \times \frac{180^\circ}{\pi}$$
* **Why the $65.0^\circ$ Threshold?**: Flatow et al. (1994) mapped subacromial contact patterns during arm elevation using stereophotogrammetry. When the humerus abducts beyond $65^\circ$ during pressing movements, the greater tuberosity of the humerus impinges directly against the undersurface of the acromion, reducing the subacromial space from ~10 mm down to under 4 mm and pinching the **supraspinatus tendon**. Cogley et al. (2005) demonstrated that pressing with elbows tucked within $45\text{--}65^\circ$ maintains maximal pectoral recruitment while eliminating subacromial shear.

---

### Calculation 5: Bicep Curl Elbow Drift and Torso Swing Formulas
* **Code Reference**: [`backend/kinematics.py:525-555`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L525-L555)
* **Citation**: NSCA Essentials of Strength Training (*Haff & Triplett, 2016*)
* **Mathematical Formulas**:
  * **Elbow Drift**: Angle between the humerus $\vec{v}_{\text{arm}} = \text{Elbow} - \text{Shoulder}$ and the downward gravity vector $\vec{g} = (0, 1)$:
    $$\theta_{\text{drift}} = \arccos\left(\frac{\vec{v}_{\text{arm}} \cdot \begin{bmatrix} 0 \\ 1 \end{bmatrix}}{\|\vec{v}_{\text{arm}}\|}\right) \times \frac{180^\circ}{\pi} > 30.0^\circ$$
  * **Torso Swing**: Angle between the spinal vector $\vec{v}_{\text{torso}} = \text{Shoulder} - \text{Hip}$ and the true vertical vector $\vec{v}_{\text{up}} = (0, -1)$:
    $$\theta_{\text{swing}} = \arccos\left(\frac{\vec{v}_{\text{torso}} \cdot \begin{bmatrix} 0 \\ -1 \end{bmatrix}}{\|\vec{v}_{\text{torso}}\|}\right) \times \frac{180^\circ}{\pi} > 20.0^\circ$$
* **Clinical Justification**: Allowing the elbow to drift forward $> 30^\circ$ turns the bicep curl into an anterior deltoid front raise, removing mechanical tension from the biceps brachii short and long heads. Swinging the torso backward $> 20^\circ$ relies on hyperextension momentum of the lumbar spine, which multiplies shear load on the lumbar intervertebral discs.

---

### Calculation 6: High Knees Torso Lean & Coordinate Inversion Knee Elevation
* **Code Reference**: [`backend/kinematics.py:645-670`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L645-L670)
* **Citation**: American Council on Exercise (ACE) Technique Standards; Mann (2013), *Mechanics of Sprinting*
* **Mathematical Formulas**:
  * **Knee Elevation Check**: In computer vision image space, the vertical $y$-axis is inverted ($y=0$ is at the top of the camera frame, $y=1.0$ is at the bottom). Therefore, a knee reaching hip height is represented by:
    $$y_{\text{knee}} \le y_{\text{hip}}$$
    When $y_{\text{knee}} \le y_{\text{hip}}$, the femur is horizontal or elevated above parallel, confirming true $\ge 90^\circ$ hip flexion.
  * **Torso Lean Check**:
    $$\theta_{\text{lean}} = \arccos\left(\frac{(\text{Shoulder} - \text{Hip}) \cdot \begin{bmatrix} 0 \\ -1 \end{bmatrix}}{\|\text{Shoulder} - \text{Hip}\|}\right) \times \frac{180^\circ}{\pi} > 15.0^\circ$$
* **Biomechanical Justification**: Leaning the torso forward $> 15^\circ$ artificially closes the hip angle, giving the illusion of high knees without actual psoas major activation, while forcing compensatory thoracic and lumbar flexion.

---

### Calculation 7: Jumping Jack Arm ROM & Stance Width Ratio
* **Code Reference**: [`backend/kinematics.py:575-605`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/backend/kinematics.py#L575-L605)
* **Citation**: ACSM Aerobic Calisthenics Exercise Standards
* **Mathematical Formulas**:
  * **Arm Abduction ROM**:
    $$\theta_{\text{abduction}} = \text{Angle}(\text{Elbow}, \text{Shoulder}, \text{Hip}) \ge 140.0^\circ$$
  * **Dynamic Stance Width Ratio**:
    $$\text{Ratio} = \frac{\|\text{Ankle}_{\text{left}} - \text{Ankle}_{\text{right}}\|}{\|\text{Hip}_{\text{left}} - \text{Hip}_{\text{right}}\|} \ge 1.35$$
* **Biomechanical Justification**: Reaching $\ge 140^\circ$ of glenohumeral abduction engages full scapulohumeral upward rotation and activates the serratus anterior and lateral deltoids. Requiring feet to land $\ge 1.35\times$ hip width enforces true plyometric stretch-shortening cycles in the hip abductors (gluteus medius).

---

### Calculation 8: Body Mass Index (BMI) & Devine Ideal Body Weight (IBW)
* **Code Reference**: [`biomechai_flutter_latest/lib/screens/body_measurement_screen.dart`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_flutter_latest/lib/screens/body_measurement_screen.dart)
* **Clinical Citations**: [Keys et al. (1972), PMID: 4650929](https://pubmed.ncbi.nlm.nih.gov/4650929/); [Devine (1974), PMID: 4435882](https://pubmed.ncbi.nlm.nih.gov/4435882/); [Pai & Paloucek (2000), PMID: 10981254](https://pubmed.ncbi.nlm.nih.gov/10981254/)
* **Mathematical Formulas**:
  $$\text{BMI} = \frac{\text{Weight (kg)}}{\left(\frac{\text{Height (cm)}}{100}\right)^2}$$
  $$\text{IBW}_{\text{Devine}} = 50.0\text{ kg} + 2.3 \times \left(\frac{\text{Height (cm)}}{2.54} - 60\right)$$
  $$\text{Healthy Range} = [\text{IBW} - 5.0\text{ kg}, \quad \text{IBW} + 5.0\text{ kg}]$$
* **Proof & Clinical Validation**: Keys et al. (1972) evaluated relative weight formulas across 7,424 healthy men and proved that the Quetelet metric ($W/H^2$) showed the highest correlation with body fat percentage while being completely independent of skeletal height. Devine (1974) published the gold standard equation for calculating physiological drug dosing based on height-predicted lean body mass, validated across medical literature by Pai & Paloucek (2000).

---

### Calculation 9: PoseC3D 3D Spatiotemporal Limb Heatmap Rasterization
* **Code Reference**: [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py:44-55`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py#L44-L55)
* **Paper Citation**: [Duan et al. (CVPR 2022), arXiv:2104.13586](https://arxiv.org/abs/2104.13586)
* **Mathematical Formula**:
  For each bone segment $S_{c, t}$ connecting joint $A$ and joint $B$ in channel $c$ at frame $t$, the heatmap value at spatial pixel $(x, y)$ on the $56 \times 56$ grid is computed via a Gaussian distance function:
  $$H_c(x, y, t) = \exp\left(-\frac{\text{dist}\left((x, y), \overline{AB}\right)^2}{2\sigma^2}\right)$$
  where $\text{dist}\left((x, y), \overline{AB}\right)$ is the minimum Euclidean distance from point $(x, y)$ to the line segment $\overline{AB}$, and $\sigma = 0.6$.
* **Mathematical Proof**: Duan et al. (CVPR 2022) proved that representing human skeletons as stacked 3D continuous Gaussian volumes rather than sparse graph coordinates confers spatial convolution smoothness. Setting $\sigma = 0.6$ creates a tubular limb of width $\approx 3$ pixels on a $56 \times 56$ grid. If $\sigma < 0.3$, the lines disappear during strided 3D pooling. If $\sigma > 1.2$, the left and right legs fuse into a single blob, blinding the network to bilateral limb asymmetry.

---

### Calculation 10: Linear Learning Rate Scaling Rule & Bernoulli Dropout
* **Code Reference**: [`models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py:29, 103`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py#L29)
* **Citations**: [Goyal et al. (2017), arXiv:1706.02677](https://arxiv.org/abs/1706.02677); [Srivastava et al. (2014), JMLR](https://jmlr.org/papers/v15/srivastava14a.html)
* **Mathematical Formulas**:
  $$\eta = \eta_{\text{base}} \times \frac{B}{B_{\text{base}}} = 0.1 \times \frac{16}{128} = 0.0125 \approx \mathbf{0.01}$$
  $$P(r_j = 0) = p = 0.60, \quad P(r_j = 1) = 1 - p = 0.40, \quad \tilde{\mathbf{y}} = \frac{1}{1 - p} (\mathbf{r} \odot \mathbf{y})$$
* **Proof & Optimization Justification**: Goyal et al. (2017) proved that when the minibatch size $B$ is scaled, setting the learning rate $\eta$ proportional to $B$ keeps the expected gradient step magnitude constant across parameter space: $\mathbb{E}\left[\Delta w\right] \propto \eta \sum_{i=1}^B \nabla L_i(w) = \text{const}$. Inverted Bernoulli dropout with probability $p = 0.60$ scales remaining activations by $\frac{1}{1-0.60} = 2.5\times$ during training, ensuring that the expected activation magnitude at test time matches training without extra arithmetic overhead: $\mathbb{E}[\tilde{\mathbf{y}}] = \mathbf{y}$.


