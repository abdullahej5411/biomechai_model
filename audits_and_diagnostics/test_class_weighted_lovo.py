"""
Test whether class imbalance (not just missing temporal features) explains part of the
v3 -> v4 accuracy regression, by re-running the same 599-fold LOVO-CV with
class_weight='balanced' -- the only change from the original v4 evaluation.

This does NOT overwrite exercise_classifier_v4.pkl or any existing v4 artifact.
It only produces a new, separate comparison result.

Reads: model_training/cleanup_v4/merged_dataset.json (the same 2,309-clip dataset
used for the original v4 LOVO-CV -- adjust the path below if it lives elsewhere).
"""
import os, json, warnings
warnings.filterwarnings('ignore')

import numpy as np
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
MERGED_DATASET_PATH = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4', 'merged_dataset.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4', 'class_weighted_lovo_results.json')

with open(MERGED_DATASET_PATH) as f:
    all_clips = json.load(f)

print(f"Loaded {len(all_clips)} clips from {MERGED_DATASET_PATH}")

# Group by (exercise, video_id) -- same grouping used in every prior LOVO-CV run in this project
video_keys = sorted(set((c['exercise'], c['video_id']) for c in all_clips))
print(f"Total unique (exercise, video_id) folds: {len(video_keys)}")

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

    # ONLY CHANGE from the original v4 evaluation: class_weight='balanced'
    clf = RandomForestClassifier(
        n_estimators=200, max_depth=15, min_samples_leaf=2,
        random_state=42, n_jobs=1, class_weight='balanced'
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
print(f"=== CLASS-WEIGHTED LOVO-CV overall accuracy: {overall_acc*100:.2f}% ===")
print(f"=== Original (unweighted) v4 LOVO-CV overall accuracy: 50.76% ===\n")

print("Classification report (class_weight='balanced'):")
rep_dict = classification_report(y_true_all, y_pred_all, zero_division=0, output_dict=True)
print(classification_report(y_true_all, y_pred_all, zero_division=0))

labels = sorted(set(y_true_all))
cm = confusion_matrix(y_true_all, y_pred_all, labels=labels)
print("Confusion matrix (rows=true, cols=pred):")
header = "                " + " ".join(f"{l[:10]:>11s}" for l in labels)
print(header)
for i, l in enumerate(labels):
    print(f"{l[:15]:16s}" + " ".join(f"{cm[i][j]:11d}" for j in range(len(labels))))

# Save results
output = {
    'overall_accuracy_weighted': overall_acc,
    'overall_accuracy_unweighted_v4_reference': 0.5076,
    'report_dict': rep_dict,
    'confusion_matrix': cm.tolist(),
    'fold_results': [
        {'exercise': ex, 'video_id': vid, 'true': t, 'pred': p}
        for ex, vid, t, p in fold_results
    ],
}
with open(OUTPUT_PATH, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to {OUTPUT_PATH}")
