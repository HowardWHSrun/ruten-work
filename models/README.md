# DLC / PyTorch model backups

This folder contains a **four-camera DeepLabCut (PyTorch)** training backup from `2026-01-08`.

- **Folder:** `backup_four_camera_models_20260108_212859/`
- **Contents:** Per-camera project dirs (`cam-topleft`, `cam-topright`, `cam-bottomleft`, `cam-bottomright`) plus optional `predictions/`.

## Download on the workstation (SSH)

```bash
cd ~/Ruten   # or wherever you keep repos
git clone https://github.com/HowardWHSrun/ruten-work.git
cd ruten-work
# If this was a shallow clone and models are missing history, use full clone:
# git fetch --unshallow   # only if needed
```

Models live under:

`models/backup_four_camera_models_20260108_212859/`

Total size is ~2.3 GB; use a stable network or `git clone` from the office network.
