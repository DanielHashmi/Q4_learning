#!/usr/bin/env python3
"""Validate every Project 3 extraction output and its duplicate report."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
output = ROOT / "output"
errors = []
all_entities = []
for source in sources:
    path = output / f"{source['document']}.json"
    if not path.is_file():
        errors.append(f"missing output: {path.name}")
        continue
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
        continue
    if data.get("document") != source["document"]:
        errors.append(f"wrong document identifier in {path.name}")
    ids = {entity.get("id") for entity in data.get("entities", [])}
    if None in ids or len(ids) != len(data.get("entities", [])):
        errors.append(f"duplicate or missing entity IDs in {path.name}")
    for entity in data.get("entities", []):
        if entity.get("type") not in {"PROJECT", "ARTIFACT", "TOOL", "PROCESS", "GATE", "MEMORY"}:
            errors.append(f"invalid entity type in {path.name}")
        source_ref = entity.get("source", {})
        if source_ref.get("document") != source["document"] or not isinstance(source_ref.get("line"), int) or source_ref["line"] < 1:
            errors.append(f"invalid entity source in {path.name}")
    for relation in data.get("relations", []):
        if relation.get("subject") not in ids or relation.get("object") not in ids:
            errors.append(f"dangling relation in {path.name}")
    all_entities.extend(data.get("entities", []))

duplicates_path = output / "duplicates.json"
if not duplicates_path.is_file():
    errors.append("missing duplicates.json")
else:
    duplicates = json.loads(duplicates_path.read_text(encoding="utf-8"))
    if not duplicates:
        errors.append("duplicate report is empty; the documents should expose at least one alias family")

if errors:
    print("Project 3 extraction validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"Project 3 extraction valid: {len(sources)} documents, {len(all_entities)} entity mentions")
print(f"Duplicate report: {len(duplicates)} concept families")
