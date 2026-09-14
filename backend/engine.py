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
    POSEC3D_CONFIG,
    POSEC3D_CHECKPOINT,
    CLASSES,
    CLASS_DISPLAY_NAMES,
    COCO_MP_MAP
)

# Insert model directory into sys.path
sys.path.insert(0, os.path.join(BASE_DIR, "models", "posec3d_v5_limb"))
sys.path.insert(0, os.path.join(BASE_DIR, "mmaction2_repo"))

from mmaction.apis import init_recognizer, inference_recognizer
from mmengine.dataset import Compose
from mmengine.registry import init_default_scope

class PoseC3DEngine:
    def __init__(self, device: str = "cpu"):
        print(f"[PoseC3DEngine] Initializing PoseC3D v5 model on {device}...")
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
        return self.last_prediction

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

        kp_input = coco_kps[np.newaxis, ...] # (1, T, 17, 2)
        kp_score = np.ones((1, T, 17), dtype=np.float32) * 0.9

        anno = {
            "frame_dir": "",
            "label": -1,
            "img_shape": (h, w),
            "origin_shape": (h, w),
            "start_index": 0,
            "modality": "Pose",
            "total_frames": T,
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
