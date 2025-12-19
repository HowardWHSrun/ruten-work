# Demo Results

This directory contains example output files from each phase of the evaluation pipeline. These demonstrate the structure and format of the results you can expect when running the notebooks.

## Directory Structure

```
demo_results/
├── session_demo/                    # Demo session folder structure
│   └── out_metrics/
│       └── Evaluation_Metrics/
│           ├── metrics_step1/       # Phase 1 Step 1 outputs
│           ├── metrics_step2/       # Phase 1 Step 2 outputs
│           ├── metrics_step3/       # Phase 1 Step 3 outputs
│           ├── metrics_step4/       # Phase 1 Step 4 outputs
│           └── metrics_step5/       # Phase 1 Step 5 outputs
│   └── out_3d_eval/                 # Phase 2 outputs
├── phase3_results/                  # Phase 3 outputs
├── phase4_results/                  # Phase 4 outputs
└── README.md                        # This file
```

## Phase 1 - Per-Camera Tracking QC

### Step 1: Visibility & Continuity Audit
- `detection_coverage.csv` - Per-node coverage metrics for each camera
- `per_frame_node_counts.csv` - Frame-by-frame node detection counts
- `node_list.json` - Canonical node list and FPS

### Step 2: Pixel Accuracy vs Ground Truth
- `pixel_error_summary.csv` - Mean, median, p95 pixel errors and PCK metrics

### Step 3: Temporal Drift Check
- `drift_summary.csv` - Drift slopes and R² values per camera/node

### Step 4: Marker Stability / Jitter Audit
- `jitter_summary.csv` - Frame-to-frame jitter metrics

### Step 5: Inter-Camera Sync / Lag Check
- `sync_lag_matrix.csv` - Timing offsets between camera pairs

## Phase 2 - 3D Reconstruction QC

### Step 1: 3D Track Integrity Audit
- `phase2_step1_coverage_jitter.csv` - 3D coverage, jitter, and dropout metrics

### Step 2: Geometric Consistency / Reprojection Error
- `phase2_step2_reprojection_error.csv` - Reprojection error per camera/joint

## Phase 3 - Visualization and Behavioral Analysis

### Step 1: Normal Vector Stability Analysis
- `normal_vector_stability_analysis.csv` - Frame-by-frame normal vector metrics
- `normal_vector_stability_sec_blocks.csv` - Per-second block analysis

### Step 2: Chewing Sidedness Analysis
- `chewing_sidedness_analysis.csv` - Frame-by-frame sidedness classification

## Phase 4 - Gape & Feeding Evaluation

- `per_session_metrics.csv` - Per-session performance metrics
- `summary_metrics.csv` - Aggregated metrics with 95% confidence intervals

## Notes

These are example/demo files with synthetic data to illustrate the output format. Real results will have:
- More frames (typically thousands)
- More nodes/joints
- More cameras
- Actual tracking data values

Use these files as references for understanding the expected output structure when running the evaluation notebooks.

