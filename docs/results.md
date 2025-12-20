---
layout: default
title: Experimental Results
---

# Experimental Results

This page showcases example results from the evaluation pipeline. These demonstrate the types of metrics and outputs you can expect when running the evaluation notebooks.

---

## Demo Results Overview

We provide demo results for all phases to illustrate the output format and structure. These can be found in the [`demo_results/`](https://github.com/HowardWHSrun/ruten-work/tree/main/demo_results) directory of the repository.

---

## Phase 1 Results - Per-Camera Tracking QC

### Step 1: Detection Coverage

**Example metrics from `detection_coverage.csv`:**

| Camera | Node | Coverage (Raw) | Coverage (Thresholded) | Median Run Length |
|--------|------|----------------|------------------------|-------------------|
| cam_1 | UpperLip_Center | 95% | 92% | 450 frames |
| cam_1 | LowerLip_Center | 98% | 96% | 520 frames |
| cam_2 | UpperLip_Center | 93% | 90% | 420 frames |
| cam_2 | LowerLip_Center | 96% | 94% | 480 frames |

**Interpretation:**
- Coverage > 90% indicates reliable tracking
- Median run length > 400 frames suggests stable, continuous detection
- Lower coverage may indicate occlusion or tracking challenges

### Step 2: Pixel Accuracy

**Example metrics from `pixel_error_summary.csv`:**

| Camera | Node | Mean Error (px) | Median Error (px) | PCK @ 2px | PCK @ 5px |
|--------|------|-----------------|-------------------|-----------|-----------|
| cam_1 | UpperLip_Center | 2.3 | 2.1 | 85% | 95% |
| cam_1 | LowerLip_Center | 1.9 | 1.8 | 92% | 98% |
| cam_2 | UpperLip_Center | 2.5 | 2.3 | 82% | 93% |

**Interpretation:**
- Mean error < 3px is generally acceptable for most applications
- PCK @ 5px > 90% indicates good accuracy
- Lower errors suggest better anatomical alignment

### Step 3: Temporal Drift

**Example metrics from `drift_summary.csv`:**

| Camera | Node | Drift Slope (px/10k frames) | R² | Classification |
|--------|------|----------------------------|----|----------------|
| cam_1 | UpperLip_Center | 0.15 | 0.02 | stable |
| cam_1 | LowerLip_Center | 0.08 | 0.01 | stable |
| cam_2 | UpperLip_Center | 0.18 | 0.02 | stable |

**Interpretation:**
- Slope < 0.5 px/10k frames indicates minimal drift
- Low R² (< 0.1) suggests stable tracking without systematic drift
- "stable" classification means tracking remains consistent over time

### Step 4: Jitter Analysis

**Example metrics from `jitter_summary.csv`:**

| Camera | Node | Median Jitter (px) | P95 Jitter (px) | Residual Jitter (px) |
|--------|------|---------------------|-----------------|----------------------|
| cam_1 | UpperLip_Center | 0.8 | 1.9 | 0.5 |
| cam_1 | LowerLip_Center | 0.6 | 1.5 | 0.4 |
| cam_2 | UpperLip_Center | 0.9 | 2.1 | 0.6 |

**Interpretation:**
- Median jitter < 1px indicates smooth tracking
- Residual jitter < 0.6px suggests minimal noise
- Higher jitter may affect velocity/acceleration calculations

### Step 5: Camera Synchronization

**Example metrics from `sync_lag_matrix.csv`:**

| Camera From | Camera To | Lag (frames) | Lag (ms) | Correlation |
|-------------|-----------|--------------|----------|-------------|
| cam_1 | cam_2 | 0.2 | 1.67 | 0.98 |
| cam_1 | cam_3 | 0.1 | 0.83 | 0.97 |
| cam_1 | cam_4 | -0.1 | -0.83 | 0.99 |

**Interpretation:**
- Lag < 1 frame indicates good synchronization
- Correlation > 0.95 suggests cameras are well-aligned
- Negative lag means the "from" camera is slightly behind

---

## Phase 2 Results - 3D Reconstruction QC

### Step 1: 3D Track Integrity

**Example metrics from `phase2_step1_coverage_jitter.csv`:**

| Joint | Coverage (%) | Median Jitter (mm/frame) | P95 Jitter (mm/frame) | Longest Gap (ms) |
|-------|--------------|--------------------------|-----------------------|------------------|
| UpperLip_Center | 94.5% | 0.12 | 0.28 | 45.0 |
| LowerLip_Center | 97.2% | 0.09 | 0.22 | 32.0 |
| OutlineRight_Mouth | 88.3% | 0.18 | 0.42 | 78.0 |

**Interpretation:**
- Coverage > 90% indicates reliable 3D reconstruction
- Jitter < 0.2 mm/frame is acceptable for most biomechanical analyses
- Gaps < 100ms suggest continuous tracking

### Step 2: Reprojection Error

**Example metrics from `phase2_step2_reprojection_error.csv`:**

| Camera | Joint | Median Reprojection Error (px) | P95 Reprojection Error (px) |
|--------|-------|-------------------------------|-----------------------------|
| cam_1 | UpperLip_Center | 1.8 | 3.5 |
| cam_1 | LowerLip_Center | 1.5 | 2.9 |
| cam_2 | UpperLip_Center | 2.0 | 3.8 |

**Interpretation:**
- Median error < 2px indicates good geometric consistency
- P95 error < 4px suggests the 3D reconstruction aligns well with camera views
- Higher errors may indicate calibration issues or camera desync

---

## Phase 3 Results - Behavioral Analysis

### Step 1: Normal Vector Stability

**Example metrics from `normal_vector_stability_analysis.csv`:**

Key statistics:
- **Mean angular dispersion**: 2.4 degrees
- **Stable frames**: 85% of total frames
- **Mean angle change**: 1.2 degrees per frame
- **Max angular velocity**: 262.5 deg/s

**Per-second block analysis** shows:
- Mean normal vectors per second
- Angle shifts between consecutive seconds
- Continuity enforcement to avoid 180-degree jumps

**Interpretation:**
- Low angular dispersion (< 5°) indicates stable reference plane
- High percentage of stable frames suggests consistent head orientation
- Angular velocity spikes may indicate movement events

### Step 2: Chewing Sidedness

**Example metrics from `chewing_sidedness_analysis.csv`:**

Summary statistics:
- **Total frames**: 10,000
- **Active chewing frames**: 3,500 (35%)
- **Left classification**: 45% of active frames
- **Right classification**: 40% of active frames
- **Neutral classification**: 15% of active frames
- **Dominant side**: Left

**Interpretation:**
- Balanced left/right distribution suggests no strong lateral preference
- High active chewing percentage indicates good data quality
- Dominant side analysis helps characterize chewing patterns

---

## Phase 4 Results - Gape & Feeding Evaluation

### Per-Session Metrics

**Example metrics from `per_session_metrics.csv`:**

| Session ID | Cycles | Median Latency (frames) | Median Abs Latency | Perfect Onset Rate | F1 Score | Bout Recall |
|------------|--------|-------------------------|-------------------|-------------------|----------|-------------|
| session_001 | 45 | 0.5 | 1.2 | 0.89 | 0.92 | 0.95 |
| session_002 | 52 | -0.3 | 0.9 | 0.94 | 0.94 | 0.97 |
| session_003 | 38 | 1.1 | 1.5 | 0.82 | 0.89 | 0.91 |

**Interpretation:**
- Median latency near 0 indicates accurate timing
- Perfect onset rate > 0.85 suggests good prediction accuracy
- F1 score > 0.90 indicates strong feeding pattern detection
- Bout recall > 0.90 means most feeding bouts are detected

### Summary Statistics

**Example metrics from `summary_metrics.csv` (with 95% CI):**

| Metric | Mean | 95% CI Low | 95% CI High |
|--------|------|------------|-------------|
| Median Latency | 0.20 | -0.15 | 0.55 |
| Median Abs Latency | 1.08 | 0.85 | 1.31 |
| Perfect Onset Rate | 0.904 | 0.872 | 0.936 |
| F1 Feeding | 0.918 | 0.895 | 0.941 |
| Bout Recall | 0.944 | 0.920 | 0.968 |

**Interpretation:**
- Confidence intervals provide statistical robustness
- Narrow intervals indicate consistent performance across sessions
- Mean values with CIs allow for model comparison

---

## Accessing Demo Results

All demo result files are available in the repository:

- **Phase 1 & 2**: `demo_results/session_demo/`
- **Phase 3**: `demo_results/phase3_results/`
- **Phase 4**: `demo_results/phase4_results/`

You can download these files to understand the expected output format and structure.

---

## Notes

- These are example results with synthetic data to illustrate output formats
- Real results will have more frames, nodes, and cameras
- Actual values will depend on your specific tracking data and configuration
- Use these as references when interpreting your own evaluation results

---

[← Back to Home](index.html)

