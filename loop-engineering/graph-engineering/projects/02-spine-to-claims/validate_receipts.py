#!/usr/bin/env python3
"""Validate claims and resolve source paths from either local graph root."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
claims = json.loads((ROOT / "claims.json").read_text(encoding="utf-8"))
required = {"id", "subject", "predicate", "object", "confidence", "source", "produced_by", "created"}
errors = []
ids = [c.get("id") for c in claims]
if len(claims) != 10:
    errors.append(f"expected ten claims, found {len(claims)}")
if len(ids) != len(set(ids)):
    errors.append("claim IDs must be unique")
for claim in claims:
    missing = required - claim.keys()
    if missing:
        errors.append(f"{claim.get('id')}: missing {sorted(missing)}")
    confidence = claim.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append(f"{claim.get('id')}: invalid confidence")
    source = claim.get("source", {})
    if source.get("kind") == "inference":
        continue
    if source.get("kind") != "file" or not source.get("path") or not isinstance(source.get("line"), int):
        errors.append(f"{claim.get('id')}: malformed file source")
    elif not any((base / source["path"]).resolve().is_file() for base in (ROOT, ROOT / "..")):
        errors.append(f"{claim.get('id')}: source file does not exist: {source['path']}")
if errors:
    print("Project 2 claim validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
inferences = sum(c["source"]["kind"] == "inference" for c in claims)
print(f"Project 2 claims valid: {len(claims)} claims")
print(f"Inference baseline: {inferences}/{len(claims)} claims")
