# Local Preview Setup

To preview the GitHub Pages site locally before it's published:

## Quick Start

1. **Install Ruby and Bundler** (if not already installed):
   ```bash
   # macOS (using Homebrew)
   brew install ruby
   
   # Or use system Ruby if available
   ```

2. **Install Jekyll and dependencies**:
   ```bash
   cd docs
   bundle install
   ```

3. **Start the local server**:
   ```bash
   ./start_local_server.sh
   ```
   
   Or manually:
   ```bash
   bundle exec jekyll serve --baseurl /ruten-work
   ```

4. **Open in browser**:
   Navigate to: `http://localhost:4000/ruten-work/`

## Alternative: Simple Python Server

If you don't want to install Jekyll, you can view the markdown files directly:

```bash
cd docs
python3 -m http.server 8000
```

Then open: `http://localhost:8000/index.html`

Note: This won't render Jekyll features, but you can read the markdown content.

## Troubleshooting

**Issue: `bundle: command not found`**
- Install bundler: `gem install bundler`

**Issue: Jekyll build errors**
- Make sure you're in the `docs/` directory
- Try: `bundle update`

**Issue: Port already in use**
- Use a different port: `bundle exec jekyll serve --port 4001`

