# BioMechAI — Raw Video Backlog Investigation Report

_Generated: 2026-08-30 | Read-only reconnaissance — no source video files were modified._

---

## 1. Per-Exercise Backlog Counts & Clean Candidate Pool

**Total videos on disk: 1,000 MP4 files (plus 54 incomplete `.part` files) | Total size: ~9.83 GB**

| Exercise | Videos on Disk | WITH Landmarks (Baseline) | Backlog (Raw) | Set A (<500KiB) | Set B (Base Dups) | Overlap ($A \cap B$) | Total Excluded ($A \cup B$) | **Clean Pool** |
|---|---|---|---|---|---|---|---|---|
| **bicep_curl** | 156 | 10 | 146 | 14 | 16 | 1 | 29 | **117** |
| **high_knees** | 85 | 9 | 76 | 4 | 15 | 0 | 19 | **57** |
| **jumping_jack** | 138 | 10 | 128 | 3 | 28 | 0 | 31 | **97** |
| **lunge** | 155 | 8 | 147 | 18 | 21 | 0 | 39 | **108** |
| **plank** | 156 | 10 | 146 | 5 | 19 | 0 | 24 | **122** |
| **pushup** | 153 | 10 | 143 | 8 | 25 | 0 | 33 | **110** |
| **squat** | 157 | 10 | 147 | 2 | 34 | 0 | 36 | **111** |
| **TOTAL** | **1,000** | **67** | **933** | **54** | **158** | **1** | **211** | **722** |

### Mathematical Recomputation (Zero Double-Counting)
* **Total Raw Backlog**: **933 files**
* **Set A (Small / Corrupt < 500 KiB)**: **54 files**
* **Set B (Confirmed Baseline MD5 Duplicates)**: **158 files**
* **Overlap ($A \cap B$)**: **1 file** (`bicep_curl_03_02.mp4` — is both < 500 KiB and a bit-for-bit duplicate of `bicep_curl_03.mp4`)
* **Union of Exclusions ($A \cup B$)**: $|A| + |B| - |A \cap B| = 54 + 158 - 1 =$ **211 files**
* **REAL CLEAN CANDIDATE POOL**: **$933 - 211 =$ 722 genuine candidate videos**

---

## 2. Derivation: How 345 Pair Matches = 158 Distinct Backlog Files

The 345 pair matches found during MD5 cross-verification map to exactly 158 physical backlog files because **several baseline videos are themselves duplicates of each other**:

| Multiplicity | Backlog Files | Baseline Matches per File | Total Pairs Generated |
|---|---|---|---|
| Matched 1 baseline video | 69 files | $\times 1$ | 69 pairs |
| Matched 2 baseline videos | 35 files | $\times 2$ | 70 pairs |
| Matched 3 baseline videos | 16 files | $\times 3$ | 48 pairs |
| Matched 4 baseline videos | 32 files | $\times 4$ | 128 pairs |
| Matched 5 baseline videos | 6 files | $\times 5$ | 30 pairs |
| **TOTALS** | **158 distinct files** | | **345 pairs** |

_Example: In `pushup`, baseline files `pushup_01`, `pushup_02`, `pushup_04`, and `pushup_05` are identical videos. A single backlog file matching them produces 4 pair records._

---

## 3. Why Did Extraction Stop at 67 Videos?

1. **No logs, checkpoint files, or git commits** were found explaining the stopping point.
2. **Timestamp Audit**: For 6 out of 7 exercises, the earliest backlog video timestamp is **~27–28 hours newer** than the latest processed video.
3. **Conclusion**: The 933 backlog videos were downloaded **after** the original 67-video landmark extraction was performed, and extraction was never rerun on the new downloads.

---

## 4. Final Recommendation & Next Steps

* **Usable Backlog Size**: **722 clean, non-baseline, healthy video candidates**.
* **Intra-Backlog Redundancy**: The clean 722 pool will still contain intra-backlog duplicates (multiple downloads of the same videos within the backlog itself).
* **Extraction Protocol**:
  1. Filter out the **211 exclusion union** files.
  2. Pre-deduplicate the remaining 722 files by file size and MD5 hashes.
  3. Extract MediaPipe landmark clips on the surviving unique candidates.
  4. Run 4-decimal landmark signature deduplication against Batch 1 and Batch 2 before final merging.
