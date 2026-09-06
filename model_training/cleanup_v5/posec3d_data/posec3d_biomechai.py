default_scope = 'mmaction'

# Pretrained PoseC3D model trained on NTU RGB+D 60 (60-class human action recognition)
# Architecture is identical to ours — all backbone weights load cleanly.
# Primary: NTU RGB+D 60 (CVPR 2022)
load_from = 'https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint_20220815-38db104b.pth'
# FineGYM alternative (Phase 3c - high dynamic gymnastics/aerobics):
# load_from = 'https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_gym-keypoint/slowonly_r50_8xb16-u48-240e_gym-keypoint_20220815-da338c58.pth'

custom_imports = dict(imports=['drive_sync_hook'], allow_failed_imports=False)

model = dict(
    type='Recognizer3D',
    backbone=dict(
        type='ResNet3dSlowOnly',
        depth=50,
        pretrained=None,
        in_channels=17, # 17 COCO Keypoints
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
        num_classes=7, # 7 BioMechAI exercises
        dropout_ratio=0.7, # Phase 3a: increased from 0.5 to mitigate confirmed overfitting
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

optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.001), # Phase 3a: increased from 0.0003
    clip_grad=dict(max_norm=40, norm_type=2))

train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=20, val_interval=2) # Phase 3a: reduced from 24 to 20, peak observed at ep 18
val_cfg = dict(type='ValLoop')
val_evaluator = [dict(type='AccMetric')]
test_evaluator = None
test_dataloader = None
test_cfg = None

default_hooks = dict(
    checkpoint=dict(type='CheckpointHook', interval=2, max_keep_ckpts=3, save_best='auto'),
    logger=dict(type='LoggerHook', interval=20))

custom_hooks = [
    dict(type='DriveCheckpointSyncHook',
         token_json_path='/kaggle/working/token.json',
         drive_folder_id='18RWFWo73gzQ1WZXNB5t3KTEr9cScz9Rx',
         work_dir='/kaggle/working/biomechai_posec3d_full_run')
]
