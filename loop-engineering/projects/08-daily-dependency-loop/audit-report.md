# Dependency audit report

**Date:** 2026-09-29
**Run ID:** 20260929T101355Z-36554252986
**Scope:** production dependencies of the project root manifest
**Toolchain:** node v22.23.2 / npm 10.9.8

## Result

**PASS** — no action required, no dependency changes made.

## Commands

| Command | Exit | Output |
| --- | --- | --- |
| `npm audit --omit=dev --audit-level=high` | 0 | `found 0 vulnerabilities` |
| `npm test` | 0 | 1 passed, 0 failed |
| `npm run lint` | 0 | `lint passed` |

## Dependency inventory

`package.json` declares no `dependencies` and no `devDependencies`; the
project is `private` and ships only the standard-library test/lint scripts
(`node --test`, `node scripts/lint.js`). `npm ls --omit=dev --all` resolves to
an empty tree, so the zero-vulnerability result is structurally expected rather
than the result of suppressed advisories.

## Adjacent manifest

The nested `.opencode/` directory carries its own independent
`package.json`/lockfile for agent tooling with a single pinned dependency,
`@opencode-ai/plugin@1.18.33`. It sits outside the root audit path, so
`npm audit --omit=dev --audit-level=high` at the project root does not cover it.
Run separately it also reports `found 0 vulnerabilities`. Recorded here so the
zero-finding result is not misread as covering the whole tree.

## Findings

- No high or critical advisories in production scope.
- No drift between `package.json` and `package-lock.json` (lockfile v3, no
  entries beyond the root package).
- Nothing to upgrade; no manifest or lockfile was modified in this run.

## Changes in this run

`audit-report.md` only. `progress.md`, workflows, source files, and all package
manifests are untouched.
