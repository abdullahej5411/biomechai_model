# BioMechAI Accuracy Fix — PHASE 3 of 5 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 4's instructions separately after reviewing your Phase 3 output.**

## Context (read only what you need — do not act on anything beyond THIS phase)

This is the BioMechAI PoseC3D fine-tuned exercise classifier (7 classes). Current state:

- **RF v5 baseline** (RandomForest, honest LOVO-CV): 52.91% overall, 52.14% macro recall.
- **PoseC3D v1** (current fine-tuned model, NTU60-pretrained, 24 epochs, evaluated on 115
  held-out videos / 444 clips): 49.77% overall, 51.83% macro recall. Best checkpoint was
  epoch 18, not epoch 24, despite training loss continuing to drop to 0.23 by epoch 23.
- **Two live hypotheses, neither yet confirmed:**
  1. Possible overfitting (loss very low, validation accuracy plateaued, best checkpoint
     earlier than the final epoch).
  2. Jumping_jack's collapse may not be fully explained by the 3 known frame-truncated
     source videos.

**Goal of the overall task:** diagnose the real cause(s) of the accuracy ceiling, apply fixes
based on actual evidence, retrain once, and honestly compare the result.

---

## MANDATORY RULE 0 — WHERE THIS RUNS, AND KAGGLE SESSIONS DO NOT PERSIST

**Every command in this phase MUST run inside a Kaggle notebook — never on the local
machine.** No `venv\Scripts\python.exe`, no local `pip install`, no local `git clone` of
MMAction2, no PowerShell/local filesystem environment setup, ever, for any part of this task.

**Kaggle sessions do NOT remember anything between sessions — including a restarted kernel
in the same notebook.** Every pip install, every cloned repo, every patched file from a
previous session is gone in a new one. This means: **at the start of every new Kaggle
session, before any phase-specific command, run the complete setup cell in
`KAGGLE_SESSION_SETUP.md` exactly as written.** Do not assume the environment is already
correct just because it worked in an earlier session — always run that cell fresh. Do not
rediscover its fixes one at a time through trial and error; they are already documented there.

**Do NOT treat a local copy of a checkpoint file** (e.g. under `models/posec3d_v5/` in the
local repo, which exists only because of the post-training repository reorganization) **as
something to evaluate on the local machine.** Evaluation happens inside the Kaggle session,
using the Kaggle-resident checkpoint (still present in the Kaggle working directory from the
training run, or re-downloaded from the Drive backup folder into the fresh session) — never
the local copy, and never on local hardware.

**If unsure whether a required file exists in the current Kaggle session, CHECK FIRST with a
read-only command before doing anything else.**

---

## MANDATORY RULE 1 — STOP ON FIRST ERROR (no self-directed troubleshooting)

**If any command produces an error, unexpected output, or does not behave as expected: STOP
immediately. Print the exact, complete error message. Do NOT:**
- Try an alternative approach on your own initiative
- Install a package you think might fix it
- Patch, edit, or modify any source file to work around it
- Move on to a different method and keep going
- Spend more than one attempt on the same problem before stopping

**Report the exact error and STOP. Wait for the user's next instruction.** A phase that hits
an unexpected error and stops cleanly is a successful outcome of this rule — it means the
circuit breaker worked. A phase that pushes through 20 self-directed fixes to "succeed
anyway" is a failure of this rule, even if it eventually produces output, because it means
GPU-hours and time were spent solving problems nobody asked it to solve.

---

## Two more standing rules

- **Never present an invented, hypothetical, or illustrative example as if it were real
  script output.**
- **Every number in your output must be traceable to a script's actual printed result.**

**You are being given this task ONE PHASE AT A TIME, on purpose.** You will only receive the
next phase's instructions after the user has reviewed this phase's output. Do not attempt to
infer, plan for, or begin work on later phases.

**Prerequisite: Phase 1's overfitting verdict and Phase 2's jumping_jack diagnosis must both
be complete. If either is missing, STOP and report — do not guess at their conclusions.**

**This phase is a text edit to a config file — it does not require the full
`KAGGLE_SESSION_SETUP.md` cell. If you want to validate the edited config actually loads
(recommended), run the setup cell's Steps 1, 4-5, and 7 (MMEngine/MMAction2 install + patches
+ verification) — not the full training-specific steps, since no training happens here.**

---

## Your task for THIS phase only: choose and prepare fixes, in the existing config file

**Edit the existing `posec3d_biomechai.py` config already used for training** — the real one,
not a new copy. Apply only fixes matching confirmed findings.

### 3a. If Phase 1 confirmed overfitting
- Increase `dropout_ratio` in the classification head config
- Add or increase weight decay in the optimizer config
- Plan fewer max epochs, relying on existing `save_best='auto'` checkpointing

**If Phase 1 ruled out overfitting, skip 3a and say so explicitly.**

### 3b. Enable skeleton-specific data augmentation (regardless of Phase 1's result)
Check whether `train_pipeline` already includes these; add if missing:
- Random horizontal flip with correct left-right keypoint swap mapping
- Random rotation/scale jitter on 2D keypoints
- Temporal augmentation (random start offset within the 90 frames)

### 3c. FineGYM-pretrained checkpoint as an alternative starting point
Check MMAction2's current model zoo for the real current checkpoint — do not hardcode a
filename from memory.

### 3d. If Phase 2 found jumping_jack has a second undiagnosed problem
Investigate with real evidence before deciding a fix — do not guess.

**Do not retrain in this phase. Do not run any training command.**

**If validating the config produces an error you don't immediately understand — STOP per
Rule 1, report it, do not start troubleshooting the MMEngine config system or installing
things beyond what the setup cell already covers.**

## Required output format (then stop)

- Which fixes from 3a-3d are being applied, each tied explicitly to a Phase 1/2 finding.
- The actual modified config sections as real diffs.
- Nothing else. Stop after this — wait for explicit review before Phase 4 trains anything.
