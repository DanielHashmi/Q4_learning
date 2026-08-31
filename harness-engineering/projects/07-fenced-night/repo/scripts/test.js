// scripts/test.js — real, tiny assertion-based test (no deps)
import { add } from "../src/index.js";

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    console.error(`FAIL: ${label} — expected ${expected}, got ${actual}`);
    process.exitCode = 1;
  } else {
    console.log(`PASS: ${label}`);
  }
}

assertEqual(add(2, 3), 5, "add(2,3) === 5");
assertEqual(add(-1, 1), 0, "add(-1,1) === 0");

if (process.exitCode === 1) process.exit(1);
console.log("test: all passed");
