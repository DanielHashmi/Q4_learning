# Project 6: The Grounded Reviewer

This project upgrades a reviewer from “the report sounds plausible” to “every
factual statement points at a source-backed graph claim.” It uses a small graph
with claims sourced to real files in the loop-engineering repository and runs
five maker/checker beats.

## Run

```bash
python3 real_loop.py
python3 validate.py
```

`real_loop.py` copies the existing Project 3 shell loop into a throwaway
workspace, runs that real loop five times, and captures its actual tool output
before sending each report through the grounded reviewer. Each invocation has
a three-minute timeout so an unavailable provider is recorded as a failed tool
beat rather than hanging forever. `run_beats.py` is retained as the compact
contract fixture.

## Reviewer rules

- A factual statement must name a resolvable active claim ID.
- A claim whose source is `inference` cannot ground a factual statement.
- Missing support yields `REVISE` with a precise `missing` entry.
- A verdict includes the rubric and the exact `grounded_in` IDs.

The second beat intentionally makes an unsupported claim, receives `REVISE`,
then has the maker withdraw it. The third beat cites an inference claim and is
also rejected. This is the important separation: a graph may preserve an
inference honestly, but the reviewer may not launder it into evidence.
