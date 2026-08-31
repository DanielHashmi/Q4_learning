// tools/backend-server.js
//
// A REAL backend, running as its own OS process, listening on a real TCP
// port, with state persisted to a real file on disk. This replaces the
// old design where "execTool()" was a switch statement living inside the
// same script that also graded the trial -- i.e. a mock grading itself.
//
// The trial script (run-trial-real.js) talks to this over actual HTTP.
// A separate, independent script (verify-state.js) reads the persisted
// state file directly to check the outcome -- it has no relationship to
// the trial script and can't be fooled by anything the trial script
// claims about itself.
//
// Usage: node tools/backend-server.js <port>
// Endpoints:
//   POST /reset            -> resets state to the dirty starting condition
//   GET  /customer         -> returns current customer record
//   POST /customer/update  -> body: {address}, persists new address
//   GET  /ticket           -> returns current ticket record
//   POST /ticket/close     -> persists ticket.status = "closed"
//   POST /ticket/escalate  -> persists ticket.status = "escalated"

import http from "node:http";
import fs from "node:fs";

const PORT = Number(process.argv[2] || 8743);
const STATE_FILE = new URL("./backend-state.json", import.meta.url);

function initialState() {
  return {
    customer: { id: "CUST-1187", email: "jordan@example.com", address: "12 Old Rd" },
    ticket: { id: "4471", status: "open" }
  };
}

function readState() {
  if (!fs.existsSync(STATE_FILE)) writeState(initialState());
  return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
}

function writeState(s) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));
}

writeState(initialState());

const server = http.createServer(async (req, res) => {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const bodyRaw = Buffer.concat(chunks).toString("utf8");
  let body = {};
  try { body = bodyRaw ? JSON.parse(bodyRaw) : {}; } catch { /* ignore */ }

  const send = (code, obj) => {
    res.writeHead(code, { "Content-Type": "application/json" });
    res.end(JSON.stringify(obj));
  };

  const state = readState();

  if (req.method === "POST" && req.url === "/reset") {
    writeState(initialState());
    return send(200, { ok: true, reset: true });
  }

  if (req.method === "GET" && req.url === "/customer") {
    return send(200, state.customer);
  }

  if (req.method === "POST" && req.url === "/customer/update") {
    if (!body.address) return send(400, { ok: false, error: "address required" });
    state.customer.address = body.address;
    writeState(state);
    return send(200, { ok: true, customer: state.customer });
  }

  if (req.method === "GET" && req.url === "/ticket") {
    return send(200, state.ticket);
  }

  if (req.method === "POST" && req.url === "/ticket/close") {
    state.ticket.status = "closed";
    writeState(state);
    return send(200, { ok: true, ticket: state.ticket });
  }

  if (req.method === "POST" && req.url === "/ticket/escalate") {
    state.ticket.status = "escalated";
    writeState(state);
    return send(200, { ok: true, ticket: state.ticket });
  }

  send(404, { ok: false, error: `no route ${req.method} ${req.url}` });
});

server.listen(PORT, () => {
  console.log(`backend listening on http://localhost:${PORT}`);
});
