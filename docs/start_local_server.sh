#!/bin/bash
# Script to start local Jekyll server for preview

echo "Starting Jekyll local server..."
echo "The site will be available at: http://localhost:4000/ruten-work/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
bundle exec jekyll serve --baseurl /ruten-work

