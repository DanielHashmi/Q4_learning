#!/usr/bin/env python3
"""Run five concrete maker/checker beats and preserve every verdict."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from reviewer import load_claims, review  # noqa: E402

claims = load_claims()
beats = [
    {"beat":"beat-1", "maker":"reports a TODO with a source claim", "report":{"facts":[{"text":"task.js has an error-handling TODO","claim_id":"claim_task_error_handling_todo"}]}},
    {"beat":"beat-2", "maker":"claims a timezone fix without graph support", "report":{"facts":[{"text":"timezone handling is fixed","claim_id":"claim_missing_timezone_fix"}], "next_attempt":{"action":"withdraw", "reason":"no source-backed claim existed"}}},
    {"beat":"beat-3", "maker":"cites an inference as if it were evidence", "report":{"facts":[{"text":"the daily loop is always safe","claim_id":"claim_inference_example"}], "next_attempt":{"action":"withdraw", "reason":"inference cannot ground a factual statement"}}},
    {"beat":"beat-4", "maker":"reports two source-backed facts", "report":{"facts":[{"text":"task.js has an error-handling TODO","claim_id":"claim_task_error_handling_todo"},{"text":"the daily loop has a human gate","claim_id":"claim_daily_human_gate"}]}},
    {"beat":"beat-5", "maker":"removes an unsupported assertion after revision", "report":{"facts":[], "withdrawn":["unverified deployment success"]}},
]
verdicts = []
for beat in beats:
    verdict = review(beat["report"], claims)
    verdicts.append({"beat":beat["beat"], "maker":beat["maker"], "verdict":verdict, "next_attempt":beat["report"].get("next_attempt"), "withdrawn":beat["report"].get("withdrawn", [])})
(Path(__file__).parent / "verdicts.json").write_text(json.dumps(verdicts, indent=2) + "\n", encoding="utf-8")
print(f"Ran {len(verdicts)} grounded reviewer beats")
print(f"REVISE verdicts: {sum(item['verdict']['verdict'] == 'REVISE' for item in verdicts)}")
