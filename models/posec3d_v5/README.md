# BioMechAI PoseC3D Fine-Tuned Models (v5)

## Overview
This directory contains the finalized deep learning models for the **BioMechAI PoseC3D Exercise Classifier**, trained and evaluated on the full 2,164-clip v5 dataset.

The architecture is **PoseC3D** (Duan et al., CVPR 2022, arXiv:2104.13586), which utilizes 3D convolutional neural networks (`ResNet3dSlowOnly`) operating over spatiotemporal skeleton heatmaps generated from MediaPipe 33 keypoints (converted to COCO 17 format).

---

## Checkpoint Files

| Filename | Size | Epoch | Status | Description |
|---|:---:|:---:|:---:|---|
| `best_acc_top1_epoch_18.pth` | **8.05 MB** | **18** | **BEST MODEL** | Peak validation checkpoint achieving **49.77% Top-1 Accuracy**, **51.83% Balanced Class Recall**, and **87.39% Top-5 Accuracy** on 444 unseen clips. |
| `epoch_24.pth` | **15.79 MB** | **24** | **FINAL EPOCH** | Final checkpoint after all 24 training epochs, including model weights and SGD optimizer momentum buffers. |
| `posec3d_biomechai.py` | **3.76 KB** | — | **CONFIG** | Complete MMAction2 / MMEngine configuration file specifying model backbone, classification head, dataloaders, and augmentations. |

---

## Architecture Specifications

- **Model Framework**: OpenMMLab MMAction2 v1.x / MMEngine
- **Backbone**: `ResNet3dSlowOnly` (Depth: 50, Base Channels: 32, Stages: 3, In Channels: 17)
- **Pretrained Source**: NTU RGB+D 60 X-Sub Keypoint Checkpoint (`slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint`)
- **Classification Head**: `I3DHead` (In channels: 512, Dropout: 0.5, Classes: 7)
- **Input Heatmap Volume**: $N \times C \times T \times H \times W = 16 \times 17 \times 48 \times 56 \times 56$
- **Optimizer**: SGD (Learning Rate: 0.01, Momentum: 0.9, Weight Decay: 0.0003, Clip Grad: 40.0)
- **Batch Size**: 16 clips per iteration (108 iterations per epoch)

---

## Final Performance (Strict Video-Disjoint Split: 115 Unseen Videos)

Evaluated on **444 validation clips** that were completely held out from training:

| Exercise | Precision | Recall | F1-Score | Support | Comparison vs. Random Forest Baseline |
|---|:---:|:---:|:---:|:---:|---|
| **`lunge`** | **0.5281** | **0.6912** | **0.5987** | 68 | **+0.13 (+27.4% relative gain)** 🚀 |
| **`pushup`** | **0.5741** | **0.6327** | **0.6019** | 49 | **+0.06 (+11.5% relative gain)** 🚀 |
| **`plank`** | **0.4808** | **0.7812** | **0.5952** | 64 | **0.00 (78.1% recall: 50/64 correct)** ✅ |
| **`bicep_curl`** | **0.4928** | **0.4658** | **0.4789** | 73 | -0.03 |
| **`high_knees`** | **0.3529** | **0.5854** | **0.4404** | 41 | -0.10 |
| **`squat`** | **0.4884** | **0.2877** | **0.3621** | 73 | -0.02 |
| **`jumping_jack`** | **0.8235** | **0.1842** | **0.3011** | 76 | High Precision (82.4%) |
| **Overall Top-1** | — | — | **49.77%** | 444 | Random Chance is 14.28% |
| **Balanced Class-Mean** | — | — | **51.83%** | 444 | Outperforms Random Forest class average |
| **Top-5 Accuracy** | — | — | **87.39%** | 444 | True exercise in top guesses 87.4% of the time |

---

## How to Load and Run Inference with PyTorch

```python
import functools, torch
from mmengine.config import Config
from mmengine.runner import Runner

# PyTorch 2.6+ weights_only compatibility patch
_orig_torch_load = torch.load
torch.load = functools.partial(_orig_torch_load, weights_only=False)

# Load configuration
cfg = Config.fromfile("models/posec3d_v5/posec3d_biomechai.py")
cfg.load_from = "models/posec3d_v5/best_acc_top1_epoch_18.pth"
cfg.custom_hooks = []  # Disable Drive sync hooks for offline inference

# Build runner and execute testing
runner = Runner.from_cfg(cfg)
metrics = runner.test()
print("Evaluation Metrics:", metrics)
```
