# Stdio and Streamable #7

## Stdio

Client launches the server as a subprocess and they talk through terminal input/output streams. No ports, no URLs, no network — just two processes connected by pipes. Fully bidirectional, meaning both sides can initiate messages. Every MCP feature works without any configuration. The only hard limit is that both client and server must be on the same machine

Don't use Streamable HTTP when:

You're still learning MCP — the extra setup adds friction
Your use case is purely local — STDIO is simpler and more capable
You hit Node version issues — don't fight tooling while learning concepts

## Streamable

Streamable HTTP is the production-grade, remote-capable MCP transport, it unlocks cloud hosting and multiple clients, client and server communicate over HTTP using Server-Sent Events (SSE) to solve HTTP's one-way limitation, The client POSTs a request, the server keeps the connection open as a live stream and pushes multiple messages back through it. Enables remote hosting and multiple clients, but requires mcp-remote as a bridge for clients like Claude Desktop, depends on Node.js (v20.18.1+), and silently breaks major features if you set stateless_http=True or json_response=True

Use Streamable HTTP when:

Your server needs to be hosted on a cloud/remote machine
Multiple clients need to connect to the same server simultaneously
You're building a public MCP API for others to use
You're deploying to production

## Exercise

1. Streamable HTTP is more powerful for production, but strictly inferior to STDIO for local use, more setup, more dependencies, more ways to break

2. Hard limit: same machine only, the moment you need remote or cloud hosting, STDIO cannot help you

3. HTTP was designed for one-way request-response. The server doesn't know the client's URL, so pushing messages back was not easy, but SSE is a solution which makes it easy

4. Streamable best for: Remote hosting, cloud deployments, public APIs, multiple simultaneous clients

5. Stdio best for: Local development, CLI tools, desktop apps, learning MCP

6. Transports are the delivery system for MCP messages, they determine how messages physically travel between client and server. Think of messages as letters and transports as the postal service

Good Luck 👋🏻