import json

with open('backlog_phase2_extraction_log.json') as f:
    d = json.load(f)

for ex in ['squat', 'lunge']:
    rows = d['details'][ex]
    print(f"### {ex.upper()} Candidates ({len(rows)} videos)\n")
    print("| Video Filename | Duration | Target Clips | Clips Extracted | Clips Discarded |")
    print("|---|---|---|---|---|")
    for r in rows:
        fn = r['filename']
        dur = f"{r['duration_seconds']:.1f} s"
        tc = r['target_clips']
        ce = r['clips_extracted']
        cd = r['clips_discarded']
        print(f"| `{fn}` | {dur} | {tc} | {ce} | {cd} |")
    print()
