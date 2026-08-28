# Project 3: First Extraction

This project turns three real project READMEs into schema-constrained graph
records. The documents are not fabricated samples: they are the README files
for Projects 3, 8, and 12 of the existing loop-engineering portfolio.

## The pipeline

```text
documents -> extraction prompt / local extractor -> JSON contract -> duplicate report
```

`prompt.md` is the model prompt. `extract.py --mode opencode` prepares one
request per document for OpenCode and validates the JSON response. The default
`--mode offline` is a deterministic, zero-cost extractor based on explicit
rules. It is useful in CI and teaches the same contract without pretending that
a model call happened.

## Run

```bash
python3 extract.py --mode offline
python3 validate.py
bash validate-jq.sh
```

On Windows:

```powershell
py extract.py --mode offline
py validate.py
```

The output is written to `output/` and the duplicate report to
`output/duplicates.json`. Every entity keeps its original `surface_form` and
the document/line where it appeared. We do not merge aliases in this project;
that is Project 5's resolution drill.

To use OpenCode with a configured provider:

```bash
python3 extract.py --mode opencode
```

`validate-jq.sh` is the assignment-faithful response gate: it uses `jq` to
reject malformed records before the duplicate report is trusted. The command
fails closed if OpenCode returns non-JSON or schema-invalid data.
No result is trusted merely because the CLI exited successfully.

## What to learn

Extraction answers: “What typed pieces appear in this document?” It does not
answer: “Which two names are the same real entity?” Keeping those jobs separate
prevents an early, confident false merge. Notice the duplicate report: the
same memory concept appears as `progress.md`, `spine`, and `committed spine`.
Those are surface forms, not yet one canonical identity.
