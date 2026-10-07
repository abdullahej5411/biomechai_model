# BioMechAI Audits & Diagnostics

## Overview
This directory contains diagnostic scripts, integrity verifiers, cross-validation sweeps, and audit documentation created during deep-dive investigations into dataset hygiene, cross-exercise contamination, and classification behavior.

---

## File Inventory & Descriptions

### 1. Data Integrity & Contamination Audits
| File | Type | Purpose |
|---|:---:|---|
| `verify_phase5_integrity.py` | Script | Verifies dataset integrity for v5: checks video-disjoint partitioning (0 subject overlap between 457 train / 115 val videos), landmark bounds, and absence of corrupted rows. |
| `REBUILD_v5_remove_contamination.py` | Script | Reconstructs the v5 dataset by purging cross-exercise duplicate files and re-establishing clean, unpolluted class boundaries. |
| `cross_exercise_contamination_report.json` | Data | Manifest detailing identified cross-exercise duplicate pairs and their resolution. |
| `run_cross_exercise_sweep.py` | Script | Full-corpus audit script searching for identical video clips mistakenly labeled under multiple exercises. |
| `DIAGNOSE_v5_exclusion_mismatch.py` | Script | Resolves discrepancies between candidate exclusion sets and processed video manifests. |
| `verify_check1_and_check2.py` | Script | Automated dual-check verification confirming exclusion set mathematical intersections. |
| `check_baseline_backlog_dups.py` | Script | MD5 hash comparison detecting collisions between baseline videos and backlog candidates. |
| `check_3_files_md5.py` | Script | Targeted byte-level hash verification script for contested files. |
| `compute_clean_candidates.py` | Script | Computes set differences ($Candidate - Exclusions$) to establish clean candidate pools. |

### 2. Biomechanical & Classification Diagnoses
| File | Type | Purpose |
|---|:---:|---|
| `analyze_item4_squat_lunge.py` | Script | Diagnoses the primary confusion pair (`squat` vs `lunge`), analyzing joint angle overlap and duration distributions. |
| `run_item4_analysis.py` | Script | Executes deep statistical evaluation on squat and lunge kinematic features. |
| `check_camera_perspective.py` | Script | Analyzes camera perspective angles (frontal vs. sagittal) and their correlation with classification errors. |
| `check_item1_batch2_vs_backlog.py` | Script | Compares Batch 2 videos against backlog candidates to prevent internal duplication. |
| `test_class_weighted_lovo.py` | Script | Experiments with class-weighted cross-entropy loss in LOVO-CV to counter class imbalances. |
| `test_capped_class_weighted_lovo.py` | Script | Evaluates class-weight clipping to prevent minority-class overcompensation during training. |
| `evaluate_plain_unweighted_v4_115vid.py` | Script | Evaluates the plain unweighted Random Forest v4 model on the identical 115 validation videos, generating `plain_unweighted_lovo_115vid_results.json` for unconfounded head-to-head benchmarking. |
| `run_open_items_complete.py` | Script | Comprehensive verification runner covering all open architectural questions. |

### 3. Verification Instructions & Documentation
| File | Description |
|---|---|
| `BIOMECHAI_MODULE3_DATA_CLEANUP_AGENT_INSTRUCTIONS.md` | Authoritative step-by-step instructions and boundaries for the Module 3 data cleanup agent. |
| `BIOMECHAI_OPEN_ITEMS_CONFIRMATION.md` | Formal confirmation log addressing and closing all open audit items. |
| `BIOMECHAI_RAW_VIDEO_BACKLOG_CHECK.md` | Checklist and findings from the raw video backlog examination. |
