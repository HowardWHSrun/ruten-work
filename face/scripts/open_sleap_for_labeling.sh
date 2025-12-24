#!/bin/bash
# Script to open SLEAP with videos from a session folder for labeling
# Usage: ./open_sleap_for_labeling.sh <session_folder>

SESSION_FOLDER="$1"
SLEAP_BIN="/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin"

if [ -z "$SESSION_FOLDER" ]; then
    echo "Usage: $0 <session_folder>"
    echo "Example: $0 /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face\ Video/2025-05-28_14-10-08_894597"
    exit 1
fi

if [ ! -d "$SESSION_FOLDER" ]; then
    echo "Error: Session folder not found: $SESSION_FOLDER"
    exit 1
fi

# Check if videos exist
VIDEOS=(
    "$SESSION_FOLDER/cam-bottomleft.mp4"
    "$SESSION_FOLDER/cam-bottomright.mp4"
    "$SESSION_FOLDER/cam-topleft.mp4"
    "$SESSION_FOLDER/cam-topright.mp4"
)

MISSING_VIDEOS=()
for video in "${VIDEOS[@]}"; do
    if [ ! -f "$video" ]; then
        MISSING_VIDEOS+=("$video")
    fi
done

if [ ${#MISSING_VIDEOS[@]} -gt 0 ]; then
    echo "Warning: Some videos are missing:"
    for video in "${MISSING_VIDEOS[@]}"; do
        echo "  - $video"
    done
fi

# Backup preferences and open SLEAP
echo "Backing up SLEAP preferences..."
mv ~/.sleap/1.4.1/preferences.yaml ~/.sleap/1.4.1/preferences.yaml.bak 2>/dev/null || true

echo "Opening SLEAP with videos from: $SESSION_FOLDER"
cd "$SESSION_FOLDER"
PATH="$SLEAP_BIN:$PATH" "$SLEAP_BIN/sleap-label" \
    cam-bottomleft.mp4 \
    cam-bottomright.mp4 \
    cam-topleft.mp4 \
    cam-topright.mp4

echo "SLEAP opened. Start labeling!"




