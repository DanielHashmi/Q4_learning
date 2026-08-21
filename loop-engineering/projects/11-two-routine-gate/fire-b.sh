#!/usr/bin/env bash
set -Eeuo pipefail

branch=${1:-}
run_id=${2:-}
approval_note=${3:-}
repo=${GITHUB_REPOSITORY:-DanielHashmi/Q4_learning}
token=${PROJECT11_B_BEARER_TOKEN:-}
if [[ ! "$run_id" =~ ^[0-9]+$ || ! "$branch" =~ ^claude/project-11-draft-[0-9]+$ || -z "$approval_note" || -z "$token" ]]; then
  echo 'usage: PROJECT11_B_BEARER_TOKEN=<token> fire-b.sh <draft-branch> <run-id> <approval-note>' >&2
  exit 2
fi

payload=$(python3 - "$branch" "$run_id" "$approval_note" <<'PY'
import json
import sys
print(json.dumps({"ref": "main", "inputs": {
    "draft_branch": sys.argv[1], "draft_run_id": sys.argv[2],
    "approval_note": sys.argv[3],
}}))
PY
)
curl --fail-with-body --silent --show-error \
  -X POST "https://api.github.com/repos/$repo/actions/workflows/project-11-routine-b.yml/dispatches" \
  -H "Authorization: Bearer $token" \
  -H 'Accept: application/vnd.github+json' \
  -H 'X-GitHub-Api-Version: 2022-11-28' \
  -H 'Content-Type: application/json' \
  --data "$payload"
echo "Routine B fired for $branch (run $run_id)."
