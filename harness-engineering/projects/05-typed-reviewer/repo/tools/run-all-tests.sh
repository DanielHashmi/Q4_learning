#!/bin/sh
export JQ_BIN="/c/Users/kk/Desktop/Q4_learning/harness-engineering/projects/_tools/jq.exe"
cd "$(dirname "$0")/.."

echo "=== TEST A: well-formed PASS ==="
echo '{"verdict":"PASS","reasons":[],"risk":"low"}' | sh tools/validate-verdict.sh
echo "exit code: $?"
echo

echo "=== TEST B: well-formed FAIL ==="
echo '{"verdict":"FAIL","reasons":["test deleted, not fixed"],"risk":"high"}' | sh tools/validate-verdict.sh
echo "exit code: $?"
echo

echo "=== TEST C: well-formed but invalid verdict (MAYBE) ==="
echo '{"verdict":"MAYBE","reasons":[],"risk":"low"}' | sh tools/validate-verdict.sh
echo "exit code: $?"
echo

echo "=== TEST D: non-JSON free text ==="
echo 'This mostly passes, though I have some doubts about the edge cases...' | sh tools/validate-verdict.sh
echo "exit code: $?"
