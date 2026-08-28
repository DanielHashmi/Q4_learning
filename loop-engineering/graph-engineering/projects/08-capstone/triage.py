#!/usr/bin/env python3
"""Triage loop: capture Git output and append a source-backed claim."""
from __future__ import annotations
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def run_tool(repo: Path, args: list[str]) -> tuple[str, int]:
    result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=False)
    return result.stdout + result.stderr, result.returncode

parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, required=True)
parser.add_argument("--graph", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--run-id", required=True)
args = parser.parse_args()
args.graph.mkdir(parents=True, exist_ok=True)
args.evidence.mkdir(parents=True, exist_ok=True)
output, exit_code = run_tool(args.repo, ["show", "--format=fuller", "--stat", "--check", "HEAD"])
evidence_file = args.evidence / f"{args.run_id}.log"
evidence_file.write_text(output, encoding="utf-8")
commit = run_tool(args.repo, ["rev-parse", "HEAD"])[0].strip()
subject = run_tool(args.repo, ["show", "-s", "--format=%s", "HEAD"])[0].strip()
run = {"id":args.run_id,"kind":"triage","evidence":str(evidence_file.relative_to(args.graph.parent)).replace("\\","/"),"claim_ids":[f"claim_{args.run_id}_fix"],"result":"PASS" if exit_code == 0 else "FAIL","version":"triage-v1"}
claims = json.loads((args.graph / "claims.json").read_text(encoding="utf-8"))
claims.append({"id":f"claim_{args.run_id}_fix","subject":"latest_change","predicate":"fixed_by","object":commit,"confidence":0.98,"source":{"kind":"tool_output","command":"git show --format=fuller --stat --check HEAD","exit_code":exit_code,"ref":str(evidence_file.relative_to(args.graph.parent)).replace("\\","/")},"produced_by":args.run_id,"created":datetime.now(timezone.utc).date().isoformat(),"description":subject})
runs = json.loads((args.graph / "runs.json").read_text(encoding="utf-8"))
runs.append(run)
(args.graph / "claims.json").write_text(json.dumps(claims, indent=2) + "\n", encoding="utf-8")
(args.graph / "runs.json").write_text(json.dumps(runs, indent=2) + "\n", encoding="utf-8")
print(f"Triage wrote claim {claims[-1]['id']} from captured Git output")
