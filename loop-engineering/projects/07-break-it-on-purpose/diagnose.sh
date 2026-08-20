#!/usr/bin/env bash
set -Eeuo pipefail
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
[[ -s "$dir/run.log" && -s "$dir/progress.md" && -s "$dir/cost.json" ]] || exit 1
python3 - "$dir/cost.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); expected=(d['input_tokens']+d['output_tokens'])*d['runs_per_week']*52//12
assert d['monthly_tokens']==expected
print(f"monthly_tokens={d['monthly_tokens']} monthly_cost_usd={d['monthly_cost_usd']}")
PY
tail -n 1 "$dir/run.log" | grep -Fq 'status=FAIL'
grep -Fq 'status: needs a human' "$dir/progress.md"
printf 'diagnosis: '; tail -n 1 "$dir/run.log"
echo 'diagnosis_source: run.log + progress.md + cost.json only'
