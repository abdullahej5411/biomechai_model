"""
Item 4 Investigation: Analyzing Squat vs. Lunge Confusion Asymmetry
"""
import os, json, joblib
import numpy as np

# Load dataset and model
with open('model_training/cleanup_v4/merged_dataset.json') as f:
    clips = json.load(f)

clf = joblib.load('model_training/cleanup_v4/exercise_classifier_v4.pkl')
scaler = joblib.load('model_training/cleanup_v4/scaler_v4.pkl')
encoder = joblib.load('model_training/cleanup_v4/label_encoder_v4.pkl')

# Load fold results from class-weighted and capped LOVO results
with open('model_training/cleanup_v4/capped_class_weighted_lovo_results.json') as f:
    capped_res = json.load(f)

fold_map = {}
for r in capped_res['fold_results']:
    fold_map[(r['exercise'], r['video_id'])] = r['pred']

# Also run LOVO or out-of-fold predictions
X_all = np.array([c['features'] for c in clips])
y_all = np.array([c['exercise'] for c in clips])

# Feature 40: mean knee diff (|knee_l - knee_r|)
# Feature 41: mean hip diff (|hip_l - hip_r|)
# Feature 42: max knee diff
# Feature 43: max hip diff

squat_clips = [c for c in clips if c['exercise'] == 'squat']
lunge_clips = [c for c in clips if c['exercise'] == 'lunge']

squats_knee_diff = [c['features'][40] for c in squat_clips]
lunges_knee_diff = [c['features'][40] for c in lunge_clips]

squats_hip_diff = [c['features'][41] for c in squat_clips]
lunges_hip_diff = [c['features'][41] for c in lunge_clips]

print("=== ALL SQUATS vs ALL LUNGES FEATURE DISTRIBUTIONS ===")
print(f"Squat Mean Knee Difference (|Knee_L - Knee_R|):  {np.mean(squats_knee_diff):.2f}° ± {np.std(squats_knee_diff):.2f}° (Median: {np.median(squats_knee_diff):.2f}°)")
print(f"Lunge Mean Knee Difference (|Knee_L - Knee_R|):  {np.mean(lunges_knee_diff):.2f}° ± {np.std(lunges_knee_diff):.2f}° (Median: {np.median(lunges_knee_diff):.2f}°)")

print(f"\nSquat Mean Hip Difference (|Hip_L - Hip_R|):    {np.mean(squats_hip_diff):.2f}° ± {np.std(squats_hip_diff):.2f}° (Median: {np.median(squats_hip_diff):.2f}°)")
print(f"Lunge Mean Hip Difference (|Hip_L - Hip_R|):    {np.mean(lunges_hip_diff):.2f}° ± {np.std(lunges_hip_diff):.2f}° (Median: {np.median(lunges_hip_diff):.2f}°)")

# Now check how many squats have high knee difference (> 15 degrees) due to 2D perspective / oblique angle:
squats_high_asym = [c for c in squat_clips if c['features'][40] > 15.0]
print(f"\nSquats with 2D Knee Asymmetry > 15° (Camera Perspective Distortion): {len(squats_high_asym)}/{len(squat_clips)} ({100*len(squats_high_asym)/len(squat_clips):.1f}%)")

# Now check feature importances of Random Forest for knee/hip difference
feature_importances = clf.feature_importances_
top_feat_idx = np.argsort(feature_importances)[::-1][:10]
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

print("\n=== TOP 10 MOST IMPORTANT FEATURES IN RANDOM FOREST ===")
for rank, idx in enumerate(top_feat_idx):
    print(f"  #{rank+1:2d} | Feature {idx:2d} ({feature_names[idx]:<18}): {feature_importances[idx]*100:.2f}%")

# Check why Squat -> Lunge happens:
# When Squat has high knee diff or high hip diff, what does RF predict?
preds_squats = clf.predict(scaler.transform(np.array([c['features'] for c in squat_clips])))
pred_classes = encoder.inverse_transform(preds_squats)
squat_pred_counts = {ex: np.sum(pred_classes == ex) for ex in encoder.classes_}
print("\nDirect Model Predictions on All 336 Squat Clips:")
for ex, count in squat_pred_counts.items():
    print(f"  Predicted as {ex:<15}: {count:3d} clips ({100*count/len(squat_clips):.1f}%)")
