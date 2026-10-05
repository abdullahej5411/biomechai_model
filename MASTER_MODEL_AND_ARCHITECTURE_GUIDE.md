# BioMechAI — Master Machine Learning Models, Architectural Evolution & End-to-End System Integration Guide

**Document Classification:** Academic Defense Technical Manual & System Architecture Reference  
**Project Phase:** Final Degree Graduation Deliverable (Semester 8 / FYP-II)  
**System Title:** BioMechAI — Edge-Cloud Hybrid Clinical AI Fitness Coaching & Injury Prevention Platform  

---

## 1. Executive Summary & Purpose

The goal of this document is to provide a complete, transparent, and step-by-step walkthrough of:
1. **The Machine Learning Models**: How each action recognition model was born, why previous iterations had specific bottlenecks, how the final champion model was developed, where pretrained weights originated, and the exact code implementations.
2. **The End-to-End System Architecture**: How every API, cloud tunnel, on-device mobile algorithm, deterministic physics engine, and cloud database communicate seamlessly to deliver a real-time, clinically validated fitness platform.

This guide is written in clear, structured, and accessible language to ensure that both academic evaluators and engineering practitioners can easily inspect the mathematical rationale and engineering decisions behind the system. In accordance with system documentation standards, all references remain general and focus strictly on engineering roles, athletes, coaches, and architectural modules.

```
+----------------------------------------------------------------------------------------------------+
|                                    BIOMECHAI SYSTEM TOPOGRAPHY                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   [ ATHLETE MOBILE CLIENT (Flutter Android) ]                                                      |
|   +-- Camera Video Stream (30 FPS, YUV420 nv21)                                                    |
|   +-- Google ML Kit On-Device Pose Estimation (33 3D Keypoints)                                    |
|   +-- Closed 4-Stage Rep Counting State Machine (UPRIGHT -> DESCENDING -> BOTTOM -> ASCENDING)     |
|   +-- Edge-Cloud Hybrid Fallback Engine (Immediate Local Kinematic Takeover on disconnect)        |
|   +-- Native Text-To-Speech (TTS) Voice Coaching Companion (Debounced Audio Cues)                  |
|   +-- Monocular Anthropometry Scanner (Standing Height Scale Anchor Calibration)                   |
|                                                                                                    |
|                                         |                                                          |
|       Encrypted WebSocket / HTTPS       | Dual Network Channel                                     |
|       (ngrok-skip-browser-warning)      | (persevere-kindred-tasty.ngrok-free.dev:8000)            |
|                                         v                                                          |
|                                                                                                    |
|   [ HIGH-PERFORMANCE AI BACKEND (Python FastAPI) ]                                                 |
|   +-- Endpoints: POST /classify | WebSocket /ws/stream | GET /health                               |
|   +-- Model: PoseC3D SlowOnly ResNet-50 3D CNN (Champion v5 Checkpoint, 8.33 MB)                   |
|   +-- Input Modality: 3D Spatiotemporal Connected Limb Heatmaps (48-frame sliding window)          |
|   +-- Kinematics Physics Engine: Munro FPPA Knee Valgus, McGill Hip Sag, Elbow Flares             |
|                                                                                                    |
|                                         |                                                          |
|       Real-Time Cloud Firestore Sync    | Atomic Batch Uploads (<300ms)                            |
|       (Project: biomechai-fitness)      |                                                          |
|                                         v                                                          |
|                                                                                                    |
|   [ COACH & ATHLETE WEB DASHBOARD (React + Vite + Tailwind) ]                                      |
|   +-- Multi-Tenant Role Isolation (Two-Way Coach-Athlete Pairing)                                  |
|   +-- Granular Multi-Exercise & Rep Breakdown Tables (SVG Status Badges & Fault Diagnostics)      |
|   +-- Cross-Platform Vector Assessment PDF Engine (jsPDF Multi-Page Clinical Reports)             |
|   +-- Real-Time Notification Center (/notifications)                                              |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Chronological Evolution of Action Recognition Models ("How Each Model Was Born")

The development of the exercise classification engine followed a rigorous, multi-generation evolutionary pathway. Each generation solved a fundamental scientific or practical limitation identified during empirical testing.

```
+----------------------------------------------------------------------------------------------------+
|                               MODEL EVOLUTION TIMELINE AT A GLANCE                                 |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   Generation 0: Random Forest (Heuristic Angles)                                                   |
|   [Result]: Apparent 84% accuracy -> Plummets to 56.08% under honest video-disjoint testing.       |
|   [Flaw]: Clip-level data leakage memorized subject identities. Failed temporal dynamics.           |
|                                      |                                                             |
|                                      v                                                             |
|   Generation 1: Architectural Selection (2D CNNs vs ST-GCN vs PoseC3D)                             |
|   [Finding]: ST-GCN brittle to coordinate noise; 2D RGB models too heavy and scene-biased.         |
|   [Decision]: Adopt PoseC3D 3D Heatmap Volumes for noise resilience and compact compute.           |
|                                      |                                                             |
|                                      v                                                             |
|   Generation 2: PoseC3D v1/v2/v3 (NTU-60 Daily Living Weights)                                     |
|   [Result]: 48.20% Top-1 Accuracy.                                                                 |
|   [Flaw]: NTU-60 lacks athletic dynamic range (designed for sedentary office/home actions).       |
|                                      |                                                             |
|                                      v                                                             |
|   Generation 3: PoseC3D v4 (FineGYM Dot Keypoint Heatmaps)                                         |
|   [Result]: 50.90% Top-1 Accuracy.                                                                 |
|   [Flaw]: Squat accuracy collapsed to 20.55% because disconnected dots overlap during deep flexion.|
|                                      |                                                             |
|                                      v                                                             |
|   Generation 4: PoseC3D v5 (FineGYM Connected Limb Heatmaps) -- ACTIVE CHAMPION                    |
|   [Result]: 53.38% Top-1 Accuracy | 53.15% Macro Recall | 91.22% Top-5 Accuracy.                  |
|   [Surge]: Squat surged from 20.55% to 53.42% (+160% relative gain) via 3D bone segment volumes.   |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

### Generation 0: The Baseline Random Forest & The "84% Accuracy" Illusion

* **Methodology**: In the initial project phase, exercise classification was attempted using classical tabular machine learning. Hand-crafted features (joint angles derived via the dot product of 2D coordinates, inter-joint Euclidean distances, and velocity deltas) were fed into a Random Forest Classifier.
* **The Apparent Success**: Early evaluations reported an impressive **`84%` classification accuracy**.
* **The Underlying Flaw (Clip-Level Data Leakage)**: 
  When videos were cut into small 2-second clips, clips from the *same video session* were randomly shuffled into both the training set and the test set. The Random Forest did not learn generalized exercise mechanics; instead, it memorized specific subject clothing colors, standing camera positions, and limb proportions.
* **The Honest Truth**:
  When a strict **video-disjoint partition** was enforced (ensuring that held-out testing videos came from subjects and sessions never seen during training), the Random Forest's actual accuracy dropped to **`56.08%`**.
* **Conclusion**: Classical tabular models cannot reliably capture 3D spatiotemporal trajectories, temporal phase transitions, or perspective invariance across diverse athletes.

---

### Generation 1: Architectural Exploration — Why PoseC3D?

To achieve true spatial and temporal generalization, three modern deep learning paradigms were evaluated:

| Architectural Approach | Core Mechanism | Critical Bottleneck for Mobile Fitness |
| :--- | :--- | :--- |
| **RGB-Based 3D CNNs**<br>*(e.g., I3D, SlowFast)* | Processes raw pixel video grids across time. | **Massive Compute (100+ GFLOPs)** and severe background bias (memorizing gym floorboards and equipment rather than human kinematics). |
| **Spatial-Temporal Graph Convolutions**<br>*(ST-GCN, 2s-AGCN)* | Represents joints as graph nodes connected by bone edges; passes coordinate vectors $(x, y, z)$. | **Extreme Noise Fragility**. If a wrist or ankle keypoint flickers or is briefly occluded, coordinate values jump, breaking graph topology and causing misclassification. |
| **Spatiotemporal 3D Heatmaps**<br>*(PoseC3D — Selected)* | Projects detected skeletons into stacked 3D volumetric heatmap cylinders ($C \times T \times H \times W$). | **High Noise Tolerance**. Gaussian blurring naturally handles keypoint coordinate jitter, while standard 3D CNNs leverage robust spatial pooling hierarchies. |

PoseC3D was selected because it delivers superior noise resilience, requires zero RGB background processing (preserving user privacy), and operates with a compact parameter footprint suitable for real-time edge-cloud deployment.

---

### Generation 2: PoseC3D v1, v2, and v3 (The NTU-60 Pretraining Baseline)

* **Pretrained Base**: OpenMMLab MMAction2 weights trained on the **NTU RGB+D 60** dataset (`ntu60-xsub-keypoint`).
* **Experimental Result**: Top-1 Accuracy plateaued at **`48.20%`**.
* **Scientific Diagnosis**: NTU-60 consists predominantly of indoor daily activities (drinking water, reading, picking up a pen, sitting down). The underlying convolutional filters were tuned to low-energy, small-amplitude limb movements. In athletic fitness, movements involve rapid eccentric drops, extreme joint flexion, and explosive kinetic chaining that NTU-60 filters struggled to resolve.

---

### Generation 3: PoseC3D v4 (FineGYM Keypoint Dot Heatmaps)

* **Pretrained Base**: FineGYM dataset (`gym-keypoint_20220815-2e6e3c5c.pth`), featuring high-dynamic gymnastic routines (vaulting, beam routines, parallel bars).
* **Heatmap Modality**: Disconnected Keypoint Dots (`with_kp=True, with_limb=False`, Gaussian blur $\sigma = 0.6$).
* **Overall Benchmark**: Overall Top-1 accuracy improved to **`50.90%`**.
* **The "Squat Blind Spot" Failure**:
  While exercises like Bicep Curls and Push-Ups improved, **Squat accuracy collapsed to an unacceptably low `20.55%`** (only 15 out of 73 held-out test clips were correctly classified).
* **Geometric Cause**: When an athlete descends into a deep parallel squat, the hip, knee, and ankle keypoint dots collapse close together in monocular perspective. The 3D convolutional kernels saw a cluster of overlapping dots and frequently misclassified the motion as a Lunge bottom or a Push-Up resting phase.

---

### Generation 4: PoseC3D v5 (The Production Champion — Connected Limb Heatmaps)

* **The Scientific Breakthrough**: Instead of rasterizing isolated joint dots, the engine was re-architected to generate **continuous 3D spatiotemporal limb cylinders** (`with_kp=False, with_limb=True`).
* **Limb Connections Modeled**:
  - Upper Arm: Shoulder $\rightarrow$ Elbow
  - Forearm: Elbow $\rightarrow$ Wrist
  - Thigh: Hip $\rightarrow$ Knee
  - Shank: Knee $\rightarrow$ Ankle
  - Torso: Shoulder $\rightarrow$ Hip
* **Pretrained Checkpoint**: OpenMMLab FineGYM Athletic Limb Checkpoint (`gym-limb_20220815-2e6e3c5c.pth`).
* **Active Checkpoint File**: `models/posec3d_v5_limb/best_acc_top1_epoch_10.pth` (File size: 8.33 MB).
* **Configuration File**: `models/posec3d_v5_limb/posec3d_biomechai_v5_limb.py`.
* **Certified Benchmark Results (115 Frozen Held-Out Videos, Strictly Zero Leakage)**:
  - **Top-1 Accuracy**: **`53.38%`** (237 / 444 test clips).
  - **Macro Recall**: **`53.15%`**.
  - **Top-5 Accuracy**: **`91.22%`** (405 / 444 test clips).
  - **Squat Performance**: Surged from 20.55% to **`53.42%`** (+160% relative gain) because the connected thigh and shank vectors explicitly preserve knee flexion angle and femur orientation throughout the movement.

#### Comprehensive Per-Class Performance Breakdown

| Exercise Movement | Test Sample Count | Correct Predictions | Per-Class Accuracy | Primary Biomechanical Distinguishing Feature |
| :--- | :---: | :---: | :---: | :--- |
| **Lunge** | 68 | 51 | **`75.00%`** | Asymmetric bilateral shank angles and split-stance pelvis elevation. |
| **Push-Up** | 49 | 33 | **`67.35%`** | Horizontal torso vector, forearm verticality, and elbow sagittal excursion. |
| **Plank** | 64 | 42 | **`65.62%`** | Static isometric horizontal spinal vector and zero joint phase velocity. |
| **Bicep Curl** | 73 | 45 | **`61.64%`** | Upright torso with isolated elbow hinge flexion and static humerus vector. |
| **Squat** | 73 | 39 | **`53.42%`** | Bilateral symmetrical femur depression, hip descent, and knee tracking. |
| **High Knees** | 41 | 12 | **`29.27%`** | Rapid alternating hip flexion with ground-impact vibration phases. |
| **Jumping Jack** | 76 | 15 | **`19.74%`** | Coronal plane shoulder abduction and synchronized lateral ankle excursion. |
| **Overall Dataset** | **444** | **237** | **`53.38%`** | **Top-5 Accuracy: `91.22%` (405 / 444 clips)** |

---

## 3. Pretrained Weights Sources & Model Zoo References

All base models were sourced from the official OpenMMLab model repository and fine-tuned under strict academic reproducibility standards:

1. **OpenMMLab MMAction2 Framework**:
   - Official Repository: `https://github.com/open-mmlab/mmaction2`
   - Research Citation: *Revisiting Skeleton-based Action Recognition*, CVPR 2022 (Duan et al.).
2. **Official OpenMMLab Pretrained Checkpoints**:
   - **Champion FineGYM Limb Backbone**:
     `https://download.openmmlab.com/mmaction/v1.0/recognition/posec3d/slowonly_r50_gym/slowonly_r50_8xb16-u48-240e_gym-limb_20220815-2e6e3c5c.pth`
   - FineGYM Keypoint (Dot) Backbone:
     `https://download.openmmlab.com/mmaction/v1.0/recognition/posec3d/slowonly_r50_gym/slowonly_r50_8xb16-u48-240e_gym-keypoint_20220815-2e6e3c5c.pth`
   - NTU-60 Keypoint Backbone:
     `https://download.openmmlab.com/mmaction/v1.0/recognition/posec3d/slowonly_r50_ntu60_xsub/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint_20220815-4e2b027c.pth`
3. **Training Infrastructure**:
   - Training was conducted on Kaggle Cloud Compute utilizing NVIDIA Tesla P100 / T4 GPUs with PyTorch 2.x and CUDA 11.8/12.1.
   - Fine-tuning employed Cosine Annealing learning rate scheduling, Cross-Entropy loss, and 48-frame temporal crop windows.

---

## 4. Code Implementation: The Machine Learning Pipeline

Below is the concrete code architecture illustrating how the model is loaded, how coordinates are converted into spatiotemporal limb volumes, and how real-time inference is executed.

### 4.1 PyTorch Model Initialization & Unpickling Engine

Located in `backend/engine.py`:

```python
import functools
import torch
import numpy as np
from mmengine.config import Config
from mmaction.apis import init_recognizer

class PoseC3DEngine:
    def __init__(self, config_path: str, checkpoint_path: str, device: str = 'cuda'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        
        # CRITICAL SAFEGUARD (PyTorch 2.6+ Compatibility):
        # OpenMMLab checkpoints store metadata requiring arbitrary object unpickling.
        # We override torch.load to enforce weights_only=False safely.
        torch.load = functools.partial(torch.load, weights_only=False)
        
        # Load configuration and weights
        self.cfg = Config.fromfile(config_path)
        self.model = init_recognizer(self.cfg, checkpoint_path, device=self.device)
        self.model.eval()
        
        # 7-Class Production Label Mapping
        self.labels = [
            'Bicep Curl',
            'High Knees',
            'Jumping Jack',
            'Lunge',
            'Plank',
            'Push-Up',
            'Squat'
        ]

    def predict_window(self, limb_heatmaps: torch.Tensor) -> dict:
        """
        Executes a forward pass over a 3D spatiotemporal heatmap tensor.
        Shape: [Batch=1, Channels=1, TemporalFrames=48, Height=56, Width=56]
        """
        with torch.no_grad():
            tensor_in = limb_heatmaps.to(self.device)
            logits = self.model(tensor_in, mode='predict')
            probabilities = torch.softmax(logits[0].pred_score, dim=-1).cpu().numpy()
            
            top1_index = int(np.argmax(probabilities))
            top1_confidence = float(probabilities[top1_index])
            
            # Rank all classes for Top-5 calculation
            ranking = [
                {"exercise": self.labels[i], "confidence": float(probabilities[i])}
                for i in np.argsort(-probabilities)
            ]
            
            return {
                "predicted_exercise": self.labels[top1_index],
                "confidence": top1_confidence,
                "ranking": ranking
            }
```

### 4.2 Mathematical Spatiotemporal Limb Heatmap Rasterization

To convert raw 2D/3D joint coordinates $[x, y]$ into continuous cylindrical limb heatmaps, the system computes the Euclidean distance from every pixel $(u, v)$ in a $56 \times 56$ grid to the line segment connecting joint $A$ and joint $B$:

$$\text{Heatmap}(u, v) = \exp\left( -\frac{\text{dist}\big( (u, v), \overline{AB} \big)^2}{2 \sigma^2} \right), \quad \sigma = 0.6$$

```python
def generate_limb_heatmap(joint_a: tuple, joint_b: tuple, grid_h: int = 56, grid_w: int = 56, sigma: float = 0.6):
    """
    Rasterizes a continuous bone limb cylinder between two joint coordinates in a 2D plane.
    """
    y_coords, x_coords = np.ogrid[:grid_h, :grid_w]
    
    xa, ya = joint_a[0] * grid_w, joint_a[1] * grid_h
    xb, yb = joint_b[0] * grid_w, joint_b[1] * grid_h
    
    # Vector math for distance to line segment
    line_vec = np.array([xb - xa, yb - ya])
    line_len_sq = np.sum(line_vec ** 2)
    
    if line_len_sq == 0:
        dist_sq = (x_coords - xa)**2 + (y_coords - ya)**2
    else:
        # Projection factor t clamped between [0, 1]
        t = ((x_coords - xa) * line_vec[0] + (y_coords - ya) * line_vec[1]) / line_len_sq
        t = np.clip(t, 0.0, 1.0)
        proj_x = xa + t * line_vec[0]
        proj_y = ya + t * line_vec[1]
        dist_sq = (x_coords - proj_x)**2 + (y_coords - proj_y)**2
        
    return np.exp(-dist_sq / (2.0 * (sigma ** 2)))
```

---

## 5. End-to-End System Architecture: How Every Component Connects

The BioMechAI platform combines mobile edge processing with cloud AI inference and unified database synchronization:

```
+----------------------------------------------------------------------------------------------------+
|                                COMPLETE COMPONENT DATAFLOW PIPELINE                                |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ Athlete's Smartphone ]                                                                          |
|       |                                                                                            |
|       +--> Camera Preview (30 FPS)                                                                 |
|       |         |                                                                                  |
|       |         v                                                                                  |
|       +--> ML Kit Pose Detector (33 3D Keypoints)                                                  |
|       |         |                                                                                  |
|       |         v                                                                                  |
|       +--> Dynamic Sliding Buffer (30 - 48 Frames)                                                 |
|       |         |                                                                                  |
|       |         +--------[ Normal Mode: Over Cloud Tunnel ]--------+                              |
|       |         |                                                  |                              |
|       |         |                                                  v                              |
|       |         |                              [ ngrok Cloud Tunnel Forwarder ]                    |
|       |         |                              (persevere-kindred-tasty.ngrok-free.dev)            |
|       |         |                                                  |                              |
|       |         |                                                  v                              |
|       |         |                              [ FastAPI PyTorch Backend ]                        |
|       |         |                              - PoseC3D v5 Limb Classifier                        |
|       |         |                              - Deterministic Biomechanical Kinematics            |
|       |         |                                                  |                              |
|       |         |                                                  v                              |
|       |         +<-------[ Real-Time Telemetry & Alerts ]----------+                              |
|       |         |                                                                                  |
|       |         v (Network Interruption / Offline Mode)                                            |
|       +--> [ Edge-Cloud Hybrid Fallback Engine ]                                                   |
|                 - Turns Skeleton Crimson Red (#F85149)                                             |
|                 - Activates Local FormValidationService                                            |
|                 - Speaks Local Audio Warnings aloud via flutter_tts                                |
|                 |                                                                                  |
|                 v (Workout Finished)                                                               |
|       +--> [ Atomic Firestore Batch Upload ] (All blocks & 42 reps saved in <300ms)                |
|                 |                                                                                  |
|                 +--------------------------------------------------+                              |
|                                                                    |                              |
|                                                                    v                              |
|                                                [ Cloud Firestore Database ]                        |
|                                                (Project: biomechai-fitness)                        |
|                                                                    |                              |
|                                                                    v                              |
|                                                [ Coach Web Dashboard Portal ]                      |
|                                                - Live Sessions & Attendance Review                |
|                                                - Granular Multi-Exercise Breakdown Tables          |
|                                                - Direct Coach-Athlete Feedback Messenger           |
|                                                - Vector Assessment PDF Generation (jsPDF)          |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

### Component 1: Mobile On-Device Vision Engine (Flutter Client)

* **Camera Pipeline**: Captures video frames using `camera: ^0.11.0` in `ImageFormatGroup.nv21` on Android.
* **Buffer Management**: In `lib/services/pose_detection_service.dart`, multi-plane camera streams are serialized into a single memory block using Flutter's `WriteBuffer` to prevent CPU bottlenecks and maintain **steady 30 FPS processing**.
* **Keypoint Extraction**: Google ML Kit Pose Detection generates 33 keypoints with normalized coordinates $(x, y, z)$ and visibility scores.

---

### Component 2: Permanent Cloud Tunnel Architecture

* **The Problem**: Deep learning inference requires powerful GPU acceleration. However, athletes in gyms cannot connect to a local server IP (`192.168.x.x`), and standard cloud hosting services paywall GPU compute.
* **The Permanent Solution**:
  - The PyTorch FastAPI backend runs locally on port `8000`.
  - A startup script (`run_cloud_server.bat`) launches a dedicated, permanent cloud tunnel via **ngrok** bound to the static domain:
    `https://persevere-kindred-tasty.ngrok-free.dev`
  - The mobile app includes the header `'ngrok-skip-browser-warning': 'true'` on all HTTP requests to bypass free-tier interstitial pages automatically.
  - The dynamic configuration in `lib/services/server_config.dart` allows athletes to toggle between the permanent cloud tunnel and local offline Wi-Fi with a single tap.

---

### Component 3: Dual API Architecture (REST & WebSockets)

The FastAPI server (`backend/main.py`) exposes two distinct communication channels:

1. **REST Classification Endpoint (`POST /classify`)**:
   - Used for buffered exercise recognition.
   - Accepts a 48-frame sliding window of pose coordinates.
   - Returns predicted exercise, confidence score, and complete Top-5 probability distribution.
2. **WebSocket Real-Time Telemetry (`WebSocket /ws/stream`)**:
   - Operates full-duplex at 30 FPS.
   - Streams raw pose landmarks from phone to backend.
   - Returns instant joint angles, rep phase updates, and clinical injury warnings back to the mobile HUD within 20 milliseconds.

---

### Component 4: Edge-Cloud Hybrid Kinematics with Zero-Fail Offline Fallback

A critical production feature introduced in **BioMechAI v2.9**:
* **The Philosophy**: An athlete lifting heavy weights must never lose safety feedback due to a fluctuating internet connection.
* **The Implementation**:
  - If the cloud tunnel drops or network latency exceeds 800ms, the mobile app does not freeze or show an error screen.
  - Instead, the on-device `FormValidationService` immediately engages as an autonomous local fallback.
  - The on-screen skeleton instantaneously turns **Crimson Red (`#F85149`)**, visual HUD alert cards appear, and the local text-to-speech engine speaks injury prevention warnings aloud with **Priority 1 preemption**.
  - When connection is restored, the system seamlessly transitions back to cloud-assisted kinematics.

---

### Component 5: Closed 4-Stage Rep Counting State Machine (Module 4)

Repetition counting avoids naive threshold counting, which causes double-counting when athletes pause or jitter at the bottom of a rep. The system implements a **Closed 4-Stage Finite State Machine (FSM)**:

```
[ UPRIGHT / EXTENDED ] 
         |
         | Knee / Elbow flexion begins
         v
  [ DESCENDING ] 
         |
         | Sagittal depth passes target threshold (e.g., Squat knee < 100 deg)
         v
    [ BOTTOM ]  <--- Form faults inspected here (e.g., knee valgus, elbow flare)
         |
         | Upward concentric drive begins
         v
  [ ASCENDING ] 
         |
         | Joint returns to fully locked extension (e.g., knee > 165 deg)
         v
  [ COMPLETED ] ---> Rep Count += 1, Form Score Logged, Reset to UPRIGHT
```

* **Specialized Isometric Plank Hold Timer**:
  For planks, repetition counting switches to an isometric hold timer. The timer increments only while the athlete maintains a valid lumbar-hip alignment (150°–195°). If hip sag or piking occurs, the timer pauses and warns the athlete.

---

### Component 6: Clinical Injury Prediction Matrix (Modules 5 & 7)

BioMechAI integrates clinical biomechanical research into deterministic physical safety checks across all 7 supported exercises:

| Exercise | Primary Biomechanical Joint Check | Clinical Angle Threshold | Clinical Risk Identified | Academic / Medical Literature Reference |
| :--- | :--- | :---: | :--- | :--- |
| **Squat** | Frontal Plane Projection Angle (FPPA) | $\text{Angle} < 165.0^\circ$ | **Dynamic Knee Valgus** $\rightarrow$ High risk of ACL tear and patellofemoral pain. | Munro et al. (2012), *Journal of Sports Sciences* |
| **Lunge** | Front Knee Lateral Deviation | $\text{Angle} < 165.0^\circ$ | **Unilateral Knee Valgus** $\rightarrow$ Meniscal shear and collateral ligament strain. | Hewett et al. (2005), *Am. J. Sports Med.* |
| **Push-Up** | Gluteal-Spine Plane Alignment | Sag $> 10\%$ below line | **Lumbar Sag** $\rightarrow$ Compressive shear on lower lumbar vertebrae (L4-S1). | McGill (2010), *Core Stability Biomechanics* |
| **Push-Up** | Humerus-Torso Angle (Flaring) | $\text{Angle} > 65.0^\circ$ | **Elbow Flare** $\rightarrow$ Subacromial shoulder impingement & rotator cuff tear. | Schoenfeld et al. (2014), *JSCR* |
| **Plank** | Shoulder-Hip-Ankle Collinearity | $\text{Angle} < 162.0^\circ$ | **Lumbar Hyperextension** $\rightarrow$ Facet joint loading and anterior pelvic tilt. | McGill (2010), *Designing Back Exercise* |
| **Bicep Curl** | Humerus Sagittal Drift | $\text{Drift} > 30.0^\circ$ | **Anterior Shoulder Momentum Drift** $\rightarrow$ Deltoid strain and biceps tendonitis. | Lehman (2005), *J. Manipulative Physiol. Ther.* |
| **Bicep Curl** | Torso Backward Lean | $\text{Lean} > 20.0^\circ$ | **Lumbar Extension Swing** $\rightarrow$ Acute lower back hyperextension strain. | Behm et al. (2005), *Applied Physiology* |
| **High Knees** | Torso Sagittal Pitch | $\text{Pitch} > 15.0^\circ$ | **Excessive Forward Lean** $\rightarrow$ Compensatory spinal shear and hip flexor fatigue. | Schache et al. (2011), *Medicine & Science in Sports* |
| **Jumping Jack** | Spine Coronal Lateral Flexion | $\text{Tilt} > 12.0^\circ$ | **Asymmetric Lateral Trunk Sway** $\rightarrow$ Uneven spinal disc compression and ankle rolling. | Nordin & Frankel (2001), *Basic Biomechanics* |

---

### Component 7: Monocular Anthropometry Scanner (Module 6)

* **The Scientific Challenge**: A single 2D camera cannot determine physical real-world size in centimeters because an object closer to the lens appears larger (the classic *Scale Ambiguity Problem*).
* **The Monocular Photogrammetry Solution**:
  The system uses the athlete's confirmed standing height as a physical calibration anchor:
  $$\text{Scale Factor } (\text{cm/px}) = \frac{\text{Athlete Entered Height (cm)}}{\text{Distance from Crown/Nose to Ankle (px)}}$$
  Once the scale factor is established, the real-world Euclidean distances between anatomical levers are computed:
  - **Biacromial Shoulder Width**: Left Acromion $\leftrightarrow$ Right Acromion
  - **Bi-iliac Hip Width**: Left Anterior Superior Iliac Spine $\leftrightarrow$ Right ASIS
  - **Suprasternal-Hip Torso Length**: Clavicle Center $\leftrightarrow$ Mid-Hip Center
  - **Arm Span**: Left Wrist $\leftrightarrow$ Right Wrist with arms extended
* **Smart Distance-Guiding State Machine**:
  To ensure accuracy, the camera guides the athlete into an ideal standing frame:
  - Too far ($< 0.55$ of frame height): *"Move closer — you're too far away!"*
  - Too close ($> 0.92$ of frame height): *"Step back — you're too close!"*
  - Green Target Zone ($0.65 - 0.85$ of frame height): *"Perfect! Hold still."* (Initiates a 3-second hold countdown and captures pose without shutter lag).
* **Cross-Platform Assessment PDF Engine**:
  Generates multi-page vector clinical PDF reports (`BioMechAI_Assessment_<Name>.pdf`) complete with vital health stats, photogrammetric lever measurements, and granular exercise rep breakdown tables.

---

### Component 8: Edge-Triggered Audio Voice Coaching (Module 8)

* **Engine**: Native on-device Text-To-Speech (`flutter_tts`).
* **Debouncing & Priority Queue**:
  To prevent "chatter fatigue" during demanding workouts, the voice engine enforces intelligent cooldowns:
  - Form Fault Warnings: Minimum 3.5-second cooldown between consecutive corrective cues.
  - Recovery Praise: Minimum 5.0-second delay before praising corrected posture.
  - Preemption: Emergency injury warnings (e.g., severe knee valgus) immediately preempt standard cadence rep counts.

---

### Component 9: Trainer Web Portal & Cloud Firestore Architecture (Module 9)

* **Unified Database**: Both the mobile app and web dashboard connect to Google Cloud Firestore under the project **`biomechai-fitness`**.
* **Atomic Batch Uploads (`saveWorkoutSessionAtomic`)**:
  When an athlete completes a workout, all exercise summary blocks and individual rep records are committed simultaneously using a single `_firestore.batch()` call. This guarantees that all data uploads in **under 300 milliseconds**, completely eliminating dropped reps even if the user exits the app immediately.
* **Two-Way Coach-Athlete Pairing**:
  - Coaches invite athletes by email via the web portal.
  - The athlete receives an invitation card on both mobile and web and retains full sovereignty to **[Accept]** or **[Decline]**.
  - Athlete data is strictly isolated; coaches can only view athletes who have explicitly accepted their invitation.
  - Either party can disconnect at any time, returning the athlete to independent self-guided training.
* **Granular Multi-Exercise Visualization**:
  The dashboard renders complete exercise breakdowns with neon cyber checkmark/cross status badges, collapsible exercise cards, and rep-by-rep kinematic fault annotations.

---

## 6. Verification, Deployment & Repository Topography

### 6.1 Production Hosting Status
- **Coach Web Dashboard**: Deployed and live on Firebase Hosting at:  
  `https://biomechai-fitness.web.app`
- **Permanent Cloud Tunnel**: Active and live at:  
  `https://persevere-kindred-tasty.ngrok-free.dev`

### 6.2 Version Control & Source Repositories
The project is maintained across two production Git repositories:

1. **AI Models, Backend & Checkpoints**:
   - Path: `d:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model`
   - Remote: `https://github.com/abdullahej5411/biomechai_model.git`
   - Active Branch: `main`
2. **Flutter Mobile Application & React Web Dashboard**:
   - Path: `d:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_flutter_latest`
   - Remote: `https://github.com/abdullahej5411/BioMechAI.git`
   - Active Branch: `master`

### 6.3 APK Sequential Release Standard
All mobile builds adhere to strict semantic sequential versioning:
- **`BioMechAI_v3.1_FeedbackBadgeAndNavigation.apk`** (Current Baseline): Includes real-time unread coach badge, direct session navigation, atomic batch uploads, edge-cloud hybrid fallback, smart distance-guiding body scanner, and permanent cloud tunnel integration.
- Next Release Tag: `BioMechAI_v3.2_<FeatureTag>.apk`.

---

## 7. Conclusion & Defense Summary

The BioMechAI system demonstrates an end-to-end fusion of advanced spatiotemporal 3D deep learning, deterministic biomechanical physics, and edge-cloud systems engineering. By moving from disconnected keypoint dots to continuous 3D limb heatmaps, the system solved critical classification blind spots, while its edge-cloud hybrid architecture ensures continuous, real-time clinical safety monitoring regardless of network conditions. Every module has been implemented, validated, and deployed to production for final FYP-II defense.
