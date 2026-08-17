# Project 02: Conditional Loop

**Difficulty**: Easy to Medium  
**Concepts**: Conditional loop, Maker-checker pattern  
**Approaches**: Soft cap (prompt-based) | Hard cap (shell-enforced)

## What This Is

A project to practice conditional loops where **the command decides when to stop** (not the agent).

**Core pattern:**
- `npm test` exit code 0 = success, stop
- Exit code non-zero = agent fixes bugs, continue
- Cap at 6 attempts to prevent infinite loops

## The Setup

`math.js` has 3 bugs. `test.js` has 3 tests. All tests fail initially.

**The bugs:**
1. `add(a, b)` - uses subtraction instead of addition
2. `multiply(a, b)` - missing return statement  
3. `isEven(n)` - logic is inverted

## How to Run

### Approach 1: Soft Cap (Simplest)

**Uses:** Claude Code's `/goal` command  
**Cap enforcement:** In the prompt text (you ask Claude to count and stop)

```bash
# Verify tests fail
npm test

# Run the loop
/goal Fix bugs until tests pass. Run npm test. If it fails, read the output, identify what's wrong in math.js, fix the bugs, then run npm test again. Stop when npm test exits with code 0 or after 6 attempts.
```

**Pros:**
- Simplest to use
- No scripting needed
- Claude Code built-in feature

**Cons:**
- Agent might not respect the limit
- Count could be lost in context compaction

---

### Approach 2: Hard Cap (Shell-Enforced)

**Uses:** Shell script + ANY agent CLI (`claude -p`, `opencode run`, etc.)  
**Cap enforcement:** Shell `for` loop guarantees max attempts

```bash
cd shell-loop

# Edit loop.sh to choose your agent CLI:
# - claude -p     (for Claude Code)
# - opencode run  (for OpenCode)

bash loop.sh
```

**Pros:**
- **Guaranteed** maximum attempts
- Shell handles counting, not the agent
- Works with Claude Code, OpenCode, or any agent with a CLI

**Cons:**
- Requires basic shell scripting
- Slightly more complex setup

See `shell-loop/README.md` for details on using any agent CLI with this pattern.

---

## Success Criteria

✅ **Good**: Loop stops at attempt 2-3 because tests passed  
❌ **Bad**: Loop stops at attempt 6 because hit the cap

If you consistently hit the cap:
- The agent isn't reading test output correctly
- Fixes aren't being applied properly
- The prompt needs to be more specific

## The Pattern (Same in Both Approaches)

```
1. Run npm test (checker command)
2. Check exit code
3. If 0: SUCCESS, stop
4. If non-zero AND attempts < 6: agent fixes bugs, continue
5. If non-zero AND attempts = 6: FAILURE, stop
```

**Key insight:** The test runner's exit code is authoritative, not the agent's judgment.

The command's exit code is objective and reliable - better than agent judgment.

## Key Difference Between Approaches

| Aspect | Soft Cap (`/goal`) | Hard Cap (Shell) |
|--------|-------------------|------------------|
| **Who counts?** | Agent (Claude) | Shell script |
| **Who enforces?** | Agent (might fail) | Shell (guaranteed) |
| **Tools needed** | Claude Code only | Any agent with CLI |
| **Complexity** | Simple | Medium |
| **Reliability** | Good | Excellent |

Both demonstrate the same **conditional loop pattern**. The difference is reliability of the iteration cap, not the core concept.

## From the Loop Engineering Doc

Both approaches implement Concept 5 (Conditional Loop / Run-Until-Done):

> "There is no built-in 'give up after N tries.' If you want a limit, write it into the condition."

That's the soft cap (Approach 1).

> "Always cap the tries. A loop that retries with no limit is how token bills grow out of control."

That's why the hard cap (Approach 2) exists - guaranteed enforcement.

## Project Structure

```
02-conditional-loop/
├── math.js           # Buggy code
├── test.js           # Failing tests
├── package.json      # npm test config
├── README.md         # This file
└── shell-loop/       # Hard cap implementation
    ├── loop.sh       # Shell-enforced cap (any agent CLI)
    └── README.md     # Details on using with any agent
```
