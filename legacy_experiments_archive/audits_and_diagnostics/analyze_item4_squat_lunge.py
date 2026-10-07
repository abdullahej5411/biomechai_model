"""
Detailed Empirical Investigation for Item 4: Squat vs. Lunge Confusion Asymmetry
"""
import os, json, warnings
warnings.filterwarnings('ignore')
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

BASE_DIR = r'model_training\cleanup_v4'
with open(os.path.join(BASE_DIR, 'merged_dataset.json')) as f:
    all_clips = json.load(f)

# Group by (exercise, video_id)
video_keys = sorted(set((c['exercise'], c['video_id']) for c in all_clips))

# Collect unweighted predictions per clip
fold_results = []
for i, (held_out_ex, held_out_vid) in enumerate(video_keys):
    train_clips = [c for c in all_clips if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips = [c for c in all_clips if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

    X_train = np.array([c['features'] for c in train_clips])
    y_train = np.array([c['exercise'] for c in train_clips])
    X_test = np.array([c['features'] for c in test_clips])
    y_test = np.array([c['exercise'] for c in test_clips])

    le = LabelEncoder().fit(y_train)
    scaler = StandardScaler().fit(X_train)

    clf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_leaf=2, random_state=42, n_jobs=1)
    clf.fit(scaler.transform(X_train), le.transform(y_train))
    preds = le.inverse_transform(clf.predict(scaler.transform(X_test)))

    for clip, pred in zip(test_clips, preds):
        fold_results.append({
            'exercise': clip['exercise'],
            'video_id': clip['video_id'],
            'true': clip['exercise'],
            'pred': pred,
            'features': clip['features']
        })

print(f"Total evaluated clips: {len(fold_results)}")

# Subgroup feature extraction
squat_as_squat = [r['features'] for r in fold_results if r['true'] == 'squat' and r['pred'] == 'squat']
squat_as_lunge = [r['features'] for r in fold_results if r['true'] == 'squat' and r['pred'] == 'lunge']
lunge_as_lunge = [r['features'] for r in fold_results if r['true'] == 'lunge' and r['pred'] == 'lunge']
lunge_as_squat = [r['features'] for r in fold_results if r['true'] == 'lunge' and r['pred'] == 'squat']

print(f"\nSubgroup Clip Counts:")
print(f"  Squat -> Squat (Correct):     {len(squat_as_squat):3d} clips")
print(f"  Squat -> Lunge (Misclassified):{len(squat_as_lunge):3d} clips")
print(f"  Lunge -> Lunge (Correct):     {len(lunge_as_lunge):3d} clips")
print(f"  Lunge -> Squat (Misclassified):{len(lunge_as_squat):3d} clips")

sas_mean = np.mean(squat_as_squat, axis=0)
sal_mean = np.mean(squat_as_lunge, axis=0)
lal_mean = np.mean(lunge_as_lunge, axis=0)
las_mean = np.mean(lunge_as_squat, axis=0)

# Feature dictionary based on extract_features:
# 0-7: mean angles (knee_l, knee_r, hip_l, hip_r, elbow_l, elbow_r, shoulder_l, shoulder_r)
# 8-15: std angles
# 16-23: min angles
# 24-31: max angles
# 32-39: range angles
# 40-41: mean knee diff, mean hip diff
# 42-43: max knee diff, max hip diff
# 44-49: body inclination / vertical torso metrics
feature_names = [
    'mean_knee_l', 'mean_knee_r', 'mean_hip_l', 'mean_hip_r',
    'mean_elbow_l', 'mean_elbow_r', 'mean_shoulder_l', 'mean_shoulder_r',
    'std_knee_l', 'std_knee_r', 'std_hip_l', 'std_hip_r',
    'std_elbow_l', 'std_elbow_r', 'std_shoulder_l', 'std_shoulder_r',
    'min_knee_l', 'min_knee_r', 'min_hip_l', 'min_hip_r',
    'min_elbow_l', 'min_elbow_r', 'min_shoulder_l', 'min_shoulder_r',
    'max_knee_l', 'max_knee_r', 'max_hip_l', 'max_hip_r',
    'max_elbow_l', 'max_elbow_r', 'max_shoulder_l', 'max_shoulder_r',
    'range_knee_l', 'range_knee_r', 'range_hip_l', 'range_hip_r',
    'range_elbow_l', 'range_elbow_r', 'range_shoulder_l', 'range_shoulder_r',
    'mean_knee_diff', 'mean_hip_diff', 'max_knee_diff', 'max_hip_diff',
    'mean_torso_angle', 'std_torso_angle', 'min_torso_angle', 'max_torso_angle',
    'mean_body_incline', 'std_body_incline'
]

print("\n=== Key Diagnostic Features across Subgroups ===")
key_indices = [
    0, 1,    # mean knee L, R
    2, 3,    # mean hip L, R
    40, 42,  # mean knee diff, max knee diff
    41, 43,  # mean hip diff, max hip diff
    44, 48   # mean torso angle, mean body incline
]

print(f"{'Feature Name':<20} | {'Squat->Squat':>12} | {'Squat->Lunge':>12} | {'Lunge->Lunge':>12} | {'Lunge->Squat':>12}")
print("-" * 80)
for idx in key_indices:
    name = feature_names[idx] if idx < len(feature_names) else f'feat_{idx}'
    print(f"{name:<20} | {sas_mean[idx]:12.2f} | {sal_mean[idx]:12.2f} | {lal_mean[idx]:12.2f} | {las_mean[idx]:12.2f}")

print("\n=== Asymmetry Analysis ===")
print(f"Mean Knee Difference (Feature 40):")
print(f"  Squat->Squat: {sas_mean[40]:.2f}°")
print(f"  Squat->Lunge: {sal_mean[40]:.2f}° (Elevated artificial asymmetry!)")
print(f"  Lunge->Lunge: {lal_mean[40]:.2f}°")
print(f"  Lunge->Squat: {las_mean[40]:.2f}° (Reduced asymmetry)")

print(f"\nMean Hip Difference (Feature 41):")
print(f"  Squat->Squat: {sas_mean[41]:.2f}°")
print(f"  Squat->Lunge: {sal_mean[41]:.2f}°")
print(f"  Lunge->Lunge: {lal_mean[41]:.2f}°")
print(f"  Lunge->Squat: {las_mean[41]:.2f}°")
