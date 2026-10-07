"""
Check whether any baseline video (already used in reported training/eval results)
has a size-match — and, if so, a confirmed content-match — somewhere in the
unprocessed raw_videos backlog.

Read-only. Does not modify, delete, or move any files.
"""
import os
import hashlib

RAW_DIR = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model\data\raw_videos'
LM_DIR  = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model\data\landmarks'


def get_lm_video_stems(exercise):
    """Video filename stems (no extension) that have extracted landmarks -- i.e. baseline."""
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


exercises = sorted(
    d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))
)

print("=== Baseline-vs-Backlog size collision check ===\n")

total_size_matches = 0
total_confirmed_dupes = 0
findings = []

for ex in exercises:
    ex_raw = os.path.join(RAW_DIR, ex)
    lm_stems = get_lm_video_stems(ex)

    baseline_files = []  # (filename, size, full_path)
    backlog_files = []

    for f in os.listdir(ex_raw):
        if not f.endswith('.mp4'):
            continue
        full_path = os.path.join(ex_raw, f)
        size = os.path.getsize(full_path)
        stem = f.replace('.mp4', '')
        if stem in lm_stems:
            baseline_files.append((f, size, full_path))
        else:
            backlog_files.append((f, size, full_path))

    # Build a size -> [backlog files] lookup for fast matching
    backlog_by_size = {}
    for f, size, path in backlog_files:
        backlog_by_size.setdefault(size, []).append((f, path))

    for bf_name, bf_size, bf_path in baseline_files:
        matches = backlog_by_size.get(bf_size, [])
        if not matches:
            continue
        for m_name, m_path in matches:
            total_size_matches += 1
            baseline_md5 = md5_full(bf_path)
            backlog_md5 = md5_full(m_path)
            confirmed = baseline_md5 == backlog_md5
            if confirmed:
                total_confirmed_dupes += 1
            findings.append({
                'exercise': ex,
                'baseline_file': bf_name,
                'baseline_size': bf_size,
                'backlog_file': m_name,
                'confirmed_duplicate': confirmed,
                'baseline_md5': baseline_md5,
                'backlog_md5': backlog_md5,
            })

print(f"Total size-matching pairs found: {total_size_matches}")
print(f"Confirmed (MD5-verified) duplicates: {total_confirmed_dupes}\n")

if findings:
    print("=== Details ===")
    for item in findings:
        status = "CONFIRMED DUPLICATE" if item['confirmed_duplicate'] else "SIZE COINCIDENCE (different content)"
        print(f"[{item['exercise']}] baseline '{item['baseline_file']}' "
              f"({item['baseline_size']} bytes) <-> backlog '{item['backlog_file']}' "
              f"=> {status}")
else:
    print("No size-matching pairs found between baseline and backlog videos.")

print("\n=== Action needed ===")
if total_confirmed_dupes > 0:
    print(f"{total_confirmed_dupes} baseline video(s) already have a confirmed duplicate "
          f"sitting in the backlog. These backlog files must be excluded (not merely "
          f"deduplicated against each other) before any backlog extraction runs, or the "
          f"same video will end up double-counted across baseline and new data.")
else:
    print("No further action needed on this specific risk -- clear to proceed to backlog "
          "extraction, as long as the baseline-vs-backlog check remains part of that "
          "pipeline's dedup step (not just backlog-vs-backlog and backlog-vs-batch2).")
