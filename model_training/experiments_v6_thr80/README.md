# BioMechAI — Experiment v6: PoseC3D Limb Model with Threshold 80

## Objective
This directory hosts the isolated sandbox for **PoseC3D v6 (Threshold 80 Experiment)**.

## Baseline to Beat (Champion Model v5)
- **Top-1 Accuracy**: **`53.38%`** (237/444 clips on 115 frozen held-out videos)
- **Macro Recall**: **`53.15%`**
- **Top-5 Accuracy**: **`91.22%`**
- **Champion Checkpoint**: `models/posec3d_v5_limb/best_acc_top1_epoch_10.pth` (8.33 MB)

## Threshold 80 Parameters in This Experiment
1. **Gradient Clipping Threshold**: `clip_grad(max_norm=80, norm_type=2)` (updated from 40).
2. **Training Schedule Threshold**: `max_epochs=80` (updated from 18).
3. **Dataset Landmark Proposal Threshold**: `box_thr=0.8` (updated from 0.5).
4. **Target Evaluation Criterion**: Checkpoint Top-1 Accuracy on 444 held-out clips must strictly exceed `53.38%` to qualify for promotion.

## File Contents
- `BioMechAI_PoseC3D_v6_Kaggle_Training_Thr80.ipynb`: Self-contained 2-cell Kaggle notebook ready to run on an NVIDIA Tesla GPU.
