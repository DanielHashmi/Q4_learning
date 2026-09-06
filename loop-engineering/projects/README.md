# Loop Engineering Projects

A practical progression for turning agent work into **reliable, repeatable loops**: observe long tasks, stop on objective signals, preserve state between runs, verify changes independently, and gate automation with human review.

## Project map

| Project | Focus | What it demonstrates |
| --- | --- | --- |
| [01 · In-Session Loop](./01-in-session-loop/) | Monitoring | A session-bound loop checks a long-running task at intervals and reports completion. |
| [02 · Conditional Loop](./02-conditional-loop/) | Bounded iteration | Exit codes decide whether to stop, while a hard shell cap prevents infinite retries. |
| [03 · Unattended Schedule](./03-unattended-schedule/) | Durable state | GitHub Actions uses committed `progress.md` as a spine across fresh scheduled runners. |
| [04 · Fix Loop](./04-fix-loop/) | Safe autonomy | Isolated worktrees, independent checks, and a read-only reviewer gate fixes before PR creation. |
| [05 · Codify the Body](./05-codify-body/) | Reusable workflow | Multiple candidates run in isolated workspaces with external scope, test, lint, and verdict checks. |
| [06 · Doorbell Loop](./06-doorbell-loop/) | Event triggers | Pull-request events automatically start a read-only OpenCode review without a manual prompt. |
| [07 · Break It on Purpose](./07-break-it-on-purpose/) | Failure observability | Bounded failures produce durable logs, human checkpoints, and cost evidence for diagnosis. |
| [08 · Daily Dependency Loop](./08-daily-dependency-loop/) | Unattended maintenance | A daily audit uses a spine, isolated worktree, independent gates, budgets, and PR-based human approval. |
| [09 · Routine Rehearsal](./09-routine-rehearsal/) | Honest outcomes | A green workflow can still contain a failed task; the transcript is the acceptance evidence. |
| [10 · Secrets Drill](./10-secrets-drill/) | Secret delivery | A fresh cloud clone cannot provide a gitignored `.env`; an injected environment variable can. |
| [11 · Two-Routine Gate](./11-two-routine-gate/) | Multi-stage approval | A reviewed draft from Routine A is verified by an authenticated, bounded Routine B. |
| [12 · Dreaming Loop](./12-dreaming-loop/) | Evidence-backed improvement | Repeated corrections become the basis for a minimal, human-reviewed rules-change proposal. |

## The progression

```text
observe → condition → remember → isolate → codify → trigger → fail visibly → maintain → rehearse → inject safely → gate → improve
```

The projects build toward a complete loop with four complementary parts: a **heartbeat** that starts work, a **body** that performs it, a **spine** that preserves durable state, and **gates** that verify results before anything consequential happens.

## Start here

Read the projects in numerical order for the intended progression. If you want the smallest complete example, begin with [02 · Conditional Loop](./02-conditional-loop/) for objective stop conditions and bounded retries. For the unattended end state, continue to [08 · Daily Dependency Loop](./08-daily-dependency-loop/) and [12 · Dreaming Loop](./12-dreaming-loop/).

> These projects are educational experiments. Review each project’s README for required credentials, repository secrets, workflow permissions, and external-service setup before running it.
