# Instructions to Push to GitHub

## Prerequisites
1. Make sure you have git installed
2. Make sure you have access to the repository: https://github.com/ruten-neuro/Centralized-behavioral-video-analysis-pipeline-Howard

## Current Situation
The current directory is part of a larger git repository. We need to create a new git repository specifically for this project.

## Steps to Push

### Step 1: Create a new git repository in this folder

```bash
cd /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main

# Remove existing git connection (if any) - this won't affect parent repo
# We'll create a fresh git repo just for this folder

# Initialize a new git repository
git init

# Add remote repository
git remote add origin https://github.com/ruten-neuro/Centralized-behavioral-video-analysis-pipeline-Howard.git

# Add all files in this directory
git add .

# Create initial commit
git commit -m "Initial commit: Add Phase 3 visualization analysis and CT pedestal integration

- Added Phase 3 notebooks for normal vector stability and chewing sidedness analysis
- Enhanced Phase 2 notebooks with CT marker-based pedestal computation
- Updated README with proper attribution to Vishal Soni's original work
- Added documentation for Phase 3 features

Original framework by Vishal Soni
Phase 3 and CT integration by Howard Wang"

# Push to GitHub
git branch -M main
git push -u origin main
```

### Alternative: If the repository already exists on GitHub

If the repository already exists and has files, you may need to pull first:

```bash
cd /Users/howardwang/Desktop/Ruten/Evaluation-Metrics_Vishal-main

# Initialize git
git init

# Add remote
git remote add origin https://github.com/ruten-neuro/Centralized-behavioral-video-analysis-pipeline-Howard.git

# Pull existing files (if any)
git pull origin main --allow-unrelated-histories

# Add all files
git add .

# Commit
git commit -m "Add Phase 3 visualization analysis and CT pedestal integration

- Added Phase 3 notebooks for normal vector stability and chewing sidedness analysis
- Enhanced Phase 2 notebooks with CT marker-based pedestal computation
- Updated README with proper attribution to Vishal Soni's original work
- Added documentation for Phase 3 features"

# Push
git push -u origin main
```

### If you get authentication errors

You may need to authenticate. Options:
1. Use GitHub CLI: `gh auth login`
2. Use personal access token instead of password
3. Set up SSH keys

## Verify

After pushing, verify by visiting:
https://github.com/ruten-neuro/Centralized-behavioral-video-analysis-pipeline-Howard

You should see:
- All Phase 1, Phase 2, and Phase 3 notebooks
- Updated README.md with proper attribution
- All project files
- PUSH_TO_GITHUB.md (this file)

