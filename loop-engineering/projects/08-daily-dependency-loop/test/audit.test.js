const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
test("audit report has the required heading", () => {
  assert.match(fs.readFileSync("audit-report.md", "utf8"), /^# Dependency audit report/m);
});
