const fs = require("node:fs");
if (!fs.readFileSync("audit-report.md", "utf8").startsWith("# Dependency audit report\n")) process.exit(1);
console.log("lint passed");
