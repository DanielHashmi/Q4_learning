#!/bin/sh
# .claude/hooks/reviewer-allowlist.sh — the reviewer may run only these
cmd=$(cat | jq -r '.tool_input.command // empty')
case "$cmd" in
  "npm test"*|"npm run lint"*|"git diff"*) exit 0 ;;
  *) echo "Blocked: reviewer may run only npm test, npm run lint, git diff" >&2
     exit 2 ;;
esac
