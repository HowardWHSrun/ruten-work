#!/bin/bash
# Open SLEAP with bottom right camera video and n20 labels for n40 labeling

SESSION_DIR="/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
LABEL_FILE="/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-bottomright/cam-bottomright.n20.slp"
SLEAP_BIN="/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin"

echo "Opening SLEAP with bottom right camera..."
echo "Video: $SESSION_DIR/cam-bottomright.mp4"
echo "Labels: $LABEL_FILE"
echo ""

cd "$SESSION_DIR"
"$SLEAP_BIN/sleap-label" "$LABEL_FILE"
