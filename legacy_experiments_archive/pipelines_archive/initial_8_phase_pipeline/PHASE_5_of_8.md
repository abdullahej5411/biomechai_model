# BioMechAI New Video Collection — PHASE 5 of 8 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 6's instructions separately after reviewing your Phase 5 output.**

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

**Prerequisite: Phase 4's `batch2_duplicates.json` and the surviving clip list must exist.
If not, stop and tell the user Phase 4 needs to be run first.**

---

## Your task for THIS phase only: final motion-sanity pass on the combined dataset

Re-run the motion filter (same `overall_motion` function as Phase 3), this time computed
against the **combined** (existing + new-surviving) per-exercise motion distribution, since
the median may shift slightly with more data added. Exclude anything now falling below 20%
of the updated combined median.

**Do not merge feature matrices or retrain anything in this phase — that's Phase 6/7. Only
apply this final filter and report the result.**

## Required output format (then stop)

- Per-exercise table: clips entering this phase, updated combined median motion value, clips
  excluded by this final pass, clips finally accepted.
- Nothing else. Stop after this.
