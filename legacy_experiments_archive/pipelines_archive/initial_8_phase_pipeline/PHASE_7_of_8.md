# BioMechAI New Video Collection — PHASE 7 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 8's instructions separately after reviewing your Phase 7 output.**

## Context (read only what you need — do not act on anything beyond THIS phase)

This repo already went through a data cleanup pass; see `model_training/cleanup_v2/` if
present (read its `REPORT.md` first, if it exists, to know the current accepted dataset).
That pass found honest accuracy (via leave-one-video-out cross-validation) was ~35%, because
each exercise had only 4-8 genuinely distinct source videos after removing duplicates.

**Goal of the overall task (spanning multiple phases, most of which you do NOT have yet):**
collect new source videos per exercise, verify each is genuinely new, extract landmarks,
filter low-quality clips, merge into the dataset, and re-run the honest evaluation.

**You are being given this task ONE PHASE AT A TIME, on purpose.** You will only receive the
next phase's instructions after the user has reviewed this phase's output. Do not attempt to
infer, plan for, or begin work on later phases — you don't have their exact requirements yet,
and guessing at them risks doing something the user didn't ask for.

**Prerequisite: Phase 6's merged feature matrix must exist. If not, stop and tell the user
Phase 6 needs to be run first.**

**The prior cleanup task's honest LOVO-CV accuracy was 35.71% overall, with lunge at 0% F1
across all folds. This phase re-runs that same evaluation on the merged (existing + new)
dataset — its whole purpose is to check whether the added data actually moved this number.**

---

## Your task for THIS phase only: re-run the honest evaluation on the merged dataset

1. **Minimum-viable-class-size check**: flag any exercise still under 4 unique videos in the
   merged dataset.
2. **Leave-one-video-out cross-validation (LOVO-CV)** over every video in the merged dataset,
   same RandomForest hyperparameters as before (200 trees, max_depth=15, min_samples_leaf=2,
   random_state=42):

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

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

3. **Train the final deployable model** on all merged clips (no held-out video), same
   hyperparameters.

**Do not save final artifacts or write the report file in this phase — that's Phase 8. Only
evaluate and report the numbers here.**

## Required output format (then stop)

- New overall LOVO-CV accuracy vs. the old 35.71%, side by side.
- Per-class precision/recall/F1, old vs. new, side by side — explicit statement on whether
  lunge improved from 0%, stayed at 0%, or is still statistically unreliable.
- Full confusion matrix for the new evaluation.
- Nothing else. Stop after this.
