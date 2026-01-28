#!/usr/bin/env python3
"""Setup script to create the dlc-models directory structure that DLC expects for inference."""

import yaml
from pathlib import Path

BASE_DIR = Path("/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main")
MODELS_DIR = BASE_DIR / "backup_four_camera_models_20260108_212859"
CAMERAS = ["cam-bottomleft", "cam-bottomright", "cam-topleft", "cam-topright"]

def setup_camera_model(camera_name):
    """Set up the dlc-models directory structure for a camera."""
    print(f"Setting up {camera_name}...")
    
    # Paths
    pytorch_base = MODELS_DIR / camera_name / "dlc-models-pytorch" / "iteration-0"
    model_name = f"{camera_name}2026-01-01-trainset95shuffle1"
    pytorch_test = pytorch_base / model_name / "test"
    pytorch_train = pytorch_base / model_name / "train"
    
    # Create dlc-models structure (what DLC expects)
    dlc_models_base = MODELS_DIR / camera_name / "dlc-models" / "iteration-0" / model_name
    dlc_models_test = dlc_models_base / "test"
    dlc_models_test.mkdir(parents=True, exist_ok=True)
    
    # Copy and update pose_cfg.yaml
    if pytorch_test.exists() and (pytorch_test / "pose_cfg.yaml").exists():
        with open(pytorch_test / "pose_cfg.yaml", 'r') as f:
            pose_cfg = yaml.safe_load(f)
        
        # Update dataset path
        pose_cfg['dataset'] = str(MODELS_DIR / camera_name)
        
        # Write updated pose_cfg.yaml
        with open(dlc_models_test / "pose_cfg.yaml", 'w') as f:
            yaml.dump(pose_cfg, f, default_flow_style=False, sort_keys=False)
        
        print(f"  ✅ Created {dlc_models_test / 'pose_cfg.yaml'}")
    else:
        print(f"  ⚠️  Source pose_cfg.yaml not found")
    
    # Create symlink to PyTorch train directory
    dlc_models_train = dlc_models_base / "train"
    if not dlc_models_train.exists() and pytorch_train.exists():
        dlc_models_train.parent.mkdir(parents=True, exist_ok=True)
        try:
            dlc_models_train.symlink_to(pytorch_train)
            print(f"  ✅ Created symlink: {dlc_models_train} -> {pytorch_train}")
        except Exception as e:
            print(f"  ⚠️  Could not create symlink: {e}")
    
    print(f"  ✅ Directory structure created for {camera_name}")

def main():
    """Set up all camera models."""
    print("Setting up DLC models for inference...")
    print("=" * 60)
    
    for camera in CAMERAS:
        setup_camera_model(camera)
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
