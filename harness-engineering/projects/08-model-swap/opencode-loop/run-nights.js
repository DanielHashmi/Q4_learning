#!/usr/bin/env node
/**
 * run-nights.js — Project 8 capstone orchestrator
 *
 * Runs three nights of the hardened OpenCode loop against real Gemini models.
 * Each night uses a different model pair (coder vs reviewer), exposes the
 * behaviour-coupling failure mode, applies a contract-coupling fix, and
 * commits the result.
 *
 * Usage:  node run-nights.js [--night 1|2|3]   (default: all three)
 */

const { execSync, spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

// ── model pairs (coder, reviewer) ─────────────────────────────────────────
const NIGHTS = [
  {
    n: 1,
    label: "divide-by-zero",
    coderModel: "google/gemini-2.5-flash",
    reviewerModel: "google/gemini-2.5-flash-lite",
    queueFile: "queue/night-1-divide.md",
    setupFn: setupNight1,
    prompt: `Read queue/night-1-divide.md. Fix divide() in math.js so that divide(1,0) throws an Error and divide(10,2) returns 5. Run npm test to confirm. Then run npm run lint. Commit with: git add math.js && git commit -m "fix: divide throws on zero [night-1]"`,
  },
  {
    n: 2,
    label: "average-empty-array",
    coderModel: "google/gemini-2.5-flash-lite",
    reviewerModel: "google/gemini-2.5-flash",
    queueFile: "queue/night-2-average.md",
    setupFn: setupNight2,
    prompt: `Read queue/night-2-average.md. Add average(arr) to math.js so that average([]) throws Error("empty array") and average([2,4,6]) returns 4. Run npm test to confirm. Then run npm run lint. Commit with: git add math.js test.js && git commit -m "feat: average throws on empty [night-2]"`,
  },
  {
    n: 3,
    label: "factorial-negative",
    coderModel: "google/gemini-2.5-flash",
    reviewerModel: "google/gemini-2.5-flash-lite",
    queueFile: "queue/night-3-factorial.md",
    setupFn: setupNight3,
    prompt: `Read queue/night-3-factorial.md. Add factorial(n) to math.js so that factorial(-1) throws Error("negative input") and factorial(5) returns 120 and factorial(0) returns 1. Run npm test to confirm. Then run npm run lint. Commit with: git add math.js test.js && git commit -m "feat: factorial throws on negative [night-3]"`,
  },
];

// ── night setup functions (inject buggy state + expand test.js) ───────────

function setupNight1() {
  // math.js already has the buggy divide from baseline commit — no changes needed
  log("  [setup] night-1: buggy divide already in place");
}

function setupNight2() {
  // Append a buggy average to math.js and add its tests
  const mathPath = "math.js";
  const math = fs.readFileSync(mathPath, "utf8");
  if (!math.includes("function average")) {
    fs.appendFileSync(
      mathPath,
      `\nfunction average(arr) {\n  return arr.reduce((a, b) => a + b, 0) / arr.length;\n}\n\nmodule.exports = { divide, average };\n`
    );
    // Fix the module.exports line (remove duplicate)
    let fixed = fs.readFileSync(mathPath, "utf8");
    fixed = fixed.replace(
      /module\.exports = \{ divide \};\s*\nfunction average/,
      "function average"
    );
    // Rewrite exports at end
    fixed = fixed.replace(/module\.exports[\s\S]*$/, "module.exports = { divide, average };\n");
    fs.writeFileSync(mathPath, fixed);
  }
  // Expand test.js with average tests
  const testPath = "test.js";
  const test = fs.readFileSync(testPath, "utf8");
  if (!test.includes("average")) {
    const extra = `
const { average } = require("./math.js");
let threw2 = false;
try { average([]); } catch(e) { threw2 = true; }
if (!threw2) { console.error("FAIL: average([]) should throw"); process.exit(1); }
if (average([2,4,6]) !== 4) { console.error("FAIL: average([2,4,6]) should be 4"); process.exit(1); }
console.log("average tests passed");
`;
    // Insert before final process.exit(0)
    const patched = test.replace("process.exit(0);", extra + "\nprocess.exit(0);");
    fs.writeFileSync(testPath, patched);
  }
  log("  [setup] night-2: buggy average appended to math.js, tests expanded");
}

function setupNight3() {
  // Append a buggy factorial to math.js and add its tests
  const mathPath = "math.js";
  const math = fs.readFileSync(mathPath, "utf8");
  if (!math.includes("function factorial")) {
    let fixed = math.replace(
      /module\.exports = \{[^}]+\};?\s*$/,
      ""
    ).trim();
    fixed += `\n\nfunction factorial(n) {\n  if (n === 0) return 1;\n  return n * factorial(n - 1); // BUG: no guard for n < 0 → infinite recursion\n}\n\nmodule.exports = { divide, average, factorial };\n`;
    fs.writeFileSync(mathPath, fixed);
  }
  // Expand test.js with factorial tests
  const testPath = "test.js";
  const test = fs.readFileSync(testPath, "utf8");
  if (!test.includes("factorial")) {
    const extra = `
const { factorial } = require("./math.js");
let threw3 = false;
try { factorial(-1); } catch(e) { threw3 = true; }
if (!threw3) { console.error("FAIL: factorial(-1) should throw"); process.exit(1); }
if (factorial(5) !== 120) { console.error("FAIL: factorial(5) should be 120"); process.exit(1); }
if (factorial(0) !== 1) { console.error("FAIL: factorial(0) should be 1"); process.exit(1); }
console.log("factorial tests passed");
`;
    const patched = test.replace("process.exit(0);", extra + "\nprocess.exit(0);");
    fs.writeFileSync(testPath, patched);
  }
  log("  [setup] night-3: buggy factorial appended to math.js, tests expanded");
}

// ── helpers ───────────────────────────────────────────────────────────────

function log(msg) {
  const ts = new Date().toISOString();
  const line = `[${ts}] ${msg}`;
  console.log(line);
  fs.appendFileSync("logs/run-nights.log", line + "\n");
}

function setReviewerModel(model) {
  const agentPath = ".opencode/agent/reviewer.md";
  let content = fs.readFileSync(agentPath, "utf8");
  content = content.replace(/^model: .+$/m, `model: ${model}`);
  fs.writeFileSync(agentPath, content);
  log(`  [config] reviewer model → ${model}`);
}

function runOpenCode(model, prompt, label) {
  log(`  [opencode] coder=${model} running: ${label}`);
  const result = spawnSync(
    "opencode",
    ["run", "-m", model, "--auto", "--format", "json", prompt],
    { encoding: "utf8", timeout: 300_000, maxBuffer: 10 * 1024 * 1024 }
  );

  const logFile = `logs/night-${label}-coder.log`;
  fs.writeFileSync(logFile, (result.stdout || "") + "\n---STDERR---\n" + (result.stderr || ""));

  if (result.status !== 0) {
    log(`  [opencode] FAILED (exit ${result.status}) — see ${logFile}`);
    return false;
  }
  log(`  [opencode] coder run complete → ${logFile}`);
  return true;
}

function runReviewer(reviewerModel, label) {
  log(`  [reviewer] model=${reviewerModel}`);
  const prompt = `Run npm test and npm run lint. Then run git diff HEAD~1 to see what changed. Return a JSON verdict: { "verdict": "PASS" or "FAIL", "reasons": [], "risk": "low" or "high" }`;

  const result = spawnSync(
    "opencode",
    ["run", "--agent", "reviewer", "-m", reviewerModel, "--auto", "--format", "json", prompt],
    { encoding: "utf8", timeout: 120_000, maxBuffer: 5 * 1024 * 1024 }
  );

  const logFile = `logs/night-${label}-reviewer.log`;
  fs.writeFileSync(logFile, (result.stdout || "") + "\n---STDERR---\n" + (result.stderr || ""));

  // Extract JSON verdict from output (contract-coupling: strip markdown fences)
  const raw = result.stdout || "";
  const cleaned = raw.replace(/```json\s*/g, "").replace(/```\s*/g, "");
  const match = cleaned.match(/\{[\s\S]*?"verdict"[\s\S]*?\}/);
  if (!match) {
    log(`  [reviewer] WARNING: could not parse JSON verdict — see ${logFile}`);
    return { verdict: "UNKNOWN", reasons: ["could not parse reviewer output"], risk: "high" };
  }
  try {
    const verdict = JSON.parse(match[0]);
    log(`  [reviewer] verdict=${verdict.verdict} risk=${verdict.risk}`);
    return verdict;
  } catch {
    log(`  [reviewer] WARNING: JSON parse error — raw match: ${match[0]}`);
    return { verdict: "UNKNOWN", reasons: ["JSON parse error"], risk: "high" };
  }
}

function markDone(label) {
  let spine = fs.readFileSync("progress.md", "utf8");
  spine = spine.replace(`- [ ] ${label}`, `- [x] ${label}`);
  // Add to Done section
  spine = spine.replace(
    "## Done\n",
    `## Done\n- ${label} (${new Date().toISOString()})\n`
  );
  fs.writeFileSync("progress.md", spine);
  log(`  [progress] marked ${label} done in progress.md`);
}

function markEscalated(label, reason) {
  let spine = fs.readFileSync("progress.md", "utf8");
  const ts = new Date().toISOString();
  spine = spine.replace(
    "## Open / needs a human\n(escalations land here — model, reason, timestamp)",
    `## Open / needs a human\n- ${label}: ${reason} (${ts})`
  );
  fs.writeFileSync("progress.md", spine);
  log(`  [escalate] ${label} → Open/needs-human: ${reason}`);
}

function appendRatchet(night, coderModel, reviewerModel, verdict, testsPass) {
  const row = `| night-${night} | ${coderModel} | ${reviewerModel} | ${testsPass ? "✅" : "❌"} | ${verdict.verdict} | ${verdict.risk} | ${(verdict.reasons || []).join("; ") || "—"} |`;
  const ratchetPath = "logs/ratchet.md";
  if (!fs.existsSync(ratchetPath)) {
    fs.writeFileSync(
      ratchetPath,
      "# Ratchet log\n\n| Night | Coder | Reviewer | Tests | Verdict | Risk | Reasons |\n|---|---|---|---|---|---|---|\n"
    );
  }
  fs.appendFileSync(ratchetPath, row + "\n");
  log(`  [ratchet] appended row for night-${night}`);
}

function testsPass() {
  const r = spawnSync("node", ["test.js"], { encoding: "utf8" });
  return r.status === 0;
}

// ── main loop ─────────────────────────────────────────────────────────────

async function main() {
  fs.mkdirSync("logs", { recursive: true });
  log("=== Project 8 Model-Swap Capstone — Starting ===");

  const onlyNight = process.argv.includes("--night")
    ? parseInt(process.argv[process.argv.indexOf("--night") + 1], 10)
    : null;

  for (const night of NIGHTS) {
    if (onlyNight && night.n !== onlyNight) continue;

    log(`\n${"=".repeat(60)}`);
    log(`NIGHT ${night.n}: ${night.label}`);
    log(`  coder  → ${night.coderModel}`);
    log(`  reviewer → ${night.reviewerModel}`);
    log(`${"=".repeat(60)}`);

    // 1. Setup: inject buggy state + expand tests
    night.setupFn();

    // 2. Confirm tests are RED before agent runs
    const redBefore = !testsPass();
    log(`  [verify] tests RED before run: ${redBefore}`);
    if (!redBefore) {
      log(`  [skip] tests already pass — night ${night.n} already done, skipping`);
      continue;
    }

    // 3. Patch reviewer model in .opencode/agent/reviewer.md
    setReviewerModel(night.reviewerModel);

    // 4. Run the coder agent (constrain verb: opencode.json permissions, inform verb: queue file, correct verb: tests)
    const coderOk = runOpenCode(night.coderModel, night.prompt, `${night.n}-${night.label}`);

    // 5. Verify tests pass (contract: exit code)
    const green = testsPass();
    log(`  [verify] tests GREEN after coder run: ${green}`);

    // 6. Run reviewer subagent (verify verb)
    const verdict = runReviewer(night.reviewerModel, `${night.n}-${night.label}`);

    // 7. Append to ratchet log
    appendRatchet(night.n, night.coderModel, night.reviewerModel, verdict, green);

    // 8. Escalate or mark done (escalate/correct verbs)
    if (!green || verdict.verdict === "FAIL" || verdict.risk === "high") {
      markEscalated(
        `night-${night.n}-${night.label}`,
        `tests=${green}, verdict=${verdict.verdict}, risk=${verdict.risk}: ${(verdict.reasons || []).join("; ")}`
      );
      log(`  ⚠️  Night ${night.n} ESCALATED — human review needed`);
    } else {
      markDone(`night-${night.n}-${night.label}`);
      log(`  ✅  Night ${night.n} DONE`);
    }
  }

  log("\n=== All nights complete. See logs/ratchet.md and progress.md ===");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
