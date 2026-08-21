# Project 11: The Two-Routine Gate

Routine A creates a reviewable draft on an isolated `claude/*` branch and
opens a pull request. A human reviews it. Routine B runs only after an
authenticated API dispatch, verifies A's draft, performs one small follow-up
action, and records a transcript.

This is the GitHub Actions/OpenCode equivalent of the course's Claude Routine
pattern. The workflow-dispatch API is the event trigger and
`PROJECT11_B_BEARER_TOKEN` is stored as a repository secret. The token is
never written to a file or printed.

Run `bash verify.sh` for local checks. For the real gate, dispatch
`project-11-routine-a.yml`, read its PR, then use `fire-b.sh` with the stored
token, branch, run ID, and a non-empty approval note. A does not invoke B.
B never operates on `main`, is bounded to one follow-up record, and uploads a
transcript.
