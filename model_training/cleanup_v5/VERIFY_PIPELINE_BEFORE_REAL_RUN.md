# BioMechAI — Verify the PoseC3D Pipeline Before Committing GPU Hours

### Purpose

Run these five checks, in order, on your REAL data and REAL Kaggle/Colab setup, before
starting the actual fine-tuning run. Each check must show real command output — same rule as
every other task in this project: no summarizing "it should work," show what actually
happened.

**If any check fails, stop and report it. Do not proceed to the next check or to real
training until the failure is understood and fixed.**

---

## Check 1 — Keypoint conversion runs on real data without silent failures

Run the Part 1 conversion script (from the fine-tuning guide) on the real v5 dataset. Report:
- Total clips attempted
- Total clips successfully converted
- Total clips skipped (landmark file not found) — list the first 10 if any exist
- The min/max x and y values across a sample of 20 converted clips (should fall within
  [0, 1000], given the chosen 1000×1000 reference frame)
- For 3 sample clips, print the shoulder-to-hip distance in the converted coordinates, and
  confirm it's a plausible, non-zero, non-absurd number (sanity check that the body wasn't
  collapsed to a point or scaled wrong)

## Check 2 — Train/val split is genuinely video-disjoint

After building `custom_dataset_train.pkl` and `custom_dataset_val.pkl`, run:

```python
import pickle
with open('custom_dataset_train.pkl', 'rb') as f:
    train = pickle.load(f)
with open('custom_dataset_val.pkl', 'rb') as f:
    val = pickle.load(f)

train_videos = set((a['label'], a['video_id']) for a in train)
val_videos = set((a['label'], a['video_id']) for a in val)
overlap = train_videos & val_videos

print(f"Train videos: {len(train_videos)}, Val videos: {len(val_videos)}")
print(f"Overlap (MUST be 0): {len(overlap)}")
if overlap:
    print("!!! LEAKAGE DETECTED !!!", list(overlap)[:10])
```

Report the exact output. Overlap must be exactly 0.

## Check 3 — MMAction2 environment loads the model without training

After installation, confirm the environment actually works before spending any GPU time
training:

```python
from mmaction.apis import init_recognizer
model = init_recognizer('<your_config>.py', '<pretrained_checkpoint>.pth', device='cuda:0')
print("Model loaded successfully:", type(model))
```

Report whether this succeeds or the exact error if it doesn't.

## Check 4 — Tiny end-to-end dry run (the most important check)

Build a miniature version of the dataset — 5 clips per exercise (35 total) instead of the
full set — using the same conversion and split code. Run actual training for 1-2 epochs on
this tiny set:

```bash
python tools/train.py <your_config>.py --cfg-options train_dataloader.dataset.ann_file=tiny_train.pkl val_dataloader.dataset.ann_file=tiny_val.pkl train_cfg.max_epochs=2 --work-dir /kaggle/working/dryrun
```

Report:
- Did training complete both epochs without crashing?
- Did the loss value change between epoch 1 and epoch 2 (even a small change confirms
  learning is happening, not just that the script ran)?
- Did a `.pth` checkpoint file actually appear in the work directory?

## Check 5 — Cross-platform checkpoint resume actually works

Using the tiny dry-run setup from Check 4:
1. Confirm the checkpoint from Check 4 uploaded to the shared Drive folder (check the Drive
   folder directly, or via `drive_sync`'s list-files call).
2. On the OTHER platform (if you just did Check 4 on Kaggle, do this part on Colab, and vice
   versa), run the resume-aware launcher script pointed at the same tiny dataset.
3. Report: did it detect the existing checkpoint, download it, and resume from the correct
   epoch number — or did it start over from epoch 0?

---

## What "ready for the real run" looks like

All five checks show real, reported output, with:
- Check 1: zero or near-zero skipped clips, sane coordinate ranges
- Check 2: zero video overlap
- Check 3: model loads without error
- Check 4: training completes, loss changes, checkpoint file exists
- Check 5: resume picks up the checkpoint correctly on the other platform

Only once all five are confirmed should the real fine-tuning run start on the full dataset.
