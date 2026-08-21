#!/usr/bin/env bash
set -Eeuo pipefail
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp "$dir/dreaming-state.md" "$tmp/state.md"
cat > "$tmp/progress.md" <<'EOF'
# planted verification log

### 2026-08-21T00:00:00Z-seed-a
- correction: preflight must run before artifact upload

### 2026-08-22T00:00:00Z-seed-b
- correction: preflight must run before artifact upload
- obsolete_rule: temporary debug logging
EOF
PROGRESS_FILE="$tmp/progress.md" STATE_FILE="$tmp/state.md" OUTPUT_DIR="$tmp/proposal" DREAM_RUN_ID=local-rehearsal bash "$dir/dream.sh" >/dev/null
bash "$dir/check-proposal.sh" "$tmp/proposal"
grep -Fq '2026-08-21' "$tmp/proposal/proposed-rules-change.md"
grep -Fq '2026-08-22' "$tmp/proposal/proposed-rules-change.md"
grep -Fq 'temporary debug logging' "$tmp/proposal/proposed-deletion.md"
! find "$tmp" -maxdepth 2 -type f \( -name 'CLAUDE.md' -o -name 'AGENTS.md' \) | grep -q .
echo 'Project 12 verification passed: repeated planted evidence became a cited PR proposal.'
