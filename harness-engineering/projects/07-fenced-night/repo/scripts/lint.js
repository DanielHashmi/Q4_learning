// scripts/lint.js — real, tiny linter (no deps)
// Checks: unused `const` declarations, and a leading UTF-8 BOM on files
// where a BOM can silently break parsing (YAML frontmatter, JSON).
import fs from "node:fs";

const jsFiles = ["src/index.js"];
const bomSensitiveFiles = [
  ".claude/agents/reviewer.md",
  ".opencode/agent/reviewer.md",
  ".claude/settings.json",
  "opencode.json",
];

let failed = false;

for (const file of jsFiles) {
  const src = fs.readFileSync(file, "utf8");
  const declRe = /\bconst\s+(\w+)\s*=/g;
  let m;
  const decls = [];
  while ((m = declRe.exec(src))) decls.push(m[1]);
  for (const name of decls) {
    const uses = (src.match(new RegExp(`\\b${name}\\b`, "g")) || []).length;
    if (uses <= 1) {
      console.error(`${file}: '${name}' is declared but never used`);
      failed = true;
    }
  }
}

for (const file of bomSensitiveFiles) {
  if (!fs.existsSync(file)) continue;
  const buf = fs.readFileSync(file);
  const hasBom = buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf;
  if (hasBom) {
    console.error(`${file}: has a leading UTF-8 BOM — strip it, it can break YAML/JSON parsing`);
    failed = true;
  }
}

if (failed) process.exit(1);
console.log("lint: clean");
