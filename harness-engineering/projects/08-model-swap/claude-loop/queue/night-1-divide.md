# Queue item: divide-by-zero

**Status:** open

**Spec:** `divide(a, b)` in `math.js` must throw an `Error` when `b === 0`,
and otherwise return `a / b`. Right now it silently returns `Infinity`/`NaN`.

**Acceptance:** `npm test` exits 0. Fix only `divide`. No other changes to `math.js`.
