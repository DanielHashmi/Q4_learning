import { add } from "../src/index.js";
import assert from "node:assert";
try {
  assert.strictEqual(add(2, 3), 5);
  console.log("test: 1 passed");
  process.exit(0);
} catch (e) {
  console.error("test: FAILED - " + e.message);
  process.exit(1);
}
