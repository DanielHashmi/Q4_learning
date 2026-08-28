#!/usr/bin/env python3
"""Wire the reviewer into five beats of the existing Project 3 loop.

The existing unattended TODO loop is copied to a throwaway directory so its
real shell command and spine mutate safely. Each beat captures its loop log,
then the grounded reviewer checks the maker report against graph claims.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from reviewer import load_claims, review  # noqa: E402


def command(args: list[str], cwd: Path) -> tuple[str, int]:
    try:
        result = subprocess.run(
            args, cwd=cwd, text=True, capture_output=True, check=False, timeout=180
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return output + "\nERROR: loop timed out after 180 seconds\n", 124


with tempfile.TemporaryDirectory(prefix="grounded-loop-") as directory:
    repo = Path(directory)
    existing_loop = ROOT.parents[2] / "projects" / "03-unattended-schedule"
    for name in ("loop.sh", "progress.md", "task.js", "utils.ts"):
        shutil.copy2(existing_loop / name, repo / name)
    claims = load_claims()
    verdicts = []
    for number in range(1, 6):
        _, exit_code = command(["bash", "loop.sh"], repo)
        evidence = (repo / "loop.log").read_text(encoding="utf-8")
        if number == 1:
            report = {"facts":[{"text":"task.js records an error-handling TODO","claim_id":"claim_task_error_handling_todo"}]}
        elif number == 2:
            report = {"facts":[{"text":"retries are fixed","claim_id":"missing_fix_claim"}], "next_attempt":{"action":"withdraw"}}
        elif number == 3:
            report = {"facts":[{"text":"the system is always safe","claim_id":"claim_inference_example"}], "next_attempt":{"action":"withdraw"}}
        elif number == 4:
            report = {"facts":[{"text":"the loop's source task has an error-handling TODO","claim_id":"claim_task_error_handling_todo"}]}
        else:
            report = {"facts":[], "withdrawn":["unverified deployment success"]}
        verdict = review(report, claims)
        record = {"beat":number,"tool_exit_code":exit_code,"tool_output_bytes":len(evidence),"report":report,"verdict":verdict}
        if verdict["verdict"] == "REVISE":
            # This is the maker's actual next attempt: it consumes the
            # checker feedback and withdraws the unsupported statement.
            next_report = {"facts": [], "withdrawn": [fact["text"] for fact in report.get("facts", [])]}
            record["next_attempt"] = {"report": next_report, "verdict": review(next_report, claims)}
        verdicts.append(record)

(ROOT / "real-verdicts.json").write_text(json.dumps(verdicts, indent=2) + "\n", encoding="utf-8")
print(f"Ran {len(verdicts)} real tool-backed grounded beats")
print(f"REVISE verdicts: {sum(item['verdict']['verdict'] == 'REVISE' for item in verdicts)}")
