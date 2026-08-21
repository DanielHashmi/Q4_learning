#!/usr/bin/env bash
set -Eeuo pipefail
mode="${1:-}"
case "$mode" in success|failure) ;; *) echo 'usage: run-one-off.sh success|failure' >&2; exit 2 ;; esac
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
transcript="${TRANSCRIPT_PATH:-$dir/transcript-$mode.txt}"
stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
{
  echo "infrastructure_status=GREEN"
  echo "run_started_at=$stamp"
  echo "mode=$mode"
  echo 'prompt=prompt.md'
  if [[ "$mode" == success ]]; then
    echo 'task_status=PASS'
    echo 'task_evidence=read success-input.md and produced summary'
  else
    echo 'task_status=FAIL'
    echo 'task_evidence=missing file: missing-input.md'
    echo 'diagnosis=task failed; infrastructure completed normally'
  fi
  echo "run_finished_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$transcript"
cat "$transcript"
# The outer one-off infrastructure is green even when the task reports FAIL.
exit 0
