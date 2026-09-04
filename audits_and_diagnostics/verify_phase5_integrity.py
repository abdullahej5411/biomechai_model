"""
Phase 5 Comprehensive Integrity Verification Script
"""
import os, sys, json, joblib, shutil
import numpy as np

BASE_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
V4_DIR = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4')
V3_DATASET = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'merged_dataset.json')

EXERCISES = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']

print("=" * 80)
print("PHASE 5 COMPREHENSIVE INTEGRITY VERIFICATION")
print("=" * 80)

# 1. Deliverables on Disk
files_to_check = [
    ('exercise_classifier_v4.pkl', 1000000),  # > 1 MB
    ('scaler_v4.pkl', 1000),                 # > 1 KB
    ('label_encoder_v4.pkl', 100),            # > 100 B
    ('merged_dataset.json', 1000000),         # > 1 MB
    ('merged_v4_lovo_cv_results.json', 1000), # > 1 KB
    ('pilot_lovo_cv_results.json', 1000),     # > 1 KB
    ('full_extraction_log.json', 10000),      # > 10 KB
    ('REPORT.md', 5000),                     # > 5 KB
]

print("\n1. Verifying Deliverable Files on Disk:")
for fname, min_size in files_to_check:
    fpath = os.path.join(V4_DIR, fname)
    assert os.path.exists(fpath), f"MISSING FILE: {fpath}"
    size = os.path.getsize(fpath)
    assert size >= min_size, f"FILE TOO SMALL: {fname} ({size} bytes)"
    print(f"  [PASS] {fname:<32} ({size/1024:.1f} KB)")

# 2. Merged Dataset Audit
print("\n2. Auditing Merged Dataset (merged_dataset.json):")
with open(os.path.join(V4_DIR, 'merged_dataset.json')) as f:
    v4_clips = json.load(f)

print(f"  Total clips in v4: {len(v4_clips)} (Expected: 2,309 = 495 v3 + 587 P2 + 1,227 P4)")
assert len(v4_clips) == 2309

# Check features shape
for idx, c in enumerate(v4_clips):
    assert len(c['features']) == 50, f"Clip {idx} feature length != 50"
    assert c['exercise'] in EXERCISES, f"Invalid exercise {c['exercise']}"
print("  [PASS] All 2,309 clips have valid 50-dimensional feature vectors.")

# Check zero drops from v3
with open(V3_DATASET) as f:
    v3_clips = json.load(f)

v3_features = set((c['exercise'], c['video_id'], tuple(np.round(c['features'], 4))) for c in v3_clips)
v4_features = set((c['exercise'], c['video_id'], tuple(np.round(c['features'], 4))) for c in v4_clips)

assert v3_features.issubset(v4_features), "ERROR: Some v3 clips were dropped!"
print(f"  [PASS] All {len(v3_clips)} v3 clips are 100% preserved in v4 (Zero silent drops).")

# 3. Class Support & Minimum Viable Class Size
print("\n3. Auditing Class Sizes & Video Diversity:")
expected_supports = {
    'bicep_curl': 299,
    'high_knees': 241,
    'jumping_jack': 304,
    'lunge': 394,
    'plank': 397,
    'pushup': 338,
    'squat': 336
}

for ex in EXERCISES:
    cls_clips = [c for c in v4_clips if c['exercise'] == ex]
    cls_vids = set(c['video_id'] for c in cls_clips)
    assert len(cls_clips) == expected_supports[ex], f"Support mismatch in {ex}"
    assert len(cls_vids) >= 4, f"Class {ex} has < 4 videos"
    print(f"  [PASS] {ex:<15}: {len(cls_vids):3d} unique videos | {len(cls_clips):3d} clips")

# 4. LOVO-CV Cross-Validation Results
print("\n4. Auditing LOVO-CV Results (merged_v4_lovo_cv_results.json):")
with open(os.path.join(V4_DIR, 'merged_v4_lovo_cv_results.json')) as f:
    lovo_res = json.load(f)

assert lovo_res['total_clips'] == 2309
assert lovo_res['total_folds'] == 599
cm = np.array(lovo_res['confusion_matrix'])
assert cm.sum() == 2309
assert np.isclose(lovo_res['accuracy'], 0.5075790385448246)
print(f"  [PASS] 599 folds evaluated. Overall LOVO-CV Accuracy: {lovo_res['accuracy']*100:.2f}%")
print(f"  [PASS] Confusion matrix sum: {cm.sum()} (Matches total clips)")

# 5. Model Loading & Inference Test
print("\n5. Testing Model Loading & Inference Pipeline:")
clf = joblib.load(os.path.join(V4_DIR, 'exercise_classifier_v4.pkl'))
scaler = joblib.load(os.path.join(V4_DIR, 'scaler_v4.pkl'))
encoder = joblib.load(os.path.join(V4_DIR, 'label_encoder_v4.pkl'))

# Test sample inference
sample_features = np.array(v4_clips[0]['features']).reshape(1, -1)
scaled = scaler.transform(sample_features)
probs = clf.predict_proba(scaled)[0]
pred_idx = np.argmax(probs)
pred_class = encoder.inverse_transform([pred_idx])[0]

assert len(probs) == 7
assert np.isclose(probs.sum(), 1.0)
assert pred_class in EXERCISES
print(f"  [PASS] Deployable RandomForestClassifier loaded successfully ({len(clf.estimators_)} trees).")
print(f"  [PASS] Sample test input classified as: '{pred_class}' with probability {probs[pred_idx]:.3f}.")
print(f"  [PASS] Probabilities sum to: {probs.sum():.4f} across 7 classes.")

print("\n" + "=" * 80)
print("ALL VERIFICATION CHECKS PASSED: PHASE 5 IS 100% COMPLETE, SOUND, AND READY.")
print("=" * 80)
