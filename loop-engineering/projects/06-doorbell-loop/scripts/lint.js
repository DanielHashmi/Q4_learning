const fs = require("node:fs");
const path = require("node:path");

for (const relative of ["src/range.js", "test/range.test.js"]) {
  const file = path.join(__dirname, "..", relative);
  const source = fs.readFileSync(file, "utf8");
  new Function(source.replace(/module\.exports\s*=.*$/m, ""));
}

console.log("lint passed");
