#!/bin/bash
# Quick script to open SLEAP with one video from the session
# Usage: ./open_sleap_now.sh [camera_name]
# Example: ./open_sleap_now.sh cam-bottomleft

SESSION_DIR="/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-10-08_894597"
SLEAP_BIN="/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin"

# Get camera name from argument or default to cam-bottomleft
CAMERA="${1:-cam-bottomleft}"
VIDEO_FILE="$CAMERA.mp4"

# Kill any existing SLEAP processes
pkill -f "sleap-label" 2>/dev/null
sleep 1

# Backup preferences
mkdir -p ~/.sleap/1.4.1
mv ~/.sleap/1.4.1/preferences.yaml ~/.sleap/1.4.1/preferences.yaml.bak 2>/dev/null

# Change to session directory
cd "$SESSION_DIR"

# Check if video exists
if [ ! -f "$VIDEO_FILE" ]; then
    echo "Error: Video file not found: $VIDEO_FILE"
    echo "Available videos:"
    ls -1 *.mp4
    exit 1
fi

echo "Opening SLEAP..."
echo ""
echo "After SLEAP opens:"
echo "  1. Go to File > Open Video"
echo "  2. Navigate to: $SESSION_DIR"
echo "  3. Select: $VIDEO_FILE"
echo ""
echo "Or simply drag and drop the video file into the SLEAP window"
echo ""

# Open SLEAP without arguments - user will load video from GUI
"$SLEAP_BIN/sleap-label"

