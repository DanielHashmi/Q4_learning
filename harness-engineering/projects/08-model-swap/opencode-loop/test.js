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


const { average } = require("./math.js");
let threw2 = false;
try { average([]); } catch(e) { threw2 = true; }
if (!threw2) { console.error("FAIL: average([]) should throw, not return NaN"); process.exit(1); }
if (average([2, 4, 6]) !== 4) { console.error("FAIL: average([2,4,6]) should be 4"); process.exit(1); }
console.log("average tests passed");

const { factorial } = require("./math.js");
let threw3 = false;
let threw3Msg = "";
try { factorial(-1); } catch(e) { threw3 = true; threw3Msg = e.message; }
if (!threw3) { console.error("FAIL: factorial(-1) should throw, not recurse forever"); process.exit(1); }
if (threw3Msg !== "negative input") { console.error("FAIL: factorial(-1) should throw Error('negative input'), got: " + threw3Msg); process.exit(1); }
if (factorial(5) !== 120) { console.error("FAIL: factorial(5) should be 120"); process.exit(1); }
if (factorial(0) !== 1)   { console.error("FAIL: factorial(0) should be 1");   process.exit(1); }
console.log("factorial tests passed");
console.log("all tests passed");
process.exit(0);
