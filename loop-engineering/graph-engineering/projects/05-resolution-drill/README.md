# Project 5: Resolution Drill

Extraction preserves names exactly as written. Resolution is the separate
reasoning step that asks which mentions refer to one canonical entity.

This project consumes Project 3 output, expands it to twenty real surface forms
from those documents, and adds a deliberately ambiguous trap: two different
entities both called `review`. The resolver must merge genuine aliases while
keeping the two reviews apart.

## Run

```bash
python3 prepare_forms.py
python3 resolve.py --mode offline
python3 validate.py
```

For the required trap experiment, run `python3 run_trap.py --mode opencode`.
It resolves the twenty-form corpus, plants two same-name `review` entities,
then runs the resolver again and validates the second result.

`--mode opencode` asks OpenCode to produce the complete canonical clusters.
The result is rejected unless every input alias appears exactly once and every
cluster supplies an ID, rationale, and confidence. The offline resolver is the
deterministic free CI path.

## What to learn

Resolution is not string deduplication. A shared surface form is weak evidence;
descriptions and context matter more. Every canonical cluster keeps all source
surface forms, a rationale, and confidence. A wrong merge is more damaging than
leaving two names unresolved, because it corrupts every future edge attached to
that identity.
