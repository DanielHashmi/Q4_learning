---
name: project-05-body
description: Runs one isolated Project 5 candidate through the maker-checker body.
---

# Project 5 body procedure

1. Treat the current worktree as the only source of truth.
2. Read the production module and tests before editing.
3. Change only `src/coupon.js` when the candidate asks for a fix.
4. Never weaken, delete, or rewrite tests or project infrastructure.
5. Run `npm test` and `npm run lint` after a maker change.
6. Leave the candidate uncommitted for the reviewer.
7. Do not inspect git history, other worktrees, or previous artifacts.
8. Report the changed files and exact verification results.
