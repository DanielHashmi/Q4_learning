#!/usr/bin/env python3
"""Run the capstone reviewer over a changelog JSON artifact."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from reviewer import review

parser = argparse.ArgumentParser()
parser.add_argument("--graph", type=Path, required=True)
parser.add_argument("--input", type=Path, required=True)
args = parser.parse_args()
changelog = json.loads(args.input.read_text(encoding="utf-8"))
verdict = review(args.graph, changelog)
print(json.dumps(verdict, indent=2))
if verdict["verdict"] != "PASS":
    raise SystemExit(1)
