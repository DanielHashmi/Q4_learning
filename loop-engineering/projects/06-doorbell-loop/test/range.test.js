const test = require("node:test");
const assert = require("node:assert/strict");
const { firstN } = require("../src/range");

test("returns exactly the requested number of items", () => {
  assert.deepEqual(firstN(["a", "b", "c", "d"], 3), ["a", "b", "c"]);
});

test("allows zero", () => {
  assert.deepEqual(firstN(["a"], 0), []);
});
