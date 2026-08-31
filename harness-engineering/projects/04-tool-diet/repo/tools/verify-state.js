// tools/verify-state.js
//
// Independent check of the backend's REAL persisted state, run as a
// separate process with no connection to run-trial-real.js. This is the
// only source of truth for whether a trial actually succeeded.
//
// Usage: node tools/verify-state.js <port>

const PORT = process.argv[2] || "8743";
const BASE = `http://localhost:${PORT}`;

const customer = await (await fetch(`${BASE}/customer`)).json();
const ticket = await (await fetch(`${BASE}/ticket`)).json();

const addressCorrect = customer.address === "99 Main St";
const ticketClosed = ticket.status === "closed";

console.log(JSON.stringify({
  addressCorrect, ticketClosed, taskDone: addressCorrect && ticketClosed,
  customer, ticket
}));
