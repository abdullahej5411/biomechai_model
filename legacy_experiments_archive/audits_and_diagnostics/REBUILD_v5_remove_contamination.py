"""
Build v5: remove ALL cross-exercise-contaminated videos (found in the full sweep) and
re-verify same-exercise duplicates dataset-wide, then rebuild the merged dataset and
re-run the honest LOVO-CV evaluation.

This is the first evaluation run on a dataset confirmed free of cross-exercise label
contamination -- treat this as the real baseline going into PoseC3D, not v4.
"""
import os
import json
import hashlib
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

MERGED_V4_PATH = r'model_training\cleanup_v4\merged_dataset.json'
CONTAMINATION_REPORT_PATH = 'cross_exercise_contamination_report.json'
OUTPUT_DIR = r'model_training\cleanup_v5'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Load the cross-exercise contamination report from the sweep
with open(CONTAMINATION_REPORT_PATH) as f:
    contamination = json.load(f)

# Build the set of (exercise, video_id) pairs to fully exclude -- ALL copies of ANY
# video involved in a cross-exercise group, regardless of which label it's under
excluded_video_ids = set()  # (exercise, video_id_without_extension)
for group in contamination['cross_exercise_details']:
    for f in group['files']:
        # filename like 'squat_01_06.mp4' -> video_id 'squat_01_06'
        video_id = f['filename'].replace('.mp4', '')
        excluded_video_ids.add((f['exercise'], video_id))

print(f"Total videos to exclude (cross-exercise contamination): {len(excluded_video_ids)}")
by_ex_excluded = defaultdict(int)
for ex, vid in excluded_video_ids:
    by_ex_excluded[ex] += 1
for ex, n in sorted(by_ex_excluded.items()):
    print(f"  {ex}: {n} videos excluded")

# Step 2: Load the current v4 merged dataset, remove any clip whose video is in the
# exclusion set
with open(MERGED_V4_PATH) as f:
    v4_clips = json.load(f)

print(f"\nv4 total clips before exclusion: {len(v4_clips)}")

v5_clips = []
removed_clips = []
for c in v4_clips:
    key = (c['exercise'], c['video_id'])
    if key in excluded_video_ids:
        removed_clips.append(c)
    else:
        v5_clips.append(c)

print(f"v5 total clips after exclusion: {len(v5_clips)}")
print(f"Clips removed: {len(removed_clips)}")

removed_by_ex = defaultdict(int)
for c in removed_clips:
    removed_by_ex[c['exercise']] += 1
print("\nClips removed per exercise:")
for ex, n in sorted(removed_by_ex.items()):
    print(f"  {ex}: {n} clips")

v5_video_counts = defaultdict(set)
for c in v5_clips:
    v5_video_counts[c['exercise']].add(c['video_id'])
print("\nv5 unique videos remaining per exercise:")
for ex, vids in sorted(v5_video_counts.items()):
    print(f"  {ex}: {len(vids)} videos")

with open(os.path.join(OUTPUT_DIR, 'merged_dataset.json'), 'w') as f:
    json.dump(v5_clips, f)
print(f"\nSaved cleaned v5 dataset to {OUTPUT_DIR}\\merged_dataset.json")

# Step 3: Re-run honest LOVO-CV on v5
print("\n" + "=" * 70)
print("Running LOVO-CV on v5 (contamination-free dataset)...")
print("=" * 70)

video_keys = sorted(set((c['exercise'], c['video_id']) for c in v5_clips))
print(f"Total unique (exercise, video_id) folds: {len(video_keys)}")

fold_results = []
for i, (held_out_ex, held_out_vid) in enumerate(video_keys):
    train_clips = [c for c in v5_clips
                   if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips = [c for c in v5_clips
                  if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

    X_train = np.array([c['features'] for c in train_clips])
    y_train = np.array([c['exercise'] for c in train_clips])
    X_test = np.array([c['features'] for c in test_clips])
    y_test = np.array([c['exercise'] for c in test_clips])

    le = LabelEncoder().fit(y_train)
    scaler = StandardScaler().fit(X_train)
    clf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=2,
                                  random_state=42, n_jobs=1)
    clf.fit(scaler.transform(X_train), le.transform(y_train))
    preds = le.inverse_transform(clf.predict(scaler.transform(X_test)))

    for true, pred in zip(y_test, preds):
        fold_results.append((held_out_ex, held_out_vid, true, pred))

    if (i + 1) % 100 == 0:
        print(f"  ...completed {i + 1}/{len(video_keys)} folds")

y_true_all = [r[2] for r in fold_results]
y_pred_all = [r[3] for r in fold_results]
overall_acc = sum(t == p for t, p in zip(y_true_all, y_pred_all)) / len(y_true_all)

print(f"\n=== v5 (contamination-free) LOVO-CV accuracy: {overall_acc*100:.2f}% ===")
print(f"=== v4 (contaminated) reference accuracy: 50.76% ===\n")
print("Classification report (v5):")
print(classification_report(y_true_all, y_pred_all, zero_division=0))

labels = sorted(set(y_true_all))
cm = confusion_matrix(y_true_all, y_pred_all, labels=labels)
print("Confusion matrix (rows=true, cols=pred):")
header = "                " + " ".join(f"{l[:10]:>11s}" for l in labels)
print(header)
for i, l in enumerate(labels):
    print(f"{l[:15]:16s}" + " ".join(f"{cm[i][j]:11d}" for j in range(len(labels))))

# Specifically highlight squat<->lunge change
squat_i, lunge_i = labels.index('squat'), labels.index('lunge')
print(f"\nSquat->Lunge misclassifications: {cm[squat_i][lunge_i]} (v4 was 101)")
print(f"Lunge->Squat misclassifications: {cm[lunge_i][squat_i]} (v4 was 69)")

output = {
    'overall_accuracy_v5': overall_acc,
    'overall_accuracy_v4_reference': 0.5076,
    'excluded_video_count': len(excluded_video_ids),
    'clips_removed': len(removed_clips),
    'fold_results': [{'exercise': ex, 'video_id': vid, 'true': t, 'pred': p}
                      for ex, vid, t, p in fold_results],
}
with open(os.path.join(OUTPUT_DIR, 'v5_lovo_cv_results.json'), 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to {OUTPUT_DIR}\\v5_lovo_cv_results.json")
