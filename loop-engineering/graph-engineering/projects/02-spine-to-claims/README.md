# Project 2: Spine to Claims

This project takes ten durable findings from the real Project 3 and Project 8
loop spines and records them as typed claims. A `progress.md` file is still useful
for diary entries, retries, and context. `claims.json` is stricter: it stores
only findings that another agent should be able to query, along with how the
finding was established.

The most useful result is the inference count. A claim marked
`{"kind":"inference"}` is not forbidden or hidden; it is an honest label that
the current evidence is the agent's reasoning rather than an independently
captured observation. Here, all ten claims are currently file-backed, so the
inference count is zero. That is itself a useful baseline: future unsourced
findings must be marked as inference rather than given a fabricated receipt.

## Run

```bash
python3 validate.py
```

The validator checks the required claim fields, unique IDs, confidence range,
source shape, and that every file-backed source points at a file in this
repository. It also prints the inference count.

## Concept

Provenance is the receipt attached to memory. `produced_by` tells us which beat
wrote a claim; `source` tells us what a later agent can inspect; `supersedes`
would preserve the predecessor when a later claim corrects an earlier one.
Nothing here is declared universal truth. The graph records what was claimed,
why, and how confident the author was.
