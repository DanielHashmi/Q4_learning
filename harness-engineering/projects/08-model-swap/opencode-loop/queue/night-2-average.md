# Queue item: average-empty-array

**Status:** open

**Spec:** Add `average(arr)` to `math.js`. It must:
- Return the arithmetic mean of a non-empty number array
- Throw an `Error` with message "empty array" when `arr.length === 0`
- NOT return `NaN` or `Infinity` for edge cases

**Acceptance:** `npm test` passes (test.js already contains the average tests).
Fix only `average`. Do not touch `divide`.
