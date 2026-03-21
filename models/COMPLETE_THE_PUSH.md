# Finish uploading these models (if push did not finish from Cursor)

The four-camera backup is committed locally in **two commits** (~1.15 GB each) to stay under GitHub’s large-push limits.

On **your Mac**, in a terminal:

```bash
cd /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main/ruten-work-upload
git status
git log --oneline -3
```

You should see two commits:

1. `Add DLC four-camera model backup (part 1/2: top cameras + predictions)`
2. `Add DLC four-camera model backup (part 2/2: bottom cameras)`

Then push (use HTTPS + Personal Access Token, or `gh auth login`, or SSH remote):

```bash
git remote -v
git push origin main
```

If GitHub asks for credentials, use a **Personal Access Token** (classic) with `repo` scope as the password.

---

## Download on Amaterasu (after push succeeds)

```bash
cd ~/Ruten   # or your preferred directory
git clone https://github.com/HowardWHSrun/ruten-work.git
cd ruten-work
ls models/backup_four_camera_models_20260108_212859
```

Path to the backup:

`models/backup_four_camera_models_20260108_212859/`
