// tools/run-trial-real.js
//
// Real test: the live Gemini API picks tools, and every tool call is a
// REAL HTTP request to a separate backend process (backend-server.js)
// with its own state persisted to disk. This script does NOT grade
// itself -- it only logs what happened. Run verify-state.js afterward,
// as a completely separate process, to check the real outcome.
//
// Usage:
//   node tools/backend-server.js 8743   (in its own terminal/process)
//   node tools/run-trial-real.js <before|after> <trialNumber> <port>
//
// Error handling (Concept 10 fix, applied for real): every network call
// (to the backend AND to the Gemini API) goes through fetchWithRetry --
// transient failures get retried with growing backoff, capped at 3
// attempts. If retries are exhausted, or anything else throws, the whole
// script still emits exactly ONE well-formed JSON line to stdout (an
// error record, never a raw stack trace) and exits with a distinct code
// (2), so a shell loop appending stdout to results.jsonl can never end
// up with a corrupted line mixed into the file the way it did before
// this fix (see project-6/repo/HARNESS.md, Day 6).

import fs from "node:fs";

const API_KEY = process.env.GEMINI_API_KEY;
if (!API_KEY) {
  console.error("Set GEMINI_API_KEY env var first.");
  process.exit(1);
}

const which = process.argv[2] || "before";
const trialNum = process.argv[3] || "1";
const PORT = process.argv[4] || "8743";
const BASE = `http://localhost:${PORT}`;

const MAX_RETRIES = 3;
const BASE_DELAY_MS = 500;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Wraps fetch with capped retries and growing backoff. Retries on
// network-level failures (connect timeout, refused, reset, DNS, etc --
// anything fetch() itself throws for) and on 5xx responses. Does NOT
// retry on 4xx responses, since those are a real answer from the server,
// not a transient infra problem, and retrying them would just waste time.
async function fetchWithRetry(url, opts, label) {
  let lastErr;
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      const res = await fetch(url, opts);
      if (res.status >= 500) {
        throw new Error(`${label}: server error ${res.status}`);
      }
      return res;
    } catch (err) {
      lastErr = err;
      console.error(`${label}: attempt ${attempt}/${MAX_RETRIES} failed: ${err.message || err}`);
      if (attempt < MAX_RETRIES) {
        await sleep(BASE_DELAY_MS * attempt); // 500ms, 1000ms
      }
    }
  }
  throw new Error(`${label}: exhausted ${MAX_RETRIES} retries: ${lastErr?.message || lastErr}`);
}

const manifest = JSON.parse(fs.readFileSync(`tools/${which}-tools.json`, "utf8"));

async function execTool(name) {
  // Every branch below is a real network call to a separate process,
  // now retried through fetchWithRetry instead of a bare await fetch().
  switch (name) {
    case "get_customer":
    case "fetch_customer_info":
    case "lookup_customer_record":
    case "get_customer_details":
    case "search_customers":
    case "find_customer_by_email": {
      const r = await fetchWithRetry(`${BASE}/customer`, undefined, "GET /customer");
      return JSON.stringify(await r.json());
    }
    case "update_customer":
    case "edit_customer_info":
    case "patch_customer_record": {
      const r = await fetchWithRetry(`${BASE}/customer/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: "99 Main St" })
      }, "POST /customer/update");
      return JSON.stringify(await r.json());
    }
    case "close_ticket":
    case "resolve_ticket": {
      const r = await fetchWithRetry(`${BASE}/ticket/close`, { method: "POST" }, "POST /ticket/close");
      return JSON.stringify(await r.json());
    }
    case "escalate_ticket": {
      const r = await fetchWithRetry(`${BASE}/ticket/escalate`, { method: "POST" }, "POST /ticket/escalate");
      return JSON.stringify(await r.json());
    }
    default:
      return JSON.stringify({ ok: false, error: `unknown tool ${name}` });
  }
}

const functionDeclarations = manifest.map(t => ({
  name: t.name,
  description: t.description,
  parameters: {
    type: "OBJECT",
    properties: { input: { type: "STRING", description: "any identifying info needed (id, email, etc.)" } },
    required: []
  }
}));

// trialNum is folded into the task text so no two requests are byte-identical
// (rules out any server-side response caching affecting the comparison).
const task = `(request ref ${trialNum}) A customer, jordan@example.com, emailed asking to update their shipping address to '99 Main St', and also wants their support ticket #4471 closed since the issue is fixed. Handle both parts of this request by calling the appropriate tool(s). Once both parts are actually done, stop calling tools.`;

const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key=${API_KEY}`;

async function main() {
  // Reset the REAL backend to the dirty starting state over the network.
  await fetchWithRetry(`${BASE}/reset`, { method: "POST" }, "POST /reset");

  const contents = [{ role: "user", parts: [{ text: task }] }];
  const callLog = [];
  const MAX_TURNS = 6;
  let turn = 0;
  let stoppedReason = "max_turns";

  while (turn < MAX_TURNS) {
    turn++;
    const body = {
      contents,
      tools: [{ functionDeclarations }],
      toolConfig: { functionCallingConfig: { mode: "AUTO" } },
      generationConfig: { temperature: 1.0 }
    };

    const res = await fetchWithRetry(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    }, "POST generateContent");
    const data = await res.json();

    if (!res.ok) {
      // A real (non-5xx, so not retried) API error -- e.g. bad request,
      // bad key, quota. Report it as one clean JSON line, same discipline
      // as the retry-exhaustion path below, rather than a bare stack trace.
      throw new Error(`HTTP_ERROR turn=${turn} ${JSON.stringify(data)}`);
    }

    const parts = data.candidates?.[0]?.content?.parts || [];
    const calls = parts.filter(p => p.functionCall);

    if (calls.length === 0) {
      stoppedReason = "model_stopped_calling_tools";
      break;
    }

    contents.push({ role: "model", parts });

    const responseParts = [];
    for (const c of calls) {
      const name = c.functionCall.name;
      callLog.push(name);
      const result = await execTool(name); // REAL network call, retried, awaited for real
      responseParts.push({ functionResponse: { name, response: { result } } });
    }
    contents.push({ role: "user", parts: responseParts });
  }

  // This script does NOT check or report success/failure of the task.
  // That check happens in verify-state.js, run separately, against the
  // backend's persisted file, so the trial script can't grade itself.
  console.log(JSON.stringify({ which, trialNum, turns: turn, stoppedReason, callLog }));
}

try {
  await main();
} catch (err) {
  // Single point of failure handling for the whole script: no matter what
  // throws (exhausted retries, a genuine HTTP error, a bug), exactly one
  // well-formed JSON line goes to stdout and nothing else does. Diagnostic
  // detail goes to stderr, which a results.jsonl-appending shell loop
  // should redirect separately (`> results.jsonl 2> trial-errors.log`),
  // never merged into stdout.
  console.error(err.stack || err.message || String(err));
  console.log(JSON.stringify({ which, trialNum, turns: null, stoppedReason: "error", callLog: [], error: err.message || String(err) }));
  process.exit(2);
}