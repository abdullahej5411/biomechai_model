import os
import hashlib

files = [
    r'data\raw_videos\lunge\lunge_04_13.mp4',
    r'data\raw_videos\pushup\pushup_07_06.mp4',
    r'data\raw_videos_batch2\squat\squat_b2_04.mp4'
]

print(f"{'Filename':<20} | {'Exists':<6} | {'Size (Bytes)':<14} | {'Freshly Computed MD5 Hash':<32}")
print("-" * 80)

for p in files:
    if os.path.exists(p):
        hasher = hashlib.md5()
        with open(p, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        h = hasher.hexdigest()
        sz = os.path.getsize(p)
        print(f"{os.path.basename(p):<20} | {str(True):<6} | {sz:<14} | {h}")
    else:
        print(f"{os.path.basename(p):<20} | {str(False):<6} | {'N/A':<14} | NOT FOUND: {p}")
