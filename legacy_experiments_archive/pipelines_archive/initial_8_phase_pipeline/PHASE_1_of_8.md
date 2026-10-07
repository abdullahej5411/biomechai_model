# BioMechAI New Video Collection — PHASE 1 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work, even if you can guess what a
reasonable next step would be — the user will give you Phase 2's instructions separately
after reviewing your Phase 1 output.**

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

---

## Your task for THIS phase only: establish the current accepted-video baseline (read-only)

Before anything gets downloaded, build the authoritative list of every video ID currently
accepted into the dataset, per exercise — this is what all new downloads will later be
checked against. Two sources need to be combined:

1. Videos in `data/landmarks/{exercise}/` that were **not** listed in
   `model_training/cleanup_v2/excluded_duplicates.json` (i.e. the surviving, deduplicated
   set from the prior task).
2. Their raw landmark signatures (round to 4 decimal places, concatenate all clips per video
   in sorted clip order) so new candidates can later be compared against them:

```python
import numpy as np

def video_signature(clip_dict):
    parts = [np.round(np.array(clip_dict[c]), 4).flatten() for c in sorted(clip_dict)]
    return tuple(np.concatenate(parts)) if parts else None
```

Save the result as `baseline_videos.json`: `{exercise: [{video_id, signature}]}`.

**This phase is read-only — do not download, extract, delete, or modify anything.**

## Required output format (then stop)

- A per-exercise table: unique video count found in the baseline, compared against this
  reference (verify against the real repo, report discrepancies if any):

| Exercise | Reference count | Your count | Match? |
|---|---|---|---|
| jumping_jack | 4 | ? | ? |
| plank | 5 | ? | ? |
| lunge | 5 | ? | ? |
| bicep_curl | 6 | ? | ? |
| pushup | 6 | ? | ? |
| squat | 8 | ? | ? |
| high_knees | 8 | ? | ? |

- Confirmation that `baseline_videos.json` was saved, and its path.
- Nothing else. Stop after this table and confirmation.
