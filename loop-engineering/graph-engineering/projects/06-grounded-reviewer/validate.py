#!/usr/bin/env python3
"""Validate the grounded-reviewer contract and five-beat evidence.

Use ``--run-real`` when a fresh provider-backed rehearsal is wanted. The
default validates the last recorded rehearsal without invoking a provider.
"""
import json
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument("--run-real", action="store_true")
args = parser.parse_args()
if args.run_real:
    real_loop = subprocess.run([sys.executable, str(ROOT / "real_loop.py")], text=True, capture_output=True, check=False)
    if real_loop.returncode:
        print(real_loop.stdout + real_loop.stderr)
        raise SystemExit(1)
claims = json.loads((ROOT / "graph" / "claims.json").read_text(encoding="utf-8"))
claim_ids = {claim["id"] for claim in claims}
inference_ids = {claim["id"] for claim in claims if claim.get("source", {}).get("kind") == "inference"}
verdicts = json.loads((ROOT / "real-verdicts.json").read_text(encoding="utf-8"))
errors = []
if len(verdicts) != 5:
    errors.append(f"expected five beats, found {len(verdicts)}")
if not any(item["verdict"]["verdict"] == "REVISE" and item["verdict"]["missing"] for item in verdicts):
    errors.append("at least one REVISE verdict must name missing evidence")
for item in verdicts:
    verdict = item["verdict"]
    if verdict.get("rubric") != "grounded-reviewer-v1":
        errors.append(f"missing rubric in {item['beat']}")
    if not set(verdict.get("grounded_in", [])).issubset(claim_ids):
        errors.append(f"unresolvable grounded claim in {item['beat']}")
    if set(verdict.get("grounded_in", [])) & inference_ids:
        errors.append(f"inference claim grounded in {item['beat']}")
for item in verdicts:
    if item["verdict"]["verdict"] == "REVISE":
        next_attempt = item.get("next_attempt", {})
        if not next_attempt.get("report", {}).get("withdrawn") or next_attempt.get("verdict", {}).get("verdict") != "PASS":
            errors.append(f"{item['beat']} did not show evidence or withdrawal after REVISE")
if errors:
    print("Project 6 grounded-review validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print("Project 6 grounded-review validation passed: five beats, missing-edge REVISE, inference blocked")
