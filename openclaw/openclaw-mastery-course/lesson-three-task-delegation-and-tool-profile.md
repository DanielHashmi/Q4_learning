# 3️⃣ Lesson 3 — Task Delegation and Tool Profile

## Lesson Overview

By the end you will be able to trace any message through the five-step **agent loop**, read the dashboard's tool badges as diagnostic output, and use **tool profiles** to control what your agent is allowed to do — not just what it knows.

> **Before you start:** Open the dashboard (`http://127.0.0.1:18789/`) and your messaging channel side by side. The dashboard is your instrument panel for this entire lesson. Everything you learn here is confirmed by reading it.
> 

---

## 1. The Core Distinction: Knowing vs. Doing

Every AI assistant *knows* how to list files on a computer. ChatGPT can describe the exact shell command. But describing a command and running it are different acts — they require different privileges.

This is the architectural line between a chatbot and an OpenClaw Employee:

| Capability | Chatbot | OpenClaw Employee |
| --- | --- | --- |
| Answer from training data | ✅ | ✅ |
| Remember context in session | ✅ | ✅ |
| Execute commands on your machine | ❌ | ✅ (with `exec` tool) |
| Read/write your files | ❌ | ✅ (with file tools) |
| Perform web searches | ✅ (most chatbot's like ChatGPT does, they call `web_search` tool) | ✅ (same `web_search` tool) |

The distinction is not intelligence. It is **access**. The tool profile is what controls that access — it is the key card, not the knowledge.

---

## 2. The Three-Task Experiment

Send these three tasks to your agent in order. After each one, go to the dashboard and click the message to inspect what happened.

---

### Task A — Knowledge

Send:

```
Tell me about yourself. What can you help me with?
```

The agent responds with a description of its capabilities.

**Now check the dashboard.** Click on this message. You will see:

- The response text
- The model used
- A token count
- **No tool badge**

The agent loaded its workspace files, reasoned over the request, and replied. It never touched your machine, never opened the internet. This is identical to what ChatGPT does.

---

### Task B — Your Machine

Send:

```
List the 5 largest files in my home directory.
```

The agent responds with actual file names and sizes from your computer — data that exists nowhere on the internet.

**Now check the dashboard.** You will see something new:

- An **"Exec" badge** next to the message
- A "Tool output" section you can expand
- Inside: the exact shell command the agent ran, and its raw output

The agent did not suggest a command for you to copy and paste. It ran the command itself, on your machine, and reported the results.

---

### Task C — The Internet

Send:

```
Search the web for "The AI Agent Factory" book. What is its thesis
and who authored it? It was published in 2026.
```

The agent responds with information it found via a live web search — not from its training data, not from your files.

**Now check the dashboard.** A different badge this time:

- A **"web_search" badge**
- Tool output showing the search results it retrieved

---

### What You Just Observed

Three tasks. Three different paths. Same agent, same loop.

| Task | What It Needed | Dashboard Badge | Loop Step 4 |
| --- | --- | --- | --- |
| A — Knowledge | Training data + workspace files | None | Skipped |
| B — Your machine | `exec` tool | Exec | Ran shell command |
| C — The internet | `web_search` tool | web_search | Ran live search |

The dashboard is not just a chat history viewer. It is an X-ray of the agent's decision-making. The badge tells you which path the agent took and why.

---

## 3. The Agent Loop

What the dashboard is showing you is the **agent loop** — the five-step cycle every message follows through the gateway.

```
1. INTAKE            Gateway receives and validates your message
2. CONTEXT ASSEMBLY  Workspace files, skills, and bootstrap build the prompt
3. MODEL INFERENCE   LLM reasons about the request and available tools
4. TOOL EXECUTION    Tools run if the model decided they are needed
5. REPLY & PERSIST   Response streams back; saved to session history
```

**Task A:** Steps 1 → 2 → 3 → 5. Step 4 skipped. Model decided at step 3 that no tools were needed. No badge.

**Task B:** Steps 1 → 2 → 3 → 4 (`exec`) → 5. Model decided at step 3 that a shell command was needed. Ran it at step 4. Exec badge.

**Task C:** Steps 1 → 2 → 3 → 4 (`web_search`) → 5. Same structure, different tool selected at step 3.

**The critical insight is in step 3.** The LLM is not just answering — it is deciding which tools (if any) to invoke. This decision is not pre-programmed per question type. The model reasons about it every time based on the request, the available tools, and the workspace context.

**Step 4 can also chain.** For complex tasks, the model may invoke multiple tools sequentially — read a file, then search the web based on its contents, then write a summary. The dashboard shows each tool call as a separate badge. You will see this in practice in Lesson 5.

### The Gateway Log

The dashboard shows summaries. When you need the raw event stream:

```bash
openclaw logs --follow
# File: /tmp/openclaw/openclaw-YYYY-MM-DD.log (rotated daily)
```

Every intake event, every tool invocation, every model call, every error — it is all in the log. Dashboard for understanding. Log for debugging.

---

## 4. Tool Profiles: Controlling What the Agent Can Do

Check your current tool profile:

```bash
openclaw config get tools.profile
```

The result is `coding` — the default after installation. The coding profile includes: file I/O, `exec` (runtime), sessions, memory, and image tools. That is why Tasks B and C worked.

But the agent's profile is not fixed. It is a configuration you control.

### View Profiles in the Dashboard

1. Open the dashboard (`http://127.0.0.1:18789/`)
2. Click **Agents** in the left sidebar
3. Click the **Tools** tab
4. Look at the current tool list and the **Quick Presets** at the bottom

You will see four presets:

| Profile | What It Includes | What Is Disabled |
| --- | --- | --- |
| **coding** | File I/O, exec, sessions, memory, image | Default after install |
| **messaging** | Message, session list/history/send/status | File access, exec, web search |
| **minimal** | `session_status` only | Almost everything |
| **full** | All tools, unrestricted | Nothing |

### Switch to Messaging and Watch It Break

1. In the dashboard, click **Messaging** under Quick Presets
2. Watch the tool list change — only five tools remain
3. Click **Save** (top right corner)
4. No restart needed. The change applies immediately.

Now send this to your agent:

```
List what is on my Desktop.
```

This is a **new** file request the agent cannot answer from memory. With the messaging profile active, it has no `exec` tool and no file I/O tools.

Check the dashboard. No tool badge. No exec. The agent knows how to list files — the knowledge did not change. But the messaging profile removed the tools it needs to act on that knowledge.

**This is the boundary.** Knowledge and access are separately controlled.

### Switch Back to Coding

1. Dashboard → Agents → Tools tab
2. Click **Coding** under Quick Presets
3. Click **Save**

Send the Desktop listing request again. The Exec badge reappears. Real listing returned.

### Why This Matters in Production

A customer-facing support agent with `exec` access is a security incident waiting to happen. A single clever prompt could instruct it to run arbitrary commands. Tool profiles are the first layer of defense.

The principle: grant the minimum access required for the task. A messaging-only agent needs messaging tools. An internal ops agent might need file I/O. A public bot needs neither. You will build layered `allow`/`deny` rules in Lesson 13.

---

## 5. Practical Exercises

### Exercise 1: Agent Self-Diagnostic

Your agent can read its own log. Send this:

```
Read today's gateway log at /tmp/openclaw/openclaw-YYYY-MM-DD.log
(where YYYY-MM-DD is today's date) and explain what happened
during the last file-listing task I sent you. Walk me through
each step of what the gateway did.
```

After it responds:

- Compare its explanation to what you saw in the dashboard
- Did it identify all five loop steps?
- Did it mention the `exec` tool call specifically?
- Did it report the exact command that was run?

**What you are learning:** The agent can analyze its own execution. The dashboard shows you a summary; the log gives the agent the raw data to reason over. This self-diagnostic capability is only possible because the agent has system access — which is exactly what makes tool profiles a security concern.

---

### Exercise 2: Profile Boundary Test

Switch your agent to the `minimal` profile (dashboard → Agents → Tools → Minimal → Save).

Then send these three tasks in sequence:

```
What is 2 + 2?
```

```
List the files in my home directory.
```

```
Search the web for the current price of Bitcoin.
```

For each one:

- What did the agent do?
- What badge appeared in the dashboard?
- Did the agent refuse, fail silently, or succeed?

After the experiment, switch back to the coding profile.

**What you are learning:** The minimal profile makes the boundary between knowledge and access concrete. The agent still has all its training-data knowledge. It simply cannot act on most of it.

---

### Exercise 3: When Would You Restrict Access?

Use any AI assistant (Claude, ChatGPT, Gemini) with the OpenClaw tools documentation:

```
Read https://docs.openclaw.ai/tools and answer:
When would you use the messaging profile instead of the full profile?
Give three real-world scenarios where restricting an agent's tools
is the right design decision, not a limitation to work around.
```

**What you are learning:** Tool restriction is architecture, not a constraint to minimize. The question of what to restrict is a product and security design question, not a technical one. Every profile choice is a statement about what the agent should be allowed to do on behalf of whom.

---

### Exercise 4: The Chatbot Comparison

Ask your agent:

```
Compare yourself to ChatGPT. What can you do that ChatGPT cannot?
Be specific and honest about the differences.
```

After it responds:

- Does its self-assessment match what you observed in the three-task experiment?
- Does it correctly identify tool execution (not just knowledge) as the concrete difference?
- Does it mention any limitations honestly?

**What you are learning:** An agent that can accurately describe its own capabilities and limitations is easier to use correctly and harder to misuse accidentally. Compare its answer against the dashboard evidence you now have.

---

## Key Takeaways

**The Agent Loop — five steps every message follows:**

1. **Intake** — gateway receives and validates the message
2. **Context Assembly** — workspace files, skills, and bootstrap build the prompt
3. **Model Inference** — LLM reasons about the request and which tools (if any) to invoke
4. **Tool Execution** — tools run only if the model requested them at step 3 (skipped otherwise)
5. **Reply & Persist** — response streams back and saves to session history

**Knowledge vs. Access:**

- The model always *knows* how to list files
- The tool profile controls whether it is *allowed* to
- These are separately controlled — changing a profile changes access, not knowledge

**Dashboard as diagnostic instrument:**

- No badge → step 4 skipped → knowledge-only response
- Exec badge → shell command ran on your machine
- web_search badge → live web query executed
- Multiple badges → tool chain (step 4 ran more than once)

**Tool Profiles — four defaults:**

- `coding` — full local access (default after install)
- `messaging` — messaging only, no system access
- `minimal` — almost nothing
- `full` — unrestricted

**The principle:** Grant minimum access required for the task. Production agents are scoped by role, not by convenience.

---

## Up Next

**Lesson 4 — Workspace Files:** You have seen the agent load "workspace files" at step 2 of the loop. Now you open them, edit them, and watch behavior change. `SOUL.md`, `IDENTITY.md`, `USER.md` — the DNA of your OpenClaw Employee.