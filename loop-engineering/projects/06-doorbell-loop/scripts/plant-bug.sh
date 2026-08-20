#!/usr/bin/env bash
set -Eeuo pipefail

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
python3 - "$project_dir/src/range.js" <<'PY'
from pathlib import Path
import sys

file = Path(sys.argv[1])
text = file.read_text()
fixed = "return items.slice(0, count);"
buggy = "return items.slice(0, count + 1);"
if fixed not in text:
    raise SystemExit("fixed implementation was not found")
file.write_text(text.replace(fixed, buggy, 1))
PY
echo "planted off-by-one bug in src/range.js"
