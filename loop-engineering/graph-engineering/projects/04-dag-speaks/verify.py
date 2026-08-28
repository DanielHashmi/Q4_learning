#!/usr/bin/env python3
"""Integration-test the DAG queries against a real temporary Git repository."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from graph import descendants, frontier, git, lineage  # noqa: E402


def run(*args: str, cwd: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL)


with tempfile.TemporaryDirectory(prefix="graph-dag-") as directory:
    env = os.environ.copy()
    env.update({"GIT_AUTHOR_NAME": "Graph Test", "GIT_AUTHOR_EMAIL": "graph@example.invalid", "GIT_COMMITTER_NAME": "Graph Test", "GIT_COMMITTER_EMAIL": "graph@example.invalid"})
    run("init", "-q", cwd=directory)
    file_path = Path(directory) / "state.txt"
    file_path.write_text("root\n", encoding="utf-8")
    run("add", ".", cwd=directory)
    subprocess.run(["git", "commit", "-qm", "root"], cwd=directory, env=env, check=True)
    root = git("rev-parse", "HEAD", cwd=directory)
    file_path.write_text("main\n", encoding="utf-8")
    run("commit", "-qam", "main", cwd=directory)
    main_tip = git("rev-parse", "HEAD", cwd=directory)
    run("checkout", "-qb", "experiment", cwd=directory)
    file_path.write_text("experiment\n", encoding="utf-8")
    run("commit", "-qam", "experiment", cwd=directory)
    experiment_tip = git("rev-parse", "HEAD", cwd=directory)
    run("checkout", "-q", "master", cwd=directory)

    assert main_tip in descendants(root, directory)
    assert experiment_tip in descendants(root, directory)
    tips = set(frontier(directory))
    assert {main_tip, experiment_tip} == tips, (tips, main_tip, experiment_tip)
    assert lineage(root, main_tip, directory) == [main_tip]

print("Project 4 DAG verification passed: descendants, frontier, and lineage")
