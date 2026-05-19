# Lesson 12 — Orchestrate Other Agents

## Lesson Overview

Your agents work in isolation. This lesson connects them. You will use `sessions_spawn` to delegate tasks between agents, learn why the model — not the infrastructure — is the weakest link in orchestration, understand the two-layer concurrency model that determines how many customers can be served simultaneously, and control Claude Code from WhatsApp using ACP.

> **Critical before you start:** Orchestration tools require a capable model. Free-tier models fabricate reasons not to use them. If `sessions_spawn` does not fire, the problem is the model, not the platform. This lesson is where the $50-100/month model upgrade pays for itself.

> **Before you start:** Terminal open, dashboard open, both agents from Lesson 10 running.

---

## 1. The Model Limitation (Read This First)

Before attempting any orchestration command, understand the failure mode you will hit with free-tier or lightweight models.

**The free-tier orchestration failure pattern:**

1. You ask the agent to spawn a subagent
2. The model claims it "does not have permission" or the tool is "limited to specific session types" — both are hallucinations
3. You push back and ask if it has `sessions_spawn`
4. The model admits it has the tool but invents restrictions that do not exist
5. After two or three rounds of insistence, the model finally calls the tool, and it works

This is worse than simply ignoring the tool. The model generates plausible-sounding refusals that make you think the platform is broken. The same pattern from Lesson 8 (hallucinated cron flags) applies here.

**The workaround:**

```
Step 1: Clear the session context (/reset or /new)
        Old conversation history with refusal patterns causes the model to mimic them.

Step 2: Be explicit and persistent
        "Do you have the sessions_spawn tool? Use it now.
        Spawn a subagent that researches [topic]. Do not answer directly."

Step 3: If permission errors appear, push back
        Those are hallucinations. The tool works. Insist.
```

With a capable model (Claude Sonnet, GPT-4 class), this workaround is unnecessary. The model recognizes when delegation is appropriate and uses the tool unprompted. **Production orchestration requires a capable model.** If `sessions_spawn` only fires after you insist, your model is not reliable enough for autonomous delegation.

---

## 2. Subagent Delegation with sessions_spawn

`sessions_spawn` creates a subagent that runs a task independently and announces the result back to your chat.

**Default behavior:** Subagents run in the background. Your main agent remains responsive while the subagent works. When the subagent finishes, its result appears as an announcement in your chat. You can send other messages while it runs.

### Basic Delegation

Send your agent on WhatsApp:

```
Use sessions_spawn to research the top 3 trends in AI agent
platforms for 2026. Spawn a subagent for this task.
Do not answer directly.
```

While the subagent runs, check its status:

```
/subagents list
```

This shows each active subagent's model, runtime, status, and token usage. When the subagent finishes, the result announces back to your chat.

**If the agent answered directly without spawning:** Your model ignored the tool. Start a new session (`/reset`) and try with explicit prompting.

### Managing Subagents

| Command | Purpose |
| --- | --- |
| `/subagents list` | Show active and recent subagents with status, model, runtime, token usage |
| `/subagents kill 1` | Stop a running subagent |

### Two Delegation Patterns

**sessions_spawn (blocking):** Creates a subagent and waits for the full result before the main agent responds. Use when you need the complete answer before replying.

**sessions_yield (async):** The main agent responds immediately with "I'll get back to you" and the subagent runs in the background. Use when a 14-second pause feels unnatural in a chat context. `sessions_yield` matches WhatsApp's conversational cadence better.

### Nesting: Orchestrator Patterns

By default, subagents cannot spawn their own subagents. To enable orchestrator patterns:

```bash
openclaw config set agents.defaults.subagents.maxSpawnDepth 2
```

With depth 2:

- Main agent (depth 0) spawns an orchestrator (depth 1)
- Orchestrator spawns workers (depth 2)
- Results cascade upward: workers announce to orchestrators, orchestrators announce to you

**Tracking nested flows:**

```bash
openclaw tasks flow list                    # see active flows
openclaw tasks flow cancel <id>             # stop an entire tree at once
```

You will not need this until you increase `maxSpawnDepth` above 1.

---

## 3. The Two-Layer Concurrency Model

With orchestration working, the next question is: what happens when multiple customers message simultaneously? The answer is a two-layer queueing system.

### Layer 1: Session Lane (Per-Customer)

Every customer gets their own session lane. Within a session lane, messages are processed **sequentially** (`maxConcurrent = 1`).

```
Customer A sends: "Book 2pm tomorrow"
Customer A sends: "Wait, make that 3pm"

Session Lane A: [Book 2pm] ──→ [Change to 3pm]
                 processed first   waits for first
```

**Why sequential?** Conversation context matters. If "Book 2pm" and "Change to 3pm" run in parallel, you get a race condition — the booking might complete before the correction is processed. Sequential processing within a session guarantees message order.

### Layer 2: Global Lane (Shared)

The global lane is shared across all session lanes. If `maxConcurrent = 4`.

```
Session Lane A ──┐
Session Lane B ──┤
Session Lane C ──┼── Global Lane (max 4 concurrent) ──→ Model
Session Lane D ──┤
Session Lane E ──┘
         ↑
  Customer E waits here if all 4 slots are occupied
```

When a session lane's message is ready to process, it enqueues into the global lane. The global lane allows up to 4 concurrent executions. Four different customers can have their messages processed simultaneously.

### Concurrency Math: 5 Simultaneous Customers

1. Each message enters its own session lane
2. All five session lanes enqueue into the global lane
3. The global lane accepts the first 4 immediately
4. Customer 5 queues in the global lane
5. When one of the 4 finishes (typical agent turn: 3-8 seconds), customer 5 is dequeued

Customer 5 waits approximately 3-8 seconds. Not minutes..

### Real-World Scale: 55 Customers

| Time of Day | Active Customers | Simultaneous Messages | Queue Behavior |
| --- | --- | --- | --- |
| Morning check | 10-15 | 1-2 at same second | No queueing |
| Peak hour | 20-25 | 2-3 at same second | Rare, brief queueing |
| Blast scenario | 20+ respond | 10-20 at same second | Clears in waves, ~25 sec total |

With `maxConcurrent=4`, even a blast notification triggering 20 simultaneous responses clears in waves of 4. Four served immediately, four more after the first wave finishes (~5 seconds), and so on. Full queue clears in roughly 25 seconds. Acceptable for WhatsApp, where human expectation is a response within a minute.

### No Cross-Contamination

Session lanes are completely independent. Customer A's conversation history, context, and memory are never visible during Customer B's agent turn. The global lane controls **concurrency** (how many run at once), not **isolation** (what each sees). Isolation is handled by the session system from Lesson 2.

### Adjusting Concurrency

```bash
# Default setting
openclaw config get agents.defaults.maxConcurrent 8

# Increase for a more powerful server
openclaw config set agents.defaults.maxConcurrent 10
```

**Constraint:** Your model provider must handle the parallel request volume. At `maxConcurrent=4`, that is 4 simultaneous API calls. Free-tier providers with 15 requests per minute will hit rate limits within seconds. This is another reason production orchestration requires a paid model provider.

## 4. Queue Internals

Three details worth knowing for debugging:

**Generation tracking:** Each lane has a generation counter that increments on gateway restart. Stale tasks from a previous run are ignored — prevents zombie tasks from corrupting queue state.

**Gateway draining:** When the gateway shuts down, new enqueue attempts fail immediately instead of silently queuing work that will never execute.

**Wait callbacks:** Tasks that sit in queue beyond 2 seconds trigger a warning. This is how the gateway detects congestion before customers notice.

---

## 5. ACP: Control Claude Code from WhatsApp

ACP (Agent Client Protocol) is how OpenClaw controls external coding agents. From WhatsApp, you can spawn a Claude Code session that reads your codebase, runs commands, and reports back. Supported harnesses: Claude Code, Codex, Cursor, Copilot, Gemini CLI.

### Enable the ACP Plugin

The `acpx` plugin ships bundled with OpenClaw but is not enabled by default. Run `/acp doctor` in your WhatsApp chat to check:

```
/acp doctor
```

If output shows `ACP_BACKEND_MISSING`, follow the install steps printed by `/acp doctor`. After installing:

```bash
openclaw config set plugins.entries.acpx.enabled true
openclaw config set acp.enabled true
openclaw config set plugins.entries.acpx.config.permissionMode approve-reads
openclaw gateway restart
```

**The `permissionMode` line is critical.** ACP sessions are non-interactive — Claude Code cannot prompt you for permission through WhatsApp. Without a permission mode set, every file read or command execution is denied with `ACP_TURN_FAILED: Permission denied`.

| Mode | What It Allows |
| --- | --- |
| `approve-reads` | Read files and list directories. Block writes/exec. |
| `approve-all` | Read, write, and execute commands. |
| `deny-all` | Block everything (testing only). |

Start with `approve-reads`. Move to `approve-all` only when you trust the task and understand the risk.

Run `/acp doctor` again. The output should show `healthy: yes` before continuing.

### Spawn an External Agent

From WhatsApp:

```
/acp spawn claude --bind here
```

The `--bind here` flag binds the Claude Code session to your current conversation so that `/acp steer` commands reach it. Without `--bind here`, the session spawns but is unbound.

**Wait for the spawn confirmation before sending any commands.** If you send `/acp steer` before the session is ready, you get `ACP_SESSION_INIT_FAILED` because the steer targets your main WhatsApp agent instead of the spawned Claude Code session.

Once spawn confirms, send your request now:

```
/acp steer Summarize the README.md in my current project
```

Claude Code takes 10-30 seconds depending on the task. Check status:

```
/acp status
```

When done:

```
/acp close
```

**ACP sessions are persistent.** The session stays alive after completing a task, and you can send multiple `/acp steer` commands to the same session — it is a continuous conversation with Claude Code, not a one-shot task.

> ⚠️ **ACP sessions are NOT sandboxed.** Claude Code spawned via `/acp spawn claude` has the same filesystem access as Claude Code running in your terminal. The `permissionMode` you configured applies to all ACP sessions, whether you spawn them manually or the agent spawns them programmatically.

> **On Discord/Slack:** Use `--thread auto` to place the ACP session in its own thread for continuous back-and-forth. WhatsApp does not support threads, so `--bind here` is the only option.

### Your Agent Can Spawn Claude Code Too

You used `/acp spawn` manually. Your agent can do this on its own. The `sessions_spawn` tool supports `runtime="acp"`, meaning the agent can programmatically delegate a coding task to Claude Code:

```
Review the failing tests in my project and summarize the issues.
Use sessions_spawn with runtime acp to delegate this to Claude Code.
```

The agent spawns a Claude Code session, sends it the task, and announces the result. This is how your personal AI employee hands off technical work to a coding specialist: you describe what you need, the agent decides whether to handle it directly or delegate.

---

## 6. Practical Exercises

### Exercise 1 — Spawn a Subagent

Send your agent a delegation request:

```
Use sessions_spawn to research the top 3 trends in AI agent
platforms for 2026. Spawn a subagent for this task.
Do not answer directly.
```

While it runs, check status:

```
/subagents list
```

If the agent answered directly without spawning: your model ignored the tool. Note what it said, start a new session (`/reset`), and retry with explicit prompting.

Record:

- Did the model use the tool on the first try, or did it resist?
- How long did the subagent take?
- Was the result higher quality than a direct answer would have been?

**What you are learning:** `sessions_spawn` delegates work to a subagent. Model quality determines whether delegation happens autonomously or requires insistence. This distinction matters for production deployment decisions.

---

### Exercise 2 — The Concurrency Calculation

Ask your agent:

```
If I have maxConcurrent set to 4 and 7 customers message at the
same second, each taking 5 seconds to process, how long does
customer 7 wait? Explain the two-layer concurrency model.
```

Do your own calculation first, then compare:

- Customers 1-4 start immediately
- Customers 5-7 queue in the global lane
- After 5 seconds, the first 4 finish
- Customers 5-7 start
- Customer 7 waits approximately 5 seconds, not 15

Does the agent's answer match your calculation? Does it correctly explain session lanes (per-customer, sequential) vs the global lane (shared, parallel)?

**What you are learning:** The concurrency model processes in parallel waves, not sequentially. Understanding this lets you predict latency and set `maxConcurrent` correctly for your workload and model provider's rate limits.

---

### Exercise 3 — Three-Step Delegation Chain

Design a task that requires three agents:

1. Main agent receives the request and orchestrates
2. Subagent A researches a topic
3. Subagent B analyzes the research and formats a report

First increase spawn depth:

```bash
openclaw config set agents.defaults.subagents.maxSpawnDepth 2
```

Then send to your main agent:

```
I need a market analysis report on AI agent platforms.
Use sessions_spawn to:
1. Spawn one subagent to research the top 5 platforms and their features
2. Spawn another subagent to analyze competitive positioning
Then combine both results into a structured report.
```

Monitor with:

```bash
openclaw tasks flow list
```

**What you are learning:** Nested orchestration and the difference between parallel subagents (both spawn at once) vs sequential (one spawns after the other's result). The task flow list shows the delegation tree.

---

### Exercise 4 — Spawn Claude Code via ACP

If you have Claude Code installed, enable ACP and spawn it:

```
/acp doctor
```

Following any setup steps. Then:

```
/acp spawn claude --bind here
```

Wait for spawn confirmation. Then:

```
/acp steer Summarize the README.md in my current project
```

Check `/acp status`. Close when done with `/acp close`.

Then try having your main agent spawn Claude Code:

```
Review the most recently modified file in my project
and summarize any issues. Use sessions_spawn with runtime
acp to delegate this to Claude Code.
```

**What you are learning:** ACP turns external coding agents into OpenClaw-managed sessions. The difference between `/acp spawn` (manual) and `sessions_spawn runtime="acp"` (programmatic) is who initiates the delegation — you, or the agent itself.

---

### Exercise 5 — Model Reliability Assessment

Test your model's orchestration reliability. Send the same delegation request five times, starting a new session each time:

```
Use sessions_spawn to summarize the current time and date.
Spawn a subagent. Do not answer directly.
```

Count:

- How many times did the model use `sessions_spawn` on the first try?
- How many times did it resist?
- What hallucinated reasons did it give?

If the success rate is below 4/5, your model is not reliable enough for autonomous orchestration in production. Document the result.

**What you are learning:** Reliability testing is a prerequisite for production deployment. A model that sometimes delegates and sometimes refuses is not suitable for customer-facing orchestration. The number you measure here informs the Lesson 14 deployment decision.

---

## Key Takeaways

**Two delegation patterns:**

- `sessions_spawn` (blocking): main agent waits for the full result before responding
- `sessions_yield` (async): main agent responds immediately, subagent works in background

**Two-layer concurrency:**

- Session lane (per-customer): sequential, preserves conversation order
- Global lane (shared): parallel, default `maxConcurrent=8`
- With 4 slots and 7 customers: customers 1-4 start immediately, 5-7 wait ~5 seconds
- `maxConcurrent` must not exceed your model provider's rate limit

**ACP:**

- `/acp spawn claude --bind here` controls Claude Code from WhatsApp
- `permissionMode` is required for non-interactive sessions (`approve-reads` to start)
- `sessions_spawn runtime="acp"` lets your agent spawn Claude Code programmatically
- ACP sessions are NOT sandboxed — same filesystem access as terminal Claude Code

## Up Next

**Lesson 13 — Hooks and Security:** Your agents can now delegate to each other and spawn external coding sessions. Before deploying to real users, you need approval gates — points where a human reviews what the agent is about to do. Lesson 13 covers the three-tier security model and how to build hooks that intercept agent actions.
