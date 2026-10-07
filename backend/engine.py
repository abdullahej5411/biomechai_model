"""
BioMechAI Engine: PoseC3D Action Recognition (Module 3)
Loads SlowOnly-R50 limb checkpoint and handles rolling buffer inference
as well as direct sequence classification from Flutter app payloads.
"""

import os
import sys
import asyncio
import torch
import numpy as np
from collections import deque
from typing import Dict, Any, Tuple, List, Optional

# Monkeypatch torch.load for PyTorch 2.6+ MMEngine compatibility
_orig_torch_load = torch.load
torch.load = lambda *args, **kwargs: _orig_torch_load(*args, **{**kwargs, "weights_only": False})

# Limit CPU threads to 2 to prevent CPU core exhaustion during 3D CNN inference
torch.set_num_threads(2)

from backend.config import (
    BASE_DIR,
    ACTIVE_MODEL_VERSION,
    POSEC3D_CONFIG,
    POSEC3D_CHECKPOINT,
    CLASSES,
    CLASS_DISPLAY_NAMES,
    COCO_MP_MAP
)

# Insert model directories into sys.path
sys.path.insert(0, os.path.dirname(POSEC3D_CONFIG))
sys.path.insert(0, os.path.join(BASE_DIR, "models", "posec3d_v5_limb"))
sys.path.insert(0, os.path.join(BASE_DIR, "mmaction2_repo"))

from mmaction.apis import init_recognizer, inference_recognizer
from mmengine.dataset import Compose
from mmengine.registry import init_default_scope

class PoseC3DEngine:
    def __init__(self, device: str = "cpu"):
        print(f"[PoseC3DEngine] Initializing PoseC3D ({ACTIVE_MODEL_VERSION}) model on {device}...")
        print(f"[PoseC3DEngine] Loading checkpoint: {POSEC3D_CHECKPOINT}")
        init_default_scope("mmaction")
        self.model = init_recognizer(POSEC3D_CONFIG, POSEC3D_CHECKPOINT, device=device)
        self.cfg = self.model.cfg
        if not hasattr(self.cfg, "test_pipeline") and hasattr(self.cfg, "val_pipeline"):
            self.cfg.test_pipeline = self.cfg.val_pipeline
        self.pipeline = Compose(self.cfg.test_pipeline)
        
        self.buffer_size = 48
        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.last_prediction = {"exercise": "buffering", "display_name": "Buffering...", "confidence": 0.0, "probabilities": {}}
        self.is_inferring = False
        print("[PoseC3DEngine] Model loaded and ready!")

    def push_coco_keypoints(self, keypoints_17_2d: np.ndarray):
        """Pushes a (17, 2) array of normalized or pixel coordinates into the rolling buffer."""
        self.frame_buffer.append(keypoints_17_2d.astype(np.float32))

    def push_landmarks(self, landmarks_33: List[List[float]]):
        """No-op for PoseC3D engine which consumes COCO-17 keypoints."""
        pass

    def is_buffer_full(self) -> bool:
        return len(self.frame_buffer) == self.buffer_size

    async def trigger_async_inference(self, img_shape: Tuple[int, int] = (480, 640)):
        """Spawns non-blocking PoseC3D inference in a background worker thread."""
        if self.is_inferring or not self.is_buffer_full():
            return
        self.is_inferring = True
        try:
            snapshot = list(self.frame_buffer)
            pred = await asyncio.to_thread(self._predict_from_snapshot, snapshot, img_shape)
            self.last_prediction = pred
        except Exception as e:
            print(f"[PoseC3D Async Inference Error]: {e}")
        finally:
            self.is_inferring = False

    def _predict_from_snapshot(self, snapshot: list, img_shape: Tuple[int, int]) -> Dict[str, Any]:
        buf_array = np.array(snapshot, dtype=np.float32)
        kp_input = buf_array[np.newaxis, ...]
        kp_score = np.ones((1, len(snapshot), 17), dtype=np.float32) * 0.9

        h, w = img_shape
        fake_anno = {
            "frame_dir": "",
            "label": -1,
            "img_shape": (h, w),
            "origin_shape": (h, w),
            "start_index": 0,
            "modality": "Pose",
            "total_frames": len(snapshot),
            "keypoint": kp_input,
            "keypoint_score": kp_score
        }

        with torch.no_grad():
            res = inference_recognizer(self.model, fake_anno, test_pipeline=self.pipeline)
            scores = res.pred_score.cpu().numpy()
            top_idx = int(np.argmax(scores))
            cls_name = CLASSES[top_idx]
            conf = float(scores[top_idx])

        all_probs = {CLASSES[i]: round(float(scores[i]), 4) for i in range(len(CLASSES))}
        return {
            "exercise": cls_name,
            "display_name": CLASS_DISPLAY_NAMES.get(cls_name, cls_name),
            "confidence": round(conf, 4),
            "buffer_pct": 100.0,
            "probabilities": all_probs
        }

    def predict_buffer(self, img_shape: Tuple[int, int] = (480, 640)) -> Dict[str, Any]:
        """Runs PoseC3D on the rolling 48-frame buffer."""
        if not self.is_buffer_full():
            fill_pct = (len(self.frame_buffer) / self.buffer_size) * 100.0
            return {
                "exercise": "buffering",
                "display_name": "Buffering...",
                "confidence": 0.0,
                "buffer_pct": round(fill_pct, 1),
                "probabilities": {}
            }

        buf_array = np.array(self.frame_buffer, dtype=np.float32) # (48, 17, 2)
        kp_input = buf_array[np.newaxis, ...]                     # (1, 48, 17, 2)
        kp_score = np.ones((1, 48, 17), dtype=np.float32) * 0.9

        h, w = img_shape
        fake_anno = {
            "frame_dir": "",
            "label": -1,
            "img_shape": (h, w),
            "origin_shape": (h, w),
            "start_index": 0,
            "modality": "Pose",
            "total_frames": 48,
            "keypoint": kp_input,
            "keypoint_score": kp_score
        }

        with torch.no_grad():
            res = inference_recognizer(self.model, fake_anno, test_pipeline=self.pipeline)
            scores = res.pred_score.cpu().numpy()
            top_idx = int(np.argmax(scores))
            cls_name = CLASSES[top_idx]
            conf = float(scores[top_idx])

        all_probs = {CLASSES[i]: round(float(scores[i]), 4) for i in range(len(CLASSES))}
        self.last_prediction = {
            "exercise": cls_name,
            "display_name": CLASS_DISPLAY_NAMES.get(cls_name, cls_name),
            "confidence": round(conf, 4),
            "buffer_pct": 100.0,
            "probabilities": all_probs
        }
    def clear_buffer(self):
        """Clears rolling buffer and resets prediction state when athlete leaves frame."""
        self.frame_buffer.clear()
        self.last_prediction = {
            "exercise": "out_of_frame",
            "display_name": "Step into Frame",
            "confidence": 0.0,
            "buffer_pct": 0.0,
            "probabilities": {}
        }

    def predict_from_landmarks_sequence(self, raw_sequence: List[List[List[float]]], img_shape: Tuple[int, int] = (480, 640)) -> Dict[str, Any]:
        """
        Accepts raw sequence of frames from Flutter app:
        Shape: (T, 33, 3) where joints are MediaPipe indices.
        Extracts COCO-17 keypoints and feeds into PoseC3D.
        """
        raw_arr = np.array(raw_sequence, dtype=np.float32) # (T, 33, 3) or (T, 33, 2)
        T = raw_arr.shape[0]
        if T < 16:
            return {"exercise": "unknown", "display_name": "Unknown", "confidence": 0.0, "probabilities": {}}

        # Extract COCO-17
        coco_kps = np.zeros((T, 17, 2), dtype=np.float32)
        h, w = img_shape
        for c_idx, mp_idx in enumerate(COCO_MP_MAP):
            # Flutter sends normalized x, y in [0, 1]
            coco_kps[:, c_idx, 0] = raw_arr[:, mp_idx, 0] * w
            coco_kps[:, c_idx, 1] = raw_arr[:, mp_idx, 1] * h

        # Physical presence guard: Only evaluate frames that actually contain a human body
        frame_has_pts = np.sum(np.abs(coco_kps) > 1e-3, axis=(1, 2)) > 5
        valid_coco = coco_kps[frame_has_pts]
        T_valid = valid_coco.shape[0]

        if T_valid < 16:
            return {
                "exercise": "Waiting for Athlete...",
                "raw_class": "unknown",
                "display_name": "Waiting for Athlete...",
                "confidence": 0.0,
                "probabilities": {}
            }

        bbox_w = float(np.max(valid_coco[:, :, 0]) - np.min(valid_coco[:, :, 0]))
        bbox_h = float(np.max(valid_coco[:, :, 1]) - np.min(valid_coco[:, :, 1]))
        if bbox_w < 30.0 or bbox_h < 40.0:
            return {
                "exercise": "Waiting for Athlete...",
                "raw_class": "unknown",
                "display_name": "Waiting for Athlete...",
                "confidence": 0.0,
                "probabilities": {}
            }

        kp_input = valid_coco[np.newaxis, ...] # (1, T_valid, 17, 2)
        kp_score = np.ones((1, T_valid, 17), dtype=np.float32) * 0.9

        anno = {
            "frame_dir": "",
            "label": -1,
            "img_shape": (h, w),
            "origin_shape": (h, w),
            "start_index": 0,
            "modality": "Pose",
            "total_frames": T_valid,
            "keypoint": kp_input,
            "keypoint_score": kp_score
        }

        with torch.no_grad():
            res = inference_recognizer(self.model, anno, test_pipeline=self.pipeline)
            scores = res.pred_score.cpu().numpy()
            top_idx = int(np.argmax(scores))
            cls_name = CLASSES[top_idx]
            conf = float(scores[top_idx])

        all_probs = {CLASSES[i]: round(float(scores[i]), 4) for i in range(len(CLASSES))}
        return {
            "exercise": CLASS_DISPLAY_NAMES.get(cls_name, cls_name),
            "raw_class": cls_name,
            "confidence": round(conf, 4),
            "probabilities": all_probs
        }


# ==============================================================================
# Historical Random Forest Baseline Engine (FYP-I 84% Tabular Model)
# ==============================================================================
def extract_rf_features(landmarks: List[Any]) -> np.ndarray:
    """
    Extracts 50 tabular biomechanical features matching the original FYP-I 84% Random Forest model.
    Landmarks shape: (T, 33, 3) or (T, 33, 2).
    """
    lm = np.array(landmarks, dtype=np.float32)
    def angle(a, b, c):
        ba = lm[:, a, :2] - lm[:, b, :2]
        bc = lm[:, c, :2] - lm[:, b, :2]
        cos = np.sum(ba * bc, axis=1) / (np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1) + 1e-9)
        return np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))

    angle_seqs = {
        'knee_l': angle(23, 25, 27), 'knee_r': angle(24, 26, 28),
        'elbow_l': angle(11, 13, 15), 'elbow_r': angle(12, 14, 16),
        'hip_l': angle(11, 23, 25), 'hip_r': angle(12, 24, 26),
        'shoulder_l': angle(13, 11, 23), 'shoulder_r': angle(14, 12, 24)
    }
    feats = []
    for name, seq in angle_seqs.items():
        feats.extend([
            float(np.mean(seq)),
            float(np.std(seq)),
            float(np.min(seq)),
            float(np.max(seq)),
            float(np.max(seq) - np.min(seq))
        ])
    for name, seq in angle_seqs.items():
        vel = np.diff(seq)
        feats.append(float(np.mean(np.abs(vel))) if len(vel) > 0 else 0.0)
    feats.append(float(np.mean(np.abs(angle_seqs['knee_l'] - angle_seqs['knee_r']))))
    feats.append(float(np.mean(np.abs(angle_seqs['shoulder_l'] - angle_seqs['shoulder_r']))))
    return np.array(feats, dtype=np.float32)


class RandomForestEngine:
    def __init__(self):
        import joblib
        from backend.config import RF_MODEL_PATH, RF_SCALER_PATH, RF_LE_PATH
        print(f"[RandomForestEngine] Initializing 84% Random Forest baseline model...")
        print(f"[RandomForestEngine] Loading model: {RF_MODEL_PATH}")
        self.model = joblib.load(RF_MODEL_PATH)
        self.scaler = joblib.load(RF_SCALER_PATH)
        self.le = joblib.load(RF_LE_PATH)
        self.buffer_size = 60
        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.last_prediction = {"exercise": "buffering", "display_name": "Buffering...", "confidence": 0.0, "probabilities": {}}
        self.is_inferring = False
        print(f"[RandomForestEngine] Model loaded and ready! Classes: {list(self.le.classes_)}")

    def push_coco_keypoints(self, keypoints_17_2d: np.ndarray):
        pass

    def push_landmarks(self, landmarks_33: List[List[float]]):
        self.frame_buffer.append(landmarks_33)

    def is_buffer_full(self) -> bool:
        return len(self.frame_buffer) >= 25

    def clear_buffer(self):
        self.frame_buffer.clear()
        self.last_prediction = {
            "exercise": "out_of_frame",
            "display_name": "Step into Frame",
            "confidence": 0.0,
            "buffer_pct": 0.0,
            "probabilities": {}
        }

    async def trigger_async_inference(self, img_shape: Tuple[int, int] = (480, 640)):
        if self.is_inferring or len(self.frame_buffer) < 25:
            return
        self.is_inferring = True
        try:
            snapshot = list(self.frame_buffer)
            pred = await asyncio.to_thread(self.predict_from_landmarks_sequence, snapshot, img_shape)
            self.last_prediction = pred
        except Exception as e:
            print(f"[RandomForestEngine Async Inference Error]: {e}")
        finally:
            self.is_inferring = False

    def predict_from_landmarks_sequence(self, raw_sequence: List[List[List[float]]], img_shape: Tuple[int, int] = (480, 640)) -> Dict[str, Any]:
        if not raw_sequence or len(raw_sequence) < 16:
            return {
                "exercise": "Waiting for Athlete...",
                "raw_class": "unknown",
                "display_name": "Waiting for Athlete...",
                "confidence": 0.0,
                "probabilities": {}
            }

        feats = extract_rf_features(raw_sequence)
        scaled = self.scaler.transform([feats])
        probs = self.model.predict_proba(scaled)[0]
        top_idx = int(np.argmax(probs))
        raw_cls = str(self.le.classes_[top_idx])
        conf = float(probs[top_idx])

        all_probs = {str(c): round(float(p), 4) for c, p in zip(self.le.classes_, probs)}
        return {
            "exercise": CLASS_DISPLAY_NAMES.get(raw_cls, raw_cls),
            "raw_class": raw_cls,
            "confidence": round(conf, 4),
            "probabilities": all_probs
        }


def create_engine(device: str = "cpu"):
    """Unified engine factory routing to the active model architecture."""
    if ACTIVE_MODEL_VERSION in ["rf", "random_forest"]:
        return RandomForestEngine()
    return PoseC3DEngine(device=device)

