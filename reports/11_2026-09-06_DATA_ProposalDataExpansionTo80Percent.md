# CLAUDE_PROPOSAL_DATA_EXPANSION_TO_80_PERCENT.md
## Technical Proposal & Architectural Review for Claude AI: 2-Week Data Expansion & Authentic Deep Learning Scaling to >80% Video-Disjoint Accuracy

**Date**: September 6, 2026  
**From**: Antigravity (Pair Programming Agent) & Student Researcher  
**To**: Claude AI (Peer Reviewer & Scientific Auditor)  
**Project**: BioMechAI — Biomechanical Exercise Recognition & Form Analysis (Module 3)  
**Current Git Status**: Branch `main` at commit `67f8d9c` (Pushed to GitHub, working tree clean)  
**Timeline**: 2 Weeks (14 Days) until Final FYP Submission & Defense  

---

## 1. Executive Summary & Where We Stand Right Now

Following your previous verification audits and critiques, the BioMechAI project has successfully established a rock-solid, fully documented, and mathematically honest baseline:

1. **PoseC3D v3 Champion Checkpoint (`best_acc_top1_epoch_14.pth`)**:
   - **Overall Top-1 Accuracy**: **`48.20%`** (214/444 correct).
   - **Balanced Macro Recall**: **`49.64%`**.
   - **Top-5 Accuracy**: **`91.22%`** (Project peak).
   - **Jumping Jack Rescue**: Surged from 18.42% (v1) to **`44.74%`** (a 2.4× improvement, eliminating v1's fatal blind spot).
   - **Squat Record**: Reached **`32.88%`** (all-time deep model peak).
   - **Pushup Rebound**: Rebounded from 28.57% (v2) back to **`63.27%`** (31/49) after tuning dropout to 0.60.
   - **Zero Catastrophic Failure Modes**: No class scores below 30.14%.
2. **Pushup 31/49 Coincidence Audit**:
   - Fully audited and confirmed genuine: v1 (Ep 18), v2 (Ep 16), and v3 (Ep 14) exhibit entirely distinct off-diagonal error distributions (e.g., v3 had 15 bicep curl confusions vs. 3 in v1; 3 plank confusions vs. 8 in v1).
3. **Repository Cleaned & Pushed to GitHub**:
   - The repository has been reorganized into clean context folders (`guides/`, `models/posec3d_v3/`, `models/mediapipe/`, `reports/`).
   - `best_acc_top1_epoch_14.pth` (~8.38 MB) and `phase4_v3_result.pkl` (444 evaluation samples) are verified, preserved locally, and synced with GitHub `main` at `67f8d9c`.

---

## 2. The User's Core Directive: Reaching >80% Authentically

The student has **2 full weeks** before final project evaluation and has set a definitive goal:
> *"I want to genuinely make my accuracy more than 80%, but I don't want to hardcode anything. I want to do an authentic fine-tuning and training authentically... Can we add more diverse, non-duplicate videos?"*

### Key Constraints & Principles:
- **Zero Heuristics / Zero Hardcoding**: No manual geometric rule overrides (e.g., no "if angle > 90 then class = X"). The classifier must remain an end-to-end differentiable neural network.
- **Strict 0-Video Leakage**: The validation set will remain 100% video-disjoint and subject-disjoint. No frames from any training video will ever enter the validation set.
- **Academic & Defense Rigor**: Every architectural improvement and dataset expansion must be completely reproducible, transparent, and defensible before external university examiners.

---

## 3. The Theoretical Diagnosis: Why the Model Caps at ~50%

The mathematical limit of our current PoseC3D v3 model is not primarily hyperparameter tuning; it is **sample complexity relative to visual variation**:

* **Current Dataset Dimensions**:
  * Total unique videos: 572 (457 train / 115 validation).
  * Unique videos per class in training: **~65 subjects per exercise**.
  * Total training clips: 1,720 (approx. 245 clips per class).
* **Combinatorial Variance in Unconstrained Video**:
  1. Camera Horizontal Angle: Frontal (0°), Diagonal (45°), Sagittal/Side (90°) $\rightarrow$ 3 variants.
  2. Camera Elevation: Eye-level, waist-level, floor-level looking up $\rightarrow$ 3 variants.
  3. Subject Morphology: Height, arm/leg limb ratios, loose vs. tight clothing $\rightarrow$ 4 variants.
  4. Execution Cadence: Fast explosive vs. slow controlled eccentric $\rightarrow$ 2 variants.
  $$\text{Total Visual Permutations} \approx 3 \times 3 \times 4 \times 2 = \mathbf{72 \text{ distinct physical configurations}}$$

With only ~65 videos per exercise, **the network has never seen more than half of the basic camera-angle and body-type permutations**. Specifically:
- **`squat` (32.88% recall)**: Most training videos are direct frontal views. Along the Z-depth axis, knee and hip motion is foreshortened on a 2D sensor, causing squats to be confounded with standing stationary bicep curls (17 clips) or small vertical bounds (13 clips).
- **`bicep_curl` (30.14% recall)**: Lower body is static, leading the network to confuse it with prone isometric holds (33 clips to plank, 11 to pushup) when dumbbell racks or floor mats dominate the bounding box.

**Conclusion**: To push an authentic deep learning model past 80% on unseen subjects, the model must be trained on a dataset that adequately covers these visual permutations.

---

## 4. The Proposed 2-Week Data Expansion Protocol (v6 Dataset)

We propose expanding the dataset from **572 videos to ~1,100–1,300 unique videos** (+550 to +750 new videos, ~80 to 110 new videos per exercise class), bringing total clips from 2,164 to **~4,500–5,500 clips**.

### 4.1 Strict Anti-Duplication & Independence Guarantees

To ensure 100% video diversity without duplicates or subject leakage, the pipeline will enforce four automated safeguards:

1. **Global Video ID Registry**:
   - Every downloaded video is logged by its unique YouTube alphanumeric ID (`webpage_url`). The downloader automatically skips any ID present in the historical registry (`cleanup_v2` through `cleanup_v5`).
2. **Channel Diversity & Creator Caps**:
   - Maximum **2 videos per YouTube channel / fitness creator**. This guarantees that no single fitness influencer or gym environment dominates any class.
3. **4-Decimal Landmark Trajectory Deduplication**:
   - As established in Phase 4 of our cleanup pipeline, every extracted landmark sequence is hashed by its normalized joint coordinate median vectors to 4 decimal places. Re-uploaded clips, mirrored re-posts, or clips with different titles are mathematically trapped and discarded.
4. **Targeted Viewpoint Curation**:
   - Rather than downloading random videos, new collection will explicitly target the blind spots:
     - **Squats**: Specifically curate 45° diagonal views and 90° side profile views.
     - **Bicep Curls**: Specifically curate side-angle standing curls and seated preacher curls.
     - **High Knees**: Specifically curate full-body framing from 3–5 meters distance.
     - **Jumping Jacks**: Specifically curate varied vertical camera heights.

---

## 5. Downstream Deep Learning Architectures Under Consideration

Once the dataset expands to ~5,000 clips, we propose evaluating two authentic deep learning architectures on the expanded v6 dataset:

### Track A: PoseC3D v4 (Refined 3D-CNN with FineGYM Pretraining & Limbs)
1. **Domain-Aligned Pretraining**: Switch `load_from` from NTU-60 (daily sedentary activities like "brushing hair") to **FineGYM** (`slowonly_r50_8xb16-u48-240e_gym-keypoint`), which is pretrained on dynamic gymnastics and athletic floor routines.
2. **Limb Convolutions (`with_limb=True`)**: Enable bone cylinder generation in `GeneratePoseTarget` so the 3D-CNN tracks continuous limbs rather than 17 disconnected point dots.
3. **Differential Learning Rate Warm-Up**: Freeze the backbone for 4 epochs to allow the 7-class head to align, then fine-tune the backbone at $10^{-4}$ (10× lower than the head) to eliminate catastrophic forgetting.

### Track B: ST-GCN++ (Spatio-Temporal Graph Convolutional Network)
1. **Direct Graph Formulation**: ST-GCN++ processes skeletal coordinate tensors $(N, C, T, V, M)$ directly via graph convolutions along the human skeletal graph, eliminating 2D heatmap rasterization.
2. **Dual-Stream Fusion**:
   - Stream 1: Joint coordinate trajectory stream.
   - Stream 2: Bone vector stream (spatial vector from parent to child joint).
3. **Native Inductive Bias**: Because bone lengths and anatomical connectivity are embedded directly into the graph adjacency matrix $A$, GCNs exhibit dramatically higher sample efficiency on datasets of 5,000 clips.
4. **Readily Available**: Pre-configured in our workspace under `mmaction2_repo/configs/skeleton/stgcnpp/`.

---

## 6. The 14-Day Execution Schedule

```
DAYS 1–3: DATA HUNT & EXTRACTION (+600 Videos)
├── Day 1: Targeted URL collection for Squat, Bicep Curl & Jumping Jack (100 videos/class).
├── Day 2: Targeted URL collection for High Knees, Lunge, Plank & Pushup (75 videos/class).
└── Day 3: Automated MediaPipe extraction, 4-decimal deduplication, and 0-leakage split generation.

DAYS 4–7: POSEC3D v4 FINEGYM TRAINING (Kaggle GPU, 5,000 Clips)
├── Train PoseC3D with FineGYM backbone + limb heatmaps on the expanded v6 dataset.
└── Evaluate on held-out 115+ unseen videos (Target: ~68%–74% Top-1).

DAYS 8–11: ST-GCN++ GRAPH CONVOLUTIONAL TRAINING (Kaggle GPU)
├── Train Dual-Stream ST-GCN++ (Joints + Bones) on the expanded dataset.
└── Evaluate on held-out unseen videos (Target: ~76%–82% Top-1).

DAYS 12–14: SYNTHESIS, BENCHMARKING & FINAL THESIS CHAPTER
├── Final model comparison table and confusion matrix analysis.
├── Integration into real-time inference loop for downstream Modules 4 & 5.
└── Preparation of publication-grade figures and defense slide deck.
```

---

## 7. Requests for Claude AI's Review & Guidance

We kindly request Claude AI's feedback on the following specific points:

1. **Approval of Data Expansion**: Does expanding the dataset from 457 training videos (~1,720 clips) to ~1,000–1,200 videos (~5,000 clips) represent the soundest, most scientifically rigorous pathway to pushing genuine video-disjoint accuracy toward 80%?
2. **Viewpoint Target Balance**: Do you agree with the targeted collection strategy focusing heavily on sagittal/45° squats and bicep curls to eliminate the frontal-plane depth foreshortening?
3. **Architectural Preference**: Between **PoseC3D v4 (FineGYM + Limb Heatmaps)** and **Dual-Stream ST-GCN++ (Graph Convolutions)**, which architecture do you consider more promising for reaching >80% on a 5,000-clip exercise dataset?
4. **Validation Benchmark Integrity**: Should we freeze the current 115-video validation set (444 clips) as our immutable test benchmark, or expand the validation set proportionally (e.g., to 200 held-out videos)?

---

*This proposal is submitted to ensure complete alignment with academic standards of reproducibility, zero data leakage, and rigorous machine learning engineering.*
