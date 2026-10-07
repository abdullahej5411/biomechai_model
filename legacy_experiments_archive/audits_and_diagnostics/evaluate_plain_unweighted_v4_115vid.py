"""
BioMechAI — Plain Unweighted RF v4 Evaluation on 115 Validation Videos
Evaluates the exact unweighted Random Forest v4 model (Phase 5 hyperparameters)
over the 115 held-out validation video folds to produce an unconfounded head-to-head baseline.
Outputs: model_training/cleanup_v4/plain_unweighted_lovo_115vid_results.json
"""
import os, json, pickle, time, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v4_dataset_file = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4', 'merged_dataset.json')
val_pkl_file = os.path.join(BASE_DIR, 'model_training', 'cleanup_v5', 'posec3d_data', 'custom_dataset_val.pkl')
out_file = os.path.join(BASE_DIR, 'model_training', 'cleanup_v4', 'plain_unweighted_lovo_115vid_results.json')

print("Starting plain unweighted v4 LOVO-CV on 115 held-out videos...")
t0 = time.time()

# 1. Load v4 dataset
with open(v4_dataset_file, 'r') as f:
    v4_clips = json.load(f)
print(f"Loaded v4 dataset: {len(v4_clips)} clips.")

# 2. Load 115 val video IDs
with open(val_pkl_file, 'rb') as f:
    val_data = pickle.load(f)
val_vids = set(x['video_id'] for x in val_data)
print(f"Loaded {len(val_vids)} val video IDs.")

# 3. Find unique (exercise, video_id) folds for these 115 videos in v4
val_video_keys = sorted(list(set((c['exercise'], c['video_id']) for c in v4_clips if c['video_id'] in val_vids)))
print(f"Found {len(val_video_keys)} unique video folds matching the 115 val videos.")

# 4. Run LOVO-CV folds for each of the 115 videos
# Plain unweighted: exactly matching Phase 5 (run_backlog_phase5.py)
fold_results_plain_v4 = []

for idx, (held_out_ex, held_out_vid) in enumerate(val_video_keys, 1):
    train_clips = [c for c in v4_clips if (c['exercise'], c['video_id']) != (held_out_ex, held_out_vid)]
    test_clips  = [c for c in v4_clips if (c['exercise'], c['video_id']) == (held_out_ex, held_out_vid)]

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

    for true, pred in zip(y_test, preds):
        fold_results_plain_v4.append({
            'exercise': held_out_ex,
            'video_id': held_out_vid,
            'true': true,
            'pred': pred
        })

    if idx % 25 == 0 or idx == len(val_video_keys):
        print(f"  Processed {idx}/{len(val_video_keys)} folds... ({time.time() - t0:.1f}s)")

# 5. Save results to JSON
with open(out_file, 'w') as f:
    json.dump({
        'total_clips': len(fold_results_plain_v4),
        'total_folds': len(val_video_keys),
        'fold_results': fold_results_plain_v4
    }, f, indent=2)
print(f"\nSaved plain unweighted v4 115-video results to: {out_file}")

# 6. Summary metrics
classes = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']
y_true = [r['true'] for r in fold_results_plain_v4]
y_pred = [r['pred'] for r in fold_results_plain_v4]

acc = accuracy_score(y_true, y_pred)
cr = classification_report(y_true, y_pred, labels=classes, output_dict=True)
recalls = [cr[c]['recall'] for c in classes]
macro_recall = np.mean(recalls)

print(f"\n=======================================================")
print(f"PLAIN UNWEIGHTED RF v4 on 115 VAL VIDEOS ({len(fold_results_plain_v4)} clips):")
print(f"Top-1 Accuracy: {acc:.4f} ({acc*100:.2f}%)")
print(f"Macro Recall:   {macro_recall:.4f} ({macro_recall*100:.2f}%)")
print(f"Total time: {time.time() - t0:.1f}s")
