# Project 3: Morning TODO Brief With a Spine

This project is an unattended GitHub Actions loop that turns TODO comments into
a short, durable morning brief. Every Actions runner is fresh; `progress.md` is
the committed memory that lets the next run avoid repeating prior findings.

## What It Demonstrates

- **Heartbeat:** GitHub Actions runs at 9:00 AM Asia/Karachi, Monday to Friday.
- **Spine:** Each run reads `progress.md`, updates it through OpenCode, and
  commits the result to `main`.
- **Guardrail:** The workflow fails if OpenCode changes any file other than
  `progress.md`.

The original first run recorded six TODOs. The next run recorded only `No new
TODOs found.` This proves that two separate, fresh GitHub runners shared state
through the committed spine.

## How A Run Works

```text
GitHub schedule or manual trigger
        |
        v
Fresh Ubuntu runner checks out main
        |
        v
OpenCode CLI reads progress.md and scans task.js plus utils.ts
        |
        v
OpenCode appends new TODOs, or "No new TODOs found."
        |
        v
GitHub Actions commits only progress.md to main
        |
        v
The next fresh runner starts with that committed spine
```

The workflow lives at the Git repository root because GitHub discovers workflows
only from `.github/workflows/`. The project code and its state remain in
`loop-engineering/projects/03-unattended-schedule`.

## Files

- `../../../.github/workflows/project-03-morning-brief.yml`: schedule, OpenCode CLI invocation, and guarded commit.
- `progress.md`: the spine and audit log.
- `task.js` and `utils.ts`: six deliberately small TODO examples.
- `loop.sh`: optional local experiment; GitHub Actions uses the workflow instead.

## Required Setup

1. Commit and push the repository's `main` branch to GitHub.
2. In GitHub, open **Settings -> Secrets and variables -> Actions**.
3. Create a repository secret named `OPENCODE_API_KEY` with your OpenCode API key.
4. In **Settings -> Actions -> General**, allow workflows to have read/write repository permissions.
5. If `main` is protected, allow GitHub Actions to push this workflow's spine commits or configure an appropriate bypass rule.

The workflow installs OpenCode, runs `opencode run --model opencode/big-pickle`,
and uses the built-in `GITHUB_TOKEN` only to commit `progress.md`. Big Pickle is
the free OpenCode model used by the verified runs.

## Verified Proof

The workflow was tested manually twice on August 18, 2026:

- [First proof run](https://github.com/DanielHashmi/Q4_learning/actions/runs/32106497786) recorded all six TODOs.
- [Second proof run](https://github.com/DanielHashmi/Q4_learning/actions/runs/32106577026) added only `No new TODOs found.`

The matching commits are `f895a4c` and `5bd31a5`. The current
`progress.md` therefore already contains the completed proof.

## Rehearse The Spine Again

To demonstrate the same behavior yourself after cloning the completed project:

1. Add one new TODO comment to `task.js` or `utils.ts`.
2. Open **Actions**, choose **Project 3 - Morning TODO Brief**, and select **Run workflow**.
3. Confirm the run adds exactly that TODO to `progress.md` and commits it.
4. Run the same workflow again without changing the sample files.
5. Confirm the second run adds only a dated `No new TODOs found.` entry.

This is a better rehearsal than expecting the original six TODOs to be new a
second time: the committed spine deliberately remembers them already.

## Operational Notes

- Scheduled workflows run from the latest commit on the default branch.
- GitHub Actions can delay scheduled runs during high load; use manual dispatch for testing.
- The concurrency lock prevents two runs from reading the same stale spine.
- API keys stay in GitHub Secrets and never belong in source files or commits.
- The workflow is intentionally narrow: OpenCode may update the spine, but not the sample code or workflow.

## Success Criteria

- The workflow appears in the repository Actions tab.
- A run records a newly introduced TODO exactly once.
- A following run records no duplicate TODO entries.
- Every allowed state change is a `progress.md` commit.
- Scheduled runs continue with the laptop closed.
