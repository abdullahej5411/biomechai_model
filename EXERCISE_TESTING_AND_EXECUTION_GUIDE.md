# BioMechAI — Complete Exercise Testing & Execution Guide

Welcome to the **BioMechAI Practical Testing Guide**. This document explains step-by-step how to position your camera and perform each of the **7 supported exercises** so you can easily test and verify every feature of the app—including real-time rep counting, posture grading, skeleton color changes, and voice coaching.

All technical, medical, and biomechanical terms are explained in **plain, simple everyday words** so that anyone can follow along.

---

## 1. Quick Camera & Environment Setup (Do This First!)

Before starting any exercise, set up your testing area:

1. **Camera Placement**:
   * Prop your phone against a wall, water bottle, or put it on a chair/tripod at roughly **hip or chest height**.
   * Keep the phone **vertical (portrait mode)**.
2. **Distance**:
   * Stand back about **2.0 to 2.5 meters (6 to 8 feet)** from the camera.
   * **Rule of Thumb**: Your **entire body** must be visible on screen from the **top of your head down to the tips of your shoes**.
3. **Lighting & Clothing**:
   * Make sure the room has good lighting. 
   * Avoid standing directly in front of a bright window (backlighting makes your body look like a dark shadow).
   * Wear clothes that contrast with your background so the AI camera can clearly track your joints.

---

## 2. How the App Works During Exercise

* **Exercise Selection**:
  * **Option A (Manual - Recommended for quick testing)**: Tap the exercise dropdown at the top, select your exercise (e.g., *Squat*), and step into position.
  * **Option B (Auto-Detect via AI)**: Stand still for 1 second in frame, then begin your movement naturally. The AI will recognize your exercise automatically and lock in!
* **Skeleton Color Codes**:
  * 🟢 **Neon Blue / Cyan**: **Perfect, safe posture!** Your angles are aligned.
  * 🔴 **Crimson Red**: **Form error or injury risk detected!** The AI detected a posture mistake.
* **Rep Counter**:
  * Reps only count when you complete the **full motion** (Starting position $\rightarrow$ Going down $\rightarrow$ Reaching the bottom $\rightarrow$ Returning fully to the start).
* **Voice Coaching**:
  * The app speaks aloud through your phone speaker to correct mistakes (e.g., *"Push your knees outward!"*, *"Keep your hips up!"*) and praises good reps (*"Great depth!"*).

---

## 3. Step-by-Step Guide for Each of the 7 Exercises

---

### Exercise 1: Squat

> **Best Camera Angle**: **Front-Diagonal View** (Stand facing roughly 45 degrees towards the camera so it can see both your knee bend and knee spacing).

#### How to Do a Perfect Rep (Green Skeleton)
1. **Starting Position**: Stand tall with your feet about shoulder-width apart, toes pointing slightly outward. Keep your chest up and your hands in front of your chest.
2. **Going Down**: Push your hips backward and bend your knees as if you are sitting back into a low chair.
3. **The Bottom Position**: Lower yourself until your **thighs are parallel to the floor** (roughly a 90° bend at the knees). Keep your knees pushed out in line with your feet.
4. **Coming Up**: Push through your heels to stand straight back up until your hips and knees are fully extended. The rep counter will click!

#### How to Intentionally Test a Form Error (Red Skeleton & Audio Warning)
* **Test 1: Knee Cave-In (Dynamic Knee Valgus)**:
  * *What it means in simple terms*: Your knees wobble and collapse inward toward each other like an "X" shape instead of staying pushed out. This puts dangerous twisting pressure on your knee joints and your **ACL** (the main stabilizing ligament in your knee).
  * *How to trigger it*: As you lower down, deliberately bring your knees close together until they almost touch.
  * *Result*: The skeleton turns **Crimson Red**, a red warning card appears, and the AI voice warns: *"Knees caving in! Push knees outward to protect ACL."*
* **Test 2: Shallow Depth**:
  * *What it means*: Bending your knees only a few inches instead of doing a full squat.
  * *How to trigger it*: Crouch down only 20% and stand right back up.
  * *Result*: The rep counter will **not** count the rep because you did not reach proper depth.

---

### Exercise 2: Push-Up

> **Best Camera Angle**: **Side Profile View** (Place your phone on the floor or a low step facing your side so it can see your full body line from head to toe).

#### How to Do a Perfect Rep (Green Skeleton)
1. **Starting Position**: Place your hands slightly wider than shoulder-width apart on the floor. Step your feet back so your body forms a straight, flat plank line from your ears down to your heels.
2. **Going Down**: Keep your core (stomach muscles) tight. Bend your elbows and lower your chest toward the floor until your chest is about a fist's distance from the ground. Keep your elbows angled backward at roughly 45 degrees (like an arrow shape, not a "T" shape).
3. **Coming Up**: Push the floor away through your palms until your arms are fully straight again. The rep counter will click!

#### How to Intentionally Test a Form Error (Red Skeleton & Audio Warning)
* **Test 1: Belly Dropping (Hip Sag)**:
  * *What it means in simple terms*: Letting your stomach and hips droop toward the floor like a sagging banana. This pinches the joints in your lower back (lumbar spine).
  * *How to trigger it*: While doing a push-up, let your hips sink down toward the floor so your back arches excessively.
  * *Result*: The skeleton turns **Crimson Red**, and the voice warns: *"Hips sagging! Tighten your core to protect your lower back."*
* **Test 2: Chicken Wings (Elbow Flare)**:
  * *What it means in simple terms*: Sticking your elbows straight out sideways at 90 degrees (like chicken wings). This pinches and irritates the tendons in your shoulder socket (called *shoulder impingement*).
  * *How to trigger it*: Flare your elbows straight out to the left and right as you lower down.
  * *Result*: Red warning alert and voice: *"Tuck your elbows! Flaring arms risks shoulder impingement."*

---

### Exercise 3: Plank (Isometric Hold)

> **Best Camera Angle**: **Side Profile View** (Phone on the floor or a low surface facing your side).

#### How to Do a Perfect Hold (Timer Running & Green Skeleton)
1. **Starting Position**: Rest your forearms on the floor, elbows directly under your shoulders. Step your feet back on your toes.
2. **Body Alignment**: Squeeze your stomach, glutes (butt muscles), and thighs so your body forms a **single straight line** from your head to your ankles.
3. **The Hold**: Hold this straight posture completely still. 
4. **Result**: As long as your body remains straight (within the safe 150° to 195° range), the **Plank Hold Timer** will continuously count up second-by-second (e.g., `00:15s`, `00:30s`).

#### How to Intentionally Test a Form Error (Red Skeleton & Timer Pause)
* **Test 1: Sagging Hips**:
  * *How to trigger it*: Let your hips sag downward toward the floor.
  * *Result*: The skeleton turns **Crimson Red**, the hold timer pauses, and the voice warns: *"Hips sagging! Squeeze core and glutes to protect spine."*
* **Test 2: Butt in the Air (Hip Pike)**:
  * *How to trigger it*: Push your butt high up in the air like a triangle or tent.
  * *Result*: The skeleton turns **Crimson Red**, and the timer pauses until you flatten your body back into a straight line.

---

### Exercise 4: Bicep Curl

> **Best Camera Angle**: **Front View or 45-Degree Side View** (Phone at waist or chest height).

#### How to Do a Perfect Rep (Green Skeleton)
1. **Starting Position**: Stand tall with your feet hip-width apart. Hold weights (or simply clench your fists) by your sides with your palms facing forward.
2. **Arm Position**: Keep your upper arms (the part between your shoulder and elbow) **pinned snugly against the sides of your ribs**.
3. **The Curl**: Bend your elbows and curl your hands upward toward your shoulders, keeping your upper arms still. Squeeze at the top.
4. **Lowering Down**: Slowly lower your hands back down until your elbows are fully straight. The rep counter will click!

#### How to Intentionally Test a Form Error (Red Skeleton & Audio Warning)
* **Test 1: Swinging Upper Arms (Elbow Drift)**:
  * *What it means in simple terms*: Swinging your elbows forward and lifting your upper arms to heave the weight up. This cheats by using your shoulder muscles instead of your biceps, straining the front of your shoulder.
  * *How to trigger it*: Swing your elbows forward 4 or 5 inches away from your ribs as you curl up.
  * *Result*: Red skeleton and voice: *"Keep your upper arms pinned to your sides — do not swing your elbows."*
* **Test 2: Leaning Back (Torso Swing)**:
  * *What it means in simple terms*: Arching your back and swinging your whole upper body backward to build momentum. This puts heavy strain on your lower spine.
  * *How to trigger it*: Lean your chest and back backwards as you pull your arms up.
  * *Result*: Red skeleton and voice: *"Avoid leaning back! Use only your arms to lift."*

---

### Exercise 5: Lunge

> **Best Camera Angle**: **Front-Diagonal View** (Standing at a slight 45-degree angle to the phone).

#### How to Do a Perfect Rep (Green Skeleton)
1. **Starting Position**: Stand upright with your feet hip-width apart, hands on your hips or in front of your chest.
2. **Stepping Forward**: Take a big, controlled step forward with one leg.
3. **Lowering Down**: Bend both knees until your front thigh is parallel to the ground and your back knee hovers an inch or two above the floor. Make sure your front knee stays centered right over your middle toes (not collapsing inward).
4. **Pushing Back**: Press firmly through your front heel to step back to the starting position. The rep counter will click!

#### How to Intentionally Test a Form Error (Red Skeleton & Audio Warning)
* **Test: Front Knee Collapsing Inward**:
  * *What it means*: Just like in squats, your front knee wobbles inward toward your center line when bending.
  * *How to trigger it*: As you step forward and bend, intentionally let your front knee buckle inward toward the opposite leg.
  * *Result*: Red skeleton and voice: *"Front knee collapsing inward! Align knee with your second toe."*

---

### Exercise 6: High Knees

> **Best Camera Angle**: **Front or Side View** (Phone at waist height, showing your whole body).

#### How to Do a Perfect Rep (Green Skeleton)
1. **Starting Position**: Stand tall with your feet hip-width apart and your chest held high.
2. **The Movement**: Run in place, driving one knee forcefully upward until your **thigh is parallel to the ground** (hip height), then quickly switch legs in a rhythmic, athletic sprint.
3. **Torso Control**: Keep your upper body straight and upright—do not lean heavily forward or backward.

#### How to Intentionally Test a Form Error (Red Skeleton & Audio Warning)
* **Test 1: Excessive Forward Lean**:
  * *What it means*: Hunching or leaning your chest far forward over your legs. This overworks your hip flexors and rounds your lower spine.
  * *How to trigger it*: Lean your chest forward by more than 15 degrees while lifting your knees.
  * *Result*: Red skeleton and voice: *"Keep chest upright! Do not lean forward."*
* **Test 2: Lazy Knees (Low Height)**:
  * *How to trigger it*: Barely lift your feet off the floor (shuffling instead of driving your knees up to hip height).
  * *Result*: The rep counter will not register reps because the required hip flexion angle was not reached.

---

### Exercise 7: Jumping Jack

> **Best Camera Angle**: **Front View** (Phone facing you directly, showing your full arm span and foot stance).

#### How to Do a Perfect Rep (Green Skeleton)
1. **Starting Position**: Stand upright with your feet together and your arms resting at your sides.
2. **The Jump**: Jump your feet out wide (wider than your shoulders) while simultaneously swinging your arms out and all the way **overhead until your hands are above your head**.
3. **The Return**: Jump your feet back together and bring your arms back to your sides in one smooth, balanced motion. The rep counter will click!

#### How to Intentionally Test a Form Error (Red Skeleton & Audio Warning)
* **Test 1: Incomplete Arm Raise**:
  * *What it means*: Flapping your arms only halfway up (to shoulder height) instead of reaching all the way overhead.
  * *How to trigger it*: Jump out with your feet, but only lift your arms to shoulder level (like a "T").
  * *Result*: The rep will be flagged as incomplete or will not count until your hands go overhead.
* **Test 2: Lateral Torso Wobble**:
  * *What it means*: Tilting or wobbling your spine sideways to one side when landing, which puts uneven twisting stress on your joints.
  * *How to trigger it*: Lean your torso noticeably to the left or right when jumping out.
  * *Result*: Red skeleton and voice: *"Keep your spine centered and balanced."*

---

## 4. Finishing and Verifying the Workout

Once you finish testing any of the exercises above:

1. **Tap the End Workout Button** (the red square stop button at the bottom of the camera screen).
2. **Review Your Instant Post-Session Summary**:
   * **Overall Form Score**: A circular gauge showing your average posture quality (e.g., `85%`, `92%`).
   * **Total Duration**: Exact workout length in seconds.
   * **Valid Reps vs Total Reps**: Shows how many reps were performed with correct form vs how many had posture errors.
   * **Exercise Breakdown Timeline**: Displays each exercise block performed during the session.
3. **Verify the Saved Record**:
   * Tap **Done / Return Home**.
   * On the **Home Screen**, scroll down to **"Recent Sessions"**—your newly completed session will appear right at the top!
   * Tap the session to open **Session Details** to see your complete performance summary and any clinical fault notes.
4. **Test Trainer Feedback & Bell Notification**:
   * If a coach enters a comment on this session via the **Web Dashboard** (`https://biomechai-fitness.web.app`):
   * Your phone's **Home Screen Bell Icon** will immediately show a cyan badge with the number `1`!
   * Tap the bell to open the **Notification Screen**.
   * Tap the feedback card to jump directly into the session details and see your coach's notes highlighted in the blue feedback box!

---

## 5. Summary Cheat Sheet: What Good vs Bad Looks Like

| Exercise | What the AI Wants to See (Good) | What Triggers the Red Alert (Bad) |
| :--- | :--- | :--- |
| **Squat** | Thighs parallel to floor, knees pushed outward over toes | Knees collapsing inward toward each other (*Dynamic Knee Valgus*) |
| **Push-Up** | Body completely straight, elbows tucked at 45° | Hips sagging toward the floor (*Hip Sag*) or elbows flaring at 90° (*Chicken Wings*) |
| **Plank** | Straight horizontal line from head to heels held still | Hips sagging down or sticking butt high up in a triangle (*Hip Pike*) |
| **Bicep Curl** | Upper arms glued to ribs, only forearms moving | Elbows swinging forward or torso leaning backward to cheat momentum |
| **Lunge** | Front thigh parallel to ground, front knee tracking straight | Front knee caving inward toward the other leg |
| **High Knees** | Knees lifting to hip level with an upright tall spine | Leaning chest far forward or barely lifting knees off floor |
| **Jumping Jack** | Hands reaching fully overhead, balanced even landing | Arms only raised to shoulder height or leaning torso sideways |

---
*Created for BioMechAI Final Production Defense & Verification.*
