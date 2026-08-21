# Project 8: Your Own Daily Loop

This capstone runs a daily dependency-audit chore unattended. Each beat reads
`progress.md`, creates an isolated worktree, asks a maker to refresh
`audit-report.md`, asks a separate read-only reviewer to grade it, runs an
independent audit and file-scope check, and opens a GitHub pull request through
`gh` only when every gate passes.

Budget guards stop runaway work: one candidate, one report file, five-minute
agent timeouts, three attempts per agent, and a maximum diff of 200 lines.
The workflow uses a concurrency group so two beats cannot consume the same
spine concurrently. All artifacts are uploaded even after failure.

Run `bash verify.sh`. The real unattended loop is the repository-root workflow
`.github/workflows/project-08-daily-loop.yml`. The human gate remains the PR
merge decision.
