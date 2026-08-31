# Queue item: divide-by-zero

**Status:** open

**Spec:** `divide(a, b)` in `math.js` must throw an `Error` when `b === 0`,
and otherwise return `a / b`. Right now it just returns `Infinity`/`NaN`/
whatever JS division does on zero, which violates the spec.

**Acceptance:** `npm test` passes. Fix only `divide`. Make no other changes
to `math.js`.
