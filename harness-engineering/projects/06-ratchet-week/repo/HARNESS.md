# HARNESS.md — the ratchet log

Honest substitute for a literal 7-day wait (see ../README.md for why): these
are 7 real, distinct mistakes that actually happened during this multi-session
build of Projects 1–5 (one of them in this repo's own top-level index file),
each classified into one of the four failure classes from Concept 10's
table, with one fix written to that class's own surface.

---

**Day 1 — Verification: `2>&1` inside a PowerShell session running with
`$ErrorActionPreference = 'Stop'` corrupted `$LASTEXITCODE` when testing
hook exit codes for Project 2.** Reproduced directly this session: a Node
script that writes to stderr and exits 2, piped through bare `2>&1`,
reports the correct code (2) under the default `Continue` preference, but
under `Stop` PowerShell throws a `NativeCommandError` on the stderr line
and `$LASTEXITCODE` ends up `-1` instead of `2` — silently wrong, not just
noisy.
Class: **Verification failure** (bad work nearly got called done — a
corrupted exit code could have made a real `exit 2` block look like success).
Fix, on the verification surface: always shell out through git-bash
(`C:\Program Files\Git\bin\bash.exe -c "..."`) or `cmd /c "... > out 2> err"`
for any command whose exit code is being asserted on Windows, never bare
`2>&1` inside a PowerShell pipeline that might be running under strict
error mode. Codified in `02-lint-hook` and reused for real in Project 5's
test runner.

**Day 2 — Context: OpenCode did not autodetect a local Ollama server; agent
assumed it would and wasted a cycle discovering it silently used no model.**
Class: **Context failure** (it didn't know the provider had to be declared
explicitly). Fix, on the context surface: the working `provider` block that
fixed it, inlined here since the notes file that originally held it
(`STATUS.md`) has since been deleted by the user as no longer useful:
```json
"provider": {
  "ollama": {
    "npm": "@ai-sdk/openai-compatible",
    "name": "Ollama (local)",
    "options": { "baseURL": "http://localhost:11434/v1" },
    "models": { "ornith:9b": { "name": "ornith:9b" } }
  }
}
```
added to `opencode.json`, then `opencode run "<prompt>" --model ollama/ornith:9b`.
Note: this block does not currently appear in any committed `opencode.json`
in this tree (checked `01-first-wall/repo/opencode.json` and
`07-fenced-night/repo/opencode.json` directly — neither has a `provider` key),
so this fix was real and used live in-session but was never actually
persisted into a project's config. That gap is itself worth naming rather
than hiding.

**Day 3 — Planning: backgrounding `opencode run` via
`Start-Process cmd.exe ... -WindowStyle Hidden` hung indefinitely with zero
output for 3+ minutes in Project 2's live-agent smoke test.** (This entry's
only supporting record was `STATUS.md`, since deleted by the user; the
detail is preserved here from having read that file earlier in this same
session — it can no longer be independently re-checked against a file on
disk, which is itself worth flagging honestly rather than pretending
otherwise.)
Class: **Planning failure** (right tool, wrong shape of the call — an async
fire-and-forget pattern applied to a call that needed to be awaited
synchronously). Fix, on the structure surface: rule added — "run `opencode
run` synchronously in the foreground for any prompt short enough to return
in under ~30s; only background genuinely long unattended jobs, and even then
poll a log file rather than assuming completion." This is a smaller/differently-shaped
unit of work, not a tool or permission change, which is why it is filed as
planning and not constraint.

**Day 4 — Context: Project 5's own `README.md` cites `tools/live-verification-output.txt`
as the raw transcript proving the reviewer subagent's live allow/deny test
("pulled with `opencode export`, not hand-typed"), but that file was never
actually saved to disk or committed — checked directly this session, in
both the current working tree and the full git history, and it does not
exist anywhere.** (Earlier draft of this entry claimed a different mistake
— that OpenCode's `permission` block let an agent actually read `.env` in
Project 1 — but re-checking `01-first-wall/README.md`'s own Test A shows
that read was genuinely BLOCKED by OpenCode's ask-and-auto-reject default.
That was a pre-test hypothesis from `STATUS.md` that never got updated once
the real test disproved it, so it's replaced here rather than left as a
claim contradicted by its own cited evidence.)
Class: **Context failure** (an assumption that the `opencode export` output
had actually been persisted to disk was never checked before being written
into the README as a citable fact). Fix, on the context surface: any
README/RESULTS line that says "see raw transcript in `<file>`" gets written
only after confirming that file is saved AND committed — never from memory
of having run the export command. The underlying live-verification result
(the allow/deny contract itself) may still be true, but as written it
currently rests on an unchecked citation instead of an artifact a reader can
actually open — exactly the gap Concept 10 warns about: work that looks
done because nobody re-checked the artifact.

**Day 5 — Context: `jq` was assumed to be present system-wide for Project 5's
typed-output validation and was not.**
Class: **Context failure** (an environment assumption was wrong — nobody
told the harness, and the harness didn't check). Fix, on the context surface:
a real `jq.exe` binary is now vendored at `projects/_tools/jq.exe` and every
script that depends on it takes the binary path as a `JQ_BIN` override
(see `05-typed-reviewer/repo/tools/validate-verdict.sh`) instead of
assuming a bare `jq` on `PATH`.

**Day 6 — Verification: Project 4's `run-trial-real.js` had no error handling
around the Gemini API `fetch()` call, so a transient `ConnectTimeoutError`
during trial runs corrupted `results-real.jsonl` with raw Node stack traces
mixed in with valid JSON lines, requiring manual cleanup before the file
could be parsed for README.md.**
Class: **Verification failure** (bad/malformed output could have silently
polluted the dataset the way an unchecked reviewer reply pollutes a merge
decision). Fix, on the verification surface: the corrected trial run for
this project discarded and fully re-ran all 12 trials into a clean file
rather than trying to salvage the mixed log. **Update, this session: the
actual script fix is now applied for real**, not just logged as a plan --
see `04-tool-diet/repo/tools/run-trial-real.js`. Every network call
(backend endpoints and the Gemini API) goes through a `fetchWithRetry`
helper: capped at 3 attempts with growing backoff, retrying only on thrown
network errors and 5xx responses (a 4xx is a real answer, not an infra
flake, so it is not retried). The whole script is wrapped in one
top-level try/catch so any failure - retries exhausted or otherwise -
still emits exactly ONE well-formed JSON line to stdout (never a raw
stack trace) and exits 2, with diagnostics on stderr instead. Live-
verified both directions: a forced connection failure produced 3 real
retry attempts then one clean JSON error line, exit 2; a regression run
against the real backend still produced the same call sequence as before,
exit 0, independently confirmed via `verify-state.js`. This is exactly the
"transient failure -> retry with growing wait, hard cap" recovery rule
from Concept 10.

**Day 7 — Context: the top-level `projects/README.md` index table claimed
Project 4's writeup "discloses" an earlier single-turn test that showed a
difference between the two tool manifests, but `04-tool-diet/README.md`
contains no such disclosure anywhere — checked directly this session; the
only "earlier test" language in that file describes two different dropped
test designs (a version that graded itself, and a version with no
execution or end-state check), neither of which matches what the index
table claimed.**
Class: **Context failure** (a specific claim about what another file
contains was written into the index table without confirming the
referenced file actually contains it — the same shape as Day 4: an
unverified citation trusted as fact).
Fix, on the context surface: corrected the index table's own line to stop
claiming a disclosure that isn't there, and applied Day 4's rule
retroactively to this file too — a summary line that says "disclosed in
the writeup" only gets written after actually finding that content in the
target file, never from a general impression of what the project covered.
See the corrected line in `../README.md`.

---

## Pattern check (the ratchet's own self-test)
Two of the seven days above are Verification failures with a common shape:
**an exit code or output stream was trusted without being independently
re-derived on this platform (Windows/PowerShell) or without error-handling
around a network call.** Per Concept 10's own discipline ("if you see a
second, you classified the first one wrong" is the warning sign to check for
recurrence, not miss-classification here — two *different* mechanisms,
same *class*), the fix that generalizes across both Day 1 and Day 6: **any
script in this project tree that asserts on an exit code or parses command
output must either run through git-bash/cmd with captured streams, or wrap
network calls in try/catch with capped retries** — now written here once, so
it does not need rediscovering a third time.

Applying that same self-check to the Context failures turns up two more
pairs, not just one. First: Day 2 and Day 5 are both, as written above, a
runtime dependency assumed present or auto-configuring itself, discovered
wrong only when something broke ("OpenCode did not autodetect a local
Ollama server; agent assumed it would" / "`jq` was assumed to be present
system-wide... and was not") — two different missing dependencies (a
provider config, a binary), same class, same root shape: an unverified
environment assumption. The generalized fix that covers both: **any script
or config in this project tree that depends on a specific tool, binary, or
provider being present must either vendor/declare it explicitly or fail
loudly with a named missing-dependency error before doing any real work**
— rather than silently assuming, discovering the gap mid-task, and losing
a cycle to it. Only Day 5 actually applies this fix for real:
`projects/_tools/jq.exe` is a genuine vendored binary, committed and
present on disk. Day 2's fix does not meet its own bar — as Day 2's own
entry says, the `provider` block was used live, in-session, but was never
persisted into any committed `opencode.json` in this tree. So the
generalized fix is only half-applied; that gap is left visible here rather
than papered over.

Second: Day 4 and Day 7 share their own tighter shape — both are a claim
about what another file contains, written and trusted without ever opening
that file to check. Day 4 cited a transcript file as proof without
confirming it was saved and committed; Day 7 cited a "disclosure" in
another project's writeup without confirming that writeup actually said it.
The generalized fix that covers both: **any line that says "see X" or
"disclosed in Y" must be written only after X/Y is actually opened and the
claimed content confirmed present — never from memory or a general
impression of what a file probably covers.** Day 4's fix already states
this rule for README/RESULTS citations; Day 7 is that same rule applying
to index-table citations too, and the index table itself has now been
corrected to match.
