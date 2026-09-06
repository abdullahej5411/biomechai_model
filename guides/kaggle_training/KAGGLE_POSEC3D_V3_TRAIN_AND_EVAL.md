# BioMechAI — PoseC3D v3 Complete Kaggle GPU Training & Evaluation

Copy and paste the cell below directly into a new cell in your Kaggle notebook (with GPU Tesla T4 enabled).
This script:
1. Re-verifies video disjoint split integrity (0 video leakage).
2. Writes `pose_transforms_extra.py` (introducing `RandomRotateKeypoints` for camera viewpoint tilt) directly to `/kaggle/working/`.
3. Writes `posec3d_biomechai_v3.py` with `dropout=0.6`, `weight_decay=0.0005`, and `max_epochs=18`.
4. Trains PoseC3D v3 across 18 epochs on Tesla T4 GPU.
5. Automatically isolates the peak validation checkpoint (`best_acc_top1_epoch_*.pth`).
6. Automatically runs full 444-clip held-out evaluation, prints the 7-class confusion matrix, and computes the complete 4-Way Comparison Table.

---

```python
import os, sys, subprocess, pickle, glob
import numpy as np

# ======================================================================
# STEP 0: Verify Dataset Split Integrity
# ======================================================================
TRAIN_PKL = "/kaggle/input/datasets/abdullahej/biomechai-production-data/custom_dataset_train.pkl"
VAL_PKL   = "/kaggle/input/datasets/abdullahej/biomechai-production-data/custom_dataset_val.pkl"

if not os.path.exists(TRAIN_PKL):
    TRAIN_PKL = "/kaggle/working/custom_dataset_train.pkl"
if not os.path.exists(VAL_PKL):
    VAL_PKL = "/kaggle/working/custom_dataset_val.pkl"

with open(TRAIN_PKL, "rb") as f:
    train_data = pickle.load(f)
with open(VAL_PKL, "rb") as f:
    val_data = pickle.load(f)

train_vids = set(x["video_id"] for x in train_data)
val_vids = set(x["video_id"] for x in val_data)
overlap = train_vids.intersection(val_vids)

print("="*75)
print("🚀 POSEC3D v3: PRE-TRAINING INTEGRITY VERIFICATION")
print("="*75)
print(f"Train Clips : {len(train_data)} across {len(train_vids)} videos")
print(f"Val Clips   : {len(val_data)} across {len(val_vids)} videos")
print(f"Video Overlap: {len(overlap)} (Strict 0 Video Leakage: {len(overlap) == 0})")
assert len(overlap) == 0, "FATAL: Video leakage detected between train and val splits!"
print("✅ Split integrity verified: strictly 0 video overlap.")

# ======================================================================
# STEP 1: Write Custom Transform (RandomRotateKeypoints) to Disk
# ======================================================================
# Patch: Disable conflicting multimodal import in MMAction2 (fixes transformers conflict)
models_init = '/kaggle/working/mmaction2/mmaction/models/__init__.py'
if os.path.exists(models_init):
    with open(models_init, 'r') as f:
        code = f.read()
    if 'from .multimodal import *' in code and not '# from .multimodal import *' in code:
        code = code.replace('from .multimodal import *', '# from .multimodal import *')
        with open(models_init, 'w') as f:
            f.write(code)
        print("✅ Patched mmaction/models/__init__.py (disabled unused multimodal import).")

transform_code = r'''import numpy as np
from mmcv.transforms import BaseTransform
from mmaction.registry import TRANSFORMS

@TRANSFORMS.register_module()
class RandomRotateKeypoints(BaseTransform):
    """Randomly rotate 2D keypoints around image center to synthesize camera tilt.
    
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
'''

with open("/kaggle/working/pose_transforms_extra.py", "w") as f:
    f.write(transform_code)
print("✅ Created /kaggle/working/pose_transforms_extra.py with RandomRotateKeypoints transform.")

# ======================================================================
# STEP 2: Write PoseC3D v3 Config File to Disk
# ======================================================================
config_code = r'''default_scope = 'mmaction'

load_from = 'https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint_20220815-38db104b.pth'

custom_imports = dict(imports=['pose_transforms_extra', 'drive_sync_hook'], allow_failed_imports=True)

model = dict(
    type='Recognizer3D',
    backbone=dict(
        type='ResNet3dSlowOnly',
        depth=50,
        pretrained=None,
        in_channels=17,
        base_channels=32,
        num_stages=3,
        out_indices=(2,),
        stage_blocks=(4, 6, 3),
        conv1_stride_s=1,
        pool1_stride_s=1,
        inflate=(0, 1, 1),
        spatial_strides=(2, 2, 2),
        temporal_strides=(1, 1, 2),
        dilations=(1, 1, 1)),
    cls_head=dict(
        type='I3DHead',
        in_channels=512,
        num_classes=7,
        dropout_ratio=0.6, # Option B (v3): moderate sweet spot
        average_clips='prob'))

dataset_type = 'PoseDataset'
data_root = './'
ann_file_train = 'custom_dataset_train.pkl'
ann_file_val = 'custom_dataset_val.pkl'

left_kp = [1, 3, 5, 7, 9, 11, 13, 15]
right_kp = [2, 4, 6, 8, 10, 12, 14, 16]

train_pipeline = [
    dict(type='UniformSampleFrames', clip_len=48),
    dict(type='PoseDecode'),
    dict(type='PoseCompact', hw_ratio=1., allow_imgpad=True),
    dict(type='Resize', scale=(-1, 64)),
    dict(type='RandomResizedCrop', area_range=(0.56, 1.0)),
    dict(type='Resize', scale=(56, 56), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5, left_kp=left_kp, right_kp=right_kp),
    dict(type='RandomRotateKeypoints', max_angle=12.0, prob=0.5), # Option B: camera viewpoint tilt jitter
    dict(type='GeneratePoseTarget', sigma=0.6, use_score=True, with_kp=True, with_limb=False),
    dict(type='FormatShape', input_format='NCTHW_Heatmap'),
    dict(type='PackActionInputs')
]

val_pipeline = [
    dict(type='UniformSampleFrames', clip_len=48, num_clips=1, test_mode=True),
    dict(type='PoseDecode'),
    dict(type='PoseCompact', hw_ratio=1., allow_imgpad=True),
    dict(type='Resize', scale=(-1, 56)),
    dict(type='CenterCrop', crop_size=56),
    dict(type='GeneratePoseTarget', sigma=0.6, use_score=True, with_kp=True, with_limb=False),
    dict(type='FormatShape', input_format='NCTHW_Heatmap'),
    dict(type='PackActionInputs')
]

train_dataloader = dict(
    batch_size=16,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        pipeline=train_pipeline))

val_dataloader = dict(
    batch_size=16,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        pipeline=val_pipeline,
        test_mode=True))

test_dataloader = dict(
    batch_size=16,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        pipeline=val_pipeline,
        test_mode=True))

optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0005), # Option B: moderate weight decay
    clip_grad=dict(max_norm=40, norm_type=2))

train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=18, val_interval=2) # Option B: 18 epochs peak window
val_cfg = dict(type='ValLoop')
val_evaluator = [dict(type='AccMetric')]
test_cfg = dict(type='TestLoop')
test_evaluator = [dict(type='AccMetric')]

default_hooks = dict(
    checkpoint=dict(type='CheckpointHook', interval=2, max_keep_ckpts=3, save_best='auto'),
    logger=dict(type='LoggerHook', interval=20))

custom_hooks = [
    dict(type='DriveCheckpointSyncHook',
         token_json_path='/kaggle/working/token.json',
         drive_folder_id='18RWFWo73gzQ1WZXNB5t3KTEr9cScz9Rx',
         work_dir='/kaggle/working/biomechai_posec3d_v3_run')
]
'''

CONFIG_PATH = "/kaggle/working/posec3d_biomechai_v3.py"
with open(CONFIG_PATH, "w") as f:
    f.write(config_code)
print(f"✅ Created {CONFIG_PATH} with PoseC3D v3 specifications.")

# ======================================================================
# STEP 3: Launch Retraining (18 Epochs)
# ======================================================================
WORK_DIR = "/kaggle/working/biomechai_posec3d_v3_run"
os.makedirs(WORK_DIR, exist_ok=True)

cmd = [
    sys.executable, "/kaggle/working/mmaction2/tools/train.py",
    CONFIG_PATH,
    "--cfg-options",
    f"train_dataloader.dataset.ann_file={TRAIN_PKL}",
    f"val_dataloader.dataset.ann_file={VAL_PKL}",
    f"test_dataloader.dataset.ann_file={VAL_PKL}",
    f"custom_hooks.0.work_dir={WORK_DIR}",
    "--work-dir", WORK_DIR
]

env = os.environ.copy()
env["PYTHONPATH"] = "/kaggle/working:" + env.get("PYTHONPATH", "")

print("\n" + "="*75)
print("🚀 LAUNCHING POSEC3D v3 TRAINING (18 EPOCHS) ON TESLA T4 GPU...")
print("="*75)

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
for line in process.stdout:
    print(line, end="")

process.wait()
assert process.returncode == 0, f"❌ Training failed with returncode {process.returncode}"
print("\n" + "="*75)
print("🎉 POSEC3D v3 TRAINING COMPLETED SUCCESSFULLY!")
print("="*75)

# ======================================================================
# STEP 4: Automated Evaluation of the Peak Validation Checkpoint
# ======================================================================
best_ckpts = glob.glob(os.path.join(WORK_DIR, "best_acc_top1_epoch_*.pth"))
if not best_ckpts:
    best_ckpts = glob.glob(os.path.join(WORK_DIR, "epoch_*.pth"))
best_ckpts.sort(key=os.path.getmtime)
peak_ckpt = best_ckpts[-1]
print(f"\n🔍 Evaluating Peak Checkpoint: {os.path.basename(peak_ckpt)}")

DUMP_PKL = "/kaggle/working/phase4_v3_result.pkl"
test_cmd = [
    sys.executable, "/kaggle/working/mmaction2/tools/test.py",
    CONFIG_PATH,
    peak_ckpt,
    "--dump", DUMP_PKL,
    "--cfg-options",
    f"test_dataloader.dataset.ann_file={VAL_PKL}"
]

test_proc = subprocess.run(test_cmd, capture_output=True, text=True, env=env)
print(test_proc.stdout)
if test_proc.returncode != 0:
    print(test_proc.stderr)
    raise RuntimeError("Evaluation failed!")

# ======================================================================
# STEP 5: Generate Confusion Matrix & 4-Way Comparison Table
# ======================================================================
with open(DUMP_PKL, "rb") as f:
    results = pickle.load(f)

classes = sorted(list(set(x["label"] for x in val_data)))
cm = np.zeros((len(classes), len(classes)), dtype=int)
top1_correct = 0

for item, pred in zip(val_data, results):
    true_cls = item["label"]
    scores = pred["pred_scores"]
    pred_cls = np.argmax(scores)
    cm[true_cls, pred_cls] += 1
    if true_cls == pred_cls:
        top1_correct += 1

total_clips = len(val_data)
top1_acc = (top1_correct / total_clips) * 100.0
recalls = [cm[i, i] / cm[i].sum() * 100.0 for i in range(len(classes))]
macro_recall = np.mean(recalls)

class_names = ['bicep_curl', 'high_knees', 'jumping_jack', 'lunge', 'plank', 'pushup', 'squat']

print("\n" + "="*75)
print(f"📊 POSEC3D v3 EVALUATION RESULTS ({os.path.basename(peak_ckpt)})")
print("="*75)
print(f"Overall Top-1 Accuracy: {top1_acc:.2f}% ({top1_correct}/{total_clips})")
print(f"Balanced Macro Recall : {macro_recall:.2f}%\n")

print("Confusion Matrix:")
header = f"{'':15}" + "".join([f"{name[:6]:>8}" for name in class_names]) + f"{'Total':>8}"
print(header)
for i, name in enumerate(class_names):
    row = f"{name:15}" + "".join([f"{cm[i, j]:>8}" for j in range(len(class_names))]) + f"{cm[i].sum():>8}"
    print(row)

print("\n" + "="*75)
print("🏆 AUTHORITATIVE 4-WAY COMPARISON TABLE")
print("="*75)
print(f"{'Exercise':15} | {'RF v5':>8} | {'PoseC3D v1':>10} | {'PoseC3D v2':>10} | {'PoseC3D v3':>10}")
print("-" * 65)

# Baseline references
rf_ref = [60.27, 46.34, 52.63, 66.18, 71.88, 57.14, 36.99]
v1_ref = [46.58, 58.54, 18.42, 69.12, 78.12, 63.27, 28.77]
v2_ref = [26.03, 43.90, 39.47, 76.47, 76.56, 28.57, 23.29]

for i, name in enumerate(class_names):
    print(f"{name:15} | {rf_ref[i]:>7.2f}% | {v1_ref[i]:>9.2f}% | {v2_ref[i]:>9.2f}% | {recalls[i]:>9.2f}%")

print("-" * 65)
print(f"{'Overall Top-1':15} | {'56.08%':>8} | {'49.77%':>10} | {'44.82%':>10} | {top1_acc:>9.2f}%")
print(f"{'Macro Recall':15} | {'55.92%':>8} | {'51.83%':>10} | {'44.90%':>10} | {macro_recall:>9.2f}%")
print("="*75)
```
