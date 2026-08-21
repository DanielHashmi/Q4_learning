#!/usr/bin/env bash
set -Eeuo pipefail

mode=${1:-}
case "$mode" in
  dotenv|environment) ;;
  *) echo "usage: $0 <dotenv|environment>" >&2; exit 2 ;;
esac

dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
transcript=${TRANSCRIPT_PATH:-"$dir/transcript-$mode.txt"}
started=$(date -u +%Y-%m-%dT%H:%M:%SZ)

{
  echo 'infrastructure_status=GREEN'
  echo "run_started_at=$started"
  echo "mode=$mode"
  echo 'prompt=prompt.md'

  if [[ "$mode" == dotenv ]]; then
    if [[ -f "$dir/.env" ]]; then
      echo 'dotenv_present=YES'
      echo 'task_status=FAIL'
      echo 'task_evidence=.env exists only in the working copy; a fresh cloud clone must not rely on it'
    else
      echo 'dotenv_present=NO'
      echo 'task_status=FAIL'
      echo 'task_evidence=missing file: .env'
      echo 'diagnosis=gitignored files never reach the fresh GitHub clone'
    fi
  else
    if [[ -n "${PROJECT10_DUMMY_TOKEN:-}" ]]; then
      echo 'task_status=PASS'
      echo "task_evidence=read PROJECT10_DUMMY_TOKEN from environment (length=${#PROJECT10_DUMMY_TOKEN})"
      echo 'token_output=redacted'
    else
      echo 'task_status=FAIL'
      echo 'task_evidence=environment variable PROJECT10_DUMMY_TOKEN is unset'
    fi
  fi

  echo "run_finished_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$transcript"

cat "$transcript"
# A green infrastructure run is intentional even when the task failed.
exit 0
