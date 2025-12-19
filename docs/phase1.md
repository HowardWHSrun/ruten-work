---
layout: default
title: Phase 1 - Per-Camera Tracking QC
---

# Phase 1 — Per-camera tracking QC (5 steps)

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

## Usage

### Evaluation notebooks — Phase 1

In the repo, you have notebooks in the folder:

```
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

---

## Outputs

All outputs are stored under:
`<session_name>/out_metrics/Evaluation_Metrics/`

- Step 1 notebook writes into `metrics_step1/`
- Step 2 notebook writes into `metrics_step2/`
- Step 3 notebook writes into `metrics_step3/`
- Step 4 notebook writes into `metrics_step4/`
- Step 5 notebook writes into `metrics_step5/`

Each step produces CSV files and visualizations specific to that evaluation metric.

---

[← Back to Home](index.html) | [Next: Phase 2 →](phase2.html)

