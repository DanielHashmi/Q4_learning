# 7️⃣ Lesson 7 — Connect External Tools (MCP Servers)

## Lesson Overview

Skills give your agent knowledge. MCP servers give it access. In this lesson you connect your first MCP server, encounter OpenClaw's most counterintuitive behavior (silent failure), and learn the two config scopes and three transport options that govern every MCP connection you will ever make.

> **Before you start:** Terminal open, dashboard open (`http://127.0.0.1:18789/`), messaging channel ready. This lesson is two commands and a diagnosis.
> 

---

## 1. Why MCP, Not a Skill

From Lesson 6's decision tree:

```
Agent needs to KNOW something        → Skill
Agent needs to ACCESS something      → MCP server
Agent needs a new gateway capability → Plugin
```

A skill teaches the agent *how* to handle a topic using its training data. An MCP server gives the agent a live tool that reaches outside the gateway to an external service.

The clearest test: **can this be answered from training data, or does it require a live query?**

- "How do timezones work?" → Training data → Skill (or no extension at all)
- "What time is it in Tokyo right now?" → Live clock → MCP server
- "What are the company's open Jira tickets?" → Live database → MCP server
- "What is the OAMCM marketing framework?" → Domain knowledge → Skill

The agent's training data is frozen at a point in time. MCP servers are the bridge to anything that needs to be live.

---

## 2. Your First MCP Server

Two commands:

```bash
openclaw config set mcp.servers.time '{"command":"uvx","args":["mcp-server-time"]}'
openclaw gateway restart
```

That is the complete installation. No API key. No configuration file. No code.

**What just happened:**

- `openclaw config set mcp.servers.time` wrote a JSON entry into `~/.openclaw/openclaw.json` under the `mcp.servers` key
- `openclaw gateway restart` restarted the gateway, which read the new config and spawned `mcp-server-time` as a child process via `uvx`
- The server registered its tools with the gateway
- Your agent now has those tools available

### Verify the Connection

**In the dashboard:** Open **Agents → Tools**. Look for two new tools: `get_current_time` and `convert_time`. If they appear, the MCP server connected successfully.

**In the terminal:**

```bash
openclaw mcp list
```

You should see `time` in the list with its status.

> **Skills vs MCP tools — a common confusion:** If you ask your agent "What tools do you have?", it may list its *skills* but not its MCP tools. Skills (loaded from SKILL.md files) and MCP tools (from running server processes) are different things. The dashboard → Agents → Tools tab shows both, clearly separated. Use the dashboard to verify MCP tools, not the chat.
> 

### Use It

```
What time is it in Tokyo right now?
```

The answer should be a specific live time — not a generic "UTC+9" rule. Check the dashboard: you will see a tool badge showing the agent used `get_current_time`.

**The two tools this server provides:**

| Tool | What It Does | Timezone Format |
| --- | --- | --- |
| `get_current_time` | Takes a timezone, returns current time and DST status | IANA (e.g., `Asia/Tokyo`) |
| `convert_time` | Takes source timezone, a time, and target timezone; returns converted time | IANA |

Try both:

```
Convert 3pm New York time to Tokyo time.
```

---

## 3. Managing MCP Servers

The MCP CLI gives you shorthand commands that are equivalent to `openclaw config set mcp.servers.*`:

```bash
# List all configured servers
openclaw mcp list

# See details for one server
openclaw mcp show time

# Add or update a server
openclaw mcp set time '{"command":"uvx","args":["mcp-server-time"]}'

# Remove a server
openclaw mcp unset time
```

All MCP server configs live in `openclaw.json` under `mcp.servers`. Every agent on the gateway gets access to these tools by default (gateway-level config). Scoping to one agent is covered in Section 5.

---

## 4. Silent Failure: The Most Counterintuitive Behavior

This is the single most important thing in this lesson. Run this deliberately to experience it:

```bash
openclaw config set mcp.servers.time '{"command":"uvx","args":["this-server-does-not-exist"]}'
openclaw gateway restart
```

Now ask:

```
What time is it in Tokyo right now?
```

The agent answers. It does not say "I cannot do this." It does not say "the MCP server failed." It gives you the UTC+9 explanation from training data — exactly as it did before you installed anything.

**Check the dashboard.** No time tools listed. The tools disappeared without an error message in chat.

**Stream the gateway log:**

```bash
openclaw logs --follow
```

The log shows the failure: a non-zero exit code from the server process that could not start. Press Ctrl+C once you have seen it.

**Why this happens:** The agent never knew the tools existed because the server never started. From the agent's perspective, the tool simply isn't there. It responds normally using what it does have access to.

### Failure Diagnosis Table

| Symptom | What the Log Shows | Fix |
| --- | --- | --- |
| Wrong package name | Non-zero exit code | Verify exact package name |
| Missing runtime | `uvx: command not found` or `npx: command not found` | Install `uv` or Node.js |
| Remote server unreachable | Connection timeout | Verify URL and server status |
| Gateway not restarted | Old config still active | `openclaw gateway restart` |
| Tools missing, no error | Server crashed silently | Check full log, not just chat |

**The diagnostic pattern:**

1. Ask a question that requires the MCP tool
2. No expected response → check dashboard for missing tools
3. Tools missing → `openclaw logs --follow` for the real error
4. Never trust chat silence as "working"

**Revert to the working config before continuing:**

```bash
openclaw config set mcp.servers.time '{"command":"uvx","args":["mcp-server-time"]}'
openclaw gateway restart
```

---

## 5. Two Config Scopes

Every MCP server config sits at one of two levels. The choice determines which agents can see the tools.

| Scope | Location | Who Gets the Tools |
| --- | --- | --- |
| **Gateway-level** | `openclaw.json` under `mcp.servers` | All agents on this gateway |
| **Workspace-level** | `~/.openclaw/workspace/.mcp.json` | Only the agent whose workspace contains this file |

**Gateway-level** (what you have done so far with `openclaw config set`): tools are shared across every agent you run on this gateway. Good for tools every agent should have.

**Workspace-level** (`.mcp.json` in the agent's workspace directory): tools are scoped to one agent. Good for specialized tools that only one agent should access — a customer support agent should not have your personal calendar tools.

### Moving a Server from Gateway to Workspace Scope

```bash
# Remove from gateway-level
openclaw config unset mcp.servers.time

# Create or edit ~/.openclaw/workspace/.mcp.json
```

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    }
  }
}
```

```bash
openclaw gateway restart
```

Your main agent still sees the time tools. A second agent with a different workspace would not — because the config lives in your workspace, not the gateway.

---

## 6. Three Transport Options

Every MCP server uses one of three transports. The transport determines how the gateway communicates with the server process.

| Transport | Config Keys | When to Use |
| --- | --- | --- |
| **stdio** | `command`  • `args` | Local server: npm package, Python script, any local process |
| **SSE** | `url` (default for URL config) | Remote server using HTTP Server-Sent Events |
| **streamable-http** | `url`  • `"transport":"streamable-http"` | Remote server using HTTP streaming |

### stdio (Local)

The gateway spawns the server as a child process. What you have been using:

```bash
openclaw mcp set time '{"command":"uvx","args":["mcp-server-time"]}'
```

`uvx` runs Python-based MCP servers. `npx` runs Node.js-based ones:

```bash
openclaw config set mcp.servers.context7 '{"command":"npx","args":["-y","@upstash/context7-mcp"]}'
```

### SSE (Remote)

Connect to a server running at a URL:

```bash
openclaw mcp set remote-tools '{"url":"https://mcp.example.com"}'
openclaw gateway restart
```

SSE is the default when a `url` field is present with no `transport` field.

### Streamable-HTTP (Remote)

```bash
openclaw mcp set streaming-tools '{"url":"https://mcp.example.com/stream","transport":"streamable-http"}'
```

Both remote transports support auth headers and connection timeouts. You will connect a production remote MCP server in Chapter 57.

### Transport Selection Rule

```
Server runs on your machine    →  stdio  (command + args)
Server runs at a URL           →  SSE or streamable-http  (url)
```

If in doubt about which remote transport to use, try SSE first. It is the more widely supported default.

---

## 7. The MCP Workflow Pattern

Every MCP connection follows the same five steps:

```
1. CONFIGURE   openclaw mcp set <name> '<json>'
2. RESTART     openclaw gateway restart
3. VERIFY      Dashboard → Agents → Tools (do the tools appear?)
4. TEST        Ask a question that requires the new tools
5. LOG         If tools missing: openclaw logs --follow
```

Do not skip step 3. The dashboard is the verification layer. Do not use chat as verification — silent failure means the agent will respond normally even when tools are missing.

---

## 8. Practical Exercises

### Exercise 1 — Add a Second MCP Server

Add a documentation lookup server alongside the time server:

```bash
openclaw config set mcp.servers.context7 '{"command":"npx","args":["-y","@upstash/context7-mcp"]}'
openclaw gateway restart
```

Verify in the dashboard: you should see tools from both the time server and context7.

Then ask your agent:

```
Look up the FastAPI documentation for creating route handlers.
```

Check the dashboard for a tool badge from context7.

**What you are learning:** MCP servers are additive. Each `config set` adds an independent set of tools without affecting existing ones. The toolbox grows with each server you connect.

---

### Exercise 2 — Deliberately Trigger and Diagnose Silent Failure

Run the silent failure scenario from Section 4 yourself. Set a bad package name, restart, ask a timezone question, observe the chat response, check the dashboard, then stream the log.

Record:

- What did the agent say in chat?
- What did the dashboard show under Agents → Tools?
- What did the log show?
- How long did it take you to diagnose the cause?

Then revert to the correct config and verify the tools return.

**What you are learning:** Silent failure is the hardest failure mode to debug because everything *looks* fine. The log is the only place the failure is visible. This exercise builds the muscle memory to check the log first.

---

### Exercise 3 — Scope a Server to Workspace Level

Move the time server from gateway-level to workspace-level config:

1. `openclaw config unset mcp.servers.time`
2. Create `~/.openclaw/workspace/.mcp.json` with the time server config
3. `openclaw gateway restart`
4. Verify in the dashboard: your main agent should still see the time tools

Then check `~/.openclaw/openclaw.json` directly:

```bash
cat ~/.openclaw/openclaw.json | grep -A5 mcp
```

The time server should no longer appear under `mcp.servers` in `openclaw.json`. It is now in `.mcp.json` in your workspace.

**What you are learning:** The two config scopes and when to use each. Gateway scope for shared tools; workspace scope for agent-specific tools.

---

### Exercise 4 — Agent Tool Self-Report

Ask your agent:

```
What MCP servers are currently connected? List each server and its available tools.
```

Then compare the agent's answer with what the dashboard shows under Agents → Tools.

If they match: your MCP configuration is clean and the agent's self-awareness is accurate.

If they differ: check the gateway log for servers that connected but registered no tools, or servers that failed silently.

**What you are learning:** Your agent can report its own tool inventory. This is the fastest zero-terminal verification method. Discrepancies between chat and dashboard are diagnostic signals.

---

### Exercise 5 — Classify MCP vs Skill for Five Scenarios

For each scenario below, decide: MCP server, skill, or plugin? Then explain why.

1. The agent needs to know the STAR interview response framework
2. The agent needs to check live stock prices
3. The agent needs to read and write files in your company's Google Drive
4. The agent needs to know how to write ISO 27001 compliance reports in your company's specific template format
5. The agent needs to receive Slack messages as a new input channel

Write your classification and reasoning before checking:

- 1 = Skill (domain knowledge, no live access needed)
- 2 = MCP server (live price data)
- 3 = MCP server (live read/write access to external system)
- 4 = Skill (company-specific template knowledge)
- 5 = Plugin (new channel = new gateway capability)

**What you are learning:** The boundary cases between extension types. If you got all five right before checking, the decision tree from Lesson 6 is fully internalized.

---

## Key Takeaways

**MCP in one sentence:** An MCP server gives your agent live access to external tools without writing code. One config command, one gateway restart, new tools in the dashboard.

**Silent failure is the hardest failure mode:**

- MCP failures produce no error in chat
- The agent responds normally, just without the expected tools
- The gateway log (`openclaw logs --follow`) is the only diagnostic
- Always verify in the dashboard, never in chat alone

**Two config scopes:**

- Gateway-level (`mcp.servers` in `openclaw.json`) = shared across all agents
- Workspace-level (`.mcp.json` in workspace directory) = scoped to one agent

**Three transports:**

- `command` + `args` = stdio, local process (most common)
- `url` = SSE, remote HTTP server
- `url` + `"transport":"streamable-http"` = streamable-http, remote HTTP streaming

**MCP servers are additive.** Each server adds its tools independently. Multiple servers coexist in one config, each with its own namespace.

**The test for MCP vs Skill:** Can this be answered from training data, or does it require a live query? If live query is needed, it's MCP.

---

## Up Next

**Lesson 8 — Proactive Behavior (Heartbeats & Cron Jobs):** Your agent currently waits for you to ask. In Lesson 8 you give it a schedule — heartbeats that check on a timer and cron jobs that fire at exact times. This is the dimension that separates an AI Employee from a chat interface.