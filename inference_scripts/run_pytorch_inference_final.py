#!/usr/bin/env python3
"""
Run DLC PyTorch model inference on all videos using DLC's PyTorch inference API.
This script uses DLC's built-in PyTorch support to run inference.
"""

import os
import sys
import yaml
from pathlib import Path

try:
    import deeplabcut
    # Use PyTorch-specific analyze_videos for DLC 3.0
    from deeplabcut.pose_estimation_pytorch import analyze_videos as pytorch_analyze_videos
except ImportError as e:
    print(f"ERROR: DeepLabCut not available: {e}")
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

def setup_model_structure(camera_name):
    """Set up the directory structure DLC expects for PyTorch models."""
    # DLC expects models in dlc-models/iteration-X/... structure
    # But we have them in dlc-models-pytorch/
    # We'll create symlinks or update configs to point to the right place
    
    pytorch_base = MODELS_DIR / camera_name / "dlc-models-pytorch" / "iteration-0"
    model_name = f"{camera_name}2026-01-01-trainset95shuffle1"
    pytorch_train = pytorch_base / model_name / "train"
    
    # Create dlc-models structure if it doesn't exist
    dlc_base = MODELS_DIR / camera_name / "dlc-models" / "iteration-0" / model_name
    dlc_train = dlc_base / "train"
    dlc_test = dlc_base / "test"
    
    # Create directories
    dlc_test.mkdir(parents=True, exist_ok=True)
    
    # Create symlink to pytorch train directory if it doesn't exist
    if not dlc_train.exists() and pytorch_train.exists():
        try:
            dlc_train.symlink_to(pytorch_train)
        except FileExistsError:
            pass  # Already exists
    
    # Copy/update pose_cfg.yaml in test directory
    pytorch_test = pytorch_base / model_name / "test"
    if pytorch_test.exists() and (pytorch_test / "pose_cfg.yaml").exists():
        with open(pytorch_test / "pose_cfg.yaml", 'r') as f:
            pose_cfg = yaml.safe_load(f)
        
        pose_cfg['dataset'] = str(MODELS_DIR / camera_name)
        
        with open(dlc_test / "pose_cfg.yaml", 'w') as f:
            yaml.dump(pose_cfg, f, default_flow_style=False, sort_keys=False)
    
    return dlc_base

def update_config_for_inference(camera_name):
    """Update config.yaml for inference."""
    config_path = MODELS_DIR / camera_name / "config.yaml"
    
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    
    # Update paths
    cfg['project_path'] = str(MODELS_DIR / camera_name)
    cfg['engine'] = 'pytorch'  # Ensure PyTorch engine is set
    if 'video_sets' in cfg:
        cfg['video_sets'] = {}
    
    # Write updated config
    temp_config = MODELS_DIR / camera_name / "config_inference.yaml"
    with open(temp_config, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
    
    return temp_config

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
            print(f"  ⚠️  Video not found: {video_file.name}")
            continue
        
        print(f"\n  Processing {camera}...")
        print(f"    Video: {video_file.name}")
        
        model_path = get_model_path(camera)
        if not model_path.exists():
            print(f"    ❌ Model not found: {model_path}")
            continue
        
        print(f"    Model: {model_path.name}")
        
        try:
            # Set up model structure
            setup_model_structure(camera)
            
            # Update config
            temp_config = update_config_for_inference(camera)
            
            print(f"    Running inference (this may take a while)...")
            
            # Use DLC 3.0's PyTorch-specific analyze_videos function
            # This is the correct function for PyTorch models
            # Use -1 to get the best snapshot, or None to use config default
            pytorch_analyze_videos(
                str(temp_config),
                str(video_file),  # Can be a single video or list
                videotype='.mp4',
                shuffle=1,
                trainingsetindex=0,
                snapshot_index=-1,  # Use -1 for best snapshot, or None for config default
                device=None,  # Use CPU (or 'cuda' for GPU)
                save_as_csv=True,
                destfolder=str(session_results_dir),
                modelprefix='',
            )
            
            # Check for output files
            h5_files = list(session_results_dir.glob(f"{camera}*.h5"))
            csv_files = list(session_results_dir.glob(f"{camera}*.csv"))
            
            if h5_files:
                print(f"    ✅ Completed: {h5_files[0].name}")
            elif csv_files:
                print(f"    ✅ Completed: {csv_files[0].name}")
            else:
                # Check for any output with camera name
                all_outputs = list(session_results_dir.glob(f"*{camera}*"))
                if all_outputs:
                    print(f"    ✅ Completed: {[f.name for f in all_outputs]}")
                else:
                    print(f"    ⚠️  Inference completed but output files not found")
                    print(f"    Check: {session_results_dir}")
            
            # Cleanup temp config
            if temp_config.exists():
                temp_config.unlink()
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            # Don't print full traceback for cleaner output, but log it
            import traceback
            error_details = traceback.format_exc()
            # Save error to file for debugging
            error_log = RESULTS_DIR / f"error_{session_name}_{camera}.txt"
            with open(error_log, 'w') as f:
                f.write(f"Error processing {camera} in {session_name}\n")
                f.write(f"{str(e)}\n\n")
                f.write(error_details)
            print(f"    Error details saved to: {error_log}")
            continue

def main():
    """Main function."""
    print("DLC PyTorch Inference - Processing All Videos")
    print("=" * 60)
    print(f"Models: {MODELS_DIR}")
    print(f"Videos: {VIDEOS_DIR}")
    print(f"Results: {RESULTS_DIR}")
    print("=" * 60)
    
    if not MODELS_DIR.exists():
        print(f"❌ Models directory not found: {MODELS_DIR}")
        sys.exit(1)
    
    if not VIDEOS_DIR.exists():
        print(f"❌ Videos directory not found: {VIDEOS_DIR}")
        sys.exit(1)
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all session folders
    session_folders = [f for f in VIDEOS_DIR.iterdir() 
                       if f.is_dir() and not f.name.startswith('.')]
    session_folders.sort()
    
    print(f"\nFound {len(session_folders)} video sessions")
    print("Starting inference...\n")
    
    # Process each session
    for session_folder in session_folders:
        run_inference_for_session(session_folder)
    
    print(f"\n{'='*60}")
    print("All sessions processed!")
    print(f"Results saved in: {RESULTS_DIR}")
    print(f"{'='*60}")
    
    # Summary
    total_h5 = len(list(RESULTS_DIR.rglob("*.h5")))
    total_csv = len(list(RESULTS_DIR.rglob("*.csv")))
    print(f"\nSummary:")
    print(f"  H5 files: {total_h5}")
    print(f"  CSV files: {total_csv}")

if __name__ == "__main__":
    main()
