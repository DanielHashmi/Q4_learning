#!/usr/bin/env bash
set -Eeuo pipefail

dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
bash "$dir/run-a.sh" 12345 claude/project-11-draft-12345 "$tmp/a" >/dev/null
grep -Fq 'draft_status=CREATED' "$tmp/a/transcript-a.txt"
grep -Fq 'follow_up_status=NOT_FIRED' "$tmp/a/transcript-a.txt"
bash "$dir/run-b.sh" claude/project-11-draft-12345 12345 'approved in local rehearsal' "$tmp/a" >/dev/null
grep -Fq 'draft_recheck=PASS' "$tmp/a/transcript-b.txt"
grep -Fq 'follow_up_status=COMPLETE' "$tmp/a/transcript-b.txt"
grep -Fq 'follow_up_status: COMPLETE' "$tmp/a/progress.md"
if bash "$dir/run-b.sh" main 12345 'must be rejected' "$tmp/a" >/dev/null 2>&1; then exit 1; fi
if bash "$dir/run-b.sh" claude/project-11-draft-99999 99999 'must be rejected' "$tmp/a" >/dev/null 2>&1; then exit 1; fi
if grep -Fq 'approved in local rehearsal' "$tmp/a/transcript-b.txt"; then exit 1; fi
echo 'Project 11 verification passed: B requires an isolated reviewed draft and explicit approval.'
