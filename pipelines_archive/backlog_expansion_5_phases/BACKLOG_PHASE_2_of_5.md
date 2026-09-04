# BioMechAI Backlog Extraction — PHASE 2 of 5 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 3's instructions separately after reviewing your Phase 2 output.**

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

**Prerequisite: `backlog_clean_deduped_candidates.json` from Phase 1 must exist. If it
doesn't, stop and tell the user Phase 1 needs to be run first.**

---

## Your task for THIS phase only: pilot-extract landmarks for squat and lunge only

Extract landmarks only for **squat and lunge** candidates from Phase 1's deduplicated list.
Do not touch the other 5 exercises in this phase.

**Duration-aware clip count** — backlog videos range from ~5 seconds to ~32 minutes. A fixed
5-clips-per-video (the original approach) badly under-samples long videos:

```python
def clip_count_for_duration(duration_seconds):
    # 1 clip per ~90 seconds of footage, minimum 3, maximum 15 per video
    return max(3, min(15, round(duration_seconds / 90)))
```

**Mandatory motion-sanity filter at extraction time**, same method used throughout this
project:

```python
import numpy as np

def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    diffs = np.diff(lm, axis=0)
    disp = np.linalg.norm(diffs, axis=2)
    return disp.mean()
```

Compare each new clip's motion against the **current squat/lunge class median** (compute
this from the existing v3 merged data for these two classes). Discard any clip below 20% of
that median before saving.

**Do not merge, evaluate, or retrain anything in this phase — that's Phase 3. Only extract.**

## Required output format (then stop)

- Per-video: duration, clip count used, clips extracted, clips discarded by motion filter —
  for every squat and lunge candidate processed.
- Per-exercise totals: candidates processed, total clips extracted, total clips discarded.
- Nothing else. Stop after this.
