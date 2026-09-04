"""
Backlog Phase 1 of 5:
Step 1: Fresh-recompute baseline vs backlog exclusions (Set A: <500KiB, Set B: Baseline MD5 Duplicates, Overlap, Union, Clean Pool).
Step 2: Full-file MD5 intra-backlog deduplication on the clean pool.
Saves: backlog_clean_deduped_candidates.json
"""
import os, sys, json, hashlib
from collections import defaultdict, Counter

BASE_DIR  = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
RAW_DIR   = os.path.join(BASE_DIR, 'data', 'raw_videos')
LM_DIR    = os.path.join(BASE_DIR, 'data', 'landmarks')
OUT_FILE  = os.path.join(BASE_DIR, 'backlog_clean_deduped_candidates.json')

exercises = sorted([d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))])

def md5_full(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def get_lm_video_stems(exercise):
    lm_path = os.path.join(LM_DIR, exercise)
    stems = set()
    if os.path.isdir(lm_path):
        for f in os.listdir(lm_path):
            if f.endswith('.json'):
                parts = f.rsplit('_clip', 1)
                if len(parts) == 2:
                    stems.add(parts[0])
    return stems

# --- STEP 1: Fresh File Audit & Exclusion Recomputation ---
all_files = []
for ex in exercises:
    ex_path = os.path.join(RAW_DIR, ex)
    for f in os.listdir(ex_path):
        all_files.append((ex, f, os.path.join(ex_path, f)))

ext_counts = Counter(os.path.splitext(f)[1].lower() for _, f, _ in all_files)
print("=== STEP 1: DISK AUDIT ===")
print(f"Total raw directory entries: {len(all_files)}")
for ext, cnt in ext_counts.most_common():
    print(f"  {ext if ext else '(no ext)'}: {cnt}")
print()

step1_table = []
all_clean_pool_files = [] # list of (ex, filename, full_path)

for ex in exercises:
    ex_raw = os.path.join(RAW_DIR, ex)
    lm_stems = get_lm_video_stems(ex)

    baseline_files = []
    backlog_files = []

    for f in sorted(os.listdir(ex_raw)):
        if not f.endswith('.mp4'):
            continue
        full_path = os.path.join(ex_raw, f)
        size = os.path.getsize(full_path)
        stem = f.replace('.mp4', '')
        
        if stem in lm_stems:
            baseline_files.append((f, size, full_path))
        else:
            backlog_files.append((f, size, full_path))

    # Fast size lookup for baseline matches
    backlog_by_size = {}
    for f, size, path in backlog_files:
        backlog_by_size.setdefault(size, []).append((f, path))

    base_dups = set()
    for bf_name, bf_size, bf_path in baseline_files:
        matches = backlog_by_size.get(bf_size, [])
        for m_name, m_path in matches:
            if md5_full(bf_path) == md5_full(m_path):
                base_dups.add(m_name)

    small_files = set(f for f, size, _ in backlog_files if size < 512 * 1024)
    overlap = small_files & base_dups
    union_excl = small_files | base_dups
    
    clean_pool = [ (f, path) for f, size, path in backlog_files if f not in union_excl ]
    for f, path in clean_pool:
        all_clean_pool_files.append((ex, f, path))

    step1_table.append({
        'exercise': ex,
        'total_mp4': len(baseline_files) + len(backlog_files),
        'baseline': len(baseline_files),
        'backlog': len(backlog_files),
        'small': len(small_files),
        'base_dups': len(base_dups),
        'overlap': len(overlap),
        'union_excl': len(union_excl),
        'clean_pool': len(clean_pool)
    })

# --- STEP 2: Intra-Backlog MD5 Deduplication on Clean Pool ---
print("=== STEP 2: INTRA-BACKLOG DEDUPLICATION ===")
step2_table = []
final_dataset = {}

for ex in exercises:
    ex_clean_files = [(f, path) for e, f, path in all_clean_pool_files if e == ex]
    
    # Hash every clean candidate
    hash_to_files = defaultdict(list)
    for f, path in ex_clean_files:
        h = md5_full(path)
        hash_to_files[h].append((f, path))
    
    kept_representatives = []
    duplicate_records = []
    
    for h, files in hash_to_files.items():
        # Keep the first file as the unique representative
        rep_file, rep_path = files[0]
        kept_representatives.append({
            'filename': rep_file,
            'filepath': rep_path,
            'md5': h,
            'filesize': os.path.getsize(rep_path)
        })
        if len(files) > 1:
            duplicate_records.append({
                'representative': rep_file,
                'md5': h,
                'duplicates': [f for f, _ in files[1:]]
            })

    final_dataset[ex] = {
        'unique_count': len(kept_representatives),
        'clean_pool_before_dedup': len(ex_clean_files),
        'intra_backlog_duplicate_groups': len(duplicate_records),
        'intra_backlog_duplicate_files_pruned': len(ex_clean_files) - len(kept_representatives),
        'unique_candidates': kept_representatives,
        'duplicates_logged': duplicate_records
    }

    step2_table.append({
        'exercise': ex,
        'clean_before': len(ex_clean_files),
        'dup_groups': len(duplicate_records),
        'dups_pruned': len(ex_clean_files) - len(kept_representatives),
        'final_unique': len(kept_representatives)
    })

# Save output JSON
with open(OUT_FILE, 'w') as f:
    json.dump(final_dataset, f, indent=2)

print(f"Saved final deduplicated candidate list to: {OUT_FILE}\n")

# Print Step 1 formatted table
print("=" * 105)
print("STEP 1 RECOMPUTED TABLE")
print("=" * 105)
print(f"| {'Exercise':<15} | {'Total MP4':<10} | {'Baseline':<9} | {'Backlog':<8} | {'<500KiB':<8} | {'Base Dups':<10} | {'Overlap':<8} | {'Union Excl':<11} | {'Clean Pool':<11} |")
print(f"|{'-'*17}|{'-'*12}|{'-'*11}|{'-'*10}|{'-'*10}|{'-'*12}|{'-'*10}|{'-'*13}|{'-'*13}|")

tot_mp4 = sum(r['total_mp4'] for r in step1_table)
tot_base = sum(r['baseline'] for r in step1_table)
tot_back = sum(r['backlog'] for r in step1_table)
tot_small = sum(r['small'] for r in step1_table)
tot_bdup = sum(r['base_dups'] for r in step1_table)
tot_ovlp = sum(r['overlap'] for r in step1_table)
tot_un = sum(r['union_excl'] for r in step1_table)
tot_cln = sum(r['clean_pool'] for r in step1_table)

for r in step1_table:
    print(f"| {r['exercise']:<15} | {r['total_mp4']:<10} | {r['baseline']:<9} | {r['backlog']:<8} | {r['small']:<8} | {r['base_dups']:<10} | {r['overlap']:<8} | {r['union_excl']:<11} | {r['clean_pool']:<11} |")

print(f"|{'-'*17}|{'-'*12}|{'-'*11}|{'-'*10}|{'-'*10}|{'-'*12}|{'-'*10}|{'-'*13}|{'-'*13}|")
print(f"| {'TOTAL':<15} | {tot_mp4:<10} | {tot_base:<9} | {tot_back:<8} | {tot_small:<8} | {tot_bdup:<10} | {tot_ovlp:<8} | {tot_un:<11} | {tot_cln:<11} |")

print("\n" + "=" * 85)
print("STEP 2 INTRA-BACKLOG DEDUPLICATION TABLE")
print("=" * 85)
print(f"| {'Exercise':<15} | {'Clean Before Dedup':<20} | {'Dup Groups Found':<18} | {'Dups Pruned':<13} | {'Final Unique Count':<20} |")
print(f"|{'-'*17}|{'-'*22}|{'-'*20}|{'-'*15}|{'-'*22}|")

tot_cb = sum(r['clean_before'] for r in step2_table)
tot_dg = sum(r['dup_groups'] for r in step2_table)
tot_dp = sum(r['dups_pruned'] for r in step2_table)
tot_fu = sum(r['final_unique'] for r in step2_table)

for r in step2_table:
    print(f"| {r['exercise']:<15} | {r['clean_before']:<20} | {r['dup_groups']:<18} | {r['dups_pruned']:<13} | {r['final_unique']:<20} |")

print(f"|{'-'*17}|{'-'*22}|{'-'*20}|{'-'*15}|{'-'*22}|")
print(f"| {'TOTAL':<15} | {tot_cb:<20} | {tot_dg:<18} | {tot_dp:<13} | {tot_fu:<20} |")
