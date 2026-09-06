# BioMechAI PoseC3D v3 — Production Champion Model

## Model Overview
* **Model Name**: PoseC3D v3 (Production Champion)
* **Checkpoint File**: `best_acc_top1_epoch_14.pth` (Epoch 14)
* **Architecture**: `ResNet3dSlowOnly` + `I3DHead` (CVPR 2022)
* **Framework**: MMAction2 v1.2.0 / MMEngine 0.10.7 / PyTorch 2.10
* **Pretrained Weights**: NTU RGB+D 60 X-Sub Keypoint Checkpoint
* **Key Innovations**:
  1. **Moderate Classification Regularization**: `dropout_ratio = 0.60` (prevents feature starvation on subtle limb exercises).
  2. **Viewpoint Jitter Augmentation**: `RandomRotateKeypoints` ($\pm 12^\circ$ random 2D rotation) teaches camera-tilt invariance for squats and lunges.
  3. **Moderate Optimizer Weight Decay**: `weight_decay = 0.0005`.
  4. **Optimized Training Ceiling**: Capped at 18 epochs to capture peak generalization (achieved at Epoch 14).

---

## Held-Out Evaluation Performance (115 Videos / 444 Clips)
* **Overall Top-1 Accuracy**: **`48.20%`** (214/444 correct)
* **Balanced Macro Recall**: **`49.64%`**
* **Top-5 Accuracy**: **`91.22%`** (All-time project peak!)

### Per-Class Recall Breakdown
| Exercise | Correct / Support | Recall (%) | Outcome Analysis |
|---|:---:|:---:|---|
| **`pushup`** | 31 / 49 | **63.27%** | Fully restored to project peak (cured v2's 28.57% collapse) |
| **`jumping_jack`** | 34 / 76 | **44.74%** | **All-time deep record** (+26.32 pp over v1's 18.42%) |
| **`high_knees`** | 22 / 41 | **53.66%** | Strong dynamic recognition |
| **`squat`** | 24 / 73 | **32.88%** | **Best deep model score** (+4.11 pp over v1, +9.59 pp over v2) |
| **`bicep_curl`** | 22 / 73 | **30.14%** | Stable baseline |
| **`lunge`** | 41 / 68 | **60.29%** | Solid leg stride tracking |
| **`plank`** | 40 / 64 | **62.50%** | Stable isometric pose detection |

---

## Why PoseC3D v3 Is the Production Champion Over PoseC3D v1
In an end-user fitness app, single-class failures destroy usability. 
* In PoseC3D v1, `jumping_jack` failed over 81% of the time (18.42% recall).
* In PoseC3D v3, `jumping_jack` jumped to **44.74%**, while `pushup` was maintained at **63.27%** and `squat` improved to **32.88%**.
* PoseC3D v3 has **zero catastrophic blind spots** (lowest class is 30.14%).
* Trading only 1.57 pp of average Top-1 accuracy (48.20% vs 49.77%) to eliminate an 18% catastrophic failure mode makes PoseC3D v3 the far superior, safer, and more deployable model for real human users.
