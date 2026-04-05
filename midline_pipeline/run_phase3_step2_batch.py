#!/usr/bin/env python3
"""
Batch runner for Phase 3 Step 2 (chewing sidedness) without notebook execution.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class Phase3Result:
    session_id: str
    status: str
    message: str
    output_csv: str | None = None
    summary_json: str | None = None


def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, v / n, np.nan)


def _find_node(nodes: list[str], query: str) -> str | None:
    if query in nodes:
        return query
    q = query.lower()
    for n in nodes:
        if n.lower() == q:
            return n
    return None


def _load_long_csv(csv_path: Path) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray]:
    df = pd.read_csv(csv_path)
    required = {"frame", "node", "x", "y", "z", "time_s"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"missing required columns: {sorted(missing)}")

    frames = np.sort(df["frame"].unique())
    nodes = sorted(df["node"].unique().tolist())
    frame_idx = {f: i for i, f in enumerate(frames)}
    node_idx = {n: i for i, n in enumerate(nodes)}
    x3 = np.full((len(frames), len(nodes), 3), np.nan, dtype=float)
    times = np.full(len(frames), np.nan, dtype=float)
    grouped = df.groupby(["frame", "node"], sort=False).first().reset_index()
    for _, row in grouped.iterrows():
        fi = frame_idx[row["frame"]]
        ni = node_idx[row["node"]]
        x3[fi, ni, :] = [row["x"], row["y"], row["z"]]
        times[fi] = row["time_s"]
    return x3, frames, nodes, times


def _classify_frame(speed: float, score: float, vel_thresh: float, score_thresh: float) -> str:
    if not np.isfinite(speed) or speed < vel_thresh:
        return "neutral"
    if not np.isfinite(score):
        return "neutral"
    if score > score_thresh:
        return "right"
    if score < -score_thresh:
        return "left"
    return "neutral"


def run_phase3_step2_for_csv(
    csv_path: Path,
    output_dir: Path,
    node_8_name: str = "node_8",
    node_9_name: str = "node_9",
    landmark_names: tuple[str, str, str] = ("node_1", "node_2", "node_3"),
    velocity_threshold: float = 0.1,
    sidedness_threshold: float = 0.02,
) -> Phase3Result:
    x3, frames, nodes, times = _load_long_csv(csv_path)
    n8 = _find_node(nodes, node_8_name)
    n9 = _find_node(nodes, node_9_name)
    l0 = _find_node(nodes, landmark_names[0])
    l1 = _find_node(nodes, landmark_names[1])
    l2 = _find_node(nodes, landmark_names[2])
    if not all([n8, n9, l0, l1, l2]):
        return Phase3Result(
            session_id=csv_path.parent.name,
            status="failed",
            message=(
                "required nodes missing. need node_8,node_9 and 3 landmarks; "
                f"available sample={nodes[:10]}"
            ),
        )

    idx = {n: i for i, n in enumerate(nodes)}
    p8 = x3[:, idx[n8], :]
    p9 = x3[:, idx[n9], :]
    mid = (p8 + p9) / 2.0

    a = x3[:, idx[l0], :]
    b = x3[:, idx[l1], :]
    c = x3[:, idx[l2], :]
    nrm = _normalize(np.cross(b - a, c - a))

    dt = np.gradient(times)
    safe_dt = np.where(np.isfinite(dt) & (dt > 0), dt, np.nanmedian(dt[np.isfinite(dt) & (dt > 0)]))
    vx = np.gradient(mid[:, 0]) / safe_dt
    vy = np.gradient(mid[:, 1]) / safe_dt
    vz = np.gradient(mid[:, 2]) / safe_dt
    vel = np.column_stack([vx, vy, vz])
    speed = np.linalg.norm(vel, axis=1)
    score = np.sum(vel * nrm, axis=1)
    cls = [
        _classify_frame(float(speed[i]), float(score[i]), velocity_threshold, sidedness_threshold)
        for i in range(len(frames))
    ]

    out_df = pd.DataFrame(
        {
            "frame": frames,
            "time_s": times,
            "node_8_x": p8[:, 0],
            "node_8_y": p8[:, 1],
            "node_8_z": p8[:, 2],
            "node_9_x": p9[:, 0],
            "node_9_y": p9[:, 1],
            "node_9_z": p9[:, 2],
            "midpoint_x": mid[:, 0],
            "midpoint_y": mid[:, 1],
            "midpoint_z": mid[:, 2],
            "velocity_x": vel[:, 0],
            "velocity_y": vel[:, 1],
            "velocity_z": vel[:, 2],
            "velocity_magnitude": speed,
            "normal_x": nrm[:, 0],
            "normal_y": nrm[:, 1],
            "normal_z": nrm[:, 2],
            "sidedness_score": score,
            "classification": cls,
        }
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / "chewing_sidedness_analysis.csv"
    out_json = output_dir / "chewing_sidedness_summary.json"
    out_df.to_csv(out_csv, index=False)

    left_count = int((out_df["classification"] == "left").sum())
    right_count = int((out_df["classification"] == "right").sum())
    neutral_count = int((out_df["classification"] == "neutral").sum())
    total = max(len(out_df), 1)
    summary = {
        "total_frames": int(len(out_df)),
        "left_count": left_count,
        "right_count": right_count,
        "neutral_count": neutral_count,
        "left_percent": 100.0 * left_count / total,
        "right_percent": 100.0 * right_count / total,
        "neutral_percent": 100.0 * neutral_count / total,
        "dominant_side": "right"
        if right_count > left_count
        else ("left" if left_count > right_count else "neutral"),
        "velocity_threshold": velocity_threshold,
        "sidedness_threshold": sidedness_threshold,
    }
    out_json.write_text(json.dumps(summary, indent=2))
    return Phase3Result(
        session_id=csv_path.parent.name,
        status="success",
        message="phase3 step2 complete",
        output_csv=str(out_csv),
        summary_json=str(out_json),
    )


def run_from_manifest(manifest_json: Path) -> list[dict[str, Any]]:
    payload = json.loads(manifest_json.read_text())
    run_results: list[dict[str, Any]] = []
    for rec in payload["sessions"]:
        session_root = Path(rec["session_root"])
        csv_path = session_root / "out_sleap" / "all_nodes_3d_long.csv"
        if not csv_path.exists():
            run_results.append(
                {
                    "session_id": rec["session_id"],
                    "status": "skipped",
                    "message": "missing all_nodes_3d_long.csv",
                }
            )
            continue
        result = run_phase3_step2_for_csv(
            csv_path=csv_path,
            output_dir=session_root / "phase3_step2",
        )
        run_results.append(result.__dict__)
    return run_results


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Phase 3 Step 2 across a batch manifest.")
    p.add_argument("--manifest-json", type=Path, required=True, help="Path to batch sessions manifest.")
    p.add_argument("--output-json", type=Path, required=True, help="Path to write phase3 batch summary JSON.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    results = run_from_manifest(args.manifest_json)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps({"results": results}, indent=2))
    print(f"wrote: {args.output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
