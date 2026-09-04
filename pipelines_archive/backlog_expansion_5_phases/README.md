# Backlog Expansion 5-Phase Pipeline (Archive)

## Overview
This directory contains the procedural code, manifests, and phase reports from the **1,000-Video Backlog Expansion Pipeline** that grew the dataset from 119 videos (v3) to 599 videos (v4).

---

## The 5 Backlog Phases

| Phase | Runner Script | Documentation | Manifest / Output | Purpose |
|:---:|---|---|---|---|
| **1** | `run_backlog_phase1.py` | `BACKLOG_PHASE_1_of_5.md` | `backlog_clean_deduped_candidates.json` (170.6 KB) | Full MD5 audit of 1,054 files in `data/raw_videos/`. Removed 158 baseline collisions, 54 corrupted files, and 102 duplicate groups, locking **489 unique clean candidate videos**. |
| **2** | `run_backlog_phase2.py` | `BACKLOG_PHASE_2_of_5.md` | `backlog_phase2_extraction_log.json` (29.9 KB) | Pilot landmark extraction on Squat (73 videos $\rightarrow$ 272 clips) and Lunge (87 videos $\rightarrow$ 315 clips) using 90-frame duration-aware sampling. |
| **3** | `run_backlog_phase3.py` | `BACKLOG_PHASE_3_of_5.md` | `backlog_phase3_lovo_results.json` (2.9 KB) | Pilot LOVO-CV decision gate on 1,082 clips. Verified Squat F1 increased from 0.34 $\rightarrow$ 0.51 (+0.17), proving data volume resolved the bottleneck. |
| **4** | `run_backlog_phase4.py` | `BACKLOG_PHASE_4_of_5.md` | `backlog_phase4_extraction_log.json` (62.6 KB) | Full landmark extraction on remaining 5 classes (329 candidate videos $\rightarrow$ 1,227 valid clips). Grand total: 1,814 clean backlog clips. |
| **5** | `run_backlog_phase5.py` | `BACKLOG_PHASE_5_of_5.md` | Merged dataset manifest | Dataset unification (495 baseline + 1,814 backlog = 2,309 clips across 599 unique videos), 599-fold LOVO-CV, and final v4 model training. |

---

## Output Manifests
- **`backlog_clean_deduped_candidates.json`**: Authoritative manifest of all 489 clean, deduplicated backlog video candidates.
- **`backlog_phase2_extraction_log.json`**: Per-video extraction log for squat and lunge pilot.
- **`backlog_phase3_lovo_results.json`**: Decision-gate classification report and metrics for the 277-fold pilot.
- **`backlog_phase4_extraction_log.json`**: Complete extraction log across all 329 videos in the remaining 5 exercises.
