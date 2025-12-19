---
layout: default
title: Phase 3 - Visualization and Behavioral Analysis
---

# Phase 3 — Visualization and Behavioral Analysis (2 steps)

## What Phase 3 is trying to prove

Phase 3 provides visualization and behavioral analysis tools for understanding motion patterns in the 3D tracking data. These analyses help characterize:
- Stability of reference planes (e.g., head orientation)
- Chewing sidedness and lateral preference

## How Phase 3 helps us

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

## Why we need this for analysis

- These visualizations and metrics help understand behavioral patterns in the tracking data
- They provide quantitative measures of stability and sidedness that can be used for downstream analysis
- They complement Phase 1 and Phase 2 by focusing on behavioral characteristics rather than tracking quality

In short:  
**Phase 1 = Did 2D tracking behave?**  
**Phase 2 = Is the 3D reconstruction trustworthy enough to measure biomechanics on it?**  
**Phase 3 = What behavioral patterns can we extract from the 3D data?**

## Phase 3 — Evaluation Metrics

| Step | Phase 3 Evaluation Metric (What this step is doing for us) |
|------|--------------------------------------------------------------|
| **Step 1 – Normal Vector Stability Analysis** | For every frame, we compute the plane normal vector from 3 landmark points (typically head landmarks) and measure stability metrics. We compute: (i) frame-to-frame angle changes and angular velocities, (ii) rolling mean normal vectors over different time windows (0.5s, 1s, 5s), (iii) rolling standard deviation of angles from the rolling mean, (iv) low-pass filtered normals to reduce noise, and (v) state classification (stable/changing) based on stability thresholds. We also provide per-second block analysis with mean normal vectors and angle shifts between seconds. This answers: **"How stable is the reference plane orientation over time, and when are periods of stability vs. movement?"** This helps understand head orientation stability and detect periods of movement vs. stability. |
| **Step 2 – Chewing Sidedness Analysis** | For every frame, we compute the midpoint between two tracked nodes (typically node_8 and node_9), calculate its velocity using central differences, and project the velocity vector onto the plane normal to determine sidedness. We classify each frame as "left", "right", or "neutral" based on velocity magnitude and sidedness score, filtering out idle movements to focus on active chewing. We report summary statistics including total frames, active chewing frames, classification breakdown (left/right/neutral percentages), average sidedness scores, and dominant side. This answers: **"What is the lateral preference in chewing, and how does sidedness vary over time?"** This helps characterize lateral chewing preference and patterns. |

---

## Usage

### Evaluation notebooks — Phase 3

In the repo, you have notebooks in the folder:

```
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

---

## Outputs

Phase 3 notebooks create output files in a configured directory (typically `results/` or another specified output directory):

- Phase 3 Step 1: `normal_vector_stability_analysis.csv`, `normal_vector_stability_sec_blocks.csv`
- Phase 3 Step 2: `chewing_sidedness_analysis.csv`

---

[← Phase 2](phase2.html) | [Back to Home](index.html) | [Next: Phase 4 →](phase4.html)

