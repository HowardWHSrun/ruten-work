---
layout: default
title: Complete Workflow Guide
---

# Complete Pipeline Workflow

This guide walks you through running the complete evaluation pipeline from start to finish.

---

## 1. Prepare session data

Make a new folder for one session under `session_data/<session_name>/`.

Put in (for that session):
- all `cam_*.analysis.h5` (per-camera 2D tracks),
- `calibration.json`,
- the current 3D track dump (`points3d.h5` or `final_3d_tracks.npz`).

**Example session folder structure:**

```
session_data/
└─ <session_name>/
   ├─ cam_1.analysis.h5
   ├─ cam_2.analysis.h5
   ├─ cam_3.analysis.h5
   ├─ cam_4.analysis.h5
   ├─ calibration.json
   └─ points3d.h5   /   final_3d_tracks.npz
```

---

## 2. Run Phase 1 — Per-Camera Tracking QC

Open and run notebooks in order:  
`Evaluation_Metric_Step_1.ipynb` → ... → `Evaluation_Metric_Step_5.ipynb`

Point them at the session folder:

```python
session_path = "session_data/<session_name>/"
```

Phase 1 code will create `out_metrics/Evaluation_Metrics/` inside that session folder and populate:
- `metrics_step1/`
- `metrics_step2/`
- `metrics_step3/`
- `metrics_step4/`
- `metrics_step5/`

**What Phase 1 checks:**
- Step 1: Visibility & continuity of tracked nodes
- Step 2: Pixel accuracy vs ground truth
- Step 3: Temporal drift over time
- Step 4: Marker stability and jitter
- Step 5: Inter-camera synchronization

---

## 3. Run Phase 2 — 3D Reconstruction QC

Open and run notebooks in order:  
`Phase_2_Evaluation_Metric_Step_1.ipynb` → `Phase_2_Evaluation_Metric_Step_2.ipynb`

Use the same session folder:

```python
session_path = "session_data/<session_name>/"
```

**Optional:** Configure CT pedestal integration if needed:

```python
# ========== CT PEDESTAL CONFIGURATION (OPTIONAL) ==========
nose_landmark_name = "F"    # update to your tracked nose joint name
include_ct_pedestals = True # set False to disable
# =========================================================
```

Phase 2 code will create `out_3d_eval/` inside that session folder.  
- `out_3d_eval/` holds all Phase 2 evaluation results (Step 1 and Step 2).

**What Phase 2 checks:**
- Step 1: 3D track integrity (coverage, jitter, dropout)
- Step 2: Geometric consistency (reprojection error)

---

## 4. Run Phase 3 — Visualization and Behavioral Analysis

Open and run notebooks in order:  
`Phase_3_Evaluation_Metric_Step_1.ipynb` → `Phase_3_Evaluation_Metric_Step_2.ipynb`

Provide a CSV file with 3D node data (`frame`, `node`, `x`, `y`, `z`, `time_s`):

```python
csv_path = r"data/processed/all_nodes_3d_long.csv"
```

Configure landmark nodes for plane computation and analysis.

Phase 3 code will create output CSVs in the configured directory (typically `results/`).

**What Phase 3 analyzes:**
- Step 1: Normal vector stability (reference plane orientation)
- Step 2: Chewing sidedness (lateral preference)

---

## 5. Run Phase 4 — Gape & Feeding Evaluation

Open and run:  
`Phase_4_Evaluation.ipynb`

Provide two CSV files: `gt.csv` (ground truth) and `pred.csv` (predictions):

```python
gt_csv_path = "data/gt.csv"
pred_csv_path = "data/pred.csv"
```

**Configuration:**
```python
perfect_tol = 1.0  # e.g. ±1 frame at 60 Hz
```

The notebook will:
- Load and align ground truth and prediction CSVs by `session_id` and `frame`
- Compute per-session metrics (latency, F1, bout recall)
- Aggregate metrics across sessions with bootstrap 95% CI
- Display `per_session_df` and `summary_df`
- Optionally plot median latency per session

**What Phase 4 evaluates:**
- Gape onset timing accuracy
- Feeding pattern detection performance

---

## Final Output Structure

After running all phases, your session folder will look like:

```
session_data/
└─ <session_name>/
   ├─ cam_1.analysis.h5
   ├─ cam_2.analysis.h5
   ├─ cam_3.analysis.h5
   ├─ cam_4.analysis.h5
   ├─ calibration.json
   ├─ points3d.h5   /   final_3d_tracks.npz
   │
   ├─ out_metrics/
   │  └─ Evaluation_Metrics/
   │     ├─ metrics_step1/
   │     ├─ metrics_step2/
   │     ├─ metrics_step3/
   │     ├─ metrics_step4/
   │     └─ metrics_step5/
   │
   └─ out_3d_eval/
      └─ ... Phase 2 evaluation results (Step 1 and Step 2) ...
```

**Phase 3 and Phase 4 outputs:**
- Phase 3: Output CSVs in configured directory (typically `results/`)
- Phase 4: Results displayed in notebook (can be exported)

---

## Summary

At that point, all four phases are complete:
- **Phase 1 QC** (2D per-camera sanity)
- **Phase 2 QC** (3D trustworthiness)
- **Phase 3 Analysis** (visualization and behavioral patterns)
- **Phase 4 Evaluation** (gape timing and feeding prediction accuracy)

---

[← Back to Home](index.html)

