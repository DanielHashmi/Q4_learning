#!/usr/bin/env python3
"""Validate the capstone graph contract, watcher, and two-run proof."""
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).parent
demo = subprocess.run([sys.executable, str(ROOT / "demo.py")], text=True, capture_output=True, check=False)
if demo.returncode:
    print(demo.stdout + demo.stderr)
    raise SystemExit(1)
metrics = ROOT / "runtime-metrics.json"
result = subprocess.run([sys.executable, str(ROOT / "watcher.py"), "--metrics", str(metrics)], text=True, capture_output=True, check=False)
if result.returncode:
    print(result.stdout + result.stderr)
    raise SystemExit(1)
data = json.loads(metrics.read_text(encoding="utf-8"))
if data["triage_claims_written"] < 1 or data["counter_metric"] != "review_revise_count":
    raise SystemExit("invalid capstone counter metric")
two_run = subprocess.run([sys.executable, str(ROOT / "two_run_demo.py")], text=True, capture_output=True, check=False)
if two_run.returncode:
    print(two_run.stdout + two_run.stderr)
    raise SystemExit(1)
proof = json.loads((ROOT / "two-run-result.json").read_text(encoding="utf-8"))
if proof["verdict"] != "PASS" or proof["source_checkout_available_in_second_run"]:
    raise SystemExit("two-run memory proof failed")
print("Project 8 validation passed: watcher and separated memory-only second run")
