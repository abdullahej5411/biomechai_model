"""
BioMechAI — Exercise Classifier Data Cleanup & Honest Retrain
Full pipeline: Phase 0 -> Phase 6
Run from: d:/Study Folder/Semester 8/FYP-I/Final Evaluation/fypbiomechai/biomechai_model/
"""
import re, os, sys, json, warnings
import numpy as np

# --- PATHS ------------------------------------------------------------------
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
LANDMARKS_DIR   = os.path.join(BASE_DIR, "data", "landmarks")
RAW_VIDEOS_DIR  = os.path.join(BASE_DIR, "data", "raw_videos")
MODELS_DIR      = os.path.join(BASE_DIR, "models")
CLEANUP_DIR     = os.path.join(BASE_DIR, "model_training", "cleanup_v2")
EXERCISES       = ['squat', 'pushup', 'jumping_jack', 'bicep_curl', 'lunge', 'plank', 'high_knees']

os.makedirs(CLEANUP_DIR, exist_ok=True)

# --- LOGGING ----------------------------------------------------------------
report_lines = []

def log(msg=""):
    print(msg)
    report_lines.append(msg)

def section(title):
    bar = "=" * 70
    log()
    log(bar)
    log("  " + title)
    log(bar)


# ============================================================================
#  PHASE 0 -- Verify repo structure
# ============================================================================
section("PHASE 0 -- Verify repo structure")

phase0_lines = []

def check_path(label, path):
    exists = os.path.exists(path)
    status = "FOUND" if exists else "MISSING"
    msg = "  [" + status + "] " + label + ": " + path
    log(msg)
    phase0_lines.append(msg)
    return exists

# 1. raw_videos
raw_ok = check_path("data/raw_videos/", RAW_VIDEOS_DIR)
if raw_ok:
    raw_subdirs = [d for d in os.listdir(RAW_VIDEOS_DIR)
                   if os.path.isdir(os.path.join(RAW_VIDEOS_DIR, d))]
    log("      Subfolders: " + str(sorted(raw_subdirs)))
    for ex in EXERCISES:
        marker = "OK" if ex in raw_subdirs else "MISSING"
        log("        [" + marker + "] " + ex)

# 2. landmarks
lm_ok = check_path("data/landmarks/", LANDMARKS_DIR)
if lm_ok:
    lm_subdirs = [d for d in os.listdir(LANDMARKS_DIR)
                  if os.path.isdir(os.path.join(LANDMARKS_DIR, d))]
    log("      Subfolders: " + str(sorted(lm_subdirs)))
    for ex in EXERCISES:
        ex_dir = os.path.join(LANDMARKS_DIR, ex)
        if os.path.isdir(ex_dir):
            files = [f for f in os.listdir(ex_dir) if f.endswith(".json")]
            log("        [OK] " + ex + ": " + str(len(files)) + " json files")
        else:
            log("        [MISSING] " + ex + ": subfolder MISSING")

# 3. Python scripts
check_path("extract_landmarks.py", os.path.join(BASE_DIR, "extract_landmarks.py"))
check_path("train_model.py",       os.path.join(BASE_DIR, "train_model.py"))
check_path("models/exercise_classifier.pkl", os.path.join(MODELS_DIR, "exercise_classifier.pkl"))
check_path("models/scaler.pkl",              os.path.join(MODELS_DIR, "scaler.pkl"))
check_path("models/label_encoder.pkl",       os.path.join(MODELS_DIR, "label_encoder.pkl"))

log()
log("  NOTE: Instructions reference 'model_training/' subdirectory, but in this repo")
log("  the scripts live at the repo root and models/ is also at the repo root.")
log("  All later phases use the actual root-level paths.")

# 4. server/server.py
server_path = os.path.join(BASE_DIR, "server", "server.py")
server_exists = check_path("server/server.py", server_path)
if not server_exists:
    log("  NOTE: server/server.py does not exist. Cannot audit model-mismatch.")
    log("        (Out of scope per instructions Section 9 -- noted only.)")

log()
log("PHASE 0 COMPLETE")


# ============================================================================
#  HELPER -- load clips
# ============================================================================
def load_all_clips():
    clips = []
    for ex in EXERCISES:
        ex_dir = os.path.join(LANDMARKS_DIR, ex)
        if not os.path.isdir(ex_dir):
            continue
        for fname in sorted(os.listdir(ex_dir)):
            m = re.match(r'^' + re.escape(ex) + r'_(\w+)_clip(\d+)\.json$', fname)
            if not m:
                continue
            vid_id  = m.group(1)
            clip_id = m.group(2)
            fpath   = os.path.join(ex_dir, fname)
            try:
                with open(fpath) as f:
                    data = json.load(f)
                lm = data.get("landmarks")
                if lm is None:
                    raise ValueError("No 'landmarks' key in JSON")
                clips.append({
                    "exercise": ex,
                    "video_id": vid_id,
                    "clip_id":  clip_id,
                    "fname":    fname,
                    "fpath":    fpath,
                    "landmarks": lm,
                })
            except Exception as e:
                print("  LOAD ERROR " + fname + ": " + str(e))
    return clips

all_clips_raw = load_all_clips()
log("\nLoaded " + str(len(all_clips_raw)) + " clips total across " + str(len(EXERCISES)) + " exercises.")


# ============================================================================
#  PHASE 1 -- Read-only analysis
# ============================================================================
section("PHASE 1 -- Read-only analysis")

# -- 1a: Duplicate detection -------------------------------------------------
log("\n-- 1a: Duplicate video detection --")

def video_signature(clip_list):
    parts = [np.round(np.array(c["landmarks"]), 4).flatten()
             for c in sorted(clip_list, key=lambda c: c["clip_id"])]
    if not parts:
        return None
    return tuple(np.concatenate(parts))

from collections import defaultdict
clips_by_vid = defaultdict(list)
for c in all_clips_raw:
    clips_by_vid[(c["exercise"], c["video_id"])].append(c)

duplicate_records = []
excluded_video_keys = set()

for ex in EXERCISES:
    keys = sorted([k for k in clips_by_vid if k[0] == ex], key=lambda k: k[1])
    seen = {}
    dups = []
    for (exercise, vid_id) in keys:
        sig = video_signature(clips_by_vid[(exercise, vid_id)])
        if sig in seen:
            dups.append((vid_id, seen[sig]))
            excluded_video_keys.add((exercise, vid_id))
            duplicate_records.append({
                "exercise": exercise,
                "video_id": vid_id,
                "duplicate_of_video_id": seen[sig]
            })
        else:
            seen[sig] = vid_id

    unique_count = len(seen)
    log("  " + ex + ": " + str(len(keys)) + " videos total, " +
        str(unique_count) + " unique signatures, " + str(len(dups)) + " duplicates")
    for dup_vid, orig_vid in dups:
        log("    -> " + ex + "_" + dup_vid + " is a duplicate of " + ex + "_" + orig_vid)

log("\n  Total duplicate videos: " + str(len(duplicate_records)))

# -- 1b: Corrupted / extraction-failed clips ---------------------------------
log("\n-- 1b: Corrupted clip detection --")

def is_corrupted(landmarks):
    lm = np.array(landmarks)
    if np.isnan(lm).any():
        return True, "nan_values"
    if lm.shape[0] < 90:
        return True, "incomplete_frames (got " + str(lm.shape[0]) + ")"
    if np.allclose(lm, lm[0], atol=1e-6):
        return True, "frozen_identical_frames"
    return False, None

corrupted_records = []
for c in all_clips_raw:
    bad, reason = is_corrupted(c["landmarks"])
    if bad:
        corrupted_records.append({
            "exercise": c["exercise"],
            "video_id": c["video_id"],
            "clip":     c["clip_id"],
            "reason":   reason,
            "fname":    c["fname"],
        })
        log("  CORRUPTED: " + c["fname"] + "  reason=" + reason)

log("\n  Total corrupted clips: " + str(len(corrupted_records)))
if not corrupted_records:
    log("  (None found)")

# -- 1c: Static / non-exercise clips -----------------------------------------
log("\n-- 1c: Static (low-motion) clip detection --")

def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    diffs = np.diff(lm, axis=0)
    disp  = np.linalg.norm(diffs, axis=2)
    return disp.mean()

corrupted_fnames = {r["fname"] for r in corrupted_records}
motion_by_ex     = defaultdict(list)

for c in all_clips_raw:
    if c["fname"] in corrupted_fnames:
        continue
    m_val = overall_motion(c["landmarks"])
    motion_by_ex[c["exercise"]].append((m_val, c))

static_records = []
for ex in EXERCISES:
    motions = motion_by_ex[ex]
    if not motions:
        continue
    vals   = [mv for mv, _ in motions]
    median = np.median(vals)
    thresh = 0.20 * median
    flagged = [(mv, c) for mv, c in motions if mv < thresh]
    log("  " + ex + ": median motion=" + format(median, ".5f") +
        ", 20% threshold=" + format(thresh, ".5f") +
        ", flagged=" + str(len(flagged)))
    for mv, c in flagged:
        log("    -> " + c["fname"] + "  motion=" + format(mv, ".5f"))
        static_records.append({
            "exercise":        c["exercise"],
            "video_id":        c["video_id"],
            "clip":            c["clip_id"],
            "motion_value":    float(mv),
            "exercise_median": float(median),
            "fname":           c["fname"],
        })

log("\n  Total static clips flagged: " + str(len(static_records)))
if not static_records:
    log("  (None found)")

# -- 1d: Reproduce current (leaky) baseline accuracy -------------------------
log("\n-- 1d: Reproducing current (leaky) baseline accuracy --")

import sklearn
log("  scikit-learn version installed: " + sklearn.__version__)

def extract_features(landmarks):
    lm = np.array(landmarks)
    features = []

    def angle(a, b, c):
        ba = lm[:, a, :2] - lm[:, b, :2]
        bc = lm[:, c, :2] - lm[:, b, :2]
        cos = np.sum(ba*bc, axis=1) / (
            np.linalg.norm(ba, axis=1) *
            np.linalg.norm(bc, axis=1) + 1e-9)
        return np.degrees(np.arccos(np.clip(cos, -1, 1)))

    angle_seqs = {
        'knee_l':     angle(23, 25, 27),
        'knee_r':     angle(24, 26, 28),
        'elbow_l':    angle(11, 13, 15),
        'elbow_r':    angle(12, 14, 16),
        'hip_l':      angle(11, 23, 25),
        'hip_r':      angle(12, 24, 26),
        'shoulder_l': angle(13, 11, 23),
        'shoulder_r': angle(14, 12, 24),
    }

    for seq in angle_seqs.values():
        features.extend([np.mean(seq), np.std(seq), np.min(seq),
                          np.max(seq), np.max(seq) - np.min(seq)])
    for seq in angle_seqs.values():
        features.append(np.mean(np.abs(np.diff(seq))))
    features.append(np.mean(np.abs(angle_seqs['knee_l']    - angle_seqs['knee_r'])))
    features.append(np.mean(np.abs(angle_seqs['shoulder_l'] - angle_seqs['shoulder_r'])))
    return np.array(features)

X_all_raw, y_all_raw = [], []
for c in all_clips_raw:
    try:
        feat = extract_features(c["landmarks"])
        X_all_raw.append(feat)
        y_all_raw.append(c["exercise"])
        c["features"] = feat
    except Exception as e:
        log("  Feature error " + c["fname"] + ": " + str(e))

X_all_raw = np.array(X_all_raw)
y_all_raw = np.array(y_all_raw)

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

le_base   = LabelEncoder()
y_enc_raw = le_base.fit_transform(y_all_raw)
sc_base   = StandardScaler()
X_sc_raw  = sc_base.fit_transform(X_all_raw)

X_tr, X_te, y_tr, y_te = train_test_split(
    X_sc_raw, y_enc_raw, test_size=0.2, random_state=42, stratify=y_enc_raw)

clf_base = RandomForestClassifier(n_estimators=200, max_depth=15,
                                   min_samples_leaf=2, random_state=42, n_jobs=-1)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    clf_base.fit(X_tr, y_tr)

y_pred_base = clf_base.predict(X_te)
baseline_acc = accuracy_score(y_te, y_pred_base)
cm_base      = confusion_matrix(y_te, y_pred_base)
cr_base      = classification_report(y_te, y_pred_base, target_names=le_base.classes_,
                                     output_dict=False)

log("\n  Phase 1d (leaky) baseline accuracy: " + format(baseline_acc*100, ".2f") + "%")
log("\n  Classification Report (current leaky pipeline):")
for line in cr_base.strip().split("\n"):
    log("    " + line)
log("\n  Confusion Matrix (leaky):")
log("    Classes: " + str(list(le_base.classes_)))
for row in cm_base:
    log("    " + str(list(row)))

# -- Phase 1 Summary ---------------------------------------------------------
log()
log("-- PHASE 1 SUMMARY --")
if duplicate_records:
    log("  Duplicates:    CONFIRMED -- " + str(len(duplicate_records)) + " duplicate video(s)")
else:
    log("  Duplicates:    NOT CONFIRMED -- 0 duplicates found")
if corrupted_records:
    log("  Corrupted:     CONFIRMED -- " + str(len(corrupted_records)) + " corrupted clip(s)")
else:
    log("  Corrupted:     NOT CONFIRMED -- 0 corrupted clips found")
if static_records:
    log("  Static clips:  CONFIRMED -- " + str(len(static_records)) + " static clip(s)")
else:
    log("  Static clips:  NOT CONFIRMED -- 0 static clips found")
log("  Leaky baseline accuracy (Phase 1d): " + format(baseline_acc*100, ".2f") + "%")
log()
log("PHASE 1 COMPLETE")
log("-" * 70)
log("Presenting Phase 1 report before proceeding to Phase 2...\n")


# ============================================================================
#  PHASE 2 -- Clean the data
# ============================================================================
section("PHASE 2 -- Data Cleanup")

excluded_vid_keys_set = {(r["exercise"], r["video_id"]) for r in duplicate_records}
corrupted_fname_set   = {r["fname"] for r in corrupted_records}
static_fname_set      = {r["fname"] for r in static_records}

surviving = list(all_clips_raw)

# 2a
before_2a = len(surviving)
surviving = [c for c in surviving if (c["exercise"], c["video_id"]) not in excluded_vid_keys_set]
after_2a  = len(surviving)
log("\n  2a. Duplicate removal: " + str(before_2a) + " -> " + str(after_2a) +
    " clips (removed " + str(before_2a - after_2a) + ")")

# 2b
before_2b = len(surviving)
surviving = [c for c in surviving if c["fname"] not in corrupted_fname_set]
after_2b  = len(surviving)
log("  2b. Corrupted removal: " + str(before_2b) + " -> " + str(after_2b) +
    " clips (removed " + str(before_2b - after_2b) + ")")

# 2c
before_2c = len(surviving)
surviving = [c for c in surviving if c["fname"] not in static_fname_set]
after_2c  = len(surviving)
log("  2c. Static removal:    " + str(before_2c) + " -> " + str(after_2c) +
    " clips (removed " + str(before_2c - after_2c) + ")")

# 2d
log("\n  2d. Feature matrix for " + str(after_2c) + " surviving clips (already computed).")
for c in surviving:
    if "features" not in c:
        c["features"] = extract_features(c["landmarks"])

log("\n  Clips per exercise after cleanup:")
for ex in EXERCISES:
    ex_clips = [c for c in surviving if c["exercise"] == ex]
    vids     = sorted(set(c["video_id"] for c in ex_clips))
    log("    " + ex + ": " + str(len(ex_clips)) + " clips from " +
        str(len(vids)) + " unique videos " + str(vids))

log()
log("PHASE 2 COMPLETE")


# ============================================================================
#  PHASE 3 -- Minimum viable class size check
# ============================================================================
section("PHASE 3 -- Minimum viable class size check")

phase3_status = {}
log()
for ex in EXERCISES:
    vids = sorted(set(c["video_id"] for c in surviving if c["exercise"] == ex))
    n    = len(vids)
    if n < 4:
        status = "INSUFFICIENT (" + str(n) + " unique videos -- not statistically meaningful)"
    else:
        status = "SUFFICIENT (" + str(n) + " unique videos)"
    phase3_status[ex] = {"videos": n, "sufficient": n >= 4, "status": status}
    log("  " + ex + ": " + status)

log()
log("PHASE 3 COMPLETE")


# ============================================================================
#  PHASE 4 -- LOVO-CV honest evaluation
# ============================================================================
section("PHASE 4 -- Leave-One-Video-Out Cross-Validation (LOVO-CV)")

all_video_keys = sorted(set((c["exercise"], c["video_id"]) for c in surviving))
log("\n  Total unique videos for LOVO-CV: " + str(len(all_video_keys)))

fold_results = []
fold_index   = 0
total_folds  = len(all_video_keys)

for held_out_ex, held_out_vid in all_video_keys:
    fold_index += 1
    train_clips = [c for c in surviving
                   if (c["exercise"], c["video_id"]) != (held_out_ex, held_out_vid)]
    test_clips  = [c for c in surviving
                   if (c["exercise"], c["video_id"]) == (held_out_ex, held_out_vid)]

    if not test_clips or not train_clips:
        log("  SKIP fold " + str(fold_index) + "/" + str(total_folds) +
            ": (" + held_out_ex + ", " + held_out_vid + ") -- empty train or test")
        continue

    X_train = np.array([c["features"] for c in train_clips])
    y_train = np.array([c["exercise"] for c in train_clips])
    X_test  = np.array([c["features"] for c in test_clips])
    y_test  = np.array([c["exercise"] for c in test_clips])

    if held_out_ex not in y_train:
        log("  SKIP fold " + str(fold_index) + "/" + str(total_folds) +
            ": (" + held_out_ex + ", " + held_out_vid + ") -- class not in training set")
        continue

    le_fold     = LabelEncoder().fit(y_train)
    scaler_fold = StandardScaler().fit(X_train)
    clf_fold    = RandomForestClassifier(n_estimators=200, max_depth=15,
                                          min_samples_leaf=2, random_state=42, n_jobs=-1)
    clf_fold.fit(scaler_fold.transform(X_train), le_fold.transform(y_train))

    X_test_sc = scaler_fold.transform(X_test)
    raw_preds = clf_fold.predict(X_test_sc)
    preds     = le_fold.inverse_transform(raw_preds)

    fold_correct = 0
    for true_label, pred_label in zip(y_test, preds):
        correct = true_label == pred_label
        fold_results.append({
            "held_out_exercise": held_out_ex,
            "held_out_video_id": held_out_vid,
            "true_label": true_label,
            "pred_label": pred_label,
            "correct": bool(correct),
        })
        if correct:
            fold_correct += 1

    print("  Fold " + str(fold_index).rjust(3) + "/" + str(total_folds) +
          " [" + held_out_ex + "_" + held_out_vid + "]: " +
          str(fold_correct) + "/" + str(len(test_clips)) + " correct")

# Aggregate LOVO-CV results
if fold_results:
    lovo_acc = float(np.mean([r["correct"] for r in fold_results]))
    true_all = [r["true_label"] for r in fold_results]
    pred_all = [r["pred_label"] for r in fold_results]

    all_classes_lovo = sorted(set(true_all) | set(pred_all))
    cm_lovo   = confusion_matrix(true_all, pred_all, labels=all_classes_lovo)
    cr_lovo   = classification_report(true_all, pred_all, labels=all_classes_lovo,
                                       zero_division=0)

    log("\n  -- LOVO-CV Results --")
    log("  Total predictions: " + str(len(fold_results)))
    log("  LOVO-CV Accuracy:  " + format(lovo_acc*100, ".2f") +
        "%  (vs leaky baseline " + format(baseline_acc*100, ".2f") + "%)")
    log("\n  Per-class metrics (LOVO-CV):")
    for line in cr_lovo.strip().split("\n"):
        log("    " + line)
    log("\n  Confusion Matrix (LOVO-CV):")
    log("    Classes: " + str(all_classes_lovo))
    for row in cm_lovo:
        log("    " + str(list(row)))
else:
    lovo_acc         = None
    cm_lovo          = None
    cr_lovo          = "No LOVO-CV results"
    all_classes_lovo = []
    log("  WARNING: No LOVO-CV fold results produced.")

# Secondary: video-grouped 80/20 split
log("\n  -- Secondary check: video-grouped 80/20 split --")
import random
rng = random.Random(42)
vid_keys_shuffled = list(all_video_keys)
rng.shuffle(vid_keys_shuffled)
split_idx    = max(1, int(len(vid_keys_shuffled) * 0.8))
train_vids_80 = set(vid_keys_shuffled[:split_idx])
test_vids_80  = set(vid_keys_shuffled[split_idx:])

train_80 = [c for c in surviving if (c["exercise"], c["video_id"]) in train_vids_80]
test_80  = [c for c in surviving if (c["exercise"], c["video_id"]) in test_vids_80]

if train_80 and test_80:
    X_t80  = np.array([c["features"] for c in train_80])
    y_t80  = np.array([c["exercise"] for c in train_80])
    X_te80 = np.array([c["features"] for c in test_80])
    y_te80 = np.array([c["exercise"] for c in test_80])

    le80  = LabelEncoder().fit(y_t80)
    sc80  = StandardScaler().fit(X_t80)
    clf80 = RandomForestClassifier(n_estimators=200, max_depth=15,
                                    min_samples_leaf=2, random_state=42, n_jobs=-1)
    clf80.fit(sc80.transform(X_t80), le80.transform(y_t80))

    test_mask = np.array([lbl in le80.classes_ for lbl in y_te80])
    X_te80_f  = X_te80[test_mask]
    y_te80_f  = y_te80[test_mask]
    preds80   = le80.inverse_transform(clf80.predict(sc80.transform(X_te80_f))) if len(X_te80_f) else []
    acc80     = float(accuracy_score(y_te80_f, preds80)) if len(preds80) else float('nan')
    log("  Video-grouped 80/20 accuracy: " + format(acc80*100, ".2f") +
        "%  (train_vids=" + str(len(train_vids_80)) + ", test_vids=" + str(len(test_vids_80)) + ")")
    log("  (Headline is LOVO-CV; this is secondary only)")
else:
    acc80 = float('nan')
    log("  Not enough data for grouped 80/20 split.")

log()
log("PHASE 4 COMPLETE")


# ============================================================================
#  PHASE 5 -- Train final deployable model on all cleaned data
# ============================================================================
section("PHASE 5 -- Train final model on all cleaned data")

X_final_all = np.array([c["features"] for c in surviving])
y_final_all = np.array([c["exercise"] for c in surviving])

le_final     = LabelEncoder().fit(y_final_all)
scaler_final = StandardScaler().fit(X_final_all)
clf_final    = RandomForestClassifier(n_estimators=200, max_depth=15,
                                       min_samples_leaf=2, random_state=42, n_jobs=-1)
clf_final.fit(scaler_final.transform(X_final_all), le_final.transform(y_final_all))

log("\n  Final model trained on " + str(len(surviving)) + " clips.")
log("  Classes: " + str(list(le_final.classes_)))
if lovo_acc is not None:
    log("  Honest accuracy estimate: LOVO-CV = " + format(lovo_acc*100, ".2f") + "%")
log()
log("PHASE 5 COMPLETE")


# ============================================================================
#  PHASE 6 -- Save outputs and write REPORT.md
# ============================================================================
section("PHASE 6 -- Save structured outputs")

import joblib

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)

save_json(os.path.join(CLEANUP_DIR, "excluded_duplicates.json"), duplicate_records)
save_json(os.path.join(CLEANUP_DIR, "excluded_corrupted.json"), corrupted_records)
save_json(os.path.join(CLEANUP_DIR, "excluded_static.json"),    static_records)

lovo_json = {
    "per_fold_results": fold_results,
    "lovo_cv_accuracy": lovo_acc,
    "confusion_matrix": {
        "classes": all_classes_lovo,
        "matrix":  cm_lovo.tolist() if cm_lovo is not None else [],
    },
    "classification_report_text": cr_lovo,
}
save_json(os.path.join(CLEANUP_DIR, "lovo_cv_results.json"), lovo_json)

joblib.dump(clf_final,     os.path.join(CLEANUP_DIR, "exercise_classifier_CLEANED.pkl"))
joblib.dump(scaler_final,  os.path.join(CLEANUP_DIR, "scaler_CLEANED.pkl"))
joblib.dump(le_final,      os.path.join(CLEANUP_DIR, "label_encoder_CLEANED.pkl"))

log("\n  Saved: excluded_duplicates.json")
log("  Saved: excluded_corrupted.json")
log("  Saved: excluded_static.json")
log("  Saved: lovo_cv_results.json")
log("  Saved: exercise_classifier_CLEANED.pkl")
log("  Saved: scaler_CLEANED.pkl")
log("  Saved: label_encoder_CLEANED.pkl")

# --- Write REPORT.md --------------------------------------------------------
log("\n  Writing REPORT.md ...")

surviving_per_ex = {}
for ex in EXERCISES:
    ex_clips = [c for c in surviving if c["exercise"] == ex]
    vids     = sorted(set(c["video_id"] for c in ex_clips))
    surviving_per_ex[ex] = {"clips": len(ex_clips), "unique_videos": len(vids), "video_ids": vids}

def fmt_cm(classes, matrix):
    rows = []
    header = "| True \\ Pred | " + " | ".join(classes) + " |"
    sep    = "|---|" + "---|" * len(classes)
    rows.append(header)
    rows.append(sep)
    for i, cls in enumerate(classes):
        row = "| **" + cls + "** | " + " | ".join(str(v) for v in matrix[i]) + " |"
        rows.append(row)
    return "\n".join(rows)

lovo_cm_md = fmt_cm(all_classes_lovo, cm_lovo.tolist()) if cm_lovo is not None else "N/A"
base_cm_md = fmt_cm(list(le_base.classes_), cm_base.tolist())

# Build dup table
dup_table_rows = []
for r in duplicate_records:
    dup_table_rows.append("| " + r["exercise"] + " | " + r["video_id"] + " | " + r["duplicate_of_video_id"] + " |")
if dup_table_rows:
    dup_table = "| Exercise | Duplicate Video ID | Original Video ID |\n|---|---|---|\n" + "\n".join(dup_table_rows)
else:
    dup_table = "_None found_"

# Build corrupted table
if corrupted_records:
    cor_rows = ["| " + r["exercise"] + " | " + r["video_id"] + " | " + r["clip"] + " | " + r["reason"] + " |"
                for r in corrupted_records]
    corrupted_table = "| Exercise | Video | Clip | Reason |\n|---|---|---|---|\n" + "\n".join(cor_rows)
else:
    corrupted_table = "**None found** -- NOT CONFIRMED (0 corrupted clips)"

# Build static table
if static_records:
    st_rows = ["| " + r["exercise"] + " | " + r["video_id"] + " | " + r["clip"] + " | " +
               format(r["motion_value"], ".5f") + " | " + format(r["exercise_median"], ".5f") + " |"
               for r in static_records]
    static_table = "| Exercise | Video | Clip | Motion | Class Median |\n|---|---|---|---|---|\n" + "\n".join(st_rows)
else:
    static_table = "**None found** -- NOT CONFIRMED (0 static clips below 20% of class median)"

# Build surviving clips table
surv_rows = []
for ex in EXERCISES:
    d   = surviving_per_ex.get(ex, {})
    suf = "OK" if phase3_status.get(ex, {}).get("sufficient", False) else "INSUFFICIENT"
    surv_rows.append("| " + ex + " | " + str(d.get("clips","0")) + " | " +
                     str(d.get("unique_videos","0")) + " | " + suf + " |")
surv_table = "| Exercise | Surviving Clips | Unique Videos | Sufficient? |\n|---|---|---|---|\n" + "\n".join(surv_rows)

# Phase 3 table
phase3_rows = []
for ex in EXERCISES:
    phase3_rows.append("| " + ex + " | " + str(phase3_status[ex]["videos"]) + " | " + phase3_status[ex]["status"] + " |")
phase3_table = "| Exercise | Unique Videos | Status |\n|---|---|---|\n" + "\n".join(phase3_rows)

# Usability verdict
insufficient = [ex for ex, d in phase3_status.items() if not d["sufficient"]]

if lovo_acc is None:
    verdict = ("LOVO-CV could not be completed due to data constraints. "
               "Collect more source videos before trusting any accuracy figure.")
elif insufficient:
    insuf_str = ", ".join(insufficient)
    verdict = (
        "The classifier is **not production-ready**. The following classes are "
        "statistically under-resourced after cleanup: **" + insuf_str + "** (fewer than 4 unique "
        "videos each). Any per-class accuracy figure for these classes is unreliable because "
        "a single unusual video can swing the result. Additionally, the leaky baseline of "
        + format(baseline_acc*100, ".1f") + "% was inflated by training and testing on clips from the same "
        "video; the honest LOVO-CV accuracy is " + format(lovo_acc*100, ".1f") + "%. "
        "Recommendation: collect 4+ additional distinct source videos for each insufficient "
        "class before relying on this model for production use."
    )
elif lovo_acc >= 0.85:
    verdict = (
        "The classifier is **reasonably usable** with an honest LOVO-CV accuracy of "
        + format(lovo_acc*100, ".1f") + "%, well above chance (14.3% for 7 classes). "
        "All classes have 4+ unique source videos. That said, the LOVO-CV accuracy is lower "
        "than the leaky clip-split baseline (" + format(baseline_acc*100, ".1f") + "%), confirming "
        "the original reported accuracy was inflated by data leakage. The model should be "
        "treated as usable but not production-grade; collecting 5-10 more diverse videos "
        "per class would substantially improve reliability."
    )
else:
    verdict = (
        "The classifier's honest LOVO-CV accuracy is " + format(lovo_acc*100, ".1f") + "%, compared to "
        "the inflated leaky baseline of " + format(baseline_acc*100, ".1f") + "%. "
        "The accuracy drop confirms that the original evaluation suffered from data leakage "
        "(clips from the same video in both train and test). "
        "The current data volume is borderline; collecting more diverse source videos per "
        "class is strongly recommended before production deployment."
    )

lovo_acc_str = (format(lovo_acc*100, ".2f") + "%") if lovo_acc is not None else "N/A"
acc80_str    = (format(acc80*100, ".2f") + "%") if not (acc80 != acc80) else "N/A"

report_md = """# BioMechAI -- Data Cleanup & Honest Retrain Report

_Generated: 2026-08-30 | scikit-learn """ + sklearn.__version__ + """_

---

## Phase 0 -- Path Verification

| Path | Status |
|---|---|
| `data/raw_videos/` | """ + ("Found" if raw_ok else "Missing") + """ |
| `data/landmarks/` | """ + ("Found" if lm_ok else "Missing") + """ |
| `extract_landmarks.py` | """ + ("Found (at repo root)" if os.path.exists(os.path.join(BASE_DIR,'extract_landmarks.py')) else "Missing") + """ |
| `train_model.py` | """ + ("Found (at repo root)" if os.path.exists(os.path.join(BASE_DIR,'train_model.py')) else "Missing") + """ |
| `models/exercise_classifier.pkl` | """ + ("Found" if os.path.exists(os.path.join(MODELS_DIR,'exercise_classifier.pkl')) else "Missing") + """ |
| `models/scaler.pkl` | """ + ("Found" if os.path.exists(os.path.join(MODELS_DIR,'scaler.pkl')) else "Missing") + """ |
| `models/label_encoder.pkl` | """ + ("Found" if os.path.exists(os.path.join(MODELS_DIR,'label_encoder.pkl')) else "Missing") + """ |
| `server/server.py` | Missing (not present in this workspace) |

> **Structural discrepancy noted:** Instructions reference `model_training/` as a subfolder
> containing scripts and `models/`. In this repo, scripts live at the repo root and `models/`
> is also at the root. All phases used the actual paths found.
> `server/server.py` does not exist in this workspace -- server/model mismatch cannot be audited
> (noted; out of scope per instructions Section 9).

---

## Phase 1 -- Confirmed Findings

### 1a. Duplicate videos

""" + dup_table + """

**Total duplicates: """ + str(len(duplicate_records)) + """** -- """ + ("CONFIRMED" if duplicate_records else "NOT CONFIRMED") + """

### 1b. Corrupted clips

""" + corrupted_table + """

### 1c. Static / low-motion clips

""" + static_table + """

### 1d. Current (leaky) baseline accuracy

**""" + format(baseline_acc*100, ".2f") + """%** -- reproduced by applying the original clip-level `train_test_split`
(`test_size=0.2, random_state=42, stratify=y`) on all """ + str(len(all_clips_raw)) + """ raw clips.
This number is **inflated** because clips from the same source video appear in both
training and test sets, allowing the classifier to memorize inter-clip patterns from
the same recording.

---

## Phase 2 -- Data Cleanup Steps

| Step | Before | After | Removed |
|---|---|---|---|
| 2a -- Duplicate videos | """ + str(before_2a) + """ clips | """ + str(after_2a) + """ clips | """ + str(before_2a - after_2a) + """ clips |
| 2b -- Corrupted clips  | """ + str(before_2b) + """ clips | """ + str(after_2b) + """ clips | """ + str(before_2b - after_2b) + """ clips |
| 2c -- Static clips     | """ + str(before_2c) + """ clips | """ + str(after_2c) + """ clips | """ + str(before_2c - after_2c) + """ clips |

### Surviving clips per exercise

""" + surv_table + """

---

## Phase 3 -- Minimum Viable Class Size

""" + phase3_table + """

---

## Phase 4 -- Honest Evaluation

### Leaky Baseline (Phase 1d) vs. LOVO-CV

| Metric | Value |
|---|---|
| Leaky clip-split accuracy | **""" + format(baseline_acc*100, ".2f") + """%** |
| Honest LOVO-CV accuracy | **""" + lovo_acc_str + """** |
| Secondary video-grouped 80/20 | **""" + acc80_str + """** |

### LOVO-CV Confusion Matrix

""" + lovo_cm_md + """

### LOVO-CV Classification Report

```
""" + cr_lovo + """
```

### Leaky Baseline Confusion Matrix (for reference)

""" + base_cm_md + """

---

## Phase 5 -- Final Model

Trained on all **""" + str(len(surviving)) + """ surviving clips** (no held-out data).
Honest accuracy estimate = LOVO-CV result above.
Artifacts saved with `_CLEANED` suffix in `model_training/cleanup_v2/`.

scikit-learn version used for `_CLEANED.pkl` artifacts: **""" + sklearn.__version__ + """**

---

## Section 7 -- Optional Preventive Measures (Not Implemented)

- [ ] Motion filter added to `extract_landmarks.py` at extraction time
- [ ] Duplicate-download check in `download_videos.py`

These were not implemented in this cleanup pass but are flagged for future work.

---

## Section 8 -- scikit-learn Version Note

The `_CLEANED.pkl` artifacts were produced with **scikit-learn """ + sklearn.__version__ + """**.
If the version that produced the original `models/*.pkl` differs, loading those files
may produce `InconsistentVersionWarning`.

---

## Plain-Language Usability Verdict

""" + verdict + """

---

_All cleanup artifacts saved to `model_training/cleanup_v2/`. Original `data/` and `models/` directories are untouched._
"""

report_path = os.path.join(CLEANUP_DIR, "REPORT.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_md)

log("  REPORT.md written to: " + report_path)
log()
log("PHASE 6 COMPLETE")

# --- Final summary ----------------------------------------------------------
section("ALL PHASES COMPLETE -- DEFINITION OF DONE")
log("  Phase 0: path verification complete")
log("  Phase 1: audit complete (duplicates=" + str(len(duplicate_records)) +
    ", corrupted=" + str(len(corrupted_records)) + ", static=" + str(len(static_records)) + ")")
log("  Phase 2: data cleaned (" + str(after_2c) + " clips survive)")
log("  Phase 3: class-size check complete")
log("  Phase 4: LOVO-CV = " + lovo_acc_str + "  vs  leaky baseline " + format(baseline_acc*100, ".2f") + "%")
log("  Phase 5: final model trained on all " + str(len(surviving)) + " clean clips")
log("  Phase 6: artifacts + REPORT.md saved to model_training/cleanup_v2/")
log()
log("  Cleanup directory: " + CLEANUP_DIR)
log("  REPORT.md:         " + report_path)
