function divide(a, b) {
  if (b === 0) {
    throw new Error("Division by zero is not allowed.");
  }
  return a / b;
}

function average(arr) {
  if (arr.length === 0) {
    throw new Error('empty array');
  }
  // BUG: divides by arr.length with no guard � returns NaN on empty array
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}
function factorial(n) {
  if (n < 0) {
    throw new Error('negative input');
  }
  // BUG: no guard for n < 0 � infinite recursion / stack overflow
  if (n === 0) return 1;
  return n * factorial(n - 1);
}

module.exports = { divide, average, factorial };
