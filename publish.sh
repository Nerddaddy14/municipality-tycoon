#!/bin/sh
# Copies the latest game file here, commits, and pushes. Run from this folder.
set -e
cp /c/Users/Stephen/jarvis/zoning-tycoon-chambers/index.html index.html
git add -A
git commit -m "Update playtest build" || echo "Nothing new to commit"
git push
