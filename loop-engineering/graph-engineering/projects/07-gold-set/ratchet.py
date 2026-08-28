#!/usr/bin/env python3
"""Run three one-line prompt experiments and keep/revert by measured F1."""
import json
import shutil
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from score import score  # noqa: E402

ROOT = Path(__file__).parent
history = []
current = 1
parser_mode = sys.argv[1] if len(sys.argv) > 1 else "offline"
if parser_mode not in {"offline", "opencode"}:
    raise SystemExit("usage: ratchet.py [offline|opencode]")
def run_version(version: int) -> tuple[dict, str]:
    output = f"predictions-v{version}.json"
    subprocess.run([sys.executable, str(ROOT / "predict.py"), "--version", str(version),
                    "--mode", parser_mode, "--output", output], check=True)
    return score(output), output

baseline, baseline_file = run_version(1)
current_metrics = baseline
history.append({"attempt":0,"prompt_version":1,"decision":"baseline","metrics":baseline,
                "prediction_file":baseline_file,"mode":parser_mode})
for attempt, candidate in enumerate((2,3,4), 1):
    metrics, prediction_file = run_version(candidate)
    if metrics["f1"] > current_metrics["f1"]:
        decision = "keep"
        current = candidate
        current_metrics = metrics
    else:
        decision = "revert"
    history.append({"attempt":attempt,"prompt_version":candidate,"decision":decision,"metrics":metrics,
                    "active_version":current,"prediction_file":prediction_file,"mode":parser_mode})
shutil.copyfile(ROOT / f"predictions-v{current}.json", ROOT / "predictions.json")
(ROOT / "ratchet-history.json").write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
print(f"Ratchet complete: active prompt v{current}; {sum(item['decision']=='revert' for item in history)} reverted attempts")
