#!/usr/bin/env python3
"""Changelog loop that reads only bounded graph context, not triage output."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from context import build

parser = argparse.ArgumentParser()
parser.add_argument("--graph", type=Path, required=True)
parser.add_argument("--claim", required=True)
args = parser.parse_args()
context = build(args.graph, args.claim)
claim = context["claim"]
line = {"text":f"{claim['subject']} {claim['predicate']} {claim['object']} ({claim.get('description','change')})","grounded_in":[claim["id"]],"context_hops":["claim","run","evidence"]}
print(json.dumps(line, indent=2))
