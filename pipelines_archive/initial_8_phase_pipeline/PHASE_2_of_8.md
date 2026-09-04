# BioMechAI New Video Collection — PHASE 2 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 3's instructions separately after reviewing your Phase 2 output.**

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

**Prerequisite: `baseline_videos.json` from Phase 1 must exist. If it doesn't, stop and tell
the user Phase 1 needs to be run first — do not attempt to redo Phase 1 yourself.**

---

## Your task for THIS phase only: search and download new candidate videos

Use the existing `download_videos.py` as a reference for how downloading currently works
(same `yt-dlp` mechanism), but do **not** reuse its exact search queries — repeating the same
queries will likely resurface the same or near-duplicate videos from the same channels that
caused the original duplication problem.

For each exercise, generate several **varied** search query phrasings (different wording —
e.g. for squat: "bodyweight squat tutorial", "how to squat proper form", "squat exercise
demonstration", "beginner squat workout" — vary rather than reusing one query repeatedly).

**Diversity constraint:** track the channel/uploader for each candidate (yt-dlp exposes this
in metadata). Cap at roughly 2-3 videos per channel per exercise — if a channel keeps coming
up, change the search query rather than keep pulling from it.

**Targets for this phase (new candidates to attempt downloading, before any duplicate
checking — over-download slightly since some will get rejected later):**

| Exercise | Target new candidates |
|---|---|
| jumping_jack | 13-14 |
| plank | 12 |
| lunge | 12 |
| bicep_curl | 11 |
| pushup | 11 |
| squat | 9 |
| high_knees | 9 |

Save to a **separate** folder: `data/raw_videos_batch2/{exercise}/` — do not mix into the
original `data/raw_videos/`.

**Do not extract landmarks, check for duplicates, or delete anything in this phase — only
download.**

## Required output format (then stop)

- Per-exercise table: candidates downloaded vs. target, with the channel/uploader for each
  file (so diversity can be checked).
- Any exercise where the target couldn't be reached, and why (search yielded too few
  results, etc.) — report honestly rather than padding with near-duplicate channels.
- Nothing else. Stop after this.
