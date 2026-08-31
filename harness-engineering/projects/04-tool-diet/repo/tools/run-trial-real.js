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
const manifest = JSON.parse(fs.readFileSync(`tools/${which}-tools.json`, "utf8"));

// Reset the REAL backend to the dirty starting state over the network.
await fetch(`${BASE}/reset`, { method: "POST" });

async function execTool(name) {
  // Every branch below is a real network call to a separate process.
  switch (name) {
    case "get_customer":
    case "fetch_customer_info":
    case "lookup_customer_record":
    case "get_customer_details":
    case "search_customers":
    case "find_customer_by_email": {
      const r = await fetch(`${BASE}/customer`);
      return JSON.stringify(await r.json());
    }
    case "update_customer":
    case "edit_customer_info":
    case "patch_customer_record": {
      const r = await fetch(`${BASE}/customer/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: "99 Main St" })
      });
      return JSON.stringify(await r.json());
    }
    case "close_ticket":
    case "resolve_ticket": {
      const r = await fetch(`${BASE}/ticket/close`, { method: "POST" });
      return JSON.stringify(await r.json());
    }
    case "escalate_ticket": {
      const r = await fetch(`${BASE}/ticket/escalate`, { method: "POST" });
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

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await res.json();

  if (!res.ok) {
    console.error(`trial=${which}-${trialNum} HTTP_ERROR turn=${turn}`, JSON.stringify(data));
    process.exit(1);
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
    const result = await execTool(name); // REAL network call, awaited for real
    responseParts.push({ functionResponse: { name, response: { result } } });
  }
  contents.push({ role: "user", parts: responseParts });
}

// This script does NOT check or report success/failure of the task.
// That check happens in verify-state.js, run separately, against the
// backend's persisted file, so the trial script can't grade itself.
console.log(JSON.stringify({ which, trialNum, turns: turn, stoppedReason, callLog }));
