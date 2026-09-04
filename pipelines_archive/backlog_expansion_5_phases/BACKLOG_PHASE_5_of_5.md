# BioMechAI Backlog Extraction — PHASE 5 of 5 (final phase)

**Do only what is described below, then stop — this is the last phase of this task.**

## Context (read only what you need — do not act on anything beyond THIS phase)

This is the BioMechAI exercise classifier (7 classes: squat, pushup, jumping_jack,
bicep_curl, lunge, plank, high_knees). Two evaluation rounds are already complete and
verified:
- **v2**: honest LOVO-CV accuracy 35.71% (cleaned original 67-video dataset, 42 unique
  videos after removing 25 duplicates)
- **v3**: honest LOVO-CV accuracy 56.36% (after adding 78 new Batch 2 videos, 119 unique
  videos total). Lunge went from 0.00 F1 to 0.48 F1. Squat barely moved: 0.33 to 0.34 F1.

Separately, `data/raw_videos/` was found to contain 1,000 total video files (not just the 67
already processed) — a large unprocessed backlog. Verified via full-file MD5 hashing:
- 54 files are corrupted/under 500KB
- 158 files are confirmed byte-identical duplicates of already-processed baseline videos
- 1 file overlaps both categories
- **Verified clean candidate pool: 722 videos** (933 backlog − 211 union of exclusions)

This 722 has NOT yet been checked for duplicates among themselves (only against baseline).

**Why squat and lunge get piloted first, not the full 722 at once:** lunge improved a lot
from more data (v2→v3); squat barely moved despite also getting more data. Testing squat and
lunge again, alone, tells you whether squat's problem is genuinely "needs more data" or
something else (feature engineering, camera angle, confusion with a specific class) that more
video volume won't fix. This determines whether it's worth the compute to process the
remaining 5 exercises.

## Two rules that apply to every phase, no exceptions

1. **Never present an invented, hypothetical, or illustrative example as if it were real
   script output.** A prior task in this project did this once — a fabricated example that
   turned out to contradict already-verified data. If asked for a real example and none is
   available from output you've actually run, say so explicitly rather than constructing a
   plausible one.
2. **Every number in your output must be traceable to a script's actual printed result.** If
   a number is derived (subtraction, union, percentage), show the inputs it came from.

**You are being given this task ONE PHASE AT A TIME, on purpose.** You will only receive the
next phase's instructions after the user has reviewed this phase's output. Do not attempt to
infer, plan for, or begin work on later phases.

**Prerequisite: Phase 2's and Phase 4's extraction outputs must both exist. If either is
missing, stop and tell the user which earlier phase needs to be run first.**

---

## Your task for THIS phase only: full merge, evaluation, and final report

1. Merge all new clips (squat/lunge from Phase 2 + the remaining 5 exercises from Phase 4)
   into the v3 merged dataset to form v4.
2. Minimum-viable-class-size check (flag anything under 4 unique videos — should not trigger
   at this scale, but check anyway).
3. Full 7-class leave-one-video-out cross-validation, same hyperparameters as every prior
   evaluation.
4. Train the final deployable model on all v4 data (no held-out video).

**If any previously-accepted clip (from v2 or v3) gets excluded during this merge** — e.g. a
recomputed combined motion median drops something previously accepted, the way 8 clips were
silently dropped between v2 and v3 without clear disclosure — **explicitly list every such
clip and the reason, in the report. Do not let this happen without disclosure a second
time.**

## Required output format (then stop — task complete)

Save to `model_training/cleanup_v4/`:
- `pilot_lovo_cv_results.json` (from Phase 3, carried forward)
- `full_extraction_log.json` (Phase 4)
- `merged_v4_lovo_cv_results.json` — full confusion matrix, per-class precision/recall/F1
- `exercise_classifier_v4.pkl`, `scaler_v4.pkl`, `label_encoder_v4.pkl`
- `REPORT.md` containing:
  - v2 → v3 → v4 accuracy comparison, overall and per-class, side by side
  - Any clips dropped from earlier versions during this merge, explicitly listed with reason
  - Squat's status specifically — did the Phase 3 pilot signal hold up at full scale
  - A plain-language verdict: is v4 ready to move on from (i.e. time to prioritize the
    roadmap's feature-engineering work and other FYP-II modules), or does the data still
    look like the active bottleneck

Confirm each file was saved, with its path, then present the same v2→v3→v4 comparison table
here as the final summary.
