const { add } = require("./math.js");
if (add(2, 3) !== 5) { console.error("FAIL: add(2,3)"); process.exit(1); }
console.log("all tests passed");
process.exit(0);
