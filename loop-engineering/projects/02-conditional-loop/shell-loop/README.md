# Shell-Enforced Hard Cap

## What This Is

A conditional loop where **the shell guarantees the iteration limit**, not the agent. This pattern works with ANY agent that has a CLI - Claude Code, OpenCode, or any other.

## The Key Difference

**Soft cap** (via `/goal`): You *ask* the agent to stop after N attempts  
**Hard cap** (this folder): The shell *guarantees* max N attempts

## The Pattern (Tool-Agnostic)

```bash
for attempt in $(seq 1 $MAX_ATTEMPTS); do
  # 1. Run the checker command
  if npm test; then
    exit 0  # Success - stop
  fi
  
  # 2. Hit the cap?
  if [ $attempt -eq $MAX_ATTEMPTS ]; then
    exit 1  # Failure - stop
  fi
  
  # 3. Agent fixes bugs
  $AGENT_CLI "fix the bugs..."
done
```

**The shell counts. The shell stops. Not the agent.**

## How to Use

### Step 1: Choose Your Agent CLI

Edit `loop.sh` and uncomment the agent you have:

```bash
# For Claude Code:
AGENT_CMD='claude -p'

# For OpenCode:
AGENT_CMD='opencode run'

# For any other agent with a CLI:
AGENT_CMD='your-agent-command'
```

### Step 2: Run It

```bash
bash loop.sh
```

## Why This Matters

### Soft Cap (via `/goal`)
```bash
/goal Fix bugs until tests pass. Stop after 6 attempts.
```

- ✅ Simplest to use
- ✅ No shell scripting needed
- ⚠️  Agent might not respect the limit
- ⚠️  Context compaction might lose count

### Hard Cap (this approach)
```bash
for i in $(seq 1 6); do
  if npm test; then break; fi
  $AGENT_CLI "fix bugs"
done
```

- ✅ **Guaranteed** maximum attempts
- ✅ Shell handles the counting
- ✅ Works with any agent CLI
- ⚠️  Requires basic shell scripting

## The Real Lesson

The **pattern** is what matters: conditional loop with command-based stop condition and capped iterations.

The **implementation** varies by tool, but the shape is identical:
1. Checker command decides success (exit code 0)
2. Agent makes fixes when checker fails
3. Loop has a hard limit (never infinite)

## Agent CLI Requirements

Your agent CLI needs to support **single-prompt execution** (non-interactive mode):

- **Claude Code**: `claude -p "prompt"` ✓
- **OpenCode**: `opencode run "prompt"` ✓
- **ChatGPT CLI**: Would work if it has single-prompt mode
- **Custom agents**: Any CLI that takes a prompt and exits after completion

If your agent doesn't have this, you can only use the `/goal` approach (soft cap).

## From the Loop Engineering Doc

This implements the pattern from Concept 5 (Conditional Loop):

> "For a smarter check, run a second `opencode run` with a dedicated review agent and have *it* print `PASS` or `FAIL`. Always cap the tries. A loop that retries with no limit is how token bills grow out of control."

The doc shows OpenCode as an example, but the principle applies to any agent CLI.
