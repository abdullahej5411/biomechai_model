import numpy as np
from mmcv.transforms import BaseTransform
from mmaction.registry import TRANSFORMS

@TRANSFORMS.register_module()
class RandomRotateKeypoints(BaseTransform):
    """Randomly rotate 2D keypoints around image center to synthesize camera viewpoint tilt.
    
    Args:
        max_angle (float): Maximum rotation angle in degrees (+/- max_angle). Default: 12.0.
        prob (float): Probability of applying rotation. Default: 0.5.
    """
    def __init__(self, max_angle=12.0, prob=0.5):
        self.max_angle = max_angle
        self.prob = prob

    def transform(self, results):
        if np.random.rand() > self.prob:
            return results
        
        angle = np.random.uniform(-self.max_angle, self.max_angle)
        rad = np.deg2rad(angle)
        cos_a, sin_a = np.cos(rad), np.sin(rad)
        
        h, w = results['img_shape'][:2]
        cx, cy = w / 2.0, h / 2.0
        
        kps = results['keypoint']
        x = kps[..., 0] - cx
        y = kps[..., 1] - cy
        
        new_x = cos_a * x - sin_a * y + cx
        new_y = sin_a * x + cos_a * y + cy
        
        new_x = np.clip(new_x, 0, w - 1)
        new_y = np.clip(new_y, 0, h - 1)
        
        results['keypoint'] = np.stack([new_x, new_y], axis=-1).astype(kps.dtype)
        return results
