# BioMechAI — Milestone Report #35: Granular Exercise Breakdown Timeline, Posture-Weighted Plank Scoring, and Direct Post-Session Navigation (v2.8)

**Date**: October 5, 2026  
**Academic Phase**: Semester 8 — FYP-II Final Defense Deliverable  
**Author**: Abdullah Ejaz Shah & BioMechAI Autonomous Engineering Agent  
**Production Artifacts**:
- Release APK: [`BioMechAI_v2.8_ExerciseBreakdown.apk`](file:///d:/Study%20Folder/Semester%208/FYP-I/Final%20Evaluation/fypbiomechai/biomechai_model/BioMechAI_v2.8_ExerciseBreakdown.apk) (98.2 MB)
- Flutter Repository Commit: `lib/screens/session_detail_screen.dart`, `lib/screens/workout_screen.dart`, `lib/providers/workout_provider.dart`, `lib/widgets/exercise_timeline_card.dart`, `lib/services/firebase_service.dart`

---

## 1. Executive Summary & Problem Analysis

In comprehensive multi-exercise workout testing, three specific UX and telemetry gaps were identified:

1. **Truncated Summary & Missing Exercise Breakdown**:
   - In `SessionDetailScreen`, exercises were rendered solely as a single text row inside the `Performance Summary` card with `maxLines: 2` and `TextOverflow.ellipsis`. When performing multiple exercises (e.g. Squat, Bicep Curl, Jumping Jack, High Knees, Lunge, Push-Up, Plank), the text was truncated after `"Pus..."`, completely hiding Plank and later exercises from the athlete's view.
   - Athletes lacked visibility into their individual exercise scores, rep counts, and hold durations.

2. **Abrupt "End Session" Navigation Flow**:
   - Tapping "End Session" previously called `Navigator.pop(context)`, immediately terminating the camera and returning the user to the `HomeScreen`. The user was forced to manually navigate to the History tab and find the latest session just to inspect their form score and workout performance.

3. **Plank Scoring Continuity in Session Aggregation**:
   - While isometric plank timing was gated to neutral spine alignment (150°–195° standard), the final form score of the plank block was evaluated based only on the final instantaneous frame posture rather than an accumulated time-weighted score over the entire duration of the hold.

---

## 2. Architecture & Implementation Details

```
+--------------------------------------------------------------------------------+
|                             WorkoutScreen Flow                                 |
|                                                                                |
|  [Active Exercise / Plank]                                                    |
|           |                                                                    |
|           v                                                                    |
|  User Taps "End Session"                                                       |
|           |                                                                    |
|           +--> 1. Finalizes active ExerciseBlock (reps, hold time, form score) |
|           +--> 2. Stops camera stream safely (avoids frame buffer leakage)     |
|           +--> 3. Captures in-memory completedBlocks list                      |
|           +--> 4. Awaits provider.endSession(userId)                           |
|           |        - Calculates weighted session form score                    |
|           |        - Writes session doc + subcollections to Firestore          |
|           |                                                                    |
|           v                                                                    |
|  Navigator.pushReplacement(SessionDetailScreen(                                |
|       session: completedSession, initialBlocks: completedBlocks                |
|  ))                                                                            |
+--------------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------------+
|                          SessionDetailScreen View                              |
|                                                                                |
|  [FormScoreRing (Overall Session Form Score)]                                  |
|  [Date & Time Stamp]                                                           |
|                                                                                |
|  [Performance Summary Card]                                                    |
|    - Duration: X seconds                                                       |
|    - Total Valid Reps: Y                                                       |
|    - Total Reps: Z                                                             |
|    - Exercises: All 7 exercises fully visible (maxLines: 4)                    |
|                                                                                |
|  [Exercise Breakdown Section] (0ms instant render via initialBlocks)           |
|    +------------------------------------------------------------------------+  |
|    | ExerciseTimelineCard: Squat                                            |  |
|    | [ScoreRing 90%]  Squat                 10:14 AM                        |  |
|    |                  10 reps (9 valid) • Legs                              |  |
|    +------------------------------------------------------------------------+  |
|    | ExerciseTimelineCard: Plank                                            |  |
|    | [ScoreRing 95%]  Plank                 10:17 AM                        |  |
|    |                  30s hold • Core                                       |  |
|    +------------------------------------------------------------------------+  |
|    | ExerciseTimelineCard: Push-Up                                          |  |
|    | [ScoreRing 85%]  Push-Up               10:20 AM                        |  |
|    |                  8 reps (7 valid) • Chest                              |  |
|    +------------------------------------------------------------------------+  |
|                                                                                |
|  [Trainer Feedback Card] (if provided by coach via Module 9 portal)           |
+--------------------------------------------------------------------------------+
```

---

## 3. Detailed Component Modifications

### 3.1. Firestore Subcollection Retrieval (`firebase_service.dart`)
Added `getSessionExerciseBlocks` to query `users/{userId}/workout_sessions/{sessionId}/exercises`:
- Uses in-memory timestamp sorting (`blocks.sort((a, b) => a.startTimestamp.compareTo(b.startTimestamp))`) to guarantee zero composite index build requirements in Firestore.

### 3.2. Granular Exercise Timeline Card (`exercise_timeline_card.dart`)
- **Isometric Hold Formatting**: When `block.exerciseName.toLowerCase() == 'plank'`, volume is formatted as `${block.totalReps}s hold • Core`.
- **Dynamic Rep Formatting**: Dynamic exercises display `${block.totalReps} reps (${block.validReps} valid) • ${weightOrGroup}`.
- **Fixed Encoding**: Eliminated corrupted bullet byte characters, ensuring crisp ` • ` separators.
- **Form Score Ring**: Visualizes each exercise's individual biomechanical score using `FormScoreRing(score: block.avgFormScore, size: 45)`.

### 3.3. Dual-Mode Session Detail Screen (`session_detail_screen.dart`)
- Converted to `StatefulWidget` accepting `final List<ExerciseBlock>? initialBlocks`.
- **Instant Display (0ms)**: When passed directly from `WorkoutScreen`, renders immediately with zero network latency.
- **Asynchronous History Fetch**: When opened from `HistoryScreen` or `HomeScreen`, automatically triggers `_loadExerciseBlocks()` with a clean `CircularProgressIndicator(color: AppTheme.blue)` loading state.
- **Responsive Summary Row**: Extended stat row `maxLines` from 2 to 4, guaranteeing that even when all 7 clinical exercises are completed in a single workout, none are cut off by ellipses.

### 3.4. Posture-Weighted Plank Scoring & Aggregation (`workout_screen.dart` & `workout_provider.dart`)
- Tracked continuous time-weighted scoring during Plank:
  $$\text{Plank Score} = \frac{\int \text{FrameScore}(t) \, dt}{\int dt}$$
  Where frames with strict spine alignment (150°–195°) and clean telemetry award 95%, and posture violations award 50%.
- `WorkoutProvider.endSession` weights both repetition counts and hold times into the overall session score:
  $$\text{Session Form Score} = \frac{\sum \text{avgFormScore}_i \times \max(\text{volume}_i, 1)}{\sum \max(\text{volume}_i, 1)}$$

### 3.5. Direct Post-Session Replacement Navigation (`workout_screen.dart`)
- In `_endSession()`:
  1. Grabs `provider` and `auth` before any async suspension to ensure complete context safety.
  2. Stops the camera image stream before upload begins.
  3. Replaces the active route with `SessionDetailScreen` via `Navigator.pushReplacement`.
  4. When the user dismisses `SessionDetailScreen`, they return cleanly to `HomeScreen` with updated recent activity.

---

## 4. Quality Assurance & Static Analysis Certification

- **Static Analysis Result**: `dart analyze` executed across all modified files yielded **0 errors** and **0 warnings**.
- **Visual Design Compliance**: Strictly preserved all tokens (`AppTheme.bg`, `AppTheme.card`, `AppTheme.card2`, `AppTheme.border`, `AppTheme.text`, `AppTheme.muted`, `AppTheme.blue`).
- **Production Build Status**: Release APK compiled successfully with Gradle:
  - Artifact: `BioMechAI_v2.8_ExerciseBreakdown.apk` (102,919,889 bytes / 98.2 MB).
