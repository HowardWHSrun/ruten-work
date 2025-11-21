# Evaluation Metrics for Multi-Camera Tracking and 3D Reconstruction

Evaluation toolkit for validating multi-camera tracking and 3D reconstruction.  
This repo provides a consistent way to audit data quality before doing any biomechanical / behavioral analysis.

**The goals are:**
- catch failures early (bad tracking, jitter, desync etc.),
- produce objective numbers we can defend,
- generate reports automatically instead of doing manual, ad-hoc checking.

---

## Credits and Attribution

**Original Work:** This repository is based on the evaluation metrics framework developed by **Vishal Soni**. The core Phase 1 and Phase 2 evaluation pipelines are from Vishal's original work.

**Additions by Howard Wang:**
- **Phase 3 - Visualization and Behavioral Analysis**: Added two new analysis notebooks for behavioral pattern extraction:
  - Normal Vector Stability Analysis (Step 1): Analyzes stability of reference plane orientation over time
  - Chewing Sidedness Analysis (Step 2): Determines lateral chewing preference from velocity patterns
- **Phase 4 - Gape & Feeding Evaluation**: Added evaluation notebook for gape onset timing and feeding pattern prediction
- **CT Pedestal Integration**: Enhanced Phase 2 notebooks to support CT marker-based pedestal computation:
  - Added functionality to compute pedestal location from CT markers (F_9 and F_11)
  - Pedestal trajectory is automatically computed from tracked nose landmark using CT-derived offset
  - Pedestal is included in all Phase 2 metrics (coverage, jitter, dropout, reprojection error)

---

## Why this exists

Downstream analysis (3D jaw motion, gape, kinematics, etc.) only makes sense if the raw inputs are trustworthy.

**Phase 1** is a battery of sanity checks run on the 2D per-camera tracking and basic multi-camera alignment.  
It answers: **"Can we trust this session enough to even start doing 3D / biomechanics?"**

If Phase 1 fails, we stop and fix tracking / calibration / sync before wasting time.

---

## How the evaluation is organized

The evaluation pipeline is organized into **4 sequential phases**, each building on the previous one:

- **Phase 1** (5 steps): Per-camera 2D tracking quality control
- **Phase 2** (2 steps): 3D reconstruction trustworthiness validation
- **Phase 3** (2 steps): Visualization and behavioral pattern analysis
- **Phase 4** (1 step): Gape onset timing and feeding pattern evaluation

---

## Phase 1 — Per-camera tracking QC (5 steps)

Phase 1 is split into 5 ordered steps.  
Each step focuses on one failure mode (coverage, pixel accuracy, drift, jitter, sync).

| Step | Phase 1 Evaluation Metric (What this step is doing for us) |
|------|--------------------------------------------------------------|
| **Step 1 – Visibility & Continuity Audit** | For every camera and every node (upper lip, lower lip, jaw ref, head, etc.) we measure: (i) how often that node is detected with confidence above threshold, (ii) how long it stays continuously detected without blinking out, and (iii) how many nodes are valid per frame over time. This immediately shows which cameras or landmarks are flaky, where tracking vanishes, and where coverage collapses mid-session. In plain words: **"Do we actually have reliable signal here, or are we blind half the time?"** |
| **Step 2 – Pixel Accuracy vs Ground Truth** | We align predictions to human-labeled ground truth (auto-fixing small frame offsets), then compute per-frame pixel error for every node in every camera. We also compute PCK-style stats (% of points landing within tight pixel radii like 2–5 px). This answers: **"When the tracker says 'this is the lower lip', is it actually on the lower lip, or is it drifting somewhere else?"** This step catches nodes that looked 'present' in Step 1 but are not anatomically usable. |
| **Step 3 – Temporal Drift Check** | Using the frame-by-frame pixel error from Step 2, we fit error vs time for each (camera, node), report the slope (px per 10k frames) and R², and flag nodes whose error steadily grows. A flat slope = stable lock. A positive slope = slow slide due to skin slip, lighting, or calibration creep. This prevents the classic failure mode: **"the first 10 seconds looked fine so we trusted the whole session."** |
| **Step 4 – Marker Stability / Jitter Audit** | We measure frame-to-frame wobble and residual jitter for each node in each camera: how much the point jumps each frame, and how much it buzzes around a short smoothed trajectory. Even if the average position is "correct", high jitter injects fake velocity/acceleration into gape, angle rate, etc. This step separates real biomechanical motion from neural-net wiggle. In other words: **"Is this trace clean enough to use for kinematics, or is it twitchy nonsense?"** |
| **Step 5 – Inter-Camera Sync / Lag Check** | For each pair of cameras, we cross-correlate the motion traces of the same node to estimate timing offset in frames and produce a lag matrix. If cam A is effectively ~1–2 frames ahead of cam B, multi-view triangulation will give fake 3D. This step answers: **"Are all cameras looking at the same instant in time?"** If not, downstream 3D fusion is automatically suspect. |

**TL;DR of Phase 1:**  
- Step 1 → **Do we even see the points**?  
- Step 2 → **When we see them, are they pixel-correct**?  
- Step 3 → **Do they stay correct, or drift off the anatomy over time**?  
- Step 4 → **Are they stable frame-to-frame, or just vibrating noise**?  
- Step 5 → **Are cameras time-aligned, or desynced**?

_Only if these 5 checks look sane do we move forward._

---

## Phase 2 — 3D Reconstruction QC (2 steps)

### What Phase 2 is trying to prove

Phase 2 asks one question:  
> "Can we trust the 3D kinematics we're about to analyze biologically?"

Everything in Phase 2 is built around that. We don't care only about 'does tracking exist' (Phase 1). Now we care about: is the fused 3D signal actually solid, continuous, and geometrically real.

### How Phase 2 helps us

1. **It quantifies 3D reliability joint by joint.**  
   Step 1 tells us which joints are stable enough to use and which joints are garbage.  
   - If coverage is low or dropout gaps are huge → that joint is not usable for biomechanics.  
   - If jitter in mm/frame is high → that joint will inject fake motion into gape, angle, velocities, etc.

   This prevents us from accidentally publishing "behavioral dynamics" that are actually tracker noise.

2. **It verifies that the 3D is physically consistent with every camera.**  
   Step 2 checks reprojection error: we reproject 3D back into each camera and measure pixel mismatch.  
   - Low reprojection error means: calibration is fine, cameras are in sync, triangulation is honest.  
   - High reprojection error means: do not trust this 3D; something is off (bad cam timing, lip swap, bad calibration).

   This is our reality check. If the 3D doesn't line up with the images, it is not scientifically defensible.

### Why we need this before analysis

- Before we start doing biology (jaw kinematics, gape cycles, chewing frequency, swallow detection, etc.), we need to know that the motion we're measuring is *real jaw motion* and not "math hallucination."
- Phase 2 gives us objective, exportable QC artifacts (CSVs, plots, summary.txt) that we can attach and say:
  - "Here is why we believe these signals," or
  - "Here is why this session / joint is disqualified."

In short:  
**Phase 1 = Did 2D tracking behave?**  
**Phase 2 = Is the 3D reconstruction trustworthy enough to measure biomechanics on it?**

### Phase 2 — Evaluation Metrics

| Step | Phase 2 Evaluation Metric (What this step is doing for us) |
|------|--------------------------------------------------------------|
| **Step 1 – 3D Track Integrity Audit (Coverage / Jitter / Dropout)** | We take the raw fused 3D trajectories (no smoothing, no cleanup, just the direct triangulated output) and score each joint in physical units. For every joint we report: **Coverage (%)** = how often this joint has a valid 3D position (not NaN), **Jitter (mm/frame)** = how much that joint is jumping frame-to-frame in 3D space (median and p95 step size), and **Longest Gap (ms)** = the worst continuous blackout where that joint disappears. Units are auto-normalized to mm, and FPS is used to convert gaps to milliseconds. This step answers: **"Is this 3D skeleton actually present, stable, and continuous — or are we missing chunks, vibrating, or blacking out?"** It's an honest health report of the raw 3D before any rescue/smoothing, so we know what is truly trustworthy. |
| **Step 2 – Geometric Consistency / Reprojection Error Audit** | For every frame, joint, and camera we take the 3D point \[X,Y,Z\], project it back into that camera using its calibration matrix, and compare that predicted 2D pixel location to what the tracker actually saw in that camera. The pixel distance is the reprojection error. We summarize median and p95 reprojection error per (camera, joint), and also per joint across cameras. This answers: **"Does the 3D point really line up with all cameras, or is the '3D' actually inconsistent with the views?"** High reprojection error flags bad calibration, camera desync (one camera a frame ahead/behind), triangulation errors (e.g. swapped upper/lower lip), or just hallucinated 3D. Low error means the 3D geometry is self-consistent and physically believable. |

---

## Phase 3 — Visualization and Behavioral Analysis (2 steps)

### What Phase 3 is trying to prove

Phase 3 provides visualization and behavioral analysis tools for understanding motion patterns in the 3D tracking data. These analyses help characterize:
- Stability of reference planes (e.g., head orientation)
- Chewing sidedness and lateral preference

### How Phase 3 helps us

1. **It quantifies normal vector stability from reference landmarks.**  
   Step 1 analyzes the stability of plane normal vectors computed from 3 landmark points (typically head landmarks).  
   - Measures angle changes, angular velocities, and rolling statistics
   - Classifies frames as "stable" or "changing" based on stability metrics
   - Provides per-second block analysis for longer-period state estimates
   - This helps understand head orientation stability and detect periods of movement vs. stability

2. **It determines chewing sidedness from velocity patterns.**  
   Step 2 analyzes chewing sidedness by comparing the velocity of a midpoint (between two tracked nodes) relative to a reference plane.  
   - Computes velocity vectors and projects them onto plane normal
   - Classifies each frame as "left", "right", or "neutral" based on velocity magnitude and sidedness score
   - Filters out idle movements to focus on active chewing
   - This helps characterize lateral chewing preference and patterns

### Why we need this for analysis

- These visualizations and metrics help understand behavioral patterns in the tracking data
- They provide quantitative measures of stability and sidedness that can be used for downstream analysis
- They complement Phase 1 and Phase 2 by focusing on behavioral characteristics rather than tracking quality

In short:  
**Phase 1 = Did 2D tracking behave?**  
**Phase 2 = Is the 3D reconstruction trustworthy enough to measure biomechanics on it?**  
**Phase 3 = What behavioral patterns can we extract from the 3D data?**

### Phase 3 — Evaluation Metrics

| Step | Phase 3 Evaluation Metric (What this step is doing for us) |
|------|--------------------------------------------------------------|
| **Step 1 – Normal Vector Stability Analysis** | For every frame, we compute the plane normal vector from 3 landmark points (typically head landmarks) and measure stability metrics. We compute: (i) frame-to-frame angle changes and angular velocities, (ii) rolling mean normal vectors over different time windows (0.5s, 1s, 5s), (iii) rolling standard deviation of angles from the rolling mean, (iv) low-pass filtered normals to reduce noise, and (v) state classification (stable/changing) based on stability thresholds. We also provide per-second block analysis with mean normal vectors and angle shifts between seconds. This answers: **"How stable is the reference plane orientation over time, and when are periods of stability vs. movement?"** This helps understand head orientation stability and detect periods of movement vs. stability. |
| **Step 2 – Chewing Sidedness Analysis** | For every frame, we compute the midpoint between two tracked nodes (typically node_8 and node_9), calculate its velocity using central differences, and project the velocity vector onto the plane normal to determine sidedness. We classify each frame as "left", "right", or "neutral" based on velocity magnitude and sidedness score, filtering out idle movements to focus on active chewing. We report summary statistics including total frames, active chewing frames, classification breakdown (left/right/neutral percentages), average sidedness scores, and dominant side. This answers: **"What is the lateral preference in chewing, and how does sidedness vary over time?"** This helps characterize lateral chewing preference and patterns. |

---

## Phase 4 — Gape & Feeding Evaluation (1 step)

### What Phase 4 is trying to prove

Phase 4 focuses on evaluating the quality of gape onset timing predictions and feeding pattern detection. It answers two key questions:

1. **How good is the gape onset timing?**
2. **How well does the predicted feeding pattern (0/1) match ground truth?**

This phase does not do any preprocessing or model prediction – it only evaluates predictions that are already computed. It uses statistically robust metrics (medians, F1, bout recall) and bootstrap 95% confidence intervals (CIs) to summarize performance across sessions.

### How Phase 4 helps us

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

### Expected Inputs

Phase 4 expects **two CSV files**:

#### Ground Truth CSV (`gt.csv`)
Required columns:
- `session_id` – string label for each recording (e.g., monkey01_day1)
- `frame` – frame index or time (must match prediction CSV)
- `feeding_gt` – ground-truth feeding label (0 = not feeding, 1 = feeding)
- `onset_gt` – 1 only at true gape onset frames, 0 otherwise

#### Prediction CSV (`pred.csv`)
Required columns:
- `session_id` – must match GT
- `frame` – must match GT (same values, same order per session)
- `feeding_pred` – model-predicted feeding label (0/1)
- `onset_pred` – 1 at predicted gape onset frames, 0 otherwise

### Phase 4 — Outputs

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

## Directory layout and data flow

This repo expects you to organize each recording session in its own folder.  
**That session folder is both your input and (after running) it will also hold that session's QC results.**

### 1. Session folder (what you start with)

You (the user) prepare a folder for one session, for example:
```text
session_data/
└─ <session_name>/
   ├─ cam_1.analysis.h5
   ├─ cam_2.analysis.h5
   ├─ cam_3.analysis.h5
   ├─ cam_4.analysis.h5
   ├─ calibration.json
   └─ points3d.h5   /   final_3d_tracks.npz
```

**Meaning:**

- `cam_*.analysis.h5` - These are the per-camera 2D tracking outputs after SLEAP (or equivalent). One file per camera view.
- `calibration.json` - Camera calibration + geometry info used to relate the different views.
- `points3d.h5` / `final_3d_tracks.npz` - A fused multi-view 3D track dump for that same session (whatever your upstream pipeline exports as the "current best 3D").

This single `<session_name>/` directory is what you point the evaluation code at.  
That is the **ONLY** path you need to give the Phase 1 and Phase 2 notebooks.

### 2. Evaluation notebooks — Phase 1

In the repo, you have notebooks in the folder:
```text
Phase 1- Sleap Videos & h5 Files/
├─ Evaluation_Metric_Step_1.ipynb
├─ Evaluation_Metric_Step_2.ipynb
├─ Evaluation_Metric_Step_3.ipynb
├─ Evaluation_Metric_Step_4.ipynb
└─ Evaluation_Metric_Step_5.ipynb
```

You open these in order (Step 1 → Step 2 → Step 3 → Step 4 → Step 5).  
Inside each notebook you provide the path to the session folder:
```python
session_path = "session_data/<session_name>/"
```

The code will read:
- all `cam_*.analysis.h5`,
- the shared `calibration.json`,
- the current 3D dump (`points3d.h5` or `final_3d_tracks.npz`).

The notebook then runs that step's QC logic for that same session.

### 3. Evaluation notebooks — Phase 2

In the repo, you have notebooks in the folder:
```text
Phase 2-3D File/
├─ Phase_2_Evaluation_Metric_Step_1.ipynb
└─ Phase_2_Evaluation_Metric_Step_2.ipynb
```

You open these in order (Step 1 → Step 2).  
Inside each notebook you provide the path to the session folder:
```python
session_path = "session_data/<session_name>/"
```

The code will read:

- **The current 3D dump** (`points3d.h5` or `final_3d_tracks.npz`)  
  → this is the main input for Phase 2, used in both Step 1 and Step 2.
  
- **All `cam_*.analysis.h5` files** (the per-camera 2D tracking outputs),  
  used in Phase 2 Step 2.
  
- **The shared `calibration.json`** (camera intrinsics/extrinsics),  
  used in Phase 2 Step 2 to reproject the 3D back into each camera view.

**Optional: CT Pedestal Integration**

Inside the notebooks, you can configure the CT pedestal integration:
```python
# ========== CT PEDESTAL CONFIGURATION (OPTIONAL) ==========
nose_landmark_name = "F"    # update to your tracked nose joint name
include_ct_pedestals = True # set False to disable
# =========================================================
```
- If enabled, the code will use the tracked nose position + hardcoded CT offsets to compute 4 virtual "pedestal" landmarks.
- These landmarks are included in the coverage, jitter, and reprojection reports.

Each notebook runs that step's QC logic for that same session and writes out CSV summaries and plots.

### 4. Evaluation notebooks — Phase 3

In the repo, you have notebooks in the folder:
```text
Phase 3-Visualization/
├─ Phase_3_Evaluation_Metric_Step_1.ipynb
└─ Phase_3_Evaluation_Metric_Step_2.ipynb
```

You open these in order (Step 1 → Step 2).  
Inside each notebook you provide the path to a CSV file with 3D node data:
```python
csv_path = r"data/processed/all_nodes_3d_long.csv"
```

The CSV file should have columns: `frame`, `node`, `x`, `y`, `z`, `time_s`.

**For Step 1 (Normal Vector Stability):**
- You configure which 3 landmark nodes to use for plane computation
- The notebook computes normal vectors and stability metrics
- Outputs: `normal_vector_stability_analysis.csv` and `normal_vector_stability_sec_blocks.csv`

**For Step 2 (Chewing Sidedness):**
- You configure which two nodes to use for midpoint calculation (e.g., node_8 and node_9)
- You configure which 3 landmark nodes to use for plane computation
- The notebook computes velocities, sidedness scores, and classifications
- Outputs: `chewing_sidedness_analysis.csv`

Each notebook runs that step's analysis and writes out CSV summaries and statistics.

### 5. Evaluation notebooks — Phase 4

In the repo, you have the notebook in the folder:
```text
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

### 6. Output structure (what the code creates for you)

When you run a notebook for a given session, the code writes results back inside that same session folder under a nested output tree.

Concretely, after running the evaluation notebooks, your session folder will now look like:
```text
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

**Important details:**

- `out_metrics/` is created automatically inside that same `<session_name>/`.
- Inside `out_metrics/`, the code creates `Evaluation_Metrics/`.
- Inside `Evaluation_Metrics/`, each Phase 1 notebook creates its own subfolder:
  - Step 1 notebook writes into `metrics_step1/`
  - Step 2 notebook writes into `metrics_step2/`
  - Step 3 notebook writes into `metrics_step3/`
  - Step 4 notebook writes into `metrics_step4/`
  - Step 5 notebook writes into `metrics_step5/`

- `out_3d_eval/` is also created automatically inside that same `<session_name>/`.
  - Inside `out_3d_eval/`, you get all Phase 2 evaluation results (Step 1 and Step 2).

This means every QC artifact for that session stays local to that session.  
You don't have to manually create these folders — the notebooks do it when they run.

**Phase 3 and Phase 4 outputs:**

Phase 3 and Phase 4 notebooks create output files in a configured directory (typically `results/` or another specified output directory):
- Phase 3: `normal_vector_stability_analysis.csv`, `normal_vector_stability_sec_blocks.csv`, `chewing_sidedness_analysis.csv`
- Phase 4: Outputs are displayed in the notebook (`per_session_df`, `summary_df`) and can be exported as needed

---

## Workflow summary

### Complete Pipeline Workflow

1. **Prepare session data**
   
   Make a new folder for one session under `session_data/<session_name>/`.
   
   Put in (for that session):
   - all `cam_*.analysis.h5` (per-camera 2D tracks),
   - `calibration.json`,
   - the current 3D track dump (`points3d.h5` or `final_3d_tracks.npz`).

2. **Run Phase 1 — Per-Camera Tracking QC**
   
   Open and run notebooks in order:  
   `Evaluation_Metric_Step_1.ipynb` → ... → `Evaluation_Metric_Step_5.ipynb`
   
   Point them at the session folder.
   
   Phase 1 code will create `out_metrics/Evaluation_Metrics/` inside that session folder and populate:
   - `metrics_step1/`
   - `metrics_step2/`
   - `metrics_step3/`
   - `metrics_step4/`
   - `metrics_step5/`

3. **Run Phase 2 — 3D Reconstruction QC**
   
   Open and run notebooks in order:  
   `Phase_2_Evaluation_Metric_Step_1.ipynb` → `Phase_2_Evaluation_Metric_Step_2.ipynb`
   
   Use the same session folder.
   
   **Optional:** Configure CT pedestal integration if needed.
   
   Phase 2 code will create `out_3d_eval/` inside that session folder.  
   - `out_3d_eval/` holds all Phase 2 evaluation results (Step 1 and Step 2).

4. **Run Phase 3 — Visualization and Behavioral Analysis**
   
   Open and run notebooks in order:  
   `Phase_3_Evaluation_Metric_Step_1.ipynb` → `Phase_3_Evaluation_Metric_Step_2.ipynb`
   
   Provide a CSV file with 3D node data (`frame`, `node`, `x`, `y`, `z`, `time_s`).
   
   Configure landmark nodes for plane computation and analysis.
   
   Phase 3 code will create output CSVs in the configured directory (typically `results/`).

5. **Run Phase 4 — Gape & Feeding Evaluation**
   
   Open and run:  
   `Phase_4_Evaluation.ipynb`
   
   Provide two CSV files: `gt.csv` (ground truth) and `pred.csv` (predictions).
   
   Configure the perfect latency tolerance.
   
   Phase 4 displays `per_session_df` and `summary_df` with performance metrics.

At that point, all four phases are complete:
- **Phase 1 QC** (2D per-camera sanity)
- **Phase 2 QC** (3D trustworthiness)
- **Phase 3 Analysis** (visualization and behavioral patterns)
- **Phase 4 Evaluation** (gape timing and feeding prediction accuracy)

---

## Maintainers

- **Original Framework**: Vishal Soni
- **Phase 3, Phase 4 & CT Integration**: Howard Wang

---

## Repository

This repository is maintained at: https://github.com/ruten-neuro/Centralized-behavioral-video-analysis-pipeline-Howard
