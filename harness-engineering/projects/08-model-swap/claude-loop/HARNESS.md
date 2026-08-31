# claude-loop — Project 8 Model-Swap Harness (Claude Code)

Mirrors `opencode-loop/` exactly, but uses the `claude` CLI instead of
`opencode`. Both harnesses run the same three-night, two-model protocol
against the same bugs, so you can compare model behaviour across tools.

## Prerequisites

```powershell
# 1. Authenticate Claude Code
claude login
# or set ANTHROPIC_API_KEY in your environment

# 2. Initialise the git repo (one-time)
cd claude-loop
git init
git add -A
git commit -m "baseline: harness + night-1 buggy divide()"
```

## Running all three nights

```powershell
node run-nights.js
```

## Running a single night

```powershell
node run-nights.js --night 1
node run-nights.js --night 2
node run-nights.js --night 3
```

## Model pairs (edit run-nights.js if your auth differs)

| Night | Coder | Reviewer |
|-------|-------|----------|
| 1 | `claude-haiku-4-5` | `claude-sonnet-4-5` |
| 2 | `claude-sonnet-4-5` | `claude-haiku-4-5` |
| 3 | `claude-haiku-4-5` | `claude-sonnet-4-5` |

Swap models in the `NIGHTS` array at the top of `run-nights.js` to match
whatever models your API key can access (`claude-3-5-haiku-20241022`,
`claude-3-5-sonnet-20241022`, etc.).

## How it differs from opencode-loop

| | opencode-loop | claude-loop |
|--|--|--|
| CLI | `opencode run -m <model> --auto` | `claude -p --model <model> --allowedTools` |
| Permissions | `opencode.json` permission block | `.claude/settings.json` + `--allowedTools` flag |
| Headless | `< NUL` (stdin redirect) | `-p` flag (non-interactive by design) |
| Reviewer | `--agent reviewer` subagent | Separate `claude -p` call with read-only tools |
| Output parsing | `--format json` event stream | `--output-format stream-json` |

## What gets logged

- `logs/ratchet.md` — per-night verdict table (committed)
- `logs/run-nights.log` — raw timestamped run log (gitignored)
- `logs/night-N-*-coder.log` — full coder session output
- `logs/night-N-*-reviewer.log` — full reviewer session output
- `progress.md` — spine (all three nights checked off when complete)
