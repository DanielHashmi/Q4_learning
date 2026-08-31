# Results — Project 8: Model Swap Capstone

> **Spec:** Run your hardened loop for three nights on a different model. Log everything
> that breaks or shifts. Done when each failure is fixed by moving it from
> behaviour-coupling to contract-coupling (exit codes, schemas, tests), and the loop
> runs clean on both models.

Two parallel harnesses — one for OpenCode + Gemini (complete), one for Claude Code +
Claude models (scaffolded, ready to run):

```
project-8-model-swap/
  opencode-loop/   ← complete: 3 real Gemini runs, 3 commits, 5 coupling bugs logged
  claude-loop/     ← ready: same structure, swap claude -p for opencode run
```

---

## OpenCode + Gemini — Results

Three real OpenCode agent sessions against the hardened harness in `opencode-loop/`,
two Gemini models swapping coder/reviewer roles each night.

| Night | Coder | Reviewer | Bug fixed | Tests | Verdict |
|-------|-------|----------|-----------|-------|---------|
| 1 | `gemini-2.5-flash` | `gemini-2.5-flash-lite` | `divide(1,0)` → throw Error | ✅ | PASS / low |
| 2 | `gemini-2.5-flash-lite` | `gemini-2.5-flash` | `average([])` → throw Error | ✅ | PASS / low |
| 3 | `gemini-2.5-flash` | `gemini-2.5-flash-lite` | `factorial(-1)` → throw Error | ✅ | PASS / low |

Git history in `opencode-loop/`:
```
1f43476  feat: factorial throws on negative  [night-3]
a73c706  feat: average throws on empty       [night-2]
0430282  fix: divide throws on zero          [night-1]
27aecf6  baseline
```

### Coupling failures surfaced (OpenCode run)

| # | Failure | Night | Coupling type | Fix |
|---|---------|-------|---------------|-----|
| 1 | `gemini-2.0-flash` doesn't exist in OpenCode's registry | pre-run | behaviour → contract | Queried `--print-logs`, found valid IDs |
| 2 | `&&` not valid in PowerShell | 1 | behaviour (assumed bash) | Agent recovered; logged as platform coupling |
| 3 | Unquoted commit message treated as pathspec | 2 | behaviour → contract | Harness double-quotes all commit messages |
| 4 | Reviewer wraps JSON verdict in markdown fences | 2 & 3 | behaviour → contract | Fence-strip carried forward from Project 5 |
| 5 | Buggy test: stack overflow accepted as valid throw | 3 setup | behaviour → contract | Test asserts `e.message === "negative input"` |

---

## Claude Code + Claude Models — Ready to Run

`claude-loop/` is a complete, working harness using `claude -p` instead of `opencode run`.
Same three nights, same bugs, same ratchet structure — model names are the only change.

### How to run

```powershell
cd claude-loop

# 1. One-time: initialise the throwaway git repo
git init
git add -A
git commit -m "baseline: harness + night-1 buggy divide()"

# 2. Run all three nights
node run-nights.js

# Or one night at a time
node run-nights.js --night 1
```

### Model pairs (edit NIGHTS in run-nights.js to match your auth)

| Night | Coder | Reviewer |
|-------|-------|----------|
| 1 | `claude-haiku-4-5` | `claude-sonnet-4-5` |
| 2 | `claude-sonnet-4-5` | `claude-haiku-4-5` |
| 3 | `claude-haiku-4-5` | `claude-sonnet-4-5` |

Alternate model names if the above return 403:
`claude-3-5-haiku-20241022`, `claude-3-5-sonnet-20241022`

### How the two harnesses differ

| | `opencode-loop/` | `claude-loop/` |
|--|--|--|
| CLI | `opencode run -m <model> --auto` | `claude -p --model <model> --allowedTools` |
| Headless | `< NUL` stdin redirect required | `-p` flag (non-interactive by design) |
| Permissions | `opencode.json` permission block | `.claude/settings.json` + `--allowedTools` |
| Reviewer | `.opencode/agent/reviewer.md` subagent | Separate `claude -p` call, read-only tools |
| Output | `--format json` event stream | `--output-format stream-json` |

---

## Harness verbs — both loops

| Verb | opencode-loop | claude-loop |
|------|---------------|-------------|
| **Constrain** | `opencode.json` bash allow/deny | `.claude/settings.json` + `--allowedTools` |
| **Inform** | `queue/night-N-*.md` spec files | same queue files |
| **Verify** | reviewer subagent runs tests + diff | separate `claude -p` reviewer call |
| **Correct** | tests exit 1; loop retried with tighter assertions | same exit-code contract |
| **Escalate** | `progress.md` Open section; `logs/ratchet.md` | same spine + ratchet |
