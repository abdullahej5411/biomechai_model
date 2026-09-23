# BioMechAI — Full Project Audit & Standing Engineering Standard
### For the agent (Antigravity). Read completely before touching any code.

---

## 0. What this document is

This is not a single task — it's the complete, current list of everything Claude (acting as
external technical auditor across this entire project) has flagged as unresolved, plus the
standing rules that govern every future round of work on this project, not just this one.
Nothing in Section 4 (the module scoreboard) may be marked complete or reported to the user
as "verified" until the specific doubts in Section 2 are closed with real evidence, per the
standard in Section 1.

---

## 1. Standing rules — apply to everything below and everything after, permanently

1. **Never present an invented, hypothetical, or illustrative example as real evidence.** If
   something hasn't actually been run/tested, say so plainly. This has been the single most
   consequential rule in this entire project — multiple real bugs were only caught because a
   claim was checked against real output instead of accepted at face value, and at least one
   round of evidence was later admitted to be "illustrative" rather than real.
2. **A module or feature is "complete" only after a fresh, real-device test — not before.**
   Writing "100% Completed" in a status table is not evidence. If the same document that
   claims completion also lists "physical verification" as a pending next step, that is a
   direct contradiction — fix the document, not just the code, so the two halves agree.
3. **Every audio claim requires an actual audio file or recording, not a text description of
   what was supposedly heard.** Static screenshots and written timelines are not sufficient
   evidence for audio behavior — this project has already had one round where a written
   timeline of spoken cues did not match the actual audio track when independently measured.
4. **When re-testing something that was previously found broken, re-test the exact same
   scenario, not a superficially similar new one.** Evidence for a different scenario does
   not confirm the original bug is fixed.
5. **Every threshold, constant, or calibrated value must trace back to its most recent,
   evidence-based decision — do not silently revert to an earlier, already-rejected value.**
   If a value must change from what was previously established, say so explicitly and give
   the reason, rather than letting it change quietly inside an unrelated commit.
6. **If a fix could plausibly explain a previously-measured discrepancy, say so explicitly
   and re-test to confirm — do not let a broad batch of unrelated improvements implicitly
   stand in for answering a specific open question.**

---

## 2. Specific open doubts — go through every one of these, in order, and answer or fix each

### 2.1 — CRITICAL: The v1.6 handover document contradicts itself
The document's roadmap section lists "physical user verification of v1.6" as a pending,
not-yet-done milestone. Its scoreboard section, two sections earlier, marks Modules 3, 4, 5,
7, and 8 — the exact modules v1.6 changed — as "100% Completed." **Resolve this before
anything else**: run the actual physical verification now, and only then update the
scoreboard to match reality. Do not report any of these five modules as complete to the user
until this is done with real evidence.

### 2.2 — CRITICAL: Does the "Boundary Glitch Abort" fix explain the original measured audio gap?
In the Day 3 video review, an independent audio-energy analysis (not a transcript, an actual
measurement of the file's waveform) found:
- A continuous ~20-second silent window from 32.7s to 52.5s, which should have contained a
  "Good form, keep going!" recovery cue per the original claimed timeline.
- The claimed "Rep 1" cue at 00:14 had no matching audio — the nearest real audio activity
  was at ~18.5-19.8s, 4.5-5.5 seconds later.
- The claimed "step back" cue at 00:58 had no matching audio in the file's last ~3 seconds —
  the nearest real audio was at ~52.5-54.5s, 3.5-5.5 seconds earlier.
- Four additional audio bursts existed in the file that the written timeline never mentioned
  at all.

The v1.6 document describes a bug where the rep state machine was "instantly aborted back to
TOP" on a transient boundary warning, "destroying the rep event" — and separately describes
exercise-type-based muting of `rep_event`. Either or both of these **may** explain the
original gap, but this has not been explicitly confirmed.

**Required action**: re-run the exact same test protocol as the original Day 3 video
(clean rep → deliberate valgus break → recovery → deliberate camera-framing break) on the
current build, capture a fresh screen recording with audio, and independently verify (the
same way as before — actual waveform/energy analysis, not a written description) that cues
now land within a reasonable margin (under ~1 second) of their actual trigger moments, with
no unexplained multi-second silent gaps where a cue should be. State explicitly whether the
original gap is now closed, and if so, which specific fix closed it.

### 2.3 — The confidence threshold has regressed without justification
Section on Bug 3 states: *"If confidence >= 0.35, it is accepted as ground truth."*

This directly contradicts the last evidence-based decision on this exact value. A full
444-sample validation sweep previously established that **at threshold 0.35, 57.0% of the
model's wrong predictions would also clear that bar** — meaning the app would confidently
display an incorrect classification more often than not among its errors. That analysis led
to adopting **T = 0.50** (74.4% precision, rejecting 72.9% of wrong predictions) as the
calibrated production value.

**Required action**: either revert to T = 0.50, or — if there's a genuine new reason 0.35 is
now correct (e.g. a materially different model, a different use case for this specific
code path) — state that reason explicitly and re-run the same threshold sweep methodology
against the *current* model to justify the new number with fresh data. Do not let a
previously-rejected value silently reappear without a documented reason.

### 2.4 — "100% rep capture, 0% standing jitter ingestion" needs real output, not a claim
This is stated as "mathematically validated via unit test simulation
(`scratch/test_rep_counter.py`)." Show the actual printed output of that script — the real
pass/fail counts, not just the sentence claiming it passed.

### 2.5 — The PoseC3D-primary architecture flip needs fresh live-device proof, specifically at the fallback boundary
Flipping PoseC3D from a secondary/fallback role to primary is a major architecture change.
This project already found one real bug once before (Day 2) where two independent feedback
systems displayed contradictory information on screen simultaneously, because a legacy
system wasn't fully disabled when a new one was wired in. The new "Offline Fallback Shield"
(local kinematics activating when the backend is unreachable or times out) is architecturally
the same category of risk in a new location.

**Required action**: on a real device, deliberately trigger the fallback (e.g. disable WiFi
or block the backend mid-session) and confirm:
- The HUD shows one clear, consistent state during the handoff — never two systems'
  conflicting guesses at once.
- The transition back to backend-primary mode (once connectivity returns) is clean, without
  a stale fallback classification lingering on screen after the backend is authoritative
  again.

Capture this as a real screen recording, the same standard as every other claim here.

### 2.6 — Module 6 (Body Measurement & Transformation Tracking) is still not built
This is explicitly the one remaining module. Do not let it slip while iterating on
already-built modules — confirm a concrete plan and timeline for it exists, separate from
the fixes above.

### 2.7 — Confirm the client-side rep-announcement design decision was deliberate, not incidental
Bug 1's fix moves rep-milestone speech triggering to the client (on-device, immediate,
sub-50ms), with the server's own `voice_cue` for reps now de-duplicated/dropped if the client
already announced it. This is a reasonable design (lower latency for a latency-sensitive
cue), but confirm explicitly: does this change conflict with the original Day 3 design (server
decides trigger moments, client has a debounce safety net) for any *other* cue types (safety
warnings, praise)? State plainly which cues are now client-triggered vs. server-triggered,
and why, so this isn't an implicit, undocumented split.

---

## 3. Required format for the response

Go through Sections 2.1 through 2.7 in order. For each one, provide:
- The real evidence (recording, log, printed test output) — not a narrative summary of what
  should be true.
- An explicit verdict: resolved, or still open, with the specific reason if still open.

Do not skip to a "everything is now fixed" summary without showing the work for each item
individually — this project has repeatedly found that a confident summary and the underlying
evidence do not always agree, and the disagreement is only caught by checking each claim on
its own.

## 4. After Section 2 is fully resolved

Only once every item in Section 2 has real evidence and an explicit verdict, update the
module scoreboard to reflect actual, verified status — and only then should any module be
described to the user or in any report as "100% Completed."
