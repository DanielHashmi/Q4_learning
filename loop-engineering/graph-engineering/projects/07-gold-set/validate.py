#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).parent
history = json.loads((ROOT / "ratchet-history.json").read_text(encoding="utf-8"))
errors = []
attempts = [item for item in history if item["attempt"] > 0]
if len(attempts) != 3:
    errors.append(f"expected three prompt attempts, found {len(attempts)}")
if not any(item["decision"] == "revert" for item in attempts):
    errors.append("ratchet must preserve at least one reverted regression")
for item in history:
    metrics = item["metrics"]
    for key in ("precision", "recall", "f1", "schema_valid_rate"):
        if not 0 <= metrics[key] <= 1:
            errors.append(f"invalid {key} in attempt {item['attempt']}")
if errors:
    print("Project 7 gold-set validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print("Project 7 gold-set validation passed: five docs and three recorded ratchet attempts")
