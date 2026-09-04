# BioMechAI — Open Items Requiring Confirmation Before Fine-Tuning

### Purpose

This is a punch-list of everything from the Module 3 data cleanup / evaluation history
(v2 → v3 → v4 → class-weighting experiments → camera-angle check) that is **still
unresolved, unverified, or contradicted by other evidence.** Before any PoseC3D fine-tuning
setup begins, go through every item below **in order**, and respond to each one with real
command/script output — not a narrative explanation of what's probably true.

**Rules that apply to every item (same as every prior task in this project):**
- Never present an invented, hypothetical, or illustrative example as real output. If you
  can't produce real evidence for something, say so directly.
- Every number must be traceable to an actual script run, shown in your response.
- If an item turns out to reveal a real problem in the current v4 dataset or model, say so
  plainly — do not soften it or bury it under an otherwise-positive summary.

**Do not begin any PoseC3D, MMAction2, or fine-tuning setup work until every item below has
been addressed and reported back for review.**

---

## 1. Backlog videos were possibly never checked against Batch 2 — this could mean undetected duplicates are in v4 right now

During backlog Phase 1, the 933-video backlog was deduplicated against:
- The original 42-video baseline (`baseline_videos.json`)
- Itself (the 102 duplicate groups / 233 redundant copies found internally)

**It was never confirmed whether backlog candidates were also checked against the 78 Batch 2
videos.** If any backlog video is actually a duplicate of a Batch 2 video, it would have
passed every dedup check that's been run so far, and it's now sitting inside the 2,309-clip
v4 dataset uncaught.

**Required action:** Using full-file MD5 (same method as every prior duplicate check), check
all 489 final backlog candidates (or the raw 722/933 pool, to be thorough) against all 78
Batch 2 video files. Report the exact count of any matches found, with filenames and MD5
hashes — same format as the earlier baseline-vs-backlog check that found `bicep_curl_03`.

---

## 2. "Zero clips dropped from v3" was asserted, not verified

The v4 report states: *"Zero Clips Dropped from Prior Versions: Exactly all 495 clips from
the approved v3 dataset were preserved without modification."*

This is the same kind of claim that turned out to be incomplete once (the v2→v3 baseline
clip count silently dropped from 182 to 174, and it took several rounds of direct questions
to get the actual list of which 8 clips and why). This claim has never been independently
checked the same way.

**Required action:** Take the list of all 495 v3 clip filenames and the list of all v4 clip
filenames. Compute the actual set difference. Confirm all 495 v3 filenames are present in
v4, or report exactly which ones are missing and why, the same way the 8 dropped v2→v3 clips
were eventually listed explicitly.

---

## 3. The Phase 1 backlog internal-dedup (102 groups, 233 copies) was never MD5-spot-verified

Every other duplicate-count claim in this project (the original 25, the 158 baseline dupes,
the multiplicity table) was confirmed with real MD5 hashes on a sample before being trusted.
This one wasn't.

**Required action:** Pick 5 of the largest duplicate groups from the 102 found in Phase 1.
For each, show the full-file MD5 hash of every video in the group, confirming they are
genuinely byte-identical (not a size-based false positive).

---

## 4. The squat↔lunge confusion direction contradicts the occlusion explanation given for it

The camera-angle check found squat and lunge are ~92-97% side/oblique view, and the
explanation offered was: in a side view, the rear leg is occluded, degrading MediaPipe's
tracking and causing confusion.

**The problem:** if occlusion specifically degrades the rear-leg signal that defines lunge,
the theory predicts lunge should be the one losing its identity and getting mistaken for
squat. But the v4 confusion matrix shows the opposite: **101 squat clips were misclassified
as lunge, versus only 69 lunge clips misclassified as squat** — squat is bleeding into lunge
more, not the reverse.

**Required action:** Do not simply restate the occlusion theory. Investigate the actual
direction of the asymmetry — e.g., check whether squat clips have measurably higher landmark
noise/occlusion than lunge clips (contrary to what the theory would predict), or propose and
test an alternative explanation for why squat is the class losing identity, not lunge. Show
whatever data supports the conclusion, not just reasoning.

---

## 5. The z-coordinate (depth) has never been used anywhere in this project — is that still the right call?

Every angle calculation in `extract_features` (used throughout v2/v3/v4 RandomForest work)
uses only `landmarks[:, :, :2]` — x and y. MediaPipe's landmarks include a z-estimate
(monocular depth relative to hips) that has never been used.

Given occlusion/depth ambiguity is now a live theory for the squat/lunge confusion (item 4),
this is worth resolving before committing to an architecture:

**Required action:** State plainly whether the planned PoseC3D pipeline will use 2D-only
keypoint heatmaps (standard, compatible with most pretrained checkpoints trained on 2D COCO
keypoints) or will attempt to incorporate MediaPipe's z-depth somehow. If the latter, explain
how that stays compatible with a pretrained checkpoint's expected input format — if it can't,
say so, and confirm 2D-only is the intended approach with the reasoning stated explicitly,
not left implicit.

---

## 6. The capped (1.3x) class-weighting result landed below both the unweighted AND fully-balanced results — unexplained

Unweighted: 50.76%. Fully-balanced: 50.76%. Capped (a value between the two, by design):
50.67% — lower than both endpoints, not between them. This is a minor item, lower priority
than 1-5, but worth a plain answer rather than leaving it unexplained.

**Required action:** Briefly confirm whether this is expected RandomForest behavior at small
margins (i.e., not a bug, just how this particular model responds to slightly different
weight configurations), or investigate further if there's reason to think it's a script
error. A short, direct answer is sufficient here — this does not need the same depth as
items 1-5.

---

## 7. PoseC3D keypoint remapping plan has not been stated yet

MediaPipe outputs 33 landmarks. Most PoseC3D pretrained checkpoints (via MMAction2) expect
COCO-format 17 keypoints. This mapping was flagged earlier as the step most likely to go
wrong silently, and it has not been planned out in detail yet.

**Required action:** Before any fine-tuning setup begins, state the exact mapping from
MediaPipe's 33 landmark indices to the 17 COCO keypoints the target pretrained checkpoint
expects (shoulders, elbows, wrists, hips, knees, ankles, etc. — noting COCO includes eyes/
ears/nose which MediaPipe also has, and noting any COCO keypoints MediaPipe doesn't cleanly
map to, if any). This should be a concrete index-to-index table, not a general description.

---

## 8. Confirm the no-fabrication rule going forward

Earlier in this project, one report included an illustrative "example" (a pushup duplicate
group) presented as if it were real script output, which turned out to be factually wrong
when checked against verified data. This was caught and corrected, but as the work moves
into a more complex fine-tuning pipeline where mistakes are more expensive to catch,
explicitly confirm understanding of the rule: **any example, filename, or number given as
"real" must come from an actual command that was actually run in this session** — not a
plausible reconstruction of what the output would probably look like.

---

## Required format for the response to this file

Go through items 1-8 in order. For each one, give:
- The actual command(s)/script(s) run
- The actual output
- A one-line plain-language verdict: confirmed fine / found a real problem / needs the
  user's decision

Do not summarize all 8 into a single paragraph at the end without showing the individual
work — each item needs its own evidence, the same way every check in this project so far
has been handled.
