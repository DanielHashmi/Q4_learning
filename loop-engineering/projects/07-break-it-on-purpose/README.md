# Project 7: Break It on Purpose

This project extends Project 3 with cost measurement, a deliberately bounded
failure, durable observability, and diagnosis from the spine alone.

Run `bash verify.sh`. It executes a healthy beat and sabotaged beats, checks
the attempt limit, writes a timestamped failure to `run.log`, records a
`needs a human` checkpoint in `progress.md`, and calculates monthly cost in
`cost.json`. The diagnosis reads only those three evidence files.

The repository-root workflow at `.github/workflows/project-07-break-it.yml`
runs the same proof on a weekday schedule or manual dispatch and uploads the
evidence even when the sabotage job fails.
