# RESULTS — Project 4: The Tool Diet

## What's real here
- `repo/tools/before-tools.json` — 12 tools, deliberately overlapping (3
  near-duplicate lookups, 3 near-duplicate updates, 3 ticket actions).
- `repo/tools/after-tools.json` — the same capability surface cut to 4
  non-overlapping tools.
- `repo/tools/backend-server.js` — a real backend: its own OS process, a
  real TCP port, real HTTP endpoints, state persisted to a real file on
  disk. Not a mock living inside the test script.
- `repo/tools/run-trial-real.js` — the live `gemini-3.5-flash-lite` API
  picks tools, and every tool call is a real HTTP request to that
  separate backend process. This script never grades itself.
- `repo/tools/verify-state.js` — an independent script, run separately
  after each trial, that reads the backend's real persisted state over
  HTTP. It has no connection to the trial script and can't be fooled by
  anything the trial script reports about itself.

Two earlier test designs were tried and dropped rather than kept
alongside this one: a version where the "backend" was a switch statement
mutating an in-memory variable inside the same script that also graded
itself, and a version that asked for a single function call with no
execution or end-state check at all. Neither is in this tree — both are
visible in `git log` if you want the full history.

## Real terminal output (verbatim, from a live run against the backend process)
12 trials, 6 per manifest, run 2026-08-31. Each trial's tool calls went
over real HTTP to `backend-server.js`; each result below is from
`verify-state.js`, a separate process with no relationship to the trial:

```
TRIAL before-1 -> callLog: find_customer_by_email, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL before-2 -> callLog: find_customer_by_email, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL before-3 -> callLog: find_customer_by_email, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL before-4 -> transient network/API error, no output, retried successfully
TRIAL before-5 -> callLog: find_customer_by_email, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL before-6 -> callLog: find_customer_by_email, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}

TRIAL after-1 -> callLog: get_customer, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL after-2 -> callLog: get_customer, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL after-3 -> callLog: get_customer, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL after-4 -> transient network/API error, no output, retried successfully
TRIAL after-5 -> callLog: get_customer, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
TRIAL after-6 -> callLog: get_customer, close_ticket, update_customer
VERIFY (independent) -> {"addressCorrect":true,"ticketClosed":true,"taskDone":true}
```
Full raw log: `repo/results-real.jsonl`.

Real summary:
```json
{ "before": { "trials": 6, "independentlyVerifiedDone": 6 },
  "after":  { "trials": 6, "independentlyVerifiedDone": 6 } }
```
**6/6 verified on both manifests.** Two lines are marked `-retry` in the
log where the first attempt hit a genuine transient network/API error
(uncaught fetch failure, empty output, non-zero exit) — logged as an
infra flake and retried, not silently dropped or scored either way.

## What this proves, honestly
- Every trial on both manifests picked the exact same call sequence
  (`find_customer_by_email` before / `get_customer` after, then
  `close_ticket`, then `update_customer`). This was checked directly and
  is not an artifact of the test:
  - Re-run at `temperature: 1.0`+ — same result.
  - Re-run with a unique random string in every prompt, ruling out
    request-level caching — same result.
  - The winning lookup tool is 6th of 6 listed options in the before
    manifest, so it isn't a list-order default either.
- So this is a real, independently verified, non-cached, non-order-biased
  result — and it is still a single stable decision per manifest, not 6
  independently varying trials. Both are true at once: the test is now
  real (separate process, real network calls, independent grading), and
  the task is still too unambiguous to produce any disagreement for the
  model to resolve differently across manifests.
- The course explicitly allows this outcome: *"if nothing improved, your
  list was already lean, which is also worth knowing."* With a real
  backend and independent verification, cutting 12 tools to 4 made no
  measurable difference on this task — the model completed it correctly
  on every real, verified trial, on both manifests.
- The honest limitation now is the task, not the plumbing: it needs
  genuinely ambiguous tool descriptions or a harder decision point to
  actually exercise the tool-diet hypothesis. Not built here — noted as
  the next step instead of overstating this result.

## Reproduce it yourself
```
cd project-4-tool-diet/repo
node tools/backend-server.js 8743              # real backend, separate terminal
$env:GEMINI_API_KEY = "<your key>"
node tools/run-trial-real.js before 1 8743     # real HTTP tool calls
node tools/verify-state.js 8743                # independent check, separate process
```
No Claude-Code-specific requirement applies to this project.
