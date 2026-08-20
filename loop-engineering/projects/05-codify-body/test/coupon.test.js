import test from "node:test";
import assert from "node:assert/strict";
import { calculateTotal } from "../src/coupon.js";

const today = new Date("2026-01-01");

test("applies the active SAVE10 coupon", () => {
  assert.equal(
    calculateTotal(100, { code: "SAVE10", expiresOn: "2026-12-31" }, today),
    90,
  );
});

test("does not apply a different coupon code", () => {
  assert.equal(
    calculateTotal(100, { code: "NOT-A-COUPON", expiresOn: "2026-12-31" }, today),
    100,
  );
});

test("does not apply an expired coupon", () => {
  assert.equal(
    calculateTotal(100, { code: "SAVE10", expiresOn: "2025-12-31" }, today),
    100,
  );
});

test("returns the subtotal when no coupon is provided", () => {
  assert.equal(calculateTotal(42, undefined, today), 42);
});
