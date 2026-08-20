# Project 5: Codify the Body

**Difficulty:** Medium to hard
**Concepts:** workflow body, worktree isolation, maker-checker

## In everyday words

Project 4 showed how to safely handle one fix. Project 5 puts that process into
one reusable machine:

1. Prepare several candidate problems.
2. Give each problem its own temporary workspace.
3. Let a maker try the fix.
4. Let a read-only checker judge the result.
5. Enforce tests, lint, and file-scope rules outside the agents.
6. Report every result and clean up the temporary workspaces.

You run the machine yourself. It does not wake itself up later and it does not
remember previous runs. That is deliberate. A heartbeat would make it start
automatically, and a spine such as `progress.md` would give it memory. Those
parts are outside this project.

## Run it

Requirements: Git, Node.js, Python 3, Bash, and an authenticated OpenCode CLI.

The default OpenCode timeout is 90 seconds per agent with up to three retries.
For a slower local model, set `OPENCODE_TIMEOUT_SECONDS` to a larger positive
integer. The candidate work fan-out remains parallel without sharing state: each candidate
receives its own OpenCode data, config, and state directories, avoiding the local
CLI's single-writer database contention.
OpenCode's generated `.opencode/node_modules/` runtime cache is
ignored; any tracked or ordinary untracked candidate-file change still fails
the independent scope check.

From the repository root:

```bash
bash loop-engineering/projects/05-codify-body/scripts/run-body.sh
```

The body runs three candidates in parallel:

- `good`: the maker should fix the coupon bug and receive `PASS`.
- `bad`: the candidate is intentionally impossible and should receive `FAIL`.
- `scope`: an unauthorized README change is planted and must receive `FAIL`.

Run the command a second time from a fresh shell. Each run gets a new artifact
directory and does not read the previous run's artifacts, sessions, or state.

## Evidence

Each run writes ignored artifacts under:

```text
artifacts/<run-id>/
├── summary.txt
├── good/
├── bad/
└── scope/
```

The candidate folders contain maker output, reviewer output, independent test
and lint output, the verdict, and the final status. The summary explicitly says
`engine_state=stateless`.

## Done when

- One command runs all three candidates without step-by-step prompting.
- The good candidate receives `PASS`.
- The bad and scope-violating candidates receive `FAIL`.
- The reviewer cannot edit files.
- Independent checks can override an agent's claimed verdict.
- OpenCode runtime cache files do not count as a maker change, while every
  tracked or ordinary untracked candidate-file change remains in scope.
- Two fresh runs produce separate evidence without sharing memory.
- The main checkout stays clean and no branch, commit, push, or PR is left
  behind.

This is an engine, not yet a complete loop. To become a loop, it would need a
heartbeat to start it and a spine to record what earlier runs already did.
