#!/bin/sh
# Commits any changes in this folder and pushes them to GitHub Pages.
set -e
git add -A
git commit -m "${1:-Update playtest build}" || echo "Nothing new to commit"
git push
