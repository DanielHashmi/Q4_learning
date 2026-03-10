# Stdio and Streamable HTTP #7

## Stdio

Client launches the server as a subprocess and they talk through terminal input/output streams. No ports, no URLs, no network, just two processes connected by pipes. Fully bidirectional, meaning both sides can initiate messages. Every MCP feature works without any configuration. The only hard limit is that both client and server must be on the same machine.

Don't use Streamable HTTP when:
Your use case is purely local. STDIO is simpler, requires no network configuration, and is the standard for local development.

## Streamable HTTP

Streamable HTTP is the current production-grade, remote-capable MCP transport. It unlocks cloud hosting and multiple clients, it uses a single endpoint with standard POST and GET requests. To keep track of the conversation, it strictly requires an `Mcp-Session-Id` and an `MCP-Protocol-Version` header.

Use Streamable HTTP when:
Your server needs to be hosted on a cloud/remote machine.
Multiple clients need to connect to the same server simultaneously.
You're deploying to production.

## Exercise

1. Streamable HTTP is more powerful for production, but strictly inferior to STDIO for local use because it requires more setup and session management

2. Hard limit: STDIO is same-machine only. The moment you need remote or cloud hosting, STDIO cannot help you

3. The old HTTP + SSE transport is now DEPRECATED. Always use Streamable HTTP with session IDs for modern remote servers

4. Streamable HTTP best for: Remote hosting, production deployments, and public APIs

5. Stdio best for: Local development, CLI tools, and learning MCP

6. Transports are the delivery system for MCP messages. They determine how messages physically travel between client and server. Think of messages as letters and transports as the postal service

Good Luck 👋🏻