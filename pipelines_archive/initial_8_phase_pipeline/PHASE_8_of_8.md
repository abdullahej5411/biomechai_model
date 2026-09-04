# BioMechAI New Video Collection — PHASE 8 of 8 (final phase)

**Do only what is described below, then stop — this is the last phase of this task.**

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

**Prerequisite: Phase 7's evaluation results must exist. If not, stop and tell the user
Phase 7 needs to be run first.**

---

## Your task for THIS phase only: save outputs and write the report

Save to a **new** `model_training/cleanup_v3/` directory (do not overwrite `cleanup_v2/`):
- `baseline_videos.json` (from Phase 1)
- `batch2_downloads.json` — what was downloaded, with channel/uploader metadata (Phase 2)
- `batch2_duplicates.json` — what got rejected and why (Phase 4)
- `batch2_static_excluded.json` — what got rejected by the motion filter (Phase 3 + 5)
- `merged_lovo_cv_results.json` — full per-fold results, confusion matrix, per-class metrics
  (Phase 7)
- `exercise_classifier_v3.pkl`, `scaler_v3.pkl`, `label_encoder_v3.pkl` (Phase 7's final
  model)
- `REPORT.md` containing:
  - How many new videos were targeted vs. actually collected per exercise, and why any
    shortfall occurred
  - Old (35.71%) vs. new LOVO-CV accuracy, overall and per class
  - Explicit statement on lunge's status
  - A plain-language verdict: is the merged dataset now adequate, or does it still need more
    collection — with reasoning (unique-videos-per-class), not just the number

## Required output format (then stop — task complete)

- Confirmation each file above was saved, with its path.
- The same old-vs-new comparison table from Phase 7, repeated here for the final record.
- The plain-language verdict.
