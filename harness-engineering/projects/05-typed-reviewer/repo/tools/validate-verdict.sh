#!/bin/sh
# tools/validate-verdict.sh
# Real field-by-field validator from Concept 9, wired to the real jq.exe
# shipped in projects/_tools. Usage: echo "$json" | tools/validate-verdict.sh
#
# Exit 0  = accepted (valid PASS/FAIL verdict, in the allowed shape)
# Exit 2  = rejected / escalate to a human ("needs a human" contract)

JQ="${JQ_BIN:-jq}"

review=$(cat)

echo "$review" | "$JQ" -e '
  (.verdict == "PASS" or .verdict == "FAIL") and
  (.risk == "low" or .risk == "high") and
  (.reasons | type == "array") and all(.reasons[]; type == "string")
' >/dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "REJECTED: reviewer broke protocol — escalating to a human" >&2
  echo "- reviewer output unparseable: needs a human" >&2
  exit 2
fi

verdict=$(echo "$review" | "$JQ" -r '.verdict')
echo "ACCEPTED: verdict=$verdict"
exit 0
