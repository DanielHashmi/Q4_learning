#!/usr/bin/env bash
set -Eeuo pipefail
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$dir/progress.md" "$dir/progress.bak"; cp "$dir/cost.json" "$dir/cost.bak"; rm -f "$dir/run.log"
trap 'mv "$dir/progress.bak" "$dir/progress.md"; mv "$dir/cost.bak" "$dir/cost.json"; rm -f "$dir/run.log"' EXIT
bash "$dir/run-loop.sh" healthy
bash "$dir/run-loop.sh" sabotage && exit 1 || true
MAX_ATTEMPTS=2 bash "$dir/run-loop.sh" sabotage && exit 1 || true
bash "$dir/diagnose.sh"
grep -Fq 'attempts=2/2' "$dir/run.log"
echo 'Project 7 verification passed.'
