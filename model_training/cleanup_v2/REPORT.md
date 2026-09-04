# BioMechAI -- Data Cleanup & Honest Retrain Report

_Generated: 2026-08-30 | scikit-learn 1.9.0_

---

## Phase 0 -- Path Verification

| Path | Status |
|---|---|
| `data/raw_videos/` | Found |
| `data/landmarks/` | Found |
| `extract_landmarks.py` | Found (at repo root) |
| `train_model.py` | Found (at repo root) |
| `models/exercise_classifier.pkl` | Found |
| `models/scaler.pkl` | Found |
| `models/label_encoder.pkl` | Found |
| `server/server.py` | Missing (not present in this workspace) |

> **Structural note:** Instructions reference `model_training/` as a subfolder containing scripts
> and `models/`. In this repo, scripts live at the repo root and `models/` is also at the root.
> All phases used the actual paths found.
>
> **Regarding `server/server.py`:** This `biomechai_model/` directory is a standalone model-training
> workspace. The `server.py` (which will serve the trained model) lives in the main Flutter project
> folder and will be updated to reference the `_CLEANED` artifacts during integration — that is a
> future step, explicitly out of scope for this cleanup task (per instructions Section 9).

---

## Phase 1 -- Confirmed Findings

### 1a. Duplicate videos

| Exercise | Duplicate Video ID | Original Video ID |
|---|---|---|
| squat | 05 | 03 |
| squat | 06 | 01 |
| pushup | 02 | 01 |
| pushup | 04 | 03 |
| pushup | 05 | 03 |
| pushup | 07 | 03 |
| jumping_jack | 03 | 01 |
| jumping_jack | 05 | 01 |
| jumping_jack | 07 | 01 |
| jumping_jack | 08 | 04 |
| jumping_jack | 09 | 02 |
| jumping_jack | 10 | 02 |
| bicep_curl | 02 | 01 |
| bicep_curl | 04 | 01 |
| bicep_curl | 05 | 01 |
| bicep_curl | 09 | 01 |
| lunge | 05 | 04 |
| lunge | 06 | 04 |
| lunge | 09 | 04 |
| plank | 02 | 01 |
| plank | 04 | 01 |
| plank | 06 | 03 |
| plank | 07 | 03 |
| plank | 08 | 01 |
| high_knees | 04 | 01 |

**Total duplicates: 25** -- CONFIRMED

### 1b. Corrupted clips

| Exercise | Video | Clip | Reason |
|---|---|---|---|
| squat | 01 | 04 | frozen_identical_frames |
| squat | 02 | 04 | frozen_identical_frames |
| squat | 06 | 04 | frozen_identical_frames |

### 1c. Static / low-motion clips

| Exercise | Video | Clip | Motion | Class Median |
|---|---|---|---|---|
| squat | 02 | 02 | 0.00043 | 0.00582 |
| squat | 03 | 00 | 0.00023 | 0.00582 |
| squat | 05 | 00 | 0.00023 | 0.00582 |
| squat | 08 | 03 | 0.00106 | 0.00582 |
| squat | 08 | 04 | 0.00032 | 0.00582 |
| squat | 09 | 00 | 0.00014 | 0.00582 |
| squat | 09 | 02 | 0.00014 | 0.00582 |
| squat | 09 | 03 | 0.00107 | 0.00582 |
| squat | 09 | 04 | 0.00052 | 0.00582 |
| pushup | 01 | 02 | 0.00099 | 0.00601 |
| pushup | 02 | 02 | 0.00099 | 0.00601 |
| pushup | 09 | 02 | 0.00098 | 0.00601 |
| jumping_jack | 01 | 00 | 0.00008 | 0.01998 |
| jumping_jack | 03 | 00 | 0.00008 | 0.01998 |
| jumping_jack | 04 | 01 | 0.00015 | 0.01998 |
| jumping_jack | 05 | 00 | 0.00008 | 0.01998 |
| jumping_jack | 07 | 00 | 0.00008 | 0.01998 |
| jumping_jack | 08 | 01 | 0.00015 | 0.01998 |
| bicep_curl | 06 | 00 | 0.00195 | 0.01051 |
| bicep_curl | 10 | 01 | 0.00078 | 0.01051 |
| lunge | 02 | 03 | 0.00106 | 0.00787 |
| lunge | 02 | 04 | 0.00023 | 0.00787 |
| lunge | 10 | 00 | 0.00084 | 0.00787 |
| plank | 01 | 02 | 0.00055 | 0.00311 |
| plank | 02 | 02 | 0.00055 | 0.00311 |
| plank | 03 | 03 | 0.00034 | 0.00311 |
| plank | 04 | 02 | 0.00055 | 0.00311 |
| plank | 05 | 02 | 0.00049 | 0.00311 |
| plank | 05 | 04 | 0.00045 | 0.00311 |
| plank | 06 | 03 | 0.00034 | 0.00311 |
| plank | 07 | 03 | 0.00034 | 0.00311 |
| plank | 08 | 02 | 0.00055 | 0.00311 |
| high_knees | 02 | 01 | 0.00104 | 0.00864 |
| high_knees | 02 | 02 | 0.00108 | 0.00864 |
| high_knees | 08 | 00 | 0.00010 | 0.00864 |
| high_knees | 08 | 02 | 0.00148 | 0.00864 |
| high_knees | 10 | 00 | 0.00007 | 0.00864 |

### 1d. Current (leaky) baseline accuracy

**82.09%** -- reproduced by applying the original clip-level `train_test_split`
(`test_size=0.2, random_state=42, stratify=y`) on all 335 raw clips.
This number is **inflated** because clips from the same source video appear in both
training and test sets, allowing the classifier to memorize inter-clip patterns from
the same recording.

---

## Phase 2 -- Data Cleanup Steps

| Step | Before | After | Removed |
|---|---|---|---|
| 2a -- Duplicate videos | 335 clips | 210 clips | 125 clips |
| 2b -- Corrupted clips  | 210 clips | 208 clips | 2 clips |
| 2c -- Static clips     | 208 clips | 182 clips | 26 clips |

### Surviving clips per exercise

| Exercise | Surviving Clips | Unique Videos | Sufficient? |
|---|---|---|---|
| squat | 30 | 8 | OK |
| pushup | 28 | 6 | OK |
| jumping_jack | 18 | 4 | OK |
| bicep_curl | 28 | 6 | OK |
| lunge | 22 | 5 | OK |
| plank | 21 | 5 | OK |
| high_knees | 35 | 8 | OK |

---

## Phase 3 -- Minimum Viable Class Size

| Exercise | Unique Videos | Status |
|---|---|---|
| squat | 8 | SUFFICIENT (8 unique videos) |
| pushup | 6 | SUFFICIENT (6 unique videos) |
| jumping_jack | 4 | SUFFICIENT (4 unique videos) |
| bicep_curl | 6 | SUFFICIENT (6 unique videos) |
| lunge | 5 | SUFFICIENT (5 unique videos) |
| plank | 5 | SUFFICIENT (5 unique videos) |
| high_knees | 8 | SUFFICIENT (8 unique videos) |

---

## Phase 4 -- Honest Evaluation

### Leaky Baseline (Phase 1d) vs. LOVO-CV

| Metric | Value |
|---|---|
| Leaky clip-split accuracy | **82.09%** |
| Honest LOVO-CV accuracy | **35.71%** |
| Secondary video-grouped 80/20 | **32.43%** |

### LOVO-CV Confusion Matrix

| True \ Pred | bicep_curl | high_knees | jumping_jack | lunge | plank | pushup | squat |
|---|---|---|---|---|---|---|---|
| **bicep_curl** | 9 | 10 | 1 | 1 | 0 | 4 | 3 |
| **high_knees** | 6 | 17 | 3 | 7 | 0 | 1 | 1 |
| **jumping_jack** | 0 | 1 | 12 | 0 | 1 | 0 | 4 |
| **lunge** | 2 | 7 | 1 | 0 | 0 | 9 | 3 |
| **plank** | 2 | 2 | 1 | 1 | 7 | 5 | 3 |
| **pushup** | 4 | 1 | 2 | 3 | 5 | 11 | 2 |
| **squat** | 3 | 2 | 6 | 4 | 3 | 3 | 9 |

### LOVO-CV Classification Report

```
              precision    recall  f1-score   support

  bicep_curl       0.35      0.32      0.33        28
  high_knees       0.42      0.49      0.45        35
jumping_jack       0.46      0.67      0.55        18
       lunge       0.00      0.00      0.00        22
       plank       0.44      0.33      0.38        21
      pushup       0.33      0.39      0.36        28
       squat       0.36      0.30      0.33        30

    accuracy                           0.36       182
   macro avg       0.34      0.36      0.34       182
weighted avg       0.34      0.36      0.35       182

```

### Leaky Baseline Confusion Matrix (for reference)

| True \ Pred | bicep_curl | high_knees | jumping_jack | lunge | plank | pushup | squat |
|---|---|---|---|---|---|---|---|
| **bicep_curl** | 10 | 0 | 0 | 0 | 0 | 0 | 0 |
| **high_knees** | 2 | 5 | 1 | 0 | 0 | 0 | 1 |
| **jumping_jack** | 0 | 0 | 10 | 0 | 0 | 0 | 0 |
| **lunge** | 1 | 0 | 0 | 6 | 0 | 1 | 0 |
| **plank** | 1 | 0 | 0 | 0 | 9 | 0 | 0 |
| **pushup** | 0 | 0 | 0 | 0 | 0 | 10 | 0 |
| **squat** | 1 | 0 | 2 | 0 | 1 | 1 | 5 |

---

## Phase 5 -- Final Model

Trained on all **182 surviving clips** (no held-out data).
Honest accuracy estimate = LOVO-CV result above.
Artifacts saved with `_CLEANED` suffix in `model_training/cleanup_v2/`.

scikit-learn version used for `_CLEANED.pkl` artifacts: **1.9.0**

---

## Section 7 -- Optional Preventive Measures (Not Implemented)

- [ ] Motion filter added to `extract_landmarks.py` at extraction time
- [ ] Duplicate-download check in `download_videos.py`

These were not implemented in this cleanup pass but are flagged for future work.

---

## Section 8 -- scikit-learn Version Note

The `_CLEANED.pkl` artifacts were produced with **scikit-learn 1.9.0**.
If the version that produced the original `models/*.pkl` differs, loading those files
may produce `InconsistentVersionWarning`.

---

## Plain-Language Usability Verdict

The classifier's honest LOVO-CV accuracy is 35.7%, compared to the inflated leaky baseline of 82.1%. The accuracy drop confirms that the original evaluation suffered from data leakage (clips from the same video in both train and test). The current data volume is borderline; collecting more diverse source videos per class is strongly recommended before production deployment.

---

_All cleanup artifacts saved to `model_training/cleanup_v2/`. Original `data/` and `models/` directories are untouched._
