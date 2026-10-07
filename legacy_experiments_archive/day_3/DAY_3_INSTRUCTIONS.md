# BioMechAI — Day 3 Instructions: Real-Time Voice Coaching (Module 8 Core Layer)

### Status entering Day 3: Day 1 (backend, guarded rep state machine) and Day 2 (Flutter
camera pipeline, unified AR HUD, WebSocket resilience) are both certified on real hardware.
Day 3 completes the `voice_cue` field already present in the telemetry schema.

---

## 0. Rules carried forward — same standard as Days 1 and 2

1. Never present invented or hypothetical output as real. Show actual device evidence.
2. Every claim must be traceable to something actually run on real hardware.
3. Show real evidence at each step before moving to the next.
4. **Apply the same "never fabricate, never spam" discipline to audio that Day 2 applied to
   the HUD text.** A warning that's true for 3 seconds should not try to speak 90 times in
   that window just because telemetry arrives at 30fps.

---

## Step 1 — Decide and document the debounce/trigger rule before writing any TTS code

**This is the most important design decision of the day — get it right before Step 2, not
after building around the wrong assumption.**

Telemetry arrives at up to 30fps on the fast path. If every frame where
`form_alert.has_warning == true` triggers a new spoken utterance, the result is unusable —
the same phrase repeating dozens of times per second.

Define explicit rules:
- **Trigger on state transition, not on state persistence.** Speak when a warning *starts*
  (previous frame: no warning → this frame: warning), not on every frame the warning remains
  true.
- **Cooldown per message type.** Even on legitimate re-triggers (e.g. the user corrects form,
  then breaks it again 2 seconds later), enforce a minimum interval (e.g. 3-4 seconds) before
  the same cue can fire again, so genuine repeated issues don't create audio spam either.
- **Priority ordering.** A safety cue (`WARN: Knee Valgus`, `WARN: Step Back!`) must be able
  to interrupt or take priority over a lower-priority cue (e.g. a rep-count announcement) —
  decide and document which cues can interrupt which, rather than leaving it to whichever
  fires last.

**Output required before Step 2**: the actual documented rule set (trigger conditions,
cooldown durations, priority table) — not code yet, just the design, so it can be checked
before implementation time is spent on it.

---

## Step 2 — Populate `voice_cue` on the backend at the right trigger moments

In `backend/main.py` (or wherever telemetry is assembled), populate the existing
`voice_cue` field using Step 1's transition rule — computed server-side, since the backend
already has the state history needed to detect a transition (it already does this for
`rep_event`).

Candidate cue moments, applying Step 1's rules:
- Rep completion (`rep_event` fires) → e.g. "Rep {N} complete."
- Warning onset (`has_warning` transitions false→true) → the specific warning message.
- Warning clears (transitions true→false) → optional, lower priority, e.g. "Good, back on
  track."

**Do not populate `voice_cue` on every frame** — it should be `null` on frames where no new
cue should fire, exactly like `rep_event` already is.

**Test in isolation first**: run the existing isolated WebSocket test script from Day 2,
stream a session with a deliberate warning-onset and rep completion, and confirm
`voice_cue` only appears on the correct transition frames, not continuously.

**Output required before Step 3**: the real test log showing `voice_cue` appearing only at
transition frames.

---

## Step 3 — Wire on-device TTS in Flutter, with its own safety-net debounce

Use an on-device TTS package (e.g. `flutter_tts`) — not a cloud/LLM round-trip — for these
short, latency-sensitive cues. Reserve any conversational LLM chat feature (already flagged
in the master plan as the most cuttable item) for a later day, separate from this core cue
system.

1. Subscribe to the telemetry stream's `voice_cue` field.
2. When non-null, speak it — but **add a client-side debounce as a second safety net**, even
   though the backend should already be gating this. Two independent layers catch the case
   where one has a bug the other doesn't.
3. Implement the priority rule from Step 1: if a new high-priority cue arrives while a
   lower-priority one is still speaking, stop the current utterance and speak the new one;
   if a low-priority cue arrives while a high-priority one is speaking, queue or drop it,
   don't interrupt.

**Do not let audio errors crash or freeze the HUD.** If TTS fails (e.g. platform permission
issue), fail silently for audio only — the visual HUD from Day 2 must keep working
regardless.

---

## Step 4 — Real hardware test, same standard as Days 1 and 2

Run a real session on the physical phone, backend on the laptop, same as before. Deliberately
include:
1. A clean rep sequence — confirm audio announces reps without overlapping or stacking cues.
2. A deliberate form break (e.g. drift into knee valgus) — confirm the safety cue fires once
   on onset, not repeatedly while the condition persists.
3. A rapid oscillation (break form, correct, break again within a few seconds) — confirm the
   cooldown prevents audio spam without silently swallowing a genuinely new warning.
4. A safety cue firing while a rep-announcement cue is mid-utterance — confirm the priority
   rule from Step 1 actually behaves as designed, not just as intended.

**Required evidence**: a real screen recording with audio, not screenshots alone this time —
audio behavior can't be verified from a still image the way the HUD text could be. Include
the matching backend log so the `voice_cue` transitions can be cross-checked against what was
actually heard.

---

## What to bring back for review

1. Step 1's documented trigger/cooldown/priority rules.
2. Step 2's isolated test log showing correct transition-only `voice_cue` population.
3. Step 3's implementation, with the client-side debounce and priority logic called out
   explicitly.
4. Step 4's real screen-recording-with-audio evidence, covering all four scenarios, plus the
   matching backend log.

Do not report Day 3 complete without Step 4's audio evidence — a design that looks correct on
paper and one that's actually pleasant and non-spammy to use live are different things, and
this project has consistently found the gap between them exactly where it wasn't checked.
