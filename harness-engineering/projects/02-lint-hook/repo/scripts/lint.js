import fs from "node:fs";
import path from "node:path";

const targets = process.argv.slice(2);
const files = targets.length ? targets : fs.readdirSync("src").map(f => path.join("src", f));

let errors = [];
for (const file of files) {
  if (!file.endsWith(".js")) continue;
  const text = fs.readFileSync(file, "utf8");
  const decls = [...text.matchAll(/\b(?:const|let)\s+([a-zA-Z_$][\w$]*)\s*=/g)].map(m => m[1]);
  for (const name of decls) {
    const usage = new RegExp(`\\b${name}\\b`, "g");
    const count = (text.match(usage) || []).length;
    if (count <= 1) {
      errors.push(`${file}: '${name}' is assigned a value but never used.`);
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
