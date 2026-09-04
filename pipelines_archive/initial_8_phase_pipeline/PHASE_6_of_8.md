# BioMechAI New Video Collection — PHASE 6 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 7's instructions separately after reviewing your Phase 6 output.**

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

**Prerequisite: Phase 5's final accepted-clip list must exist. If not, stop and tell the user
Phase 5 needs to be run first.**

---

## Your task for THIS phase only: merge and rebuild the feature matrix

Combine the accepted new clips (post Phase 5) with the existing cleaned dataset (from
`model_training/cleanup_v2/`, or the equivalent surviving set from Phase 1). Recompute the
50-feature matrix for the **new clips only** (existing clips' features don't need
recomputing) using the exact `extract_features`/`angle` functions already used in
`train_model.py` — do not modify the feature engineering:

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

**Do not evaluate or retrain a final model in this phase — that's Phase 7. Only merge and
compute features.**

## Required output format (then stop)

- Per-exercise table: total clips and total unique videos in the merged dataset (existing +
  new).
- Nothing else. Stop after this.
