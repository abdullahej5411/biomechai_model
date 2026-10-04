# BioMechAI Master Reports & Documentation Index

## Overview
This directory contains the authoritative technical, diagnostic, and evaluation reports produced throughout the development and finalization of the **BioMechAI** system for **Semester 8 (FYP-II Mid Evaluation)**. All documentation files across the project have been organized into a strict chronological sequence (`XX_YYYY-MM-DD_[CATEGORY]_[BriefDescription].md`) reflecting their exact development timeline and context.

---

## Master Chronological Documentation Manifest

| # | Filename | Date | Category | Primary Focus & Context |
|:---:|---|:---:|:---:|---|
| **01** | `01_2026-08-30_ARCH_InitialProjectContextAndClaudeGuide.md` | 2026-08-30 | Architecture | End-to-end documentation covering data expansion, landmark extraction, and cross-validation progression (v1 to v4). |
| **02** | `02_2026-08-30_DATA_RawVideoBacklogInvestigation.md` | 2026-08-30 | Data | Detailed breakdown of raw video pool audit, duplicate groups, exclusion criteria, and clean candidate counts. |
| **03** | `03_2026-08-31_MODEL_ModelEvolutionAndVersionAnalysis.md` | 2026-08-31 | Model | Comparative analysis across dataset iterations (v2: 35.7% $\rightarrow$ v3: 56.4% $\rightarrow$ v4: 50.8% $\rightarrow$ v5: 52.9% $\rightarrow$ PoseC3D). |
| **04** | `04_2026-09-01_DATA_KagglePipelineVerificationChecks1to5.md` | 2026-09-01 | Data | Mathematical proof of zero subject leakage across 457 train / 115 test videos, coordinate sanity bounds, and MD5 hash deduplication logs. |
| **05** | `05_2026-09-03_ARCH_DriveCheckpointSyncHookVerification.md` | 2026-09-03 | Architecture | Historical pre-training audit document answering all setup questions and recording Kaggle Google Drive checkpoint sync proof. |
| **06** | `06_2026-09-04_MODEL_ProductionRunAndRepoFinalization.md` | 2026-09-04 | Model | Authoritative briefing covering the 24-epoch production training run, metrics, failure analysis, and codebase cleanup. |
| **07** | `07_2026-09-04_AUDIT_BaselineAuditResponseAndDossier.md` | 2026-09-04 | Audit | Forensic line-by-line audit addressing baseline discrepancies, ground-truth provenance from JSON, and failure mode empirical diagnostics. |
| **08** | `08_2026-09-05_AUDIT_ApplesToApplesVerificationAndResolution.md` | 2026-09-05 | Audit | Definitive resolution of baseline inquiries: Jumping Jack 12-clip forensic audit, true apples-to-apples 115-video RF recomputation, and defense strategy. |
| **09** | `09_2026-09-05_DEFENSE_FineTuningMethodologyCompendium.md` | 2026-09-05 | Defense | Comprehensive master defense compendium resolving student confusions, mathematical proofs, PoseC3D architectural origins, and panel Q&A scripts. |
| **10** | `10_2026-09-06_MODEL_5PhaseAccuracyFixResolution.md` | 2026-09-06 | Model | Detailed resolution across 5 technical phases resolving accuracy bottlenecks and standardizing feature representation. |
| **11** | `11_2026-09-06_DATA_ProposalDataExpansionTo80Percent.md` | 2026-09-06 | Data | Strategic proposal detailing data expansion and feature engineering roadmap to surpass the 80% accuracy threshold. |
| **12** | `12_2026-09-07_MODEL_PoseC3D_v4_FineGYMResults.md` | 2026-09-07 | Model | Benchmark results comparing FineGYM pretrained backbone vs NTU RGB+D backbone on the v4 dataset. |
| **13** | `13_2026-09-07_MODEL_PoseC3D_v5_FineGYMLimbHeatmapResults.md` | 2026-09-07 | Model | Empirical evaluation of 3D limb heatmaps and kinematic features under PoseC3D v5 architecture. |
| **14** | `14_2026-09-07_MODEL_Epoch6VsEpoch10ComparisonAndHighKnees.md` | 2026-09-07 | Model | Comparative convergence analysis between Epoch 6 and Epoch 10, specifically targeting High Knees per-class performance. |
| **15** | `15_2026-09-07_BENCHMARK_FinalProductionTrainingAndTop5Accuracy.md` | 2026-09-07 | Benchmark | Full benchmark evaluation of champion PoseC3D model (`epoch_14.pth` with 91.22% Top-5 accuracy on 115-video held-out test split) and confusion matrix. |
| **16** | `16_2026-09-08_DEFENSE_PlainEnglishDefenseAndVivaGuide.md` | 2026-09-08 | Defense | Plain-English oral defense guide, supervisor viva script, and core concept breakdown designed for student presentation confidence. |
| **17** | `17_2026-09-08_ROADMAP_MasterStrategyAnd20DayExecutionGuide.md` | 2026-09-08 | Roadmap | 20-day end-to-end sprint plan detailing milestones, mobile integration, kinematic pipelines, and FYP-II deliverables. |
| **18** | `18_2026-09-08_AUDIT_FourCriticalFixesAuditReport.md` | 2026-09-08 | Audit | Technical audit report covering four critical architectural fixes across preprocessing, inference caching, and pipeline latency. |
| **19** | *(in `../teacher_review/`)* `19_2026-09-11_TEACHER_ModelArchitectureAndTrainingDossier.md` | 2026-09-11 | Teacher | Comprehensive dossier submitted to supervisor/evaluators detailing mathematical architecture and training pipeline. |
| **20** | *(in `../teacher_review/`)* `20_2026-09-13_TEACHER_Official9ModulesStatusAndRoadmap.md` | 2026-09-13 | Teacher | Formal status audit of all 9 official FYP modules aligning development progress with department requirements. |
| **21** | *(in `../srs_documentation/`)* `21_2026-09-15_SRS_OfficialFYPSpecificationDocument.md` | 2026-09-15 | SRS | Official markdown representation of the FYP Software Requirements Specification. |
| **22** | *(in `../srs_documentation/`)* `22_2026-09-15_SRS_ScientificAuditAndGapAnalysisGuide.md` | 2026-09-15 | SRS | Comprehensive scientific audit identifying discrepancies, outdated claims, and missing clinical citations in the original SRS. |
| **23** | `23_2026-09-16_SYSTEM_ComprehensiveHandoverAndStatusV1_6.md` | 2026-09-16 | System | Complete engineering handover document documenting APK v1.6, WebSocket pipelines, TTS engine, and client HUD. |
| **24** | `24_2026-09-17_AUDIT_FormalComplianceResponseAndRecord.md` | 2026-09-17 | Audit | Formal compliance response addressing audit questions regarding dataset provenance, split cleanliness, and model weights. |
| **25** | `25_2026-09-18_SUPERVISOR_CompleteModelAndTerminologyGuide.md` | 2026-09-18 | Supervisor | Clear guide addressing confusing terminology (PoseC3D vs 2D/3D CNNs, transfer learning vs fine-tuning) for supervisor interactions. |
| **26** | `26_2026-09-23_MODULES_Complete9ModulesMasterGuide.md` | 2026-09-23 | Modules | **Authoritative Master Engineering Guide** covering all 9 modules, exact algorithms, clinical thresholds, and real-time mobile integration. |
| **27** | *(in `../srs_documentation/`)* `27_2026-09-30_SRS_PartnerExactSearchAndReplaceManual.md` | 2026-09-30 | SRS | Exact word-for-word, page-by-page search & replace instruction manual for the partner's SRS Word document (also kept as `SRS_EXACT_SEARCH_AND_REPLACE_MODIFICATION_MANUAL.md`). |
| **28** | `28_2026-10-03_SYSTEM_FinalGraduationHandoverAndCloudArchitectureV2_2.md` | 2026-10-03 | System | **Final Graduation Handover & v2.2 Cloud Architecture**: Complete 9-module completion matrix, permanent ngrok cloud tunnel integration, and live viva demonstration guide. |
| **29** | `29_2026-10-03_SYSTEM_SmartScannerAndAnthropometryVerificationV2_3.md` | 2026-10-03 | System | **Smart Body Scanner & Firebase Architecture (v2.3)**: Computer vision anthropometry scale calibration, monocular optics proof, Firebase collection topography, and viva defense guide. |
| **30** | `30_2026-10-04_SYSTEM_OptionC_CrossPlatformPdfAssessmentExportV2_4.md` | 2026-10-04 | System | **Cross-Platform Assessment PDF Export Engine (v2.4)**: Option C delivery for Athlete Mobile App & Coach Web Portal. Anthropometric tables, Devine ideal vitals, and workout progression. Certified with 0 errors/0 warnings. |
| **31** | `31_2026-10-04_SYSTEM_TwoWayCoachAthletePairingAndDataIsolationV2_5.md` | 2026-10-04 | System | **Two-Way Coach-Athlete Pairing & Multi-Tenant Data Isolation (v2.5)**: Approach 2 implementation across Web & Mobile. Athlete sovereignty (Accept/Decline invitations), two-sided Unlink, multi-coach data isolation, and Chromium DOM blob PDF fix. |
| **32** | `32_2026-10-04_SYSTEM_MandatoryEmailVerificationAndGatekeeperV2_6.md` | 2026-10-04 | System | **Mandatory Email Verification & Sign-In Gatekeeper (v2.6)**: Enforces email verification across Web and Mobile registration, blocks unverified logins, provides interactive resend link flow, auto-login protection, and anti-phishing console audit. |
| **33** | `33_2026-10-04_SYSTEM_ComprehensivePostModule6EvolutionAndServicesGuide.md` | 2026-10-04 | System | **Comprehensive Post-Module-6 Evolution & Unified Services Dossier**: Master architectural guide detailing the full progression from v2.3 to v2.6, all 10 Flutter services, React contexts, FastAPI modules, and QA matrix. |

---

## Recommended Reading Order by Audience

### For FYP-II Final Defense & Viva Preparation
1. **`33_2026-10-04_SYSTEM_ComprehensivePostModule6EvolutionAndServicesGuide.md`**: Master post-Module-6 architecture, services breakdown, and graduation readiness.
2. **`32_2026-10-04_SYSTEM_MandatoryEmailVerificationAndGatekeeperV2_6.md`**: Latest production baseline (v2.6), security gatekeeper, and complete auth lifecycle.
3. **`31_2026-10-04_SYSTEM_TwoWayCoachAthletePairingAndDataIsolationV2_5.md`**: Two-way coach pairing, athlete privacy, and multi-tenant data isolation.
4. **`30_2026-10-04_SYSTEM_OptionC_CrossPlatformPdfAssessmentExportV2_4.md`**: Clinical assessment PDF generation engine across Mobile and Web.
5. **`29_2026-10-03_SYSTEM_SmartScannerAndAnthropometryVerificationV2_3.md`**: Module 6 smart camera anthropometry, distance guidance, and monocular optics proof.
6. **`28_2026-10-03_SYSTEM_FinalGraduationHandoverAndCloudArchitectureV2_2.md`**: Master graduation summary, permanent cloud tunnel deployment, and step-by-step viva presentation playbook.
7. **`16_2026-09-08_DEFENSE_PlainEnglishDefenseAndVivaGuide.md`**: Master viva answers, simplified explanations, and counter-arguments for tough questions.
8. **`09_2026-09-05_DEFENSE_FineTuningMethodologyCompendium.md`**: Deep dive into why PoseC3D was chosen, how fine-tuning works, and mathematical validation.
9. **`25_2026-09-18_SUPERVISOR_CompleteModelAndTerminologyGuide.md`**: Clear explanations resolving technical jargon and terminology.

### For Understanding the Complete BioMechAI Architecture
1. **`33_2026-10-04_SYSTEM_ComprehensivePostModule6EvolutionAndServicesGuide.md`**: Master unified services directory and complete post-Module-6 features.
2. **`32_2026-10-04_SYSTEM_MandatoryEmailVerificationAndGatekeeperV2_6.md`**: Latest system baseline (v2.6).
3. **`28_2026-10-03_SYSTEM_FinalGraduationHandoverAndCloudArchitectureV2_2.md`**: Permanent cloud tunnel and WebSocket telemetry.
4. **`26_2026-09-23_MODULES_Complete9ModulesMasterGuide.md`**: Exhaustive reference for all 9 modules, state machines, Munro FPPA formulas, and Devine BMI equations.
5. **`13_2026-09-07_MODEL_PoseC3D_v5_FineGYMLimbHeatmapResults.md`**: Official production PoseC3D v5 Limb Heatmap model performance (53.38% Top-1, 91.22% Top-5) and confusion matrix.
6. **`04_2026-09-01_DATA_KagglePipelineVerificationChecks1to5.md`**: Rigorous data split verification proving zero leakage.

### For SRS Documentation & Academic Evaluation
1. **`../srs_documentation/22_2026-09-15_SRS_ScientificAuditAndGapAnalysisGuide.md`**: Scientific gap analysis and audit of the original SRS.
2. **`../srs_documentation/27_2026-09-30_SRS_PartnerExactSearchAndReplaceManual.md`**: The exhaustive partner edit manual for the Word document.
