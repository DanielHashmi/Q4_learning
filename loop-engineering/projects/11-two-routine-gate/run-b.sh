#!/usr/bin/env bash
set -Eeuo pipefail

branch=${1:-}
run_id=${2:-}
approval_note=${3:-}
out_dir=${4:-.}
if [[ ! "$run_id" =~ ^[0-9]+$ || ! "$branch" =~ ^claude/project-11-draft-[0-9]+$ || -z "$approval_note" ]]; then
  echo 'usage: run-b.sh <claude/project-11-draft-run-id> <numeric-run-id> <approval-note> [output-dir]' >&2
  exit 2
fi

draft="$out_dir/project-11-draft.md"
progress="$out_dir/progress.md"
[[ -f "$draft" && -f "$progress" ]] || { echo 'Routine B refused: draft state is missing.' >&2; exit 3; }
grep -Fq "source_run_id: $run_id" "$draft"
grep -Fq "branch: $branch" "$draft"
grep -Fq 'status: DRAFT' "$draft"
grep -Fq 'human_decision_required: true' "$draft"
if grep -Fq 'follow_up_status: COMPLETE' "$progress"; then
  echo 'Routine B refused: follow-up already completed.' >&2
  exit 4
fi

cat > "$out_dir/follow-up-complete.md" <<EOF
# Project 11 follow-up result

- source_run_id: $run_id
- branch: $branch
- status: COMPLETE
- action: wrote this approval record
- approved: true
- approval_note_recorded: yes

The approval note is intentionally not copied into this file. The API caller
provided it, and the transcript records only that a non-empty note existed.
EOF
cat > "$progress" <<EOF
# Project 11 gate state

- draft_run_id: $run_id
- draft_branch: $branch
- draft_status: reviewed-and-approved
- follow_up_status: COMPLETE
EOF
cat > "$out_dir/transcript-b.txt" <<EOF
infrastructure_status=GREEN
routine=B
source_run_id=$run_id
branch=$branch
approval_note_present=YES
draft_recheck=PASS
action=write approval record
follow_up_status=COMPLETE
token_output=redacted
EOF
cat "$out_dir/transcript-b.txt"
