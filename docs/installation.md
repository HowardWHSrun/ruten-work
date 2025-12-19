---
layout: default
title: Installation & Setup
---

# Installation & Setup

This guide will help you set up the evaluation metrics toolkit for multi-camera tracking and 3D reconstruction.

---

## Prerequisites

- Python 3.7 or higher
- Jupyter Notebook or JupyterLab
- Required Python packages (see below)

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/HowardWHSrun/ruten-work.git
cd ruten-work
```

### 2. Install Required Python Packages

The evaluation toolkit requires the following packages:

```bash
pip install numpy pandas matplotlib scipy h5py jupyter
```

Or install from a requirements file if provided:

```bash
pip install -r requirements.txt
```

**Key dependencies:**
- `numpy` - Numerical computations
- `pandas` - Data manipulation and CSV handling
- `matplotlib` - Plotting and visualization
- `scipy` - Scientific computing (signal processing, statistics)
- `h5py` - HDF5 file reading (for SLEAP analysis files)
- `jupyter` - Notebook environment

### 3. Verify Installation

Open a Jupyter notebook and test the imports:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py
from scipy import signal
```

If all imports succeed, you're ready to go!

---

## Data Preparation

Before running the evaluation notebooks, you need to prepare your session data:

### Required Files per Session

1. **Per-camera tracking files**: `cam_*.analysis.h5`
   - One file per camera view
   - Output from SLEAP or equivalent tracking system
   - Contains 2D keypoint coordinates over time

2. **Calibration file**: `calibration.json`
   - Camera intrinsics and extrinsics
   - Used for multi-view triangulation and reprojection

3. **3D track file**: `points3d.h5` or `final_3d_tracks.npz`
   - Fused multi-view 3D trajectories
   - Output from your 3D reconstruction pipeline

### Session Folder Structure

Organize your data as follows:

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

## Quick Start

1. **Prepare your session data** (see above)

2. **Open Phase 1, Step 1 notebook**:
   ```
   Phase 1- Sleap Videos & h5 Files/Evaluation_Metric_Step_1.ipynb
   ```

3. **Configure the session path**:
   ```python
   session_path = "session_data/<session_name>/"
   ```

4. **Run the notebook cells** in order

5. **Check the outputs** in:
   ```
   <session_name>/out_metrics/Evaluation_Metrics/metrics_step1/
   ```

---

## Troubleshooting

### Common Issues

**Issue: FileNotFoundError when loading .h5 files**
- Check that file paths are correct
- Verify that files exist in the session directory
- Ensure file permissions allow reading

**Issue: Import errors**
- Make sure all required packages are installed
- Try: `pip install --upgrade <package_name>`

**Issue: Inconsistent node orders across cameras**
- Phase 1 Step 1 will detect and report this
- Ensure all cameras use the same tracking model/configuration

**Issue: Memory errors with large datasets**
- Consider processing sessions in smaller chunks
- Close other applications to free up memory

---

## Next Steps

Once installation is complete:

1. Read the [Complete Workflow Guide](workflow.html)
2. Review [Phase 1 Documentation](phase1.html) to get started
3. Check the [Phase 2](phase2.html), [Phase 3](phase3.html), and [Phase 4](phase4.html) documentation

---

[← Back to Home](index.html)

