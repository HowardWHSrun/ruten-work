#!/usr/bin/env python3
"""
Complete Pipeline Runner
========================
Runs all evaluation phases (1, 2, 3) and organizes results for easy presentation.

Results are saved to: face/results/n20/
  - phase1_step1/ through phase1_step5/
  - phase2_step1/, phase2_step2/
  - phase3_step1/, phase3_step2/
"""

import json
import subprocess
import sys
import os
import tempfile
from pathlib import Path
import shutil
from datetime import datetime

BASE_DIR = Path("/Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main")
OUT_ROOT = BASE_DIR / "face" / "results" / "n20"

def extract_and_run_notebook_cell(notebook_path, cell_idx=1, timeout=600):
    """Extract and run a specific cell from a notebook"""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    if cell_idx >= len(nb['cells']):
        return False, "Cell not found"
    
    cell = nb['cells'][cell_idx]
    if cell['cell_type'] != 'code':
        return False, "Not a code cell"
    
    code = ''.join(cell.get('source', []))
    if not code.strip():
        return False, "Empty cell"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        result = subprocess.run([sys.executable, temp_path], 
                              capture_output=True, text=True, cwd=str(BASE_DIR), timeout=timeout)
        output = result.stdout
        if result.stderr and "Traceback" in result.stderr:
            return False, result.stderr
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def organize_phase1_results():
    """Move Phase 1 results from old nested structure to new flat structure"""
    old_base = OUT_ROOT / "phase1_temp_session" / "out_metrics" / "Evaluation_Metrics"
    mappings = {
        "metrics_step1": "phase1_step1",
        "metrics_step2": "phase1_step2",
        "metrics_step3": "phase1_step3",
        "metrics_step4": "phase1_step4",
    }
    
    for old_name, new_name in mappings.items():
        old_path = old_base / old_name
        new_path = OUT_ROOT / new_name
        if old_path.exists() and not new_path.exists():
            shutil.copytree(old_path, new_path)
            print(f"  → Moved {old_name} → {new_name}")

def create_presentation_summary():
    """Create comprehensive summary for presentation"""
    summary_path = OUT_ROOT / "PRESENTATION_SUMMARY.md"
    
    summary = f"""# Evaluation Pipeline Results - Presentation Summary

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This directory contains comprehensive evaluation results from the complete tracking and analysis pipeline.

## Results Structure

### Phase 1: 2D Tracking Quality Control (Per-Camera Analysis)

#### Step 1: Detection Coverage & Fragmentation
**Location:** `phase1_step1/`

**Key Files:**
- `detection_coverage.csv` - Per-node coverage metrics by camera
- `per_frame_node_counts.csv` - Frame-by-frame node detection counts
- `node_list.json` - Node names and FPS information
- `viz_coverage_thresholded_READABLE.png` - Coverage visualization
- `viz_median_run_length_READABLE.png` - Continuity visualization

**What it tells you:**
- Which nodes are reliably tracked across cameras
- How stable tracking is (fragmentation vs continuous)
- Per-frame tracking health over time

#### Step 2: Pixel Error & PCK Metrics
**Location:** `phase1_step2/`

**Key Files:**
- `error_by_frame.csv` - Per-frame pixel errors
- `pixel_error_stats_by_cam_node.csv` - Summary statistics
- `pck_table.csv` - Percentage of Correct Keypoints at various thresholds
- `pck_curve_overall.png` - PCK curve visualization
- `per_node_error_boxplot.png` - Error distribution by node

**What it tells you:**
- Tracking accuracy in pixels
- PCK at different thresholds (e.g., 2px, 5px, 10px)
- Which nodes have highest/lowest accuracy

#### Step 3: Temporal Drift Analysis
**Location:** `phase1_step3/`

**Key Files:**
- `drift_by_cam_node.csv` - Drift metrics per camera/node
- `top_issues.csv` - Worst drift cases
- `drift_heatmap.png` - Visual drift map
- `rolling_example.png` - Example rolling error plot

**What it tells you:**
- Whether tracking accuracy degrades over time
- Which cameras/nodes show drift
- Temporal stability assessment

#### Step 4: Marker Stability & Jitter
**Location:** `phase1_step4/`

**Key Files:**
- `jitter_by_cam_node.csv` - Frame-to-frame movement (jitter)
- `jitter_top_issues.csv` - Worst jitter cases
- `jitter_heatmap.png` - Jitter visualization
- `top_series/` - Time-series plots for worst cases

**What it tells you:**
- How jumpy/noisy tracking is
- Frame-to-frame stability
- Which nodes are most stable

#### Step 5: Inter-Camera Synchronization
**Location:** `phase1_step5/`

**Key Files:**
- `lag_by_cam_pair_node.csv` - Lag between camera pairs
- `lag_typicality_summary.txt` - Synchronization quality summary

**What it tells you:**
- Camera synchronization quality
- Frame offset between cameras
- Temporal alignment assessment

### Phase 2: 3D Reconstruction Quality Control

#### Step 1: 3D Coverage, Jitter & Dropout
**Location:** `phase2_step1/`

**Key Files:**
- `3d_coverage_by_joint.csv` - Coverage percentage per joint
- `3d_jitter_by_joint.csv` - Jitter metrics (mm/frame)
- `3d_dropout_by_joint.csv` - Longest gap per joint (ms)
- `plot_coverage_by_joint.png` - Coverage visualization
- `plot_jitter_by_joint.png` - Jitter visualization
- `plot_dropout_by_joint.png` - Dropout visualization
- `summary.txt` - Overall session health summary

**What it tells you:**
- 3D tracking completeness (% coverage)
- 3D tracking noise (jitter in mm/frame)
- Worst tracking gaps (dropout in ms)
- Overall 3D data quality

#### Step 2: Reprojection Error Analysis
**Location:** `phase2_step2/`

**Key Files:**
- `reprojection_error_by_cam_and_joint.csv` - Per-camera reprojection errors
- `reprojection_error_by_joint_overall.csv` - Overall joint errors

**What it tells you:**
- How well 3D points project back to 2D
- Geometric consistency across cameras
- Calibration quality assessment

### Phase 3: Visualization & Behavioral Analysis

#### Step 1: Normal Vector Stability
**Location:** `phase3_step1/`

**Key Files:**
- `normal_vector_stability_analysis.csv` - Frame-by-frame normal vectors
- `normal_vector_stability_sec_blocks.csv` - Per-second block analysis
- `distribution_statistics.csv` - Statistical summary
- `worst_case_frames.csv` - Frames with largest deviations

**What it tells you:**
- Reference plane orientation stability
- Head pose consistency
- Behavioral pattern analysis

#### Step 2: Chewing Sidedness Analysis
**Location:** `phase3_step2/`

**Key Files:**
- `chewing_sidedness_analysis.csv` - Frame-by-frame sidedness scores

**What it tells you:**
- Lateral chewing preference
- Jaw movement patterns
- Behavioral laterality

## Quick Presentation Guide

### For Technical Audiences:
1. Start with **Phase 1 Step 1** coverage plots - shows tracking reliability
2. Show **Phase 1 Step 2** PCK curves - demonstrates accuracy
3. Present **Phase 2 Step 1** summary.txt - overall 3D quality
4. Highlight **Phase 2 Step 2** reprojection errors - geometric consistency

### For Non-Technical Audiences:
1. **Phase 1 Step 1** coverage plots - "How well does tracking work?"
2. **Phase 2 Step 1** summary.txt - "What's the overall data quality?"
3. **Phase 3** behavioral analysis - "What patterns do we see?"

## Key Metrics to Highlight

### Tracking Quality:
- **Coverage**: % of frames where nodes are detected (target: >80%)
- **PCK@5px**: Percentage of keypoints within 5 pixels (target: >90%)
- **Jitter**: Frame-to-frame movement (target: <2mm/frame for 3D)

### 3D Quality:
- **Coverage**: % of frames with valid 3D (target: >70%)
- **Jitter**: 3D tracking noise (target: <1mm/frame)
- **Reprojection Error**: 3D→2D projection accuracy (target: <5px median)

## File Formats

- **CSV files**: Can be opened in Excel, Python, R for further analysis
- **PNG files**: High-resolution plots ready for presentations
- **JSON files**: Machine-readable metadata
- **TXT files**: Human-readable summaries

## Notes

- All paths are relative to: `face/results/n20/`
- Session: 2025-05-28_14-12-04_124591
- FPS: 120 Hz (where applicable)
- Coordinate system: 3D in meters (converted to mm for display)

---
*Generated by complete pipeline runner*
"""
    
    with open(summary_path, 'w') as f:
        f.write(summary)
    
    print(f"\n✓ Created presentation summary: {summary_path}")

def main():
    print("="*70)
    print("COMPLETE EVALUATION PIPELINE RUNNER")
    print("="*70)
    print(f"Results directory: {OUT_ROOT}")
    print("="*70)
    
    phases = [
        ("Phase 1 - Step 1", "Phase 1- Sleap Videos & h5 Files/Evaluation_Metric_Step_1.ipynb", 1),
        ("Phase 1 - Step 2", "Phase 1- Sleap Videos & h5 Files/Evaluation_Metric_Step_2.ipynb", 2),
        ("Phase 1 - Step 3", "Phase 1- Sleap Videos & h5 Files/Evaluation_Metric_Step_3.ipynb", 5),
        ("Phase 1 - Step 4", "Phase 1- Sleap Videos & h5 Files/Evaluation_Metric_Step_4.ipynb", 4),
        ("Phase 1 - Step 5", "Phase 1- Sleap Videos & h5 Files/Evaluation_Metric_Step_5.ipynb", 0),
        ("Phase 2 - Step 1", "Phase 2-3D File/Phase_2_Evaluation_Metric_Step_1.ipynb", 3),
        ("Phase 2 - Step 2", "Phase 2-3D File/Phase_2_Evaluation_Metric_Step_2.ipynb", 1),
        ("Phase 3 - Step 1", "Phase 3-Visualization/Phase_3_Evaluation_Metric_Step_1.ipynb", 1),
        ("Phase 3 - Step 2", "Phase 3-Visualization/Phase_3_Evaluation_Metric_Step_2.ipynb", 1),
    ]
    
    results = []
    
    for i, (name, notebook, cell_idx) in enumerate(phases, 1):
        print(f"\n[{i}/{len(phases)}] {name}")
        print("-" * 70)
        
        notebook_path = BASE_DIR / notebook
        if not notebook_path.exists():
            print(f"✗ Notebook not found: {notebook_path}")
            results.append((name, False, "Notebook not found"))
            continue
        
        success, output = extract_and_run_notebook_cell(str(notebook_path), cell_idx)
        
        if success:
            print(f"✓ {name} completed")
            results.append((name, True, "Success"))
            
            # Organize Phase 1 results after each step
            if "Phase 1" in name:
                organize_phase1_results()
        else:
            print(f"✗ {name} failed: {output[:200]}")
            results.append((name, False, output[:200]))
    
    # Create presentation summary
    print("\n" + "="*70)
    print("ORGANIZING RESULTS FOR PRESENTATION")
    print("="*70)
    create_presentation_summary()
    
    # Final summary
    print("\n" + "="*70)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*70)
    for name, success, msg in results:
        status = "✓" if success else "✗"
        print(f"{status} {name}")
        if not success:
            print(f"    Error: {msg}")
    
    successful = sum(1 for _, s, _ in results if s)
    print(f"\nCompleted: {successful}/{len(results)} phases")
    print(f"\nResults saved to: {OUT_ROOT}")
    print(f"Presentation guide: {OUT_ROOT}/PRESENTATION_SUMMARY.md")

if __name__ == "__main__":
    main()

