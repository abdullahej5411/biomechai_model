# BioMechAI New Video Collection — PHASE 4 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 5's instructions separately after reviewing your Phase 4 output.**

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

**Prerequisite: `data/landmarks_batch2/` from Phase 3 and `baseline_videos.json` from Phase 1
must both exist. If either is missing, stop and tell the user which earlier phase needs to
be run first.**

---

## Your task for THIS phase only: check new candidates for duplicates

For every new video that survived Phase 3, compute its raw-landmark signature (same method
as Phase 1 — round to 4dp, concatenate clips in sorted order) and compare against:
- Every video already in `baseline_videos.json` (the existing accepted dataset)
- Every *other* new video from this same batch (duplicates can occur within a new batch too)

Reject and log any exact match. Do **not** loosen this to "close enough" — use the same
exact 4-decimal-rounded match as the original cleanup, since a loosened threshold is how
duplicates went undetected the first time.

**Do not run the motion filter again in this phase — that was Phase 3. Only check for
duplicates.**

## Required output format (then stop)

- `batch2_duplicates.json`: every rejected video and what it duplicated (existing video or
  another new video).
- Per-exercise table: candidates entering this phase vs. candidates surviving it.
- Nothing else. Stop after this.
