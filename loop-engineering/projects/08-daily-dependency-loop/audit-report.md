# Dependency audit report

## Audit date

- Date: 2026-09-21 (UTC)
- Environment: Node v22.23.2, npm v10.9.8

## Production dependency inventory

- `package.json` declares no `dependencies` and no `devDependencies`; the only
  scripts are `test` (`node --test`) and `lint` (`node scripts/lint.js`).
- `package-lock.json` is lockfileVersion 3 and resolves to the root package
  only — the installed dependency tree is empty.

## Checks

- `npm test` — PASS (1/1 test).
- `npm run lint` — PASS.
- `npm audit --omit=dev --audit-level=high` — 0 vulnerabilities (exit 0).

## Findings

- No production or dev dependencies are installed, so there are no known
  vulnerabilities, no outdated transitive packages, and no supply-chain
  exposure to audit.
- Keep the lockfile in sync if dependencies are ever added: run
  `npm install` and re-run `npm audit` before merging.

## Verdict

- Status: CLEAN
- Action required: none