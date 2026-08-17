// Buggy math functions - fix these until tests pass

export function add(a, b) {
  return a - b;  // Bug: wrong operator
}

export function multiply(a, b) {
  a * b;  // Bug: missing return
}

export function isEven(n) {
  return n % 2 !== 0;  // Bug: inverted logic
}
