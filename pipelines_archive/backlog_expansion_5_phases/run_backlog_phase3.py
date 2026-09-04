"""
BioMechAI Backlog Extraction — PHASE 3 of 5
- Merges Phase 2 squat and lunge clips with v3 dataset (5 other classes untouched)
- Extracts 50 features using exact kinematic extract_features function
- Runs Leave-One-Video-Out Cross-Validation (LOVO-CV) across all unique video folds
- Suppresses warnings for clean fast execution
- Reports Squat and Lunge F1 vs v3 (0.34 & 0.48) and confusion pattern
"""
import os, sys, json, warnings
warnings.filterwarnings('ignore')

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
V3_DATASET_FILE = os.path.join(BASE_DIR, 'model_training', 'cleanup_v3', 'merged_dataset.json')
LM_BACKLOG_DIR  = os.path.join(BASE_DIR, 'data', 'landmarks_backlog')
LOG_OUT_FILE    = os.path.join(BASE_DIR, 'backlog_phase3_lovo_results.json')

EXERCISES = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']

def angle(lm, a, b, c):
    ba = lm[:, a, :2] - lm[:, b, :2]
    bc = lm[:, c, :2] - lm[:, b, :2]
    cos = np.sum(ba * bc, axis=1) / (
        np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1) + 1e-9)
    return np.degrees(np.arccos(np.clip(cos, -1, 1)))

def extract_features(landmarks):
    lm = np.array(landmarks)
    features = []
    angle_seqs = {
        'knee_l':     angle(lm, 23, 25, 27),
        'knee_r':     angle(lm, 24, 26, 28),
        'elbow_l':    angle(lm, 11, 13, 15),
        'elbow_r':    angle(lm, 12, 14, 16),
        'hip_l':      angle(lm, 11, 23, 25),
        'hip_r':      angle(lm, 12, 24, 26),
        'shoulder_l': angle(lm, 13, 11, 23),
        'shoulder_r': angle(lm, 14, 12, 24),
    }
    for seq in angle_seqs.values():
        features.extend([np.mean(seq), np.std(seq), np.min(seq), np.max(seq), np.max(seq) - np.min(seq)])
    for seq in angle_seqs.values():
        features.append(np.mean(np.abs(np.diff(seq))))
    features.append(np.mean(np.abs(angle_seqs['knee_l'] - angle_seqs['knee_r'])))
    features.append(np.mean(np.abs(angle_seqs['shoulder_l'] - angle_seqs['shoulder_r'])))
    return np.array(features)

# Load v3 dataset
if not os.path.exists(V3_DATASET_FILE):
    V3_DATASET_FILE = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'merged_dataset.json')

with open(V3_DATASET_FILE, 'r') as f:
    v3_clips = json.load(f)

print(f"Loaded existing v3 dataset: {len(v3_clips)} clips.")

# Extract features for new Phase 2 squat and lunge clips
pilot_clips = list(v3_clips)
new_clips_added = {'squat': 0, 'lunge': 0}

for ex in ['squat', 'lunge']:
    ex_dir = os.path.join(LM_BACKLOG_DIR, ex)
    if not os.path.exists(ex_dir):
        print(f"ERROR: {ex_dir} does not exist!")
        sys.exit(1)
        
    for fname in sorted(os.listdir(ex_dir)):
        if not fname.endswith('.json'):
            continue
        fpath = os.path.join(ex_dir, fname)
        with open(fpath, 'r') as f:
            cdata = json.load(f)
            
        feats = extract_features(cdata['landmarks'])
        pilot_clips.append({
            'exercise': ex,
            'video_id': cdata['video_id'],
            'clip_id': fname.replace('.json', ''),
            'features': feats.tolist()
        })
        new_clips_added[ex] += 1

print(f"Added {new_clips_added['squat']} new squat clips and {new_clips_added['lunge']} new lunge clips.")
print(f"Total pilot-merged dataset: {len(pilot_clips)} clips across 7 classes.\n")

# Video counts
for ex in EXERCISES:
    vids = set(c['video_id'] for c in pilot_clips if c['exercise'] == ex)
    clips_cnt = sum(1 for c in pilot_clips if c['exercise'] == ex)
    print(f"  {ex:<15}: {len(vids):3d} unique videos | {clips_cnt:4d} clips")

# Run LOVO-CV across all unique video keys
all_video_keys = sorted(list(set((c['exercise'], c['video_id']) for c in pilot_clips)))
print(f"\nRunning LOVO-CV over {len(all_video_keys)} unique video folds...")

fold_results = []
for fold_idx, (held_out_ex, held_out_vid) in enumerate(all_video_keys, 1):
    train_clips = [c for c in pilot_clips if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips  = [c for c in pilot_clips if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

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
        n_jobs=1
    )
    clf.fit(scaler.transform(X_train), le.transform(y_train))
    preds = le.inverse_transform(clf.predict(scaler.transform(X_test)))

    for true, pred in zip(y_test, preds):
        fold_results.append((held_out_ex, held_out_vid, true, pred))

    if fold_idx % 50 == 0 or fold_idx == len(all_video_keys):
        print(f"  Processed {fold_idx}/{len(all_video_keys)} folds...")

y_true = [r[2] for r in fold_results]
y_pred = [r[3] for r in fold_results]

overall_acc = accuracy_score(y_true, y_pred)
report_dict = classification_report(y_true, y_pred, target_names=EXERCISES, output_dict=True)
report_text = classification_report(y_true, y_pred, target_names=EXERCISES)
cm = confusion_matrix(y_true, y_pred, labels=EXERCISES)

# Save LOVO-CV results
with open(LOG_OUT_FILE, 'w') as f:
    json.dump({
        'total_clips': len(pilot_clips),
        'total_folds': len(all_video_keys),
        'accuracy': float(overall_acc),
        'report_dict': report_dict,
        'report_text': report_text,
        'confusion_matrix': cm.tolist()
    }, f, indent=2)

print(f"\nSaved LOVO-CV results to: {LOG_OUT_FILE}\n")

# Print Evaluation Results
print("=" * 80)
print("PHASE 3 PILOT EVALUATION RESULTS")
print("=" * 80)

v3_squat_f1 = 0.34
v3_lunge_f1 = 0.48

new_squat_f1 = report_dict['squat']['f1-score']
new_squat_prec = report_dict['squat']['precision']
new_squat_rec = report_dict['squat']['recall']

new_lunge_f1 = report_dict['lunge']['f1-score']
new_lunge_prec = report_dict['lunge']['precision']
new_lunge_rec = report_dict['lunge']['recall']

print("SQUAT:")
print(f"  v3 F1:        {v3_squat_f1:.2f}")
print(f"  New Pilot F1: {new_squat_f1:.2f} (Precision: {new_squat_prec:.2f}, Recall: {new_squat_rec:.2f})")
print(f"  Change:       {new_squat_f1 - v3_squat_f1:+.2f}")

print("\nLUNGE:")
print(f"  v3 F1:        {v3_lunge_f1:.2f}")
print(f"  New Pilot F1: {new_lunge_f1:.2f} (Precision: {new_lunge_prec:.2f}, Recall: {new_lunge_rec:.2f})")
print(f"  Change:       {new_lunge_f1 - v3_lunge_f1:+.2f}")

print("\n--- SQUAT CONFUSION BREAKDOWN ---")
squat_idx = EXERCISES.index('squat')
squat_row = cm[squat_idx]
print(f"Total True Squat Clips: {sum(squat_row)}")
for idx, ex in enumerate(EXERCISES):
    cnt = squat_row[idx]
    pct = (cnt / sum(squat_row)) * 100
    print(f"  Predicted as {ex:<15}: {cnt:3d} ({pct:5.1f}%)")

print("\n--- LUNGE CONFUSION BREAKDOWN ---")
lunge_idx = EXERCISES.index('lunge')
lunge_row = cm[lunge_idx]
print(f"Total True Lunge Clips: {sum(lunge_row)}")
for idx, ex in enumerate(EXERCISES):
    cnt = lunge_row[idx]
    pct = (cnt / sum(lunge_row)) * 100
    print(f"  Predicted as {ex:<15}: {cnt:3d} ({pct:5.1f}%)")

print("\n--- FULL 7-CLASS CONFUSION MATRIX ---")
header = " | ".join([f"{ex[:7]:<7}" for ex in EXERCISES])
print(f"| {'True \\ Pred':<15} | {header} |")
print(f"|{'-'*17}|" + "|".join(['-'*9 for _ in EXERCISES]) + "|")
for idx, ex in enumerate(EXERCISES):
    row_str = " | ".join([f"{val:<7d}" for val in cm[idx]])
    print(f"| {ex:<15} | {row_str} |")
