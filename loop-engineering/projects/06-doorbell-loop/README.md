# Project 6: The Doorbell Loop

Project 6 connects the engineering agent to a GitHub pull-request event. A PR
opening, update, reopen, or move out of draft automatically starts an OpenCode
review. No prompt is typed after the event.

## Real GitHub setup

This project uses the official OpenCode GitHub Action shape. In a throwaway
repository with a GitHub remote, run:

```bash
opencode github install
```

Accept the GitHub App installation and workflow setup, then ensure the selected
provider key exists as an Actions secret. The checked-in
the root `.github/workflows/project-06-opencode-review.yml` is the reproducible workflow: it uses
the `pull_request` event, runs on `opened`, `synchronize`, `reopened`, and
`ready_for_review`, and asks OpenCode to review without editing the PR.

To perform the exercise, create a branch, run `bash scripts/plant-bug.sh`,
commit it, and open a PR. The event should cause an unsolicited review that
flags the off-by-one behavior in `src/range.js`. Push the corrected file to the
same PR; the `synchronize` event should fire the loop again.

## Local verification

The local verifier proves the root workflow contract without claiming that a local
shell is GitHub Actions. It checks the event, action, permissions, read-only
prompt, passing base tests, lint, and that the planted bug makes the tests fail:

```bash
npm run verify
```

The live GitHub acceptance criterion remains: a PR review appears without a
manual `/opencode` comment, and the review identifies the planted bug. GitHub
credentials, an installed OpenCode App, and an API-key secret are required for
that external check.
