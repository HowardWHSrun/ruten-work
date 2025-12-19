---
layout: default
title: Phase 2 - 3D Reconstruction QC
---

# Phase 2 — 3D Reconstruction QC (2 steps)

## What Phase 2 is trying to prove

Phase 2 asks one question:  
> "Can we trust the 3D kinematics we're about to analyze biologically?"

Everything in Phase 2 is built around that. We don't care only about 'does tracking exist' (Phase 1). Now we care about: is the fused 3D signal actually solid, continuous, and geometrically real.

## How Phase 2 helps us

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

## Why we need this before analysis

- Before we start doing biology (jaw kinematics, gape cycles, chewing frequency, swallow detection, etc.), we need to know that the motion we're measuring is *real jaw motion* and not "math hallucination."
- Phase 2 gives us objective, exportable QC artifacts (CSVs, plots, summary.txt) that we can attach and say:
  - "Here is why we believe these signals," or
  - "Here is why this session / joint is disqualified."

In short:  
**Phase 1 = Did 2D tracking behave?**  
**Phase 2 = Is the 3D reconstruction trustworthy enough to measure biomechanics on it?**

## Phase 2 — Evaluation Metrics

| Step | Phase 2 Evaluation Metric (What this step is doing for us) |
|------|--------------------------------------------------------------|
| **Step 1 – 3D Track Integrity Audit (Coverage / Jitter / Dropout)** | We take the raw fused 3D trajectories (no smoothing, no cleanup, just the direct triangulated output) and score each joint in physical units. For every joint we report: **Coverage (%)** = how often this joint has a valid 3D position (not NaN), **Jitter (mm/frame)** = how much that joint is jumping frame-to-frame in 3D space (median and p95 step size), and **Longest Gap (ms)** = the worst continuous blackout where that joint disappears. Units are auto-normalized to mm, and FPS is used to convert gaps to milliseconds. This step answers: **"Is this 3D skeleton actually present, stable, and continuous — or are we missing chunks, vibrating, or blacking out?"** It's an honest health report of the raw 3D before any rescue/smoothing, so we know what is truly trustworthy. |
| **Step 2 – Geometric Consistency / Reprojection Error Audit** | For every frame, joint, and camera we take the 3D point \[X,Y,Z\], project it back into that camera using its calibration matrix, and compare that predicted 2D pixel location to what the tracker actually saw in that camera. The pixel distance is the reprojection error. We summarize median and p95 reprojection error per (camera, joint), and also per joint across cameras. This answers: **"Does the 3D point really line up with all cameras, or is the '3D' actually inconsistent with the views?"** High reprojection error flags bad calibration, camera desync (one camera a frame ahead/behind), triangulation errors (e.g. swapped upper/lower lip), or just hallucinated 3D. Low error means the 3D geometry is self-consistent and physically believable. |

---

## Usage

### Evaluation notebooks — Phase 2

In the repo, you have notebooks in the folder:

```
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

### Optional: CT Pedestal Integration

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

---

## Outputs

All outputs are stored under:
`<session_name>/out_3d_eval/`

- `out_3d_eval/` holds all Phase 2 evaluation results (Step 1 and Step 2).

---

[← Phase 1](phase1.html) | [Back to Home](index.html) | [Next: Phase 3 →](phase3.html)

