#!/usr/bin/env python3
"""
Run DLC PyTorch model inference on all videos.
This script directly loads PyTorch models and runs inference.
"""

import os
import sys
import yaml
import torch
import numpy as np
import cv2
import h5py
from pathlib import Path
from tqdm import tqdm

# Try to import DLC's PyTorch utilities
try:
    from deeplabcut.pose_estimation_tensorflow import predict_videos
    import deeplabcut
except ImportError:
    print("ERROR: DeepLabCut not available")
    sys.exit(1)

BASE_DIR = Path("/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main")
MODELS_DIR = BASE_DIR / "backup_four_camera_models_20260108_212859"
VIDEOS_DIR = BASE_DIR / "Face Video"
RESULTS_DIR = BASE_DIR / "dlc_inference_results"

CAMERAS = ["cam-bottomleft", "cam-bottomright", "cam-topleft", "cam-topright"]

def get_model_path(camera_name):
    """Get the path to the best model snapshot for a camera."""
    model_base = MODELS_DIR / camera_name / "dlc-models-pytorch" / "iteration-0"
    model_name = f"{camera_name}2026-01-01-trainset95shuffle1"
    model_path = model_base / model_name / "train" / "snapshot-best-010.pt"
    
    if not model_path.exists():
        model_path = model_base / model_name / "train" / "snapshot-200.pt"
    
    return model_path

def get_pytorch_config_path(camera_name):
    """Get the path to the pytorch_config.yaml."""
    model_base = MODELS_DIR / camera_name / "dlc-models-pytorch" / "iteration-0"
    model_name = f"{camera_name}2026-01-01-trainset95shuffle1"
    return model_base / model_name / "train" / "pytorch_config.yaml"

def run_inference_pytorch_direct(video_path, model_path, pytorch_config_path, output_path, camera_name):
    """
    Run inference using PyTorch model directly.
    This is a simplified version - for full functionality, we'd need to load
    the DLC PyTorch model architecture and run inference properly.
    """
    print(f"    Note: Direct PyTorch inference not fully implemented.")
    print(f"    Attempting to use DLC's analyze_videos with proper setup...")
    
    # For now, let's try using DLC's function but with a workaround
    # We'll create a temporary config that points to the right structure
    return None

def run_inference_for_session(session_folder):
    """Run inference on all camera videos in a session folder."""
    session_name = session_folder.name
    print(f"\n{'='*60}")
    print(f"Processing session: {session_name}")
    print(f"{'='*60}")
    
    session_results_dir = RESULTS_DIR / session_name
    session_results_dir.mkdir(parents=True, exist_ok=True)
    
    for camera in CAMERAS:
        video_file = session_folder / f"{camera}.mp4"
        
        if not video_file.exists():
            print(f"  ⚠️  Video not found: {video_file}")
            continue
        
        print(f"\n  Processing {camera}...")
        
        model_path = get_model_path(camera)
        config_path = MODELS_DIR / camera / "config.yaml"
        
        if not model_path.exists() or not config_path.exists():
            print(f"    ❌ Model or config not found")
            continue
        
        try:
            # Update config
            with open(config_path, 'r') as f:
                cfg = yaml.safe_load(f)
            
            cfg['project_path'] = str(MODELS_DIR / camera)
            cfg['engine'] = 'pytorch'
            if 'video_sets' in cfg:
                cfg['video_sets'] = {}
            
            temp_config = MODELS_DIR / camera / "config_inference.yaml"
            with open(temp_config, 'w') as f:
                yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
            
            # Try using DLC - it might work if we have the right structure
            # Create symlink if needed
            dlc_models_train = MODELS_DIR / camera / "dlc-models" / "iteration-0" / f"{camera}2026-01-01-trainset95shuffle1" / "train"
            pytorch_train = MODELS_DIR / camera / "dlc-models-pytorch" / "iteration-0" / f"{camera}2026-01-01-trainset95shuffle1" / "train"
            
            if not dlc_models_train.exists():
                dlc_models_train.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(str(pytorch_train), str(dlc_models_train))
            
            print(f"    Running inference...")
            deeplabcut.analyze_videos(
                str(temp_config),
                [str(video_file)],
                videotype='.mp4',
                shuffle=1,
                trainingsetindex=0,
                gputouse=None,
                save_as_csv=True,
                destfolder=str(session_results_dir),
            )
            
            # Check outputs
            outputs = list(session_results_dir.glob(f"{camera}*"))
            if outputs:
                print(f"    ✅ Completed: {[f.name for f in outputs]}")
            else:
                print(f"    ⚠️  No output files found")
            
            # Cleanup
            if temp_config.exists():
                temp_config.unlink()
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            continue

def main():
    """Main function."""
    print("DLC PyTorch Inference Script")
    print("=" * 60)
    
    if not MODELS_DIR.exists() or not VIDEOS_DIR.exists():
        print("ERROR: Models or videos directory not found")
        sys.exit(1)
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    session_folders = [f for f in VIDEOS_DIR.iterdir() if f.is_dir() and not f.name.startswith('.')]
    session_folders.sort()
    
    print(f"Found {len(session_folders)} sessions")
    
    for session_folder in session_folders:
        run_inference_for_session(session_folder)
    
    print(f"\n{'='*60}")
    print("Processing complete!")
    print(f"Results in: {RESULTS_DIR}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
