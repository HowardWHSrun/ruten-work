---
layout: default
title: Phase 4 - Gape & Feeding Evaluation
---

# Phase 4 — Gape & Feeding Evaluation (1 step)

## What Phase 4 is trying to prove

Phase 4 focuses on evaluating the quality of gape onset timing predictions and feeding pattern detection. It answers two key questions:

1. **How good is the gape onset timing?**
2. **How well does the predicted feeding pattern (0/1) match ground truth?**

This phase does not do any preprocessing or model prediction – it only evaluates predictions that are already computed. It uses statistically robust metrics (medians, F1, bout recall) and bootstrap 95% confidence intervals (CIs) to summarize performance across sessions.

## How Phase 4 helps us

Phase 4 provides objective performance metrics for:

1. **Gape Onset Latency**
   - `median_latency`: Median of (predicted onset - true onset), indicating if the model is early/late/on-time
   - `median_abs_latency`: Median absolute timing error, showing typical prediction accuracy
   - `perfect_onset_rate`: Fraction of gape cycles predicted within a tight tolerance (e.g., ±1 frame)

2. **Feeding Pattern Detection**
   - `f1_feeding`: Frame-wise F1-score for the 0/1 feeding classification
   - `bout_recall`: Fraction of true feeding bouts that are detected by the model

3. **Cross-Session Reliability**
   - Bootstrap 95% confidence intervals for all metrics across sessions
   - Per-session breakdown to identify outlier sessions

## Expected Inputs

Phase 4 expects **two CSV files**:

### Ground Truth CSV (`gt.csv`)
Required columns:
- `session_id` – string label for each recording (e.g., monkey01_day1)
- `frame` – frame index or time (must match prediction CSV)
- `feeding_gt` – ground-truth feeding label (0 = not feeding, 1 = feeding)
- `onset_gt` – 1 only at true gape onset frames, 0 otherwise

### Prediction CSV (`pred.csv`)
Required columns:
- `session_id` – must match GT
- `frame` – must match GT (same values, same order per session)
- `feeding_pred` – model-predicted feeding label (0/1)
- `onset_pred` – 1 at predicted gape onset frames, 0 otherwise

## Phase 4 — Outputs

The notebook produces two key outputs:

1. **`per_session_df`** – One row per session with metrics:
   - `n_cycles` – number of gape onsets evaluated
   - `median_latency` – median timing error (frames)
   - `median_abs_latency` – median absolute timing error
   - `perfect_onset_rate` – fraction within tolerance
   - `n_frames` – total number of frames
   - `f1_feeding` – F1 score for feeding detection
   - `bout_recall` – fraction of feeding bouts detected

2. **`summary_df`** – Mean ± 95% CI across all sessions:
   - For each metric: `mean`, `ci_low`, `ci_high`
   - Provides statistically robust summary for model comparison

In short:  
**Phase 1 = Did 2D tracking behave?**  
**Phase 2 = Is the 3D reconstruction trustworthy enough to measure biomechanics on it?**  
**Phase 3 = What behavioral patterns can we extract from the 3D data?**  
**Phase 4 = How accurate are our gape timing and feeding predictions?**

---

## Usage

### Evaluation notebook — Phase 4

In the repo, you have the notebook in the folder:

```
Phase 4-Gape Analysis/
└─ Phase_4_Evaluation.ipynb
```

Inside the notebook you provide paths to two CSV files:

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

---

## Outputs

Phase 4 outputs are displayed in the notebook (`per_session_df`, `summary_df`) and can be exported as needed.

---

[← Phase 3](phase3.html) | [Back to Home](index.html)

