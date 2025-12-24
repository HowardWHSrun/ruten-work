#!/bin/bash
# Script to train all 4 camera models using sleap-nn
# Usage: ./train_all_models_sleap_nn.sh <session_name> [frame_count]
# Example: ./train_all_models_sleap_nn.sh 2025-05-28_14-12-04_124591 20

SESSION_NAME="$1"
FRAME_COUNT="${2:-20}"  # Default to 20 if not provided

if [ -z "$SESSION_NAME" ]; then
    echo "Usage: $0 <session_name> [frame_count]"
    echo "Example: $0 2025-05-28_14-12-04_124591 20"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
LABELS_DIR="$BASE_DIR/labels"
MODELS_DIR="$BASE_DIR/models"

CAMERAS=("cam-topright" "cam-topleft" "cam-bottomright" "cam-bottomleft")

# Check if config file exists
if [ ! -f "$SCRIPT_DIR/baseline.centered_instance.yaml" ]; then
    echo "Downloading training config..."
    curl -L -o "$SCRIPT_DIR/baseline.centered_instance.yaml" \
      https://raw.githubusercontent.com/talmolab/sleap-nn/refs/heads/main/docs/sample_configs/config_topdown_centered_instance_unet_medium_rf.yaml
fi

echo "Training models for session: $SESSION_NAME"
echo "Frame count: $FRAME_COUNT"
echo "=========================================="

for camera in "${CAMERAS[@]}"; do
    echo ""
    echo "Training $camera..."
    echo "----------------------------------------"
    
    LABEL_FILE="$LABELS_DIR/$SESSION_NAME/$camera/$camera.n${FRAME_COUNT}.slp"
    MODEL_DIR="$MODELS_DIR/n${FRAME_COUNT}/$camera"
    
    # Check if label file exists
    if [ ! -f "$LABEL_FILE" ]; then
        echo "ERROR: Label file not found: $LABEL_FILE"
        echo "Skipping $camera..."
        continue
    fi
    
    # Create model directory
    mkdir -p "$MODEL_DIR"
    
    # Train the model
    cd "$SCRIPT_DIR"
    
    # Try to use sleap-nn if available, otherwise fall back to Python API
    if command -v sleap-nn &> /dev/null; then
        sleap-nn train \
          --config-name baseline.centered_instance \
          --config-dir . \
          "data_config.train_labels_path=[$LABEL_FILE]" \
          trainer_config.ckpt_dir="$MODEL_DIR" \
          trainer_config.run_name="${camera}_n${FRAME_COUNT}" \
          trainer_config.max_epochs=100
    elif [ -f "/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-nn" ]; then
        /Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-nn train \
          --config-name baseline.centered_instance \
          --config-dir . \
          "data_config.train_labels_path=[$LABEL_FILE]" \
          trainer_config.ckpt_dir="$MODEL_DIR" \
          trainer_config.run_name="${camera}_n${FRAME_COUNT}" \
          trainer_config.max_epochs=100
    else
        echo "sleap-nn not found. Using Python training script instead..."
        /Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/python "$SCRIPT_DIR/train_sleap_models.py" \
          --session "$SESSION_NAME" \
          --camera "$camera" \
          --frames "$FRAME_COUNT"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully trained $camera"
    else
        echo "✗ Failed to train $camera"
    fi
done

echo ""
echo "=========================================="
echo "Training complete!"

