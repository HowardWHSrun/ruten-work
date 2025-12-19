# GitHub Pages Documentation

This directory contains the Jekyll site for the GitHub Pages documentation.

## Enabling GitHub Pages

To enable GitHub Pages for this repository:

1. Go to your repository on GitHub: `https://github.com/HowardWHSrun/ruten-work`
2. Click on **Settings**
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select:
   - **Branch**: `main`
   - **Folder**: `/docs`
5. Click **Save**

GitHub will build and publish your site at: `https://howardwhsrun.github.io/ruten-work/`

## Local Development

To test the site locally:

1. Install Jekyll: `gem install bundler jekyll`
2. Navigate to the `docs/` directory
3. Run: `bundle exec jekyll serve`
4. Open `http://localhost:4000/ruten-work/` in your browser

## Site Structure

- `_config.yml` - Jekyll configuration
- `index.md` - Homepage
- `phase1.md` through `phase4.md` - Phase documentation
- `workflow.md` - Complete workflow guide
- `installation.md` - Installation and setup guide
- `_layouts/` - HTML layout templates
- `assets/` - CSS and other assets

