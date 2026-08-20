#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  printf 'Usage: %s\n' "$0" >&2
}

if [[ $# -ne 0 ]]; then
  usage
  exit 2
fi

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
repo_root=$(cd "$project_dir/../../.." && pwd)
project_rel="${project_dir#"$repo_root/"}"
agent_model="${OPENCODE_MODEL:-opencode/big-pickle}"
agent_bin="${OPENCODE_BIN:-opencode}"
agent_timeout_seconds="${OPENCODE_TIMEOUT_SECONDS:-90}"
agent_retries="${OPENCODE_RETRIES:-3}"
agent_timeout_seconds="${agent_timeout_seconds%%[!0-9]*}"
agent_retries="${agent_retries%%[!0-9]*}"
run_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
artifact_dir="${ARTIFACT_DIR:-$project_dir/artifacts/$run_id}"
agent_runner="$project_dir/scripts/run-opencode.ps1"

if ! [[ "$agent_timeout_seconds" =~ ^[1-9][0-9]*$ ]]; then
  echo "OPENCODE_TIMEOUT_SECONDS must be a positive integer." >&2
  exit 2
fi
if ! [[ "$agent_retries" =~ ^[1-9][0-9]*$ ]]; then
  echo "OPENCODE_RETRIES must be a positive integer." >&2
  exit 2
fi

if ! command -v "$agent_bin" >/dev/null 2>&1; then
  echo "OpenCode executable not found: $agent_bin" >&2
  exit 1
fi

if ! command -v timeout >/dev/null 2>&1; then
  echo "The timeout command is required to bound agent runs." >&2
  exit 1
fi

if ! command -v powershell.exe >/dev/null 2>&1; then
  echo "powershell.exe is required to isolate OpenCode state on Windows." >&2
  exit 1
fi

if [[ -e "$artifact_dir" ]]; then
  echo "Artifact directory already exists: $artifact_dir" >&2
  echo "Choose a new ARTIFACT_DIR or remove the old run explicitly." >&2
  exit 1
fi

# Project 5 is intentionally runnable while its own files are still untracked
# during development. Tracked modifications are still rejected, and the full
# pre-run status is compared with the post-run status below.
initial_head="$(git -C "$repo_root" rev-parse --verify HEAD)"
initial_status="$(git -C "$repo_root" status --porcelain=v1 --untracked-files=all)"
modified_outside_project="$( { git -C "$repo_root" diff --name-only; git -C "$repo_root" diff --cached --name-only; } | sort -u | awk -v prefix="$project_rel/" 'index($0, prefix) != 1 { print }' )"
if [[ -n "$modified_outside_project" ]]; then
  echo "Refusing to run with modified or staged tracked files outside Project 5:" >&2
  printf '%s\n' "$modified_outside_project" >&2
  exit 1
fi

mkdir -p "$artifact_dir"

cases=(good bad scope)
main_pid="$BASHPID"
worktrees=()
branches=()
pids=()
failed=0
run_result=FAIL
run_reason="run did not complete"

# Keep temporary worktrees outside the repository so they cannot make the main
# checkout appear dirty while candidates are running. A caller may choose a
# different parent, but every run still gets its own exact directory.
if [[ -n "${WORKTREE_DIR:-}" ]]; then
  worktree_parent="$WORKTREE_DIR"
else
  worktree_parent="$(cd "$repo_root/.." && pwd)"
fi
worktree_root="$worktree_parent/.project-05-worktrees-$run_id"
if [[ -e "$worktree_root" ]]; then
  echo "Temporary worktree directory already exists: $worktree_root" >&2
  exit 1
fi
mkdir -p "$worktree_root"

for candidate in "${cases[@]}"; do
  branch="body/project-05-$candidate-$run_id"
  worktree="$worktree_root/$candidate"
  if git -C "$repo_root" show-ref --verify --quiet "refs/heads/$branch"; then
    echo "Refusing to reuse existing branch: $branch" >&2
    exit 1
  fi
  if [[ -e "$worktree" ]]; then
    echo "Refusing to reuse existing worktree path: $worktree" >&2
    exit 1
  fi
  branches+=("$branch")
  worktrees+=("$worktree")
done

write_summary() {
  local cleanup_result="$1"
  local checkout_result="$2"
  local final_head="$3"
  local final_status="$4"

  {
    printf 'run_id=%s\n' "$run_id"
    printf 'candidates=%s\n' "${cases[*]}"
    printf 'engine_state=stateless\n'
    printf 'result=%s\n' "$run_result"
    printf 'cleanup=%s\n' "$cleanup_result"
    printf 'checkout_integrity=%s\n' "$checkout_result"
    printf 'head_before=%s\n' "$initial_head"
    printf 'head_after=%s\n' "$final_head"
    printf 'status_before=%s\n' "$([[ -z "$initial_status" ]] && echo clean || echo preexisting-changes)"
    printf 'status_after=%s\n' "$([[ -z "$final_status" ]] && echo clean || echo preexisting-changes)"
    printf 'reason=%s\n' "$run_reason"
  } >"$artifact_dir/summary.txt"
}

cleanup_on_exit() {
  local exit_status=$?
  local cleanup_failed=0
  local checkout_failed=0
  local final_head
  local final_status

  # EXIT traps are inherited by background candidate subshells. Only the main
  # shell owns the complete cleanup set.
  if [[ "$BASHPID" != "$main_pid" ]]; then
    return "$exit_status"
  fi

  trap - EXIT INT TERM

  # If the main shell is leaving early, stop candidate wrapper processes before
  # removing their worktrees. The bounded timeout also terminates the agent
  # command itself when supported by the platform's timeout implementation.
  if [[ "$exit_status" -ne 0 ]]; then
    for pid in "${pids[@]}"; do
      kill "$pid" 2>/dev/null || true
    done
    sleep 1
    for pid in "${pids[@]}"; do
      kill -KILL "$pid" 2>/dev/null || true
    done
    for pid in "${pids[@]}"; do
      wait "$pid" 2>/dev/null || true
    done
  fi

  for worktree in "${worktrees[@]}"; do
    if ! git -C "$repo_root" worktree remove --force "$worktree" >/dev/null 2>&1; then
      if [[ -e "$worktree" ]]; then
        cleanup_failed=1
      fi
    fi
  done

  for branch in "${branches[@]}"; do
    if git -C "$repo_root" show-ref --verify --quiet "refs/heads/$branch"; then
      if ! git -C "$repo_root" branch -D "$branch" >/dev/null 2>&1; then
        cleanup_failed=1
      fi
    fi
  done

  if [[ -d "$worktree_root" ]] && ! rmdir "$worktree_root" 2>/dev/null; then
    cleanup_failed=1
  fi

  final_head="$(git -C "$repo_root" rev-parse --verify HEAD 2>/dev/null || printf 'unavailable')"
  final_status="$(git -C "$repo_root" status --porcelain=v1 --untracked-files=all 2>/dev/null || printf 'unavailable')"
  if [[ "$final_head" != "$initial_head" || "$final_status" != "$initial_status" ]]; then
    checkout_failed=1
  fi

  if [[ "$cleanup_failed" -ne 0 || "$checkout_failed" -ne 0 ]]; then
    run_result=FAIL
    if [[ "$cleanup_failed" -ne 0 && "$checkout_failed" -ne 0 ]]; then
      run_reason="cleanup and checkout integrity checks failed"
    elif [[ "$cleanup_failed" -ne 0 ]]; then
      run_reason="temporary worktree or branch cleanup failed"
    else
      run_reason="main checkout changed during the run"
    fi
    exit_status=1
  fi

  write_summary "$([[ "$cleanup_failed" -eq 0 ]] && echo PASS || echo FAIL)" \
    "$([[ "$checkout_failed" -eq 0 ]] && echo PASS || echo FAIL)" \
    "$final_head" "$final_status"
  return "$exit_status"
}

trap cleanup_on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

record_candidate_failure() {
  local case_dir="$1"
  local status_file="$2"
  local message="$3"
  printf 'FAIL\n%s\n' "$message" >"$case_dir/verdict.txt"
  printf 'expected=%s\nactual=FAIL\nerror=%s\n' "$4" "$message" >"$status_file"
}

agent_path() {
  local path="$1"
  if command -v wslpath >/dev/null 2>&1; then
    wslpath -w "$path"
  elif command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$path"
  else
    printf '%s\n' "$path"
  fi
}

run_agent() {
  local case_name="$1"
  local candidate_dir="$2"
  local command_name="$3"
  shift 3
  local candidate_dir_for_agent
  local agent_runner_for_agent
  local state_root="$artifact_dir/opencode-state/$case_name"
  local attempt
  local status=1
  candidate_dir_for_agent="$(agent_path "$candidate_dir")"
  agent_runner_for_agent="$(agent_path "$agent_runner")"

  (
    cd "$candidate_dir"
    for ((attempt=1; attempt<=agent_retries; attempt++)); do
      if timeout --foreground --kill-after=5s "${agent_timeout_seconds}s" \
        powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$agent_runner_for_agent" \
          -Directory "$candidate_dir_for_agent" \
          -DataHome "$(agent_path "$state_root/data")" \
          -ConfigHome "$(agent_path "$state_root/config")" \
          -StateHome "$(agent_path "$state_root/state")" \
          -OpenCode "$agent_bin" \
          "$command_name" "$@"; then
        return 0
      else
        status=$?
      fi
      if [[ "$attempt" -lt "$agent_retries" ]]; then
        sleep "$attempt"
      fi
    done
    return "$status"
  )
}

run_candidate() {
  local case_name="$1"
  local expected="$2"
  local branch="body/project-05-$case_name-$run_id"
  local worktree="$worktree_root/$case_name"
  local candidate_dir="$worktree/$project_rel"
  local case_dir="$artifact_dir/$case_name"
  local maker_output="$case_dir/maker.txt"
  local reviewer_output="$case_dir/reviewer.txt"
  local verdict_file="$case_dir/verdict.txt"
  local status_file="$case_dir/status.txt"
  local seed_head
  local maker_status=0
  local reviewer_status=0
  local test_status=0
  local lint_status=0
  local changed_files
  local scope_ok=true
  local head_ok=true
  local reviewer_verdict
  local actual

  mkdir -p "$case_dir"

  if ! git -C "$repo_root" worktree add -b "$branch" "$worktree" HEAD >"$case_dir/worktree.txt" 2>&1; then
    record_candidate_failure "$case_dir" "$status_file" "Worktree setup failed." "$expected"
    return 1
  fi

  if ! {
    mkdir -p "$candidate_dir"
    cp "$project_dir/package.json" "$project_dir/README.md" "$project_dir/.gitignore" "$candidate_dir/"
    cp -R "$project_dir/src" "$project_dir/test" "$candidate_dir/"
    cp -R "$project_dir/.opencode" "$candidate_dir/"
  }; then
    record_candidate_failure "$case_dir" "$status_file" "Candidate files could not be staged." "$expected"
    return 1
  fi

  if ! git -C "$worktree" add -- "$project_rel"; then
    record_candidate_failure "$case_dir" "$status_file" "Candidate baseline could not be staged." "$expected"
    return 1
  fi
  if git -C "$worktree" diff --cached --quiet -- "$project_rel"; then
    printf 'Project files were already present in HEAD; no baseline commit was needed.\n' >"$case_dir/baseline-commit.txt"
  elif ! git -C "$worktree" commit -m "chore: stage project 5 candidate" >"$case_dir/baseline-commit.txt" 2>&1; then
    record_candidate_failure "$case_dir" "$status_file" "Candidate baseline commit failed." "$expected"
    return 1
  fi

  if ! python3 - "$candidate_dir/src/coupon.js" "$candidate_dir/README.md" "$case_name" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1])
readme = Path(sys.argv[2])
case = sys.argv[3]
text = source.read_text()

if case in {"good", "scope"}:
    expected = 'if (coupon.code === "SAVE10") {'
    seeded = 'if (coupon.code = "SAVE10") {'
    if expected not in text:
        raise SystemExit("expected fixed coupon condition was not found")
    source.write_text(text.replace(expected, seeded, 1))
elif case == "bad":
    expected = 'if (coupon.code === "SAVE10") {'
    seeded = 'if (coupon.code === "NEVER-VALID") {'
    if expected not in text:
        raise SystemExit("expected fixed coupon condition was not found")
    source.write_text(text.replace(expected, seeded, 1))
else:
    raise SystemExit(f"unknown candidate: {case}")

if case == "scope":
    readme.write_text("# Project 5 candidate\n\nThis unauthorized change must block the candidate.\n")
PY
  then
    record_candidate_failure "$case_dir" "$status_file" "Candidate seeding failed." "$expected"
    return 1
  fi

  if ! git -C "$worktree" add -- "$project_rel/src/coupon.js"; then
    record_candidate_failure "$case_dir" "$status_file" "Candidate seed could not be staged." "$expected"
    return 1
  fi
  if ! git -C "$worktree" commit -m "chore: seed project 5 candidate" >"$case_dir/seed-commit.txt" 2>&1; then
    record_candidate_failure "$case_dir" "$status_file" "Candidate seed commit failed." "$expected"
    return 1
  fi
  seed_head="$(git -C "$worktree" rev-parse HEAD)"

  local maker_prompt
  case "$case_name" in
    good)
      maker_prompt='Fix the intentional coupon validation bug in src/coupon.js. The tests define the correct behavior. Change only src/coupon.js, leave the fix uncommitted, and run npm test and npm run lint.'
      ;;
    bad)
      maker_prompt='Do not edit this candidate. Inspect the intentionally impossible coupon behavior, run the available checks if useful, and report why it should fail review.'
      ;;
    scope)
      maker_prompt='Fix the intentional coupon validation bug in src/coupon.js. Do not edit README.md or any file other than src/coupon.js. Leave the fix uncommitted and run npm test and npm run lint.'
      ;;
  esac

  if run_agent "$case_name" "$candidate_dir" run --auto --model "$agent_model" --agent maker "$maker_prompt" >"$maker_output" 2>&1; then
    maker_status=0
  else
    maker_status=$?
  fi
  if [[ "$maker_status" -ne 0 ]]; then
    record_candidate_failure "$case_dir" "$status_file" "Maker command failed with exit code $maker_status." "$expected"
    return 1
  fi

  if run_agent "$case_name" "$candidate_dir" run --auto --model "$agent_model" --agent reviewer \
    "Review this Project 5 candidate. The intended task is coupon validation. Return PASS or FAIL as your first non-empty line, then evidence." \
    >"$reviewer_output" 2>&1; then
    reviewer_status=0
  else
    reviewer_status=$?
  fi

  # OpenCode may materialize its skill runtime under .opencode/node_modules.
  # That directory is ignored in the candidate baseline; every tracked or
  # ordinary untracked change remains in scope and is checked below.
  changed_files="$(git -C "$worktree" status --porcelain=v1 --untracked-files=all | sed -E 's/^.. //')"
  if [[ "$case_name" == "good" && "$changed_files" != "$project_rel/src/coupon.js" ]]; then
    scope_ok=false
  elif [[ "$case_name" == "bad" && -n "$changed_files" ]]; then
    scope_ok=false
  elif [[ "$case_name" == "scope" ]]; then
    scope_ok=false
  fi
  if [[ "$(git -C "$worktree" rev-parse HEAD)" != "$seed_head" ]]; then
    head_ok=false
  fi

  reviewer_verdict="$(sed -E 's/\x1B\[[0-?]*[ -/]*[@-~]//g' "$reviewer_output" | awk '{ normalized=$0; gsub(/[*_[:space:]]/, "", normalized); if (normalized == "PASS" || normalized == "FAIL") { print normalized; exit } }')"
  if [[ "$reviewer_verdict" != "PASS" && "$reviewer_verdict" != "FAIL" ]]; then
    reviewer_verdict="FAIL"
    printf 'FAIL\nMalformed reviewer output (exit code %s).\n' "$reviewer_status" >"$verdict_file"
  else
    printf '%s\n' "$reviewer_verdict" >"$verdict_file"
  fi

  if (cd "$candidate_dir" && npm test >"$case_dir/tests.txt" 2>&1); then
    test_status=0
  else
    test_status=$?
  fi
  if (cd "$candidate_dir" && npm run lint >"$case_dir/lint.txt" 2>&1); then
    lint_status=0
  else
    lint_status=$?
  fi

  actual="$reviewer_verdict"
  if [[ "$scope_ok" != true ]]; then
    actual=FAIL
    printf 'FAIL\nIndependent scope check failed. Changed files: %s\n' "$changed_files" >"$verdict_file"
  elif [[ "$head_ok" != true ]]; then
    actual=FAIL
    printf 'FAIL\nCandidate agent changed the candidate commit.\n' >"$verdict_file"
  elif [[ "$test_status" -ne 0 || "$lint_status" -ne 0 ]]; then
    actual=FAIL
    printf 'FAIL\nIndependent test or lint verification failed.\n' >"$verdict_file"
  elif [[ "$reviewer_status" -ne 0 ]]; then
    actual=FAIL
    printf 'FAIL\nReviewer command failed with exit code %s.\n' "$reviewer_status" >"$verdict_file"
  fi

  {
    printf 'expected=%s\n' "$expected"
    printf 'actual=%s\n' "$actual"
    printf 'maker_status=%s\n' "$maker_status"
    printf 'reviewer_status=%s\n' "$reviewer_status"
    printf 'tests=%s\n' "$([[ "$test_status" -eq 0 ]] && echo PASS || echo FAIL)"
    printf 'lint=%s\n' "$([[ "$lint_status" -eq 0 ]] && echo PASS || echo FAIL)"
    printf 'scope=%s\n' "$([[ "$scope_ok" == true ]] && echo PASS || echo FAIL)"
    printf 'head_unchanged=%s\n' "$([[ "$head_ok" == true ]] && echo PASS || echo FAIL)"
    printf 'changed_files=%s\n' "$changed_files"
  } >"$status_file"

  [[ "$actual" == "$expected" ]]
}

for candidate in "${cases[@]}"; do
  case "$candidate" in
    good) expected=PASS ;;
    bad|scope) expected=FAIL ;;
  esac
  run_candidate "$candidate" "$expected" &
  pids+=("$!")
done

for pid in "${pids[@]}"; do
  if ! wait "$pid"; then
    failed=1
  fi
done

if [[ "$failed" -eq 0 ]]; then
  run_result=PASS
  run_reason="all candidate verdicts matched their expected results"
  echo "Project 5 body passed. Read artifacts at $artifact_dir"
else
  run_result=FAIL
  run_reason="one or more candidate verdicts did not match the expected result"
  echo "Project 5 body failed. Read artifacts at $artifact_dir" >&2
fi

if [[ "$failed" -eq 0 ]]; then
  exit 0
fi
exit 1
