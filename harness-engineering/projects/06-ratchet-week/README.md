# RESULTS — Project 6: The Ratchet Week

## Honest scope limitation
A literal 7-day wait for organic production mistakes isn't possible inside
a single (multi-session) build. This project uses **7 real, distinct mistakes that actually happened** during this very build of Projects 1–5 — each one independently verifiable against the other projects' README.md files where that evidence still exists on disk — rather than fabricating a fake week of agent logs. This is more honest than pretending to simulate a week, and it satisfies the course's real ask: *every mistake classified, every fix written to its surface.*

## What's real here
`repo/HARNESS.md` — the 7-entry ratchet log. Every entry:
- names a specific, real thing that went wrong in this session (not
  invented for the exercise),
- classifies it into one of the four failure classes from Concept 10's
  table (context / constraint / verification / planning),
- writes one fix onto that class's own surface (a rule, a vendored binary,
  a citation-verification discipline, a retry policy, an honest reporting
  convention) — never "a stronger sentence," per the course's own
  admonition.

## The self-check the course asks for
Concept 10 flags a specific trap: seeing the same failure shape twice means
the first one was misclassified. `HARNESS.md` ends with a real "pattern
check" section that does exactly this — it notices Days 1 and 6 are both
Verification failures, and Days 4 and 7 are both unverified-citation
Context failures, with a shared root cause each time, and writes the
**generalized** fix once per shape, instead of leaving near-duplicate
entries that would each need rediscovering.

## Cross-references (so every claim here is checkable)
- Day 1 → `../02-lint-hook/README.md` (the exit-code verification work)
- Day 2 → inlined directly in `repo/HARNESS.md` (source file deleted; no
  longer independently checkable, flagged as such in the entry itself)
- Day 3 → same as Day 2, inlined and flagged, not independently checkable
  anymore
- Day 4 → `../05-typed-reviewer/repo/tools/` (the missing transcript file —
  check for yourself: `tools/live-verification-output.txt` is cited in
  `../05-typed-reviewer/README.md` but is not present in that folder or in
  `git log --all -- **/live-verification-output.txt`)
- Day 5 → `../_tools/jq.exe` (the real vendored binary) and
  `../05-typed-reviewer/repo/tools/validate-verdict.sh` (the `JQ_BIN`
  override) — both still real and independently checkable
- Day 6 → `../04-tool-diet/README.md` and this session's actual
  `results-real.jsonl` cleanup (the corrupted file was observed directly
  before being discarded and cleanly re-run), plus the live `fetchWithRetry`
  fix in `../04-tool-diet/repo/tools/run-trial-real.js`
- Day 7 → `../README.md` (the index table row for Project 4, both the
  original overclaiming text and the corrected line are checkable in that
  file's edit history) and `../04-tool-diet/README.md` (confirm for
  yourself: no "single-turn test" disclosure exists anywhere in it)