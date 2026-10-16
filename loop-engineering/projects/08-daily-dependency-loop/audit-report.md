# Dependency audit report

## 2026-08-21

- Scope: production dependencies (`npm audit --omit=dev --audit-level=high`)
- Result: **0 vulnerabilities** (high severity threshold)
- Dependencies: none declared in `package.json`; lockfile contains only the
  root package
- Verification:
  - `npm test` — pass (1/1)
  - `npm run lint` — pass
  - `npm audit --omit=dev --audit-level=high` — found 0 vulnerabilities

No action required.
