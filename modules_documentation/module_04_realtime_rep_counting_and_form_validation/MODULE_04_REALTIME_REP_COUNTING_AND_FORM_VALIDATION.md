# BioMechAI — Module 04: Real-Time Repetition Counting, Posture-Gated Isometric Hold Clock, & Multi-Stage State Machine Validation

<div class="toc">
<h2>Table of Contents & Rapid-Lookup Index</h2>
<ul>
<li><a href="#sec1">1. Executive Summary & Core Mission</a></li>
<li><a href="#sec2">2. Real-World Rep Counting Failures: Why Accelerometers & Peak Counters Fail</a></li>
<li><a href="#sec3">3. Step-by-Step Chronological Engineering Evolution</a></li>
<li><a href="#sec4">4. The Closed 4-Stage Finite State Machine Architecture</a>
    <ul>
        <li><a href="#sec4-1">4.1 Stage 1: TOP / UPRIGHT (Standing Neutral Lock)</a></li>
        <li><a href="#sec4-2">4.2 Stage 2: DESCENDING (Eccentric Muscle Loading)</a></li>
        <li><a href="#sec4-3">4.3 Stage 3: BOTTOM / INFLECTION (Biomechanical Turnaround Depth)</a></li>
        <li><a href="#sec4-4">4.4 Stage 4: ASCENDING (Concentric Drive)</a></li>
        <li><a href="#sec4-5">4.5 Stage 5: REPETITION CERTIFIED (Return to TOP)</a></li>
    </ul>
</li>
<li><a href="#sec5">5. Exercise-Specific Angular Thresholds & Hysteresis Gating (All Exercises)</a></li>
<li><a href="#sec6">6. Anti-Glitch Hardening & Physics-Based Velocity Clamping</a>
    <ul>
        <li><a href="#sec6-1">6.1 Anatomical Angular Velocity Limit (Delta theta <= 48 deg per frame)</a></li>
        <li><a href="#sec6-2">6.2 Minimum Cadence Time Lock (>= 10 frames / ~0.33 seconds)</a></li>
        <li><a href="#sec6-3">6.3 Incomplete Half-Rep Rejection & Reset Logic</a></li>
        <li><a href="#sec6-4">6.4 Boundary Truncation & Occlusion Guards (y in [0.01, 0.985])</a></li>
    </ul>
</li>
<li><a href="#sec7">7. The Posture-Gated Isometric Plank Hold Engine (Milestone #27 / #36)</a>
    <ul>
        <li><a href="#sec7-1">7.1 The Isometric Paradox (Why Planks Cannot Use Rep Counters)</a></li>
        <li><a href="#sec7-2">7.2 The 150°-190° Spinal Angle Gatekeeper</a></li>
        <li><a href="#sec7-3">7.3 Real-Time Clock Freezing & Visual Crimson Red Alerts</a></li>
        <li><a href="#sec7-4">7.4 Seamless Resumption & Audible Milestone Cadence</a></li>
    </ul>
</li>
<li><a href="#sec8">8. Quality Partitioning: Total Reps vs. Valid Reps</a></li>
<li><a href="#sec9">9. Cloud vs. Edge Synchronization (Zero-Latency Local Counting)</a></li>
<li><a href="#sec10">10. Scientific Standards, Biomechanical Literature, & NSCA Guidelines</a></li>
<li><a href="#sec11">11. Panel Defense Quick-Reference: Frequently Asked Questions & Rapid Answers</a></li>
</ul>
</div>

---

<h2 id="sec1">1. Executive Summary & Core Mission</h2>

<p>
Module 04 acts as the impartial, digital competition judge of the BioMechAI platform. In resistance and functional training, counting repetitions is universally prone to human cognitive bias: tired athletes subconsciously cut depth short, cheat by bouncing at the bottom, or exaggerate their volume. Module 04 replaces subjective estimation with a deterministic, mathematically unyielding <strong>Closed 4-Stage Finite State Machine (FSM)</strong> coupled with an <strong>Isometric Posture-Gated Hold Engine</strong>.
</p>

<blockquote>
<strong>Plain-English Concept:</strong> Imagine an Olympic powerlifting referee sitting on a low stool next to your squat rack. The referee doesn't count "one rep" just because you bounced your hips a little bit. You must start completely upright, descend until your hip crease breaks below your knee, hold that bottom position for a fraction of a second, drive all the way back up, and lock your knees straight again. If you only go halfway down, the referee stares at you in silence—the count stays at zero. That is exactly how Module 04 operates using real-time computer vision.
</blockquote>

<p>
The module delivers:
</p>
<ul>
    <li><strong>Closed 4-Stage Repetition State Machine</strong>: Cyclically enforces <code>TOP</code> $\to$ <code>DESCENDING</code> $\to$ <code>BOTTOM</code> $\to$ <code>ASCENDING</code> $\to$ <code>TOP</code>, mathematically preventing double-counting or skipped movement phases.</li>
    <li><strong>Hysteresis Angular Thresholds</strong>: Enforces wide separation between descent and return boundaries across all exercises (e.g., Squat: $120.0^\circ$ down, $148.0^\circ$ up), completely eliminating boundary flickering.</li>
    <li><strong>Physics-Based Angular Velocity Clamping</strong>: Drops unphysical coordinate glitches exceeding $48.0^\circ$ per $33\text{ ms}$ video frame ($\sim 1,450^\circ/\text{s}$), rejecting camera lens noise.</li>
    <li><strong>Posture-Gated Isometric Plank Clock (Milestone #27 / #36)</strong>: Replaces repetition logic during planks with a 1 Hz hold clock that automatically freezes whenever spinal alignment collapses below $150^\circ$ or pikes above $190^\circ$.</li>
    <li><strong>Strict Quality Partitioning</strong>: Distinguishes between <code>totalReps</code> (raw movements finished) and <code>validReps</code> (reps certified with $>45\%$ score and zero high-severity clinical faults).</li>
</ul>

---

<h2 id="sec2">2. Real-World Rep Counting Failures: Why Naive Approaches Fail</h2>

<p>
Most commercial fitness trackers fail at repetition counting because they rely on simplistic, flawed assumptions:
</p>

<ol>
    <li><strong>Wearable Accelerometers & Smartwatches</strong>:
        <br>Smartwatches only measure gross wrist acceleration. If an athlete does bodyweight squats while holding their hands steady in front of their chest, the watch detects zero wrist motion and registers zero reps. Conversely, if an athlete sits on a bench and gestures with their hands, the watch detects wrist movement and falsely credits them with 10 squats!
    </li>
    <li><strong>Naive Sinusoidal Peak Detectors</strong>:
        <br>Early vision systems plotted joint height over time and looked for local mathematical minima/maxima. When an athlete reached the bottom of a heavy squat and shivered or hesitated, the wavy curve produced four rapid peaks, causing the counter to falsely jump by $+4\text{ reps}$ in half a second!
    </li>
    <li><strong>Cheating & Incomplete Half-Reps</strong>:
        <br>Without a closed multi-stage state machine, an athlete performing rapid "quarter-squats" (bending knees by only $20^\circ$) triggers naive threshold counters, rewarding dangerous and ineffective exercise habits.
    </li>
</ol>

<p>
Module 04 eliminates every one of these failure modes through rigorous biomechanical state transitions, temporal cadence locks, and anatomical angle gating.
</p>

---

<h2 id="sec3">3. Step-by-Step Chronological Engineering Evolution</h2>

<p>
Module 04 progressed through three distinct architectural generations:
</p>

<h3>Generation 1: Single-Threshold Trigger (FYP-I Baseline)</h3>
<p>
In the early FYP-I prototype, the app used a single boolean threshold: <code>if (kneeAngle < 120) count++</code>.
</p>
<div class="alert-box">
<strong>Critical Failure Discovered:</strong> If an athlete descended into a squat and hovered at $119^\circ$, tiny natural micro-tremors crossed the $120^\circ$ boundary back and forth dozens of times per second. The rep counter spun wildly out of control, logging 50 repetitions in a single 3-second hold!
</div>

<h3>Generation 2: Dual-Threshold Hysteresis FSM (Semester 8 Baseline)</h3>
<p>
The team solved boundary jitter by introducing <strong>Hysteresis Gating</strong> with two distinct thresholds: a descent inflection threshold ($120^\circ$) and a return lockout threshold ($148^\circ$). The state flipped to <code>down</code> only at $120^\circ$ and could not register a rep until returning past $148^\circ$.
</p>

<h3>Generation 3: Hardened 4-Stage FSM & Posture-Gated Hold Engine (Milestone #27 / #36)</h3>
<p>
During the final graduation hardening, the team elevated Module 04 into an enterprise biomechanical judge:
</p>
<ul>
    <li>Engineered the <strong>Closed 4-Stage State Machine</strong>: Requires positive progression through <code>TOP</code> $\to$ <code>DESCENDING</code> $\to$ <code>BOTTOM</code> $\to$ <code>ASCENDING</code> $\to$ <code>TOP</code>.</li>
    <li>Implemented the <strong>Velocity Spike Filter</strong>: Discards angular jumps $>48^\circ$ per frame.</li>
    <li>Enforced <strong>Minimum Cadence Time Lock</strong>: Demands at least 2 consecutive frames in the bottom inflection zone and a minimum cycle time of $\ge 10\text{ frames}$ ($\ge 0.33\text{ seconds}$).</li>
    <li>Integrated the <strong>Posture-Gated Isometric Plank Engine</strong>: Solved the "plank paradox" by creating a continuous hold clock gated by McGill's $150^\circ-190^\circ$ spinal alignment boundaries.</li>
</ul>

---

<h2 id="sec4">4. The Closed 4-Stage Finite State Machine Architecture</h2>

<p>
A repetition is modeled not as a point in time, but as a continuous physical journey through four distinct mechanical states:
</p>

<pre><code>THE CLOSED 4-STAGE REPETITION STATE MACHINE (RepCounterService.dart & kinematics.py)
===================================================================================
                       +-------------------------------+
                       |   STAGE 1: TOP / UPRIGHT      |
                       |  Angle > 148.0 deg (Extended) |
                       +---------------+---------------+
                                       |
                   Knee Flexion Initiated (Angle < 148 deg)
                                       v
                       +-------------------------------+
                       |    STAGE 2: DESCENDING        |
                       |  Eccentric Loading Movement   |
                       +---------------+---------------+
                                       |
                   Deep Depth Reached (Angle < 120.0 deg)
                   AND Held for >= 2 Consecutive Frames
                                       v
                       +-------------------------------+
                       |  STAGE 3: BOTTOM / INFLECTION |
                       |  Verified Full Parallel Depth |
                       +---------------+---------------+
                                       |
                   Concentric Drive (Angle Rising > 120 deg)
                                       v
                       +-------------------------------+
                       |    STAGE 4: ASCENDING         |
                       |  Concentric Extension Push    |
                       +---------------+---------------+
                                       |
                   Full Upright Extension Reached (Angle > 148.0 deg)
                   AND Cycle Duration >= 10 Frames (>= 0.33s)
                                       v
                       +-------------------------------+
                       |   REPETITION CERTIFIED!       |
                       |  totalReps++ (validReps++)    |
                       |  Audio Cue: "Rep 1" (Pri. 2)  |
                       +---------------+---------------+
                                       |
                                       +---> Return to STAGE 1 (Loop Cycle)
===================================================================================</code></pre>

<h3 id="sec4-1">4.1 Stage 1: TOP / UPRIGHT (Standing Neutral Lock)</h3>
<p>
The athlete begins in anatomical neutral extension ($\theta > 148.0^\circ$). The state machine confirms full standing lock and initializes the tracking cycle counter.
</p>

<h3 id="sec4-2">4.2 Stage 2: DESCENDING (Eccentric Muscle Loading)</h3>
<p>
As the athlete begins bending their knees or elbows, the joint angle drops below $148.0^\circ$. The machine transitions to <code>DESCENDING</code>. During this phase, velocity checks verify smooth, controlled descent.
</p>

<h3 id="sec4-3">4.3 Stage 3: BOTTOM / INFLECTION (Biomechanical Turnaround Depth)</h3>
<p>
The athlete breaches the deep inflection threshold ($\theta < 120.0^\circ$). To prevent false triggers from momentary frame dropouts, the engine enforces a <strong>Turnaround Hold</strong>: the joint must remain below $120.0^\circ$ for at least two consecutive video frames ($>66\text{ ms}$) or reach deep inflection ($\theta < 112.0^\circ$). The state shifts to <code>down</code>.
</p>

<h3 id="sec4-4">4.4 Stage 4: ASCENDING (Concentric Drive)</h3>
<p>
The athlete drives upward out of the bottom position. The joint angle begins expanding back upward past $120.0^\circ$. The state machine enters <code>ASCENDING</code>.
</p>

<h3 id="sec4-5">4.5 Stage 5: REPETITION CERTIFIED (Return to TOP)</h3>
<p>
When the joint angle expands fully past the upright return threshold ($\theta > 148.0^\circ$), the machine checks the <strong>Cadence Lock</strong>: total cycle frames must be $\ge 10\text{ frames}$ ($\sim 0.33\text{ seconds}$).
<br><strong>The Repetition is Certified:</strong>
</p>
<ul>
    <li><code>totalReps</code> increments by $+1$.</li>
    <li>If the repetition maintained safe posture (Score $\ge 45\%$ and zero high-severity breaches), <code>validReps</code> increments by $+1$.</li>
    <li>The on-device voice coach speaks aloud: <em>"Rep [N]"</em> (Priority 2 Milestone).</li>
    <li>State resets cleanly to <code>up</code> ready for the next rep.</li>
</ul>

---

<h2 id="sec5">5. Exercise-Specific Angular Thresholds & Hysteresis Gating</h2>

<p>
Because each exercise involves different skeletal levers and ranges of motion, Module 04 hardcodes custom hysteresis threshold pairs into <code>RepCounterService.dart</code>:
</p>

<table>
    <thead>
        <tr>
            <th>Exercise</th>
            <th>Primary Joint Tracked</th>
            <th>Bottom Inflection Threshold (<code>downThresh</code>)</th>
            <th>Top Return Threshold (<code>upThresh</code>)</th>
            <th>Hysteresis Separation ($\Delta \theta$)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Squat</strong></td>
            <td>Knee Flexion ($\angle \text{Hip-Knee-Ankle}$)</td>
            <td><strong>$120.0^\circ$</strong> (Parallel Depth)</td>
            <td><strong>$148.0^\circ$</strong> (Full Extension)</td>
            <td>$28.0^\circ$ separation</td>
        </tr>
        <tr>
            <td><strong>Lunge</strong></td>
            <td>Leading Knee Flexion</td>
            <td><strong>$118.0^\circ$</strong> (Deep Split)</td>
            <td><strong>$146.0^\circ$</strong> (Standing Lock)</td>
            <td>$28.0^\circ$ separation</td>
        </tr>
        <tr>
            <td><strong>Push-Up</strong></td>
            <td>Elbow Flexion ($\angle \text{Shoulder-Elbow-Wrist}$)</td>
            <td><strong>$105.0^\circ$</strong> (Chest to Floor)</td>
            <td><strong>$142.0^\circ$</strong> (Plank Lockout)</td>
            <td>$37.0^\circ$ separation</td>
        </tr>
        <tr>
            <td><strong>Bicep Curl</strong></td>
            <td>Elbow Flexion</td>
            <td><strong>$108.0^\circ$</strong> (Full Peak Curl)</td>
            <td><strong>$140.0^\circ$</strong> (Bottom Extension)</td>
            <td>$32.0^\circ$ separation</td>
        </tr>
        <tr>
            <td><strong>High Knees</strong></td>
            <td>Hip Flexion ($\angle \text{Shoulder-Hip-Knee}$)</td>
            <td><strong>$112.0^\circ$</strong> (Thigh Parallel)</td>
            <td><strong>$145.0^\circ$</strong> (Foot on Ground)</td>
            <td>$33.0^\circ$ separation</td>
        </tr>
        <tr>
            <td><strong>Jumping Jack</strong></td>
            <td>Shoulder Abduction (Inverted Logic)</td>
            <td><strong>$50.0^\circ$</strong> (Arms Down at Sides)</td>
            <td><strong>$80.0^\circ$</strong> (Arms Raised Overhead)</td>
            <td>$30.0^\circ$ separation</td>
        </tr>
        <tr>
            <td><strong>Plank</strong></td>
            <td>Spinal Alignment ($\angle \text{Shoulder-Hip-Ankle}$)</td>
            <td><em>N/A (Isometric Static Hold)</em></td>
            <td><em>N/A (Isometric Static Hold)</em></td>
            <td><em>Posture-Gated 1 Hz Clock</em></td>
        </tr>
    </tbody>
</table>

---

<h2 id="sec6">6. Anti-Glitch Hardening & Physics-Based Velocity Clamping</h2>

<p>
To ensure absolute reliability in competitive and clinical evaluations, Module 04 incorporates four layers of mathematical anti-glitch defense:
</p>

<h3 id="sec6-1">6.1 Anatomical Angular Velocity Clamping ($\Delta \theta \le 48.0^\circ$)</h3>
<p>
Human biomechanics dictates that a human joint cannot rotate faster than approximately $1,400^\circ$ per second under load. At $30\text{ FPS}$, a single video frame spans $33.3\text{ milliseconds}$. Therefore, the maximum physically possible joint rotation in a single frame is:
</p>

<div class="formula-card">
$$\Delta \theta_{\max} = \omega_{\max} \cdot \Delta t \approx 1,450^\circ/\text{s} \times 0.0333\text{ s} \approx 48.0^\circ$$
</div>

<p>
In <code>RepCounterService.dart</code>, the velocity filter checks every incoming angle against the previous frame:
</p>
<pre><code>// Velocity spike filter: human limbs cannot rotate > 48 deg in 33ms
if ((angle - _prevAngle).abs() > 48.0 && _prevAngle > 35.0) {
  angle = _prevAngle; // Clamps to previous verified physical position
}
_prevAngle = angle;</code></pre>
<p>
If a shadow or lighting change causes a keypoint to jump across the screen by $70^\circ$ in a single frame, the spike is immediately rejected, preserving tracking integrity.
</p>

<h3 id="sec6-2">6.2 Minimum Cadence Time Lock ($\ge 10\text{ frames} / \sim 0.33\text{s}$)</h3>
<p>
Even in explosive athletic training, a complete eccentric-concentric movement cycle cannot occur in under $0.33\text{ seconds}$. The variable <code>_framesSinceLastRep</code> accumulates on every frame. If an athlete rebounds out of the bottom in $<10\text{ frames}$, the rep is held until the minimum physiological cadence is satisfied, preventing vibration double-counting.
</p>

<h3 id="sec6-3">6.3 Incomplete Half-Rep Rejection & Reset Logic</h3>
<p>
If an athlete descends partially (e.g., reaching $128^\circ$ instead of the required $120.0^\circ$) and re-extends back to standing, the state machine recognizes that <code>Stage 3 (BOTTOM)</code> was never satisfied. When the angle re-expands past $148^\circ + 10.0^\circ$ ($158^\circ$), the machine automatically purges the state back to <code>up</code> without counting a repetition:
</p>
<pre><code>else if (angle > (upThresh + 10.0)) {
  // Re-extended without sufficient depth hold: reset cleanly
  _state = 'up';
  _framesInDownState = 0;
}</code></pre>

<h3 id="sec6-4">6.4 Boundary Truncation & Occlusion Guards</h3>
<p>
In <code>backend/kinematics.py</code>, tracking frames are rejected if:
</p>
<ul>
    <li>Ankles or feet drop below the bottom screen edge ($y > 0.985$).</li>
    <li>The athlete's head is truncated by the top screen edge ($y < 0.01$).</li>
    <li>Key joint detection visibility falls below $0.35$ (severe occlusion).</li>
</ul>

---

<h2 id="sec7">7. The Posture-Gated Isometric Plank Hold Engine</h2>

<p>
Planks present an engineering paradox: <strong>An isometric exercise has zero repetitions</strong>. An athlete does not move up and down; they maintain a static, motionless posture against gravity.
</p>

<blockquote>
<strong>Plain-English Concept:</strong> In naive fitness apps, a plank timer is just a dumb stopwatch: you press "Start", and the clock ticks from 1 to 60 seconds even if you are lying flat on your stomach checking your phone! In BioMechAI, the plank timer is a smart, posture-gated clock. It only ticks when your body is held in a textbook straight line. The instant your hips sag toward the floor or pike into the air, the clock freezes dead in its tracks. You don't get credit for a single second of holding a bad plank!
</blockquote>

<h3>The Posture-Gated Hold Architecture (Milestone #27 / #36)</h3>
<p>
Implemented in <code>workout_screen.dart</code>, the plank hold engine executes a continuous 1 Hz clock gated by Dr. Stuart McGill's spinal alignment standard ($150^\circ-190^\circ$):
</p>

<pre><code>POSTURE-GATED ISOMETRIC PLANK HOLD ENGINE
===================================================================================
1. Frame Evaluated: Spinal Line (Shoulder-to-Hip-to-Ankle)
   |
   +---> Is Angle between 150.0 deg and 190.0 deg?
            |
            |-- YES (Safe Neutral Spine):
            |   * Skeleton: Lime Green (#3FB950)
            |   * Hold Clock: ADVANCES (+1 second)
            |   * Periodic Voice Announcements: "10 seconds held", "20 seconds held"...
            |
            +-- NO (POSTURE BREACH DETECTED!):
                * Is Angle < 150.0 deg? -> "Raise your hips, keep body straight!"
                * Is Angle > 190.0 deg? -> "Lower your hips into a straight line!"
                * Skeleton: Instantly flashes Crimson Red (#F85149)
                * Hold Clock: IMMEDIATELY FREEZES! (Accumulation halted)
                * Voice Alert: Priority 1 Safety Interrupt
===================================================================================</code></pre>

<h3>Intelligent Resumption Voice Cadence:</h3>
<p>
When the athlete corrects their body elevation and re-enters the $150^\circ-190^\circ$ zone:
</p>
<ol>
    <li>The skeleton immediately transitions from Crimson Red back to Lime Green.</li>
    <li>The hold clock seamlessly resumes accumulating seconds from where it paused.</li>
    <li>The on-device voice coach speaks aloud: <em>"Resuming Plank"</em>, providing positive reinforcement without resetting the clock to zero.</li>
</ol>

---

<h2 id="sec8">8. Quality Partitioning: Total Reps vs. Valid Reps</h2>

<p>
To maintain clinical rigor, Module 04 partitions exercise volume into two distinct metrics:
</p>

<pre><code>Repetition Quality Split
===================================================================================
TOTAL REPS = Completed physical movement cycles through TOP-BOTTOM-TOP.
VALID REPS = Movement cycles completed with:
             1. Overall Form Score >= 45.0%
             2. Zero High-Severity Clinical Violations (hasHighSeverity == false)
===================================================================================</code></pre>

<p>
If an athlete performs 10 squat repetitions, but on reps 4 and 7 their knees buckled inward into severe dynamic knee valgus ($<165^\circ$), the system logs:
<br><strong>Total Reps: 10 | Valid Reps: 8</strong>
<br>This distinction is preserved in Cloud Firestore (<code>/workout_sessions/{id}</code>) and highlighted in the Trainer Web Dashboard, allowing coaches to audit movement efficiency.
</p>

---

<h2 id="sec9">9. Cloud vs. Edge Synchronization: Zero-Latency Local Counting</h2>

<p>
A common pitfall in connected fitness systems is network latency lag: if rep counting is performed exclusively on a cloud server, network jitter causes rep announcements to arrive $500-1,000\text{ ms}$ late.
</p>

<p>
<strong>BioMechAI's Hybrid Solution:</strong>
</p>
<ul>
    <li><strong>Edge Priority Execution</strong>: Repetition counting is calculated <em>on-device in Dart</em> via <code>RepCounterService</code>. Rep completions and audible announcements fire in $<15\text{ milliseconds}$ directly from the smartphone camera stream.</li>
    <li><strong>Cloud Shadow Verification</strong>: The cloud backend (<code>backend/kinematics.py</code>) executes a parallel <code>RepetitionStateMachine</code> at 30 Hz. When cloud telemetry arrives, the app checks:
        <pre><code>if (repNum != null && repNum <= _repCounter.totalReps) {
  return; // Already announced on-device in <50ms! Suppress duplicate audio
}</code></pre>
    </li>
    <li>This guarantees the athlete receives instant audio confirmation the exact millisecond they lock out a rep, while the cloud server maintains a verified audit log.</li>
</ul>

---

<h2 id="sec10">10. Scientific Standards, Biomechanical Literature, & NSCA Guidelines</h2>

<ul>
    <li><strong>National Strength and Conditioning Association (NSCA Essentials, 4th Edition)</strong>:
        <br>Governs repetition cadence and range-of-motion definitions: defines parallel squat depth as the crease of the hip passing below the top of the patella ($\theta \approx 90^\circ-115^\circ$), and full lockout as complete knee and hip extension ($\theta > 146^\circ$).
    </li>
    <li><strong>Dr. Stuart M. McGill (2010)</strong>:
        <br><em>"Core Training: Evidence Translating to Better Performance and Injury Prevention."</em>
        <br>Establishes the scientific basis for our isometric plank engine: proved that isometric abdominal endurance is superior to dynamic spinal flexion (sit-ups) for spine stability, provided the shoulder-hip-ankle line is maintained between $150^\circ$ and $190^\circ$.
    </li>
    <li><strong>Kompf & Arandjelović (2016)</strong>:
        <br><em>"The Sticking Point in the Bench Press and Squat: Analysis and Overcoming Strategies."</em> Sports Medicine, 46(6), 751-766.
        <br>Provides the biomechanical rationale for our turnaround hold and velocity clamping: athletes exhibit deceleration near the inflection point, proving that legitimate reps require inflection stabilization ($>66\text{ ms}$).
    </li>
</ul>

---

<h2 id="sec11">11. Panel Defense Quick-Reference: Frequently Asked Questions & Rapid Answers</h2>

<div class="defense-card">
<strong>Q1: Why did you use a Finite State Machine instead of simple peak detection or wearable smartwatch accelerometers?</strong><br>
<em>Rapid Defense Answer:</em> Smartwatches only detect wrist acceleration, which fails on lower-body exercises like squats and lunges. Simple peak detection algorithms fail whenever an athlete shivers or hesitates, causing double-counting glitches. Our closed 4-stage Finite State Machine mathematically enforces the complete physical movement cycle: TOP $\to$ DESCENDING $\to$ BOTTOM $\to$ ASCENDING $\to$ TOP. It is physically impossible to register a repetition without completing every anatomical phase.
</div>

<div class="defense-card">
<strong>Q2: How does the system prevent an athlete from cheating by doing fast "half-reps" or quarter-squats?</strong><br>
<em>Rapid Defense Answer:</em> We enforce strict Hysteresis Gating. In a squat, the state machine requires the knee angle to break below the $120.0^\circ$ parallel depth threshold and hold for at least 2 consecutive frames before transitioning to the bottom state. If an athlete only descends to $130^\circ$ (a quarter squat) and stands back up, the bottom state is never triggered, and the rep counter remains at zero.
</div>

<div class="defense-card">
<strong>Q3: How does your system track planks if there are no moving repetitions to count?</strong><br>
<em>Rapid Defense Answer:</em> We engineered a Posture-Gated Isometric Hold Engine. During planks, repetition counting is deactivated, and a dedicated 1 Hz hold clock takes over. Crucially, the clock is gated by Dr. Stuart McGill's spinal alignment standard ($150^\circ-190^\circ$). The second the athlete's hips sag below $150^\circ$, the hold clock immediately freezes, the skeleton turns Crimson Red, and the voice coach orders: <em>"Raise your hips, keep body straight!"</em>. The clock resumes only when textbook posture is restored.
</div>

<div class="defense-card">
<strong>Q4: What is the "Velocity Spike Filter" in your code, and why is 48 degrees the chosen threshold?</strong><br>
<em>Rapid Defense Answer:</em> In human biomechanics, joints cannot rotate faster than approximately $1,450^\circ$ per second under load. At 30 FPS ($33\text{ ms}$ per frame), the maximum physically possible angular displacement is $48.0^\circ$. If camera lighting noise causes a keypoint to jump by $70^\circ$ in a single frame, our filter clamps the value back to the previous verified position, preventing camera glitches from corrupting the state machine.
</div>

<div class="defense-card">
<strong>Q5: What is the difference between "Total Reps" and "Valid Reps" on the workout summary screen?</strong><br>
<em>Rapid Defense Answer:</em> Total Reps measures pure mechanical volume (how many full movement cycles were finished). Valid Reps measures clinical movement quality: a repetition is only certified as Valid if the overall form score is $\ge 45\%$ and zero high-severity orthopedic faults occurred (such as severe knee valgus or spinal sag). This distinction allows coaches to immediately see if an athlete is compromising joint health to chase repetition volume.
</div>

<div class="defense-card">
<strong>Q6: How do you prevent repetition announcements from lagging behind the athlete's actual movements?</strong><br>
<em>Rapid Defense Answer:</em> We execute repetition state transitions on-device directly within the mobile app's <code>RepCounterService</code>. Rep counting occurs locally in $<15\text{ milliseconds}$, triggering the native TTS voice coach the exact millisecond the athlete completes the rep. While the cloud server runs a shadow state machine for verification, local execution eliminates all network latency lag.
</div>

<div class="defense-card">
<strong>Q7: What happens to the repetition count if an athlete steps out of the camera frame to drink water?</strong><br>
<em>Rapid Defense Answer:</em> In <code>workout_screen.dart</code>, when an athlete steps out of frame, the system pauses tracking and caches their completed reps in memory (<code>_savedReps = _repCounter.totalReps</code>). When the athlete returns to the camera frame, the system restores their exact rep count and announces: <em>"Resuming [Exercise Name]"</em>, allowing continuous training without lost workout data.
</div>
