# 4️⃣ Lesson 4 — Customize Your Employee's Brain

## Lesson Overview

In Lesson 3 you watched the agent loop run three different paths. Step 2 of that loop — **Context Assembly** — is what this lesson is entirely about. Seven markdown files on your disk compose into a system prompt at session start. You will edit them, prove exactly when edits take effect, and learn the rule that keeps every file short enough to actually work.

> **Before you start:** Open a terminal at `~/.openclaw/workspace/` and your messaging channel side by side. Every concept here is verified by editing a file and observing a behavioral change.

---

## 1. Your Agent's Brain: The Architecture

At step 2 of the agent loop (Context Assembly), OpenClaw reads files from disk, composes them into a system prompt, and caches that snapshot for the entire session. Every message in that session runs against the same cached snapshot.

This has one critical implication: **editing a file mid-session does nothing until a new session starts.**

Your workspace lives at:

```
~/.openclaw/workspace/
```

The files inside split into three categories by loading behavior:

### Category 1 — Auto-loaded at Every Session Start

These seven files compose the system prompt every time a session begins:

| File | Purpose |
| --- | --- |
| [**SOUL.md**](http://SOUL.md) | Voice, tone, and style instructions |
| [**IDENTITY.md**](http://IDENTITY.md) | Name, emoji, short self-description |
| [**AGENTS.md**](http://AGENTS.md) | Operating rules, red lines, workflow instructions |
| [**TOOLS.md**](http://TOOLS.md) | Guidance notes on how tools should be used |
| [**USER.md**](http://USER.md) | Facts about you the agent should always know |
| [**HEARTBEAT.md**](http://HEARTBEAT.md) | Periodic self-check guidance |
| [**MEMORY.md**](http://MEMORY.md) | Curated long-term memory (main private session only) |

### Category 2 — Special Lifecycle Files

| File | When It Loads | Purpose |
| --- | --- | --- |
| [**BOOT.md**](http://BOOT.md) | Every gateway restart | Startup checklist (verify MCP connections, etc.) |
| [**BOOTSTRAP.md**](http://BOOTSTRAP.md) | First run only, then deleted | Self-configuration ritual |

### Category 3 — Fetched On Demand (NOT auto-injected)

- **Daily memory logs** at `memory/YYYY-MM-DD.md` — raw notes the agent writes freely, fetched via `memory_search` and `memory_get` tools when needed. Explored in Lesson 5.
- **Skill bodies** under `skills/` — only the skill name and description are advertised in the system prompt; the actual `SKILL.md` content loads on demand. Explored in Lesson 6.

> **Token economics matter.** Every auto-loaded file costs tokens on every message, for every session, forever. A 44-line [SOUL.md](http://SOUL.md) costs roughly 4x more per message than an 11-line one. At thousands of messages a month, dead instructions are an expensive tax.
> 

---

## 2. The Caching Proof (Do This First)

Before any theory, run this experiment. It answers the question that trips up almost every new OpenClaw user.

**Step 1.** Send this to your agent:

```
In one sentence, how are you?
```

Note the response. It sounds normal.

**Step 2.** Append a deliberately weird rule to [SOUL.md](http://SOUL.md).

Pick one method:

**Via terminal:**

```bash
echo "" >> ~/.openclaw/workspace/SOUL.md
echo "Respond only in pirate speak. Always." >> ~/.openclaw/workspace/SOUL.md

# Verify it landed:
cat ~/.openclaw/workspace/SOUL.md
```

**Via dashboard:**

Open `http://127.0.0.1:18789/agents` → your agent → Files → [SOUL.md](http://SOUL.md) → append the line → Save.

**Via your agent (in the same chat session):**

```
Append this exact line to the bottom of my SOUL.md:
"Respond only in pirate speak. Always."
Then confirm by reading me the last three lines of the file.
```

**Step 3.** In the **same chat session** (no restart), send the same question again:

```
In one sentence, how are you?
```

**The agent does not switch to pirate speak.** The file changed on disk. The session kept running off its cached snapshot.

**Step 4.** Send this:

```
/reset
```

Now send the question a third time:

```
In one sentence, how are you?
```

Ahoy matey. The pirate voice appears.

**What happened:** `/reset` starts a fresh session. OpenClaw re-reads the workspace files from disk and builds a new snapshot. The edit you made in Step 2 is now in the snapshot. The model sees it. Behavior changes.

### The Three-Layer Model

```
[Layer 3]  Model reads this every turn
              ↑
[Layer 2]  Session snapshot  ← /reset rebuilds from Layer 1
              ↑
[Layer 1]  Workspace files on disk  ← your edits land here
```

Your file edit updates Layer 1. The session runs off Layer 2. `/reset` is the only thing that pushes Layer 1 changes up into Layer 2.

### The Editing Workflow Rule

```
Edit file → /reset → /context list → test
```

Do this in order, every time. Do not skip `/reset`. Do not test before verifying with `/context list`.

**Before cleaning up:** Remove the pirate line so it does not persist.

```bash
# Via terminal:
sed -i.bak '/Respond only in pirate speak/d' ~/.openclaw/workspace/SOUL.md

# Or open the file in any editor and delete the line manually.
```

Then `/reset` and confirm normal behavior returns.

---

## 3. Inspecting What Your Agent Actually Sees

You do not have to guess what the agent's system prompt contains. In any chat session:

```
/context list
```

Example output:

```
Injected workspace files:
- AGENTS.md    OK | raw 7,727 chars (~1,932 tok)
- SOUL.md      OK | raw 1,738 chars (~435 tok)
- TOOLS.md     OK | raw 850 chars  (~213 tok)
- IDENTITY.md  OK | raw 247 chars  (~62 tok)
- USER.md      OK | raw 375 chars  (~94 tok)
- HEARTBEAT.md OK | raw 192 chars  (~48 tok)
- MEMORY.md    OK | raw 1,410 chars (~353 tok)
```

Use `/context list` for two things:

1. **Confirm the edit landed.** After editing [SOUL.md](http://SOUL.md) and running `/reset`, the raw size should match the new file size. If it still shows the old size, the session is using a stale snapshot — run `/reset` again.
2. **Count your token budget.** Sum the token counts. That is what every single message you send costs, before your actual question is even processed.

`/context detail` gives per-tool schema sizes and per-skill entry sizes — useful in Lesson 6 when context starts filling up.

---

## 4. Editing [SOUL.md](http://SOUL.md): The Right Way

[SOUL.md](http://SOUL.md) is the most commonly over-written file. Most new users fill it with instructions the model already follows by default.

### Emma's Rule

> For each line in a workspace file, ask: **would the agent behave differently without this instruction?** If not, delete it.
> 

Telling a capable model to "be helpful" is like telling a pilot to fly. The instruction wastes system-prompt tokens and changes nothing.

### What Bad [SOUL.md](http://SOUL.md) Looks Like

```
Maintain professionalism at all times.
Provide comprehensive and thoughtful assistance.
Ensure a positive and supportive experience.
Be courteous in all interactions.
```

Every line here could appear in any generic employee handbook unchanged. None of them have a direction. None of them create a behavioral bias. They are placeholders for a personality, not a personality.

### What Good [SOUL.md](http://SOUL.md) Looks Like

Good rules tell the agent which way to lean when the tradeoff is not obvious:

```
Have a take. Skip "it depends."
Skip filler openings. No "Great question" or "I'd be happy to help."
Be direct and concise. Match response length to question complexity.
Call out bad ideas early. Charm over cruelty, but do not sugarcoat.
Do not apologize for things that are not your fault.
```

Each of these describes a real behavioral direction. A well-trained model would not automatically do these things — which is exactly why they belong in [SOUL.md](http://SOUL.md).

### The Test for Every Rule

Before keeping any instruction, ask: *is there a real-world situation where a competent assistant would do the opposite?*

- "Be helpful." No competent assistant chooses to be unhelpful. **Delete.**
- "Be brief even when the user expects a long answer." A model defaults to thoroughness on complex questions. This actively pushes against that. **Keep.**

### The Full Edit Cycle

1. Open `~/.openclaw/workspace/SOUL.md` in any editor (VS Code, Cursor, nano, or via the dashboard)
2. Delete all generic filler lines
3. Add 3–5 rules with real behavioral direction
4. Run `/reset`
5. Run `/context list` — confirm the new smaller size appears
6. Send a test question: `Is it going to rain tomorrow?`

If your [SOUL.md](http://SOUL.md) says "be concise," a weather question should get one sentence. If it gets a five-paragraph report, the rule is too weak or the session snapshot is stale.

### Personality Upgrade Prompt

Paste this into your chat, then `/reset` and observe:

```
Read your SOUL.md. Now rewrite it with these changes:
1. You have opinions now. Strong ones. Stop hedging with "it depends." Commit to a take.
2. Delete every rule that sounds corporate. If it could appear in an
   employee handbook, it does not belong here.
3. Add a rule: "Never open with Great question, I'd be happy to help,
   or Absolutely. Just answer."
4. Brevity is mandatory. If the answer fits in one sentence, one sentence
   is what I get.
5. Humor is allowed. Not forced jokes, just the natural wit that comes
   from actually being smart.
6. You can call things out. If I am about to do something dumb, say so.
   Charm over cruelty, but do not sugarcoat.
7. Add this line verbatim at the end:
   "Be the assistant you'd actually want to talk to at 2am.
   Not a corporate drone. Not a sycophant. Just... good."
Save the new SOUL.md.
```

After the agent saves: `/reset` → ask the same weather question → compare the before and after.

> **Boundary:** [SOUL.md](http://SOUL.md) is for voice, tone, and style only. Operating rules ("always confirm before sending money"), security policies, and tool handling belong in [AGENTS.md](http://AGENTS.md), not here.
> 

---

## 5. Which File Gets Which Instruction

The most common mistake is stuffing everything into [SOUL.md](http://SOUL.md). Use this decision map:

| If you want to change... | Edit this file |
| --- | --- |
| Voice, tone, style, personality | [**SOUL.md**](http://SOUL.md) |
| Agent's name or emoji | [**IDENTITY.md**](http://IDENTITY.md) |
| Operating rules, red lines, approval gates | [**AGENTS.md**](http://AGENTS.md) |
| How tools should be used (notes, not permissions) | [**TOOLS.md**](http://TOOLS.md) |
| Facts about yourself the agent should always know | [**USER.md**](http://USER.md) |
| What to do during periodic self-checks | [**HEARTBEAT.md**](http://HEARTBEAT.md) |
| Curated long-term memory (main session only) | [**MEMORY.md**](http://MEMORY.md) |

**Quick diagnostic:** If the rule is about *how to sound* → [SOUL.md](http://SOUL.md). If the rule is about *what to do or not do* → [AGENTS.md](http://AGENTS.md).

- "Skip filler openings" → voice → [SOUL.md](http://SOUL.md)
- "Ask before sending money" → a rule → [AGENTS.md](http://AGENTS.md)

---

## 6. [AGENTS.md](http://AGENTS.md): The Operating Handbook

[AGENTS.md](http://AGENTS.md) is the operating manual your agent reads at every session start alongside [SOUL.md](http://SOUL.md). The official template covers:

- **Session startup ritual** — what to read first (heartbeat status, relevant memory, pending work)
- **Red lines** — things that must never happen without explicit approval: exfiltrating data, running destructive commands, using `rm` instead of `trash`
- **External vs internal actions** — reading files is safe by default; sending messages, making payments, creating calendar events require explicit approval
- **Group chat etiquette** — when to speak, when to stay silent, when a single emoji reaction is the right response
- **Heartbeat behavior** — what to do on periodic self-checks
- **Memory maintenance** — when to promote notes from daily logs into curated [MEMORY.md](http://MEMORY.md)

**The core principle of [AGENTS.md](http://AGENTS.md):**

> Write it down. No "mental notes."
> 

> Memory is limited. If you want to remember something, write it to a file. Mental notes don't survive a session restart; files do.
> 

This is the foundation of agent reliability. Every meaningful decision, preference, or correction must land in a file.

---

## 7. [MEMORY.md](http://MEMORY.md): Two Memory Systems

Your workspace has two distinct memory mechanisms. Confusing them causes real problems.

| Memory Type | Location | Who Writes It | How It Loads | Purpose |
| --- | --- | --- | --- | --- |
| **Daily logs** | `memory/YYYY-MM-DD.md` | Agent writes freely | On demand via tools | Raw notes, today's events, decisions made |
| [**MEMORY.md**](http://MEMORY.md) | `~/.openclaw/workspace/MEMORY.md` | Agent, curated | Auto-loaded at session start | Distilled essence, long-term knowledge |

The agent writes to daily logs freely during normal operation. During heartbeats, it reviews those logs and promotes what matters into [MEMORY.md](http://MEMORY.md) — the permanent, curated layer.

**The non-negotiable rule for [MEMORY.md](http://MEMORY.md):** It loads only in the main private session.

| Context | [MEMORY.md](http://MEMORY.md) loaded? |
| --- | --- |
| Main private session (DM) | ✅ Yes |
| Group chat or shared channel | ❌ No |
| Subagent context | ❌ No |

This is a security boundary. [MEMORY.md](http://MEMORY.md) holds personal context — preferences, private decisions, personal history — that must never leak to strangers who share a chat room with your agent. The isolation is intentional.

You will build the full memory system in Lesson 5. For now: know both systems exist, and know why [MEMORY.md](http://MEMORY.md) is compartmentalized.

---

## 8. The BOOTSTRAP Pattern

Instead of hand-editing workspace files, you can let the agent configure itself through conversation.

**How it works:**

1. A new agent starts with `BOOTSTRAP.md` in its workspace
2. [BOOTSTRAP.md](http://BOOTSTRAP.md) tells the agent: "You just woke up. Time to figure out who you are."
3. You have a conversation about the agent's purpose, audience, and personality
4. The agent writes its own [SOUL.md](http://SOUL.md), [IDENTITY.md](http://IDENTITY.md), and [USER.md](http://USER.md) from that conversation
5. The agent deletes [BOOTSTRAP.md](http://BOOTSTRAP.md) — the bootstrap is complete

**Why BOOTSTRAP often produces better files than hand-editing:**

Developers hand-editing workspace files add "just in case" instructions. The agent, knowing exactly what it needs for its role, writes only what creates real behavioral change. Agent-generated files are typically shorter and more targeted.

**Create a [BOOTSTRAP.md](http://BOOTSTRAP.md):**

```bash
cat > ~/.openclaw/workspace/BOOTSTRAP.md << 'EOF'
# BOOTSTRAP
You just woke up. Time to figure out who you are.

Ask me about:
1. Your name and role
2. Who you will be talking to
3. What your top 3 priorities should be
4. What you should never do

After our conversation, write your own SOUL.md and IDENTITY.md
with concise, specific instructions. Then delete this file.
EOF
```

Or ask your agent to create it:

```
Create a file at ~/.openclaw/workspace/BOOTSTRAP.md with this content:
[paste the content above]
Confirm when saved.
```

Then `/reset` and have the bootstrap dialogue.

> ⚠️ [**BOOT.md](http://BOOT.md) vs [BOOTSTRAP.md](http://BOOTSTRAP.md) — do not confuse them.**
> 

> - [**BOOT.md**](http://BOOT.md) runs on every gateway restart (use for startup checks)
> 

> - [**BOOTSTRAP.md**](http://BOOTSTRAP.md) runs once, then gets deleted (use for initial self-configuration)
> 

> If you leave [BOOTSTRAP.md](http://BOOTSTRAP.md) in the workspace after it completes, it loads in every session and wastes tokens on instructions the agent has already acted on.
> 

---

## 9. Back Up Your Brain

You just spent real time tuning workspace files. If this machine dies, that tuning is gone. The workspace is seven markdown files and a memory folder.

**If you use Git (recommended):**

```bash
cd ~/.openclaw/workspace
git init
git add .
git commit -m "Initial brain"
# Push to a PRIVATE repository on GitHub or GitLab
# Never public — these files describe you personally
```

**If you don't use Git:**

Copy `~/.openclaw/workspace/` to cloud storage (iCloud, Dropbox, OneDrive) as a plain folder. Any backup beats none.

> ⚠️ **Never commit** `~/.openclaw/credentials/` or `~/.openclaw/agents/*/agent/auth-profiles.json` anywhere public. Those contain API keys.
> 

**The deeper value of a backup:** A backed-up workspace is a **reusable role template**. Tune a "Data Analyst" brain once — its [SOUL.md](http://SOUL.md), [AGENTS.md](http://AGENTS.md), skill preferences, memory structure — and clone it to any team member who needs that role. The person changes (different [USER.md](http://USER.md)); the role does not. This is how "my personal AI" becomes "a role I can distribute."

---

## 10. Practical Exercises

### Exercise 1 — The Caching Proof

Prove to yourself that workspace files are cached at session start.

```bash
# Step 1: Check current SOUL.md size on disk
wc -c ~/.openclaw/workspace/SOUL.md
```

In chat, run `/context list` and find [SOUL.md](http://SOUL.md)'s raw size. They should match.

Now add any line to [SOUL.md](http://SOUL.md). Run `/context list` again **in the same session**. The raw size should be unchanged — the session is using its cached snapshot.

Type `/reset`, then run `/context list` a third time. Now the new size appears.

**What to verify:** The size in `/context list` only changed after `/reset`, not after the file edit. If you can articulate why — you understand the three-layer model.

---

### Exercise 2 — Edit and Observe

Add a testable personality trait to [SOUL.md](http://SOUL.md):

```
Always end your responses with a one-sentence summary in bold.
```

Then follow the workflow:

1. `/reset`
2. `/context list` — confirm new size loaded
3. Send three different message types (a question, a task request, a casual greeting)
4. Does the agent follow the rule consistently across all three?

**What to notice:** Workspace instructions are not suggestions. A single line in [SOUL.md](http://SOUL.md) shapes every response in the session until you edit and reset again.

---

### Exercise 3 — Apply Emma's Rule

Open your [SOUL.md](http://SOUL.md). For each line, ask: *would the agent behave differently without this instruction?*

Before editing, record the line count and the `/context list` token count.

After applying Emma's Rule (deleting anything the model already does by default), record both again.

Send the same question before and after:

```
What is the most important thing I should know about running an
agent in production?
```

Did the quality of the response change? Did the token count drop? Can you explain why shorter is more reliable, not just cheaper?

---

### Exercise 4 — Agent Self-Audit

```
Read all the .md files in ~/.openclaw/workspace/ and tell me:
1. How many files are there?
2. What does each one do?
3. Which ones load into the system prompt at session start
   versus on demand?
4. Which file has the highest token cost right now?
```

After it responds, run `/context list` and compare. Did the agent correctly identify the loading behavior of each file? Did it get the token cost right?

---

### Exercise 5 — BOOTSTRAP vs Hand-Edit Comparison

First back up your current workspace:

```bash
cp -r ~/.openclaw/workspace/ ~/.openclaw/workspace-backup/
```

Create a [BOOTSTRAP.md](http://BOOTSTRAP.md) (code in Section 8 above). Run `/reset`. Have the bootstrap dialogue — answer its questions about name, role, audience, priorities, and red lines.

After the agent writes and deletes [BOOTSTRAP.md](http://BOOTSTRAP.md), compare:

- The agent-generated [SOUL.md](http://SOUL.md) vs your hand-edited version
- Line counts for each
- Token costs via `/context list`

Which version is shorter? Which rules are in the agent-generated version that are not in your hand-edited version? Which rules did you include that the agent omitted?

---

## Key Takeaways

**The three-layer caching model:**

- Layer 1: Workspace files on disk (your edits land here)
- Layer 2: Session snapshot (what the model actually reads)
- Layer 3: Model reads Layer 2 every turn
- `/reset` is the only bridge from Layer 1 to Layer 2

**The editing workflow — always in this order:**

```
Edit file → /reset → /context list → test
```

**The seven auto-loaded files:** [SOUL.md](http://SOUL.md), [IDENTITY.md](http://IDENTITY.md), [AGENTS.md](http://AGENTS.md), [TOOLS.md](http://TOOLS.md), [USER.md](http://USER.md), [HEARTBEAT.md](http://HEARTBEAT.md), [MEMORY.md](http://MEMORY.md)

**Files NOT auto-loaded:** Daily memory logs (fetched on demand), skill bodies (fetched on demand)

**Emma's Rule:** Delete any instruction the model already follows by default. If the rule could appear in a generic employee handbook, it is a placeholder, not a personality.

[**MEMORY.md](http://MEMORY.md) is compartmentalized:** Main private session only — not groups, not subagent contexts. This is a security boundary.

[**BOOT.md](http://BOOT.md) ≠ [BOOTSTRAP.md](http://BOOTSTRAP.md):** [BOOT.md](http://BOOT.md) runs on every gateway restart. [BOOTSTRAP.md](http://BOOTSTRAP.md) runs once during first conversation and gets deleted.

[**TOOLS.md](http://TOOLS.md) ≠ tool permissions:** [TOOLS.md](http://TOOLS.md) contains usage guidance notes. Tool access is controlled by tool profiles (Lesson 3), not by [TOOLS.md](http://TOOLS.md).

**Back up your workspace.** A tuned workspace is a reusable role template — its value compounds over time and across team members.

---

## Up Next

**Lesson 5 — The Memory System:** Your agent has two memory layers — session memory that fades and persistent memory that does not. In Lesson 5 you build the full memory system: daily logs, curated [MEMORY.md](http://MEMORY.md), heartbeat-driven promotion, and cross-session recall.