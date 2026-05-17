# 🔟 Lesson 10 — Add a Second Agent

## Lesson Overview

One agent handles everything right now — customer questions and internal operations in the same queue. This lesson splits the desk. You will create a second agent on the same WhatsApp number, configure routing rules, set per-agent identity and workspace, and learn why identity changes do not take effect until the next session.

> **The core concept:** Two agents, one gateway. Gateway config is shared (plugins, TTS, model). Workspace config is per-agent (SOUL.md, skills, MCP).
> 

> **Before you start:** Terminal open, dashboard open, WhatsApp active with at least one other phone or number to test with.
> 

---

## 1. Why Split the Desk

A single agent handling everything creates two problems:

**Context bleed:** Internal status updates meant for you appear in customer-facing conversations. The agent cannot know which context is appropriate unless you tell it — and you cannot tell it per-message.

**Permission mismatch:** A customer-facing agent should not have access to lead databases, internal operations tools, or admin-only skills. A single agent with broad permissions is a single point of failure.

The split is not about personality. Both agents can be friendly. The split is about **what each agent is allowed to do** and **what context it operates in**.

|  | Main Agent | Helper Agent |
| --- | --- | --- |
| Audience | Internal (you) | Customers or specialized tasks |
| Tool access | Full (coding profile) | Restricted (messaging profile) |
| Skills | All installed | Domain-specific only |
| Memory | Full MEMORY.md | Separate workspace |
| Heartbeat | Internal ops checklist | Customer-facing checks |

---

## 2. Step 1: Create the Second Agent

```bash
openclaw agents add helper-agent
```

The wizard walks you through:

- **Workspace directory:** Accept the default
- **Copy auth profiles from main agent:** Say yes
- **Configure channels now:** Select WhatsApp. If WhatsApp shows "already configured," skip it.

Verify both agents exist:

```bash
openclaw agents list --bindings
```

You should see `main (default)` and `helper-agent`. The helper has no routing rules yet, which means all messages still go to `main`.

**What was created:**

```
~/.openclaw/
├── workspace/              # main agent's workspace
   ├── SOUL.md
   ├── IDENTITY.md
   ├── AGENTS.md
   └── ...
	 └── helper-agent/ # new agent's workspace (independent)
	    ├── SOUL.md
	    ├── IDENTITY.md
	    ├── AGENTS.md
	    └── ...
```

---

## 3. Step 2: Bind It to WhatsApp and Test

Unbind first if already bind with main:

```bash
openclaw agents unbind --agent main --bind whatsapp:default
```

Now bind with`helper-agent` :

```bash
openclaw agents bind --agent helper-agent --bind whatsapp
openclaw gateway restart
```

Send a message from your other phone on WhatsApp.

**Two things to verify:**

1. **On WhatsApp:** A new agent replies. It will not introduce itself as your main agent. The tone or greeting will be different (generic, since you have not set its identity yet).
2. **On the dashboard:** Open `openclaw dashboard`. You will see the conversation under the `helper-agent` tab, not `main`. The dashboard shows which agent handled each message.

If `helper-agent` answered: the binding works.

If `main` answered: the binding did not take effect. Run `openclaw agents list --bindings` and verify the routing rule exists. Then check that you restarted the gateway.

**What happened:** Both agents share the same WhatsApp number. The routing layer decides which agent handles each message. When you bound `helper-agent` to WhatsApp, it became the handler for all incoming WhatsApp messages. Your `main` agent now only handles messages on channels with no binding.

---

## 4. Step 3: Set Its Identity

Your helper agent introduces itself generically because it has no identity set. Tell it who it is on WhatsApp:

```
Update your IDENTITY.md. Your name is Helper, your role is research
assistant, and your emoji is 🔍. You help me find information and
summarize documents.
```

Verify:

```
Show me your IDENTITY.md
```

Now start a new session and test:

```
/new
Introduce yourself
```

The agent should introduce itself with the new identity.

**If it still uses the old name:** You are in a cached session. `/new` starts a fresh one. If `/new` does not work, close the conversation and open a new DM.

### Session Cache: Why Changes Are Not Instant

This is the same three-layer caching model from Lesson 4, applied to multi-agent routing:

```
[Layer 1]  Workspace files on disk    ← your identity edit lands here
[Layer 2]  Session snapshot           ← cached at session start
[Layer 3]  Model reads Layer 2        ← same cached snapshot every turn
```

Identity changes take effect at **session boundaries**, not mid-conversation. Customers in active conversations keep the old persona until their session expires or they start a new one. In production, plan identity rollouts around session expiry, not the moment you save the file.

**The session is the shift boundary.** Reassigning a worker does not change the current shift. It changes the next one.

---

## 5. Step 4: Customize the Workspace

Your helper agent has its own independent workspace:

```bash
ls ~/.openclaw/workspace/helper-agent/
```

Same files as main: SOUL.md, IDENTITY.md, AGENTS.md, TOOLS.md, USER.md, HEARTBEAT.md. Each file is independent.

Edit `helper-agent`'s SOUL.md to define its specialization:

```
Update your SOUL.md to specialize in research. Your job is to find
information, summarize documents, and answer questions with sources.
You are thorough and always cite where you found things.
```

### The Gateway vs Workspace Split

| Config Type | Location | Scope | What It Covers |
| --- | --- | --- | --- |
| **Gateway config** | `openclaw.json` | All agents | Plugins, TTS, model settings, channels |
| **Workspace config** | `workspace-*/` | One agent | SOUL.md, IDENTITY.md, skills, MCP, HEARTBEAT.md |

Install a plugin → both agents get it.

Edit SOUL.md → only that agent changes.

Install a skill in one workspace → the other agent cannot use it.

**This is intentional.** A customer-facing agent should not have admin-only skills. Workspace isolation is the access control layer for capabilities.

---

## 6. Step 5: Route by Sender (Same Number, Different Agents)

Right now, ALL WhatsApp messages go to `helper-agent` because of the channel-wide binding. What if specific contacts should reach `main` and others should reach `helper-agent`?

**First, remove the channel-wide rule:**

```bash
openclaw agents unbind --agent helper-agent --bind whatsapp
openclaw gateway restart
```

Send a message. It should go back to `main` (the fallback). No message is ever lost; the main agent is the safety net.

**Now add a sender-specific rule.** Open `~/.openclaw/openclaw.json` and add a `bindings` key at the top level (same level as `agents`, `gateway`, `channels`):

```json
{
  "bindings": [
    {
      "agentId": "helper-agent",
      "match": {
        "channel": "whatsapp",
        "peer": { "kind": "direct", "id": "+923001234567" }
      }
    }
  ],
  "agents": { },
  "gateway": { }
}
```

Replace `+923001234567` with the number you message **from** (your phone, not the agent's registered number).

```bash
openclaw gateway restart
```

Send from that number → goes to `helper-agent`.

Send from a different number → goes to `main`.

Peer-specific bindings always win over channel-wide bindings. Placing more specific rules first in the array is good practice even though priority is not position-dependent.

---

## 7. Step 6: Two WhatsApp Numbers (Optional)

If you have two phones or two SIMs, you can link separate WhatsApp accounts and give each its own agent:

```bash
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account business
```

Then in `openclaw.json`:

```json
{
  "bindings": [
    { "agentId": "home", "match": { "channel": "whatsapp", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "whatsapp", "accountId": "business" } }
  ]
}
```

Two phone numbers, two agents, one gateway. Each account maintains its own authentication and sessions.

---

## 8. The Routing Decision Tree

When the gateway receives a message, it resolves the handler in this order:

```
1. Check bindings array in openclaw.json
   ├── Match peer-specific rule (most specific)? → use that agent
   ├── Match account-specific rule?              → use that agent
   └── Match channel-wide rule?                  → use that agent
2. No matching binding?
   └── Fall back to main agent (always catches everything)
```

The fallback is a safety guarantee: no message is ever dropped due to missing routing config.

---

## 9. Practical Exercises

### Exercise 1 — Compare Two Agents on the Same Question

Bind `helper-agent` with a research-focused SOUL.md. Ask both agents the same question.

Route to helper-agent:

```
What are the top 3 trends in AI agents for 2026?
```

Unbind and route back to main. Ask the same question.

Compare:

- Does the specialized SOUL.md produce a different answer?
- Does the research agent cite sources more consistently?
- What is the token cost difference in the dashboard?

**What you are learning:** Two agents with different SOUL.md files give structurally different answers to the same question. The workspace is where capability differentiation happens.

---

### Exercise 2 — Dashboard Side-by-Side

Open the Control UI (`openclaw dashboard`). Click between your two agent tabs.

Ask both agents:

```
What tools do you have access to?
```

Are the tool lists the same? They should be — gateway-level plugins are shared. The difference is in workspace files, not tool access.

Then ask each agent:

```
What skills do you have installed?
```

Are the skill lists the same? They should differ if you installed skills in only one workspace.

**What you are learning:** The dashboard makes the gateway vs workspace split visible. Same tools (gateway config). Different skills and identity (workspace config).

---

### Exercise 3 — Session Cache Test

While `helper-agent` is bound to WhatsApp, start a conversation and note the agent's identity. Then:

1. Update `helper-agent`'s IDENTITY.md to change the name
2. Continue the SAME conversation — does the name change?
3. Start a new conversation with `/new` — does the name change?

Record how many messages it took for the identity change to appear.

**What you are learning:** Session cache is the mechanism, not a bug. Identity changes are guaranteed to appear on the next session boundary. Understanding this prevents production confusion when a persona update seems to "not work."

---

### Exercise 4 — Design Your Split

Think about your actual use case. Write down 3-5 tasks you want automated.

For each task, decide:

- Which agent should handle it?
- What tools does that agent need?
- What should that agent NOT have access to?
- What workspace files need to be different?

Then ask your main agent:

```
I want to split my work between you and a helper agent. Here are my
tasks: [list them]. Which ones should you handle, and which should
the helper handle? Why? What tool access would each agent need?
```

Compare the agent's recommendation with your own design.

**What you are learning:** Multi-agent design is about access control and context boundaries, not personality. The split should be based on what each agent is allowed to do and what context it needs — not how it talks.

---

### Exercise 5 — Peer-Specific Routing

Set up sender-specific routing so your own number always goes to `main` and a test number goes to `helper-agent`.

Verify by sending from both numbers and checking the dashboard to confirm which agent handled each message.

Then try sending from a third number that has no specific binding. Confirm it falls back to `main`.

**What you are learning:** The binding system is a routing table. Peer-specific rules take priority. The main agent is always the fallback. No message is lost.

---

## Key Takeaways

**Two agents, one gateway:**

```bash
openclaw agents add helper-agent
openclaw agents unbind --agent main --bind whatsapp
openclaw agents bind --agent helper-agent --bind whatsapp
openclaw gateway restart
```

**The gateway vs workspace split:**

- Gateway config (shared): plugins, TTS, model, channels
- Workspace config (per-agent): SOUL.md, IDENTITY.md, skills, MCP, HEARTBEAT.md

Install a plugin → both agents. Edit SOUL.md → one agent.

**Session cache:** Identity and workspace changes take effect on new sessions, not existing ones. `/new` starts a fresh session. Existing conversations keep the old persona until they expire.

**Routing precedence:** Peer-specific > account-specific > channel-wide > main (fallback). The main agent never drops a message.

**The split is about access, not personality.** A customer-facing agent should not have admin-only skills. Workspace isolation enforces this at the capability level.

**Verify in the dashboard.** The agent tabs show which agent handled each conversation. Use this to confirm routing rules before testing with real users.

---

## Up Next

**Lesson 11 — Evaluating Readiness:** You have built a full Personal AI Employee across ten lessons. Before deploying it to real users, you need to know what actually works and what does not. Lesson 11 covers honest evaluation: the 28 documented gotchas, production readiness criteria, and how to test an agent the way a real user would.