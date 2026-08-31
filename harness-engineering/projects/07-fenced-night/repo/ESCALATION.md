# Escalation contract (reusable, tool-agnostic)

Extracted from `night-prompt.txt` so the rule survives outside one run's
scratch prompt.

For each queue candidate:
1. Investigate and fix, running the project's own checks (`npm test`,
   `npm run lint`) before trusting any fix.
2. Hand the diff to the reviewer subagent; treat its reply as JSON.
3. **Escalate, don't act**, if any of: the reply isn't valid JSON, `verdict`
   isn't `PASS`, or `risk` is `"high"`. Append the item and the reviewer's
   stated reasons to the "Open / needs a human" section of `progress.md`.
   Do not commit. Do not open a PR.
4. **Proceed** only if `verdict` is `PASS` and `risk` is low: commit the fix
   and mark the item done in `progress.md`.
5. Work stays inside the repo. On finish, report exactly what ran, what each
   tool call returned, and anything blocked, denied, or failed — no summary
   without the underlying evidence.
