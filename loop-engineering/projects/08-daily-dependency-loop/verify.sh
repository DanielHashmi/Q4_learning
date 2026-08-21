#!/usr/bin/env bash
set -Eeuo pipefail
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
for file in README.md progress.md package.json audit-report.md test/audit.test.js scripts/lint.js .opencode/agents/maker.md .opencode/agents/reviewer.md; do
  [[ -f "$dir/$file" ]] || { echo "missing $file" >&2; exit 1; }
done
grep -Fq 'worktree' "$dir/README.md"
grep -Fq 'progress.md' "$dir/README.md"
grep -Fq 'gh' "$dir/README.md"
grep -Fq 'mode: primary' "$dir/.opencode/agents/maker.md"
grep -Fq 'edit: false' "$dir/.opencode/agents/reviewer.md"
(cd "$dir" && npm test)
(cd "$dir" && npm run lint)
echo 'Project 8 local contract passed.'
