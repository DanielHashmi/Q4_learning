# Project 8: Two Loops, One Graph

This capstone is the complete memory-graph build:

```text
triage loop -> claims + runs + raw tool evidence
                         |
                         v
                 changelog loop -> two-hop context -> grounded reviewer
```

The graph is deliberately ordinary files so it remains free and inspectable:

- `graph/entities.json` stores identities;
- `graph/claims.json` stores append-only facts;
- `graph/runs.json` links beats to their evidence; and
- `evidence/` stores captured output from Git, not model prose.

## Run the real capstone rehearsal

```bash
python3 two_run_demo.py
```

The demo creates a separate throwaway Git repository under the system temp
directory, creates a real commit that fixes a TODO, runs the triage loop against
that repository, commits the graph through a pre-commit guard, and asks the
changelog loop for a two-hop context. It then deliberately tampers with an old
claim and proves the guard rejects the mutation. The main repository is not
used as the mutable test target.

## What proves completion

The final result includes:

1. a changelog line grounded in a claim ID;
2. a path from that claim to its producing run and captured Git output;
3. a runtime-derived `REVISE` counter-metric watched by the reviewer loop; and
4. a failed append-only tamper attempt.

The changelog loop never runs the original Git command. It only reads the
graph's two-hop context. `two_run_demo.py` proves this across separate first
and second workspaces: the second workspace has graph memory and evidence but
no source checkout.
