import os, hashlib

RAW_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model\data\raw_videos'
LM_DIR  = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model\data\landmarks'

exercises = sorted([d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))])

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

def md5_full(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

all_backlog = set()
small_files = set() # < 500KiB (512,000 bytes)
baseline_duplicates = set()
pair_details = []

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
            all_backlog.add((ex, f))
            if size < 512 * 1024:
                small_files.add((ex, f))

    # Fast size lookup for baseline matches
    backlog_by_size = {}
    for f, size, path in backlog_files:
        backlog_by_size.setdefault(size, []).append((f, path))

    for bf_name, bf_size, bf_path in baseline_files:
        matches = backlog_by_size.get(bf_size, [])
        for m_name, m_path in matches:
            if md5_full(bf_path) == md5_full(m_path):
                baseline_duplicates.add((ex, m_name))
                pair_details.append((ex, bf_name, m_name))

union_exclusions = small_files | baseline_duplicates
overlap_exclusions = small_files & baseline_duplicates
clean_candidates = all_backlog - union_exclusions

print('=== MATHEMATICAL SET OPERATIONS ===')
print(f'Total Backlog Files:                  {len(all_backlog)}')
print(f'A) Small / Corrupt Files (<500KiB):   {len(small_files)}')
print(f'B) Baseline MD5 Duplicates:           {len(baseline_duplicates)} (from {len(pair_details)} pair matches)')
print(f'Overlap (A & B):                      {len(overlap_exclusions)}')
print(f'Union Exclusions (A | B):             {len(union_exclusions)}')
print(f'REAL CLEAN CANDIDATE POOL:            {len(clean_candidates)} (933 - {len(union_exclusions)})')
print()

if overlap_exclusions:
    print('Files present in BOTH small-files and baseline-duplicates:')
    for ex, f in sorted(overlap_exclusions):
        print(f'  - {ex}/{f}')
print()

print('=== PER-EXERCISE BREAKDOWN ===')
print('| Exercise        | Backlog  | <500KiB   | Base Dups  | Overlap  | Union Excl  | Clean Pool  |')
print('|-----------------|----------|-----------|------------|----------|-------------|-------------|')

for ex in exercises:
    ex_b = [f for e, f in all_backlog if e == ex]
    ex_s = [f for e, f in small_files if e == ex]
    ex_d = [f for e, f in baseline_duplicates if e == ex]
    ex_ov = set(ex_s) & set(ex_d)
    ex_un = set(ex_s) | set(ex_d)
    ex_cl = len(ex_b) - len(ex_un)
    print(f'| {ex:<15} | {len(ex_b):<8} | {len(ex_s):<9} | {len(ex_d):<10} | {len(ex_ov):<8} | {len(ex_un):<11} | {ex_cl:<11} |')

print('|-----------------|----------|-----------|------------|----------|-------------|-------------|')
print(f'| TOTAL           | {len(all_backlog):<8} | {len(small_files):<9} | {len(baseline_duplicates):<10} | {len(overlap_exclusions):<8} | {len(union_exclusions):<11} | {len(clean_candidates):<11} |')

# Explain how 345 pairs maps to 158 distinct files
print('\n=== WHY 345 PAIRS MAP TO 158 DISTINCT BACKLOG FILES ===')
from collections import Counter
backlog_match_counts = Counter(m_name for ex, bf, m_name in pair_details)
match_freq = Counter(backlog_match_counts.values())
for count, freq in sorted(match_freq.items()):
    print(f'{freq} backlog file(s) each matched {count} different baseline video(s) -> total pairs = {freq * count}')
print(f'Sum of unique backlog files = {sum(match_freq.values())} files | Sum of pairs = {len(pair_details)} pairs')
