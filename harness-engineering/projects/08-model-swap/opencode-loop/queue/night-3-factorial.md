# Queue item: factorial-negative

**Status:** open

**Spec:** Add `factorial(n)` to `math.js`. It must:
- Return `n!` for non-negative integers (0! = 1)
- Throw an `Error` with message "negative input" when `n < 0`
- NOT return `NaN`, `Infinity`, or incorrect values for edge cases

**Acceptance:** `npm test` passes (test.js already contains the factorial tests).
Fix only `factorial`. Do not touch `divide` or `average`.
