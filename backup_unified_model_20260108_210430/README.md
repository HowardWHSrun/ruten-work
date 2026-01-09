# Unified Face Model Backup

This folder contains a backup of the trained unified DLC model and related files.

## Backup Date
$(date)

## Contents

### 1. dlc-models/
Contains the trained model weights, snapshots, and checkpoints from training iteration 0.
- Model: unified-face-model-DLC_resnet50-2026-01-01
- Training iterations: 50,000
- Network: ResNet-50

### 2. evaluation-results/
Contains model evaluation results including:
- Test/train error metrics
- Per-keypoint evaluation results
- Snapshot evaluation at iteration 50,000

### 3. training-datasets/
Contains the training datasets used to train the model:
- Unaugmented dataset
- Documentation and metadata

### 4. labeled-data/
Contains the labeled training data from all 4 camera views:
- cam-topleft/
- cam-topright/
- cam-bottomleft/
- cam-bottomright/
- Total: 321 labeled frames

### 5. config.yaml
The DeepLabCut configuration file used for training.

### 6. videos/
Symlinks to the video files used for training (for reference).

## Model Details

- **Task**: unified-face-model
- **Scorer**: DLC_resnet50
- **Date**: 2026-01-01
- **Keypoints**: 11 keypoints (labeled '1' through '11')
- **Training Fraction**: 0.95
- **Network Type**: resnet_50
- **Engine**: pytorch

## Usage

To restore this backup:
1. Copy the contents back to:
   `monkey_behavior_cheese3d_gui/model/unified-face-model/backend/unified-face-model-DLC_resnet50-2026-01-01/`

2. Or use this backup as a reference for creating new models.

## Notes

- The model was trained on data from all 4 camera views (topleft, topright, bottomleft, bottomright)
- This is a unified model that can be used for all camera angles in Cheese3D
- The backup size is approximately 466 MB
