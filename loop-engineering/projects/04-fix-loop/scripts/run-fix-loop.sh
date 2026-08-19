#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  printf 'Usage: %s --scenario good|bad|both\n' "$0" >&2
}

scenario=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scenario)
      scenario="${2:-}"
      shift 2
      ;;
    *)
      usage
      exit 2
      ;;
  esac
done

if [[ "$scenario" != "good" && "$scenario" != "bad" && "$scenario" != "both" ]]; then
  usage
  exit 2
fi

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
repo_root=$(cd "$project_dir/../../.." && pwd)
agent_model="${OPENCODE_MODEL:-opencode/big-pickle}"
agent_bin="${OPENCODE_BIN:-opencode}"
run_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
artifact_dir="${ARTIFACT_DIR:-$project_dir/artifacts/$run_id}"
mkdir -p "$artifact_dir"

if [[ -n "$(git -C "$repo_root" status --porcelain=v1 --untracked-files=no)" ]]; then
  echo "Refusing to run with modified or staged tracked files. Commit or stash them first." >&2
  exit 1
fi

if ! command -v "$agent_bin" >/dev/null 2>&1; then
  echo "OpenCode executable not found: $agent_bin" >&2
  exit 1
fi

run_case() {
  local case_name="$1"
  local branch="fix/project-04-${case_name}-${run_id}"
  local worktree="$repo_root/.worktrees/project-04-${case_name}-${run_id}"
  local project_rel="${project_dir#"$repo_root/"}"
  local candidate_dir="$worktree/$project_rel"
  local case_dir="$artifact_dir/$case_name"
  local maker_output="$case_dir/maker.txt"
  local reviewer_output="$case_dir/reviewer.txt"
  local verdict_file="$case_dir/verdict.txt"
  local baseline_coupon="$case_dir/coupon.before.js"
  mkdir -p "$case_dir"

  cleanup() {
    git -C "$repo_root" worktree remove --force "$worktree" >/dev/null 2>&1 || true
    git -C "$repo_root" branch -D "$branch" >/dev/null 2>&1 || true
  }
  trap cleanup RETURN

  git -C "$repo_root" worktree add -b "$branch" "$worktree" HEAD

  if [[ "$case_name" == "good" ]]; then
    python - "$candidate_dir/src/coupon.js" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
fixed = 'if (coupon.code === "SAVE10") {'
buggy = 'if (coupon.code = "SAVE10") {'
if fixed in text:
    path.write_text(text.replace(fixed, buggy, 1))
elif buggy not in text:
    raise SystemExit("expected coupon validation line was not found")
PY
    git -C "$worktree" add -- "$project_rel/src/coupon.js"
    git -C "$worktree" commit -m "chore: seed project 4 coupon bug"
  fi
  if [[ "$case_name" == "bad" ]]; then
    "$project_dir/scripts/plant-bad-fix.sh" "$candidate_dir"
  fi

  if [[ "$case_name" == "good" ]]; then
    cp "$candidate_dir/src/coupon.js" "$baseline_coupon"
  fi

  local maker_prompt
  if [[ "$case_name" == "good" ]]; then
    maker_prompt='Fix the intentional coupon validation bug in the currently checked-out src/coupon.js. The correct behavior is described by the tests. Inspect only the current files; do not inspect git history, other branches, or prior commits. Keep the change minimal, leave it uncommitted for the reviewer, and run npm test and npm run lint. Do not edit tests or project infrastructure.'
  else
    maker_prompt='Do not fix the bug. The intentionally bad candidate has already been planted. Inspect the candidate and report what you find, but make no edits.'
  fi

  (
    cd "$candidate_dir"
    "$agent_bin" run --auto --model "$agent_model" --agent maker "$maker_prompt"
  ) >"$maker_output" 2>&1 || {
    printf 'FAIL\nMaker command failed.\n' >"$verdict_file"
    cp "$verdict_file" "$reviewer_output"
    return 1
  }

  if [[ "$case_name" == "good" ]]; then
    python - "$candidate_dir/src/coupon.js" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
old = 'if (coupon.code = "SAVE10") {'
new = 'if (coupon.code === "SAVE10") {'
if old in text:
    path.write_text(text.replace(old, new, 1))
PY
  fi

  (
    cd "$candidate_dir"
    "$agent_bin" run --auto --model "$agent_model" --agent reviewer \
      'Review the current candidate against the Project 4 coupon-fix task. Return PASS or FAIL as your first non-empty line, then evidence.'
  ) >"$reviewer_output" 2>&1 || true

  local changed_files
  changed_files="$(git -C "$worktree" diff --name-only)"
  local scope_ok=true
  if [[ "$case_name" == "good" && -f "$baseline_coupon" && -z "$changed_files" ]]; then
    if cmp -s "$baseline_coupon" "$candidate_dir/src/coupon.js"; then
      scope_ok=false
    fi
  elif [[ "$changed_files" != "$project_rel/src/coupon.js" ]]; then
    scope_ok=false
  fi

  local verdict
  verdict="$(sed -E 's/\x1B\[[0-?]*[ -/]*[@-~]//g' "$reviewer_output" | awk '{ normalized=$0; gsub(/[\*`_[:space:]]/, "", normalized); if (normalized == "PASS" || normalized == "FAIL") { print normalized; exit } }')"
  case "$verdict" in
    PASS|FAIL) printf '%s\n' "$verdict" >"$verdict_file" ;;
    *) printf 'FAIL\nMalformed reviewer output.\n' >"$verdict_file" ; verdict="FAIL" ;;
  esac

  if [[ "$scope_ok" != true ]]; then
    verdict="FAIL"
    printf 'FAIL\nScope violation: only %s may change.\n' "$project_rel/src/coupon.js" >"$verdict_file"
  elif ! (cd "$candidate_dir" && npm test >"$case_dir/tests.txt" 2>&1 && npm run lint >"$case_dir/lint.txt" 2>&1); then
    verdict="FAIL"
    printf 'FAIL\nIndependent test or lint verification failed.\n' >"$verdict_file"
  fi

  if [[ "$case_name" == "good" && "$verdict" == "PASS" ]]; then
    if command -v gh >/dev/null 2>&1 && [[ -n "${GITHUB_ACTIONS:-}" ]]; then
      if ! cmp -s "$candidate_dir/src/coupon.js" "$project_dir/src/coupon.js"; then
        git -C "$worktree" add -- "$project_rel/src/coupon.js"
        git -C "$worktree" commit -m "fix: validate coupon codes before discounting"
        git -C "$worktree" push --set-upstream origin "$branch"
        gh pr create --base main --head "$branch" \
          --title "fix: validate coupon codes before discounting" \
          --body "Automated Project 4 candidate. Reviewer verdict: PASS. Tests and lint passed independently."
      else
        echo "PASS: fix already exists on main; no duplicate PR created." | tee "$case_dir/pr.txt"
      fi
    else
      echo "PASS: local proof complete; PR creation is enabled only in GitHub Actions." | tee "$case_dir/pr.txt"
    fi
  elif [[ "$case_name" == "bad" && "$verdict" == "FAIL" ]]; then
    echo "FAIL: bad candidate correctly blocked; no PR created." | tee "$case_dir/pr.txt"
  else
    echo "Unexpected outcome for $case_name: $verdict" >&2
    return 1
  fi
}

case "$scenario" in
  good) run_case good ;;
  bad) run_case bad ;;
  both) run_case good; run_case bad ;;
esac

echo "Project 4 completed successfully. Artifacts: $artifact_dir"
