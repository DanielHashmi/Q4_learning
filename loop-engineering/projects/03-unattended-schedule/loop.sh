#!/bin/bash

# Project 3: Unattended Schedule with Spine
# This script demonstrates the spine pattern - memory between loop runs

# Change to script directory
cd "$(dirname "$0")"

# Redirect all output to log file (append mode)
exec >> loop.log 2>&1

echo "=== Loop Run Started: $(date) ==="

opencode run "
You are a TODO scanner that maintains memory between runs via progress.md (the spine).

CRITICAL: Follow this exact order:

1. READ progress.md first to see what TODOs have already been recorded
2. SCAN all *.js and *.ts files in the current directory for TODO comments
3. COMPARE the findings against what's already in progress.md
4. APPEND only NEW TODOs to progress.md with this format:

   ### Scan at YYYY-MM-DD HH:MM:SS
   - file.js:line - TODO description

   If no new TODOs found, write:
   ### Scan at YYYY-MM-DD HH:MM:SS
   No new TODOs found.

5. OUTPUT a summary: how many TODOs scanned, how many were new, how many were already recorded

The spine works when run 2 says 'No new TODOs found' because it READ what run 1 wrote.
"

echo "=== Loop Run Completed: $(date) ==="
echo ""
