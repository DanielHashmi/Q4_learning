# Project 1: Draw Your Real System

This is the first graph-engineering project. It maps the loop-engineering
projects that already exist in this repository into a governance graph.

The important distinction is between:

- a **node**, a thing we can name and inspect (loop, checker, file, gate, or
  anchor); and
- an **edge**, a directed, labeled relationship such as `reads`, `checks`, or
  `gated_by`.

The graph is deliberately stored twice: `system.json` is machine-readable and
`system.mmd` is the human-readable Mermaid view. The JSON is the source of
truth; the Mermaid file is a teaching view that can be rendered by GitHub or
any Mermaid viewer.

## What this maps

The inventory names the real loop projects in `../projects/`:

- the scheduled morning brief and daily dependency loop;
- the fix loop and its OpenCode PR review loop;
- the break-it loop and its independent verification;
- the two-routine approval gate; and
- the dreaming loop that proposes improvements from committed history.

It also records the durable files and human decisions that connect them.

## Run it

From this directory:

```bash
python3 validate.py
```

On Windows, the equivalent is:

```powershell
py validate.py
```

The validator checks node types, unique IDs, valid edge endpoints, non-empty
edge labels, and the two required observations from the assignment:

1. a finding that exists only in an agent transcript; and
2. an optimizing loop with no counter-metric watcher.

Both observations are marked with `risk: true` in `system.json`. They are not
claims that the system is broken; they are the gaps this course asks us to make
visible before we build shared memory.

## What to study

The transcript-only finding demonstrates why prose logs are not shared memory:
another loop cannot reliably query or cite it. The unobserved throughput metric
demonstrates a governance problem: an optimizer can improve its number while a
different, more important outcome quietly gets worse.

Project 2 will convert real durable findings into claims with provenance. That
will replace the transcript-only placeholder with a record that a later agent
can query and verify.
