# Queue item: average-empty-array

**Status:** open

**Spec:** Add `average(arr)` to `math.js`. It must:
- Return the arithmetic mean of a non-empty number array
- Throw `Error("empty array")` when `arr.length === 0`
- Never return `NaN` or `Infinity`

**Acceptance:** `npm test` exits 0 (including existing divide tests).
Add only `average`. Do not touch `divide`.
