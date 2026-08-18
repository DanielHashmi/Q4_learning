export function calculateTotal(subtotal, coupon, today = new Date("2026-01-01")) {
  if (!Number.isFinite(subtotal) || subtotal < 0) {
    throw new TypeError("subtotal must be a non-negative number");
  }

  if (!coupon) {
    return subtotal;
  }

  // Intentional bug for Project 4: assignment makes every coupon look valid.
  if (coupon.code === "SAVE10") {
    const expiry = new Date(coupon.expiresOn);
    if (expiry >= today) {
      return subtotal * 0.9;
    }
  }

  return subtotal;
}
