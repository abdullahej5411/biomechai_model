# BioMechAI — Day 2 Instructions: Flutter Mobile Camera Pipeline & Real-Time AR HUD

### Status entering Day 2: Day 1 backend (FastAPI, dual-timescale pipeline, guarded rep
state machine, dynamic IP discovery + QR pairing) is certified and verified on real
hardware. Day 2 connects the Flutter mobile app to that backend and renders results live.

---

## 0. Rules carried forward from Day 1 — same standard, no exceptions

1. **Never present an invented, hypothetical, or illustrative example as real output.** If
   asked for evidence and none exists yet, say so and go get it — don't construct a
   plausible-looking substitute.
2. **Every claim must be traceable to something actually run** — a real log, a real
   screenshot from a real device, a real code diff. Not a description of what should happen.
3. **Show real evidence at each step below before moving to the next one.** Don't build all
   of Day 2 in one pass and present it as a finished whole — this project has repeatedly
   found real bugs by checking incrementally, not at the end.
4. **Apply the same "reject and flag, never silently substitute" principle from the backend
   to the frontend.** If the WebSocket disconnects, if the backend is unreachable, or if
   landmark confidence is low, the UI must show that state honestly (e.g. "Reconnecting...",
   "Step back into frame") — never freeze on or fabricate a stale-but-plausible-looking value.

---

## Step 1 — Confirm the actual current architecture before building anything

**Do not assume where pose extraction happens — verify it from the real codebase first.**

Check whether the Flutter app's existing on-device pose detection (`PoseDetectionService`,
using Google ML Kit, documented in the original project architecture) is still present and
functional. This matters because it determines the data flow:

- **If on-device extraction is still working**: the phone extracts MediaPipe/ML-Kit landmarks
  locally, streams the small landmark payload (33 points × 3 coordinates, not raw video
  frames) to the backend over the already-tested WebSocket endpoint, and the backend returns
  fast-path (flexion, FPPA, rep count, valgus alert) and slow-path (PoseC3D class, confidence)
  results. This is the architecture the Day 1 WiFi latency test was actually built around —
  it streamed pre-extracted landmark JSON, not video.
- **If it's not present or broken**: STOP and report this before building anything further.
  Sending raw video frames instead would multiply the bandwidth and latency Day 1 spent this
  much effort proving was fine — that's a fundamentally different, unverified performance
  profile, not a small implementation detail.

**Output required before Step 2**: confirmation of which data flow is actually in place, with
the real file/class checked, not an assumption.

---

## Step 2 — Wire the WebSocket client into the app using the existing pairing system

Reuse the dynamic discovery already built and verified on Day 1 (`GET /api/pairing`, QR
pairing at `/pair`) — do not hardcode an IP anywhere in the Flutter client. The app should:

1. On launch or on a "Connect" action, either scan the QR code or call `/api/pairing`
   directly if already paired, to obtain the current `ws_stream_url`.
2. Open the WebSocket connection.
3. **Test this in isolation first** — connect and log the raw incoming messages to the
   console, without yet touching any UI rendering. Confirm real messages are arriving
   before building anything on top of them.

**Output required**: a real console log showing actual received WebSocket messages from a
live backend session, before Step 3 begins.

---

## Step 3 — Build the AR HUD rendering layer

Using the confirmed data flow from Step 1, render on top of the live camera preview:

1. **Skeleton overlay** — reuse the existing `SkeletonPainter` (`CustomPainter`) if still
   present and functional; adapt it to whichever landmark source Step 1 confirmed, rather
   than rewriting it from scratch.
2. **Rep counter** — bound to the backend's rep count field, updating live.
3. **Form/valgus alert banner** — bound to the backend's alert field (`Form: Normal`,
   `WARN: Knee Valgus`, `WARN: Step Back! (FEET_OUT_OF_FRAME)`). This must display the
   backend's actual guard states from Day 1, including the "step back" warning — don't drop
   that state just because it's less exciting to show than a clean rep count.
4. **PoseC3D classification label + confidence** — bound to the slow-path result, showing
   "Buffering..." while the 48-frame window fills, exactly as the backend reports it. Do not
   hide the buffering state or fabricate an early guess.

**Do not silently default any of these fields to a placeholder if the WebSocket disconnects
or a message is malformed** — show a visible disconnected/error state instead, per Rule 4.

---

## Step 4 — Real end-to-end test on real hardware

This is the step that actually matters — everything before it is preparation for this test.

1. Run the FastAPI backend on the laptop, exactly as in Day 1.
2. Run the Flutter app on a real physical phone (not an emulator — emulator camera/network
   behavior doesn't represent the real deployment).
3. Pair via the QR flow.
4. Perform real squats in front of the phone camera, deliberately including:
   - A few clean reps (confirm rep counter increments correctly, PoseC3D eventually shows
     `squat` with rising confidence).
   - A deliberate "step back out of frame" moment (confirm the HUD shows the step-back
     warning and does **not** count a phantom rep — this is the exact bug fixed on Day 1;
     Day 2 needs to prove the fix is visible and correct all the way to the screen, not just
     in the backend log).
   - A brief WebSocket disconnect (turn off WiFi mid-session) — confirm the HUD shows a
     genuine disconnected state rather than freezing on the last good frame's data.

**Required evidence**: a real screen recording or a sequence of real timestamped screenshots
from the physical phone showing all three scenarios above, plus the backend's terminal log
from the same session so the two can be cross-checked against each other — the same standard
of proof used for every claim on Day 1.

---

## What to bring back for review

1. Step 1's architecture confirmation (with the actual file/class checked).
2. Step 2's real WebSocket message log.
3. Step 3's implementation, with the guard-state handling explicitly called out.
4. Step 4's full real-device test evidence — screen recording/screenshots plus matching
   backend log — covering clean reps, the step-back scenario, and a disconnect.

Do not report Day 2 as complete without Step 4's evidence. Everything before it is scaffolding;
Step 4 is the only step that proves the scaffolding actually works end to end.
