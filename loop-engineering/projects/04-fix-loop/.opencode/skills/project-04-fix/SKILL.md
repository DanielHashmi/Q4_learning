---
name: project-04-fix
description: Runs the Project 4 safe fix procedure: isolate one candidate, make the smallest fix, verify it, and send it to a read-only checker before any PR is created.
---

# Project 4 safe fix procedure

Use this skill for the Project 4 coupon-validation candidate only.

1. Read the production module and tests before editing.
2. Work only in the current isolated checkout.
3. Change only `src/coupon.js`; do not edit tests, workflows, agent files, or scripts.
4. Preserve the tests as the specification. Never weaken or delete a failing test.
5. Run `npm test` and `npm run lint` after the change.
6. Leave commits, pushes, and PR creation to the outer orchestrator.
7. Report the changed file and verification results; do not claim success without running both commands.
