"""
Comprehensive, dataset-wide, CROSS-EXERCISE duplicate sweep.

Every prior dedup check in this project was scoped to a single exercise folder at a time.
This is the first pass that ignores exercise-folder boundaries entirely and checks EVERY video file
against EVERY other video file in the whole project, to catch cases like
lunge_04_13.mp4 / pushup_07_06.mp4 / squat_b2_04.mp4 -- one physical video mislabeled under
three different exercises.

Read-only. Does not delete or move anything -- only reports findings.
"""
import os
import hashlib
from collections import defaultdict
import json

BASE_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'

# All video source roots in the project
ROOTS = [
    os.path.join(BASE_DIR, 'data', 'raw_videos'),
    os.path.join(BASE_DIR, 'data', 'raw_videos_batch2'),
]

def md5_full(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

print("Scanning all video files across all roots (ignoring exercise-folder boundaries)...")

hash_to_files = defaultdict(list)  # hash -> [(exercise, filename, full_path, size), ...]
total_files = 0

for root in ROOTS:
    if not os.path.isdir(root):
        print(f"  WARNING: root not found: {root}")
        continue
    for exercise in sorted(os.listdir(root)):
        ex_path = os.path.join(root, exercise)
        if not os.path.isdir(ex_path):
            continue
        for fname in sorted(os.listdir(ex_path)):
            if not fname.endswith('.mp4'):
                continue
            full_path = os.path.join(ex_path, fname)
            size = os.path.getsize(full_path)
            h = md5_full(full_path)
            hash_to_files[h].append((exercise, fname, full_path, size))
            total_files += 1

print(f"Total video files scanned: {total_files}")
print(f"Total distinct content hashes: {len(hash_to_files)}\n")

# Separate into: same-exercise duplicate groups (already expected/known) vs
# CROSS-exercise groups (the new, critical finding)
same_exercise_groups = []
cross_exercise_groups = []

for h, files in hash_to_files.items():
    if len(files) < 2:
        continue
    exercises_involved = set(f[0] for f in files)
    if len(exercises_involved) > 1:
        cross_exercise_groups.append((h, files))
    else:
        same_exercise_groups.append((h, files))

print("=" * 70)
print(f"SAME-EXERCISE duplicate groups (expected, already known type): {len(same_exercise_groups)}")
print(f"CROSS-EXERCISE duplicate groups (NEW -- mislabeled content):    {len(cross_exercise_groups)}")
print("=" * 70)

if cross_exercise_groups:
    print("\n!!! CROSS-EXERCISE CONTAMINATION FOUND !!!\n")
    for h, files in cross_exercise_groups:
        exercises_involved = sorted(set(f[0] for f in files))
        print(f"Hash {h} -- appears under {len(exercises_involved)} DIFFERENT exercise labels: "
              f"{exercises_involved}")
        for ex, fname, path, size in files:
            print(f"    [{ex:15s}] {fname:30s} ({size} bytes) -- {path}")
        print()
else:
    print("\nNo cross-exercise contamination found beyond the already-known case "
          "(if that one isn't in this list, check ROOTS paths above).")

# Save full results for the record
output = {
    'total_files_scanned': total_files,
    'total_distinct_hashes': len(hash_to_files),
    'same_exercise_duplicate_groups': len(same_exercise_groups),
    'cross_exercise_duplicate_groups': len(cross_exercise_groups),
    'cross_exercise_details': [
        {
            'hash': h,
            'exercises_involved': sorted(set(f[0] for f in files)),
            'files': [{'exercise': f[0], 'filename': f[1], 'path': f[2], 'size': f[3]} for f in files]
        }
        for h, files in cross_exercise_groups
    ]
}
OUTPUT_PATH = os.path.join(BASE_DIR, 'cross_exercise_contamination_report.json')
with open(OUTPUT_PATH, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nFull results saved to {OUTPUT_PATH}")

print("\n=== Recommendation ===")
if cross_exercise_groups:
    total_contaminated_files = sum(len(files) for _, files in cross_exercise_groups)
    print(f"{len(cross_exercise_groups)} distinct videos are mislabeled across a total of "
          f"{total_contaminated_files} file entries. For each cross-exercise group, EXCLUDE "
          f"ALL copies from ALL exercise categories entirely -- do not attempt to keep one "
          f"under a 'best guess' label, since the video's actual content (single exercise vs. "
          f"multi-exercise compilation) has not been manually verified. This is the safe "
          f"default given time constraints; if time allows later, these specific videos could "
          f"be manually reviewed to see if a portion is salvageable under one correct label.")
else:
    print("Clear to proceed -- no further cross-exercise contamination detected in this sweep.")
