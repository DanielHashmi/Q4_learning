#!/usr/bin/env bash
set -Eeuo pipefail

run_id=${1:-}
branch=${2:-}
out_dir=${3:-draft}
if [[ ! "$run_id" =~ ^[0-9]+$ || ! "$branch" =~ ^claude/project-11-draft-[0-9]+$ ]]; then
  echo 'usage: run-a.sh <numeric-run-id> <claude/project-11-draft-run-id> [output-dir]' >&2
  exit 2
fi

mkdir -p "$out_dir"
cat > "$out_dir/project-11-draft.md" <<EOF
# Project 11 follow-up draft

- source_run_id: $run_id
- branch: $branch
- status: DRAFT
- proposed_action: write one immutable approval record after human review
- scope: this rehearsal only; no deploy, merge, payment, or external message
- human_decision_required: true

This file is a proposal. Routine A has not performed the follow-up action.
EOF
cat > "$out_dir/progress.md" <<EOF
# Project 11 gate state

- draft_run_id: $run_id
- draft_branch: $branch
- draft_status: awaiting-human-review
- follow_up_status: not-fired
EOF
cat > "$out_dir/transcript-a.txt" <<EOF
infrastructure_status=GREEN
routine=A
run_id=$run_id
branch=$branch
action=draft-only
draft_status=CREATED
follow_up_status=NOT_FIRED
human_gate=REQUIRED
EOF
cat "$out_dir/transcript-a.txt"
