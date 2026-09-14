"""
BioMechAI Kinematics & Fast-Timescale Biomechanical Engine (30 Hz)
Per-frame joint angle geometry, Munro FPPA dynamic knee valgus evaluation,
and closed finite state machine repetition counting.
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional
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

def validate_landmark_tracking(
    hip: Any,
    knee: Any,
    ankle: Any,
    min_visibility: float = 0.65,
    max_boundary_y: float = 0.94
) -> Tuple[bool, str]:
    """
    Validates anatomical landmark visibility and camera framing.
    Rejects tracking frames where:
    1. Ankles/feet drop out of camera boundary (y > max_boundary_y).
    2. Any key joint has low MediaPipe detection confidence (visibility < min_visibility).
    """
    joints = [("hip", hip), ("knee", knee), ("ankle", ankle)]
    for name, lm in joints:
        vis = getattr(lm, "visibility", 1.0)
        if vis is not None and vis < min_visibility:
            return False, f"LOW_VISIBILITY_{name.upper()}"
        y = getattr(lm, "y", lm[1] if isinstance(lm, (list, tuple)) else 0.5)
        if y > max_boundary_y:
            return False, f"FEET_OUT_OF_FRAME_{name.upper()}"
        if y < 0.02:
            return False, f"HEAD_OUT_OF_FRAME_{name.upper()}"
    return True, "VALID"

class RepetitionStateMachine:
    """
    Strict Finite State Machine: TOP -> DESCENDING -> BOTTOM -> ASCENDING -> TOP
    A repetition ONLY increments when returning to TOP (> TOP_RETURN_THRESHOLD)
    after having reached a verified valid BOTTOM (< BOTTOM_DEPTH_THRESHOLD).
    Rejects corrupted depth readings when landmarks are occluded or out-of-frame.
    """
    def __init__(self):
        self.rep_count = 0
        self.stage = "TOP"
        self.min_flexion_reached = 180.0
        self.last_rep_event: Optional[Dict[str, Any]] = None

    def update(self, knee_flexion: float, frame_idx: int, is_tracking_valid: bool = True) -> Optional[Dict[str, Any]]:
        rep_completed_event = None

        # Only update minimum depth on anatomically valid, non-occluded frames
        can_update_depth = is_tracking_valid and (knee_flexion >= KNEE_FLEXION_SANITY_FLOOR)

        if self.stage == "TOP" and knee_flexion < 150.0:
            self.stage = "DESCENDING"
            if can_update_depth:
                self.min_flexion_reached = knee_flexion
        elif self.stage == "DESCENDING":
            if can_update_depth:
                if knee_flexion < self.min_flexion_reached:
                    self.min_flexion_reached = knee_flexion
                if knee_flexion < BOTTOM_DEPTH_THRESHOLD:
                    self.stage = "BOTTOM"
            elif knee_flexion > 150.0:
                # Stood back up without verified bottom or with occluded landmarks: reset cleanly
                self.stage = "TOP"
                self.min_flexion_reached = 180.0
        elif self.stage == "BOTTOM":
            if can_update_depth and knee_flexion < self.min_flexion_reached:
                self.min_flexion_reached = knee_flexion
            if is_tracking_valid and knee_flexion > 110.0:
                self.stage = "ASCENDING"
        elif self.stage == "ASCENDING":
            # Rep completion ONLY fires when returning to TOP on a verified, valid frame
            if is_tracking_valid and knee_flexion > TOP_RETURN_THRESHOLD:
                self.rep_count += 1
                rep_completed_event = {
                    "rep_number": self.rep_count,
                    "frame_idx": frame_idx,
                    "min_flexion": round(self.min_flexion_reached, 1),
                    "return_flexion": round(knee_flexion, 1),
                    "threshold_crossed": TOP_RETURN_THRESHOLD
                }
                self.last_rep_event = rep_completed_event
                self.stage = "TOP"
                self.min_flexion_reached = 180.0
            elif can_update_depth and knee_flexion < BOTTOM_DEPTH_THRESHOLD:
                # Re-entered bottom before completing extension
                self.stage = "BOTTOM"

        return rep_completed_event

    def reset(self):
        self.rep_count = 0
        self.stage = "TOP"
        self.min_flexion_reached = 180.0
        self.last_rep_event = None

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

class VoiceCoachingEngine:
    """
    Day 3 Module 8: Real-Time Voice Coaching Engine.
    Enforces edge-triggered state transitions, cooldown windows,
    and priority preemption so audio coaching never spams at 30 FPS.
    """
    def __init__(self, warning_cooldown_sec: float = 3.5, recovery_cooldown_sec: float = 5.0):
        self.prev_has_warning = False
        self.prev_alert_code = "NORMAL_NEUTRAL"
        self.last_warning_voice_time = 0.0
        self.last_recovery_voice_time = 0.0
        self.warning_cooldown_sec = warning_cooldown_sec
        self.recovery_cooldown_sec = recovery_cooldown_sec

    def evaluate(
        self,
        rep_event: Optional[Dict[str, Any]],
        form_alert: Dict[str, Any],
        current_time: float
    ) -> Optional[Dict[str, Any]]:
        current_has_warning = form_alert.get("has_warning", False)
        current_code = form_alert.get("code", "NORMAL_NEUTRAL")

        cue = None

        # Priority 1: Safety Warning Onset (false -> true) OR change in warning code
        if current_has_warning:
            is_onset = not self.prev_has_warning
            is_code_change = (current_code != self.prev_alert_code)
            has_cooldown_expired = (current_time - self.last_warning_voice_time) >= self.warning_cooldown_sec

            if (is_onset or is_code_change) and has_cooldown_expired:
                cue_text = form_alert.get("voice_cue") or "Check your form!"
                cue = {
                    "cue_id": current_code,
                    "text": cue_text,
                    "priority": 1,
                    "type": "safety_warning"
                }
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

        # Priority 3: Form Recovery (true -> false)
        elif self.prev_has_warning and not current_has_warning:
            if (current_time - self.last_recovery_voice_time) >= self.recovery_cooldown_sec:
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

