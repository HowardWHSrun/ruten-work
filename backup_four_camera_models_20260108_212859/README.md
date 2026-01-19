# Four Camera Models Backup

This folder contains backups of the four separate camera-specific DLC models.

## Backup Date
January 8, 2026

## Contents

### Camera Models

Each camera has its own trained model:

1. **cam-topleft/** - Model trained specifically for top-left camera view
2. **cam-topright/** - Model trained specifically for top-right camera view
3. **cam-bottomleft/** - Model trained specifically for bottom-left camera view
4. **cam-bottomright/** - Model trained specifically for bottom-right camera view

Each model directory contains:
- `config.yaml` - DeepLabCut configuration
- `labeled-data/` - Labeled training frames for that camera
- `dlc-models/` - Trained model weights and checkpoints
- `training-datasets/` - Training datasets
- `evaluation-results/` - Model evaluation metrics
- `videos/` - Video files used for training

### predictions/
Contains prediction files (H5 format) from pose tracking using these models:
- Session: 2025-05-28_14-12-04_124591
- Files: cam-topleft.h5, cam-topright.h5, cam-bottomleft.h5, cam-bottomright.h5

## Model Details

Each camera model:
- **Network Type**: resnet_50
- **Engine**: pytorch
- **Keypoints**: 11 keypoints (labeled '1' through '11')
- **Training Fraction**: 0.95

## Usage

### To restore a specific camera model:
```bash
# Example: restore cam-topleft model
cp -r cam-topleft/ monkey_behavior_cheese3d/models/dlc/
```

### To restore all models:
```bash
cp -r cam-*/ monkey_behavior_cheese3d/models/dlc/
```

### To restore predictions:
```bash
cp -r predictions/ monkey_behavior_cheese3d/
```

## Notes

- These are camera-specific models (one model per camera view)
- Each model was trained on data from its specific camera angle
- This approach uses separate models for each view, as opposed to a unified model
- Total backup size: varies by model
