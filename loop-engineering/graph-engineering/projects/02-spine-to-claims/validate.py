#!/usr/bin/env python3
"""Validate the Project 2 claim records without third-party dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
claims = json.loads((ROOT / "claims.json").read_text(encoding="utf-8"))
required = {"id", "subject", "predicate", "object", "confidence", "source", "produced_by", "created"}
errors = []
ids = [claim.get("id") for claim in claims]

if len(ids) != len(set(ids)):
    errors.append("claim IDs must be unique")
if len(claims) != 10:
    errors.append(f"expected ten claims, found {len(claims)}")

for claim in claims:
    missing = required - claim.keys()
    if missing:
        errors.append(f"{claim.get('id')}: missing {sorted(missing)}")
    if not isinstance(claim.get("confidence"), (int, float)) or not 0 <= claim["confidence"] <= 1:
        errors.append(f"{claim.get('id')}: confidence must be between 0 and 1")
    source = claim.get("source", {})
    if source.get("kind") == "inference":
        continue
    if source.get("kind") != "file" or not source.get("path") or not isinstance(source.get("line"), int):
        errors.append(f"{claim.get('id')}: file source needs path and integer line")
    elif not (ROOT / source["path"]).resolve().is_file():
        errors.append(f"{claim.get('id')}: source file does not exist: {source['path']}")

if errors:
    print("Project 2 claim validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

inferences = sum(claim["source"]["kind"] == "inference" for claim in claims)
print(f"Project 2 claims valid: {len(claims)} claims")
print(f"Inference baseline: {inferences}/{len(claims)} claims")
