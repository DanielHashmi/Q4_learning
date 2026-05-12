# 5️⃣ Lesson 5 — Memory & Commands

## Lesson Overview

Session memory fades when a conversation ends. This lesson builds the persistence layer that does not. You will store a preference that survives across sessions, verify it on disk (not just in chat), test cross-session recall, and learn the full memory architecture behind it. You will also discover slash commands — gateway-intercepted instructions that cost zero tokens and respond instantly.

> **Core habit this lesson teaches:** Verbal confirmation is not proof of a file write. Verify on disk.
> 

> **Before you start:** Open a terminal, your messaging channel, and the dashboard (`http://127.0.0.1:18789/`) side by side.
> 

---

## 1. The Problem: Session Memory Fades

Everything your agent learned about you in a conversation exists in the session snapshot (Layer 2 from Lesson 4). When the session ends, that snapshot is gone. The next session starts fresh from the workspace files on disk.

This means:

- "Remember I like bullet-point summaries" → gone tomorrow
- "My timezone is UTC+5" → gone tomorrow
- "Never use numbered lists for reports" → gone tomorrow

The fix is not repeating yourself. The fix is writing preferences to a file that loads every session.

---

## 2. Store a Preference

Send this to your agent:

```
Save in memory: I prefer all summaries under 100 words as bullet points.
Never use numbered lists for summaries.
```

**Why "Save in memory:" specifically?**

If you say "Remember this:" or "Note that:", the agent may respond with "Got it!" without writing anything to disk. The phrase "Save in memory:" signals an explicit file write. The intent is the same. The action is different.

---

## 3. Verify on Disk — Not Just in Chat

After the agent confirms, open a terminal and run:

```bash
cat ~/.openclaw/workspace/MEMORY.md
```

You should see your preference:

```
# Preferences
- Summary format: Always under 100 words, use bullet points, never numbered lists.
```

**If the file is empty or the preference is missing:** The agent acknowledged your request without acting on it. Send the request again with "Save in memory:" at the start.

**Verify in the dashboard too:** Open the dashboard and look at your recent chat. Find the message where you asked the agent to save the preference. There should be a **tool badge** indicating a file write operation. This badge is visual proof the agent wrote to disk.

---

## 4. Test Cross-Session Recall

Close the conversation. Start a new one. Then send:

```
What are my preferences for summaries?
```

The agent recalls your bullet-point preference without you repeating it. It did not re-read the old conversation. It read MEMORY.md, which loaded when the new session started.

---

## 5. The Full Memory Architecture

What you just used is one part of a larger system. Your agent has multiple memory layers, each with a different scope, loading behavior, and purpose.

### The Two Memory Locations

| Location | What It Stores | When It Loads |
| --- | --- | --- |
| `~/.openclaw/workspace/MEMORY.md` | Curated long-term memory: preferences, facts, key decisions | Every session start (DM only) |
| `~/.openclaw/workspace/memory/YYYY-MM-DD.md` | Daily logs: session notes, observations, raw history | Today + yesterday at session start |
| `memory/older/*.md` | Archive of all older daily logs | On demand via `memory_search` only |

```bash
# See your daily log files
ls ~/.openclaw/workspace/memory/
```

You will see one file per day your agent has been active.

### MEMORY.md Security Boundary

MEMORY.md loads **only in your main private session** (DMs).

| Context | [MEMORY.md](http://MEMORY.md) loaded? |
| --- | --- |
| Main private session (DM) | ✅ Yes |
| Group chat or shared channel | ❌ No |
| Subagent context | ❌ No |

This is not a technical limitation — it is a security boundary. MEMORY.md holds personal context, preferences, and private facts. That content must not leak to strangers who share a group chat with your agent.

### Cross-Channel Memory Behavior

Memory files live at the agent level, not the channel level. If you save a preference over WhatsApp and later connect on Discord, both channels read the same MEMORY.md.

Whether they share the same conversation history is separate, controlled by `session.dmScope`:

- `main` (default): all DMs share one session
- `per-channel-peer`: each channel gets its own isolated session

**Short version:** Memory persists across channels. Sessions are routed per config.

---

## 6. The Three-Tier Retrieval System

At session start, only MEMORY.md + today's log + yesterday's log auto-load. Older logs stay on disk. The agent retrieves them on demand through two tools:

**`memory_search`** — Hybrid retrieval combining vector similarity (meaning matching) and keyword matching (exact terms, IDs, code symbols). Returns a ranked list of snippets. Auto-detects your embedding provider (OpenAI, Gemini, Voyage, or Mistral) from whichever API key is available.

**`memory_get`** — Reads a specific memory file or line range. Used when the agent already knows the path (e.g., today's log) or when a `memory_search` snippet needs its full context.

```
Turn starts:
│
├── Tier 1: MEMORY.md + today + yesterday
│           → loaded at session start
│           → Most turns stop here
│
├── Tier 2: memory_search
│           → Hybrid retrieval, ranked snippets
│           → Used when Tier 1 doesn't have what's needed
│
└── Tier 3: memory_get
            → Full file read
            → Used when a specific file or line range is needed
```

The design is intentional: load recent context automatically, search older context on demand. Loading every daily log since installation would burn tokens on irrelevant history.

---

## 7. The Three Paths to MEMORY.md

Notes reach MEMORY.md through exactly three paths. **Heartbeats are not one of them** — heartbeats run periodic self-checks defined in HEARTBEAT.md, unrelated to memory promotion.

### Path 1: Manual

You say `Save in memory:`. The agent writes to MEMORY.md immediately. You verify on disk. This is the path you fully control.

### Path 2: Compaction Memory Flush

When a conversation runs long, the context window fills up. OpenClaw handles this through **compaction**: older turns get summarized into a compressed version, freeing space. The summary preserves the gist but loses precise wording.

Before compaction runs, OpenClaw runs a **silent memory flush**: a hidden turn where the agent is instructed to write anything important from the conversation to MEMORY.md or today's daily log. Durable context escapes to disk. Then compaction summarizes the older turns.

This is on by default. The sequence:

```
1. Context window nearing full
2. [Silent turn] Agent saves durable context to MEMORY.md / daily log
3. Compaction summarizes older turns
4. Conversation continues with freed space
```

Trigger compaction manually:

```
/compact
```

In the dashboard: you will see a tool badge for any file writes the flush triggered, followed by a summary turn.

### Path 3: Dreaming (Opt-In)

Daily logs accumulate. Most entries are noise. Some are signal. **Dreaming** is OpenClaw's background consolidation pass that promotes only material meeting a quality bar.

Dreaming runs in three phases:

| Phase | Purpose | Promotes to MEMORY.md? |
| --- | --- | --- |
| **Light** | Sort and stage recent material. Dedupe. Record reinforcement signals. | No |
| **REM** | Build theme and reflection summaries. Record signals for Deep phase. | No |
| **Deep** | Score candidates. Promote those passing score, recall-frequency, and query-diversity thresholds. | Yes |
- **Light Phase** = **Collects and cleans** recent memory data. Think of it as gathering and sorting raw notes.
- **REM Phase** = **Finds patterns and themes** in those notes. Think of it as stepping back and asking *"what does all this mean?"*

**Only the Deep phase ever appends to MEMORY.md.** A candidate must pass three gates simultaneously: ranking score, recall frequency (surfaced multiple times), and query diversity (appeared across different kinds of queries on different days).

**Enable dreaming** — add to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

**Control dreaming from chat:**

```
/dreaming status
/dreaming on
/dreaming off
```

**Review what dreaming promoted:**

```bash
cat ~/.openclaw/workspace/DREAMS.md
```

The `DREAMS.md` file is only generated in your agent's workspace once the dreaming system executes its first background sweep or when you manually run a memory backfill command.

You can force the creation of **`DREAMS.md`** by running a manual backfill command from your terminal:

```
openclaw memory rem-backfill --path ./memory
```

But this command only works if you have daily memories, otherwise you see this:

```bash
Memory rem-backfill found no YYYY-MM-DD.md files at ~/.openclaw/memory
```

`DREAMS.md` contains narrative-style diary entries: what was staged, what themes were found, what was promoted. The dashboard's **Dreams** tab shows the same data with phase counts and next scheduled run.

---

## 8. Active Memory: The Anticipation Layer (Opt-In)

Even with MEMORY.md loaded, the main agent only searches memory when you remind it to. By the time you remind it, the natural moment for recall has passed.

**Active memory** changes this. It is a blocking sub-agent that runs before every DM reply with two tools (`memory_search` and `memory_get`) and one job: decide whether anything in long-term memory is relevant to what you just said. If something is relevant, it returns a compact summary. If nothing is, it returns `NONE`. That summary is injected as hidden system context for the main reply.

Result: the agent incorporates a preference you saved weeks ago without you reminding it. The recall happened in a sub-agent turn before the main reply was generated.

**Why it is opt-in:** It runs before every eligible reply, adding latency (hundreds of ms to seconds per reply) and token cost on every turn. Start with it off.

**Enable in `openclaw.json`:**

```json
{
  "plugins": {
    "entries": {
      "active-memory": {
        "enabled": true,
        "config": {
          "agents": ["main"],
          "allowedChatTypes": ["direct"],
          "queryMode": "recent",
          "promptStyle": "balanced",
          "timeoutMs": 15000,
          "maxSummaryChars": 220
        }
      }
    }
  }
}
```

Restart gateway and verify if it’s working**:**

```
/verbose on
```

After enabling, send a message that should benefit from a saved preference. The reply looks normal, but two status lines appear:

```
🧩 Active Memory: ok 842ms recent 34 chars
🔎 Active Memory Debug: Bullet points only, never numbered lists.
```

First line: active memory ran in 842ms, returned 34 chars. Second line: the hidden context the main model received.

**Session-scoped controls (no config change needed):**

```
/active-memory off
/active-memory on
/active-memory status
```

**Tuning `queryMode`:**

- `recent` (default) — good starting point
- `recall-heavy` — surfaces more, more often
- `precision-heavy` or `strict` — surfaces less, only high-confidence matches

---

## 9. When You Outgrow the Builtin Engine

The default memory backend is SQLite with vector + keyword search. It handles most personal setups without configuration.

| Backend | What It Adds | When to Switch |
| --- | --- | --- |
| **Builtin** (default) | SQLite, vector + keyword search | Most personal setups |
| **QMD** | BM25 + vector + reranking, indexes external directories, can index session transcripts | Higher-quality results, search beyond workspace, or fully local |
| **Honcho** | AI-native service, auto-builds user profiles, cross-session and multi-agent tracking | Automatic profile building or shared memory across agents |
| **LanceDB** | Local embeddings, Ollama-friendly | Fully local with no external API |

All four backends expose the same `memory_search` and `memory_get` tool surface. Your workspace files and skills do not change when you swap backends — only the config changes.

Do not switch today. When the builtin engine feels slow or limited, read the [memory concepts docs](https://docs.openclaw.ai/concepts/memory).

---

## 10. Slash Commands

Your agent responds to natural language. It also accepts slash commands. Send:

```
/help
```

The response is instant. No "thinking" indicator. No tool badge. The gateway intercepted `/help` and returned the result directly. **The model never processed your message. Zero tokens spent.**

Now send:

```
/status
```

Instant diagnostics: current model, session state, quota information.

### Prove the Difference

Ask the same thing in natural language:

```
What model are you currently using?
```

Slower. May show a thinking indicator. No tool badge — the model had to interpret your question, reason about it, and compose a response. The latency difference is the proof.

### Command Reference

| Command | What It Does |
| --- | --- |
| `/help` | Lists available commands |
| `/status` | Model, session state, quota diagnostics |
| `/model <name>` | Switch model mid-conversation |
| `/reset` | Fresh session (clears conversation, keeps memory) |
| `/compact` | Summarize older turns + silent memory flush |
| `/context list` | Show loaded workspace files and token counts |
| `/context detail` | Per-tool and per-skill context breakdown |
| `/commands` | Full list of available commands (grows as plugins are added) |
| `/verbose on` | Show active memory runtime and hidden context debug |
| `/dreaming status` | Dreaming phase status |
| `/active-memory status` | Active memory status |

> **After installing your first plugin in Lesson 6:** Run `/commands` again. The list grows. Each plugin registers its own commands.
> 

### CLI Memory Commands

These run from a terminal, outside the chat:

```bash
# Check index health and which embedding provider is active
openclaw memory status

# Search notes from the command line (bypasses the agent entirely)
openclaw memory search "query"

# Rebuild the search index if results seem stale
openclaw memory index --force
```

Use these when the agent's recall seems wrong. `search` confirms what the index can actually find. `index --force` fixes most "should remember this but doesn't" situations.

---

## 11. Practical Exercises

### Exercise 1 — Build a Memory Profile

Tell your agent to save five things about you. Use "Save in memory:" for each:

1. Your role
2. Your preferred communication style
3. Your timezone
4. A current project you are working on
5. One thing the agent should never do

After all five saves, close the conversation and start a new one. Ask:

```
What do you know about me?
```

Then verify on disk:

```bash
cat ~/.openclaw/workspace/MEMORY.md
```

Does what the agent recalls match what is on disk exactly? Are there any discrepancies? If the agent recalls something not in the file, it is hallucinating. If the file has something the agent did not mention, the context window may be getting full.

---

### Exercise 2 — Dashboard Detective

Open the dashboard and scroll through your recent chat history. For each message where you asked the agent to remember something:

- Is there a tool badge?
- Did the tool badge indicate a file write?

Now send two test messages:

```
Remember this: my favorite color is blue.
```

Then:

```
Save in memory: my preferred meeting length is 25 minutes.
```

Check the dashboard for tool badges on each. Did both trigger a file write? Or only the second one?

Then check the disk:

```bash
cat ~/.openclaw/workspace/MEMORY.md
```

Which entries are there?

**What you are learning:** The phrasing matters. "Remember this" often produces verbal acknowledgment without action. "Save in memory:" triggers an actual write. The dashboard shows you which is which.

---

### Exercise 3 — Gateway vs Model Latency

Time these two interactions:

1. Send `/status` — note the response time
2. Ask "What is your current status?" in natural language — note the response time

Then try switching models mid-conversation:

```
/model gemini-2.5-flash
```

Ask a question. Then switch back:

```
/model gemini-3.1-flash-lite-preview
```

The model switches without restarting the session.

**What you are learning:** Slash commands are gateway-intercepted. They cost zero tokens and respond instantly. Natural language goes through the full five-step agent loop. The `/model` command is the practical demonstration: instant model swap, no restart, no session disruption.

---

### Exercise 4 — Compaction and the Silent Flush

Have a long conversation with your agent. Ask it twenty or thirty questions — anything that keeps the conversation going. Then send:

```
/compact
```

After compaction, check the dashboard. You should see:

1. A tool badge for any file writes the silent flush triggered
2. A summary turn
3. Continuation of the conversation

Then check the disk:

```bash
cat ~/.openclaw/workspace/MEMORY.md
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

Did the flush write anything new? What did it decide was worth preserving?

**What you are learning:** Compaction is not a loss. It is a controlled compression with a safety net. The silent flush runs first, giving the agent one chance to write durable context to files before older turns are summarized.

---

### Exercise 5 — Memory Search CLI

After at least one full day of conversations with your agent:

```bash
# Check index health
openclaw memory status

# Search for something you discussed
openclaw memory search "[topic you discussed]"

# Try rebuilding the index
openclaw memory index --force
openclaw memory search "[same topic]"
```

Did the search results improve after rebuilding? Does the CLI search find things the agent did not surface in conversation?

**What you are learning:** The CLI memory surface lets you debug recall without going through the agent. If the agent says it cannot remember something, `openclaw memory search` tells you whether the failure is a retrieval problem or a context problem.

---

## Key Takeaways

**The store-verify-recall cycle — do this in order every time:**

```
"Save in memory:" → cat ~/.openclaw/workspace/MEMORY.md → dashboard tool badge
→ close conversation → open new session → ask the agent
```

**Two memory locations:**

- `MEMORY.md` — curated notebook, loads every DM session
- `memory/YYYY-MM-DD.md` — daily journal, today + yesterday auto-load, older on demand

**Three paths to MEMORY.md:**

1. Manual (`Save in memory:`)
2. Compaction memory flush (silent, before summarization)
3. Dreaming deep phase (opt-in, scheduled, gated by score + recall frequency + query diversity)

**Heartbeats ≠ memory promotion.** Heartbeats run self-checks. They do not promote notes to MEMORY.md.

**MEMORY.md is compartmentalized:** DM sessions only. Never groups, never subagents. Security boundary, not a technical limitation.

**Slash commands bypass the model:** Zero tokens, instant response. `/help`, `/status`, `/model`, `/reset`, `/compact`, `/commands`. Natural language uses the full agent loop.

**Verify on disk, not just in chat.** Verbal confirmation is not proof of a file write.

**Active memory is opt-in:** Blocking sub-agent before every DM reply. Adds latency and tokens on every turn. Off by default for good reason.

**Keep MEMORY.md curated, not a dump.** A MEMORY.md with 200 entries pushes later entries past the model's attention window. When it starts growing too large, curate it down to the entries that actually change behavior.

---

## Up Next

**Lesson 6 — Skills and the Ecosystem:** Your agent knows what it was trained on. Skills let it know what you need it to know — domain-specific knowledge, workflows, and external integrations installed directly into the workspace.