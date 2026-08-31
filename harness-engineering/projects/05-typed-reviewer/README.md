# RESULTS — Project 5: The Typed Reviewer

## What's real here
- `repo/.claude/agents/reviewer.md` — the exact typed-verdict reviewer from
  the course (Read + Bash tools, haiku model, a `PreToolUse` hook naming the
  allowlist script).
- `repo/.claude/hooks/reviewer-allowlist.sh` — the exact command allowlist
  hook: only `npm test*`, `npm run lint*`, `git diff*` pass; everything else
  gets `exit 2`.
- `repo/.opencode/agent/reviewer.md` — the OpenCode equivalent: `mode:
  subagent`, `edit: deny`, `bash` denied by default with the same three
  commands allowed.
- `repo/tools/validate-verdict.sh` — the real field-by-field `jq` validator
  from Concept 9, wired to the actual `jq.exe` binary already downloaded to
  `projects/_tools/jq.exe` (no fake/stubbed jq).
- `repo/tools/run-all-tests.sh` and `repo/tools/test-output.txt` — a real
  4-case test run, captured verbatim (not retyped) via git-bash.

## Real terminal output (verbatim, from `tools/test-output.txt`)
```
=== TEST A: well-formed PASS ===
ACCEPTED: verdict=PASS
exit code: 0

=== TEST B: well-formed FAIL ===
ACCEPTED: verdict=FAIL
exit code: 0

=== TEST C: well-formed but invalid verdict (MAYBE) ===
REJECTED: reviewer broke protocol — escalating to a human
- reviewer output unparseable: needs a human
exit code: 2

=== TEST D: non-JSON free text ===
REJECTED: reviewer broke protocol — escalating to a human
- reviewer output unparseable: needs a human
exit code: 2
```

## What this proves
- (a) A well-formed PASS is accepted, exit 0.
- (b) A well-formed FAIL is accepted, exit 0 (FAIL is a valid verdict — the
  contract validates *shape*, not favorable outcome).
- (c) The course's own trap case — `{"verdict":"MAYBE",...}`, syntactically
  perfect JSON — is genuinely **rejected**, because the validator checks
  `.verdict` against its allowed *values*, not merely its presence. Exit 2,
  same as the hook contract's blocking code.
- (d) Free-text prose (a model "explaining" instead of returning JSON) is
  also rejected with the same exit 2 and the same escalation message,
  because `jq -e` fails to parse it as JSON at all.
- In both (c) and (d) the script never guesses at an answer — it escalates,
  matching the course's "the loop moves on, the item waits for a person"
  contract exactly.

## Reproduce it yourself
```
cd project-5-typed-reviewer/repo
"C:\Program Files\Git\bin\bash.exe" -c "sh tools/run-all-tests.sh"
```
Requires `_tools/jq.exe` (already present one level up from `projects/`) and
git-bash for POSIX `sh`/exit-code semantics.

## Live end-to-end verification
The reviewer subagent's allow/deny contract has been proven live against
a real model, not just via the jq layer above. Full raw transcript in
`tools/live-verification-output.txt` (pulled with `opencode export`, not
hand-typed). Summary:

- **Allowed commands actually ran.** Delegated to the OpenCode `reviewer`
  subagent via a real `opencode run ... --agent build` invocation (the
  primary agent's task tool handed off to `reviewer`). It genuinely executed
  `npm test`, `npm run lint`, and `git diff`, and returned
  `{ "verdict": "PASS", "reasons": [], "risk": "low" }`.
- **A disallowed command was actually blocked.** In that same run, the
  model itself (unprompted) tried a fourth command outside the allowlist:
  `bash tools/run-all-tests.sh`. It was rejected with a real permission
  error naming the exact allow/deny rule set (`npm test*` / `npm run lint*`
  / `git diff*` allow, everything else deny). The subagent didn't retry
  around it - it just finished with the three permitted commands.

**OpenCode side:** `.opencode/agent/reviewer.md` pointed to `google/gemini-3.5-flash-lite` - the allow/deny contract lives in the `permission` block and is enforced the same way regardless of model.

**Claude Code side:** `.claude/agents/reviewer.md`,
`.claude/hooks/reviewer-allowlist.sh`, and `.claude/settings.json` are
unchanged from the course and are ready to run as-is.