import { add, multiply, isEven } from './math.js';

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  ${error.message}`);
    failed++;
  }
}

function assertEquals(actual, expected) {
  if (actual !== expected) {
    throw new Error(`Expected ${expected}, got ${actual}`);
  }
}

console.log('Running tests...\n');

test('add(2, 3) should return 5', () => {
  assertEquals(add(2, 3), 5);
});

test('multiply(4, 5) should return 20', () => {
  assertEquals(multiply(4, 5), 20);
});

test('isEven(4) should return true', () => {
  assertEquals(isEven(4), true);
});

console.log(`\n${passed} passed, ${failed} failed`);

// Exit with error code if any tests failed
process.exit(failed > 0 ? 1 : 0);
