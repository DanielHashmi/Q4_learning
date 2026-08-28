#!/usr/bin/env python3
"""Small, testable wrappers around Git's commit-DAG traversal primitives."""
from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict


def git(*args: str, cwd: str = ".") -> str:
    result = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def descendants(base: str, cwd: str = ".") -> list[str]:
    text = git("rev-list", "--all", "--ancestry-path", f"{base}..", cwd=cwd)
    return text.splitlines() if text else []


def frontier(cwd: str = ".") -> list[str]:
    commits = git("rev-list", "--all", cwd=cwd).splitlines()
    children: dict[str, set[str]] = defaultdict(set)
    for commit in commits:
        parents = git("rev-list", "--parents", "-n", "1", commit, cwd=cwd).split()[1:]
        for parent in parents:
            children[parent].add(commit)
    return sorted(commit for commit in commits if not children[commit])


def lineage(base: str, target: str = "HEAD", cwd: str = ".") -> list[str]:
    text = git("rev-list", "--reverse", "--ancestry-path", f"{base}..{target}", cwd=cwd)
    return text.splitlines() if text else []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD~3")
    parser.add_argument("--target", default="HEAD")
    parser.add_argument("--frontier", action="store_true")
    parser.add_argument("--cwd", default=".")
    args = parser.parse_args()
    if args.frontier:
        print("\n".join(frontier(args.cwd)))
        return
    print("descendants:")
    print("\n".join(descendants(args.base, args.cwd)) or "(none)")
    print("lineage:")
    print("\n".join(lineage(args.base, args.target, args.cwd)) or "(none)")


if __name__ == "__main__":
    main()
