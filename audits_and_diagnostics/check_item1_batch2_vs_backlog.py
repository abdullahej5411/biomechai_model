import os, hashlib, json

def get_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

batch2_dir = 'data/raw_videos_batch2'
b2_files = {}
for root, _, files in os.walk(batch2_dir):
    for f in files:
        if f.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            p = os.path.join(root, f)
            b2_files[get_md5(p)] = (root, f)

print(f"Total Batch 2 video files hashed: {len(b2_files)}")

# Check against the 489 clean backlog candidates
with open('backlog_clean_deduped_candidates.json') as f:
    cand_dict = json.load(f)

cand_matches = []
total_cands = 0
for ex, data in cand_dict.items():
    cands = data['unique_candidates']
    total_cands += len(cands)
    for vid_entry in cands:
        # Check structure of vid_entry
        if isinstance(vid_entry, dict):
            fn = vid_entry.get('filename') or vid_entry.get('video_file')
        else:
            fn = vid_entry
        p = os.path.join('data', 'raw_videos', ex, fn)
        if not os.path.exists(p):
            p = os.path.join('data', 'raw_videos', fn)
        if os.path.exists(p):
            md5 = get_md5(p)
            if md5 in b2_files:
                cand_matches.append((ex, fn, b2_files[md5], md5))
        else:
            print(f"Warning: candidate file not found: {p}")

print(f"Total unique candidates in backlog_clean_deduped_candidates.json: {total_cands}")
print(f"Total matches between the 489 clean backlog candidates and Batch 2: {len(cand_matches)}")
if cand_matches:
    for ex, fn, b2_info, md5 in cand_matches:
        print(f"  DUPLICATE IN V4 CANDIDATES: {ex}/{fn} <==> {b2_info[0]}/{b2_info[1]} (MD5: {md5})")
else:
    print("  [CONFIRMED] Zero matches found! None of the 489 clean backlog candidates overlap with Batch 2.")

# Also check whether any clips from backlog in merged_dataset.json came from Batch 2 video_ids
with open('model_training/cleanup_v4/merged_dataset.json') as f:
    v4_clips = json.load(f)

with open('model_training/cleanup_v2/merged_dataset.json') as f:
    v3_clips = json.load(f)

v3_vids = set((c['exercise'], c['video_id']) for c in v3_clips)
v4_backlog_clips = [c for c in v4_clips if (c['exercise'], c['video_id']) not in v3_vids]
v4_backlog_vids = set((c['exercise'], c['video_id']) for c in v4_backlog_clips)

print(f"\nUnique video IDs in v3 baseline+batch2: {len(v3_vids)}")
print(f"Unique video IDs in v4 backlog: {len(v4_backlog_vids)}")
overlap_vids = v3_vids.intersection(v4_backlog_vids)
print(f"Video ID overlap between v3 and v4 backlog clips: {len(overlap_vids)}")
