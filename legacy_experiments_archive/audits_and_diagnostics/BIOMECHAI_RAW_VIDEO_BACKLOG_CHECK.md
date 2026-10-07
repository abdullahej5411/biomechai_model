# BioMechAI — Raw Video Backlog Investigation
### Read-only reconnaissance task for an AI coding agent

---

## 0. What this task is and isn't

`data/raw_videos/` reportedly contains 1,054 files, but only 335 clips (from 67 videos) were
ever extracted into `data/landmarks/`. That's a large gap, and it's worth understanding
before deciding whether to search for more videos (Batch 3) or process what's already on
disk.

**This is a single, read-only investigation. Do not extract landmarks, delete files, or
modify anything in this task.** The goal is a report the user can make a decision from — not
to start processing the backlog. If the findings suggest processing the backlog is worth
doing, that becomes a separate task with its own instructions, after the user reviews this
report.

---

## 1. Count what's actually on disk

For each exercise subfolder in `data/raw_videos/`:
- Total video file count
- Total file size (helps sanity-check against any "~12GB" or similar figure previously
  mentioned)

Compare against `data/landmarks/{exercise}/` to determine, per video file in
`raw_videos/{exercise}/`, whether it has **any** corresponding clips in `landmarks/{exercise}/`
(match by video ID embedded in filename, e.g. `squat_11.mp4` → look for
`squat_11_clip*.json`).

**Output:** a per-exercise table:

| Exercise | Videos on disk | Videos WITH extracted landmarks | Videos WITHOUT (backlog) |
|---|---|---|---|
| squat | ? | ? | ? |
| ... | | | |

## 2. Look for an explanation of why extraction stopped

Check for any of the following, in order, and report what's found:
- A log, checkpoint, or progress file from `extract_landmarks.py`'s prior runs (e.g. a
  `.log`, `progress.json`, or similar in `model_training/` or the repo root)
- Git history on `extract_landmarks.py` or `data/landmarks/` — commit messages or dates that
  might indicate when extraction was last run, and whether it errored out or was manually
  stopped
- Any README, comment, or note in the repo referencing why only a subset was processed
  (e.g. "processed first N videos due to time constraints," a rate-limit or crash mentioned
  anywhere)
- If nothing is found: say so plainly rather than speculating — "no record found explaining
  the stopping point" is a valid and useful finding.

## 3. Spot-check a sample of the unprocessed backlog for validity

Before assuming all ~987 unprocessed videos are usable, sample ~5 videos per exercise from
the "WITHOUT landmarks" group and check, using file metadata only (duration, resolution,
file size — do not attempt to watch/interpret video content):
- Any videos with suspiciously short duration (<5 seconds) or corrupted/zero file size —
  these likely failed to download properly and aren't usable candidates.
- Any exact-duplicate file sizes within the sample (a quick proxy for potential duplicate
  downloads, similar to the Problem 1 pattern found in the original 67-video set) — full
  duplicate verification would need landmark extraction first, so this is just a preliminary
  flag, not a conclusion.

**Output:** a short table of the sampled videos with duration/size, and any flagged as
likely-invalid.

## 4. Report

Summarize, in a `RAW_VIDEO_BACKLOG_REPORT.md` saved at the repo root (not inside
`model_training/`, since this isn't part of the training pipeline output):
- Per-exercise backlog counts (Section 1's table)
- Whatever was found (or not found) explaining the stopping point (Section 2)
- Spot-check findings (Section 3)
- One explicit recommendation sentence: does this backlog look like a viable, mostly-usable
  source for a Batch 3 extraction pass, or does the spot-check suggest problems (e.g. many
  failed/corrupted downloads) that would need filtering before it's worth extracting?

**Do not proceed to extraction. Stop after the report is written and present it to the
user.**
