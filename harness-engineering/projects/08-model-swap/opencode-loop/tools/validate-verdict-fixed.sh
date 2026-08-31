#!/bin/sh
# tools/validate-verdict.sh
# The FIXED, contract-coupled version (Project 8's real finding applied).
#
# Project 8 caught a real behavior-coupling bug: the original validator
# (copied from Project 5) assumed models return bare JSON. gemini-3.5-flash-lite
# does; gemini-2.5-flash wraps its reply in a ```json ... ``` markdown fence.
# Same correct verdict, different surface text — and the naive validator
# REJECTED the wrapped one, which is a false escalation, not a real protocol
# break. The fix: strip a markdown code fence if present, THEN validate the
# JSON contract itself. This makes the contract robust to a model's
# formatting habits while still rejecting genuine protocol breaks (bad
# verdict values, missing fields, actual non-JSON prose).
#
# Usage: echo "$review" | tools/validate-verdict.sh
# Exit 0 = accepted. Exit 2 = rejected / escalate to a human.

JQ="${JQ_BIN:-jq}"

raw=$(cat)

# Strip a leading/trailing ```json or ``` fence if the model added one.
# This is the ONLY model-specific-formatting concession; the JSON contract
# itself below is unchanged and unweakened.
stripped=$(printf '%s' "$raw" | sed -e '/^```/d')

echo "$stripped" | "$JQ" -e '
  (.verdict == "PASS" or .verdict == "FAIL") and
  (.risk == "low" or .risk == "high") and
  (.reasons | type == "array") and all(.reasons[]; type == "string")
' >/dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "REJECTED: reviewer broke protocol — escalating to a human" >&2
  echo "- reviewer output unparseable: needs a human" >&2
  exit 2
fi

verdict=$(echo "$stripped" | "$JQ" -r '.verdict')
echo "ACCEPTED: verdict=$verdict"
exit 0
