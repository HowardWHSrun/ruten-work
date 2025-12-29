# How to Open SLEAP for Labeling

This guide explains how to open SLEAP with different cameras and label files for your workflow.

## Prerequisites

- SLEAP is installed in: `/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin`
- Current session: `2025-05-28_14-12-04_124591`
- Video location: `/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591/`
- Labels location: `/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/`

## Quick Reference

### Open All 4 Cameras (No Labels)
```bash
cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label cam-bottomleft.mp4 cam-bottomright.mp4 cam-topleft.mp4 cam-topright.mp4
```

### Open Single Camera with n20 Labels

#### Bottom Left
```bash
cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-bottomleft/cam-bottomleft.n20.slp"
```

#### Bottom Right
```bash
cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-bottomright/cam-bottomright.n20.slp"
```

#### Top Left
```bash
cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-topleft/cam-topleft.n20.slp"
```

#### Top Right
```bash
cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
/Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-topright/cam-topright.n20.slp"
```

## Using Scripts

### Script 1: Open All Cameras (No Labels)
```bash
bash /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/scripts/open_sleap_for_labeling.sh "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
```

### Script 2: Open Bottom Right with n20 Labels (for n40 labeling)
```bash
bash /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/scripts/open_bottomright_n40.sh
```

## Workflow: Labeling n40 Based on n20

1. **Open SLEAP with n20 labels** (choose the camera you want to work on):
   ```bash
   # For bottom right:
   cd "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"
   /Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-bottomright/cam-bottomright.n20.slp"
   ```

2. **Add more nodes** in SLEAP for n40

3. **Save the project** as `.n40.slp`:
   - Go to `File > Save Project As...`
   - Save to: `/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-bottomright/cam-bottomright.n40.slp`
   - (Replace `cam-bottomright` with the camera you're working on)

## Available Label Files

For session `2025-05-28_14-12-04_124591`, the following label files exist:

- `cam-bottomleft/cam-bottomleft.n20.slp` - Bottom left with n20 nodes
- `cam-bottomleft/cam-bottomleft.slp` - Bottom left original
- `cam-bottomright/cam-bottomright.n20.slp` - Bottom right with n20 nodes
- `cam-bottomright/cam-bottomright.slp` - Bottom right original
- `cam-topleft/cam-topleft.n20.slp` - Top left with n20 nodes
- `cam-topleft/cam-topleft.slp` - Top left original
- `cam-topright/cam-topright.n20.slp` - Top right with n20 nodes
- `cam-topright/cam-topright.slp` - Top right original

## Tips

- **Opening a `.slp` file directly** will load both the video and the labels automatically
- **Opening video files directly** will open them without labels (you can load labels manually via `File > Open Project`)
- If SLEAP doesn't open, check the terminal for error messages
- Make sure no other SLEAP instances are running (they might block new instances)

## Troubleshooting

### SLEAP won't open
1. Check if SLEAP is already running: `ps aux | grep sleap-label`
2. Kill existing processes: `pkill -f "sleap-label"`
3. Try opening again

### Can't find files
- Verify the session folder exists: `ls "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face Video/2025-05-28_14-12-04_124591"`
- Verify label files exist: `ls "/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/face/labels/2025-05-28_14-12-04_124591/cam-bottomright/"`

### Opening in new Terminal window (macOS)
If you want to open SLEAP in a new Terminal window:
```bash
osascript -e 'tell application "Terminal" to do script "cd /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/Face\\ Video/2025-05-28_14-12-04_124591 && /Users/howardwang/miniconda3/envs/sleap-141-qt5/bin/sleap-label cam-bottomright.mp4"'
```
