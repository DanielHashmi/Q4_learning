#!/usr/bin/env python3
"""Run Project 5's required before/after trap experiment."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("offline", "opencode"), default="opencode")
args = parser.parse_args()

before = ROOT / "surface_forms_before_trap.json"
if not before.exists():
    subprocess.run([sys.executable, str(ROOT / "prepare_forms.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "resolve.py"), "--mode", args.mode,
                "--input", str(before), "--output", str(ROOT / "resolved-before-trap.json")], check=True)
subprocess.run([sys.executable, str(ROOT / "resolve.py"), "--mode", args.mode], check=True)
subprocess.run([sys.executable, str(ROOT / "validate.py")], check=True)
result = json.loads((ROOT / "resolved.json").read_text(encoding="utf-8"))
reviews = [cluster for cluster in result["clusters"] if any(
    alias["surface_form"] == "review" for alias in cluster["aliases"])]
if len(reviews) != 2:
    raise SystemExit(f"trap failed: expected two separate review clusters, found {len(reviews)}")
print("Trap experiment passed: the two same-name review entities remain separate")
