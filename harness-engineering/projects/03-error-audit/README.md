# RESULTS — Project 3: The Error Audit

## What's real here
- `repo/tools/customer-lookup.js` — a real simulated API connector with three
  genuine failure modes (missing scope, malformed ID, rate limit), each with
  a `--style bad|good` switch controlling the wording of the error message.
  The rate-limit failure is genuinely stateful (fails on attempt 1, succeeds
  from attempt 2 onward), so a real retry can actually work — it's not a trap.
- `repo/tools/rule-based-recoverer.js` — a real, literal-minded "agent" with
  **no world knowledge**: it can only act on text patterns it explicitly
  recognizes in an error message (grant a scope, reformat an ID, retry after
  a rate limit). If the message doesn't spell out what to do, it gives up.

## Part A — deterministic proof (no LLM involved)
Ran `node tools/rule-based-recoverer.js` for real. Actual output, summarized:

| Scenario | Bad-AX message | Recovered? | Good-AX message | Recovered? |
|---|---|---|---|---|
| missing-scope | `"Error 403"` | **No** | `"403: this token has no scope. Request a token with the 'customers:read' scope from /auth/token, then retry with the same customerId."` | **Yes** (2 attempts) |
| malformed-id | `"Invalid input."` | **No** | `"Invalid customerId 'notavalidid'. Expected format CUST-###### (6 digits), e.g. CUST-004521. Reformat and retry."` | **Yes** (2 attempts) |
| rate-limited | `"Too many requests."` | **No** | `"429: rate limited. Retry after 2000ms. Do not change the request; wait and resend the identical call."` | **Yes** (2 attempts) |

Real summary object printed by the script:
```json
{ "bad": { "missing-scope": false, "malformed-id": false, "rate-limited": false },
  "good": { "missing-scope": true, "malformed-id": true, "rate-limited": true } }
```
**0/3 recovered on bad AX. 3/3 recovered on good AX.** Same connector, same
failures, same recovery logic — the only variable changed was the wording of
the error message. This isolates AX as the causal factor.

## Part B — live-agent test (real `google/gemini-3.5-flash-lite` calls)

### Test 1: agent allowed to read source
Prompt: run the bad-style missing-scope call, act on the message, retry once.

The agent immediately **read `tools/customer-lookup.js`'s source** to
understand *why* it got `Error 403`, then retried with `--scope read` and
succeeded. **This is a real, important nuance the deterministic test above
can't show:** a capable LLM agent with file-read access doesn't strictly need
good AX in the error string — it can go read the implementation instead. Bad
AX matters most when the agent *can't* or *won't* read the source (a
black-box third-party API, a compiled binary, a locked-down sandbox that
denies reading connector internals, or a smaller/cheaper agent that doesn't
think to look).

### Test 2: agent explicitly told not to read source (bad-AX only)
Prompt: same failure, but explicitly instructed not to read the source file,
using only the terminal message.

Real transcript (verbatim tool calls, abridged):
```
$ node tools/customer-lookup.js CUST-004521 --scope none --style bad
{"ok":false,"message":"Error 403"}

I will run the command with --help ...
$ node tools/customer-lookup.js
{"ok":false,"message":"Invalid customerId 'undefined'. ..."}

I will check the script usage with --help.
$ node tools/customer-lookup.js --help
{"ok":false,"message":"Invalid customerId '--help'. ..."}

I will retry the lookup command changing --style bad to --style good.
$ node tools/customer-lookup.js CUST-004521 --scope none --style good
{"ok":false,"message":"403: this token has no scope. Request a token with the 'customers:read' scope..."}

I will retry with --scope customers:read --style good.
$ node tools/customer-lookup.js CUST-004521 --scope customers:read --style good
{"ok":true, ...}
```
**This is exactly the flailing the crash course describes.** Given only
`"Error 403"`, the agent tried `--help`, tried running with no arguments,
and only found the real fix by accidentally discovering the `--style` flag
existed and flipping it to `good` — which is an artifact of this test
harness's own CLI design (a real production API wouldn't expose a
"make my errors more helpful" flag), not a real recovery strategy. It got
lucky. In a real system without a `--style` escape hatch, this line of
guessing would have dead-ended exactly like the rule-based recoverer did.

## What this proves, honestly
- The deterministic 0/3 vs 3/3 result is unambiguous and reproducible: it
  isolates message wording as the entire cause of recovery success/failure.
- The live-agent test shows the same pattern *plus* a real caveat worth
  keeping in mind: capable agents with broad tool access can sometimes route
  around bad AX by reading source or guessing at flags — which doesn't make
  bad AX acceptable, it just means the cost of bad AX shows up as **wasted
  turns, wasted tokens, and non-reproducible "got lucky" fixes** instead of
  outright failure. Good AX turns a multi-step guessing spiral into a single
  deterministic corrective action, for both a rule-based recoverer and a
  frontier LLM agent alike.

## Reproduce it yourself
```
cd project-3-error-audit/repo
node tools/rule-based-recoverer.js
opencode run "Run 'node tools/customer-lookup.js CUST-004521 --scope none --style bad'. Do NOT read the source. React only to the message." --model google/gemini-3.5-flash-lite
```
No Claude-Code-specific requirement applies to this project.
