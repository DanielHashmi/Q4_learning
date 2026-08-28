#!/usr/bin/env python3
"""Validate the reversible resolution result and the same-name trap."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
forms = json.loads((ROOT / "surface_forms.json").read_text(encoding="utf-8"))
result = json.loads((ROOT / "resolved.json").read_text(encoding="utf-8"))
errors = []
if len(forms) != 22:
    errors.append(f"expected 22 forms (20 corpus forms plus two trap forms), found {len(forms)}")
aliases = [alias for cluster in result.get("clusters", []) for alias in cluster.get("aliases", [])]
if aliases and all(isinstance(alias, int) for alias in aliases):
    if sorted(aliases) != list(range(len(forms))):
        errors.append("every input index must appear exactly once")
    else:
        for cluster in result["clusters"]:
            cluster["aliases"] = [forms[index] for index in cluster["aliases"]]
elif len(aliases) != len(forms):
    errors.append("every input form must appear in exactly one cluster")
for cluster in result.get("clusters", []):
    if not cluster.get("canonical_id") or not cluster.get("rationale"):
        errors.append("every cluster needs an ID and rationale")
    if not 0 <= cluster.get("confidence", -1) <= 1:
        errors.append(f"invalid confidence in {cluster}")
    for alias in cluster.get("aliases", []):
        if not alias.get("surface_form") or not alias.get("source"):
            errors.append(f"alias lost its receipt: {alias}")
reviews = [cluster for cluster in result["clusters"] if any(alias["surface_form"] == "review" for alias in cluster["aliases"])]
if len(reviews) != 2:
    errors.append(f"same-name trap must remain two clusters, found {len(reviews)}")
if any(len(cluster["aliases"]) > 1 and any(alias["surface_form"] == "review" for alias in cluster["aliases"]) for cluster in reviews):
    errors.append("the ambiguous review mentions must not be merged")
if errors:
    print("Project 5 resolution validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print(f"Project 5 resolution valid: {len(forms)} forms, {len(result['clusters'])} clusters")
print("Same-name trap preserved: automated review and human review remain separate")
