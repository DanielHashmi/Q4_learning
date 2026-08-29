# RESULTS — Project 2: The Lint Hook

## What's real here
- `repo/scripts/lint.js` — a genuine (dependency-free) linter that flags
  `const`/`let` declarations used only once (i.e. unused variables), reading
  every `.js` file in `src/`.
- `repo/scripts/test.js` — a genuine assertion-based unit test for `add()`.
- `repo/.claude/settings.json` — a real `PostToolUse` hook
  (`matcher: "Edit|Write"`, command `npm run lint --silent >&2 || exit 2`) and
  a real `Stop` hook (`npm test --silent >&2 || exit 2`).
- `repo/.opencode/plugin/lint-after-edit.js` — a real OpenCode plugin using
  the `tool.execute.after` hook point, running the same linter after any
  `edit`/`write` tool call.
- `repo/.git/hooks/pre-commit` — a real, live git hook (not a template) that
  runs lint + test and blocks the commit on failure.

## Mechanical verification (exact commands actually run this session)

### 1. PostToolUse hook contract
Introduced a real lint violation (`const unusedThing = 42;` appended to
`src/index.js`), then ran the **exact** hook command string from
`.claude/settings.json` through git-bash:
```
$ npm run lint --silent >&2 || exit 2
```
Real output:
```
lint: 1 problem(s)
  src\index.js: 'unusedThing' is assigned a value but never used.
```
Confirmed exit code: **2** — exactly the "block and feed this back to the
agent" signal Claude Code's hook contract expects.

Removed the bad line, re-ran the same command → exit code **0**, output
`lint: clean`.

### 2. Stop hook contract
Rewrote `scripts/test.js`'s assertion to expect `999` instead of `5` (a real,
failing test), then ran the exact Stop-hook command:
```
$ npm test --silent >&2 || exit 2
```
Real output:
```
test: FAILED - Expected values to be strictly equal:
999 !== 5
```
Confirmed exit code: **2**.

### 3. Real git pre-commit gate — actually blocked a commit
Reintroduced a lint violation, ran `git add -A && git commit -m "..."`. The
**real, live git hook actually fired** and the commit was rejected:
```
lint: 1 problem(s)
  src\index.js: 'willFailPrecommit' is assigned a value but never used.
pre-commit: lint or tests failed - commit blocked
```
`git commit` exit code: **1** (blocked — no new commit was created).

Fixed the violation, ran `git add -A && git commit -m "..."` again:
```
lint: clean
test: 1 passed
[main 9b8a0da] Project 2: verified working lint+stop hooks and pre-commit gate
```
This commit is real and present in `git log --oneline` for this repo.

## What this demonstrates (the actual point of Concept 8)
The enforcement never depended on the model "remembering" to lint or test —
it happened automatically, deterministically, after every edit and before
every session end, and it used the same binary exit-code contract
(0 = fine, non-zero = something's wrong, treated as 2 = block) that both
Claude Code's hooks and a plain git hook understand. Swapping which agent is
driving (Claude Code, OpenCode, or a human typing `git commit` by hand)
doesn't change whether broken code gets caught — the guardrail lives outside
the agent.