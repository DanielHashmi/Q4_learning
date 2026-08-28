#!/usr/bin/env python3
"""Pure grounded-review function used by the five-beat rehearsal."""
from __future__ import annotations

import json
from pathlib import Path


def active_claims(claims: list[dict]) -> dict[str, dict]:
    superseded = {claim["supersedes"] for claim in claims if claim.get("supersedes")}
    return {claim["id"]: claim for claim in claims if claim["id"] not in superseded}


def review(report: dict, claims: list[dict]) -> dict:
    active = active_claims(claims)
    grounded = []
    missing = []
    for fact in report.get("facts", []):
        claim_id = fact.get("claim_id")
        if not claim_id:
            missing.append(f"source-backed claim for: {fact.get('text', 'unnamed factual statement')}")
            continue
        claim = active.get(claim_id)
        if claim is None:
            missing.append(f"active claim {claim_id} for: {fact.get('text', 'unnamed factual statement')}")
        elif claim.get("source", {}).get("kind") == "inference":
            missing.append(f"non-inference evidence for: {fact.get('text', 'unnamed factual statement')}")
        else:
            grounded.append(claim_id)
    return {
        "verdict": "PASS" if not missing else "REVISE",
        "grounded_in": grounded,
        "missing": missing,
        "rubric": "grounded-reviewer-v1",
    }


def load_claims() -> list[dict]:
    return json.loads((Path(__file__).parent / "graph" / "claims.json").read_text(encoding="utf-8"))
