#!/usr/bin/env python3
"""Report entity and relation metrics together for the active prediction."""
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from score import score
entity = score()
relation_output = subprocess.run([sys.executable, str(ROOT / "score_relations.py")], text=True, capture_output=True, check=True)
print(json.dumps({"entities":entity,"relations":json.loads(relation_output.stdout)}, indent=2))
