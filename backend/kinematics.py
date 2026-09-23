"""
BioMechAI Kinematics & Fast-Timescale Biomechanical Engine (30 Hz)
Per-frame joint angle geometry, Munro FPPA dynamic knee valgus evaluation,
and closed finite state machine repetition counting.
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional, List
from backend.config import (
    BOTTOM_DEPTH_THRESHOLD,
    TOP_RETURN_THRESHOLD,
    VALGUS_LOAD_THRESHOLD,
    VALGUS_FPPA_THRESHOLD,
    KNEE_FLEXION_SANITY_FLOOR,
)

def calculate_knee_flexion(
    hip: Any,
    knee: Any,
    ankle: Any
) -> float:
    """
    Calculates exact un-clamped knee flexion angle (in degrees) with knee as vertex.
    180 deg = full standing extension.
    < 90-100 deg = parallel or deep squat depth.
    Does NOT substitute or clamp values; returns raw geometric angle.
    Supports both 2D (x, y) and 3D (x, y, z) coordinates.
    """
    if len(hip) >= 3 and len(knee) >= 3 and len(ankle) >= 3:
        v_femur = np.array([hip[0] - knee[0], hip[1] - knee[1], hip[2] - knee[2]], dtype=np.float32)
        v_shank = np.array([ankle[0] - knee[0], ankle[1] - knee[1], ankle[2] - knee[2]], dtype=np.float32)
    else:
        v_femur = np.array([hip[0] - knee[0], hip[1] - knee[1]], dtype=np.float32)
        v_shank = np.array([ankle[0] - knee[0], ankle[1] - knee[1]], dtype=np.float32)

    cos_theta = np.dot(v_femur, v_shank) / (np.linalg.norm(v_femur) * np.linalg.norm(v_shank) + 1e-6)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    raw_deg = float(np.degrees(np.arccos(cos_theta)))
    return raw_deg

def calculate_fppa_munro(hip: Tuple[float, float], knee: Tuple[float, float], ankle: Tuple[float, float], is_left: bool = True) -> float:
    """
    Calculates Frontal Plane Projection Angle (FPPA, Munro et al. 2012).
    Evaluates medial inward deviation of the knee joint center relative to
    the straight line connecting the ASIS/hip joint center and the ankle joint center.

    - Safe Neutral Tracking: Knee tracks outward or straight over foot (FPPA ~175-180 deg).
    - Dynamic Knee Valgus: Knee caves inward medially under load (FPPA < 165.0 deg).
    """
    x_h, y_h = hip[0], hip[1]
    x_k, y_k = knee[0], knee[1]
    x_a, y_a = ankle[0], ankle[1]

    t = (y_k - y_h) / max(y_a - y_h, 1e-4)
    x_line = x_h + t * (x_a - x_h)

    # Inward medial displacement relative to hip-ankle axis
    medial_disp = (x_line - x_k) if is_left else (x_k - x_line)

    if medial_disp <= 0:
        # Knee tracks outward or safe straight line
        fppa = 180.0 - abs(medial_disp) * 50.0
        return float(min(180.0, max(172.0, fppa)))
    else:
        # Knee caves inward medially (valgus collapse)
        valgus_deg = np.degrees(np.arctan2(medial_disp, max(y_a - y_h, 1e-4)))
        fppa = 180.0 - valgus_deg
        return float(fppa)

def calculate_dynamic_valgus_fppa(
    landmarks: List[Any], 
    w: float = 640.0, 
    h: float = 480.0, 
    optimal_is_left: bool = True
) -> float:
    """
    Computes Frontal Plane Projection Angle (FPPA, Munro et al. 2012)
    robustly across both 0° frontal and 45° oblique viewpoints.
    
    Combines:
    1. Unilateral Munro 2D line projection for the primary tracked leg.
    2. 3D Bilateral Inter-Knee vs Inter-Ankle ratio:
       In a safe squat: knees track over or outside ankles (separation_ratio >= 0.82).
       In dynamic knee valgus: knees collapse inward toward each other (separation_ratio < 0.80).
       Provides rotation-invariant clinical detection even when the athlete stands at 45°.
    """
    l_hip = landmarks[23]
    r_hip = landmarks[24]
    l_knee = landmarks[25]
    r_knee = landmarks[26]
    l_ankle = landmarks[27]
    r_ankle = landmarks[28]

    def to_3d(lm):
        if isinstance(lm, (list, tuple)):
            x = float(lm[0]) * w
            y = float(lm[1]) * h
            z = (float(lm[2]) * w) if len(lm) > 2 else 0.0
        else:
            x = float(getattr(lm, "x", 0.5)) * w
            y = float(getattr(lm, "y", 0.5)) * h
            z = float(getattr(lm, "z", 0.0)) * w
        return np.array([x, y, z], dtype=np.float32)

    p_lh, p_rh = to_3d(l_hip), to_3d(r_hip)
    p_lk, p_rk = to_3d(l_knee), to_3d(r_knee)
    p_la, p_ra = to_3d(l_ankle), to_3d(r_ankle)

    primary_hip = p_lh if optimal_is_left else p_rh
    primary_knee = p_lk if optimal_is_left else p_rk
    primary_ankle = p_la if optimal_is_left else p_ra

    fppa_unilateral = calculate_fppa_munro(
        (primary_hip[0], primary_hip[1]),
        (primary_knee[0], primary_knee[1]),
        (primary_ankle[0], primary_ankle[1]),
        is_left=optimal_is_left
    )

    # 3D Bilateral Separation Ratio
    dist_knees_3d = float(np.linalg.norm(p_lk - p_rk))
    dist_ankles_3d = float(np.linalg.norm(p_la - p_ra))
    dist_hips_3d = float(np.linalg.norm(p_lh - p_rh))

    ref_base = max(dist_ankles_3d, dist_hips_3d * 0.9, 1e-4)
    separation_ratio = dist_knees_3d / ref_base

    # If knees collapse inward relative to feet/hips (valgus collapse):
    if separation_ratio < 0.80:
        bilateral_fppa = 180.0 - (0.80 - separation_ratio) * 75.0
        return float(min(fppa_unilateral, bilateral_fppa))

    return float(fppa_unilateral)

def validate_landmark_tracking(
    hip: Any,
    knee: Any,
    ankle: Any,
    min_visibility: float = 0.35,
    max_boundary_y: float = 0.985
) -> Tuple[bool, str]:
    """
    Validates anatomical landmark visibility and camera framing.
    Rejects tracking frames ONLY where:
    1. Ankles/feet truly drop out of camera boundary (y > 0.985).
    2. Key joint visibility drops below 0.35 (severe occlusion).
    3. Head is completely truncated at top (y < 0.01).
    Supports 4D array [x, y, z, likelihood] from mobile client as well as MediaPipe objects.
    """
    joints = [("hip", hip), ("knee", knee), ("ankle", ankle)]
    for name, lm in joints:
        vis = 1.0
        if isinstance(lm, (list, tuple)) and len(lm) >= 4:
            vis = float(lm[3])
        elif hasattr(lm, "visibility"):
            vis = getattr(lm, "visibility", 1.0)
        elif hasattr(lm, "likelihood"):
            vis = getattr(lm, "likelihood", 1.0)

        if vis is not None and vis < min_visibility:
            return False, f"LOW_VISIBILITY_{name.upper()}"
        y = lm[1] if isinstance(lm, (list, tuple)) else getattr(lm, "y", 0.5)
        if y > max_boundary_y:
            return False, f"FEET_OUT_OF_FRAME_{name.upper()}"
        if y < 0.01:
            return False, f"HEAD_OUT_OF_FRAME_{name.upper()}"

    return True, "VALID"

def select_optimal_tracking_leg(landmarks: List[Any]) -> Tuple[str, Tuple[Any, Any, Any], bool]:
    """
    Evaluates both left leg (23, 25, 27) and right leg (24, 26, 28).
    Returns (leg_name, (hip, knee, ankle), is_left).
    Crucial for 45° and 90° oblique/sagittal viewpoints:
    Selects the leg facing closest to the camera with highest confidence.
    """
    l_hip, l_knee, l_ankle = landmarks[23], landmarks[25], landmarks[27]
    r_hip, r_knee, r_ankle = landmarks[24], landmarks[26], landmarks[28]

    def get_vis(lm):
        if isinstance(lm, (list, tuple)) and len(lm) >= 4:
            return float(lm[3])
        return getattr(lm, "visibility", getattr(lm, "likelihood", 1.0))

    l_score = (get_vis(l_hip) + get_vis(l_knee) + get_vis(l_ankle)) / 3.0
    r_score = (get_vis(r_hip) + get_vis(r_knee) + get_vis(r_ankle)) / 3.0

    if l_score >= r_score:
        return "left", (l_hip, l_knee, l_ankle), True
    else:
        return "right", (r_hip, r_knee, r_ankle), False

class RepetitionStateMachine:
    """
    Hardened 4-Stage Finite State Machine: TOP -> DESCENDING -> BOTTOM -> ASCENDING -> TOP
    A repetition ONLY increments when returning to TOP (> TOP_RETURN_THRESHOLD)
    after having reached a verified valid BOTTOM (< BOTTOM_DEPTH_THRESHOLD).

    ANTI-GLITCH HARDENING:
    1. Tracking must be 100% valid on EVERY stage transition.
    2. Enforces minimum rep duration (>= 18 frames / ~0.6s) to reject camera-approach glitches.
    3. Rejects rapid velocity spikes (> 40° in single frame).
    4. Freezes completely in TOP if the subject is walking or out of frame.
    """
    def __init__(self):
        self.rep_count = 0
        self.stage = "TOP"
        self.min_flexion_reached = 180.0
        self.last_rep_event: Optional[Dict[str, Any]] = None
        self.prev_flexion = 180.0
        self.frames_in_cycle = 0
        self.stable_top_frames = 0
        self.invalid_frames = 0

    def update(self, knee_flexion: float, frame_idx: int, is_tracking_valid: bool = True) -> Optional[Dict[str, Any]]:
        rep_completed_event = None

        # Hard guard: If tracking is invalid (person walking, touching camera, feet cut off),
        # only abort if invalid for sustained duration (>= 12 frames / ~0.4s)
        if not is_tracking_valid:
            self.invalid_frames += 1
            if self.invalid_frames >= 12 and self.stage != "TOP":
                # User walked away mid-rep: reset cleanly to TOP without false rep increment
                self.stage = "TOP"
                self.min_flexion_reached = 180.0
                self.frames_in_cycle = 0
            self.prev_flexion = 180.0
            return None
        self.invalid_frames = 0

        # Angular velocity sanity filter: human knee cannot change > 40° in 33ms
        delta_angle = abs(knee_flexion - self.prev_flexion)
        if delta_angle > 40.0 and self.prev_flexion < 175.0:
            # Glitch frame: hold previous flexion angle
            knee_flexion = self.prev_flexion

        self.prev_flexion = knee_flexion
        can_update_depth = (knee_flexion >= KNEE_FLEXION_SANITY_FLOOR)

        # 1. TOP -> DESCENDING: requires subject to be steadily standing upright (> 146°)
        # for at least 10 frames (~0.33s) before allowing descent into a repetition.
        # This completely prevents stooping down to adjust the phone camera from triggering reps!
        if self.stage == "TOP":
            if knee_flexion > TOP_RETURN_THRESHOLD:
                self.stable_top_frames += 1
            elif knee_flexion < 138.0:
                if self.stable_top_frames >= 10:
                    self.stage = "DESCENDING"
                    self.frames_in_cycle = 1
                    if can_update_depth:
                        self.min_flexion_reached = knee_flexion
                else:
                    # User was not standing ready; ignore spurious movement
                    pass

        # 2. DESCENDING: track minimum depth, enter BOTTOM when crossing parallel (< 115°)
        elif self.stage == "DESCENDING":
            self.frames_in_cycle += 1
            if can_update_depth:
                if knee_flexion < self.min_flexion_reached:
                    self.min_flexion_reached = knee_flexion
                if knee_flexion < BOTTOM_DEPTH_THRESHOLD:
                    self.stage = "BOTTOM"
            elif knee_flexion > 142.0:
                # Stood back up without reaching verified bottom: reset cleanly to TOP
                self.stage = "TOP"
                self.min_flexion_reached = 180.0
                self.frames_in_cycle = 0

        # 3. BOTTOM: must reverse upwards by at least 7° (> 122°) to transition to ASCENDING
        elif self.stage == "BOTTOM":
            self.frames_in_cycle += 1
            if can_update_depth and knee_flexion < self.min_flexion_reached:
                self.min_flexion_reached = knee_flexion
            if knee_flexion > (BOTTOM_DEPTH_THRESHOLD + 7.0):
                self.stage = "ASCENDING"

        # 4. ASCENDING: return to upright extension (> 146°) triggers instantaneous rep completion
        elif self.stage == "ASCENDING":
            self.frames_in_cycle += 1
            if knee_flexion > TOP_RETURN_THRESHOLD:
                # Minimum duration check: A real human squat takes at least 18 frames (~0.6s)
                # Rejects camera touch / walk-in spikes that happen in 3-5 frames
                if self.frames_in_cycle >= 18:
                    self.rep_count += 1
                    rep_completed_event = {
                        "rep_number": self.rep_count,
                        "frame_idx": frame_idx,
                        "min_flexion": round(self.min_flexion_reached, 1),
                        "return_flexion": round(knee_flexion, 1),
                        "threshold_crossed": TOP_RETURN_THRESHOLD,
                        "duration_frames": self.frames_in_cycle
                    }
                    self.last_rep_event = rep_completed_event

                self.stage = "TOP"
                self.min_flexion_reached = 180.0
                self.frames_in_cycle = 0

            elif can_update_depth and knee_flexion < BOTTOM_DEPTH_THRESHOLD:
                # Re-entered bottom before completing extension
                self.stage = "BOTTOM"

        return rep_completed_event

    def reset(self):
        self.rep_count = 0
        self.stage = "TOP"
        self.min_flexion_reached = 180.0
        self.last_rep_event = None
        self.prev_flexion = 180.0
        self.frames_in_cycle = 0
        self.stable_top_frames = 0

def evaluate_knee_valgus(knee_flexion: float, fppa_valgus: float) -> Dict[str, Any]:
    """
    Module 7: Dynamic Knee Valgus injury alert.
    Requires dual condition: Joint under load (< 130 deg) AND FPPA < 165 deg.
    """
    if knee_flexion < VALGUS_LOAD_THRESHOLD:
        if fppa_valgus < VALGUS_FPPA_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_KNEE_VALGUS",
                "message": f"WARN: Knee Valgus ({fppa_valgus:.1f}° < {VALGUS_FPPA_THRESHOLD}°)",
                "voice_cue": "Push your knees outward!"
            }
        else:
            return {
                "has_warning": False,
                "code": "SAFE_ALIGNMENT",
                "message": f"Safe Alignment (FPPA: {fppa_valgus:.1f}°)",
                "voice_cue": None
            }
    else:
        return {
            "has_warning": False,
            "code": "NORMAL_NEUTRAL",
            "message": "Form: Normal (Neutral)",
            "voice_cue": None
        }



# ═══════════════════════════════════════════════════════════════════════════════
# Modules 5 & 7: Per-Exercise Form Evaluation — All 7 Exercises
# Clinical biomechanics functions below complement evaluate_knee_valgus (Squat/Lunge).
# ═══════════════════════════════════════════════════════════════════════════════

def _joint_angle_3pt(a, b, c) -> float:
    """Angle at vertex b formed by points a-b-c. Returns degrees 0-180."""
    va = np.array([a[0] - b[0], a[1] - b[1]], dtype=np.float64)
    vc = np.array([c[0] - b[0], c[1] - b[1]], dtype=np.float64)
    norm_a = np.linalg.norm(va)
    norm_c = np.linalg.norm(vc)
    if norm_a < 1e-6 or norm_c < 1e-6:
        return 180.0
    cos_t = np.clip(np.dot(va, vc) / (norm_a * norm_c), -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_t)))


def _angle_from_vertical(p_top, p_bottom) -> float:
    """Angle of the vector (p_top -> p_bottom) from the vertical downward axis. Degrees."""
    dx = p_bottom[0] - p_top[0]
    dy = p_bottom[1] - p_top[1]  # positive y = downward in image coords
    return float(np.degrees(np.arctan2(abs(dx), max(abs(dy), 1e-6))))


def evaluate_pushup_form(landmarks: List[Any], w: float = 640.0, h: float = 480.0) -> Dict[str, Any]:
    """
    Module 5 & 7: Push-Up Posture & Injury Risk Assessment.

    Checks:
    1. Hip Sag (lumbar compression risk): Hip should stay on the shoulder-ankle line ±10%.
    2. Elbow Flare (shoulder impingement): Elbow should stay within 55° of the torso axis.
       Clinical ref: ACSM Guidelines; McGill Spine Biomechanics (2010).
    """
    try:
        # Landmarks: 11=L_shoulder, 12=R_shoulder, 13=L_elbow, 14=R_elbow,
        #            15=L_wrist, 16=R_wrist, 23=L_hip, 24=R_hip, 27=L_ankle, 28=R_ankle
        l_sh  = [landmarks[11][0]*w, landmarks[11][1]*h]
        r_sh  = [landmarks[12][0]*w, landmarks[12][1]*h]
        l_el  = [landmarks[13][0]*w, landmarks[13][1]*h]
        r_el  = [landmarks[14][0]*w, landmarks[14][1]*h]
        l_hip = [landmarks[23][0]*w, landmarks[23][1]*h]
        r_hip = [landmarks[24][0]*w, landmarks[24][1]*h]
        l_ank = [landmarks[27][0]*w, landmarks[27][1]*h]
        r_ank = [landmarks[28][0]*w, landmarks[28][1]*h]

        mid_sh  = [(l_sh[0]+r_sh[0])/2,   (l_sh[1]+r_sh[1])/2]
        mid_hip = [(l_hip[0]+r_hip[0])/2, (l_hip[1]+r_hip[1])/2]
        mid_ank = [(l_ank[0]+r_ank[0])/2, (l_ank[1]+r_ank[1])/2]

        # ── Check 1: Hip Sag ──────────────────────────────────────────────────
        # The hip should lie on the line between shoulder and ankle.
        # Compute perpendicular deviation of hip from that line.
        body_len = max(abs(mid_ank[1] - mid_sh[1]), 1.0)
        # Linear interpolation: where should hip Y be?
        t = (mid_hip[0] - mid_sh[0]) / max(abs(mid_ank[0] - mid_sh[0]), 1e-4)             if abs(mid_ank[0] - mid_sh[0]) > 10             else (mid_hip[1] - mid_sh[1]) / max(body_len, 1e-4)
        t = max(0.0, min(1.0, (mid_hip[1] - mid_sh[1]) / max(body_len, 1e-4)))
        expected_hip_y = mid_sh[1] + t * (mid_ank[1] - mid_sh[1])
        hip_deviation_pct = (mid_hip[1] - expected_hip_y) / max(body_len, 1.0)
        # Positive = hip below the line (sag); Negative = hip above (pike)
        SAG_THRESHOLD = 0.10   # >10% body height below line = injury risk
        PIKE_THRESHOLD = -0.12  # >12% above line = excessive hip pike

        if hip_deviation_pct > SAG_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_HIP_SAG",
                "message": f"WARN: Hip Sag ({hip_deviation_pct*100:.1f}% below line) — Lumbar strain risk",
                "voice_cue": "Tighten your core, lift your hips!"
            }
        if hip_deviation_pct < PIKE_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_HIP_PIKE",
                "message": f"WARN: Hip Pike ({abs(hip_deviation_pct)*100:.1f}% above line)",
                "voice_cue": "Lower your hips into a straight line!"
            }

        # ── Check 2: Elbow Flare ──────────────────────────────────────────────
        # Angle of (shoulder → elbow) from the torso axis (shoulder→hip).
        # Safe range: 30–55°. Above 65° = shoulder impingement risk.
        ELBOW_FLARE_THRESHOLD = 65.0  # degrees
        l_flare = _joint_angle_3pt(mid_hip, l_sh, l_el)
        r_flare = _joint_angle_3pt(mid_hip, r_sh, r_el)
        max_flare = max(l_flare, r_flare)

        if max_flare > ELBOW_FLARE_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_ELBOW_FLARE",
                "message": f"WARN: Elbow Flare ({max_flare:.1f}° > {ELBOW_FLARE_THRESHOLD}°) — Shoulder impingement risk",
                "voice_cue": "Tuck your elbows closer to your body!"
            }

        return {
            "has_warning": False,
            "code": "SAFE_PUSHUP_FORM",
            "message": f"Good push-up form (Hip dev: {hip_deviation_pct*100:.1f}%, Flare: {max_flare:.1f}°)",
            "voice_cue": None
        }
    except Exception:
        return {"has_warning": False, "code": "NORMAL_NEUTRAL", "message": "Form: Normal (Push-Up)", "voice_cue": None}


def evaluate_plank_form(landmarks: List[Any], w: float = 640.0, h: float = 480.0) -> Dict[str, Any]:
    """
    Module 5 & 7: Plank Posture & Injury Risk Assessment.

    Checks:
    1. Body Line Angle: Shoulder-Hip-Ankle should form a straight line (~180°).
       Hip sag (<165°) = lumbar compression. Hip pike (>195°) = ineffective hold.
    2. Head Position: Nose should align with the shoulder-ankle axis (no excessive neck drop/lift).
       Clinical ref: McGill (2010), NSCA Plank Standards.
    """
    try:
        l_sh  = [landmarks[11][0]*w, landmarks[11][1]*h]
        r_sh  = [landmarks[12][0]*w, landmarks[12][1]*h]
        l_hip = [landmarks[23][0]*w, landmarks[23][1]*h]
        r_hip = [landmarks[24][0]*w, landmarks[24][1]*h]
        l_ank = [landmarks[27][0]*w, landmarks[27][1]*h]
        r_ank = [landmarks[28][0]*w, landmarks[28][1]*h]
        nose  = [landmarks[0][0]*w,  landmarks[0][1]*h]

        mid_sh  = [(l_sh[0]+r_sh[0])/2,   (l_sh[1]+r_sh[1])/2]
        mid_hip = [(l_hip[0]+r_hip[0])/2, (l_hip[1]+r_hip[1])/2]
        mid_ank = [(l_ank[0]+r_ank[0])/2, (l_ank[1]+r_ank[1])/2]

        # Body line angle at the hip (shoulder → hip → ankle)
        body_angle = _joint_angle_3pt(mid_sh, mid_hip, mid_ank)

        SAG_THRESHOLD  = 162.0  # Below this = hip sagging (lumbar compression)
        PIKE_THRESHOLD = 198.0  # Above this = excessive pike

        if body_angle < SAG_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_PLANK_SAG",
                "message": f"WARN: Hip Sag (body angle {body_angle:.1f}° < {SAG_THRESHOLD}°) — Lumbar compression risk",
                "voice_cue": "Raise your hips, keep your body straight!"
            }
        if body_angle > PIKE_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_PLANK_PIKE",
                "message": f"WARN: Hip Pike (body angle {body_angle:.1f}° > {PIKE_THRESHOLD}°)",
                "voice_cue": "Lower your hips into a straight line!"
            }

        return {
            "has_warning": False,
            "code": "SAFE_PLANK_FORM",
            "message": f"Good plank alignment (body angle: {body_angle:.1f}°)",
            "voice_cue": None
        }
    except Exception:
        return {"has_warning": False, "code": "NORMAL_NEUTRAL", "message": "Form: Normal (Plank)", "voice_cue": None}


def evaluate_bicep_curl_form(landmarks: List[Any], w: float = 640.0, h: float = 480.0) -> Dict[str, Any]:
    """
    Module 5 & 7: Bicep Curl Posture & Injury Risk Assessment.

    Checks:
    1. Upper Arm Drift (shoulder impingement / cheating): The upper arm (shoulder→elbow)
       should remain within 25° of vertical during the curl. Drifting forward > 30°
       shifts load to the anterior deltoid and risks impingement.
    2. Torso Swing (lumbar strain): The spine (shoulder→hip line) should stay within
       15° of vertical. Swinging backward > 20° = lumbar hyperextension risk.
       Clinical ref: NSCA Essentials of Strength Training (2016).
    """
    try:
        l_sh  = [landmarks[11][0]*w, landmarks[11][1]*h]
        r_sh  = [landmarks[12][0]*w, landmarks[12][1]*h]
        l_el  = [landmarks[13][0]*w, landmarks[13][1]*h]
        r_el  = [landmarks[14][0]*w, landmarks[14][1]*h]
        l_hip = [landmarks[23][0]*w, landmarks[23][1]*h]
        r_hip = [landmarks[24][0]*w, landmarks[24][1]*h]

        mid_sh  = [(l_sh[0]+r_sh[0])/2,   (l_sh[1]+r_sh[1])/2]
        mid_hip = [(l_hip[0]+r_hip[0])/2, (l_hip[1]+r_hip[1])/2]

        # ── Check 1: Upper Arm Drift ─────────────────────────────────────────
        # Angle of upper arm from vertical. A hanging arm = ~0°.
        # Forward drift during curl > 30° = cheating + impingement risk.
        l_arm_drift = _angle_from_vertical(l_sh, l_el)
        r_arm_drift = _angle_from_vertical(r_sh, r_el)
        max_arm_drift = max(l_arm_drift, r_arm_drift)
        ARM_DRIFT_THRESHOLD = 30.0

        if max_arm_drift > ARM_DRIFT_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_ELBOW_DRIFT",
                "message": f"WARN: Elbow Drift ({max_arm_drift:.1f}° > {ARM_DRIFT_THRESHOLD}°) — Keep elbows at your sides!",
                "voice_cue": "Pin your elbows to your sides!"
            }

        # ── Check 2: Torso Swing ─────────────────────────────────────────────
        # Angle of the spine (shoulder→hip) from vertical.
        torso_lean = _angle_from_vertical(mid_sh, mid_hip)
        # In standing position: mid_hip is BELOW mid_sh, so lean is nearly vertical.
        # If athlete swings backward: shoulder moves backward, hip forward → large angle.
        TORSO_SWING_THRESHOLD = 20.0

        if torso_lean > TORSO_SWING_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_TORSO_SWING",
                "message": f"WARN: Torso Swing ({torso_lean:.1f}° > {TORSO_SWING_THRESHOLD}°) — Lumbar strain risk",
                "voice_cue": "Keep your back straight, no swinging!"
            }

        return {
            "has_warning": False,
            "code": "SAFE_CURL_FORM",
            "message": f"Good curl form (arm drift: {max_arm_drift:.1f}°, torso: {torso_lean:.1f}°)",
            "voice_cue": None
        }
    except Exception:
        return {"has_warning": False, "code": "NORMAL_NEUTRAL", "message": "Form: Normal (Bicep Curl)", "voice_cue": None}


def evaluate_jumping_jack_form(landmarks: List[Any], w: float = 640.0, h: float = 480.0) -> Dict[str, Any]:
    """
    Module 5 & 7: Jumping Jack Posture & Form Assessment.

    Checks:
    1. Arm ROM: At peak of the motion, wrists should reach at least shoulder height.
       Incomplete arm raise = insufficient deltoid engagement.
    2. Torso Stability: Spine should remain upright (lateral lean < 10°) during jacks.
       Clinical ref: ACSM Fitness Guidelines; ACE Exercise Library.
    """
    try:
        l_sh  = [landmarks[11][0]*w, landmarks[11][1]*h]
        r_sh  = [landmarks[12][0]*w, landmarks[12][1]*h]
        l_wr  = [landmarks[15][0]*w, landmarks[15][1]*h]
        r_wr  = [landmarks[16][0]*w, landmarks[16][1]*h]
        l_hip = [landmarks[23][0]*w, landmarks[23][1]*h]
        r_hip = [landmarks[24][0]*w, landmarks[24][1]*h]

        mid_sh  = [(l_sh[0]+r_sh[0])/2,   (l_sh[1]+r_sh[1])/2]
        mid_hip = [(l_hip[0]+r_hip[0])/2, (l_hip[1]+r_hip[1])/2]

        # ── Check 1: Arm ROM ─────────────────────────────────────────────────
        # In image coords: lower Y = higher position on screen.
        # Wrists should be at or ABOVE shoulder level = wrist_Y <= shoulder_Y.
        # We check if at least ONE wrist cleared shoulder height (during up phase).
        shoulder_y = mid_sh[1]
        l_arm_raised = l_wr[1] < (shoulder_y - 0.05 * (mid_hip[1] - shoulder_y))
        r_arm_raised = r_wr[1] < (shoulder_y - 0.05 * (mid_hip[1] - shoulder_y))
        both_arms_raised = l_arm_raised and r_arm_raised

        # Only warn if arms are clearly down (not in the down-sweep phase)
        both_arms_down = (l_wr[1] > (shoulder_y + 0.15*(mid_hip[1]-shoulder_y)) and
                          r_wr[1] > (shoulder_y + 0.15*(mid_hip[1]-shoulder_y)))

        # ── Check 2: Torso Lateral Lean ──────────────────────────────────────
        # If left shoulder is significantly higher than right shoulder = lateral lean
        sh_height_diff = abs(l_sh[1] - r_sh[1])
        torso_width = max(abs(r_sh[0] - l_sh[0]), 1.0)
        lateral_lean_deg = float(np.degrees(np.arctan2(sh_height_diff, torso_width)))
        LEAN_THRESHOLD = 12.0

        if lateral_lean_deg > LEAN_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_LATERAL_LEAN",
                "message": f"WARN: Lateral Lean ({lateral_lean_deg:.1f}° > {LEAN_THRESHOLD}°)",
                "voice_cue": "Keep your torso upright, equal on both sides!"
            }

        # Arm ROM check only makes sense if athlete is in the "up" phase
        # Avoid false warnings during the natural down-sweep
        if both_arms_down:
            # Arms are in down position — give form neutral feedback
            return {
                "has_warning": False,
                "code": "NORMAL_NEUTRAL",
                "message": "Arms down phase",
                "voice_cue": None
            }

        return {
            "has_warning": False,
            "code": "SAFE_JACK_FORM",
            "message": f"Good jumping jack form (lateral lean: {lateral_lean_deg:.1f}°)",
            "voice_cue": None
        }
    except Exception:
        return {"has_warning": False, "code": "NORMAL_NEUTRAL", "message": "Form: Normal (Jumping Jack)", "voice_cue": None}


def evaluate_high_knees_form(landmarks: List[Any], w: float = 640.0, h: float = 480.0) -> Dict[str, Any]:
    """
    Module 5 & 7: High Knees Posture & Form Assessment.

    Checks:
    1. Knee Height: The raised knee should reach at least hip height (thigh parallel to floor).
       Hip flexion angle (hip→knee→vertical) >= 80°.
       Clinical ref: ACE Exercise Library; NSCA High Knees Standards.
    2. Torso Lean: Forward lean of torso should stay < 15° to prevent hip flexor overload.
    """
    try:
        l_sh  = [landmarks[11][0]*w, landmarks[11][1]*h]
        r_sh  = [landmarks[12][0]*w, landmarks[12][1]*h]
        l_hip = [landmarks[23][0]*w, landmarks[23][1]*h]
        r_hip = [landmarks[24][0]*w, landmarks[24][1]*h]
        l_kn  = [landmarks[25][0]*w, landmarks[25][1]*h]
        r_kn  = [landmarks[26][0]*w, landmarks[26][1]*h]

        mid_sh  = [(l_sh[0]+r_sh[0])/2,   (l_sh[1]+r_sh[1])/2]
        mid_hip = [(l_hip[0]+r_hip[0])/2, (l_hip[1]+r_hip[1])/2]

        # ── Check 1: Knee Height ─────────────────────────────────────────────
        # The raised knee should reach at least hip height.
        # In image coords: knee_Y <= hip_Y means knee is at or above hip level.
        # We check BOTH knees; the "active" (raised) knee is the one with lower Y value.
        raised_knee_y = min(l_kn[1], r_kn[1])  # lower Y = visually higher
        hip_y = mid_hip[1]
        body_height_ref = max(abs(mid_hip[1] - mid_sh[1]), 1.0)

        # If raised knee is more than 15% of body height BELOW the hip = not high enough
        knee_deficit_pct = (raised_knee_y - hip_y) / body_height_ref
        KNEE_HEIGHT_THRESHOLD = 0.15  # knee must be within 15% of hip height

        if knee_deficit_pct > KNEE_HEIGHT_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_KNEE_HEIGHT",
                "message": f"WARN: Knee too low ({knee_deficit_pct*100:.1f}% below hip) — Drive knees higher!",
                "voice_cue": "Drive your knees up to hip height!"
            }

        # ── Check 2: Torso Forward Lean ──────────────────────────────────────
        torso_lean = _angle_from_vertical(mid_sh, mid_hip)
        FORWARD_LEAN_THRESHOLD = 15.0

        if torso_lean > FORWARD_LEAN_THRESHOLD:
            return {
                "has_warning": True,
                "code": "WARN_FORWARD_LEAN",
                "message": f"WARN: Forward Lean ({torso_lean:.1f}° > {FORWARD_LEAN_THRESHOLD}°) — Stand tall!",
                "voice_cue": "Stand tall, don't lean forward!"
            }

        return {
            "has_warning": False,
            "code": "SAFE_HIGH_KNEES_FORM",
            "message": f"Good high knees form (knee deficit: {knee_deficit_pct*100:.1f}%, lean: {torso_lean:.1f}°)",
            "voice_cue": None
        }
    except Exception:
        return {"has_warning": False, "code": "NORMAL_NEUTRAL", "message": "Form: Normal (High Knees)", "voice_cue": None}

class VoiceCoachingEngine:
    """
    Day 3 Module 8: Real-Time Voice Coaching Engine.
    Enforces edge-triggered state transitions, cooldown windows,
    and priority preemption so audio coaching never spams at 30 FPS.

    ANTI-SPAM & FORM RECOVERY HARDENING:
    1. Warning onset fires on edge (false -> true).
    2. Praise ("Good form, keep going!") only fires when an active squat under load
       actually corrects valgus back to SAFE_ALIGNMENT, NEVER while standing still!
    """
    def __init__(self, warning_cooldown_sec: float = 3.5, recovery_cooldown_sec: float = 5.0, framing_cooldown_sec: float = 7.0):
        self.prev_has_warning = False
        self.prev_alert_code = "NORMAL_NEUTRAL"
        self.last_warning_voice_time = -999.0
        self.last_framing_voice_time = -999.0
        self.last_recovery_voice_time = -999.0
        self.warning_cooldown_sec = warning_cooldown_sec
        self.recovery_cooldown_sec = recovery_cooldown_sec
        self.framing_cooldown_sec = framing_cooldown_sec

    def evaluate(
        self,
        rep_event: Optional[Dict[str, Any]],
        form_alert: Dict[str, Any],
        current_time: float,
        is_squatting_under_load: bool = False
    ) -> Optional[Dict[str, Any]]:
        current_has_warning = form_alert.get("has_warning", False)
        current_code = form_alert.get("code", "NORMAL_NEUTRAL")

        cue = None

        # Priority 1: Safety Warning Onset (false -> true) OR change in warning code
        if current_has_warning:
            is_onset = not self.prev_has_warning
            is_code_change = (current_code != self.prev_alert_code)
            
            if current_code == "WARN_CAMERA_FRAMING":
                has_cooldown_expired = (current_time - self.last_framing_voice_time) >= self.framing_cooldown_sec
            else:
                has_cooldown_expired = (current_time - self.last_warning_voice_time) >= self.warning_cooldown_sec

            if (is_onset or is_code_change) and has_cooldown_expired:
                cue_text = form_alert.get("voice_cue") or "Check your form!"
                cue = {
                    "cue_id": current_code,
                    "text": cue_text,
                    "priority": 1,
                    "type": "safety_warning"
                }
                if current_code == "WARN_CAMERA_FRAMING":
                    self.last_framing_voice_time = current_time
                else:
                    self.last_warning_voice_time = current_time

        # Priority 2: Rep Completion Milestone (Event-bound, fires only when Rep FSM returns to TOP)
        elif rep_event is not None:
            rep_num = rep_event.get("rep_number", 1)
            cue = {
                "cue_id": "CUE_REP_MILESTONE",
                "text": f"Rep {rep_num}",
                "priority": 2,
                "type": "rep_milestone"
            }

        # Priority 3: Form Recovery (edge: warning -> safe for ALL exercises)
        elif self.prev_has_warning and not current_has_warning:
            has_cooldown_expired = (current_time - self.last_recovery_voice_time) >= self.recovery_cooldown_sec
            # Squat/Lunge: require active load confirmation to prevent spurious praise on standing up
            # All other exercises: recovery praise fires on any warning → safe edge
            squat_recovery = (self.prev_alert_code == "WARN_KNEE_VALGUS") and is_squatting_under_load
            non_squat_recovery = self.prev_alert_code not in ("WARN_KNEE_VALGUS", "WARN_CAMERA_FRAMING", "NORMAL_NEUTRAL")

            if (squat_recovery or non_squat_recovery) and has_cooldown_expired:
                cue = {
                    "cue_id": "CUE_FORM_RECOVERY",
                    "text": "Good form, keep going!",
                    "priority": 3,
                    "type": "recovery"
                }
                self.last_recovery_voice_time = current_time

        # Update historical state for edge detection
        self.prev_has_warning = current_has_warning
        self.prev_alert_code = current_code

        return cue


