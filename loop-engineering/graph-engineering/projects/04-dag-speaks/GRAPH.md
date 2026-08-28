# Git DAG queries for future agents

These commands use only Git. Replace `BASE` with the commit being investigated.

## 1. What was tried on top of BASE?

```bash
git log --all --ancestry-path --oneline BASE.. --decorate
```

This lists reachable descendants of `BASE`, including work on side branches.

## 2. What are the unexplored frontier tips?

```bash
git for-each-ref --format='%(refname:short) %(objectname)' refs/heads refs/remotes
```

Each listed ref is a named tip. For an exact commit-level frontier, use the
project command:

```bash
python3 graph.py --frontier
```

It finds reachable commits with no reachable child. This is closer to an
AgentHub `leaves` query than simply listing branch names.

## 3. What path produced the current state?

```bash
git log --reverse --ancestry-path --oneline BASE..HEAD
```

Use `--target <commit>` with `graph.py` when the current state is not `HEAD`.

## What Git cannot answer

Git cannot show an experiment that was never committed, or a discarded working
tree that never became an object reachable from a ref. Keep that limitation in
the graph design; do not infer “not tried” from “not committed.”
