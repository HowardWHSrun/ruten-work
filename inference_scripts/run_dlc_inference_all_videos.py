#!/usr/bin/env python3
"""
Run DLC inference on all videos in Face Video directory using the four camera models.
Each video folder will have inference results saved in a corresponding results folder.

REQUIREMENTS:
- DeepLabCut must be installed and working
- If you get protobuf import errors, try:
  1. Fix protobuf: pip install --upgrade protobuf
  2. Or use a conda environment with DLC properly installed
  3. Or activate the appropriate conda environment before running

USAGE:
    python3 run_dlc_inference_all_videos.py
"""

import os
import sys
import yaml
import shutil
from pathlib import Path

try:
    import deeplabcut
except ImportError as e:
    print("ERROR: DeepLabCut is not available or has dependency issues.")
    print(f"Error: {e}")
    print("\nTo fix:")
    print("1. Install/upgrade protobuf: pip install --upgrade protobuf")
    print("2. Or use a conda environment with DLC properly installed")
    print("3. Check DLC installation: python -c 'import deeplabcut; print(deeplabcut.__version__)'")
    sys.exit(1)

# Base paths
BASE_DIR = Path("/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main")
MODELS_DIR = BASE_DIR / "backup_four_camera_models_20260108_212859"
VIDEOS_DIR = BASE_DIR / "Face Video"
RESULTS_DIR = BASE_DIR / "dlc_inference_results"

# Camera names
CAMERAS = ["cam-bottomleft", "cam-bottomright", "cam-topleft", "cam-topright"]

def get_model_path(camera_name):
    """Get the path to the best model snapshot for a camera."""
    model_base = MODELS_DIR / camera_name / "dlc-models-pytorch" / "iteration-0"
    model_name = f"{camera_name}2026-01-01-trainset95shuffle1"
    model_path = model_base / model_name / "train" / "snapshot-best-010.pt"
    
    if not model_path.exists():
        # Try snapshot-200.pt as fallback
        model_path = model_base / model_name / "train" / "snapshot-200.pt"
    
    return model_path

def get_config_path(camera_name):
    """Get the path to the config.yaml for a camera."""
    config_path = MODELS_DIR / camera_name / "config.yaml"
    return config_path

def get_pytorch_config_path(camera_name):
    """Get the path to the pytorch_config.yaml for a camera."""
    model_base = MODELS_DIR / camera_name / "dlc-models-pytorch" / "iteration-0"
    model_name = f"{camera_name}2026-01-01-trainset95shuffle1"
    pytorch_config = model_base / model_name / "train" / "pytorch_config.yaml"
    return pytorch_config

def update_config_for_inference(config_path, camera_name):
    """Update config.yaml to point to the correct model paths in backup directory."""
    # Read the config
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    
    # Update project_path to point to backup directory
    new_project_path = str(MODELS_DIR / camera_name)
    cfg['project_path'] = new_project_path
    
    # Update video_sets if it exists (remove old paths)
    if 'video_sets' in cfg:
        cfg['video_sets'] = {}
    
    # For PyTorch models, we need to ensure the engine is set correctly
    cfg['engine'] = 'pytorch'
    
    # Write updated config to a temporary location
    temp_config_path = MODELS_DIR / camera_name / "config_temp.yaml"
    with open(temp_config_path, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
    
    return temp_config_path

def update_pytorch_config_for_inference(pytorch_config_path, camera_name):
    """Update pytorch_config.yaml to point to the correct paths."""
    # Read the pytorch config
    with open(pytorch_config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    
    # Update metadata paths
    if 'metadata' in cfg:
        new_project_path = str(MODELS_DIR / camera_name)
        cfg['metadata']['project_path'] = new_project_path
        cfg['metadata']['pose_config_path'] = str(pytorch_config_path)
    
    # Write updated config to a temporary location
    temp_config_path = MODELS_DIR / camera_name / "pytorch_config_temp.yaml"
    with open(temp_config_path, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
    
    return temp_config_path

def run_inference_for_session(session_folder):
    """Run inference on all camera videos in a session folder."""
    session_name = session_folder.name
    print(f"\n{'='*60}")
    print(f"Processing session: {session_name}")
    print(f"{'='*60}")
    
    # Create results folder for this session
    session_results_dir = RESULTS_DIR / session_name
    session_results_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each camera
    for camera in CAMERAS:
        video_file = session_folder / f"{camera}.mp4"
        
        if not video_file.exists():
            print(f"  ⚠️  Video not found: {video_file}")
            continue
        
        print(f"\n  Processing {camera}...")
        print(f"    Video: {video_file}")
        
        # Get model and config paths
        model_path = get_model_path(camera)
        config_path = get_config_path(camera)
        
        if not model_path.exists():
            print(f"    ❌ Model not found: {model_path}")
            continue
        
        if not config_path.exists():
            print(f"    ❌ Config not found: {config_path}")
            continue
        
        print(f"    Model: {model_path}")
        print(f"    Config: {config_path}")
        
        try:
            # For PyTorch models, we need to use the pytorch_config.yaml
            pytorch_config_path = get_pytorch_config_path(camera)
            
            if not pytorch_config_path.exists():
                print(f"    ⚠️  PyTorch config not found, trying standard config...")
                temp_config = update_config_for_inference(config_path, camera)
                config_to_use = temp_config
            else:
                print(f"    Using PyTorch config: {pytorch_config_path}")
                # Update pytorch config
                temp_config = update_pytorch_config_for_inference(pytorch_config_path, camera)
                config_to_use = temp_config
            
            print(f"    Running inference...")
            print(f"    Output will be saved to: {session_results_dir}")
            
            # Try using analyze_videos - DLC 2.2.3 should handle PyTorch models
            # If that doesn't work, we may need to use the PyTorch-specific API
            try:
                deeplabcut.analyze_videos(
                    str(config_to_use),
                    [str(video_file)],
                    videotype='.mp4',
                    shuffle=1,
                    trainingsetindex=0,
                    gputouse=None,
                    save_as_csv=True,
                    destfolder=str(session_results_dir),
                    modelprefix='',
                    robust_nframes=False,
                    allow_growth=False,
                    use_shelve=False,
                )
            except Exception as e:
                # If standard analyze_videos doesn't work, try with the model path directly
                print(f"    ⚠️  Standard analyze_videos failed: {e}")
                print(f"    Trying alternative approach with model path...")
                # Update config to explicitly point to the model
                raise e
            
            # Check for output files
            h5_files = list(session_results_dir.glob(f"{camera}*.h5"))
            csv_files = list(session_results_dir.glob(f"{camera}*.csv"))
            
            if h5_files:
                print(f"    ✅ Inference completed: {h5_files[0].name}")
            elif csv_files:
                print(f"    ✅ Inference completed: {csv_files[0].name}")
            else:
                # Try to find any output file with camera name
                all_outputs = list(session_results_dir.glob("*"))
                if all_outputs:
                    print(f"    ⚠️  Output files found: {[f.name for f in all_outputs]}")
                else:
                    print(f"    ⚠️  Inference may have completed but output files not found")
            
            # Clean up temp config
            if temp_config.exists():
                temp_config.unlink()
                
        except Exception as e:
            print(f"    ❌ Error during inference: {str(e)}")
            import traceback
            traceback.print_exc()
            continue

def main():
    """Main function to process all video sessions."""
    print("DLC Inference Script for All Videos")
    print("=" * 60)
    print(f"Models directory: {MODELS_DIR}")
    print(f"Videos directory: {VIDEOS_DIR}")
    print(f"Results directory: {RESULTS_DIR}")
    
    # Verify directories exist
    if not MODELS_DIR.exists():
        print(f"❌ Models directory not found: {MODELS_DIR}")
        sys.exit(1)
    
    if not VIDEOS_DIR.exists():
        print(f"❌ Videos directory not found: {VIDEOS_DIR}")
        sys.exit(1)
    
    # Create results directory
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all session folders
    session_folders = [f for f in VIDEOS_DIR.iterdir() if f.is_dir() and not f.name.startswith('.')]
    session_folders.sort()
    
    print(f"\nFound {len(session_folders)} session folders")
    
    # Process each session
    for session_folder in session_folders:
        run_inference_for_session(session_folder)
    
    print(f"\n{'='*60}")
    print("All sessions processed!")
    print(f"Results saved in: {RESULTS_DIR}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
