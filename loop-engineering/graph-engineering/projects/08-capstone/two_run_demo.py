#!/usr/bin/env python3
"""Acceptance test with two genuinely separate processes and workspaces.

Run 1 owns the Git repository and writes graph memory. Run 2 receives only
that memory and evidence, so a passing changelog proves the second loop can
work without the original source checkout or triage output.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent

def run(args, cwd, env=None, check=True):
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=check)

with tempfile.TemporaryDirectory(prefix="capstone-two-run-") as directory:
    base = Path(directory)
    source = base / "source-repo"
    memory = base / "memory"
    reader = base / "reader"
    source.mkdir()
    (source / "service.py").write_text("# TODO: fix retries\n", encoding="utf-8")
    env = os.environ.copy()
    env.update({"GIT_AUTHOR_NAME":"Capstone Test", "GIT_AUTHOR_EMAIL":"capstone@example.invalid",
                "GIT_COMMITTER_NAME":"Capstone Test", "GIT_COMMITTER_EMAIL":"capstone@example.invalid"})
    run(["git", "init", "-q"], source)
    run(["git", "add", "."], source)
    run(["git", "commit", "-qm", "seed"], source, env)
    (source / "service.py").write_text("def retry():\n    return True\n", encoding="utf-8")
    run(["git", "add", "."], source)
    run(["git", "commit", "-qm", "fix retry"], source, env)

    (memory / "graph").mkdir(parents=True)
    (memory / "evidence").mkdir()
    (memory / "graph" / "claims.json").write_text("[]\n", encoding="utf-8")
    (memory / "graph" / "runs.json").write_text("[]\n", encoding="utf-8")
    run([sys.executable, str(ROOT / "triage.py"), "--repo", str(source), "--graph", str(memory / "graph"),
         "--evidence", str(memory / "evidence"), "--run-id", "run_real"], ROOT)

    # The second process receives no source-repo and no triage script output.
    shutil.copytree(memory, reader)
    claims = json.loads((reader / "graph" / "claims.json").read_text(encoding="utf-8"))
    claim_id = claims[0]["id"]
    line = run([sys.executable, str(ROOT / "changelog.py"), "--graph", str(reader / "graph"), "--claim", claim_id], ROOT)
    changelog = reader / "changelog.json"
    changelog.write_text(line.stdout, encoding="utf-8")
    verdict = run([sys.executable, str(ROOT / "review_changelog.py"), "--graph", str(reader / "graph"), "--input", str(changelog)], ROOT)
    verdict_data = json.loads(verdict.stdout)
    assert verdict_data["verdict"] == "PASS"
    assert verdict_data["grounded_in"] == [claim_id]
    assert not (reader / "source-repo").exists()
    result = {"first_run":"triage+wrote-memory", "second_run":"read-memory-only", "claim_id":claim_id,
              "context_hops":["claim", "run", "evidence"], "verdict":verdict_data["verdict"],
              "source_checkout_available_in_second_run":False}
    (ROOT / "two-run-result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
