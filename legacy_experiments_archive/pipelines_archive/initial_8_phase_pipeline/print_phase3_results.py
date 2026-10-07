import json

with open('backlog_phase3_lovo_results.json') as f:
    d = json.load(f)

EXERCISES = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']
rep = d['report_dict']
cm = d['confusion_matrix']

print("=== PHASE 3 PILOT EVALUATION RESULTS ===")
print("Overall Accuracy:", f"{d['accuracy']*100:.2f}%")
print(f"Total clips evaluated: {d['total_clips']} across {d['total_folds']} unique video folds\n")

print("SQUAT:")
print(f"  v3 F1:        0.34")
print(f"  New Pilot F1: {rep['squat']['f1-score']:.2f} (Precision: {rep['squat']['precision']:.2f}, Recall: {rep['squat']['recall']:.2f})")
print(f"  Change:       {rep['squat']['f1-score'] - 0.34:+.2f}")

print("\nLUNGE:")
print(f"  v3 F1:        0.48")
print(f"  New Pilot F1: {rep['lunge']['f1-score']:.2f} (Precision: {rep['lunge']['precision']:.2f}, Recall: {rep['lunge']['recall']:.2f})")
print(f"  Change:       {rep['lunge']['f1-score'] - 0.48:+.2f}")

print("\n--- SQUAT CONFUSION BREAKDOWN ---")
squat_idx = EXERCISES.index('squat')
squat_row = cm[squat_idx]
print(f"Total True Squat Clips: {sum(squat_row)}")
for idx, ex in enumerate(EXERCISES):
    cnt = squat_row[idx]
    pct = (cnt / sum(squat_row)) * 100
    print(f"  Predicted as {ex:<15}: {cnt:3d} ({pct:5.1f}%)")

print("\n--- LUNGE CONFUSION BREAKDOWN ---")
lunge_idx = EXERCISES.index('lunge')
lunge_row = cm[lunge_idx]
print(f"Total True Lunge Clips: {sum(lunge_row)}")
for idx, ex in enumerate(EXERCISES):
    cnt = lunge_row[idx]
    pct = (cnt / sum(lunge_row)) * 100
    print(f"  Predicted as {ex:<15}: {cnt:3d} ({pct:5.1f}%)")

print("\n--- FULL 7-CLASS CONFUSION MATRIX ---")
header = " | ".join([f"{ex[:7]:<7}" for ex in EXERCISES])
print(f"| {'True \\ Pred':<15} | {header} |")
print(f"|{'-'*17}|" + "|".join(['-'*9 for _ in EXERCISES]) + "|")
for idx, ex in enumerate(EXERCISES):
    row_str = " | ".join([f"{val:<7d}" for val in cm[idx]])
    print(f"| {ex:<15} | {row_str} |")

print("\n--- FULL CLASSIFICATION REPORT ---")
for ex in EXERCISES:
    print(f"{ex:<15}: Precision={rep[ex]['precision']:.2f}, Recall={rep[ex]['recall']:.2f}, F1={rep[ex]['f1-score']:.2f}, Support={rep[ex]['support']}")
