# BioMechAI — Model Comparison Summary for Supervisor & Evaluators
### Final Year Project (FYP-II) — Academic Defense Summary

| Model Generation | Architecture & Modality | Data & Leakage Protocol | Top-1 Accuracy | Macro Recall | Status & Key Result |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **FYP-I Baseline** | Random Forest (50 Handcrafted Features) | Random Clip Split (**Severe Data Leakage**) | *84.00%* | *83.50%* | **Invalidated** — Model memorized subjects and clothing across splits. |
| **Random Forest v5** | Kinematic Angular Velocities (Tabular) | 115 Held-Out Videos (**Zero Leakage**) | **56.08%** | **55.92%** | **Tabular Baseline** — Honest zero-leakage benchmark on unseen humans. |
| **PoseC3D v1** | SlowOnly 3D ResNet-50 (Joint Dots) | Scratch Init, 444 Frozen Clips | **49.77%** | **51.83%** | **Early Baseline** — Strong on pushups (63%), but jumping jack blind spot (18%). |
| **PoseC3D v4** | SlowOnly 3D ResNet-50 (FineGYM Dots) | Gym-Dot Pretrained, 444 Frozen Clips | **50.90%** | **50.14%** | **Ablation** — Broke 50%, but dot ambiguity caused Squat to collapse to 20.55%. |
| **PoseC3D v5** | SlowOnly 3D ResNet-50 (**Limb Heatmaps**) | Gym-Limb Pretrained, 444 Frozen Clips | **53.38%** | **53.15%** | **Champion Baseline** — Limb heatmaps surged Squat recall by +160% (to 53.42%). |
| **PoseC3D v7 (Current)** | SlowOnly 3D ResNet-50 (**Limb Heatmaps**) | **3,159 Clean Clips (0 Dups, Zero Leakage)** | **63.54%** | **61.39%** | **⭐ ACTIVE CHAMPION** — 95% CI [56.5% – 70.0%], **97.58% live confidence**. |

---

### Key Summary Points for the Teacher:

1. **Why FYP-I was 84%**: In FYP-I, adjacent video clips of the same athlete were randomly shuffled into both train and test sets, artificially inflating the score because the model memorized background walls and clothing.
2. **True Video-Disjoint Benchmark**: Under honest zero-leakage testing across 115 new subjects, models realistically score 53%–56%.
3. **Why Connected Limb Heatmaps Matter (v5)**: Switching from 2D dot heatmaps to continuous 3D limb cylinders solved sagittal view occlusion, boosting Squat accuracy from 20.55% to 53.42% (+160% relative gain).
4. **Why v7 is the Champion (63.54%)**: We audited 4,434 clips, eliminated 987 duplicate clips and 284 low-quality/static frames, and trained on 3,159 clean clips. On strictly unique test clips, v7 jumped to **63.54% Top-1 Accuracy**, **61.39% Macro Recall**, and **97.58% live inference confidence**.
