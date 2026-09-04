# BioMechAI — PoseC3D Production Fine-Tuning: Complete Execution Guide

### Status: all pre-flight checks verified. This is the guide for the real 24-epoch run.

---

## 0. What's already confirmed true, going into this

- **Dataset**: v5, 2,164 clips across 572 unique videos, independently verified free of
  duplicates, corrupted clips, static/non-exercise clips, and cross-exercise label
  contamination.
- **Baseline to beat**: RandomForest on v5, honest LOVO-CV = **52.91%** overall
  (bicep_curl 0.51 F1, high_knees 0.54, jumping_jack 0.64, lunge 0.47, plank 0.60,
  pushup 0.54, squat 0.38).
- **Conversion pipeline**: MediaPipe→COCO-17 keypoint mapping verified correct against both
  official topologies. 2,164/2,164 clips converted with 0 skips, coordinate ranges and torso
  proportions sane.
- **Split**: 457 train videos / 115 val videos, confirmed 0 video overlap — no leakage.
- **Model**: `Recognizer3D` with `ResNet3dSlowOnly` backbone + `I3DHead`, 7-class output,
  loads correctly on Kaggle's Tesla T4 (architecture math independently verified consistent —
  512 output channels matching the head's expected input).
- **Dry run**: 2-3 epochs on a 28-clip tiny subset completed successfully, loss and accuracy
  behaved exactly as expected for an untrained model at that scale, checkpoints saved and
  resumed correctly.
- **Drive backup**: `DriveCheckpointSyncHook` confirmed live-uploading real `.pth` files to
  Drive during actual training, with headless OAuth token refresh confirmed working with zero
  browser prompts.

Nothing below needs to be re-litigated — this is the launch guide, not another audit.

---

## 1. Pre-flight checklist (2 minutes, do this every time you start or resume a session)

- [ ] GPU accelerator is ON, Internet is ON (Kaggle notebook settings)
- [ ] `token.json` is present and valid in the working directory
- [ ] `posec3d_biomechai.py` has `custom_hooks` pointing at `DriveCheckpointSyncHook` with the
      real `drive_folder_id` (`18RWFWo73gzQ1WZXNB5t3KTEr9cScz9Rx`)
- [ ] The Kaggle Dataset containing `custom_dataset_train.pkl` / `custom_dataset_val.pkl` is
      attached to the notebook (check `/kaggle/input/`)
- [ ] Check the Drive folder directly — does it already contain checkpoints from a prior
      session? If yes, this is a **resume**, not a fresh start (see Section 4).

---

## 2. Launch command (fresh start — no prior checkpoints in Drive)

```bash
PYTHONPATH=/kaggle/working:$PYTHONPATH python /kaggle/working/mmaction2/tools/train.py posec3d_biomechai.py \
    --cfg-options train_dataloader.dataset.ann_file=/kaggle/input/datasets/abdullahej/biomechaicleanup-v5posec3d-data/custom_dataset_train.pkl \
                  val_dataloader.dataset.ann_file=/kaggle/input/datasets/abdullahej/biomechaicleanup-v5posec3d-data/custom_dataset_val.pkl \
                  train_cfg.max_epochs=24 \
                  default_hooks.checkpoint.interval=2 \
                  default_hooks.logger.interval=20 \
                  custom_hooks.0.work_dir=/kaggle/working/biomechai_posec3d_full_run \
    --work-dir /kaggle/working/biomechai_posec3d_full_run
```

`checkpoint.interval=2` means a checkpoint saves (and uploads to Drive) every 2 epochs — worst
case, a session timeout loses 2 epochs of progress, not the whole run.

---

## 3. While it's running

- Real epochs will take far longer than the dry run's ~5 seconds — 1,720 training clips at
  batch size 8 is roughly 215 iterations per epoch versus the dry run's 4. **Time the first
  full epoch** once it completes, and multiply by 24 to get a realistic total-time estimate —
  don't assume it'll be quick just because the dry run was.
- Watch the logger output every 20 iterations for `loss`, `top1_acc`, `top5_acc`. Loss should
  start near `ln(7) ≈ 1.946` (random-guess baseline, matching what the dry run already showed)
  and trend downward over real epochs, not stay flat — if it's still hovering near 1.94-1.97
  after several full epochs, something is wrong with the learning rate or data pipeline, not
  just "needs more time."
- Every 2 epochs, confirm (via the Drive folder or the logged "Drive Backup: ... synced!"
  line) that the checkpoint actually uploaded — don't assume it silently worked.

---

## 4. If a Kaggle session ends before 24 epochs finish

**On a new Kaggle session:**
1. Repeat the Pre-flight checklist (Section 1) — this time the Drive folder check should
   show existing checkpoints.
2. Download the latest `epoch_N.pth` from Drive into the working directory (or re-run the
   `download_latest_checkpoint` helper from the checkpoint-sync module).
3. Re-launch with `--resume <path to epoch_N.pth>` added to the command in Section 2.

**If switching to Colab instead** (e.g. Kaggle's weekly quota is exhausted):
1. Mount Drive with the **same Google account** the checkpoints were uploaded under
   (`aejshah@gmail.com`) — a different account will not see the folder.
2. Use `posec3d_biomechai_COLAB.py` (the version with `custom_imports`/`custom_hooks`
   removed — Colab doesn't need the upload hook since it writes directly to mounted Drive).
3. Set `--work-dir /content/drive/MyDrive/BioMechAI_Checkpoints` (or wherever the mounted
   folder resolves to) so MMEngine saves checkpoints directly onto the same Drive location
   Kaggle was uploading to.
4. Add `--resume` pointing at the latest `.pth` already sitting in that Drive folder.
5. **Before trusting this for real**, confirm the resumed epoch number in the log matches
   what you expect (e.g. if Kaggle stopped after epoch 12, Colab's log should say
   `resumed epoch: 12`) — don't assume it picked up the right file without checking.

---

## 5. After training completes — evaluation (this is the part that actually matters)

**Do not trust a single accuracy number from `tools/test.py` without checking what it's
actually evaluating.** Confirm the test command points at `custom_dataset_val.pkl`
specifically — the same 115-video, video-disjoint validation set confirmed in Check 2, not
some other split.

```bash
python /kaggle/working/mmaction2/tools/test.py posec3d_biomechai.py \
    /kaggle/working/biomechai_posec3d_full_run/best_acc_top1_epoch_*.pth \
    --cfg-options val_dataloader.dataset.ann_file=/kaggle/input/datasets/abdullahej/biomechaicleanup-v5posec3d-data/custom_dataset_val.pkl \
    --dump result.pkl
```

**Then build the same reporting format used for every other result in this project** — this
is what makes the number actually usable, not just a headline percentage:

```python
import pickle
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

with open('result.pkl', 'rb') as f:
    results = pickle.load(f)  # per-sample predictions + ground truth

y_true = [r['gt_label'] for r in results]
y_pred = [r['pred_label'] for r in results]

print(classification_report(y_true, y_pred, zero_division=0))
print(confusion_matrix(y_true, y_pred))
```

(Adapt field names to whatever `result.pkl`'s actual structure turns out to be — inspect one
entry first with `print(results[0])` before assuming the key names.)

**Report this side-by-side with the v5 RandomForest baseline**, per class:

| Exercise | RF (v5) F1 | PoseC3D F1 | Change |
|---|---|---|---|
| bicep_curl | 0.51 | ? | ? |
| high_knees | 0.54 | ? | ? |
| jumping_jack | 0.64 | ? | ? |
| lunge | 0.47 | ? | ? |
| plank | 0.60 | ? | ? |
| pushup | 0.54 | ? | ? |
| squat | 0.38 | ? | ? |

Pay particular attention to **squat** — it was the class RandomForest could never fix through
data volume or class weighting, the class most likely to reveal whether the temporal
architecture change actually solved the problem the static-feature approach couldn't.

---

## 6. What to bring back for review

1. The real per-epoch loss/accuracy trend across the full 24 epochs (not just the final
   number) — confirms genuine learning happened, not a fluke final checkpoint.
2. The full classification report and confusion matrix from Section 5.
3. Confirmation of how many sessions/platform switches it took to complete, and whether the
   resume mechanism worked as expected at each boundary.
