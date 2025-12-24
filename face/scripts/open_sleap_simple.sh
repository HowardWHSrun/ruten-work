#!/bin/bash
# Simple script to open SLEAP - run this in your terminal

SESSION_DIR="/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-10-08_894597"
SLEAP_BIN="/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin"

# Kill any existing SLEAP
pkill -f "sleap-label" 2>/dev/null
sleep 1

# Backup preferences
mkdir -p ~/.sleap/1.4.1
mv ~/.sleap/1.4.1/preferences.yaml ~/.sleap/1.4.1/preferences.yaml.bak 2>/dev/null

# Change to video directory
cd "$SESSION_DIR"

echo "Opening SLEAP..."
echo "After it opens, load the video: cam-bottomleft.mp4"
echo ""

# Open SLEAP - this will run in foreground, so keep terminal open
exec "$SLEAP_BIN/sleap-label"




