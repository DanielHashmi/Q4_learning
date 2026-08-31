const { divide } = require("./math.js");

let threw = false;
try {
  divide(1, 0);
} catch (e) {
  threw = true;
}
if (!threw) {
  console.error("FAIL: divide(1, 0) should throw, not return Infinity/NaN");
  process.exit(1);
}
if (divide(10, 2) !== 5) {
  console.error("FAIL: divide(10, 2) should be 5");
  process.exit(1);
}

console.log("all tests passed");
process.exit(0);
