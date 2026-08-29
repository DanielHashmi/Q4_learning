// tools/rule-based-recoverer.js
// Simulates a minimal, literal-minded agent that can ONLY act on what an
// error message tells it to do -- no world knowledge, no guessing. This is
// the sharpest way to test AX: if the message doesn't say what to do next,
// this "agent" cannot recover, no matter how many attempts it gets.

import { execFileSync } from "node:child_process";

function tryCall(customerId, scope, style, attempt) {
  try {
    const out = execFileSync("node", ["tools/customer-lookup.js", customerId, "--scope", scope, "--style", style, "--attempt", String(attempt)], { encoding: "utf8" });
    return { ok: true, result: JSON.parse(out) };
  } catch (e) {
    const stderr = e.stderr ? e.stderr.toString().trim() : "";
    let parsed;
    try { parsed = JSON.parse(stderr); } catch { parsed = { message: stderr }; }
    return { ok: false, message: parsed.message || "" };
  }
}

function attemptRecovery(scenarioName, customerId, scope, style, maxAttempts = 3) {
  let attempts = 0;
  let currentId = customerId;
  let currentScope = scope;
  const log = [];

  while (attempts < maxAttempts) {
    attempts++;
    const res = tryCall(currentId, currentScope, style, attempts);
    log.push({ attempt: attempts, ok: res.ok, message: res.ok ? "(success)" : res.message });
    if (res.ok) {
      return { scenarioName, recovered: true, attempts, log };
    }

    const msg = res.message;
    // Only act if the message gives an explicit, matchable instruction.
    if (/'customers:read'/.test(msg) || /needs? .*scope/i.test(msg)) {
      currentScope = "read";
      continue;
    }
    const fmt = msg.match(/Expected format (CUST-#{6})/);
    if (fmt) {
      currentId = "CUST-004521";
      continue;
    }
    if (/retry after \d+ms/i.test(msg)) {
      continue; // "wait and resend" -> retry with an incremented attempt counter
    }
    // Nothing actionable in the message -> the literal-minded agent is stuck.
    return { scenarioName, recovered: false, attempts, log, stuckOn: msg };
  }
  return { scenarioName, recovered: false, attempts, log, stuckOn: "max attempts exhausted" };
}

const scenarios = [
  { name: "missing-scope", customerId: "CUST-004521", scope: "none" },
  { name: "malformed-id", customerId: "notavalidid", scope: "read" },
  { name: "rate-limited", customerId: "CUST-000000", scope: "read" },
];

const summary = {};
for (const style of ["bad", "good"]) {
  console.log(`\n=== STYLE: ${style.toUpperCase()} ===`);
  summary[style] = {};
  for (const s of scenarios) {
    const result = attemptRecovery(s.name, s.customerId, s.scope, style);
    console.log(JSON.stringify(result, null, 2));
    summary[style][s.name] = result.recovered;
  }
}
console.log("\n=== SUMMARY (recovered: true/false) ===");
console.log(JSON.stringify(summary, null, 2));
