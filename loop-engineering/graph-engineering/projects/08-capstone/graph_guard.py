#!/usr/bin/env python3
"""Frozen-node graph guard for required fields and append-only history."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(graph: Path, repo: Path | None = None) -> list[str]:
    errors = []
    claims = read_json(graph / "claims.json")
    runs = read_json(graph / "runs.json")
    claim_ids = [claim.get("id") for claim in claims]
    run_ids = [run.get("id") for run in runs]
    if len(claim_ids) != len(set(claim_ids)): errors.append("duplicate claim ID")
    if len(run_ids) != len(set(run_ids)): errors.append("duplicate run ID")
    required = {"id", "subject", "predicate", "object", "source", "produced_by", "created"}
    for claim in claims:
        if not required.issubset(claim): errors.append(f"claim {claim.get('id')} is missing required fields")
        if claim.get("source", {}).get("kind") not in {"tool_output", "inference"}: errors.append(f"claim {claim.get('id')} has invalid source kind")
        if claim.get("supersedes") and claim["supersedes"] not in claim_ids: errors.append(f"claim {claim.get('id')} supersedes missing claim")
        if claim.get("produced_by") not in run_ids: errors.append(f"claim {claim.get('id')} points to missing run")
    for run in runs:
        if not {"id", "kind", "evidence", "claim_ids", "result", "version"}.issubset(run): errors.append(f"run {run.get('id')} is missing required fields")
        if not (graph.parent / run.get("evidence", "")).is_file(): errors.append(f"run {run.get('id')} points to missing evidence")
        if not set(run.get("claim_ids", [])).issubset(set(claim_ids)): errors.append(f"run {run.get('id')} points to missing claim")
    if repo is not None:
        old = subprocess.run(["git", "show", f"HEAD:{graph.relative_to(repo).as_posix()}/claims.json"], cwd=repo, text=True, capture_output=True, check=False)
        if old.returncode == 0 and claims[:len(previous := json.loads(old.stdout))] != previous: errors.append("claims.json is not append-only")
    return errors

parser = argparse.ArgumentParser()
parser.add_argument("--graph", type=Path, required=True)
parser.add_argument("--repo", type=Path)
args = parser.parse_args()
errors = validate(args.graph.resolve(), args.repo.resolve() if args.repo else None)
if errors:
    print("GRAPH GUARD FAILED")
    for error in errors: print(f"- {error}")
    raise SystemExit(1)
print("GRAPH GUARD PASSED")
