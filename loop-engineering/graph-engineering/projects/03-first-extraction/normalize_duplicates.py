#!/usr/bin/env python3
"""Build the Project 3 alias report without merging entity mentions."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT = ROOT / "output"
ALIAS_FAMILIES = {
    "memory_spine": {"progress.md", "spine", "committed spine"},
    "opencode_tool": {"OpenCode", "OpenCode CLI"},
    "human_approval": {"human gate", "human review and merge"},
}

mentions = []
for path in sorted(OUTPUT.glob("project-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    for entity in data["entities"]:
        mentions.append({"document": data["document"], "surface_form": entity["surface_form"], "id": entity["id"], "type": entity["type"]})

duplicates = []
for concept, forms in ALIAS_FAMILIES.items():
    matched = [mention for mention in mentions if mention["surface_form"] in forms]
    distinct = {mention["surface_form"].lower() for mention in matched}
    if len(distinct) > 1:
        duplicates.append({"concept": concept, "surface_forms": matched})

(OUTPUT / "duplicates.json").write_text(json.dumps(duplicates, indent=2) + "\n", encoding="utf-8")
print(f"Duplicate report: {len(duplicates)} concept families")
