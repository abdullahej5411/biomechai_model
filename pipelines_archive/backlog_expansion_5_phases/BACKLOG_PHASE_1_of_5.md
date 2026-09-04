# BioMechAI Backlog Extraction — PHASE 1 of 5 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 2's instructions separately after reviewing your Phase 1 output.**

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

---

## Your task for THIS phase only: lock the exclusion set, then deduplicate the clean pool internally

### Step 1 — Fresh-recompute the verified numbers

Re-derive, from the real files on disk right now (do not trust the numbers stated in the
context above — recompute them):
- Total files in `data/raw_videos/` (by extension: `.mp4` vs `.part` vs other)
- Per-exercise: videos with landmarks already extracted (baseline) vs. without (backlog)
- Per-exercise: backlog files under 500KB
- Per-exercise: backlog files that are confirmed (full-file MD5, not just size) duplicates
  of a baseline video
- The union of those two exclusion categories (accounting for overlap, not simple addition)
- The resulting clean candidate pool size

Report this table. If it doesn't match the 933/54/158/1/722 figures in the context above,
that's useful information — report the real numbers you found, not the expected ones.

### Step 2 — Deduplicate the clean pool against itself

The clean candidate pool has only been checked against baseline videos so far — never
against itself. Using the same full-file MD5 method:

```python
import os, hashlib

def md5_full(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()
```

For each exercise, hash every clean candidate video, group by hash, keep the first file in
each group as the representative, log the rest as intra-backlog duplicates.

## Required output format (then stop)

- Step 1's recomputed table (per exercise: total, baseline, backlog, <500KB, baseline-dupes,
  union excluded, clean pool) — confirm or correct the 722 figure.
- Step 2's per-exercise count: clean candidates before internal dedup, intra-backlog
  duplicate groups found, final deduplicated count.
- Save the final list as `backlog_clean_deduped_candidates.json` — confirm the path.
- Nothing else. Stop after this.
