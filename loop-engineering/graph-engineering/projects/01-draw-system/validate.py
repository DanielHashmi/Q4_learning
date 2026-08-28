#!/usr/bin/env python3
"""Validate Project 1's typed governance graph using only the stdlib."""
import json
from pathlib import Path


ROOT = Path(__file__).parent
data = json.loads((ROOT / "system.json").read_text(encoding="utf-8"))
nodes = data["nodes"]
edges = data["edges"]
ids = [node["id"] for node in nodes]
errors = []

if len(ids) != len(set(ids)):
    errors.append("node IDs must be unique")
if not nodes:
    errors.append("graph must contain nodes")
if not edges:
    errors.append("graph must contain edges")

allowed_types = {"loop", "checker", "human_gate", "anchor", "memory", "finding", "metric"}
for node in nodes:
    if node.get("type") not in allowed_types:
        errors.append(f"{node.get('id')}: invalid node type")
    if not node.get("name") or not node.get("artifact"):
        errors.append(f"{node.get('id')}: name and artifact are required")

known = set(ids)
for edge in edges:
    if edge.get("from") not in known or edge.get("to") not in known:
        errors.append(f"edge has unknown endpoint: {edge}")
    if not edge.get("label"):
        errors.append(f"edge must have a label: {edge}")

observations = {item["kind"]: item for item in data.get("observations", [])}
if "transcript_only_finding" not in observations:
    errors.append("missing transcript-only finding observation")
if "unwatched_optimizing_metric" not in observations:
    errors.append("missing unwatched optimizing metric observation")

risk_ids = {node["id"] for node in nodes if node.get("risk")}
for kind, observation in observations.items():
    if observation.get("node") not in risk_ids:
        errors.append(f"observation {kind} must point to a risk node")

if errors:
    print("Project 1 graph validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"Project 1 graph valid: {len(nodes)} nodes, {len(edges)} labeled edges")
print("Observed risks: transcript-only finding; optimizing metric without a watcher")
