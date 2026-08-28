#!/usr/bin/env python3
"""Grounded reviewer for changelog outputs and the counter-metric."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from context import build

def review(graph: Path, changelog: dict) -> dict:
    grounded = []
    missing = []
    for claim_id in changelog.get("grounded_in", []):
        try: context = build(graph, claim_id)
        except (StopIteration, FileNotFoundError): missing.append(claim_id); continue
        if context["claim"].get("source", {}).get("kind") != "tool_output": missing.append(claim_id)
        else: grounded.append(claim_id)
    return {"verdict":"PASS" if not missing else "REVISE","grounded_in":grounded,"missing":missing,"rubric":"capstone-grounded-v1"}
