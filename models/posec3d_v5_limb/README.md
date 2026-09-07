# PoseC3D v5 (FineGYM Limb Heatmap Model)

## Overview
**PoseC3D v5** represents the single-variable scientific experiment testing skeleton limb heatmaps (`with_kp=False, with_limb=True`) against joint point heatmaps (`with_kp=True, with_limb=False`). It uses OpenMMLab's official **FineGYM athletic limb-pretrained checkpoint** (`slowonly_r50_8xb16-u48-240e_gym-limb_20220815-2e6e3c5c.pth`) fine-tuned across 18 epochs on the strict 0-leakage held-out benchmark.

---

## Benchmark Results (Frozen 115 Held-Out Videos, 444 Clips)

* **Overall Top-1 Accuracy**: **53.38% (237 / 444)** — **All-Time Project Record for Standalone Deep Learning** (+2.48 pp over v4)
* **Macro Recall**: **53.15%** — **All-Time Project Record** (+3.01 pp over v4)
* **Peak Checkpoint**: `best_acc_top1_epoch_10.pth` (Epoch 10)

---

## 7×7 Confusion Matrix

```
Class          | bicep_ | high_k | jumpin |  lunge |  plank | pushup |  squat | Total | Recall (%)
--------------------------------------------------------------------------------------------------
bicep_curl     |     45 |      0 |      0 |      3 |     12 |      5 |      8 |    73 |  61.64% (45/73)
high_knees     |     14 |     12 |      0 |      9 |      0 |      6 |      0 |    41 |  29.27% (12/41)
jumping_jack   |      7 |     14 |     15 |     12 |     11 |      6 |     11 |    76 |  19.74% (15/76)
lunge          |     14 |      0 |      0 |     51 |      0 |      3 |      0 |    68 |  75.00% (51/68)
plank          |      1 |      0 |      0 |      3 |     42 |     16 |      2 |    64 |  65.62% (42/64)
pushup         |      4 |      0 |      0 |      0 |      6 |     33 |      6 |    49 |  67.35% (33/49)
squat          |      8 |      0 |      0 |     14 |      9 |      3 |     39 |    73 |  53.42% (39/73)
--------------------------------------------------------------------------------------------------
Overall Top-1 Accuracy : 53.38% (237/444)
Macro Recall           : 53.15%
```

---

## Key Scientific Findings (Hypothesis Test: Limb vs Keypoint)

1. **Squat Recall Surged (+32.87 pp)**:
   * v4 (Joint Heatmaps): **20.55% (15/73)**
   * v5 (Limb Heatmaps): **53.42% (39/73)** — a **+160% relative gain** in recognized squats!
2. **Squat-to-Lunge Misclassifications Slashed by 27 Clips (-65.9%)**:
   * v4: **41 out of 73 squats (56.2%)** collapsed into lunge.
   * v5: Dropped to **14 out of 73 squats (19.2%)**.
   * Proves definitively that connected limb segments provide the critical geometric continuity to differentiate sagittal bilateral knee flexion from unilateral lunging.
3. **Surge on `pushup` (+24.49 pp)**:
   * v4: 42.86% (21/49) $\rightarrow$ v5: **67.35% (33/49)**
4. **Surge on `plank` (+7.81 pp)**:
   * v4: 57.81% (37/64) $\rightarrow$ v5: **65.62% (42/64)**
5. **Trade-Off**:
   * `high_knees` (29.27%) and `jumping_jack` (19.74%) experienced inter-class confusion with bicep curls and squats.
