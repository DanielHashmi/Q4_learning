# Project 4: The DAG Speaks

Git already stores a durable directed acyclic graph of work. This project
turns three useful questions into tested commands:

1. What commits were tried on top of a known commit?
2. Which commits are current unexplored frontier tips?
3. What commit path produced the current state?

The implementation uses Git's own object database and traversal commands; it
does not parse commit prose or depend on an agent transcript. `GRAPH.md` is the
copy-paste interface future agents can use.

## Run

```bash
python3 graph.py --base HEAD~3 --target HEAD
python3 verify.py
```

On Windows use `py` instead of `python3`.

The verifier creates a temporary repository with a branch and a side branch,
then checks descendants, frontier tips, and a lineage path. This proves the
queries rather than merely printing them against the current repository.

## The boundary

The DAG tells us what was committed and how committed work descends from prior
work. It cannot tell us which uncommitted experiments were tried and thrown
away. That absence is not a bug in the query; it is information Git never
received. Project 5 will work on a different problem: deciding when two names
in extracted facts refer to the same entity.
