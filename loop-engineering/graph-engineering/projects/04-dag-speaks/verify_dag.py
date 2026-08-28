#!/usr/bin/env python3
"""Project 4 integration test with two independent descendants of the root."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from graph import descendants, frontier, git, lineage  # noqa: E402

def run(*args, cwd, env):
    subprocess.run(["git", *args], cwd=cwd, env=env, check=True, stdout=subprocess.DEVNULL)

with tempfile.TemporaryDirectory(prefix="graph-dag-") as directory:
    env = os.environ.copy()
    env.update({"GIT_AUTHOR_NAME":"Graph Test","GIT_AUTHOR_EMAIL":"graph@example.invalid","GIT_COMMITTER_NAME":"Graph Test","GIT_COMMITTER_EMAIL":"graph@example.invalid"})
    run("init", "-q", cwd=directory, env=env)
    state = Path(directory) / "state.txt"
    state.write_text("root\n", encoding="utf-8")
    run("add", ".", cwd=directory, env=env)
    run("commit", "-qm", "root", cwd=directory, env=env)
    root = git("rev-parse", "HEAD", cwd=directory)
    run("checkout", "-qb", "experiment", cwd=directory, env=env)
    state.write_text("experiment\n", encoding="utf-8")
    run("commit", "-qam", "experiment", cwd=directory, env=env)
    experiment_tip = git("rev-parse", "HEAD", cwd=directory)
    run("checkout", "-q", "-", cwd=directory, env=env)
    state.write_text("main\n", encoding="utf-8")
    run("commit", "-qam", "main", cwd=directory, env=env)
    main_tip = git("rev-parse", "HEAD", cwd=directory)
    assert {main_tip, experiment_tip}.issubset(set(descendants(root, directory)))
    assert set(frontier(directory)) == {main_tip, experiment_tip}
    assert lineage(root, main_tip, directory) == [main_tip]
print("Project 4 DAG verification passed: descendants, frontier, and lineage")
