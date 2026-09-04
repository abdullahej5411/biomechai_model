"""
Diagnose why some cross-exercise-excluded videos didn't actually get removed from
merged_dataset.json -- for each of the 63 intended exclusions, report exactly how many
clips (if any) were actually removed. Any pair with ZERO removed clips reveals a
video_id naming mismatch that needs fixing before v5 can be trusted.
"""
import json
from collections import defaultdict

MERGED_V4_PATH = r'model_training\cleanup_v4\merged_dataset.json'
CONTAMINATION_REPORT_PATH = 'cross_exercise_contamination_report.json'

with open(CONTAMINATION_REPORT_PATH) as f:
    contamination = json.load(f)
with open(MERGED_V4_PATH) as f:
    v4_clips = json.load(f)

# Build the exact set of (exercise, video_id) intended for exclusion
excluded_video_ids = set()
for group in contamination['cross_exercise_details']:
    for f in group['files']:
        video_id = f['filename'].replace('.mp4', '')
        excluded_video_ids.add((f['exercise'], video_id))

# For each intended exclusion, count how many clips in v4 actually match it
v4_video_ids_seen = set((c['exercise'], c['video_id']) for c in v4_clips)

print(f"Total intended exclusions: {len(excluded_video_ids)}")
print(f"Total distinct (exercise, video_id) pairs actually present in merged_dataset.json: "
      f"{len(v4_video_ids_seen)}\n")

matched = []
unmatched = []
for ex, vid in sorted(excluded_video_ids):
    if (ex, vid) in v4_video_ids_seen:
        n_clips = sum(1 for c in v4_clips if c['exercise'] == ex and c['video_id'] == vid)
        matched.append((ex, vid, n_clips))
    else:
        unmatched.append((ex, vid))

print(f"Matched (successfully found and removable): {len(matched)}")
print(f"UNMATCHED (silently failed to exclude anything): {len(unmatched)}\n")

if unmatched:
    print("=== UNMATCHED exclusion targets -- these are why v5 is incomplete ===")
    for ex, vid in unmatched:
        print(f"  [{ex}] intended video_id = '{vid}'")

    # For each unmatched target, show what video_ids DO exist in merged_dataset.json
    # for that exercise, to help spot the naming pattern difference
    print("\n=== Sample of ACTUAL video_id values present in merged_dataset.json, "
          "per exercise with unmatched targets ===")
    unmatched_exercises = set(ex for ex, vid in unmatched)
    for ex in sorted(unmatched_exercises):
        actual_ids = sorted(set(c['video_id'] for c in v4_clips if c['exercise'] == ex))
        print(f"\n  {ex} -- {len(actual_ids)} distinct video_id values in merged_dataset.json:")
        print(f"    {actual_ids[:15]}{' ...' if len(actual_ids) > 15 else ''}")
        this_ex_unmatched = [vid for e, vid in unmatched if e == ex]
        print(f"  {ex} -- unmatched targets we were trying to find: {this_ex_unmatched}")
