#!/usr/bin/env bash
set -Eeuo pipefail
mode="${1:-healthy}"
case "$mode" in healthy|sabotage) ;; *) echo "usage: $0 healthy|sabotage" >&2; exit 2 ;; esac
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
max="${MAX_ATTEMPTS:-3}"; runs="${RUNS_PER_WEEK:-5}"
[[ "$max" =~ ^[1-9][0-9]*$ && "$runs" =~ ^[1-9][0-9]*$ ]] || exit 2
stamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; in=1200; out=300
monthly=$(( (in + out) * runs * 52 / 12 ))
python3 - "$dir/cost.json" "$runs" "$in" "$out" "$monthly" <<'PY'
import json,sys
p,r,i,o,m=sys.argv[1:]
data={'cadence':'weekdays','runs_per_week':int(r),'input_tokens':int(i),'output_tokens':int(o),'price_per_million_tokens_usd':0,'monthly_tokens':int(m),'monthly_cost_usd':0}
with open(p,'w') as f: json.dump(data,f,indent=2); f.write('\n')
PY
attempt=0; reason=""
while (( attempt < max )); do
  attempt=$((attempt+1))
  [[ "$mode" == healthy ]] && break
  reason="target file missing: project-03-unattended-schedule/missing-progress-input.md"
done
if [[ -n "$reason" ]]; then
  printf '%s mode=%s status=FAIL attempts=%s/%s reason=%s\n' "$stamp" "$mode" "$attempt" "$max" "$reason" >> "$dir/run.log"
  { printf '\n### %s — FAIL\n' "$stamp"; printf -- '- status: needs a human\n- failure: %s\n- attempts: %s/%s (bounded)\n- evidence: run.log, progress.md, cost.json\n' "$reason" "$attempt" "$max"; } >> "$dir/progress.md"
  exit 1
fi
printf '%s mode=%s status=PASS attempts=%s/%s\n' "$stamp" "$mode" "$attempt" "$max" >> "$dir/run.log"
printf '\n### %s — PASS\n- status: completed\n- evidence: run.log, progress.md, cost.json\n' "$stamp" >> "$dir/progress.md"
