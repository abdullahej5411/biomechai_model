# BioMechAI — PoseC3D v4 (FineGYM Pretrained Transfer Learning)

## Model Overview
* **Architecture**: SlowOnly-R50 3D ConvNet (`Recognizer3D`, `ResNet3dSlowOnly`, `I3DHead`)
* **Pre-training Base**: FineGYM Gymnastics Action Recognition (`slowonly_r50_8xb16-u48-240e_gym-keypoint_20220815-da338c58.pth`)
* **Input Representation**: 2D skeleton keypoint heatmaps across 48 temporal frames ($17 \times 48 \times 56 \times 56$), `with_kp=True`, `with_limb=False`.
* **Data Augmentations**: `UniformSampleFrames`, `PoseCompact`, `RandomResizedCrop`, `Flip`, and `RandomRotateKeypoints` (camera tilt synthesis $\pm 12^\circ$, $p=0.5$).
* **Optimization**: SGD with momentum $0.9$, learning rate $0.01$, weight decay $0.0005$, and classifier dropout $0.6$.
* **Peak Checkpoint**: `best_acc_top1_epoch_4.pth` (converged at Epoch 4).

---

## Held-Out Evaluation Benchmark (Strict 0 Video Leakage)
Evaluated strictly on **115 held-out subject videos (444 clips)** with zero subject/video overlap:

* **Top-1 Overall Accuracy**: **50.90%** ($226 / 444$ clips) — *breaks the 50% barrier for standalone PoseC3D!*
* **Balanced Macro Recall**: **50.14%**
* **Evaluation Dump**: `phase4_v4_result.pkl`

### Per-Class Confusion Matrix
```
                 bicep_   high_k   jumpin    lunge    plank   pushup    squat    Total
bicep_curl           49        0        1       10        3        0       10       73
high_knees            4       15        0       20        1        0        1       41
jumping_jack         15        0       31       16        0        8        6       76
lunge                 8        1        0       58        0        1        0       68
plank                11        0        0       16       37        0        0       64
pushup               14        0        0        5        3       21        6       49
squat                 5        0        4       41        4        4       15       73
```

### Authoritative 5-Way Comparison Table
| Exercise | Random Forest v5 | PoseC3D v1 (Scratch) | PoseC3D v2 (Overfit) | PoseC3D v3 (NTU-60) | PoseC3D v4 (FineGYM) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **bicep_curl** | 60.27% | 46.58% | 26.03% | 30.14% | **67.12%** 🚀 *(+37.0% vs v3)* |
| **high_knees** | 46.34% | 58.54% | 43.90% | 53.66% | **36.59%** |
| **jumping_jack**| 52.63% | 18.42% | 39.47% | 44.74% | **40.79%** |
| **lunge** | 66.18% | 69.12% | 76.47% | 60.29% | **85.29%** 🚀 *(All-time peak!)* |
| **plank** | 71.88% | 78.12% | 76.56% | 62.50% | **57.81%** |
| **pushup** | 57.14% | 63.27% | 28.57% | 63.27% | **42.86%** |
| **squat** | 36.99% | 28.77% | 23.29% | 32.88% | **20.55%** |
| **Overall Top-1**| **56.08%** | **49.77%** | **44.82%** | **48.20%** | **50.90%** 🎯 |
| **Macro Recall** | **55.92%** | **51.83%** | **44.90%** | **49.64%** | **50.14%** |

---

## Directory Contents
Place downloaded files directly into this directory:
1. `best_acc_top1_epoch_4.pth` — Trained PyTorch weights (~8.38 MB)
2. `phase4_v4_result.pkl` — Raw evaluation output pickle (~500 KB)
3. `posec3d_biomechai_v4.py` — Complete MMAction2 configuration file
4. `pose_transforms_extra.py` — Custom keypoint rotation transform
