# 8️⃣ Lesson 8 — Make It Proactive (Heartbeats & Cron Jobs)

## Lesson Overview

Every lesson before this one built a better chatbot. This lesson changes the category. You will give your agent a schedule — heartbeats that batch multiple checks into a single wake-up, and cron jobs that fire at exact times. When this lesson is done, your agent will message you without being asked.

> **Before you start:** Terminal open, dashboard open, messaging channel ready. You will need HEARTBEAT.md, two config commands, and one cron job.
> 

## 1. Two Mechanisms, One Concept

Two mechanisms enable proactive behavior. They solve different problems.

**Heartbeat** — A built-in gateway timer that wakes the agent periodically (default: every 30 minutes). When it fires, the gateway loads `HEARTBEAT.md` into the agent's context. The agent reads its checklist, decides whether anything needs attention, and either acts or replies with a single token: `HEARTBEAT_OK`. When the gateway sees that token, it drops the message silently. One wake-up, many checks, silence when nothing matters.

**Cron job** — A task that fires at an exact time you specify. Not "sometime in the next 30 minutes" — exactly 9:00 AM, exactly Monday at 8:00 AM. Use it when delivery must happen at a specific moment.

**The distinction that matters:**

|  | Heartbeat | Cron Job |
| --- | --- | --- |
| Timing | Approximate (30-min intervals) | Exact (cron expression) |
| Batching | Yes — multiple checks, one wake-up | No — one job, one run |
| Best for | Periodic awareness ("check if anything needs attention") | Precise delivery ("send this at 9 AM sharp") |
| Token cost per day | 48 turns (one heartbeat every 30 min) | One turn per fire per job |

---

## 2. The Cost Math

This is not abstract. It directly affects your API bill.

**Five separate cron jobs at 30-minute intervals:**

```
5 jobs × 2 fires/hour × 24 hours = 240 agent turns per day
Each turn = a full isolated API call
```

**One heartbeat with five checklist items:**

```
1 heartbeat × 2 fires/hour × 24 hours = 48 agent turns per day
Each turn checks all 5 items in a single API call
```

Same work. **80% fewer API calls.** The heartbeat batches everything into one wake-up cycle.

**The decision rule:**

- Does this need to happen at an exact time? → Cron job
- Can it be batched with other periodic checks? → Heartbeat checklist item

Most of what you want to automate is the second category.

---

## 3. Heartbeats: Building Your Agent's Pulse

### Step 1: Populate HEARTBEAT.md

Your workspace already has `~/.openclaw/workspace/HEARTBEAT.md`. By default it is empty (just comments), which means heartbeat runs are skipped entirely — no API call, no tokens spent. The moment you add real checklist items, heartbeats activate.

Send this to your agent on WhatsApp:

```
Update my HEARTBEAT.md with these checks:
- Check for unread messages that need a response
- Check for calendar events in the next 2 hours
- Check for anything that changed since the last check
Always send me a brief status report after checking, even if nothing needs attention.
```

After the agent updates the file, verify what was actually written:

```
Show me the exact contents of my HEARTBEAT.md
```

**Why verify?** Agents sometimes rewrite or simplify your instructions. If a checklist item is missing, ask the agent to add it back. The file is what runs — not the intent.

> **Note:** The last line says "always send a status report." This means every heartbeat will produce a message. That is intentional during testing — you need to see heartbeats working before you add suppression. After you confirm they work, Section 4 fixes the noise.
> 

### Step 2: Route Heartbeats to Your Channel

The moment you added checklist items, heartbeats started running. But their output goes nowhere by default — `target: none` means the gateway runs the check, gets a response, and drops it silently.

First, send any message to your agent on WhatsApp so it is the "last active" channel. Then in your terminal:

```bash
openclaw config set agents.defaults.heartbeat.every 1m
openclaw config set agents.defaults.heartbeat.target last
openclaw gateway restart
```

**What each setting does:**

- `every 1m` — speeds up from the default 30 minutes to 1 minute so you see results immediately. You will switch back to `30m` for production.
- `target last` — routes heartbeat alerts to the most recently active conversation. Since you just messaged on WhatsApp, that is WhatsApp.
- `gateway restart` — required. Without this, nothing changes.

**Alternative: Route to a specific number**

If you need heartbeats routed to a specific number regardless of which chat was last active:

```bash
openclaw config set agents.defaults.heartbeat.target whatsapp
openclaw config set agents.defaults.heartbeat.to '"+923001234567"'
```

> ⚠️ Note the quoting: single quotes around double quotes. Phone numbers start with `+`, which the config parser interprets as a positive number unless forced to be a string. The `to` number must be the number you chat **from** (your phone), not the number your agent's WhatsApp is registered on.
> 

### The Separation of Concerns

The agent controls **what** to check (`HEARTBEAT.md` content). You control **how often** and **where** (gateway config). This split is deliberate and applies throughout OpenClaw: agents own their content, operators own the infrastructure.

### Step 3: Verify It Is Running

Open your WhatsApp and wait. With a 1-minute interval, a message should arrive within a minute or two. Read it — it should be a brief status based on your checklist items.

**If no message arrives after 2 minutes, debug in this order:**

```bash
# Step 1: Is the channel connected?
openclaw channels status --probe
# Look for: WhatsApp default: enabled, configured, linked, running, connected

# Step 2: Stream the gateway log
openclaw logs --follow
# Look for [heartbeat] entries
# Most common failure: "channel not ready" (WhatsApp reconnecting)

# Step 3: Check the dashboard
# If dashboard shows heartbeat activity but nothing arrived on WhatsApp,
# the heartbeat ran but delivery failed. Check target config.
```

---

## 4. HEARTBEAT_OK Suppression

At 1-minute intervals, your phone is buzzing constantly. At 30 minutes, that is 48 messages per day saying "nothing to report." This is the noise problem. `HEARTBEAT_OK` is the solution.

Update your HEARTBEAT.md:

```
Update my HEARTBEAT.md. Keep the existing checks, but change the
last line to:
If nothing needs attention, reply with exactly this token and
nothing else: HEARTBEAT_OK
```

Verify the update:

```
Show me my HEARTBEAT.md
```

**Make sure the file contains the exact text `HEARTBEAT_OK`.** Agents sometimes paraphrase. If the agent wrote "reply that everything is okay" instead of the literal token, ask it to fix it. The gateway matches the exact string, not the intent.

### How Suppression Works

The gateway scans every heartbeat response for the `HEARTBEAT_OK` token at the start or end. When found:

1. Strips the token out
2. Checks remaining content length (configurable via `ackMaxChars`, default 300 characters)
3. If content is under the limit: drops the entire message silently
4. If content is over the limit: delivers the message anyway (something important is being reported)

When the agent finds something that needs attention, it replies with the alert text and **omits** `HEARTBEAT_OK` entirely. The gateway sees no acknowledgment token, treats it as an alert, and delivers it.

**Silent heartbeats are not wasted computation.** They are proof the agent is alive, watching, and has nothing to report.

### Switch to Production Interval

Once suppression is confirmed working:

```bash
openclaw config set agents.defaults.heartbeat.every 30m
openclaw gateway restart
```

> **The default state is free.** An empty `HEARTBEAT.md` (just comments) means heartbeat runs are skipped entirely — no API call, no tokens. To deactivate heartbeats without changing gateway config, clear the checklist back to comments only.
> 

---

## 5. Cron Jobs: Precise Scheduling

Heartbeats check "is anything wrong." Cron jobs deliver "this specific thing at this specific moment."

### Step 1: Learn the Tool First

Before using the cron tool, ask your agent what it does:

```
What is the cron schedule tasks tool for?
```

The agent explains that it schedules tasks to run at specific times or intervals, independent of your current chat. Now that you know the tool exists, use it:

```
Use the cron schedule tasks tool to send me a daily summary
every morning at 9 AM.
```

**Why name the tool explicitly?** Without "Use the cron schedule tasks tool," the agent may reach for Unix `crontab` or other system tools. In testing, a generic "create a cron job" prompt caused the agent to create a Unix crontab entry with a bash script that echoed text to stdout and never reached WhatsApp. Naming the tool explicitly fixed it every time.

### Three Cron Schedule Types

| Type | Prompt Example | Behavior |
| --- | --- | --- |
| **Recurring** | "Send a summary every day at 9 AM" | Fires on a schedule (daily, weekly, etc.) |
| **Fixed interval** | "Check for updates every 30 minutes" | Fires at a fixed repeat interval |
| **One-shot** | "Remind me in 20 minutes" | Fires once, then auto-deletes |

### Verify the Job Was Created

```
List my cron jobs
```

Or check the dashboard's **Cron Jobs** page for a visual view of all active jobs, schedules, and run history. If the job does not appear, the agent used the wrong tool — clean up and try again with the explicit tool name.

**Terminal management:**

```bash
openclaw cron list
openclaw cron edit <id>
openclaw cron remove <id>
openclaw cron --help   # full command set
```

---

## 6. Quiet Hours: Defense in Depth

An agent that messages customers at 3 AM is a compliance violation and a lost customer. Quiet hours must be enforced at two independent levels.

### Level 1: Prompt-Level (HEARTBEAT.md)

Add timing constraints to the heartbeat checklist:

```
## Quiet Hours
- Do NOT send customer messages before 8am or after 9pm
- If there are pending actions outside active hours, note them and wait
```

The agent should follow this. But "should" is not "will." Prompt-level enforcement depends on the model obeying the instruction. Models can be tricked, misled, or simply ignore instructions in certain contexts.

### Level 2: Infrastructure-Level (Active Hours Config)

```bash
openclaw config set agents.defaults.heartbeat.activeHours.start "08:00"
openclaw config set agents.defaults.heartbeat.activeHours.end "21:00"
openclaw config set agents.defaults.heartbeat.activeHours.timezone "Pakistan/Karachi"
```

Outside this window, the gateway does not run heartbeats at all. No model call. No token cost. No risk of a message being sent. The heartbeat is skipped at the infrastructure level.

### Defense in Depth

Use both. The `activeHours` config prevents heartbeats outside business hours regardless of what the model would do. The `HEARTBEAT.md` instructions add a second layer for edge cases. If either layer fails, the other catches it.

This pattern repeats in Lesson 13 (security tiers): multiple layers, each independently sufficient, so a single failure does not cascade.

## 7. Advanced: What Is Under the Surface

You have what you need to run heartbeats and crons in production. These capabilities exist when you are ready for them:

**`lightContext` + `isolatedSession`** — Two flags that cut heartbeat token costs by 95%+. Each heartbeat currently loads the full workspace (350+ lines). Light context mode loads only HEARTBEAT.md. Isolated sessions prevent context bleed between heartbeat runs.

**System events** — External webhooks can wake your agent immediately instead of waiting for the next heartbeat tick. When an urgent event fires (a payment fails, a server goes down), the agent responds in seconds instead of up to 30 minutes.

**Per-agent heartbeat config** — Each agent can have its own heartbeat schedule, independent of `agents.defaults`. Matters the moment you add a second agent in Lesson 10.

**Cron webhook output** — Cron jobs can POST results to a webhook instead of a chat channel. Useful for integrating with external systems.

Explore the automation docs when your heartbeats are running smoothly.

---

## 9. Practical Exercises

### Exercise 1 — Build Your Real Heartbeat Checklist

The examples above use generic checks. Now make one tailored to your actual work.

Ask your agent:

```
Based on what you know about me, what should my heartbeat
checklist include? Suggest 3-5 items that would actually
help me if you checked them every 30 minutes.
```

Review the suggestions. Edit them. Then:

```
Update my HEARTBEAT.md with these checks: [paste your final list].
If nothing needs attention, reply with exactly: HEARTBEAT_OK
```

Verify the file. Set the interval to `1m`. Wait for a heartbeat. Is the report more relevant than a generic one?

Then set back to `30m` for production.

**What you are learning:** A heartbeat is only as useful as its checklist. Generic checks produce generic noise. A checklist tailored to your actual work produces actionable alerts.

---

### Exercise 2 — Schedule a Real Daily Briefing

```
Use the cron schedule tasks tool to send me a morning briefing
every weekday at 9 AM. Include a summary of anything I should
focus on today.
```

Verify in the dashboard Cron Jobs page. If the job does not appear, the agent used the wrong tool. Try again with the explicit tool name.

Then schedule a one-shot reminder:

```
Use the cron schedule tasks tool to remind me in 20 minutes
to [something you actually need to do today].
```

**What you are learning:** The difference between recurring crons (daily briefing) and one-shot crons (reminders). Both require naming the tool explicitly. The dashboard confirms what was actually created.

---

### Exercise 3 — The Cost Math Applied to Your Tasks

Send this to your agent on WhatsApp:

```
I want to automate these five things. For each one, tell me
whether it should be a heartbeat checklist item or a cron job,
and why:
1. Check for new customer messages
2. Send a daily summary at 9 AM
3. Follow up on unanswered items
4. Remind me about meetings 15 minutes before they start
5. Monitor if any deadlines are approaching
```

Compare the agent's classification to your own. Then calculate:

- How many turns per day if each item were its own cron job at 30-min intervals?
- How many turns per day as a heartbeat checklist with one 9 AM cron?

**What you are learning:** The cost math is the decision framework. Periodic awareness goes in the heartbeat. Precise timing gets its own cron. The 80% reduction is not a best practice — it is the consequence of understanding which mechanism fits which problem.

---

### Exercise 4 — Quiet Hours Enforcement Test

Set active hours to a narrow window that excludes right now:

```bash
# Set active hours to 2-3 AM (should be outside normal use)
openclaw config set agents.defaults.heartbeat.activeHours.start "02:00"
openclaw config set agents.defaults.heartbeat.activeHours.end "03:00"
openclaw config set agents.defaults.heartbeat.activeHours.timezone "Pakistan/Karachi"
openclaw gateway restart
```

Wait 2 minutes. No heartbeat message should arrive. Check the gateway log:

```bash
openclaw logs --follow
# Look for [heartbeat] entries showing "outside active hours" or similar
```

Then restore production hours:

```bash
openclaw config set agents.defaults.heartbeat.activeHours.start "08:00"
openclaw config set agents.defaults.heartbeat.activeHours.end "21:00"
openclaw gateway restart
```

**What you are learning:** Infrastructure-level enforcement is the only reliable quiet hours guarantee. The gateway skips the heartbeat entirely — no model call, no possibility of a message. Prompt-level instructions alone are not sufficient for compliance.

---

### Exercise 5 — HEARTBEAT_OK Precision Test

This tests whether suppression is working correctly.

1. Set interval to `1m`
2. Wait for a heartbeat that produces `HEARTBEAT_OK` (nothing to report)
3. Count how many messages arrived on your phone in 5 minutes
4. Now add a checklist item that will definitely trigger: "Alert me that testing is in progress"
5. Wait for the next heartbeat
6. Verify: one alert message arrived, and the suppressed ones did not

Then remove the test item and restore `30m` interval.

**What you are learning:** `HEARTBEAT_OK` suppression is binary: either the agent reports something (message delivered) or it does not (silence). Verifying both states confirms the mechanism is working correctly, not just that you have not seen a failure yet.

## Key Takeaways

**Heartbeat vs Cron:**

- Heartbeats: periodic awareness, batched checks, approximate timing, 48 turns/day
- Cron jobs: precise delivery, dedicated runs, exact timing, 1 turn/fire
- Cost math: 5 items as crons = 240 turns/day; 5 items as heartbeat = 48 turns/day

## Up Next

**Lesson 9 — Voice Output:** Your agent sends text. Half your users consume audio while doing other things. In Lesson 9, two config lines and a plugin enable turn your agent's messages into voice notes delivered over WhatsApp.