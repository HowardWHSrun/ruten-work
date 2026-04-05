#!/usr/bin/env python3
"""
Batch flow requested by user:
1) find DLC outputs,
2) create 3D node results from DLC outputs,
3) create video from those 3D nodes (nodes 1->7 linked).
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

from create_3d_dots_video import process_session


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description="Run DLC->3D->video pipeline for sessions.")
    p.add_argument(
        "--results-root",
        type=Path,
        default=repo_root / "dlc_inference_results",
        help="Root directory that contains DLC output sessions.",
    )
    p.add_argument(
        "--calibration-json",
        type=Path,
        default=repo_root / "Calibration" / "calibration.json",
        help="Calibration JSON with camera projection matrices.",
    )
    p.add_argument(
        "--out-root",
        type=Path,
        default=repo_root / "midline_batch_runs" / "visualizations_from_dlc",
        help="Output root for 3D nodes and videos.",
    )
    p.add_argument("--fps", type=float, default=30.0, help="Output video FPS.")
    p.add_argument("--max-frames", type=int, default=0, help="Max frames per session. Use 0 for all.")
    p.add_argument("--likelihood-threshold", type=float, default=0.6, help="DLC likelihood threshold.")
    p.add_argument("--yaw-deg", type=float, default=35.0, help="Fixed camera yaw angle in degrees.")
    p.add_argument("--pitch-deg", type=float, default=-18.0, help="Fixed camera pitch angle in degrees.")
    p.add_argument("--limit", type=int, default=0, help="Optional: process only first N sessions.")
    return p.parse_args()


def _has_four_camera_csvs(session_dir: Path) -> bool:
    required = ["cam_bottomleft", "cam_bottomright", "cam_topleft", "cam_topright"]
    names = {p.name for p in session_dir.glob("*.csv")}
    for frag in required:
        if not any(frag in n for n in names):
            return False
    return True


def discover_sessions(results_root: Path) -> list[Path]:
    sessions: list[Path] = []
    for top in sorted(p for p in results_root.iterdir() if p.is_dir()):
        children = [c for c in top.iterdir() if c.is_dir()]
        if children:
            for c in sorted(children):
                if _has_four_camera_csvs(c):
                    sessions.append(c)
        elif _has_four_camera_csvs(top):
            sessions.append(top)
    return sessions


def main() -> int:
    args = parse_args()
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_root = args.out_root / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    sessions = discover_sessions(args.results_root)
    if args.limit and args.limit > 0:
        sessions = sessions[: args.limit]

    summary_csv = run_root / "summary.csv"
    rows: list[dict[str, str]] = []
    for session in sessions:
        session_id = f"{session.parent.name}__{session.name}"
        out_dir = run_root / session_id
        video_path = out_dir / f"{session_id}_nodes1to7_3d.mp4"
        try:
            out_video, npz_path, csv_path = process_session(
                session_dir=session,
                calibration_json=args.calibration_json,
                output_video=video_path,
                fps=args.fps,
                max_frames=args.max_frames,
                likelihood_threshold=args.likelihood_threshold,
                save_3d_dir=out_dir,
                yaw_deg=args.yaw_deg,
                pitch_deg=args.pitch_deg,
            )
            rows.append(
                {
                    "session_id": session_id,
                    "source_session": str(session),
                    "status": "success",
                    "video_path": str(out_video),
                    "points3d_npz": str(npz_path),
                    "all_nodes_csv": str(csv_path),
                    "message": "",
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "session_id": session_id,
                    "source_session": str(session),
                    "status": "failed",
                    "video_path": "",
                    "points3d_npz": "",
                    "all_nodes_csv": "",
                    "message": str(exc),
                }
            )

    with summary_csv.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "session_id",
                "source_session",
                "status",
                "video_path",
                "points3d_npz",
                "all_nodes_csv",
                "message",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processed sessions: {len(rows)}")
    print(f"Run root: {run_root}")
    print(f"Summary: {summary_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
