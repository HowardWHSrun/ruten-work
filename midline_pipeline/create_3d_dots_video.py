#!/usr/bin/env python3
"""
Create a 3D-node result + video from a DLC inference session.

Flow:
1) read DLC 2D outputs (4 cameras),
2) triangulate 3D nodes,
3) save 3D node results,
4) render MP4 from 3D nodes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


CAMERA_FRAGMENTS = {
    "cam-bottomleft.mp4": "cam_bottomleft",
    "cam-bottomright.mp4": "cam_bottomright",
    "cam-topleft.mp4": "cam_topleft",
    "cam-topright.mp4": "cam_topright",
}


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description="Create 3D dots MP4 from a session.")
    p.add_argument("--session-dir", type=Path, required=True, help="Path to one inference session folder.")
    p.add_argument(
        "--calibration-json",
        type=Path,
        default=repo_root / "Calibration" / "calibration.json",
        help="Calibration JSON containing P matrices.",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=repo_root / "midline_batch_runs" / "visualizations" / "dots_3d_preview.mp4",
        help="Output MP4 path.",
    )
    p.add_argument("--fps", type=float, default=30.0, help="Output video FPS.")
    p.add_argument(
        "--max-frames",
        type=int,
        default=0,
        help="Max frames to render. Use 0 for all frames.",
    )
    p.add_argument("--likelihood-threshold", type=float, default=0.6, help="DLC likelihood threshold.")
    p.add_argument("--yaw-deg", type=float, default=35.0, help="Fixed camera yaw angle in degrees.")
    p.add_argument("--pitch-deg", type=float, default=-18.0, help="Fixed camera pitch angle in degrees.")
    p.add_argument(
        "--save-3d-dir",
        type=Path,
        default=None,
        help="Directory to save triangulated 3D outputs (npz/csv). Defaults next to output video.",
    )
    return p.parse_args()


def load_calibration(calibration_json: Path) -> dict[str, np.ndarray]:
    payload = json.loads(calibration_json.read_text())
    return {cam: np.array(mat, dtype=float) for cam, mat in payload["P"].items()}


def find_camera_csv(session_dir: Path, camera_fragment: str) -> Path:
    matches = sorted(session_dir.glob(f"{camera_fragment}*snapshot_best-10.csv"))
    if not matches:
        matches = sorted(session_dir.glob(f"{camera_fragment}*.csv"))
    if not matches:
        raise FileNotFoundError(f"No CSV found for fragment: {camera_fragment} in {session_dir}")
    return matches[0]


def load_dlc_csv(csv_path: Path) -> tuple[np.ndarray, list[str]]:
    df = pd.read_csv(csv_path, header=[0, 1, 2], index_col=0)
    bodyparts = list(dict.fromkeys(df.columns.get_level_values(1).tolist()))
    node_names = [f"node_{bp}" for bp in bodyparts]
    t = len(df)
    n = len(bodyparts)
    arr = np.full((t, n, 3), np.nan, dtype=float)
    for i, bp in enumerate(bodyparts):
        arr[:, i, 0] = df.xs((bp, "x"), axis=1, level=[1, 2]).iloc[:, 0].to_numpy(dtype=float)
        arr[:, i, 1] = df.xs((bp, "y"), axis=1, level=[1, 2]).iloc[:, 0].to_numpy(dtype=float)
        arr[:, i, 2] = df.xs((bp, "likelihood"), axis=1, level=[1, 2]).iloc[:, 0].to_numpy(dtype=float)
    return arr, node_names


def triangulate_point(uvs: list[np.ndarray], ps: list[np.ndarray]) -> np.ndarray:
    a_rows = []
    for (u, v), p in zip(uvs, ps):
        a_rows.append(u * p[2, :] - p[0, :])
        a_rows.append(v * p[2, :] - p[1, :])
    a = np.stack(a_rows, axis=0)
    _, _, vt = np.linalg.svd(a)
    xh = vt[-1]
    if abs(xh[3]) < 1e-12:
        return np.array([np.nan, np.nan, np.nan], dtype=float)
    xh = xh / xh[3]
    return xh[:3]


def triangulate_all(
    per_cam: dict[str, np.ndarray],
    p_mats: dict[str, np.ndarray],
    likelihood_threshold: float,
    max_frames: int,
) -> tuple[np.ndarray, list[str]]:
    cams = list(per_cam.keys())
    min_t = min(per_cam[c].shape[0] for c in cams)
    n_nodes = per_cam[cams[0]].shape[1]
    node_names = [f"node_{i+1}" for i in range(n_nodes)]
    t = min_t if max_frames <= 0 else min(min_t, max_frames)
    x3 = np.full((t, n_nodes, 3), np.nan, dtype=float)

    for fi in range(t):
        for ni in range(n_nodes):
            uvs: list[np.ndarray] = []
            ps: list[np.ndarray] = []
            for cam in cams:
                x, y, lk = per_cam[cam][fi, ni, :]
                if np.isfinite(x) and np.isfinite(y) and np.isfinite(lk) and lk >= likelihood_threshold:
                    uvs.append(np.array([x, y], dtype=float))
                    ps.append(p_mats[cam])
            if len(uvs) >= 2:
                x3[fi, ni, :] = triangulate_point(uvs, ps)
    return x3, node_names


def rotation_matrix(yaw_deg: float = 35.0, pitch_deg: float = -15.0) -> np.ndarray:
    yaw = np.deg2rad(yaw_deg)
    pitch = np.deg2rad(pitch_deg)
    ry = np.array(
        [
            [np.cos(yaw), 0, np.sin(yaw)],
            [0, 1, 0],
            [-np.sin(yaw), 0, np.cos(yaw)],
        ],
        dtype=float,
    )
    rx = np.array(
        [
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)],
        ],
        dtype=float,
    )
    return rx @ ry


def _compute_world_stats(x3: np.ndarray) -> tuple[np.ndarray, float]:
    valid = np.isfinite(x3).all(axis=2)
    pts = x3[valid]
    if pts.size == 0:
        return np.zeros(3, dtype=float), 1.0
    center = np.nanmedian(pts, axis=0)
    d = np.linalg.norm(pts - center[None, :], axis=1)
    scale = float(np.nanpercentile(d, 95))
    if not np.isfinite(scale) or scale < 1e-9:
        scale = 1.0
    return center, scale


def project_points_perspective(
    points: np.ndarray,
    width: int,
    height: int,
    center: np.ndarray,
    scale: float,
    yaw_deg: float,
    pitch_deg: float,
) -> tuple[np.ndarray, np.ndarray]:
    rot = rotation_matrix(yaw_deg=yaw_deg, pitch_deg=pitch_deg)
    p = (points - center[None, :]) / scale
    p = p @ rot.T
    valid = np.isfinite(p).all(axis=1)
    uv = np.full((points.shape[0], 2), np.nan, dtype=float)
    depth = np.full(points.shape[0], np.nan, dtype=float)
    if not valid.any():
        return uv, depth

    cam_dist = 4.0
    z_cam = p[:, 2] + cam_dist
    f = 0.95 * min(width, height)
    cx = width * 0.5
    cy = height * 0.55
    ok = valid & (z_cam > 0.1)
    if not ok.any():
        return uv, depth

    uv[ok, 0] = cx + f * (p[ok, 0] / z_cam[ok])
    uv[ok, 1] = cy - f * (p[ok, 1] / z_cam[ok])
    depth[ok] = z_cam[ok]
    return uv, depth


def _draw_axes(
    frame: np.ndarray,
    width: int,
    height: int,
    center: np.ndarray,
    scale: float,
    yaw_deg: float,
    pitch_deg: float,
) -> None:
    axes = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.2, 0.0, 0.0],
            [0.0, 1.2, 0.0],
            [0.0, 0.0, 1.2],
        ],
        dtype=float,
    )
    uv, _ = project_points_perspective(
        points=axes * scale + center[None, :],
        width=width,
        height=height,
        center=center,
        scale=scale,
        yaw_deg=yaw_deg,
        pitch_deg=pitch_deg,
    )
    if not np.isfinite(uv).all():
        return
    o = tuple(np.int32(np.round(uv[0])).tolist())
    x = tuple(np.int32(np.round(uv[1])).tolist())
    y = tuple(np.int32(np.round(uv[2])).tolist())
    z = tuple(np.int32(np.round(uv[3])).tolist())
    cv2.line(frame, o, x, (80, 80, 255), 2, cv2.LINE_AA)
    cv2.line(frame, o, y, (80, 255, 80), 2, cv2.LINE_AA)
    cv2.line(frame, o, z, (255, 120, 80), 2, cv2.LINE_AA)


def render_video(
    x3: np.ndarray,
    node_names: list[str],
    output: Path,
    fps: float,
    yaw_deg: float = 35.0,
    pitch_deg: float = -18.0,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    width, height = 900, 900
    writer = cv2.VideoWriter(
        str(output),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    chain = [f"node_{i}" for i in range(1, 8)]
    idx = {n: i for i, n in enumerate(node_names)}
    chain_idx = [idx[n] for n in chain if n in idx]
    center, scale = _compute_world_stats(x3)

    for fi in range(x3.shape[0]):
        frame = np.full((height, width, 3), 255, dtype=np.uint8)
        yaw = yaw_deg
        pitch = pitch_deg
        uv, depth = project_points_perspective(
            x3[fi],
            width=width,
            height=height,
            center=center,
            scale=scale,
            yaw_deg=yaw,
            pitch_deg=pitch,
        )
        _draw_axes(frame, width, height, center=center, scale=scale, yaw_deg=yaw, pitch_deg=pitch)

        # draw chain 1->7 first
        for a, b in zip(chain_idx[:-1], chain_idx[1:]):
            if np.isfinite(uv[a]).all() and np.isfinite(uv[b]).all():
                p1 = tuple(np.int32(np.round(uv[a])).tolist())
                p2 = tuple(np.int32(np.round(uv[b])).tolist())
                d = np.nanmean([depth[a], depth[b]])
                thick = int(np.clip(5.5 - d, 2, 5))
                cv2.line(frame, p1, p2, (30, 120, 220), thick, cv2.LINE_AA)

        # draw points
        draw_order = np.argsort(np.nan_to_num(depth, nan=np.inf))[::-1]
        for ni in draw_order:
            if not np.isfinite(uv[ni]).all():
                continue
            p = tuple(np.int32(np.round(uv[ni])).tolist())
            d = float(depth[ni]) if np.isfinite(depth[ni]) else 5.0
            near_weight = float(np.clip((4.5 - d) / 3.5, 0.0, 1.0))
            color = (
                int(140 + 60 * near_weight),
                int(170 + 60 * near_weight),
                int(140 + 40 * near_weight),
            )
            radius = int(np.clip(8.0 - d, 3, 8))
            if ni in chain_idx:
                color = (40, 100, 210)
                radius = int(np.clip(9.0 - d, 5, 10))
            cv2.circle(frame, p, radius, color, -1, cv2.LINE_AA)

        cv2.putText(
            frame,
            f"Frame {fi+1}/{x3.shape[0]} | 3D view (nodes 1-7 chain)",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (40, 40, 40),
            2,
            cv2.LINE_AA,
        )
        writer.write(frame)

    writer.release()


def save_3d_results(x3: np.ndarray, node_names: list[str], fps: float, save_dir: Path) -> tuple[Path, Path]:
    save_dir.mkdir(parents=True, exist_ok=True)
    npz_path = save_dir / "points3d_from_dlc.npz"
    csv_path = save_dir / "all_nodes_3d_long.csv"

    np.savez_compressed(npz_path, X3=x3.astype(np.float32), node_names=np.array(node_names), FPS=float(fps))

    t = np.arange(x3.shape[0], dtype=float) / float(fps)
    chunks = []
    for j, node in enumerate(node_names):
        chunks.append(
            pd.DataFrame(
                {
                    "frame": np.arange(x3.shape[0], dtype=int),
                    "node": node,
                    "x": x3[:, j, 0],
                    "y": x3[:, j, 1],
                    "z": x3[:, j, 2],
                    "time_s": t,
                }
            )
        )
    pd.concat(chunks, ignore_index=True).to_csv(csv_path, index=False)
    return npz_path, csv_path


def process_session(
    session_dir: Path,
    calibration_json: Path,
    output_video: Path,
    fps: float,
    max_frames: int,
    likelihood_threshold: float,
    save_3d_dir: Path | None = None,
    yaw_deg: float = 35.0,
    pitch_deg: float = -18.0,
) -> tuple[Path, Path, Path]:
    p_mats = load_calibration(calibration_json)

    per_cam: dict[str, np.ndarray] = {}
    node_names_ref: list[str] | None = None
    for cam_key, frag in CAMERA_FRAGMENTS.items():
        csv_path = find_camera_csv(session_dir, frag)
        arr, node_names = load_dlc_csv(csv_path)
        if node_names_ref is None:
            node_names_ref = node_names
        per_cam[cam_key] = arr

    x3, node_names = triangulate_all(
        per_cam=per_cam,
        p_mats=p_mats,
        likelihood_threshold=likelihood_threshold,
        max_frames=max_frames,
    )
    three_d_dir = save_3d_dir or output_video.parent
    npz_path, csv_path = save_3d_results(x3=x3, node_names=node_names, fps=fps, save_dir=three_d_dir)
    render_video(
        x3=x3,
        node_names=node_names,
        output=output_video,
        fps=fps,
        yaw_deg=yaw_deg,
        pitch_deg=pitch_deg,
    )
    return output_video, npz_path, csv_path


def main() -> int:
    args = parse_args()
    output_video, npz_path, csv_path = process_session(
        session_dir=args.session_dir,
        calibration_json=args.calibration_json,
        output_video=args.output,
        fps=args.fps,
        max_frames=args.max_frames,
        likelihood_threshold=args.likelihood_threshold,
        save_3d_dir=args.save_3d_dir,
        yaw_deg=args.yaw_deg,
        pitch_deg=args.pitch_deg,
    )
    print(f"3D video saved: {output_video}")
    print(f"3D nodes npz: {npz_path}")
    print(f"3D nodes csv: {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
