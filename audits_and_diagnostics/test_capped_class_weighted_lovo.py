"""
Third variant of the LOVO-CV class-weighting experiment.

Previous results (already known, for reference -- do not recompute these, just compare
against them):
  - Unweighted v4:                50.76% overall. lunge F1 0.42, squat F1 0.37, high_knees F1 0.48
  - Fully balanced (class_weight='balanced'): 50.76% overall (same total, but NOT the same
    per-class result -- 5 of 7 classes improved, lunge dropped hard enough to cancel out the
    gains). lunge recall 40.4%, squat recall 35.1%, high_knees recall 43.6%.

This variant uses a CAPPED balanced weighting -- full inverse-frequency weighting overcorrected
(lunge, the largest class, lost 26 clips' worth of recall). This caps the maximum weight
multiplier so smaller classes get a boost, but not the full uncapped correction.

Does NOT overwrite any existing v4 or class_weighted artifact. Saves to a new file.
"""
import os, json, warnings
warnings.filterwarnings('ignore')

import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
MERGED_DATASET_PATH = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4', 'merged_dataset.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4', 'capped_class_weighted_lovo_results.json')
MAX_WEIGHT_MULTIPLIER = 1.3  # smallest class gets at most 1.3x the weight of the largest

with open(MERGED_DATASET_PATH) as f:
    all_clips = json.load(f)

print(f"Loaded {len(all_clips)} clips from {MERGED_DATASET_PATH}")

# Compute capped class weights ONCE, from the full dataset's class distribution
# (weights are applied per-fold during training, but the cap is based on overall class sizes)
class_counts = Counter(c['exercise'] for c in all_clips)
print("\nClass sizes (full dataset):")
for ex, n in sorted(class_counts.items()):
    print(f"  {ex}: {n}")

n_classes = len(class_counts)
n_total = len(all_clips)

# Standard sklearn 'balanced' formula: raw_w_i = n_total / (n_classes * n_i)
raw_weights = {ex: n_total / (n_classes * n) for ex, n in class_counts.items()}
min_raw, max_raw = min(raw_weights.values()), max(raw_weights.values())

# Compress into [1.0, MAX_WEIGHT_MULTIPLIER] range, linearly, preserving relative order
capped_weights = {}
for ex, w in raw_weights.items():
    if max_raw == min_raw:
        capped_weights[ex] = 1.0
    else:
        frac = (w - min_raw) / (max_raw - min_raw)
        capped_weights[ex] = 1.0 + (MAX_WEIGHT_MULTIPLIER - 1.0) * frac

print(f"\nCapped class weights (max multiplier = {MAX_WEIGHT_MULTIPLIER}):")
for ex, w in sorted(capped_weights.items()):
    print(f"  {ex}: raw_balanced={raw_weights[ex]:.3f}  ->  capped={w:.3f}")

video_keys = sorted(set((c['exercise'], c['video_id']) for c in all_clips))
print(f"\nTotal unique (exercise, video_id) folds: {len(video_keys)}")

fold_results = []

for i, (held_out_ex, held_out_vid) in enumerate(video_keys):
    train_clips = [c for c in all_clips
                   if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips = [c for c in all_clips
                  if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

    X_train = np.array([c['features'] for c in train_clips])
    y_train = np.array([c['exercise'] for c in train_clips])
    X_test = np.array([c['features'] for c in test_clips])
    y_test = np.array([c['exercise'] for c in test_clips])

    le = LabelEncoder().fit(y_train)
    scaler = StandardScaler().fit(X_train)

    # class_weight passed as an explicit dict keyed by ENCODED label, using the capped weights
    class_weight_dict = {le.transform([ex])[0]: capped_weights[ex] for ex in capped_weights}

    clf = RandomForestClassifier(
        n_estimators=200, max_depth=15, min_samples_leaf=2,
        random_state=42, n_jobs=1, class_weight=class_weight_dict
    )
    clf.fit(scaler.transform(X_train), le.transform(y_train))
    preds = le.inverse_transform(clf.predict(scaler.transform(X_test)))

    for true, pred in zip(y_test, preds):
        fold_results.append((held_out_ex, held_out_vid, true, pred))

    if (i + 1) % 100 == 0 or (i + 1) == len(video_keys):
        print(f"  ...completed {i + 1}/{len(video_keys)} folds")

print(f"\nCompleted all {len(video_keys)} folds.\n")

y_true_all = [r[2] for r in fold_results]
y_pred_all = [r[3] for r in fold_results]

overall_acc = sum(t == p for t, p in zip(y_true_all, y_pred_all)) / len(y_true_all)

print("=" * 70)
print(f"CAPPED-weighted overall accuracy:   {overall_acc*100:.2f}%")
print("Unweighted v4 overall accuracy:      50.76%  (reference)")
print("Fully-balanced overall accuracy:     50.76%  (reference)")
print("=" * 70)

print("\nClassification report (capped class weighting):")
print(classification_report(y_true_all, y_pred_all, zero_division=0))

# MANDATORY: per-class three-way comparison table -- do not rely on overall accuracy alone
# to judge whether this experiment helped, since the prior experiment showed identical
# overall accuracy hid a large per-class redistribution.
unweighted_recall_ref = {
    'bicep_curl': 0.565, 'high_knees': 0.394, 'jumping_jack': 0.615,
    'lunge': 0.470, 'plank': 0.599, 'pushup': 0.553, 'squat': 0.330
}
balanced_recall_ref = {
    'bicep_curl': 0.585, 'high_knees': 0.436, 'jumping_jack': 0.628,
    'lunge': 0.404, 'plank': 0.584, 'pushup': 0.568, 'squat': 0.351
}

report = classification_report(y_true_all, y_pred_all, zero_division=0, output_dict=True)
print("\n=== MANDATORY three-way per-class recall comparison ===")
print(f"{'Exercise':<14} {'Unweighted':>11} {'Full-balanced':>14} {'Capped(1.3x)':>13} {'Capped vs Unweighted':>21}")
for ex in sorted(unweighted_recall_ref):
    capped_recall = report[ex]['recall']
    delta = capped_recall - unweighted_recall_ref[ex]
    print(f"{ex:<14} {unweighted_recall_ref[ex]*100:>10.1f}% {balanced_recall_ref[ex]*100:>13.1f}% "
          f"{capped_recall*100:>12.1f}% {delta*100:>+20.1f}pp")

labels = sorted(set(y_true_all))
cm = confusion_matrix(y_true_all, y_pred_all, labels=labels)
print("\nConfusion matrix (rows=true, cols=pred):")
header = "                " + " ".join(f"{l[:10]:>11s}" for l in labels)
print(header)
for i, l in enumerate(labels):
    print(f"{l[:15]:16s}" + " ".join(f"{cm[i][j]:11d}" for j in range(len(labels))))

output = {
    'overall_accuracy_capped': overall_acc,
    'overall_accuracy_unweighted_reference': 0.5076,
    'overall_accuracy_full_balanced_reference': 0.5076,
    'capped_weights_used': capped_weights,
    'report_dict': report,
    'confusion_matrix': cm.tolist(),
    'fold_results': [
        {'exercise': ex, 'video_id': vid, 'true': t, 'pred': p}
        for ex, vid, t, p in fold_results
    ],
}
with open(OUTPUT_PATH, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to {OUTPUT_PATH}")
