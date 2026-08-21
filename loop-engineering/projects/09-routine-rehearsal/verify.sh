#!/usr/bin/env bash
set -Eeuo pipefail
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
bash "$dir/run-one-off.sh" success >/dev/null
bash "$dir/run-one-off.sh" failure >/dev/null
grep -Fq 'infrastructure_status=GREEN' "$dir/transcript-success.txt"
grep -Fq 'task_status=PASS' "$dir/transcript-success.txt"
grep -Fq 'infrastructure_status=GREEN' "$dir/transcript-failure.txt"
grep -Fq 'task_status=FAIL' "$dir/transcript-failure.txt"
grep -Fq 'missing file: missing-input.md' "$dir/transcript-failure.txt"
rm -f "$dir/transcript-success.txt" "$dir/transcript-failure.txt"
echo 'Project 9 verification passed: green infrastructure is distinct from task success.'
