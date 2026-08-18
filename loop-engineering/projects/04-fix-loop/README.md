# Project 4: A Safe Fix Loop

**Difficulty:** Medium to hard  
**Concepts:** worktree isolation, skills/agents, maker-checker

This project implements a small autonomous fix loop with a hard safety gate:

```text
isolated checkout → maker → independent checks → read-only reviewer → PASS → PR
                                                       └─ FAIL → no PR
```

The fixture contains one intentional coupon-validation bug. The maker may fix
only the production module. The reviewer runs the tests and lint independently,
cannot edit files, and must begin its response with exactly `PASS` or `FAIL`.

## Run locally

Requirements: Git, Node.js, Bash, and OpenCode authenticated with access to
`opencode/big-pickle`.

From the repository root (`Q4_learning`):

```bash
bash loop-engineering/projects/04-fix-loop/scripts/run-fix-loop.sh --scenario both
```

The repository must be clean before running. Local runs prove the maker-checker
decision but do not open a PR. GitHub Actions opens the PR for the good case.

## Run in GitHub Actions

1. Add an `OPENCODE_API_KEY` repository secret.
2. Open **Actions → Project 4 - Safe Fix Loop**.
3. Run the workflow with `good`, `bad`, or `both`.
4. For `both`, verify one PR for the good candidate and no PR for the bad one.
5. Read the uploaded maker, reviewer, test, lint, and verdict artifacts.

## Done when

- The original tests fail before the loop.
- A good fix receives `PASS` and opens one PR.
- The planted bad fix receives `FAIL` and opens no PR.
- The reviewer cannot edit the candidate.
- A failing independent check blocks PR creation even if the reviewer claims
  `PASS`.
- `main` is never edited or pushed directly.
