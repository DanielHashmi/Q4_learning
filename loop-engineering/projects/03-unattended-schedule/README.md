# Project 3: Morning TODO Brief With a Spine

This project is a small unattended loop that turns open TODO comments into a
morning brief. It runs in GitHub Actions, so it keeps working while the laptop
is closed. OpenCode performs the scan and update; `progress.md` is the durable
memory between fresh GitHub runners.

## What It Demonstrates

Project 3 has two required parts from the course:

- **Heartbeat:** GitHub Actions runs at 9:00 AM Asia/Karachi, Monday through Friday.
- **Spine:** Every run reads and updates `progress.md`, then GitHub commits it.

The first run records six TODOs. The second run sees those same entries in the
spine and records no duplicates. That is the proof that a fresh runner has
memory of earlier work.

## How A Run Works

```text
GitHub schedule or manual trigger
        |
        v
Fresh Ubuntu runner checks out main
        |
        v
OpenCode reads progress.md and scans the two sample files
        |
        v
OpenCode appends only new TODOs, or "No new TODOs found."
        |
        v
GitHub Actions commits progress.md to main
        |
        v
The next fresh runner starts with that committed spine
```

The GitHub Actions workflow is at the repository root because GitHub discovers
workflows only from `.github/workflows/`. The project itself remains self-contained
in `projects/03-unattended-schedule`.

## Files

- `../../../.github/workflows/project-03-morning-brief.yml`: schedule, OpenCode job, and commit step.
- `progress.md`: the spine and audit log.
- `task.js` and `utils.ts`: six deliberately small TODO examples.
- `loop.sh`: optional local OpenCode experiment; it is not used by GitHub Actions.

## Required Setup

1. Commit and push this repository to GitHub's `main` branch.
2. In GitHub, open **Settings -> Secrets and variables -> Actions**.
3. Create a repository secret named `OPENCODE_API_KEY`.
4. Put an OpenCode API key in that secret. Do not use an Anthropic key for this workflow.
5. Ensure the OpenCode workspace behind that key has an active payment method or available API credit.
6. In **Settings -> Actions -> General**, ensure workflows have read/write repository permissions.
7. If `main` is protected, allow GitHub Actions to push this workflow's commit or configure an appropriate bypass rule.

The workflow uses the built-in `GITHUB_TOKEN` only to commit the already-reviewed
spine update. It has no issue or pull-request permissions.

## Proving The Spine

After the workflow is on `main`, open **Actions**, choose **Project 3 - Morning
TODO Brief**, and select **Run workflow** twice.

Expected first run:

```text
6 TODOs scanned
6 new TODOs recorded in progress.md
```

Expected second run:

```text
6 TODOs scanned
0 new TODOs recorded
No new TODOs found.
```

After each successful run, the workflow creates a commit named
`chore(project-03): update morning TODO brief`. On the second run,
`progress.md` must contain a new dated section with `No new TODOs found.` and
must not repeat the six TODO list.

## Operational Notes

- Scheduled workflows run from the latest commit on the default branch.
- GitHub Actions may delay scheduled runs during periods of high load. Use the
  manual trigger when testing.
- The concurrency lock prevents two overlapping runs from reading the same stale
  spine and committing conflicting updates.
- The model is `opencode/big-pickle`. Change it only to a model available
  to your OpenCode account.
- Never store API keys in files or commits. Use only the repository secret.

## Success Criteria

- The workflow appears in the repository Actions tab.
- The first run records all six TODOs.
- The second run records no duplicate TODOs.
- The second run commits a `No new TODOs found.` entry to `progress.md`.
- The laptop can be closed for scheduled runs.
