# BioMechAI — PoseC3D v1 (Original Scratch Baseline)

## Model Overview
* **Model Name**: PoseC3D v1 (Original Baseline)
* **Architecture**: SlowOnly-R50 3D ConvNet (`Recognizer3D`, `ResNet3dSlowOnly`, `I3DHead`)
* **Pre-training Base**: None (trained from scratch across 24 epochs)
* **Training Data**: 1,720 training clips across 457 videos
* **Validation Data**: 444 held-out clips across 115 videos (Strict 0 Video Leakage)
* **Input Representation**: 2D skeleton keypoint heatmaps across 48 temporal frames ($17 \times 48 \times 56 \times 56$), `with_kp=True`, `with_limb=False`.
* **Peak Checkpoint**: `best_acc_top1_epoch_18.pth` (converged at Epoch 18).

---

## Checkpoint Files

| Filename | Size | Epoch | Status | Description |
|---|:---:|:---:|:---:|---|
| `best_acc_top1_epoch_18.pth` | **8.05 MB** | **18** | **PEAK CHECKPOINT** | Peak validation checkpoint achieving **49.77% Top-1 Accuracy**, **51.83% Balanced Class Recall**, and **87.39% Top-5 Accuracy** on 444 unseen clips. |
| `epoch_24.pth` | **15.79 MB** | **24** | **FINAL EPOCH** | Final checkpoint after all 24 training epochs, including model weights and SGD optimizer momentum buffers. |
| `posec3d_biomechai.py` | **3.76 KB** | — | **CONFIG** | Complete MMAction2 / MMEngine configuration file. |

---

## Architecture Specifications

- **Model Framework**: OpenMMLab MMAction2 v1.x / MMEngine
- **Backbone**: `ResNet3dSlowOnly` (Depth: 50, Base Channels: 32, Stages: 3, In Channels: 17)
- **Classification Head**: `I3DHead` (In channels: 512, Dropout: 0.5, Classes: 7)
- **Input Heatmap Volume**: $N \times C \times T \times H \times W = 16 \times 17 \times 48 \times 56 \times 56$
- **Optimizer**: SGD (Learning Rate: 0.01, Momentum: 0.9, Weight Decay: 0.0003, Clip Grad: 40.0)

---

## Performance (Strict Video-Disjoint Split: 115 Unseen Videos / 444 Clips)

| Exercise | Precision | Recall | F1-Score | Support | Comparison vs. Random Forest Baseline |
|---|:---:|:---:|:---:|:---:|---|
| **`lunge`** | **0.5281** | **0.6912** | **0.5987** | 68 | +0.03 vs. RF v5 (66.18%) |
| **`pushup`** | **0.5741** | **0.6327** | **0.6019** | 49 | +0.06 vs. RF v5 (57.14%) |
| **`plank`** | **0.4808** | **0.7812** | **0.5952** | 64 | +0.06 vs. RF v5 (71.88%) |
| **`bicep_curl`** | **0.4928** | **0.4658** | **0.4789** | 73 | -0.14 vs. RF v5 (60.27%) |
| **`high_knees`** | **0.3529** | **0.5854** | **0.4404** | 41 | +0.12 vs. RF v5 (46.34%) |
| **`squat`** | **0.4884** | **0.2877** | **0.3621** | 73 | -0.08 vs. RF v5 (36.99%) |
| **`jumping_jack`** | **0.8235** | **0.1842** | **0.3011** | 76 | High Precision (82.4%) |
| **Overall Top-1** | — | — | **49.77%** | 444 | (221 / 444 clips correct) |
| **Balanced Class-Mean** | — | — | **51.83%** | 444 | Class-balanced macro average |
| **Top-5 Accuracy** | — | — | **87.39%** | 444 | True exercise in top guesses 87.4% of the time |
