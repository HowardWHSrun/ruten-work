---
layout: default
title: Home
---

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
  - Added functionality to compute pedestal location from CT markers
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

- **[Phase 1](phase1.html)** (5 steps): Per-camera 2D tracking quality control
- **[Phase 2](phase2.html)** (2 steps): 3D reconstruction trustworthiness validation
- **[Phase 3](phase3.html)** (2 steps): Visualization and behavioral pattern analysis
- **[Phase 4](phase4.html)** (1 step): Gape onset timing and feeding pattern evaluation

---

## Quick Start

1. **[Installation & Setup](installation.html)** - Get started with the evaluation toolkit
2. **[Complete Workflow Guide](workflow.html)** - Step-by-step instructions for running all phases
3. **[Phase Documentation](phase1.html)** - Detailed documentation for each phase

---

## Repository

This repository is maintained at: [https://github.com/HowardWHSrun/ruten-work](https://github.com/HowardWHSrun/ruten-work)

---

## Maintainers

- **Original Framework**: Vishal Soni
- **Phase 3, Phase 4 & CT Integration**: Howard Wang

