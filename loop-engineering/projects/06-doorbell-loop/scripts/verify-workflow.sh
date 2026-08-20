#!/usr/bin/env bash
set -Eeuo pipefail

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
repo_root=$(cd "$project_dir/../../.." && pwd)
workflow="$repo_root/.github/workflows/project-06-opencode-review.yml"

[[ -f "$workflow" ]] || { echo "workflow is missing" >&2; exit 1; }
grep -Fq 'pull_request:' "$workflow"
grep -Fq 'types: [opened, synchronize, reopened, ready_for_review]' "$workflow"
grep -Fq 'anomalyco/opencode/github@latest' "$workflow"
grep -Fq 'OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}' "$workflow"
grep -Fq 'use_github_token: true' "$workflow"
grep -Fq 'pull-requests: write' "$workflow"
grep -Fq 'Do not modify files, commit, or push changes.' "$workflow"

(cd "$project_dir" && npm test >/tmp/project-06-test.txt)
(cd "$project_dir" && npm run lint >/tmp/project-06-lint.txt)

cp "$project_dir/src/range.js" "$project_dir/src/range.js.verify-backup"
trap 'mv "$project_dir/src/range.js.verify-backup" "$project_dir/src/range.js"' EXIT
bash "$project_dir/scripts/plant-bug.sh"
if (cd "$project_dir" && npm test >/tmp/project-06-planted-test.txt 2>&1); then
  echo "planted bug was not detected" >&2
  exit 1
fi

echo "Project 6 local contract passed: workflow trigger, connector, permissions, review prompt, base tests, lint, and planted-bug detection are valid."
