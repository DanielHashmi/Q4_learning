#!/usr/bin/env python3
"""End-to-end capstone in a fresh throwaway Git repository."""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent

def run(args, cwd, env=None, check=True):
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=check)

with tempfile.TemporaryDirectory(prefix="graph-capstone-") as temp:
    repo = Path(temp)
    env = os.environ.copy()
    env.update({"GIT_AUTHOR_NAME":"Capstone Test","GIT_AUTHOR_EMAIL":"capstone@example.invalid","GIT_COMMITTER_NAME":"Capstone Test","GIT_COMMITTER_EMAIL":"capstone@example.invalid"})
    run(["git","init","-q"], repo, env)
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.write_text(f'#!/bin/sh\n"{os.sys.executable}" "{ROOT / "graph_guard.py"}" --graph graph --repo .\n', encoding="utf-8")
    hook.chmod(0o755)
    graph = repo / "graph"; evidence = repo / "evidence"; graph.mkdir(); evidence.mkdir()
    for name in ("entities.json", "claims.json", "runs.json"): shutil.copy(ROOT / "graph" / name, graph / name)
    source = repo / "service.py"; source.write_text("# TODO: handle retries\n", encoding="utf-8")
    run(["git","add","."], repo, env); run(["git","commit","-qm","test: seed issue"], repo, env)
    source.write_text("def retry():\n    return True\n", encoding="utf-8")
    run(["git","add","service.py"], repo, env); run(["git","commit","-qm","fix: handle retries"], repo, env)
    run_id = "run_capstone_triage_001"
    run(["python3", str(ROOT / "triage.py"), "--repo", str(repo), "--graph", str(graph), "--evidence", str(evidence), "--run-id", run_id], repo, env)
    run(["git","add","graph","evidence"], repo, env); run(["git","commit","-qm","graph: record grounded fix"], repo, env)
    claims = json.loads((graph / "claims.json").read_text(encoding="utf-8")); claim_id = claims[0]["id"]
    changelog = json.loads(run(["python3", str(ROOT / "changelog.py"), "--graph", str(graph), "--claim", claim_id], repo, env).stdout)
    import sys; sys.path.insert(0, str(ROOT))
    from reviewer import review
    verdict = review(graph, changelog)
    assert verdict["verdict"] == "PASS" and verdict["grounded_in"] == [claim_id]
    claims[0]["description"] = "tampered after commit"
    (graph / "claims.json").write_text(json.dumps(claims, indent=2) + "\n", encoding="utf-8")
    run(["git", "add", "graph/claims.json"], repo, env)
    tamper = run(["git", "commit", "-qm", "should be blocked"], repo, env, check=False)
    assert tamper.returncode != 0
    metrics = {"triage_claims_written": len(claims),
               "review_passes": int(verdict["verdict"] == "PASS"),
               "review_revise_count": int(verdict["verdict"] == "REVISE"),
               "counter_metric": "review_revise_count", "watcher": "changelog-review-loop"}
    result = {"repo":str(repo),"changelog":changelog,"verdict":verdict,"tamper_rejected":True,"metrics":metrics}
    (ROOT / "runtime-metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
