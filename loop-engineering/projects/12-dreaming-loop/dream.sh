#!/usr/bin/env bash
set -Eeuo pipefail

dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(git -C "$dir" rev-parse --show-toplevel)
progress_file=${PROGRESS_FILE:-$repo_root/loop-engineering/projects/08-daily-dependency-loop/progress.md}
state_file=${STATE_FILE:-$dir/dreaming-state.md}
out_dir=${OUTPUT_DIR:-$dir/proposal}
run_id=${DREAM_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}

python3 - "$progress_file" "$state_file" "$out_dir" "$run_id" <<'PY'
from collections import defaultdict
from datetime import date
from pathlib import Path
import re
import sys

progress_path, state_path, out_dir, run_id = map(Path, sys.argv[1:])
out_dir.mkdir(parents=True, exist_ok=True)
state = state_path.read_text(encoding="utf-8")
cursor_match = re.search(r"last_processed_date:\s*(\d{4}-\d{2}-\d{2})", state)
cursor = date.fromisoformat(cursor_match.group(1)) if cursor_match else date.min
current = None
corrections = defaultdict(list)
obsolete = []
for raw in progress_path.read_text(encoding="utf-8").splitlines():
    heading = re.match(r"^###\s+(\S+)", raw)
    if heading:
        stamp = heading.group(1)
        try:
            parsed = date.fromisoformat(stamp[:10])
        except ValueError:
            try:
                parsed = date(int(stamp[:4]), int(stamp[4:6]), int(stamp[6:8]))
            except (ValueError, IndexError):
                parsed = None
        current = (stamp, parsed) if parsed else None
        continue
    if not current or current[1] <= cursor:
        continue
    correction = re.match(r"^-\s*correction:\s*(.+)$", raw)
    if correction:
        corrections[correction.group(1).strip()].append(current[0])
    obsolete_match = re.match(r"^-\s*obsolete_rule:\s*(.+)$", raw)
    if obsolete_match:
        obsolete.append((current[0], obsolete_match.group(1).strip()))

repeated = [(text, runs) for text, runs in corrections.items() if len(runs) >= 2]
if not repeated:
    (out_dir / "dreaming-report.md").write_text(
        "# Dreaming report\n\nNo repeated correction had two newer dated citations. No rules proposal was created.\n",
        encoding="utf-8")
    status = "no-repeated-evidence"
else:
    correction, runs = sorted(repeated, key=lambda item: (-len(item[1]), item[0]))[0]
    evidence = ", ".join(runs)
    (out_dir / "proposed-rules-change.md").write_text(
        "# Proposed rules change\n\n## Evidence\n"
        f"- Repeated correction: `{correction}`\n"
        f"- Cited run dates: {evidence}\n"
        f"- Frequency: {len(runs)} occurrences since {cursor.isoformat()}\n\n"
        "## Smallest change\n"
        f"Add a rule requiring the loop to address `{correction}` before publishing its result.\n\n"
        "This is a proposal only; no rules file was edited by the dreaming loop.\n",
        encoding="utf-8")
    deletion = obsolete[0] if obsolete else (runs[0], "a rule with no recent run evidence")
    (out_dir / "proposed-deletion.md").write_text(
        "# Proposed deletion\n\n"
        f"- Source date: {deletion[0]}\n"
        f"- Candidate: `{deletion[1]}`\n"
        "- Reason: no recent run needed this rule; remove only after human review.\n",
        encoding="utf-8")
    (out_dir / "dreaming-report.md").write_text(
        "# Dreaming report\n\n"
        f"- repeated_correction: `{correction}`\n"
        f"- cited_runs: {evidence}\n"
        f"- frequency: {len(runs)}\n"
        "- proposal: proposed-rules-change.md\n"
        "- deletion: proposed-deletion.md\n"
        "- rules_changed_directly: no\n",
        encoding="utf-8")
    status = "proposal-ready"

new_state = re.sub(r"last_processed_date:\s*\d{4}-\d{2}-\d{2}", f"last_processed_date: {date.today().isoformat()}", state)
new_state = re.sub(r"last_run:\s*.*", f"last_run: {run_id}", new_state)
new_state = re.sub(r"last_proposal:\s*.*", f"last_proposal: {status}", new_state)
new_state = re.sub(r"status:\s*.*", f"status: {status}", new_state)
(out_dir / "dreaming-state.md").write_text(new_state, encoding="utf-8")
print(f"dreaming_status={status}")
print(f"run_id={run_id}")
print(f"cursor={cursor.isoformat()}")
print(f"repeated_patterns={len(repeated)}")
PY
