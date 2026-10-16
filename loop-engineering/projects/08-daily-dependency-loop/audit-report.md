# Dependency audit report

## Audit run: 2026-09-01 09:00Z

- **Audit tool:** `npm audit --omit=dev --audit-level=high`
- **Result:** PASS — 0 vulnerabilities found (exit code 0)
- **Dependencies scanned:** 0 production packages. `package.json` declares no
  runtime dependencies (`private: true`, no `dependencies`/`devDependencies`),
  so there is no production dependency surface to audit.
- **`npm test`:** PASS (1/1 tests passed)
- **`npm run lint`:** PASS (lint passed)
- **Environment:** node v22.23.2, npm 10.9.8

No fixes or upgrades are required at this time.