# BioMechAI Random Forest Baselines

## Overview
This directory houses the historical and baseline machine learning models developed using tabular geometric landmark features (angles, distances, and velocities) trained with Scikit-Learn `RandomForestClassifier`.

---

## Model Evolution & Performance Summary

| Model Version | Unique Videos | Total Clips | Evaluation Method | Overall Accuracy | Hardest Class (Squat F1) |
|---|:---:|:---:|:---:|:---:|:---:|
| **v1 Baseline** | 42 | 182 | LOVO-CV | **35.71%** | 0.33 (Lunge: 0.00) |
| **v2 Batch 2** | 119 | 495 | LOVO-CV | **56.36%** | 0.34 (Lunge: 0.48) |
| **v3 Expanded** | 119 | 495 | LOVO-CV | **56.36%** | 0.34 |
| **v4 Full Backlog** | 599 | 2,309 | 599-Fold LOVO-CV | **50.76%** | 0.37 (Squat bottleneck confirmed) |
| **v5 Clean Split** | 572 | 2,164 | Video-Disjoint (115 Val) | **52.91%** | **0.38** (Lunge: 0.47, JJ: 0.64) |

---

## File Manifest

| Filename | Type | Size | Description |
|---|:---:|:---:|---|
| `exercise_classifier.pkl` | Model | ~2.0 MB | Earlier baseline Random Forest classifier trained on v2/v3 landmark features. |
| `exercise_classifier_v4.pkl` | Model | ~18.9 MB | 200-tree Random Forest classifier trained on 2,309 clips across 599 unique video folds. |
| `scaler.pkl` / `scaler_v4.pkl` | Preprocessor | ~1.8 KB | `StandardScaler` fitted on geometric feature columns. |
| `label_encoder.pkl` / `label_encoder_v4.pkl` | Preprocessor | ~660 B | `LabelEncoder` mapping 7 exercise strings to integer classes `[0..6]`. |
| `confusion_matrix.png` | Plot | ~66 KB | Visualization of the baseline confusion matrix highlighting the squat vs. lunge confusion. |

---

## Why Deep Learning Was Required (The Motivation for PoseC3D)

Tabular Random Forest models relied on static summary statistics (mean, std, min, max) of joint angles computed over a 90-frame window.
- **Squat vs. Lunge Bottleneck**: In tabular models, 41.7% of squats were persistently misclassified as lunges because joint angles look nearly identical in 2D without temporal stepping dynamics.
- **Pushup vs. Plank**: Prone floor postures have identical min/max joint positions, confusing tree-based splits.
- This plateau motivated the transition to **PoseC3D spatiotemporal 3D convolutions**, which evaluate continuous 48-frame movement volumes and boosted Lunge F1 to **0.60 (+27%)** and Pushup F1 to **0.60 (+11.5%)**.
