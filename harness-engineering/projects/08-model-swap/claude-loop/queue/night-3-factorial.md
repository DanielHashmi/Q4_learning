# Queue item: factorial-negative

**Status:** open

**Spec:** Add `factorial(n)` to `math.js`. It must:
- Return `n!` for non-negative integers (`0! = 1`)
- Throw `Error("negative input")` when `n < 0`
- Never recurse infinitely or return `NaN`

**Acceptance:** `npm test` exits 0 (including divide and average tests).
The test checks `e.message === "negative input"` — a stack overflow
(`RangeError`) does NOT pass.
Add only `factorial`. Do not touch `divide` or `average`.
