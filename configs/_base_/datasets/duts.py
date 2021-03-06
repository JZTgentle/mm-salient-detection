# dataset settings
dataset_type = 'SODDataset'
data_root = 'data/DUTS/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
crop_size = (512, 1024)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', reduce_one_label='min'),
    dict(type='Resize', img_scale=(1024*1.5, 512*1.5), ratio_range=(0, 0.5, 0.75, 1.0)),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.9),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size=crop_size, pad_val=0, seg_pad_val=0),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1024, 512),
        # img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='DUTS-TR/DUTS-TR-Image',
        ann_dir='DUTS-TR/DUTS-TR-Mask1',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='DUTS-TE/DUTS-TE-Image',
        ann_dir='DUTS-TE/DUTS-TE-Mask1',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='DUTS-TE/DUTS-TE-Image',
        ann_dir='DUTS-TE/DUTS-TE-Mask1',
        pipeline=test_pipeline))
