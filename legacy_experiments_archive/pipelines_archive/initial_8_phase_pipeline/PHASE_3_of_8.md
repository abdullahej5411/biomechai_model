# BioMechAI New Video Collection — PHASE 3 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 4's instructions separately after reviewing your Phase 3 output.**

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

**Prerequisite: `data/raw_videos_batch2/` from Phase 2 must exist with downloaded videos. If
it doesn't, stop and tell the user Phase 2 needs to be run first.**

---

## Your task for THIS phase only: extract landmarks from the new candidates

Reuse the landmark-extraction logic from `extract_landmarks.py` (same MediaPipe pose
extraction, same 90-frame / 5-clips-per-video approach), applied to
`data/raw_videos_batch2/`. Output to `data/landmarks_batch2/{exercise}/`, same filename
convention as the existing dataset.

**Mandatory motion-sanity filter (not optional this time):** while extracting, compute
overall motion for each candidate clip:

```python
import numpy as np

def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    diffs = np.diff(lm, axis=0)
    disp = np.linalg.norm(diffs, axis=2)
    return disp.mean()
```

Compare against the existing per-exercise motion median (compute this from the current
`data/landmarks/` clips for that exercise). Skip/discard — do not save — any new clip
falling below 20% of that median.

**Do not check for duplicates against the existing dataset in this phase — that's Phase 4.
Only extract and apply the motion filter.**

## Required output format (then stop)

- Per-exercise table: candidate videos processed, clips successfully extracted, clips
  skipped by the motion filter (with reason: below X% of median Y).
- Nothing else. Stop after this.
