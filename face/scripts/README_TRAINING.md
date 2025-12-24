# SLEAP Model Training Workflow

This guide explains how to train SLEAP models with 20/40/60/80 labeled frames for each of the 4 camera angles.

## Quick Reference Table

| Task | Command |
|------|---------|
| **Train all 4 cameras** | `cd face/scripts && python train_sleap_models.py --session <SESSION> --frames 20` |
| **Train one camera** | `cd face/scripts && python train_sleap_models.py --session <SESSION> --camera <CAMERA> --frames 20` |
| **Check if training running** | `ps aux \| grep train_sleap_models.py` |
| **View training progress** | `tail -f face/models/n20/<camera>/<run>/training_log.csv` |
| **Check latest epoch** | `tail -1 face/models/n20/<camera>/<run>/training_log.csv \| awk -F',' '{print \$1, \$13, \$26}'` |
| **Verify model exists** | `ls -lh face/models/n20/<camera>/<run>/best_model.h5` |
| **List all trained models** | `find face/models/n20 -name "best_model.h5"` |

**Available cameras:** `cam-topright`, `cam-topleft`, `cam-bottomright`, `cam-bottomleft`  
**Available frame counts:** `20`, `40`, `60`, `80`

## Quick Start: How to Train Models

### Prerequisites

1. **Label files organized**: Your label files should be in the session folder structure:
   ```
   face/labels/<session_name>/<camera>/<camera>.slp
   ```

2. **Video files available**: Videos should be in:
   ```
   Face Video/<session_name>/<camera>.mp4
   ```

3. **SLEAP environment**: Make sure you're using the correct Python environment with SLEAP installed.

### Step 1: Navigate to Scripts Directory

```bash
cd face/scripts
```

### Step 2: Start Training

**Option A: Train All 4 Cameras at Once**

```bash
python train_sleap_models.py --session <SESSION_NAME> --frames 20
```

**Example:**
```bash
python train_sleap_models.py --session 2025-05-28_14-12-04_124591 --frames 20
```

This will train all 4 cameras sequentially:
- cam-topright
- cam-topleft
- cam-bottomright
- cam-bottomleft

**Option B: Train a Specific Camera**

```bash
python train_sleap_models.py --session <SESSION_NAME> --camera <CAMERA_NAME> --frames 20
```

**Example:**
```bash
python train_sleap_models.py --session 2025-05-28_14-12-04_124591 --camera cam-topright --frames 20
```

**Available cameras:** `cam-topright`, `cam-topleft`, `cam-bottomright`, `cam-bottomleft`

**Available frame counts:** `20`, `40`, `60`, `80`

### Step 3: Monitor Training Progress

**Check if training is running:**
```bash
ps aux | grep train_sleap_models.py
```

**View training progress:**
```bash
# For a specific camera
tail -f face/models/n20/<camera>/<run_name>/training_log.csv

# Example for cam-topright
tail -f face/models/n20/cam-topright/cam-topright_n20/training_log.csv
```

**Check latest epoch:**
```bash
tail -1 face/models/n20/<camera>/<run_name>/training_log.csv | awk -F',' '{printf "Epoch %s | Training Loss: %.6f | Validation Loss: %.6f\n", $1, $13, $26}'
```

### Step 4: Training Completion

When training completes, you'll find:
- `best_model.h5` - The trained model (saved automatically)
- `training_config.json` - Configuration used for training
- `training_log.csv` - Complete training history

**Location:** `face/models/n20/<camera>/<run_name>/`

### Training Time Estimates

- **Per model:** 15-60 minutes (depending on hardware)
- **All 4 models:** 1-4 hours total
- Training can be stopped early (Ctrl+C) - the best model is saved automatically

### What Happens During Training

1. **Setup Phase** (1-2 minutes):
   - Loads label files
   - Creates train/validation splits (80/20)
   - Sets up model architecture (UNet with centered_instance head)
   - Downloads pretrained weights if needed

2. **Training Phase** (15-60 minutes):
   - Trains for up to 100 epochs
   - Automatically saves best model (lowest validation loss)
   - Early stopping if validation loss doesn't improve for 10 epochs
   - Learning rate reduction on plateau

3. **Completion**:
   - Best model saved as `best_model.h5`
   - Training log saved as `training_log.csv`
   - Configuration saved as `training_config.json`

### Complete Training Workflow Example

**Step-by-step example for training all 4 cameras:**

```bash
# 1. Navigate to scripts directory
cd /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/scripts

# 2. Verify label files exist
ls ../labels/2025-05-28_14-12-04_124591/*/*.slp

# 3. Start training all 4 cameras
python train_sleap_models.py --session 2025-05-28_14-12-04_124591 --frames 20

# 4. Monitor progress (in another terminal)
watch -n 5 'tail -1 ../models/n20/*/training_log.csv | awk -F"," "{print \$1, \$13, \$26}"'

# 5. Check when training completes
ls -lh ../models/n20/*/best_model.h5
```

**Expected output when training starts:**
```
############################################################
Processing cam-topright
############################################################

Created .../cam-topright.n20.slp from base labels

============================================================
Training cam-topright model with 20 labeled frames
Video: .../cam-topright.mp4
Labels: .../cam-topright.n20.slp
Model output: .../models/n20/cam-topright
============================================================

Running training with SLEAP Python API...
Creating training configuration...
Starting training...
INFO:sleap.nn.training:Loading training labels...
INFO:sleap.nn.training:Creating training and validation splits...
INFO:sleap.nn.training:  Splits: Training = 16 / Validation = 4.
INFO:sleap.nn.training:Setting up for training...
...
```

## Overview

The training workflow uses incremental labeling:
- **n20 model**: Uses 20 labeled frames
- **n40 model**: Uses the 20 frames from n20 + 20 more = 40 total
- **n60 model**: Uses the 40 frames from n40 + 20 more = 60 total  
- **n80 model**: Uses the 60 frames from n60 + 20 more = 80 total

## Directory Structure

```
face/
├── labels/
│   └── <session_name>/
│       ├── cam-bottomleft/
│       │   ├── cam-bottomleft.slp (base labels)
│       │   ├── cam-bottomleft.n20.slp
│       │   ├── cam-bottomleft.n40.slp
│       │   ├── cam-bottomleft.n60.slp
│       │   └── cam-bottomleft.n80.slp
│       ├── cam-bottomright/
│       ├── cam-topleft/
│       └── cam-topright/
├── models/
│   ├── n20/
│   │   ├── cam-bottomleft/
│   │   ├── cam-bottomright/
│   │   ├── cam-topleft/
│   │   └── cam-topright/
│   ├── n40/
│   ├── n60/
│   └── n80/
└── scripts/
    ├── open_sleap_for_labeling.sh
    └── train_sleap_models.py
```

## Step-by-Step Workflow

### Step 1: Open SLEAP for Initial Labeling

Open SLEAP with the videos from your session:

```bash
cd face/scripts
chmod +x open_sleap_for_labeling.sh
./open_sleap_for_labeling.sh "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-10-08_894597"
```

Or manually:
```bash
cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-10-08_894597"
mv ~/.sleap/1.4.1/preferences.yaml ~/.sleap/1.4.1/preferences.yaml.bak
/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label \
    cam-bottomleft.mp4 \
    cam-bottomright.mp4 \
    cam-topleft.mp4 \
    cam-topright.mp4
```

### Step 2: Label 20 Frames for Each Camera

For each camera angle:
1. Label 20 frames (distributed across the video)
2. Save the project as: `face/labels/<session_name>/<camera>/<camera>.slp`

Example for cam-bottomleft:
- Save to: `face/labels/2025-05-28_14-10-08_894597/cam-bottomleft/cam-bottomleft.slp`

### Step 3: Prepare n20 Labels

The training script will automatically create n20 label files from your base labels:

```bash
cd face/scripts
python train_sleap_models.py \
    --session 2025-05-28_14-10-08_894597 \
    --camera cam-bottomleft \
    --frames 20 \
    --prepare-only
```

This creates: `face/labels/<session>/<camera>/<camera>.n20.slp`

### Step 4: Train n20 Model

```bash
python train_sleap_models.py \
    --session 2025-05-28_14-10-08_894597 \
    --camera cam-bottomleft \
    --frames 20
```

### Step 5: Add 20 More Frames for n40

1. Open the n20 label file in SLEAP:
```bash
PATH="/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin:$PATH" \
"/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label" \
"/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-10-08_894597/cam-bottomleft/cam-bottomleft.n20.slp"
```

2. Add 20 more labeled frames (total should be 40)
3. Save the project (it will update the .n20.slp file)
4. Copy/rename it to .n40.slp:
```bash
cp face/labels/2025-05-28_14-10-08_894597/cam-bottomleft/cam-bottomleft.n20.slp \
   face/labels/2025-05-28_14-10-08_894597/cam-bottomleft/cam-bottomleft.n40.slp
```

### Step 6: Train n40 Model

```bash
python train_sleap_models.py \
    --session 2025-05-28_14-10-08_894597 \
    --camera cam-bottomleft \
    --frames 40
```

### Step 7: Repeat for n60 and n80

Follow the same pattern:
1. Open previous label file in SLEAP
2. Add 20 more frames
3. Save and copy to next level
4. Train model

### Step 8: Train All Cameras and All Frame Counts

To train everything at once:

```bash
python train_sleap_models.py \
    --session 2025-05-28_14-10-08_894597
```

This will train all 4 cameras with all 4 frame counts (20, 40, 60, 80).

## Tips

1. **Label Distribution**: Try to label frames distributed across the video, not just the beginning
2. **Quality over Quantity**: Make sure labels are accurate - bad labels will hurt model performance
3. **Incremental Approach**: Each model builds on the previous one, so accuracy matters at each step
4. **Save Frequently**: Save your SLEAP projects frequently to avoid losing work

## Training Methods

### Method 1: Using the Training Script (Recommended)

The `train_sleap_models.py` script uses SLEAP's Python API to train models programmatically. This is the easiest method for batch training multiple models.

**Train a single model:**
```bash
cd face/scripts
python train_sleap_models.py \
    --session <session_name> \
    --camera <camera_name> \
    --frames 20
```

**Train all cameras for a specific frame count:**
```bash
python train_sleap_models.py \
    --session <session_name> \
    --frames 20
```

**Train all cameras and all frame counts:**
```bash
python train_sleap_models.py \
    --session <session_name>
```

The script automatically:
- Creates the proper label file structure
- Configures training with appropriate hyperparameters
- Saves models to the correct output directories

### Method 2: Using sleap-nn Command Line (SLEAP 1.5+)

**Note:** `sleap-nn` is available in SLEAP 1.5+ (sleap-nn package). For SLEAP 1.4.1, use Method 1 (training script) or Method 3 (sleap-train).

The `sleap-nn` command-line tool uses YAML configuration files and is the modern way to train SLEAP models.

**Step 1: Download Default Training Configurations**

Get the default config files from the sleap-nn repository:

```bash
cd face/scripts

# Download config for centered_instance model (single-animal pose estimation)
curl -L -o baseline.centered_instance.yaml \
  https://raw.githubusercontent.com/talmolab/sleap-nn/refs/heads/main/docs/sample_configs/config_topdown_centered_instance_unet_medium_rf.yaml

# For top-down pipeline, you may also need a centroid model:
curl -L -o baseline.centroid.yaml \
  https://raw.githubusercontent.com/talmolab/sleap-nn/refs/heads/main/docs/sample_configs/config_centroid_unet.yaml
```

**Step 2: Train Using sleap-nn**

Train a centered_instance model (for single-animal pose estimation):

```bash
sleap-nn train \
  --config-name baseline.centered_instance \
  --config-dir . \
  "data_config.train_labels_path=[path/to/labels.slp]" \
  trainer_config.ckpt_dir="models" \
  trainer_config.run_name="model_name" \
  trainer_config.max_epochs=200
```

**Key Parameters:**
- `--config-name`: Name of the config file (without .yaml extension)
- `--config-dir`: Directory containing the config file
- `data_config.train_labels_path`: Path to your label file (in brackets for list)
- `trainer_config.ckpt_dir`: Directory to save trained models
- `trainer_config.run_name`: Name for this training run
- `trainer_config.max_epochs`: Maximum number of training epochs

**Example for our workflow:**

```bash
cd face/scripts

# Train cam-topright model
sleap-nn train \
  --config-name baseline.centered_instance \
  --config-dir . \
  "data_config.train_labels_path=[../labels/2025-05-28_14-12-04_124591/cam-topright/cam-topright.n20.slp]" \
  trainer_config.ckpt_dir="../models/n20/cam-topright" \
  trainer_config.run_name="cam-topright_n20" \
  trainer_config.max_epochs=100
```

**Training Tips:**
- Monitor validation loss during training
- You can stop training early (Ctrl+C) when validation loss plateaus
- The best model (lowest validation loss) is automatically saved as `best.ckpt`
- Training will stop early if validation loss doesn't improve (controlled by `early_stopping` in config)

### Method 3: Using SLEAP Legacy Command Line (sleap-train)

For older SLEAP versions (1.4.x), you can use `sleap-train` with JSON profiles.

**Step 1: Create a Training Profile**

Option A - Using SLEAP GUI:
1. Open your label file in SLEAP: `sleap-label path/to/labels.slp`
2. Go to "Predict" → "Run Training..."
3. Configure training parameters (model type, epochs, batch size, etc.)
4. Click "Save configuration files..." to export the profile JSON

Option B - Using Python API:
```python
from sleap.nn.config import TrainingJobConfig, ModelConfig, DataConfig, OptimizationConfig, OutputsConfig, LabelsConfig, HeadsConfig, CenteredInstanceConfmapsHeadConfig, BackboneConfig, ResNetConfig

config = TrainingJobConfig(
    data=DataConfig(
        labels=LabelsConfig(
            training_labels="path/to/labels.slp",
            validation_fraction=0.2,
        ),
    ),
    model=ModelConfig(
        backbone=BackboneConfig(resnet=ResNetConfig(version="ResNet50")),
        heads=HeadsConfig(centered_instance=CenteredInstanceConfmapsHeadConfig()),
    ),
    optimization=OptimizationConfig(
        initial_learning_rate=1e-3,
        epochs=100,
        batch_size=4,
    ),
    outputs=OutputsConfig(
        save_outputs=True,
        runs_folder="path/to/output",
        run_name="model_name",
    ),
)

# Save the config
config.save_json("training_profile.json")
```

**Step 2: Train Using sleap-train**

```bash
sleap-train path/to/training_profile.json path/to/labels.slp
```

Or if the labels path is already in the profile:
```bash
sleap-train path/to/training_profile.json
```

### Method 4: Using SLEAP Python API Directly

You can also train models directly using Python:

```python
from sleap.nn.training import Trainer
from sleap.nn.config import TrainingJobConfig

# Load or create config
config = TrainingJobConfig.load_json("training_profile.json")
# Or create programmatically as shown in Method 2

# Create trainer and train
trainer = Trainer.from_config(config)
trainer.train()
```

### Training Configuration Details

**Model Types:**
- `centered_instance`: For single-animal pose estimation (used in this workflow)
- `topdown`: For multi-animal tracking with instance detection
- `bottomup`: For multi-animal tracking without instance detection

**Backbone Options:**
- `ResNet50`, `ResNet101`, `ResNet152`: ResNet architectures
- `unet`: U-Net architecture
- `hourglass`: Hourglass network

**Key Hyperparameters:**
- `epochs`: Number of training epochs (default: 100)
- `batch_size`: Batch size for training (default: 4)
- `initial_learning_rate`: Starting learning rate (default: 1e-3)
- `validation_fraction`: Fraction of data for validation (default: 0.2)

## Troubleshooting

### Before Starting Training

**Issue: "Label file not found"**
```bash
# Check if label files exist
ls face/labels/<SESSION_NAME>/*/*.slp

# If missing, make sure you've saved labels from SLEAP:
# face/labels/<SESSION_NAME>/<camera>/<camera>.slp
```

**Issue: "Video file not found"**
```bash
# Check if video files exist
ls "Face Video/<SESSION_NAME>"/*.mp4

# Verify the session name matches exactly (case-sensitive)
```

**Issue: "Wrong Python environment"**
```bash
# Make sure you're using the SLEAP environment
which python
# Should point to: /Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/python

# Or activate the environment first
conda activate sleap-141-qt5
```

### During Training

**Issue: "Not enough frames"**
- The script will warn if a label file doesn't have enough frames
- Open the label file in SLEAP and add more frames
- Minimum recommended: 20 frames for n20 training

**Issue: "Training fails immediately"**
```bash
# Check that the video file exists and is readable
ls -lh "Face Video/<SESSION_NAME>"/*.mp4

# Ensure SLEAP is properly installed
python -c "import sleap; print(sleap.__version__)"

# Check disk space for model outputs
df -h face/models/
```

**Issue: "Out of memory"**
- Reduce batch size in `train_sleap_models.py` (change `batch_size=4` to `batch_size=2`)
- Close other applications using GPU/memory
- Use CPU-only training if GPU memory is limited

**Issue: "Training hangs or is very slow"**
- Check if GPU is being used: `nvidia-smi` (for NVIDIA) or Activity Monitor (for Mac)
- Verify data loading isn't the bottleneck (check CPU usage)
- Consider reducing image resolution in the config

### After Training

**Issue: "Model file not found"**
```bash
# Check if training actually completed
ls -lh face/models/n20/<camera>/*/best_model.h5

# Check training log for errors
tail -20 face/models/n20/<camera>/*/training_log.csv

# Verify training didn't crash
ps aux | grep train_sleap_models.py
```

**Issue: "Training stopped early"**
- This is normal! Early stopping saves the best model automatically
- Check the training log to see final epoch and loss
- The `best_model.h5` file contains the best model (lowest validation loss)

### Common Error Messages

**"FileNotFoundError: Could not find training profile"**
- You're using the wrong training method
- Use the Python script: `python train_sleap_models.py` instead of `sleap-train`

**"ImportError: cannot import name 'OptimizerConfig'"**
- Wrong SLEAP version or incorrect import
- Should be `OptimizationConfig` (not `OptimizerConfig`)
- Make sure you're using SLEAP 1.4.1

**"ValueError: Could not find a feature activation for output at stride 1"**
- Backbone/head mismatch
- For `CenteredInstanceConfmapsHead`, use UNet backbone (not ResNet)
- This is already configured correctly in the training script

**"TypeError: __init__() got an unexpected keyword argument"**
- SLEAP API parameter names may have changed
- Check the training script for correct parameter names
- Refer to SLEAP documentation for your version

### Getting Help

1. **Check training logs:**
   ```bash
   cat face/models/n20/<camera>/*/training_log.csv
   ```

2. **Verify SLEAP installation:**
   ```bash
   python -c "import sleap; print(sleap.__version__)"
   ```

3. **Test with a single camera first:**
   ```bash
   python train_sleap_models.py --session <SESSION> --camera cam-topright --frames 20
   ```

4. **Check SLEAP documentation:**
   - GitHub: https://github.com/talmolab/sleap
   - Documentation: https://sleap.ai/

## Quick Reference: Training Commands

**Most common use case - Train all 4 cameras:**
```bash
cd face/scripts
python train_sleap_models.py --session 2025-05-28_14-12-04_124591 --frames 20
```

**Train one camera:**
```bash
cd face/scripts
python train_sleap_models.py --session 2025-05-28_14-12-04_124591 --camera cam-topright --frames 20
```

**Check training status:**
```bash
# See if process is running
ps aux | grep train_sleap_models.py

# Check latest progress for a camera
tail -1 face/models/n20/cam-topright/cam-topright_n20/training_log.csv | \
  awk -F',' '{printf "Epoch %s | Loss: %.6f | Val: %.6f\n", $1, $13, $26}'
```

**Verify models are complete:**
```bash
# List all trained models
find face/models/n20 -name "best_model.h5" -exec ls -lh {} \;
```

## Top-Down Pipeline (Two Models)

If you're using the **top-down tracking pipeline** (for multi-animal or instance detection), you need to train **two models** per camera:

1. **Centroid Model**: Detects instance locations
2. **Centered Instance Model**: Predicts poses for each detected instance

**Current Training Script:** The `train_sleap_models.py` script currently trains only the **centered_instance** model. For top-down tracking, you'll also need centroid models.

**Inference with Top-Down Pipeline:**
```bash
sleap-track video.mp4 \
  -m "path/to/centroid_model/training_config.json" \
  -m "path/to/centered_instance_model/training_config.json" \
  --cpu --batch_size 4 \
  -o output.predictions.slp
```

**Note:** For single-animal tracking, you may only need the centered_instance model. The current training script is configured for this use case.

## References

- SLEAP GitHub: https://github.com/talmolab/sleap
- SLEAP Documentation: https://sleap.ai
- Creating Custom Training Profiles: https://docs.sleap.ai/latest/guides/creating-a-custom-training-profile/
- Command Line Interfaces: https://sleap.ai/develop/guides/cli.html
- sleap-nn Repository: https://github.com/talmolab/sleap-nn


