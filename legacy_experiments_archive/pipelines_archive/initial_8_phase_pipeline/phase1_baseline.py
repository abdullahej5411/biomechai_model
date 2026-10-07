"""Phase 1 of 8 — Build accepted-video baseline (read-only)."""
import re, os, json
import numpy as np
from collections import defaultdict

BASE_DIR      = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
LANDMARKS_DIR = os.path.join(BASE_DIR, 'data', 'landmarks')
EXCLUDED_FILE = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'excluded_duplicates.json')
OUT_FILE      = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'baseline_videos.json')

EXERCISES = ['squat', 'pushup', 'jumping_jack', 'bicep_curl', 'lunge', 'plank', 'high_knees']

REFERENCE_COUNTS = {
    'jumping_jack': 4,
    'plank':        5,
    'lunge':        5,
    'bicep_curl':   6,
    'pushup':       6,
    'squat':        8,
    'high_knees':   8,
}

# ── Load exclusion list ──────────────────────────────────────────────────────
with open(EXCLUDED_FILE) as f:
    excluded = json.load(f)
excluded_set = {(r['exercise'], r['video_id']) for r in excluded}
print("Loaded", len(excluded_set), "excluded (duplicate) video records.\n")

# ── Signature function (exact spec from Phase 1 instructions) ───────────────
def video_signature(clip_dict):
    parts = [np.round(np.array(clip_dict[c]), 4).flatten() for c in sorted(clip_dict)]
    return tuple(np.concatenate(parts)) if parts else None

# ── Build baseline per exercise ──────────────────────────────────────────────
baseline = {}

for ex in EXERCISES:
    ex_dir = os.path.join(LANDMARKS_DIR, ex)
    if not os.path.isdir(ex_dir):
        print("  WARNING:", ex, "directory missing")
        baseline[ex] = []
        continue

    # Group clips by video_id, skipping excluded videos
    clips_by_vid = defaultdict(dict)
    for fname in sorted(os.listdir(ex_dir)):
        m = re.match(r'^' + re.escape(ex) + r'_(\w+)_clip(\d+)\.json$', fname)
        if not m:
            continue
        vid_id  = m.group(1)
        clip_id = m.group(2)
        if (ex, vid_id) in excluded_set:
            continue  # skip duplicate videos
        fpath = os.path.join(ex_dir, fname)
        with open(fpath) as f:
            data = json.load(f)
        clips_by_vid[vid_id][clip_id] = data['landmarks']

    # Compute signature per video_id
    entries = []
    for vid_id in sorted(clips_by_vid.keys()):
        sig = video_signature(clips_by_vid[vid_id])
        entries.append({
            'video_id':  vid_id,
            'signature': list(sig) if sig is not None else []
        })

    baseline[ex] = entries
    vid_ids = [e['video_id'] for e in entries]
    print("  " + ex + ": " + str(len(entries)) + " accepted videos -> " + str(vid_ids))

# ── Save baseline_videos.json ────────────────────────────────────────────────
with open(OUT_FILE, 'w') as f:
    json.dump(baseline, f, indent=2)

print()
print("baseline_videos.json saved to:")
print("  " + OUT_FILE)
print()

# ── Print required output table ──────────────────────────────────────────────
print("| Exercise | Reference count | Your count | Match? |")
print("|---|---|---|---|")
ORDER = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']
all_match = True
for ex in ORDER:
    ref   = REFERENCE_COUNTS[ex]
    count = len(baseline.get(ex, []))
    match = "YES" if count == ref else "NO -- DISCREPANCY"
    if count != ref:
        all_match = False
    print("| " + ex + " | " + str(ref) + " | " + str(count) + " | " + match + " |")

print()
if all_match:
    print("All counts match the reference. Baseline is consistent with cleanup_v2 findings.")
else:
    print("WARNING: One or more counts do not match reference. Investigate before proceeding.")
