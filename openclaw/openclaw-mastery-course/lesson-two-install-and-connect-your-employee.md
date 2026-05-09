# 2️⃣ Lesson 2 — Install & Connect Your Employee

## Lesson Overview

This lesson is entirely hands-on. You install OpenClaw from scratch, survive the most common installation failure, connect a messaging channel, and send your first message. Theory from Lesson 1 becomes real here.

> **Prerequisites:** Node.js 22+, a terminal, a Google account, and one of: WhatsApp / Telegram / Discord.

---

## 2. Install OpenClaw

OpenClaw installs through a single command. The installer detects your OS, checks prerequisites, and sets up the OpenClaw package.

**macOS / Linux:**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell as Administrator):**

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**Windows users: WSL2 is strongly recommended.** It gives you a real Linux environment next to Windows, and every command in this course works identically inside it.

### Setting Up WSL2 (Windows only)

```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu
# Reboot when prompted, then set a UNIX username/password
```

Verify WSL2 is running:

```powershell
wsl -l -v
# Should show Ubuntu, STATE: Running, VERSION: 2
```

Then inside the Ubuntu terminal, run the Linux installer:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

If `openclaw` is not found after install:

```bash
echo 'export PATH="$HOME/.openclaw/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
openclaw --version
```

### npm Fallback

If the install script fails for any reason:

```bash
npm install -g openclaw@latest
openclaw  # starts the wizard
```

### What the Installer Creates

```
~/.openclaw/
├── openclaw.json          # Main config file
├── agents/
│   └── main/
│       └── agent/
│           └── auth-profiles.json   # Credential cache (important — see Section 6)
└── bin/
    └── openclaw            # CLI executable
```

Know this directory. Every gotcha in this lesson involves a file in it.

---

## 3. The Setup Wizard

**Do not close your terminal.** The installer transitions directly into the setup wizard. Closing the terminal mid-wizard leaves OpenClaw in a half-configured state — the most common cause of the crash loop you will read about in Section 6.

### Step 1: Security Acknowledgment

Read it. Do not click through.

The wizard warns you directly: OpenClaw is a beta hobby project, a bad prompt can trick it into unsafe actions, and it recommends a security baseline (pairing mode, [localhost](http://localhost) binding, sandboxing, least-privilege access).

This warning is architecturally important, not a formality. You are about to give an agent access to your messages, possibly your files and email. The habit of reading security warnings starts here.

### Step 2: Configure Your LLM Provider

**Google Gemini.** It's the easiest and safest option for now.

**Codex OAuth** is also an option but only if you have access to the Free Quota Usage from Codex on one of your useless email since there are chances of your account getting banned.

1. Visit [aistudio.google.com/app/api-keys](http://aistudio.google.com/app/api-keys)
2. Create a new API key
3. Paste it into the wizard

When prompted for a model, scroll down and select:

```
google/gemini-3.1-flash-lite-preview
```

This model has the highest free request quota. If you hit its daily limit mid-session, switch to `google/gemini-2.5-flash` (separate quota).

**Free tier quota reference:**

| Model | Requests/min | Requests/day |
| --- | --- | --- |
| `gemini-3.1-flash-lite-preview` | 15 | 500 |
| `gemini-2.5-flash` | 10 | 250 |
| `gemini-2.5-pro` | 5 | 50 |

To use Codex OAuth instead, select it in the wizard and follow the instructions to login with your email, You will be able to use GPT-5.4 and other GPT models.

```bash
openclaw configure --section model # Select OpenAI Codex and login
```

### Changing Your Model or API Key Later

```bash
# Check current model
openclaw config get agents.defaults.model

# Change model
openclaw config set agents.defaults.model.primary "google/gemini-2.5-flash"
openclaw gateway restart
```

**Rotating an API key:** Three options.

**Option 1 (recommended — re-run the model wizard section only):**

```bash
openclaw configure --section model
```

**Option 2 (edit config directly):**

```json
// ~/.openclaw/openclaw.json
{
  "models": {
    "providers": {
      "google": { "apiKey": "paste-new-key-here" }
    }
  }
}
```

Then: `openclaw gateway restart`

**Option 3 (env var — expert path):**

```bash
# In ~/.bashrc or ~/.zshrc
export GOOGLE_API_KEY="your-key-here"
```

```json
// ~/.openclaw/openclaw.json
{
  "models": {
    "providers": {
      "google": { "apiKey": "${GOOGLE_API_KEY}" }
    }
  }
}
```

> ⚠️ **Critical:** The auth cache at `~/.openclaw/agents/main/agent/auth-profiles.json` takes priority over environment variables. If a new key seems ignored after rotation, delete the cache file first. Full explanation in Section 6.
> 

---

## 4. Connect Your Channel

Choose one channel: WhatsApp, Telegram, or Discord. All exercises in this lesson work identically through any of them.

---

### Option A: WhatsApp

OpenClaw connects to WhatsApp using the same mechanism as WhatsApp Web: QR code pairing via the Baileys library (reverse-engineered WhatsApp Web protocol).

> ⚠️ **Important:** This is NOT an official Meta API and violates WhatsApp's Terms of Service. Meta can ban accounts running unofficial automation. Use a dedicated number for anything beyond personal learning.

**Decision: which account?**

| Option | Setup | Risk |
| --- | --- | --- |
| **Dedicated number (recommended)** | ~5 min, second SIM/eSIM/Google Voice + WhatsApp Business | Personal number stays safe |
| **Personal number** | Zero setup | Account ban risk; your number exposed via pairing codes |

**Setting up a dedicated number:**

1. Get a second phone number (spare SIM, eSIM, Google Voice, Twilio, or any prepaid number)
2. Install **WhatsApp Business** (free, on App Store / Play Store — runs alongside regular WhatsApp)
3. Register WhatsApp Business with your second number

**Scanning the QR code:**

The wizard shows a QR code in your terminal. On your phone:

1. Open **WhatsApp Business** (dedicated) or **regular WhatsApp** (personal)
2. Go to **Settings → Linked Devices → Link a Device**
3. Scan the QR code

Terminal prints: `Linked after restart; web session ready.`

**Wizard questions after pairing:**

| Question | Answer |
| --- | --- |
| Phone setup | "Separate phone" (dedicated) or "Personal Number" |
| DM policy | **Pairing** (safest default — see table below) |
| allowFrom | Leave unset |

**DM policy options:**

| Policy | How it works | When to use |
| --- | --- | --- |
| **Pairing** | Stranger gets a one-time code; you approve | Learning, personal use |
| **Allowlist** | Pre-approved numbers only | Small team with known users |
| **Open** | Anyone who knows the number can DM | Public bots (Lesson 14) |
| **Disabled** | All DMs blocked | Temporary lockdown |

In Pairing mode, your own number is auto-approved — your first self-test works immediately.

**Approving a new user later:**

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

Pairing codes expire after 1 hour. Max 3 pending requests per channel.

> I'm using a separate number, but it's also somehow being used and I don't wanted my agent to send pairing codes to people who try to contact me, so I choose **allowlist** and approved only my specific number through which I'm testing my agent, this way it doesn't sent any pairing code to anyone and only reply to my allowed number.

---

### Option B: Telegram

> Note: Telegram is blocked in some regions (including Pakistan). Use a VPN for Telegram or choose a different channel WhatsApp or Discord.
> 
1. Open Telegram → search **@BotFather** (verified blue checkmark)
2. Send `/newbot`
3. Enter a display name (e.g., `My AI Employee`)
4. Enter a username ending in `bot` (e.g., `myai_employee_bot`)
5. Copy the bot token BotFather provides
6. Paste the token into the wizard

> ⚠️ Your bot token grants full control over your Telegram bot. Treat it like a password. Never commit it to Git.
> 

---

### Option C: Discord

**Step 1: Create a Discord Server**

- Discord → click **+** in left sidebar → **Create My Own** → give it a name (e.g., `AI Office`)

**Step 2: Create a Channel**

- Click **+** next to Text Channels → name it (e.g., `ai-employee`)
- Or use the default `#general`

**Step 3: Enable Developer Mode**

- User Settings → Advanced → toggle **Developer Mode ON**

**Step 4: Create the Bot**

1. Go to [discord.com/developers/applications](http://discord.com/developers/applications)
2. Click **New Application** → name it
3. Left sidebar → **Bot** → **Reset Token** → copy the token
4. Scroll down to **Privileged Gateway Intents** → toggle ON all three:
    - Presence Intent
    - Server Members Intent
    - **Message Content Intent** ← most critical; bot cannot read messages without this
5. Click **Save Changes**

**Step 5: Invite the Bot**

1. Left sidebar → **OAuth2** → **URL Generator**
2. Scopes: check `bot`
3. Bot Permissions: check **Read Messages/View Channels**, **Send Messages**, **Read Message History**
4. Copy the generated URL → paste into a new browser tab → invite the bot to your server

**Step 6: Enter details in the wizard**

- Guild (server name), Channel name, Bot Token

> ⚠️ **Critical Discord gotcha:** By default, Discord bots only reply to **direct messages**, not channel messages. To test: click the bot's name in the member list → DM it. To enable channel replies, you need to change `groupPolicy` to `open` (covered in Section 5 below).
> 

---

### Finish the Wizard

| Wizard Step | What to Select | Reason |
| --- | --- | --- |
| Web search provider | DuckDuckGo (experimental) | Free, no API key |
| Configure skills now? | Yes → then Skip all prompts | Skills covered in Lesson 6 |
| Enable hooks? | Skip | Covered in Lesson 13 |
| Optional apps | Skip | Optional companion apps |
| How to hatch your bot? | **Hatch in TUI** | Opens terminal chat for first conversation |

The TUI opens and sends `Wake up, my friend!` to your agent. **This first conversation matters.** Tell it your name, what you work on, and how you want it to behave. This seeds its persistent memory (`MEMORY.md`).

Control UI also available anytime at:

```bash
openclaw dashboard
# Opens http://127.0.0.1:18789/ with auth token
```

---

## 5. Send Your First Message

Send this to your bot:

```
Hello. What can you help me with?
```

- **WhatsApp:** Send to the bound number from your own WhatsApp
- **Telegram:** Search for your bot username and DM it
- **Discord:** Click the bot's name in the member list → DM it (not the channel)

The agent responds. You are talking to a live agent with tool access and persistent memory.

**If no response in 30 seconds, run diagnostics in this order:**

```bash
# Step 1: Is the channel connected?
openclaw channels status --probe

# Step 2: Is the gateway healthy?
openclaw doctor

# Step 3: What is the gateway log saying?
openclaw logs --follow
# Log file: /tmp/openclaw/openclaw-YYYY-MM-DD.log (rotated daily)
```

The gateway log is the single source of truth. Every message received, every tool invoked, every error thrown appears here. The dashboard shows summaries. The log shows everything. Get into the habit of reading the log first.

---

## 6. The Three Gotchas (Read Before You Hit Them)

These are the three most common failures across OpenClaw installations. Understanding them before they happen is faster than debugging them cold.

---

### Gotcha 1: The Crash Loop

**Symptom:** The gateway crashes immediately on startup. The log repeats:

```
Gateway start blocked, gateway.mode not configured
Gateway start blocked, gateway.mode not configured
Gateway start blocked, gateway.mode not configured
```

**Why it happens:** The installer registered the background service (macOS LaunchAgent or Linux systemd) before the configuration it depends on was complete. The service tries to start, finds `gateway.mode` missing, crashes, and restarts. This is a known bug.

**The fix:**

```bash
openclaw config set gateway.mode local
openclaw gateway restart
openclaw channels status --probe
```

**If the gateway is crash-looping and won't stop:**

```bash
# macOS: remove the LaunchAgent manually
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Then set gateway.mode and start fresh
openclaw config set gateway.mode local
openclaw gateway start
```

**Verify the wizard completed correctly:**

```bash
openclaw config get gateway.mode
# Should return: local
```

---

### Gotcha 2: The Auth Cache Override

**Symptom:** You rotated your API key, set a new environment variable, but OpenClaw keeps failing with auth errors. The new key seems to be ignored.

**Why it happens:** OpenClaw caches credentials in:

```
~/.openclaw/agents/main/agent/auth-profiles.json
```

This cache takes priority over environment variables. If you set `GOOGLE_API_KEY` in your shell, OpenClaw ignores it and uses the cached (possibly expired) key. This is the opposite of what most developers expect.

**The fix:**

```bash
rm ~/.openclaw/agents/main/agent/auth-profiles.json
# Then reconfigure your provider
openclaw configure --section model
```

> `auth-profiles.json` is a cache, not your main config. Deleting it forces re-authentication. Your main config at `~/.openclaw/openclaw.json` is untouched.
> 

---

### Gotcha 3: Free-Tier Quota Exhaustion

**Symptom:** Agent stops responding; logs show quota errors.

**The fix:** Switch to the other model (separate quota):

```bash
openclaw configure --section model
# Select google/gemini-2.5-flash
openclaw gateway restart
```

> If you started with OpenRouter: its free tier allows very few requests before rate-limiting. Switch to Google Gemini.

---

## 7. Organizing with Groups

You have one agent. You will want separate conversation threads for separate concerns — code reviews, work tasks, research. Groups give you this without creating multiple agents.

Every group your employee joins gets its own **isolated session**: separate conversation history, separate context, no cross-contamination. Your personal DM session is completely separate from all groups.

**Suggested group structure:**

| Group Name | Purpose |
| --- | --- |
| AI Employee — Work | Daily tasks, scheduling, email |
| AI Employee — Code | Code reviews, technical questions |
| AI Employee — Research | Research, reading, questions |

### Enabling Group Messaging

The wizard does not configure group messaging. The fastest path is to ask your employee in a DM:

```
Set my [WhatsApp / Telegram / Discord] group policy to "open" in
the config and restart the gateway. Do not use allowlist mode.
Confirm when done and tell me the current group policy setting.
```

Your employee edits `~/.openclaw/openclaw.json`, sets `groupPolicy` to `"open"`, and restarts the gateway.

**Manual fallback (CLI):**

```bash
# WhatsApp
openclaw config set channels.whatsapp.groupPolicy "open"

# Telegram
openclaw config set channels.telegram.groupPolicy "open"

# Discord
openclaw config set channels.discord.groupPolicy "open"

openclaw gateway stop && openclaw gateway start
openclaw doctor
```

> ⚠️ **Watch for allowlist drift:** Your employee may try to "improve" the setup by switching to `allowlist` mode with explicit group IDs. This breaks group messaging silently — messages stop arriving but the employee reports success. If groups stop working: ask your employee its current `groupPolicy`, and if it's not `"open"`, change it back.
> 

**After enabling groups:** Create a group (you can be the only member besides the bot), then **@mention the bot**. Even with `groupPolicy open`, the bot requires a mention to respond in groups — it will not reply to every message in a busy thread.

**What groups are NOT:** Multi-agent. You have one employee with one identity. Groups give you separate conversation threads with the same worker. `SOUL.md`, `USER.md`, and `IDENTITY.md` load in every session. `MEMORY.md` (long-term curated memory) loads only in your main private session.

---

## 9. The Three Diagnostic Commands

These three commands solve 90% of OpenClaw problems. Run them in this order whenever something breaks:

```bash
# 1. First-response diagnostic
openclaw doctor
# Checks: Node.js version, network connectivity, config paths, service status

# 2. Channel status check
openclaw channels status --probe
# Checks: is each configured channel connected and responding?

# 3. Live log stream (the real source of truth)
openclaw logs --follow
# Every message, every tool call, every error
```

Fix anything `openclaw doctor` flags before digging into logs. If doctor is clean and channels are connected but the agent is still silent, the log will show you exactly why.

---

## 10. Practical Exercises

### Exercise 1: Real Task

Send this to your agent:

```
Write a short summary of what OpenClaw is and why someone
would use it. Keep it under 100 words.
```

Your agent generates text and delivers it through your messaging channel. This is the baseline. Lesson 3 tests what else it can do.

---

### Exercise 2: Memory Test

Send two messages a few minutes apart.

**First:**

```
My name is [your name]. I work on [your project]. Remember this.
```

**A few minutes later:**

```
What is my name and what do I work on?
```

The agent remembers within a session. This is not a stateless chat window. In Lesson 4, you will learn about `MEMORY.md` — persistent memory that survives across sessions and channels. For now, observe: context persists.

---

### Exercise 3: Break It and Read the Log

Set a deliberately invalid model name:

```bash
openclaw config set agents.defaults.model.primary "google/fake-model-that-does-not-exist"
openclaw gateway restart
```

Send a message to your agent. It will fail. Now run:

```bash
openclaw logs --follow
```

Find the error. Understand what the log tells you. Fix it:

```bash
openclaw config set agents.defaults.model.primary "google/gemini-3.1-flash-lite-preview"
openclaw gateway restart
```

**What you are learning:** Log-first debugging. The log always tells you exactly what broke and why. This habit is used in every lesson from here forward.

---

## Key Takeaways

- Install with one command → complete the wizard without closing the terminal → verify with `openclaw channels status --probe`
- **Crash loop fix:** `openclaw config set gateway.mode local` → `openclaw gateway restart`
- **Auth cache fix:** `rm ~/.openclaw/agents/main/agent/auth-profiles.json` → reconfigure provider
- **Free tier:** Use `gemini-3.1-flash-lite-preview` first; fall back to `gemini-2.5-flash` when quota runs out
- **The log** (`openclaw logs --follow`) is the single source of truth for debugging — not the dashboard, not the chat interface
- **Groups** give one agent multiple isolated conversation threads — not multiple agents
- Pairing mode is the correct DM policy for learning; change it in Lesson 14

---

## Up Next

**Lesson 3 — Task Delegation and Tool Profiles:** Send your agent something a chatbot would refuse. Knowing things and doing things are different privileges. You will draw that line in the next lesson.