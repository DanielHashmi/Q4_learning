# Project 9: Rehearse a Routine for Free

This project demonstrates the important routine lesson without pretending a
green infrastructure status proves the task succeeded. Each manual dispatch
is a one-off run. The runner always completes its infrastructure contract and
writes a transcript, while the task inside the transcript is either `PASS` or
`FAIL`.

Run locally:

```bash
bash run-one-off.sh success
bash run-one-off.sh failure
bash verify.sh
```

The root workflow `.github/workflows/project-09-routine-rehearsal.yml` exposes
the same one-off modes. Dispatch it once with `success` and once with
`failure`, then download both artifacts. Both workflow runs are green; only
the transcript explains that the second task could not read its requested
file. This is the OpenCode/GitHub equivalent of the course’s Routine drill.
