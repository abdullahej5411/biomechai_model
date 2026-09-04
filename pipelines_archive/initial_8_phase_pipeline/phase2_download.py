"""
Phase 2 of 8 — Download new candidate videos into data/raw_videos_batch2/
- Uses VARIED search queries (different wording from download_videos.py)
- Uses mobile client extractor to bypass bot detection without needing browser cookies
- Tracks uploader/channel per video; caps at ~2-3 per channel per exercise
- Avoids duplicate video IDs across searches
- Downloads to separate folder — does NOT touch data/raw_videos/
"""
import subprocess, os, sys, json, glob

BASE_DIR  = r'd:\Study Folder\Semester 8\FYP-I\Final Evaluation\fypbiomechai\biomechai_model'
OUT_BASE  = os.path.join(BASE_DIR, 'data', 'raw_videos_batch2')
LOG_FILE  = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'phase2_download_log.json')

# Verify baseline exists (Phase 1 prerequisite)
BASELINE  = os.path.join(BASE_DIR, 'model_training', 'cleanup_v2', 'baseline_videos.json')
if not os.path.exists(BASELINE):
    print("ERROR: baseline_videos.json not found. Run Phase 1 first.")
    sys.exit(1)
print("baseline_videos.json found. Proceeding with Phase 2 downloads.\n")

# Targets per exercise
TARGETS = {
    'jumping_jack': 14,
    'plank':        12,
    'lunge':        12,
    'bicep_curl':   11,
    'pushup':       11,
    'squat':        9,
    'high_knees':   9,
}

QUERIES = {
    'jumping_jack': [
        'ytsearch5:jumping jacks cardio workout demonstration',
        'ytsearch5:star jumps aerobic exercise tutorial',
        'ytsearch5:jumping jack warm up fitness routine',
    ],
    'plank': [
        'ytsearch5:plank challenge core strength exercise video',
        'ytsearch5:forearm plank position correct technique',
        'ytsearch5:abdominal plank hold fitness clip',
    ],
    'lunge': [
        'ytsearch5:walking lunge lower body workout video',
        'ytsearch5:reverse lunge exercise demonstration clip',
        'ytsearch5:lunge leg workout fitness tutorial video',
    ],
    'bicep_curl': [
        'ytsearch5:dumbbell bicep curl arm workout video',
        'ytsearch5:standing curl exercise upper body clip',
        'ytsearch5:hammer curl vs bicep curl demonstration',
    ],
    'pushup': [
        'ytsearch5:standard push up exercise form tutorial',
        'ytsearch5:how to do push ups correctly workout',
        'ytsearch5:push up proper technique bodyweight training',
        'ytsearch5:push up form guide fitness demonstration',
        'ytsearch5:floor push up reps exercise demonstration',
        'ytsearch5:perfect push up technique for beginners',
        'ytsearch5:push up variations chest fitness workout',
    ],
    'squat': [
        'ytsearch5:bodyweight squat exercise form tutorial',
        'ytsearch5:air squat proper technique workout guide',
        'ytsearch5:how to squat correctly fitness demonstration',
        'ytsearch5:squat reps workout bodyweight exercise',
        'ytsearch5:deep squat exercise demonstration clip',
        'ytsearch5:squat form guide lower body fitness',
        'ytsearch5:goblet squat bodyweight exercise clip',
    ],
    'high_knees': [
        'ytsearch5:high knees cardio workout exercise tutorial',
        'ytsearch5:running high knees fitness exercise demonstration',
        'ytsearch5:high knee march cardio routine form',
        'ytsearch5:how to do high knees correctly beginner',
        'ytsearch5:high knees sprint in place workout clip',
        'ytsearch5:high knees aerobic exercise demonstration',
        'ytsearch5:high knees warm up exercise tutorial',
    ],
}

# Load existing log if available
download_log = {}
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, 'r') as f:
            download_log = json.load(f)
    except Exception:
        download_log = {}

ORDER = ['jumping_jack', 'plank', 'lunge', 'bicep_curl', 'pushup', 'squat', 'high_knees']

for exercise in ORDER:
    ex_dir = os.path.join(OUT_BASE, exercise)
    os.makedirs(ex_dir, exist_ok=True)
    target = TARGETS[exercise]

    # Inspect existing downloaded files on disk
    existing_entries = download_log.get(exercise, [])
    valid_entries = []
    seen_video_ids = set()
    channel_count = {}

    for entry in existing_entries:
        if entry.get('status') == 'downloaded':
            fname = entry.get('filename')
            fpath = os.path.join(ex_dir, fname) if fname else None
            vid_id = entry.get('video_id')
            uploader = entry.get('uploader', 'unknown')
            if fpath and os.path.exists(fpath) and os.path.getsize(fpath) > 10000:
                if vid_id and vid_id not in seen_video_ids:
                    seen_video_ids.add(vid_id)
                    channel_count[uploader] = channel_count.get(uploader, 0) + 1
                    valid_entries.append(entry)

    print("=" * 60)
    print(f"Exercise: {exercise} | Valid existing: {len(valid_entries)} | Target: {target}")
    print("=" * 60)

    # Determine next counter
    current_numbers = []
    for f in os.listdir(ex_dir):
        if f.endswith('.mp4'):
            parts = f.replace('.mp4', '').split('_b2_')
            if len(parts) == 2 and parts[1].isdigit():
                current_numbers.append(int(parts[1]))
    next_counter = max(current_numbers, default=0) + 1

    downloaded = list(valid_entries)

    if len(downloaded) < target:
        query_list = QUERIES.get(exercise, [])
        for query in query_list:
            if len(downloaded) >= target:
                break

            print(f"Query: {query}")
            meta_cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--extractor-args', 'youtube:player_client=android,web',
                query,
                '--dump-json',
                '--no-download',
                '--flat-playlist',
                '--quiet',
                '--no-warnings',
            ]
            try:
                result = subprocess.run(meta_cmd, capture_output=True, text=True, timeout=60)
                lines  = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
            except Exception as e:
                print(f"  Meta fetch failed for query [{query}]: {e}")
                lines = []

            for line in lines:
                if len(downloaded) >= target:
                    break
                try:
                    info = json.loads(line)
                except Exception:
                    continue

                vid_id   = info.get('id', 'unknown')
                uploader = info.get('uploader') or info.get('channel') or 'unknown'
                url      = info.get('url') or info.get('webpage_url') or (f'https://www.youtube.com/watch?v={vid_id}')

                # Avoid duplicate video IDs
                if vid_id in seen_video_ids:
                    continue

                # Channel diversity cap: max 2 per channel per exercise
                if channel_count.get(uploader, 0) >= 2:
                    print(f"  SKIP (channel cap): {uploader} | {vid_id}")
                    continue

                fname_base  = f"{exercise}_b2_{next_counter:02d}"
                out_template = os.path.join(ex_dir, f"{fname_base}.%(ext)s")

                dl_cmd = [
                    sys.executable, '-m', 'yt_dlp',
                    '--extractor-args', 'youtube:player_client=android,web',
                    url,
                    '--format', 'mp4[height<=480]/best[height<=480]/best',
                    '--output', out_template,
                    '--no-playlist',
                    '--quiet',
                    '--no-warnings',
                    '--max-filesize', '80m',
                ]
                try:
                    subprocess.run(dl_cmd, timeout=120, check=True)
                    candidates = [f for f in os.listdir(ex_dir) if f.startswith(fname_base) and f.endswith('.mp4')]
                    if candidates:
                        actual_fname = candidates[0]
                        seen_video_ids.add(vid_id)
                        channel_count[uploader] = channel_count.get(uploader, 0) + 1
                        downloaded.append({
                            'filename': actual_fname,
                            'uploader': uploader,
                            'video_id': vid_id,
                            'query':    query,
                            'status':   'downloaded',
                        })
                        next_counter += 1
                        print(f"  OK [{len(downloaded)}/{target}] {actual_fname} | {uploader}")
                    else:
                        print(f"  WARN: File not found for {fname_base}")
                except Exception as e:
                    print(f"  FAIL download: {vid_id} | {e}")
                    next_counter += 1

    download_log[exercise] = downloaded
    print(f"  -> {len(downloaded)} total candidates available for {exercise} (target {target})\n")

# Save updated log
with open(LOG_FILE, 'w') as f:
    json.dump(download_log, f, indent=2)
print("Updated download log saved to:", LOG_FILE)

# Print required output format
print("\n" + "=" * 70)
print("PHASE 2 REQUIRED OUTPUT SUMMARY")
print("=" * 70)

for ex in ORDER:
    entries = download_log.get(ex, [])
    ok = [e for e in entries if e['status'] == 'downloaded']
    target = TARGETS[ex]
    print(f"\n### {ex}: {len(ok)} downloaded / target {target}")
    print(f"| {'Filename':<30} | {'Uploader/Channel':<35} |")
    print(f"|{'-'*32}|{'-'*37}|")
    for e in ok:
        print(f"| {e['filename']:<30} | {e['uploader']:<35} |")
