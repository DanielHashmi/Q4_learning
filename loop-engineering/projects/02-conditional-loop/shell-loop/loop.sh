#!/usr/bin/env bash

# Conditional Loop with Shell-Enforced Hard Cap
#
# This pattern works with ANY agent that has a CLI:
# - Claude Code: use 'claude -p "prompt"'
# - OpenCode: use 'opencode run "prompt"'
# - Any other agent CLI: substitute the command
#
# The KEY INSIGHT: The shell enforces the cap, not the agent.

set -e

MAX_ATTEMPTS=6
PROJECT_ROOT=".."

# Choose your agent CLI (uncomment the one you have)
# AGENT_CMD='claude -p'
AGENT_CMD='opencode run'

echo "Conditional Loop (Shell-Enforced Hard Cap)"
echo "==========================================="
echo "Agent: ${AGENT_CMD}"
echo "Max attempts: $MAX_ATTEMPTS"
echo ""

for attempt in $(seq 1 $MAX_ATTEMPTS); do
  echo "=== Attempt $attempt/$MAX_ATTEMPTS ==="
  echo ""

  # THE CHECKER: Command exit code decides
  if npm test --prefix "$PROJECT_ROOT"; then
    # STOP CONDITION MET: Tests passed
    echo ""
    echo "✓ SUCCESS: Tests passed on attempt $attempt"
    echo "Stop reason: npm test exit code = 0"
    exit 0
  fi

  # Tests failed
  echo ""
  echo "✗ Tests failed on attempt $attempt"

  # Check if we hit the cap
  if [ $attempt -eq $MAX_ATTEMPTS ]; then
    echo ""
    echo "✗ FAILURE: Hit maximum attempts"
    echo "Stop reason: Reached attempt cap ($MAX_ATTEMPTS)"
    exit 1
  fi

  # THE MAKER: Agent fixes bugs
  echo ""
  echo "Agent analyzing failures and fixing bugs..."
  echo ""

  # Single-prompt execution (no interactive session)
  $AGENT_CMD "Read the test output above. The tests in ../test.js are failing because ../math.js has bugs.

Analyze the test failures:
1. Read ../math.js to see the current implementation
2. Identify what each function is doing wrong
3. Fix the bugs in ../math.js

Only fix the bugs - don't add features or refactor."

  echo ""
  echo "Retrying tests..."
  echo ""
done
