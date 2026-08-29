// tools/customer-lookup.js
// A tiny simulated API connector with three realistic failure modes.
// Usage: node tools/customer-lookup.js <customerId> --scope <read|write|none> --style <bad|good> --attempt <n>

const args = process.argv.slice(2);
const customerId = args[0];
const scopeIdx = args.indexOf("--scope");
const scope = scopeIdx >= 0 ? args[scopeIdx + 1] : "read";
const styleIdx = args.indexOf("--style");
const style = styleIdx >= 0 ? args[styleIdx + 1] : "good";
const attemptIdx = args.indexOf("--attempt");
const attempt = attemptIdx >= 0 ? parseInt(args[attemptIdx + 1], 10) : 1;

function fail(exitCode, badMessage, goodMessage) {
  const msg = style === "bad" ? badMessage : goodMessage;
  console.error(JSON.stringify({ ok: false, message: msg }));
  process.exit(exitCode);
}

// Failure 1: missing/insufficient scope
if (scope === "none") {
  fail(
    1,
    "Error 403",
    "403: this token has no scope. Request a token with the 'customers:read' scope from /auth/token, then retry with the same customerId."
  );
}

// Failure 2: malformed ID
if (!customerId || !/^CUST-\d{6}$/.test(customerId)) {
  fail(
    2,
    "Invalid input.",
    `Invalid customerId '${customerId}'. Expected format CUST-###### (6 digits), e.g. CUST-004521. Reformat and retry.`
  );
}

// Failure 3: simulated rate limit. Real APIs recover after a backoff; we
// simulate that honestly by succeeding once attempt >= 2 for IDs ending in
// 000000, so a genuine "wait and retry the identical call" strategy can
// actually succeed -- this is what makes the AX test meaningful rather than
// a trap that always fails regardless of what the message says.
if (customerId.endsWith("000000") && attempt < 2) {
  fail(
    3,
    "Too many requests.",
    "429: rate limited. Retry after 2000ms. Do not change the request; wait and resend the identical call."
  );
}

// Success path
console.log(JSON.stringify({ ok: true, customerId, name: "Jordan Example", scope, attempt }));
process.exit(0);
