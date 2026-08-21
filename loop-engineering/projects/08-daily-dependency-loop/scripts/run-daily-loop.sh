#!/usr/bin/env bash
set -Eeuo pipefail

repo_root=$(git rev-parse --show-toplevel)
project_rel="loop-engineering/projects/08-daily-dependency-loop"
project_dir="$repo_root/$project_rel"
run_id="$(date -u +%Y%m%dT%H%M%SZ)-${GITHUB_RUN_ID:-local}"
artifact_dir="${ARTIFACT_DIR:-$project_dir/artifacts/$run_id}"
worktree_root="${RUNNER_TEMP:-/tmp}/project-08-worktree-$run_id"
branch="automation/project-08-audit-$run_id"
timeout_seconds="${OPENCODE_TIMEOUT_SECONDS:-300}"
retries="${OPENCODE_RETRIES:-3}"
mkdir -p "$artifact_dir"
exec > >(tee "$artifact_dir/run.log") 2>&1
printf 'run_id=%s\n' "$run_id"

cleanup() { git -C "$repo_root" worktree remove --force "$worktree_root" >/dev/null 2>&1 || true; git -C "$repo_root" branch -D "$branch" >/dev/null 2>&1 || true; }
trap cleanup EXIT
[[ "$timeout_seconds" =~ ^[1-9][0-9]*$ && "$retries" =~ ^[1-9][0-9]*$ ]] || { echo 'invalid budget'; exit 2; }
[[ -z "$(git -C "$repo_root" status --porcelain)" ]] || { echo 'main checkout must be clean'; exit 1; }
git -C "$repo_root" worktree add -b "$branch" "$worktree_root" HEAD
candidate="$worktree_root/$project_rel"

run_agent() {
  local agent="$1" prompt="$2" attempt=1 status=1
  while (( attempt <= retries )); do
    if timeout --foreground --kill-after=10s "${timeout_seconds}s" opencode run --auto --model opencode/big-pickle --agent "$agent" "$prompt"; then return 0; else status=$?; fi
    attempt=$((attempt+1)); sleep "$attempt"
  done
  return "$status"
}

if ! (cd "$candidate" && run_agent maker 'Read progress.md and package.json. Refresh only audit-report.md with a dated dependency audit. Do not change any other file. Run npm test, npm run lint, and npm audit --omit=dev --audit-level=high.'); then
  echo 'maker failed'; exit 1
fi
if ! (cd "$candidate" && run_agent reviewer 'Review this candidate read-only. Return PASS first only if audit-report.md is dated/actionable, only that file changed, and the independent checks should pass. Never edit.'); then
  echo 'reviewer failed'; exit 1
fi

changed=$(git -C "$worktree_root" status --porcelain=v1 --untracked-files=all | sed -E 's/^.. //')
[[ "$changed" == "$project_rel/audit-report.md" ]] || { echo "scope failure: $changed"; exit 1; }
(cd "$candidate" && npm test >"$artifact_dir/tests.txt")
(cd "$candidate" && npm run lint >"$artifact_dir/lint.txt")
(cd "$candidate" && npm audit --omit=dev --audit-level=high >"$artifact_dir/npm-audit.txt" 2>&1)
lines=$(git -C "$worktree_root" diff --numstat | awk '{a+=$1; d+=$2} END {print a+d+0}')
(( lines <= 200 )) || { echo "budget failure: diff lines=$lines"; exit 1; }

git -C "$worktree_root" add "$project_rel/audit-report.md"
git -C "$worktree_root" commit -m "chore(project-08): refresh dependency audit"
git -C "$worktree_root" push origin "$branch"
pr_url=$(GH_TOKEN="${GH_TOKEN:-$GITHUB_TOKEN}" gh pr create --base main --head "$branch" --title "chore(project-08): refresh dependency audit" --body "Automated Project 8 dependency audit. Maker, read-only reviewer, tests, lint, npm audit, scope, and diff-budget checks passed. Review and merge manually.")
printf 'pr_url=%s\n' "$pr_url" | tee "$artifact_dir/pr.txt"

git -C "$repo_root" pull --ff-only origin main
python3 - "$project_dir/progress.md" "$run_id" "$pr_url" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); text=p.read_text(); text += f"\n### {sys.argv[2]}\n- status: needs_human\n- audit: PASS\n- pr: {sys.argv[3]}\n- human gate: review and merge the PR\n"; p.write_text(text)
PY
git -C "$repo_root" add "$project_rel/progress.md"
git -C "$repo_root" commit -m "chore(project-08): record audit run"
git -C "$repo_root" push origin HEAD:main
echo 'Project 8 loop completed through human-gated PR creation.'
