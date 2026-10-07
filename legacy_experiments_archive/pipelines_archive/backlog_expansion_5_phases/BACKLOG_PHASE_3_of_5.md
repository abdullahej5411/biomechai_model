# BioMechAI Backlog Extraction — PHASE 3 of 5 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP HARD — this phase ends in a decision point, not just a
checkpoint. Do not begin Phase 4 under any circumstances, even if the result looks clearly
positive. Phase 4 is a large compute commitment and requires the user's explicit go-ahead,
not just the existence of this phase's output.**

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

**Prerequisite: Phase 2's extraction output must exist. If it doesn't, stop and tell the
user Phase 2 needs to be run first.**

---

## Your task for THIS phase only: evaluate whether the pilot moved squat and lunge

1. Merge the new squat/lunge clips from Phase 2 into the existing v3 merged dataset, **for
   these two classes only** — leave the other 5 exercises' data untouched.
2. Rebuild the 50-feature matrix for the new clips only, using the exact `extract_features`
   function already used throughout this project (do not modify it — copy it verbatim from
   `train_model.py` or a prior phase's script).
3. Run leave-one-video-out cross-validation on squat and lunge specifically, same
   RandomForest hyperparameters used in every prior evaluation (200 trees, max_depth=15,
   min_samples_leaf=2, random_state=42).

**Do not touch the other 5 exercises' data or retrain a full 7-class model in this phase —
this is squat/lunge only.**

## Required output format (then stop — this is a decision point)

- Squat: v3 F1 (0.34) vs. new pilot F1 — the actual number, plus the confusion pattern (what
  is squat still being confused with, if anything).
- Lunge: v3 F1 (0.48) vs. new pilot F1.
- One explicit sentence: **did squat's F1 move meaningfully (past roughly 0.45-0.50), or is
  it still flat?** This is the number the user will use to decide whether to authorize
  Phase 4. State it plainly — do not soften a flat result or oversell a marginal one.
- Nothing else. Stop after this and wait for the user's explicit decision on Phase 4.
