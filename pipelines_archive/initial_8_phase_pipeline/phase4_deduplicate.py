"""
Phase 4 of 8 — Deduplication of Batch 2 candidate videos
- Compares Batch 2 candidate videos against baseline_videos.json (Phase 1)
- Compares Batch 2 candidate videos against each other (intra-batch)
- Uses exact 4-decimal-place landmark signatures
- Saves model_training/cleanup_v2/batch2_duplicates.json
"""
import os, sys, json, re
import numpy as np
from collections import defaultdict

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
LANDMARKS_B2    = os.path.join(BASE_DIR, 'data', 'landmarks_batch2')
BASELINE_FILE   = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'baseline_videos.json')
OUT_DUP_FILE    = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'batch2_duplicates.json')
OUT_SURV_FILE   = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'batch2_surviving_videos.json')

EXERCISES = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']
ORDER     = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']

# 1. Prerequisite verification
if not os.path.exists(BASELINE_FILE):
    print("ERROR: baseline_videos.json (Phase 1) is missing!")
    sys.exit(1)

if not os.path.exists(LANDMARKS_B2):
    print("ERROR: data/landmarks_batch2/ (Phase 3) is missing!")
    sys.exit(1)

with open(BASELINE_FILE, 'r') as f:
    baseline_data = json.load(f)

print("Prerequisites verified: baseline_videos.json and landmarks_batch2/ both found.\n")

# 2. Load all clips from landmarks_batch2
def clip_signature(landmarks):
    return tuple(np.round(np.array(landmarks), 4).flatten())

def full_video_signature(clip_dict):
    parts = [np.round(np.array(clip_dict[c]), 4).flatten() for c in sorted(clip_dict)]
    return tuple(np.concatenate(parts)) if parts else None

# Build baseline signatures per exercise
baseline_sigs_by_ex = {}
for ex, entries in baseline_data.items():
    sigs = {}
    for entry in entries:
        vid_id = entry['video_id']
        sig_list = entry.get('signature', [])
        if sig_list:
            sigs[tuple(sig_list)] = vid_id
    baseline_sigs_by_ex[ex] = sigs

duplicates_list = []
summary_table = []
surviving_by_ex = {}

for exercise in ORDER:
    ex_dir = os.path.join(LANDMARKS_B2, exercise)
    if not os.path.exists(ex_dir):
        print(f"Directory missing for {exercise}")
        continue

    # Group extracted clips by candidate video_id
    clips_by_vid = defaultdict(dict)
    for fname in sorted(os.listdir(ex_dir)):
        m = re.match(rf'^{exercise}_b2_(\w+)_clip(\d+)\.json$', fname)
        if not m:
            continue
        vid_num = m.group(1)
        clip_num = m.group(2)
        fpath = os.path.join(ex_dir, fname)
        with open(fpath, 'r') as f:
            cdata = json.load(f)
        clips_by_vid[vid_num][clip_num] = cdata['landmarks']

    candidates_entering = sorted(clips_by_vid.keys())
    
    seen_batch2_full_sigs = {}
    seen_batch2_clip_sigs = {}
    
    surviving_candidates = []
    
    for vid_id in candidates_entering:
        cdict = clips_by_vid[vid_id]
        vid_name = f"{exercise}_b2_{vid_id}"
        
        # Check against baseline videos
        vid_sig = full_video_signature(cdict)
        
        is_dup = False
        dup_reason = ""
        dup_of = ""
        dup_type = ""
        
        # Check full video signature against baseline
        base_sigs = baseline_sigs_by_ex.get(exercise, {})
        if vid_sig in base_sigs:
            is_dup = True
            dup_of = f"baseline {exercise}_{base_sigs[vid_sig]}"
            dup_type = "existing_baseline"
            dup_reason = "identical full video landmark signature to baseline"
            
        # Also check individual clip signatures against baseline clips
        if not is_dup:
            for clip_id, lms in cdict.items():
                csig = clip_signature(lms)
                # Check intra-batch clip signatures
                if csig in seen_batch2_clip_sigs:
                    is_dup = True
                    dup_of = f"batch2 {exercise}_b2_{seen_batch2_clip_sigs[csig]}"
                    dup_type = "batch2_intra"
                    dup_reason = f"clip {clip_id} identical to clip in {dup_of}"
                    break
                    
        # Check full signature against already accepted batch2 candidates
        if not is_dup and vid_sig in seen_batch2_full_sigs:
            is_dup = True
            dup_of = f"batch2 {exercise}_b2_{seen_batch2_full_sigs[vid_sig]}"
            dup_type = "batch2_intra"
            dup_reason = "identical full video landmark signature to earlier batch2 video"

        if is_dup:
            duplicates_list.append({
                'exercise': exercise,
                'video_id': vid_name,
                'duplicate_of': dup_of,
                'duplicate_type': dup_type,
                'reason': dup_reason
            })
            print(f"  [REJECTED DUPLICATE] {vid_name} -> duplicate of {dup_of} ({dup_reason})")
        else:
            surviving_candidates.append(vid_name)
            seen_batch2_full_sigs[vid_sig] = vid_id
            for clip_id, lms in cdict.items():
                csig = clip_signature(lms)
                seen_batch2_clip_sigs[csig] = vid_id

    surviving_by_ex[exercise] = surviving_candidates
    summary_table.append({
        'exercise': exercise,
        'entering': len(candidates_entering),
        'surviving': len(surviving_candidates),
        'rejected': len(candidates_entering) - len(surviving_candidates)
    })
    print(f"Exercise {exercise:<15}: {len(candidates_entering)} entering -> {len(surviving_candidates)} surviving ({len(candidates_entering) - len(surviving_candidates)} rejected)")

# Save batch2_duplicates.json
with open(OUT_DUP_FILE, 'w') as f:
    json.dump(duplicates_list, f, indent=2)
print(f"\nbatch2_duplicates.json saved to: {OUT_DUP_FILE}")

# Save surviving list
with open(OUT_SURV_FILE, 'w') as f:
    json.dump(surviving_by_ex, f, indent=2)

# Print required output table
print("\n" + "=" * 70)
print("PHASE 4 REQUIRED OUTPUT TABLE")
print("=" * 70)
print(f"| {'Exercise':<15} | {'Candidates Entering':<20} | {'Candidates Surviving':<20} | {'Rejected (Duplicates)':<22} |")
print(f"|{'-'*17}|{'-'*22}|{'-'*22}|{'-'*24}|")

for row in summary_table:
    print(f"| {row['exercise']:<15} | {row['entering']:<20} | {row['surviving']:<20} | {row['rejected']:<22} |")

print("\nDuplicates summary:")
if duplicates_list:
    for d in duplicates_list:
        print(f"  - {d['video_id']}: duplicate of {d['duplicate_of']} ({d['reason']})")
else:
    print("  No duplicate videos found (all candidate videos are genuinely unique).")
