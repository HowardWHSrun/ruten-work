#!/usr/bin/env python3
"""Test script to run inference on a single video to verify DLC is working."""

import sys
from pathlib import Path
import yaml
import deeplabcut

BASE_DIR = Path("/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main")
MODELS_DIR = BASE_DIR / "backup_four_camera_models_20260108_212859"
VIDEOS_DIR = BASE_DIR / "Face Video"

# Test with first session and first camera
session_folder = VIDEOS_DIR / "2025-05-28_14-10-08_894597"
camera = "cam-bottomleft"
video_file = session_folder / f"{camera}.mp4"
config_path = MODELS_DIR / camera / "config.yaml"

print(f"Testing DLC inference...")
print(f"Video: {video_file}")
print(f"Config: {config_path}")
print(f"Video exists: {video_file.exists()}")
print(f"Config exists: {config_path.exists()}")

if not video_file.exists():
    print(f"ERROR: Video not found: {video_file}")
    sys.exit(1)

if not config_path.exists():
    print(f"ERROR: Config not found: {config_path}")
    sys.exit(1)

# Update config
with open(config_path, 'r') as f:
    cfg = yaml.safe_load(f)

cfg['project_path'] = str(MODELS_DIR / camera)
if 'video_sets' in cfg:
    cfg['video_sets'] = {}

temp_config = MODELS_DIR / camera / "config_test.yaml"
with open(temp_config, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)

print(f"\nRunning inference...")
print(f"Temp config: {temp_config}")

try:
    deeplabcut.analyze_videos(
        str(temp_config),
        [str(video_file)],
        videotype='.mp4',
        shuffle=1,
        trainingsetindex=0,
        gputouse=None,
        save_as_csv=True,
        destfolder=str(session_folder),
        modelprefix='',
        robust_nframes=False,
        allow_growth=False,
        use_shelve=False,
    )
    print("✅ Inference completed successfully!")
    
    # Check for output
    h5_files = list(session_folder.glob(f"{camera}*.h5"))
    csv_files = list(session_folder.glob(f"{camera}*.csv"))
    print(f"H5 files: {h5_files}")
    print(f"CSV files: {csv_files}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if temp_config.exists():
        temp_config.unlink()
