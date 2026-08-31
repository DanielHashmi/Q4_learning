// Lint check: unused variable heuristic on math.js
const fs = require("node:fs");

const targets = process.argv.slice(2).length
  ? process.argv.slice(2)
  : ["math.js"];

let errors = [];
for (const file of targets) {
  if (!fs.existsSync(file) || !file.endsWith(".js")) continue;
  const text = fs.readFileSync(file, "utf8");
  const decls = [...text.matchAll(/\b(?:const|let)\s+([a-zA-Z_$][\w$]*)\s*=/g)].map(m => m[1]);
  for (const name of decls) {
    const usage = new RegExp(`\\b${name}\\b`, "g");
    const count = (text.match(usage) || []).length;
    if (count <= 1) {
      errors.push(`${file}: '${name}' is assigned but never used.`);
    }
  }
}

if (errors.length) {
  console.error("lint: " + errors.length + " problem(s)");
  for (const e of errors) console.error("  " + e);
  process.exit(1);
}
console.log("lint: clean");
process.exit(0);
