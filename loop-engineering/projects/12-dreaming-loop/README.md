# Project 12: The Dreaming Loop

This weekly improvement pass reads Project 8's committed `progress.md` after
the cursor in `dreaming-state.md`, detects an identical correction repeated at
least twice, and drafts the smallest evidence-backed rules change as a PR.

It also proposes one deletion. It never edits `AGENTS.md`, `CLAUDE.md`, a
skill, or another rules file directly. The only durable rule change is a
human-reviewed PR.

Run `bash verify.sh` locally. The root workflow
`.github/workflows/project-12-dreaming-loop.yml` runs weekly and supports
manual dispatch. It runs the analyzer and a separate read-only checker, then
opens a `claude/dreaming-*` PR only when cited repeated evidence exists.
