# BioMechAI — Exercise Classifier Data Cleanup & Honest Retrain
### Instructions for an AI coding agent working directly in the project repo

---

## 0. How to work through this document

**Work through the phases below strictly in order. Do not skip ahead to modifying or
retraining anything until the analysis phases are complete and reported.** After finishing
each phase, output a short status summary to the user before moving to the next phase — this
should read as a sequential progress log (Phase 0 done → findings → Phase 1 done → findings →
...), not one final report dumped at the end. If any phase's findings contradict something
stated as fact in this document (e.g. you find no duplicates, or a different duplicate
count), report that plainly and proceed based on what you actually found in the real files —
this document's earlier numbers are from a prior snapshot, not ground truth.

---

## 1. Context

This is the `model_training/` pipeline for BioMechAI, a Flutter fitness app. It trains a
RandomForest classifier on 90-frame pose-landmark clips to recognize 7 exercises: squat,
pushup, jumping_jack, bicep_curl, lunge, plank, high_knees.

**Expected files in the repo:**
- `data/raw_videos/{exercise}/*.mp4` — downloaded source videos (via `download_videos.py`)
- `data/landmarks/{exercise}/{exercise}_{videoid}_clip{00-04}.json` — extracted 90-frame,
  33-landmark pose sequences (via `extract_landmarks.py`), 5 clips evenly time-sliced per video
- `model_training/extract_landmarks.py` — MediaPipe landmark extraction
- `model_training/train_model.py` — builds 50 biomechanical features per clip, trains
  `RandomForestClassifier`
- `model_training/models/exercise_classifier.pkl`, `scaler.pkl`, `label_encoder.pkl` —
  current trained artifacts

**The requirement this work supports:** the current classifier's reported accuracy is
suspected to not be trustworthy (see Section 2). Nothing gets fixed until that suspicion is
actually confirmed against the real files — this is an audit-then-fix task, not a fix-first
task.

**Never delete `data/raw_videos/` or `data/landmarks/`.** Never overwrite
`model_training/models/*.pkl` in place — new artifacts get a `_CLEANED` suffix and go in a
new subfolder. All cleanup works by building an *exclusion list*, not by destructively
modifying source data, so the process stays reversible and auditable.

---

## PHASE 0 — Verify the repo matches what this document expects

Before touching or analyzing anything, check that each file/path listed in Section 1 above
actually exists where expected:

1. Does `data/raw_videos/` exist, with one subfolder per exercise?
2. Does `data/landmarks/` exist, with one subfolder per exercise, containing files matching
   the pattern `{exercise}_{videoid}_clip{00-04}.json`?
3. Do `model_training/extract_landmarks.py`, `model_training/train_model.py`, and
   `model_training/models/{exercise_classifier,scaler,label_encoder}.pkl` exist?
4. Does `server/server.py` exist, and does it reference a different model file (e.g.
   `fitness_model.pkl`) than `model_training/models/exercise_classifier.pkl`?

**If any expected path is missing or named differently:** search the repo for the closest
match (e.g. a differently-cased folder, a moved `model_training/` directory) before
concluding a file doesn't exist at all. If you find it at a different path, use the actual
path for every later phase and note the discrepancy in your Phase 0 summary. If something
genuinely doesn't exist anywhere in the repo, stop and report that explicitly — do not
fabricate or skip the step silently.

**Output of this phase:** a short confirmation of each path (found / found-at-different-path
/ genuinely missing) before proceeding to Phase 1.

---

## PHASE 1 — Analyze only. Do not modify, delete, or retrain anything in this phase.

The goal here is to confirm or refute each suspected problem against the real local data,
using the exact checks below, and report the real numbers. Everything in this phase is
read-only.

### 1a. Check for duplicate source videos

For each exercise, compare every pair of videos using their **raw landmark arrays**:

```python
import re, numpy as np, json, os

def load_video_clips(landmarks_dir, exercise, video_id):
    clips = {}
    for fname in sorted(os.listdir(os.path.join(landmarks_dir, exercise))):
        m = re.match(rf'{exercise}_{video_id}_clip(\d+)\.json', fname)
        if m:
            with open(os.path.join(landmarks_dir, exercise, fname)) as f:
                clips[m.group(1)] = json.load(f)['landmarks']
    return clips

def video_signature(clip_dict):
    parts = [np.round(np.array(clip_dict[c]), 4).flatten() for c in sorted(clip_dict)]
    return tuple(np.concatenate(parts)) if parts else None

# For each exercise: build a signature per video_id. Any two video_ids with an identical
# signature are duplicates -- keep the first, mark the rest as duplicate_of the first.
```

Record, per exercise: total videos found, number of unique signatures, and the exact
duplicate pairs (`video_id -> duplicate_of video_id`).

### 1b. Check for corrupted / extraction-failed clips

```python
def is_corrupted(landmarks):
    lm = np.array(landmarks)
    if np.isnan(lm).any():
        return True, "nan_values"
    if lm.shape[0] < 90:
        return True, "incomplete_frames"
    if np.allclose(lm, lm[0], atol=1e-6):
        return True, "frozen_identical_frames"
    return False, None
```
Run this on every clip. Record the count and filenames of any corrupted clips found, by
reason.

### 1c. Check for static / non-exercise clips

```python
def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    diffs = np.diff(lm, axis=0)
    disp = np.linalg.norm(diffs, axis=2)
    return disp.mean()
```
Compute this for every non-corrupted clip, grouped by exercise. For each exercise, compute
the median motion value, then identify clips below 20% of that median. Record the count and
filenames per exercise, along with each flagged clip's motion value vs. the exercise median.

### 1d. Reproduce the current (suspected-leaky) evaluation, unchanged, as a baseline

Load the existing `models/exercise_classifier.pkl`, `scaler.pkl`, `label_encoder.pkl` as-is.
Run the same clip-level `train_test_split` the current `train_model.py` uses
(`test_size=0.2, random_state=42, stratify=y`) and report the resulting accuracy and
confusion matrix, exactly as the current pipeline would produce it. This is the "before"
number — needed so the later honest number can be compared against it.

### Phase 1 output

Report, before doing anything else:
- Confirmed duplicate video count and list, per exercise (real numbers from the actual repo,
  not the ones referenced elsewhere in this document)
- Confirmed corrupted clip count and list
- Confirmed static-clip count and list
- The reproduced current-pipeline accuracy (the "before" leaky baseline)
- One explicit sentence per suspected problem: **confirmed** or **not confirmed**, with the
  real numbers. If a problem is not confirmed (e.g. no duplicates found), say so plainly and
  do not proceed to "fix" something that isn't there.

**Stop here and present this Phase 1 report as a discrete update before starting Phase 2.**

---

## PHASE 2 — Clean the data (only for problems Phase 1 actually confirmed)

Only act on exclusions Phase 1 actually found. If Phase 1 found zero duplicates, Phase 2's
duplicate-removal step is a no-op — report that and move on, don't invent exclusions.

### Step 2a — Exclude confirmed duplicate videos
Drop every video Phase 1 marked as `duplicate_of` another video, keeping the first-seen copy.

### Step 2b — Exclude confirmed corrupted clips
Drop every clip Phase 1 flagged in 1b.

### Step 2c — Exclude confirmed static clips
Drop every clip Phase 1 flagged in 1c.

### Step 2d — Rebuild the 50-feature matrix from the surviving clips

Use the exact feature engineering already defined in `train_model.py` — do not redesign it,
just re-run it on the surviving (non-excluded) clips:

```python
def angle(lm, a, b, c):
    ba = lm[:, a, :2] - lm[:, b, :2]
    bc = lm[:, c, :2] - lm[:, b, :2]
    cos = np.sum(ba*bc, axis=1) / (
        np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1) + 1e-9)
    return np.degrees(np.arccos(np.clip(cos, -1, 1)))

def extract_features(landmarks):
    lm = np.array(landmarks)
    features = []
    angle_seqs = {
        'knee_l':     angle(lm, 23, 25, 27), 'knee_r':     angle(lm, 24, 26, 28),
        'elbow_l':    angle(lm, 11, 13, 15), 'elbow_r':    angle(lm, 12, 14, 16),
        'hip_l':      angle(lm, 11, 23, 25), 'hip_r':      angle(lm, 12, 24, 26),
        'shoulder_l': angle(lm, 13, 11, 23), 'shoulder_r': angle(lm, 14, 12, 24),
    }
    for seq in angle_seqs.values():
        features.extend([np.mean(seq), np.std(seq), np.min(seq), np.max(seq),
                          np.max(seq) - np.min(seq)])
    for seq in angle_seqs.values():
        features.append(np.mean(np.abs(np.diff(seq))))
    features.append(np.mean(np.abs(angle_seqs['knee_l'] - angle_seqs['knee_r'])))
    features.append(np.mean(np.abs(angle_seqs['shoulder_l'] - angle_seqs['shoulder_r'])))
    return np.array(features)
```
(Joint indices: 11/12=shoulders, 13/14=elbows, 15/16=wrists, 23/24=hips, 25/26=knees,
27/28=ankles — standard MediaPipe Pose landmark indices.)

**Phase 2 output:** confirm how many videos/clips remain per exercise after each exclusion
step, before moving to Phase 3.

---

## PHASE 3 — Minimum-viable-class-size check

Count surviving unique videos per exercise after Phase 2. **If any exercise has fewer than 4
surviving unique videos, flag it prominently** — e.g. "high_knees has only 3 usable videos
after cleanup; any accuracy number for this class is not statistically meaningful." Do not
silently proceed and produce a number that looks precise but isn't.

**Phase 3 output:** list of exercises, each marked sufficient or insufficient, before Phase 4.

---

## PHASE 4 — Evaluate honestly with leave-one-video-out cross-validation (LOVO-CV)

With likely single-digit unique videos per class, a single random 80/20 split is unstable —
which video happens to land in "test" can swing the result by chance. Use LOVO-CV instead:
for each exercise, hold out each unique video in turn as the test set, train on every other
video's clips (across all exercises), predict on the held-out video, and record the result.
Repeat until every video has been the test case exactly once.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

all_video_keys = [(ex, vid) for ex, vids in videos_by_exercise.items() for vid in vids]
fold_results = []

for held_out_ex, held_out_vid in all_video_keys:
    train_clips = [c for c in all_clips
                   if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips  = [c for c in all_clips
                   if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

    X_train = np.array([c['features'] for c in train_clips])
    y_train = np.array([c['exercise'] for c in train_clips])
    X_test  = np.array([c['features'] for c in test_clips])
    y_test  = np.array([c['exercise'] for c in test_clips])

    le = LabelEncoder().fit(y_train)
    scaler = StandardScaler().fit(X_train)
    clf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=2,
                                  random_state=42, n_jobs=-1)
    clf.fit(scaler.transform(X_train), le.transform(y_train))
    preds = le.inverse_transform(clf.predict(scaler.transform(X_test)))

    for true, pred in zip(y_test, preds):
        fold_results.append((held_out_ex, held_out_vid, true, pred))
```

Aggregate `fold_results` into overall accuracy, per-class precision/recall/F1, and a full
confusion matrix. This is the number to report as the honest baseline — compare it directly
against the Phase 1d "before" leaky number.

Also run a single video-level grouped 80/20 split (fixed `random_state=42`, no clip from one
video split across train/test) as a **secondary cross-check** only — report both, headline
with LOVO-CV.

**Phase 4 output:** LOVO-CV accuracy + confusion matrix + per-class metrics, vs. the Phase 1d
baseline, before Phase 5.

---

## PHASE 5 — Train the final deployable model on all cleaned data

LOVO-CV is for evaluation only — none of its per-fold models get saved. Train once more on
**all** surviving cleaned clips (no held-out video), same hyperparameters:

```python
X_all = np.array([c['features'] for c in all_clips])
y_all = np.array([c['exercise'] for c in all_clips])

le_final = LabelEncoder().fit(y_all)
scaler_final = StandardScaler().fit(X_all)
clf_final = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=2,
                                    random_state=42, n_jobs=-1)
clf_final.fit(scaler_final.transform(X_all), le_final.transform(y_all))
```
The LOVO-CV result from Phase 4 is this model's honest accuracy estimate — the final fit
itself has no held-out data left to test on.

---

## PHASE 6 — Save structured outputs and write the report

Save everything in a **new** `model_training/cleanup_v2/` directory — never overwrite
originals:
- `excluded_duplicates.json` — `{exercise, video_id, duplicate_of_video_id}` list
- `excluded_corrupted.json` — `{exercise, video_id, clip, reason}` list
- `excluded_static.json` — `{exercise, video_id, clip, motion_value, exercise_median}` list
- `lovo_cv_results.json` — per-fold results + aggregated confusion matrix + per-class metrics
- `exercise_classifier_CLEANED.pkl`, `scaler_CLEANED.pkl`, `label_encoder_CLEANED.pkl`
- `REPORT.md` containing:
  - Phase 0 path-verification results
  - Phase 1 confirmed/not-confirmed findings with real counts
  - Videos/clips remaining after each exclusion stage, per exercise
  - Any Phase 3 insufficient-data flags
  - Phase 1d "before" accuracy vs. Phase 4 LOVO-CV "after" accuracy, side by side
  - Full confusion matrix and per-class metrics
  - A one-paragraph plain-language verdict: is this classifier usable as-is, or does it
    indicate more/better source video collection is needed — state the reasoning (e.g.
    unique-videos-per-class count), not just the number

---

## 7. Recommended but optional — prevent this from recurring

Not required for Definition of Done, but flag in the report whether you did these:
- Add the Phase 1c motion filter into `extract_landmarks.py` itself, so newly extracted
  clips that fail the motion-sanity check are skipped at extraction time.
- Add a duplicate-download check into `download_videos.py` (hash/fingerprint each download,
  skip if it matches an already-downloaded video for that exercise).

## 8. Note on environment

Check the installed `scikit-learn` version against whatever produced the original
`models/*.pkl` before loading it in Phase 1d — a version mismatch can throw
`InconsistentVersionWarning` and isn't guaranteed safe long-term. Note the version used for
the `_CLEANED.pkl` outputs in the report.

## 9. Explicit pitfalls — do not do these

- **Do not** modify, delete, or retrain anything before Phase 1's analysis is complete and
  reported.
- **Do not** invent or assume exclusions Phase 1 didn't actually find in the real files.
- **Do not** use `train_test_split` on individual clips without grouping by video — this
  reintroduces leakage even after deduplication.
- **Do not** tune the RandomForest hyperparameters to chase a higher number — the goal is
  measurement, not optimization.
- **Do not** report a single 80/20 split's accuracy as the headline number — LOVO-CV is the
  primary result.
- **Do not** skip the Phase 3 class-size check to avoid an awkward result.
- **Do not** delete or overwrite `data/raw_videos/`, `data/landmarks/`, or the original
  `.pkl` files.
- **Do not** attempt to fix the server/model-mismatch issue (Section 1, item 4) in this task
  — out of scope, just note it in the report.

## 10. Definition of done

- Phase 0 through Phase 6 each produced and reported their stated output, in order.
- `model_training/cleanup_v2/REPORT.md` exists with everything listed in Phase 6.
- Retrained artifacts saved alongside (not replacing) the originals.
- The plain-language usability verdict is stated explicitly, with reasoning, not just a
  number.
