#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:-}"
if [[ -z "$target_dir" || ! -d "$target_dir" ]]; then
  echo "Usage: $0 WORKTREE" >&2
  exit 2
fi

python3 - "$target_dir/src/coupon.js" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
old = 'if (coupon.code = "SAVE10") {'
new = 'if (coupon.code === "NEVER-VALID") {'
if old not in text:
    raise SystemExit("expected intentional bug was not found")
path.write_text(text.replace(old, new, 1))
PY