# GitHub Pages Setup Instructions

## Enable GitHub Pages

To make your website live at `https://howardwhsrun.github.io/ruten-work/`:

### Step 1: Go to Repository Settings

1. Navigate to: https://github.com/HowardWHSrun/ruten-work
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** in the left sidebar

### Step 2: Configure Pages Source

Under **Source**:
- Select **Branch**: `main`
- Select **Folder**: `/docs`
- Click **Save**

### Step 3: Wait for Build

- GitHub will build your site (usually takes 1-2 minutes)
- You'll see a green checkmark when it's ready
- The site will be available at: **https://howardwhsrun.github.io/ruten-work/**

### Step 4: Verify

After a few minutes, visit:
**https://howardwhsrun.github.io/ruten-work/**

You should see the documentation homepage!

## Troubleshooting

**Site not loading?**
- Wait 2-3 minutes for the first build
- Check the Actions tab for build errors
- Make sure the branch is `main` and folder is `/docs`

**404 Error?**
- Verify the baseurl in `_config.yml` is `/ruten-work`
- Check that `index.md` exists in the `docs/` folder

**Build failing?**
- Check the Actions tab for error messages
- Ensure `_config.yml` is valid YAML
- Verify all required files are in the `docs/` directory

## Current Status

To check if Pages is enabled:
1. Go to: https://github.com/HowardWHSrun/ruten-work/settings/pages
2. You should see the configuration if it's set up

## Local Preview

See `docs/SETUP_LOCAL.md` for instructions on previewing locally before publishing.

