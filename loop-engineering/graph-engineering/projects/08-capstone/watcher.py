#!/usr/bin/env python3
"""Counter-metric watcher for the capstone's triage throughput."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--metrics", type=Path, required=True)
args = parser.parse_args()
metrics = json.loads(args.metrics.read_text(encoding="utf-8"))
required = {"triage_claims_written", "review_revise_count", "counter_metric", "watcher"}
missing = required - metrics.keys()
if missing or metrics.get("counter_metric") != "review_revise_count" or not metrics.get("watcher"):
    print(f"COUNTER WATCHER REVISE: missing or invalid metric wiring: {sorted(missing)}")
    raise SystemExit(1)
print(f"COUNTER WATCHER PASS: triage throughput={metrics['triage_claims_written']}; review revise count={metrics['review_revise_count']}")
