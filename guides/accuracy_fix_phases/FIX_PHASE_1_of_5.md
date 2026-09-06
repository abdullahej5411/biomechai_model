# BioMechAI Accuracy Fix — PHASE 1 of 5 ONLY

**Do only what is described below. When finished, output your results in the exact format
requested at the end, then STOP. Do not begin any further work — the user will give you
Phase 2's instructions separately after reviewing your Phase 1 output.**

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

---

## Step 0 — Run the Kaggle session setup cell (mandatory, do this first)

Run the complete setup cell from `KAGGLE_SESSION_SETUP.md` now, in this session, before
anything else — even if you believe this session's environment is already correct. Confirm
its final verification step ("Setup complete — safe to proceed") printed successfully.

**If it errors, STOP per Rule 1 and report — do not troubleshoot on your own initiative.**

Then confirm the checkpoint files and training `.pkl` are accessible in THIS session:
```python
import os
for p in ['<path to best_acc_top1_epoch_18.pth in this Kaggle session>',
          '<path to epoch_24.pth in this Kaggle session>',
          '<path to custom_dataset_train.pkl in this Kaggle session>']:
    print(p, "EXISTS" if os.path.exists(p) else "MISSING — needs re-downloading from Drive")
```
If anything is missing, re-download it from the Drive backup folder (a read-only download is
fine — this is expected, not a Rule 1 violation) before proceeding.

## Your actual task for this phase: confirm or rule out overfitting

Only after Step 0 passes cleanly, run these two evaluations using the exact `test.py`
invocation pattern already proven to work during Q11 verification and the production run:

```bash
python /kaggle/working/mmaction2/tools/test.py <posec3d config path> \
    <best_acc_top1_epoch_18.pth path> \
    --cfg-options val_dataloader.dataset.ann_file=<custom_dataset_train.pkl path> \
    --dump train_eval_epoch18.pkl

python /kaggle/working/mmaction2/tools/test.py <posec3d config path> \
    <epoch_24.pth path> \
    --cfg-options val_dataloader.dataset.ann_file=<custom_dataset_train.pkl path> \
    --dump train_eval_epoch24.pkl
```

If either command errors, apply Rule 1 — stop, report the exact error, do not troubleshoot.

## Required output format (then stop)

- Confirmation the setup cell completed successfully.
- Training-set top-1 accuracy and macro recall for `epoch_18` and `epoch_24`.
- Side-by-side with the known validation numbers:

| Checkpoint | Train Accuracy | Validation Accuracy | Gap |
|---|---|---|---|
| epoch_18 | ? | 49.77% / 51.83% | ? |
| epoch_24 | ? | (not yet evaluated on val) | ? |

- One explicit sentence: is overfitting **confirmed** or **ruled out**?
- Nothing else. Stop after this.
