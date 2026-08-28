#!/usr/bin/env python3
"""Run extraction and then produce the semantic alias report."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("offline", "opencode"), default="offline")
args = parser.parse_args()
subprocess.run([sys.executable, str(ROOT / "extract.py"), "--mode", args.mode], check=True)
subprocess.run([sys.executable, str(ROOT / "normalize_duplicates.py")], check=True)
