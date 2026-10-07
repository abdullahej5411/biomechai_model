"""
Phase 5 of 8 — Final Motion-Sanity Pass on the Combined Dataset
- Combines baseline clean clips (182) and surviving batch 2 clips (329)
- Computes updated combined per-exercise median motion
- Filters any clip falling below 20% of the updated combined median
- Saves logs to model_training/cleanup_v2/phase5_motion_filter_log.json
"""
import os, sys, json, re
import numpy as np

BASE_DIR        = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
CLEANUP_DIR     = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2')
ORIG_LM_DIR     = os.path.join(BASE_DIR, 'data', 'landmarks')
B2_LM_DIR       = os.path.join(BASE_DIR, 'data', 'landmarks_batch2')
OUT_LOG_FILE    = os.path.join(CLEANUP_DIR, 'phase5_motion_filter_log.json')
OUT_ACC_FILE    = os.path.join(CLEANUP_DIR, 'accepted_clips.json')

EXERCISES = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']
ORDER     = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']

# 1. Load baseline exclusions
with open(os.path.join(CLEANUP_DIR, 'excluded_duplicates.json')) as f:
    ex_dups = {(x['exercise'], x['video_id']) for x in json.load(f)}
with open(os.path.join(CLEANUP_DIR, 'excluded_corrupted.json')) as f:
    ex_corr = {(x['exercise'], x['video_id'], str(x['clip']).zfill(2)) for x in json.load(f)}
with open(os.path.join(CLEANUP_DIR, 'excluded_static.json')) as f:
    ex_stat = {(x['exercise'], x['video_id'], str(x['clip']).zfill(2)) for x in json.load(f)}

def overall_motion(landmarks):
    lm = np.array(landmarks)[:, :, :2]
    disp = np.linalg.norm(np.diff(lm, axis=0), axis=2)
    return float(disp.mean())

phase5_results = {}
all_accepted_clips = {}

for exercise in ORDER:
    # A. Collect baseline clean clips
    base_clips = []
    ex_dir = os.path.join(ORIG_LM_DIR, exercise)
    if os.path.exists(ex_dir):
        for fname in sorted(os.listdir(ex_dir)):
            if fname.endswith('.json'):
                parts = fname[:-5].split('_')
                vid = parts[1] if len(parts) == 3 else parts[2]
                clip = parts[-1].replace('clip', '')
                if (exercise, vid) not in ex_dups and (exercise, vid, clip) not in ex_corr and (exercise, vid, clip) not in ex_stat:
                    fpath = os.path.join(ex_dir, fname)
                    with open(fpath, 'r') as jf:
                        lms = json.load(jf)['landmarks']
                    base_clips.append({
                        'source': 'baseline',
                        'filename': fname,
                        'filepath': fpath,
                        'motion': overall_motion(lms)
                    })

    # B. Collect Batch 2 surviving clips
    b2_clips = []
    b2_dir = os.path.join(B2_LM_DIR, exercise)
    if os.path.exists(b2_dir):
        for fname in sorted(os.listdir(b2_dir)):
            if fname.endswith('.json'):
                fpath = os.path.join(b2_dir, fname)
                with open(fpath, 'r') as jf:
                    lms = json.load(jf)['landmarks']
                b2_clips.append({
                    'source': 'batch2',
                    'filename': fname,
                    'filepath': fpath,
                    'motion': overall_motion(lms)
                })

    all_entering = base_clips + b2_clips
    motions = [c['motion'] for c in all_entering]
    
    updated_median = float(np.median(motions)) if motions else 0.0
    updated_threshold = 0.20 * updated_median

    accepted = [c for c in all_entering if c['motion'] >= updated_threshold]
    excluded = [c for c in all_entering if c['motion'] < updated_threshold]

    phase5_results[exercise] = {
        'clips_entering': len(all_entering),
        'baseline_entering': len(base_clips),
        'batch2_entering': len(b2_clips),
        'updated_combined_median': updated_median,
        'updated_threshold': updated_threshold,
        'clips_excluded': len(excluded),
        'clips_finally_accepted': len(accepted),
        'excluded_details': excluded
    }
    all_accepted_clips[exercise] = accepted

# Save phase5 log and accepted clips
with open(OUT_LOG_FILE, 'w') as f:
    json.dump(phase5_results, f, indent=2)

with open(OUT_ACC_FILE, 'w') as f:
    json.dump(all_accepted_clips, f, indent=2)

print("\n" + "=" * 80)
print("PHASE 5 REQUIRED OUTPUT TABLE")
print("=" * 80)
print(f"| {'Exercise':<15} | {'Clips Entering':<16} | {'Updated Combined Median':<25} | {'Clips Excluded':<16} | {'Clips Finally Accepted':<24} |")
print(f"|{'-'*17}|{'-'*18}|{'-'*27}|{'-'*18}|{'-'*26}|")

for ex in ORDER:
    r = phase5_results[ex]
    print(f"| {ex:<15} | {r['clips_entering']:<16} | {r['updated_combined_median']:<25.5f} | {r['clips_excluded']:<16} | {r['clips_finally_accepted']:<24} |")

print("\nDetail of clips excluded in this final pass:")
for ex in ORDER:
    r = phase5_results[ex]
    ex_list = r['excluded_details']
    if ex_list:
        print(f"\n[{ex}] Excluded {len(ex_list)} clip(s) (< 20% of updated median {r['updated_combined_median']:.5f}, threshold {r['updated_threshold']:.5f}):")
        for c in ex_list:
            print(f"  - {c['source']}/{c['filename']} (motion = {c['motion']:.5f})")
    else:
        print(f"\n[{ex}] No clips excluded (100% accepted).")
