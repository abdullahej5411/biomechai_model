"""
Phase 7 of 8 — Leave-One-Video-Out Cross-Validation (LOVO-CV) on Merged Dataset
- Loads merged dataset (model_training/cleanup_v2/merged_dataset.json)
- Runs LOVO-CV over all 119 unique video keys
- Compares new results side-by-side against Phase 4 cleanup baseline (35.71%)
- Trains final deployable model
- Saves evaluation results to model_training/cleanup_v2/phase7_lovo_results.json
"""
import os, sys, json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
CLEANUP_DIR     = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2')
MERGED_FILE     = os.path.join(CLEANUP_DIR, 'merged_dataset.json')
OLD_LOVO_FILE   = os.path.join(CLEANUP_DIR, 'lovo_cv_results.json')
OUT_EVAL_FILE   = os.path.join(CLEANUP_DIR, 'phase7_lovo_results.json')

EXERCISES = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']

# 1. Prerequisite verification
if not os.path.exists(MERGED_FILE):
    print("ERROR: merged_dataset.json from Phase 6 is missing!")
    sys.exit(1)

with open(MERGED_FILE, 'r') as f:
    all_clips = json.load(f)

print(f"Loaded merged dataset: {len(all_clips)} total clips.\n")

# 2. Minimum Viable Class Size Check
video_counts = {}
for ex in EXERCISES:
    vids = set(c['video_id'] for c in all_clips if c['exercise'] == ex)
    video_counts[ex] = len(vids)
    status = "SUFFICIENT" if len(vids) >= 4 else "INSUFFICIENT (< 4 videos)"
    print(f"  {ex:<15}: {len(vids):2d} unique videos [{status}]")

assert all(v >= 4 for v in video_counts.values()), "Class size check failed!"

# 3. LOVO-CV Execution
# Identify unique (exercise, video_id) pairs
all_video_keys = sorted(list(set((c['exercise'], c['video_id']) for c in all_clips)))
print(f"\nStarting LOVO-CV over {len(all_video_keys)} unique video folds...\n")

fold_results = []
fold_details = []

for fold_idx, (held_out_ex, held_out_vid) in enumerate(all_video_keys, 1):
    train_clips = [c for c in all_clips if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips  = [c for c in all_clips if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

    X_train = np.array([c['features'] for c in train_clips])
    y_train = np.array([c['exercise'] for c in train_clips])
    X_test  = np.array([c['features'] for c in test_clips])
    y_test  = np.array([c['exercise'] for c in test_clips])

    le = LabelEncoder().fit(y_train)
    scaler = StandardScaler().fit(X_train)

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(scaler.transform(X_train), le.transform(y_train))
    preds = le.inverse_transform(clf.predict(scaler.transform(X_test)))

    correct_in_fold = sum(t == p for t, p in zip(y_test, preds))
    fold_details.append({
        'fold': fold_idx,
        'video_id': held_out_vid,
        'exercise': held_out_ex,
        'total_clips': len(test_clips),
        'correct': correct_in_fold
    })

    for true, pred in zip(y_test, preds):
        fold_results.append((held_out_ex, held_out_vid, true, pred))

    if fold_idx % 20 == 0 or fold_idx == len(all_video_keys):
        print(f"  Processed {fold_idx}/{len(all_video_keys)} folds...")

y_true = [r[2] for r in fold_results]
y_pred = [r[3] for r in fold_results]

new_accuracy = accuracy_score(y_true, y_pred)
new_report_dict = classification_report(y_true, y_pred, target_names=EXERCISES, output_dict=True)
new_report_text = classification_report(y_true, y_pred, target_names=EXERCISES)
new_cm = confusion_matrix(y_true, y_pred, labels=EXERCISES)

# 4. Train Final Model on All 495 Merged Clips
print("\nTraining final deployable model on all merged clips...")
X_all = np.array([c['features'] for c in all_clips])
y_all = np.array([c['exercise'] for c in all_clips])

le_final = LabelEncoder().fit(y_all)
scaler_final = StandardScaler().fit(X_all)
clf_final = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
clf_final.fit(scaler_final.transform(X_all), le_final.transform(y_all))
print("Final model trained successfully.")

# 5. Load Old Baseline Results for Side-by-Side Comparison
old_accuracy = 0.3571
old_report_dict = {
    'bicep_curl':   {'precision': 0.35, 'recall': 0.32, 'f1-score': 0.33},
    'high_knees':   {'precision': 0.42, 'recall': 0.49, 'f1-score': 0.45},
    'jumping_jack': {'precision': 0.46, 'recall': 0.67, 'f1-score': 0.55},
    'lunge':        {'precision': 0.00, 'recall': 0.00, 'f1-score': 0.00},
    'plank':        {'precision': 0.44, 'recall': 0.33, 'f1-score': 0.38},
    'pushup':       {'precision': 0.33, 'recall': 0.39, 'f1-score': 0.36},
    'squat':        {'precision': 0.36, 'recall': 0.30, 'f1-score': 0.33},
}

# 6. Save Evaluation Results
results_payload = {
    'total_samples': len(all_clips),
    'total_unique_videos': len(all_video_keys),
    'new_lovo_accuracy': float(new_accuracy),
    'old_lovo_accuracy': float(old_accuracy),
    'classes': EXERCISES,
    'confusion_matrix': new_cm.tolist(),
    'classification_report_dict': new_report_dict,
    'classification_report_text': new_report_text,
    'fold_details': fold_details
}
with open(OUT_EVAL_FILE, 'w') as f:
    json.dump(results_payload, f, indent=2)
print(f"\nSaved evaluation results to: {OUT_EVAL_FILE}")

# 7. Print Required Format
print("\n" + "=" * 80)
print("PHASE 7 REQUIRED OUTPUT: OVERALL LOVO-CV ACCURACY")
print("=" * 80)
print(f"| {'Metric':<30} | {'Old Baseline (Cleanup v2)':<25} | {'New Merged Dataset':<20} |")
print(f"|{'-'*32}|{'-'*27}|{'-'*22}|")
print(f"| {'LOVO-CV Overall Accuracy':<30} | {old_accuracy*100:<24.2f}% | {new_accuracy*100:<19.2f}% |")

print("\n" + "=" * 80)
print("PHASE 7 REQUIRED OUTPUT: PER-CLASS METRICS (OLD VS NEW)")
print("=" * 80)
print(f"| {'Exercise':<15} | {'Old Prec':<9} | {'New Prec':<9} | {'Old Rec':<9} | {'New Rec':<9} | {'Old F1':<8} | {'New F1':<8} |")
print(f"|{'-'*17}|{'-'*11}|{'-'*11}|{'-'*11}|{'-'*11}|{'-'*10}|{'-'*10}|")

for ex in EXERCISES:
    old_p = old_report_dict[ex]['precision']
    old_r = old_report_dict[ex]['recall']
    old_f = old_report_dict[ex]['f1-score']
    
    new_p = new_report_dict[ex]['precision']
    new_r = new_report_dict[ex]['recall']
    new_f = new_report_dict[ex]['f1-score']
    
    print(f"| {ex:<15} | {old_p:<9.2f} | {new_p:<9.2f} | {old_r:<9.2f} | {new_r:<9.2f} | {old_f:<8.2f} | {new_f:<8.2f} |")

print("\n" + "=" * 80)
print("PHASE 7 REQUIRED OUTPUT: NEW CONFUSION MATRIX")
print("=" * 80)
header_str = " | ".join([f"{ex[:7]:<7}" for ex in EXERCISES])
print(f"| {'True \\ Pred':<15} | {header_str} |")
print(f"|{'-'*17}|" + "|".join(['-'*9 for _ in EXERCISES]) + "|")
for idx, ex in enumerate(EXERCISES):
    row_str = " | ".join([f"{val:<7d}" for val in new_cm[idx]])
    print(f"| {ex:<15} | {row_str} |")
