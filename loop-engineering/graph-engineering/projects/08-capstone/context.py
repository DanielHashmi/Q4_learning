#!/usr/bin/env python3
"""Build bounded two-hop context: claim -> run -> raw evidence."""
import json
from pathlib import Path

def build(graph: Path, claim_id: str) -> dict:
    claims = json.loads((graph / "claims.json").read_text(encoding="utf-8"))
    runs = json.loads((graph / "runs.json").read_text(encoding="utf-8"))
    claim = next(claim for claim in claims if claim["id"] == claim_id)
    run = next(run for run in runs if run["id"] == claim["produced_by"])
    evidence = (graph.parent / run["evidence"]).read_text(encoding="utf-8")
    return {"claim":claim,"run":run,"evidence":evidence}
