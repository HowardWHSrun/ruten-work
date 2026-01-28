# DLC Inference Script

This script runs DeepLabCut inference on all videos in the `Face Video` directory using the four camera-specific models from `backup_four_camera_models_20260108_212859`.

## Overview

The script:
1. Iterates through all video folders in `Face Video/`
2. For each folder, runs inference on each camera video (cam-bottomleft, cam-bottomright, cam-topleft, cam-topright)
3. Uses the corresponding camera model from `backup_four_camera_models_20260108_212859/`
4. Saves all inference results in `dlc_inference_results/` with folders named after each video session

## Requirements

- DeepLabCut installed and working
- PyYAML installed: `pip install pyyaml`
- Proper Python environment with DLC dependencies

### Fixing Common Issues

**If you get protobuf import errors:**
```bash
pip install --upgrade protobuf
```

**If DLC is not found:**
- Make sure you're in the correct conda environment
- Verify DLC installation: `python -c "import deeplabcut; print(deeplabcut.__version__)"`

## Usage

```bash
cd /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main
python3 run_dlc_inference_all_videos.py
```

## Output Structure

Results will be saved in:
```
dlc_inference_results/
├── 2025-05-28_14-10-08_894597/
│   ├── cam-bottomleft*.h5
│   ├── cam-bottomright*.h5
│   ├── cam-topleft*.h5
│   └── cam-topright*.h5
├── 2025-05-28_14-12-04_124591/
│   └── ...
└── ...
```

Each session folder will contain:
- `.h5` files with pose predictions (one per camera)
- `.csv` files (if `save_as_csv=True`)

## Model Details

The script uses:
- **Model files**: `snapshot-best-010.pt` (or `snapshot-200.pt` as fallback)
- **Config files**: `config.yaml` from each camera model directory
- **Shuffle**: 1 (matching the training configuration)
- **Training set index**: 0

## Processing Order

1. All video folders are processed in alphabetical order
2. For each folder, all 4 cameras are processed sequentially
3. Progress is printed to the console

## Notes

- The script automatically updates config paths to point to the backup model directory
- Temporary config files are created and cleaned up automatically
- If a video file is missing for a camera, the script will skip it and continue
- If a model file is missing, the script will report an error and continue with other cameras
