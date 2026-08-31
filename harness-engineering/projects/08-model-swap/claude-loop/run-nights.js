#!/usr/bin/env node
/**
 * run-nights.js — Project 8 capstone orchestrator (Claude Code edition)
 *
 * Mirrors opencode-loop/run-nights.js exactly, but uses:
 *   claude -p --model <model> --allowedTools "..." "prompt"
 * instead of:
 *   opencode run -m <model> --auto "prompt"
 *
 * Three nights, two Claude models swapping coder/reviewer roles each night.
 *
 * Usage:
 *   node run-nights.js              # run all three nights
 *   node run-nights.js --night 1   # run a single night
 *
 * Prerequisites:
 *   - claude CLI authenticated (ANTHROPIC_API_KEY or claude login)
 *   - git repo initialised in this directory (run: git init && git add -A && git commit -m "baseline")
 *   - npm available
 */

const { spawnSync } = require("node:child_process");
const fs = require("node:fs");

// ── Allowed tools passed on CLI (mirrors .claude/settings.json but explicit)
const ALLOWED_TOOLS = [
  "Edit",
  "Read",
  "Bash(npm test*)",
  "Bash(npm run lint*)",
  "Bash(node test.js*)",
  "Bash(node lint.js*)",
  "Bash(git diff*)",
  "Bash(git log*)",
  "Bash(git status*)",
  "Bash(git add*)",
  'Bash(git commit -m *)',
].join(",");

const REVIEWER_TOOLS = [
  "Read",
  "Bash(npm test*)",
  "Bash(npm run lint*)",
  "Bash(git diff*)",
  "Bash(git log*)",
].join(",");

// ── Model pairs (coder, reviewer) — swap each night ──────────────────────────
//
// Adjust model names to match what your Claude auth token can access:
//   - claude-haiku-4-5         (fast, cheap)
//   - claude-sonnet-4-5        (balanced)
//   - claude-3-5-haiku-20241022
//   - claude-3-5-sonnet-20241022
//
const NIGHTS = [
  {
    n: 1,
    label: "divide-by-zero",
    coderModel:    "claude-haiku-4-5",
    reviewerModel: "claude-sonnet-4-5",
    setupFn: setupNight1,
    prompt: `Read queue/night-1-divide.md. Fix divide() in math.js so that divide(1,0) throws an Error and divide(10,2) returns 5. Run npm test to confirm it passes. Then run npm run lint. Then stage and commit: git add math.js && git commit -m "fix: divide throws on zero [night-1]"`,
  },
  {
    n: 2,
    label: "average-empty-array",
    coderModel:    "claude-sonnet-4-5",
    reviewerModel: "claude-haiku-4-5",
    setupFn: setupNight2,
    prompt: `Read queue/night-2-average.md. Fix average(arr) in math.js so that average([]) throws Error("empty array") and average([2,4,6]) returns 4. Run npm test to confirm all tests pass (divide tests still run). Then run npm run lint. Stage and commit: git add math.js test.js && git commit -m "feat: average throws on empty [night-2]"`,
  },
  {
    n: 3,
    label: "factorial-negative",
    coderModel:    "claude-haiku-4-5",
    reviewerModel: "claude-sonnet-4-5",
    setupFn: setupNight3,
    prompt: `Read queue/night-3-factorial.md. Fix factorial(n) in math.js: it must throw Error("negative input") when n < 0. The current version recurses infinitely on negative input. Run npm test — the test checks e.message === "negative input", so a stack overflow does NOT pass. Then run npm run lint. Stage and commit: git add math.js test.js && git commit -m "feat: factorial throws on negative [night-3]"`,
  },
];

// ── Night setup functions ────────────────────────────────────────────────────

function setupNight1() {
  log("  [setup] night-1: buggy divide already in place from baseline");
}

function setupNight2() {
  const mathPath = "math.js";
  const math = fs.readFileSync(mathPath, "utf8");
  if (!math.includes("function average")) {
    let fixed = math.replace(/module\.exports\s*=\s*\{[^}]+\};\s*$/, "").trimEnd();
    fixed += `\n\nfunction average(arr) {\n  // BUG: returns NaN when arr is empty\n  return arr.reduce((a, b) => a + b, 0) / arr.length;\n}\n\nmodule.exports = { divide, average };\n`;
    fs.writeFileSync(mathPath, fixed);
  }

  const testPath = "test.js";
  const test = fs.readFileSync(testPath, "utf8");
  if (!test.includes("average")) {
    const extra = `
const { average } = require("./math.js");
let threw2 = false;
try { average([]); } catch(e) { threw2 = true; }
if (!threw2) { console.error("FAIL: average([]) should throw, not return NaN"); process.exit(1); }
if (average([2, 4, 6]) !== 4) { console.error("FAIL: average([2,4,6]) should be 4"); process.exit(1); }
console.log("average tests passed");
`;
    const patched = test.replace('console.log("all tests passed");', extra + '\nconsole.log("all tests passed");');
    fs.writeFileSync(testPath, patched);
  }
  log("  [setup] night-2: buggy average injected, tests expanded");
}

function setupNight3() {
  const mathPath = "math.js";
  const math = fs.readFileSync(mathPath, "utf8");
  if (!math.includes("function factorial")) {
    let fixed = math.replace(/module\.exports\s*=\s*\{[^}]+\};\s*$/, "").trimEnd();
    fixed += `\n\nfunction factorial(n) {\n  // BUG: no guard for n < 0 — infinite recursion\n  if (n === 0) return 1;\n  return n * factorial(n - 1);\n}\n\nmodule.exports = { divide, average, factorial };\n`;
    fs.writeFileSync(mathPath, fixed);
  }

  const testPath = "test.js";
  const test = fs.readFileSync(testPath, "utf8");
  if (!test.includes("factorial")) {
    const extra = `
const { factorial } = require("./math.js");
let threw3 = false;
let threw3Msg = "";
try { factorial(-1); } catch(e) { threw3 = true; threw3Msg = e.message; }
if (!threw3) { console.error("FAIL: factorial(-1) should throw"); process.exit(1); }
if (threw3Msg !== "negative input") { console.error("FAIL: expected Error('negative input'), got: " + threw3Msg); process.exit(1); }
if (factorial(5) !== 120) { console.error("FAIL: factorial(5) should be 120"); process.exit(1); }
if (factorial(0) !== 1)   { console.error("FAIL: factorial(0) should be 1"); process.exit(1); }
console.log("factorial tests passed");
`;
    const patched = test.replace('console.log("all tests passed");', extra + '\nconsole.log("all tests passed");');
    fs.writeFileSync(testPath, patched);
  }
  log("  [setup] night-3: buggy factorial injected, tests expanded");
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function log(msg) {
  const ts = new Date().toISOString();
  const line = `[${ts}] ${msg}`;
  console.log(line);
  fs.mkdirSync("logs", { recursive: true });
  fs.appendFileSync("logs/run-nights.log", line + "\n");
}

function runClaude(model, allowedTools, prompt, label) {
  log(`  [claude] model=${model} running: ${label}`);
  const result = spawnSync(
    "claude",
    [
      "-p",
      "--model", model,
      "--allowedTools", allowedTools,
      "--output-format", "stream-json",
      "--verbose",
      prompt,
    ],
    { encoding: "utf8", timeout: 300_000, maxBuffer: 20 * 1024 * 1024 }
  );

  const logFile = `logs/night-${label}.log`;
  fs.writeFileSync(logFile, (result.stdout || "") + "\n---STDERR---\n" + (result.stderr || ""));

  if (result.status !== 0 && result.status !== null) {
    log(`  [claude] FAILED (exit ${result.status}) — see ${logFile}`);
    // Check if it's just a post-commit warning (work done, non-zero exit)
    const out = (result.stdout || "") + (result.stderr || "");
    const committed = out.includes("git commit") && (out.includes("[main") || out.includes("feat:") || out.includes("fix:"));
    if (!committed) return false;
    log(`  [claude] Non-zero exit but commit detected — treating as success`);
  }
  log(`  [claude] run complete → ${logFile}`);
  return true;
}

function runReviewer(model, label) {
  log(`  [reviewer] model=${model}`);
  const prompt = `Run npm test and npm run lint. Then run git diff HEAD~1. Return ONLY a JSON object — no markdown, no fences, no explanation: { "verdict": "PASS" or "FAIL", "reasons": [], "risk": "low" or "high" }`;

  const result = spawnSync(
    "claude",
    [
      "-p",
      "--model", model,
      "--allowedTools", REVIEWER_TOOLS,
      "--output-format", "stream-json",
      prompt,
    ],
    { encoding: "utf8", timeout: 120_000, maxBuffer: 5 * 1024 * 1024 }
  );

  const logFile = `logs/night-${label}-reviewer.log`;
  fs.writeFileSync(logFile, (result.stdout || "") + "\n---STDERR---\n" + (result.stderr || ""));

  // Contract-coupling: strip markdown fences before parsing (known model habit)
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
    log(`  [reviewer] JSON parse error — raw: ${match[0]}`);
    return { verdict: "UNKNOWN", reasons: ["JSON parse error"], risk: "high" };
  }
}

function testsPass() {
  const r = spawnSync("node", ["test.js"], { encoding: "utf8" });
  return r.status === 0;
}

function appendRatchet(night, coderModel, reviewerModel, verdict, green) {
  const ratchetPath = "logs/ratchet.md";
  if (!fs.existsSync(ratchetPath)) {
    fs.writeFileSync(ratchetPath,
      "# Ratchet log\n\n| Night | Coder | Reviewer | Tests | Verdict | Risk | Notes |\n|---|---|---|---|---|---|---|\n"
    );
  }
  const row = `| night-${night} | ${coderModel} | ${reviewerModel} | ${green ? "✅" : "❌"} | ${verdict.verdict} | ${verdict.risk} | ${(verdict.reasons || []).join("; ") || "—"} |`;
  fs.appendFileSync(ratchetPath, row + "\n");
  log(`  [ratchet] appended row for night-${night}`);
}

function markDone(label) {
  let spine = fs.readFileSync("progress.md", "utf8");
  spine = spine.replace(`- [ ] ${label}`, `- [x] ${label}`);
  const ts = new Date().toISOString();
  spine = spine.replace("## Done\n", `## Done\n- ${label} (${ts})\n`);
  fs.writeFileSync("progress.md", spine);
  log(`  [progress] marked ${label} done`);
}

function markEscalated(label, reason) {
  let spine = fs.readFileSync("progress.md", "utf8");
  const ts = new Date().toISOString();
  spine = spine.replace(
    "## Open / needs a human\n(escalations land here — model, reason, timestamp)",
    `## Open / needs a human\n- ${label}: ${reason} (${ts})`
  );
  fs.writeFileSync("progress.md", spine);
  log(`  [escalate] ${label} → Open/needs-human`);
}

// ── Main loop ────────────────────────────────────────────────────────────────

async function main() {
  fs.mkdirSync("logs", { recursive: true });
  log("=== Project 8 Model-Swap Capstone (Claude Code) — Starting ===");

  const onlyNight = process.argv.includes("--night")
    ? parseInt(process.argv[process.argv.indexOf("--night") + 1], 10)
    : null;

  for (const night of NIGHTS) {
    if (onlyNight && night.n !== onlyNight) continue;

    log(`\n${"=".repeat(60)}`);
    log(`NIGHT ${night.n}: ${night.label}`);
    log(`  coder    → ${night.coderModel}`);
    log(`  reviewer → ${night.reviewerModel}`);
    log(`${"=".repeat(60)}`);

    // 1. Inject buggy state + expand tests
    night.setupFn();

    // 2. Confirm tests RED before agent runs
    const redBefore = !testsPass();
    log(`  [verify] tests RED before run: ${redBefore}`);
    if (!redBefore) {
      log(`  [skip] tests already pass — night ${night.n} already done`);
      continue;
    }

    // 3. Run coder agent (constrain verb: settings.json + allowedTools)
    const coderOk = runClaude(
      night.coderModel,
      ALLOWED_TOOLS,
      night.prompt,
      `${night.n}-${night.label}-coder`
    );

    // 4. Verify tests GREEN (correct verb: exit code contract)
    const green = testsPass();
    log(`  [verify] tests GREEN after coder run: ${green}`);

    // 5. Run reviewer subagent (verify verb, read-only tools)
    const verdict = runReviewer(night.reviewerModel, `${night.n}-${night.label}`);

    // 6. Ratchet log
    appendRatchet(night.n, night.coderModel, night.reviewerModel, verdict, green);

    // 7. Escalate or mark done (escalate verb)
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

main().catch(e => { console.error(e); process.exit(1); });
