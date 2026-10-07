# Initial 8-Phase Data Pipeline (Archive)

## Overview
This directory contains the original 8-phase procedural scripts and documentation developed during the initial data processing and model evaluation pipeline (v1 through v3).

---

## The 8 Phases

| Phase | Script | Documentation | Purpose |
|:---:|---|---|---|
| **1** | `phase1_baseline.py` | `PHASE_1_of_8.md` | Initial baseline data audit and candidate file discovery. |
| **2** | `phase2_download.py` | `PHASE_2_of_8.md` | Automated video ingestion and YouTube stream download handlers. |
| **3** | `phase3_extract.py` | `PHASE_3_of_8.md` | MediaPipe 33 landmark extraction on raw video clips. |
| **4** | `phase4_deduplicate.py` | `PHASE_4_of_8.md` | Deduplication using MD5 hashing and motion threshold filtering. |
| **5** | `phase5_final_filter.py` | `PHASE_5_of_8.md` | Coordinate normalization, bounding box validation, and motion sanity filters. |
| **6** | `phase6_features.py` | `PHASE_6_of_8.md` | Feature engineering: joint angle calculation, temporal velocity, and displacement. |
| **7** | `phase7_evaluate.py` | `PHASE_7_of_8.md` | Leave-One-Video-Out Cross-Validation (LOVO-CV) evaluation with Random Forest. |
| **8** | `phase8_finalize.py` | `PHASE_8_of_8.md` | Model serialization, metric report generation, and final pipeline packaging. |

---

## Auxiliary Scripts
- `print_phase2_tables.py`, `print_phase3_results.py`, `print_phase4_tables.py`, `print_phase4_tables_part1.py`: Table formatting utilities for terminal inspection.
- `print_report.py`: Terminal summary printer for Phase 8 metrics.
