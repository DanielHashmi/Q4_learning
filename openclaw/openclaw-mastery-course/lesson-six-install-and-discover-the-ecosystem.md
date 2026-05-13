# 6️⃣ Lesson 6 — Install Skills & Discover the Ecosystem

## Lesson Overview

Your agent has a personality, persistent memory, and slash commands. Now you extend its *capabilities*. This lesson introduces the three extension types inside the gateway, when to use each one, and the escalation path that prevents you from building a TypeScript plugin when a markdown file would have worked.

> **Before you start:** Have a terminal open at `~/.openclaw/workspace/` and your messaging channel ready. Every concept here ends with a working installation you can test.
> 

---

## 1. The Map: Three Ways to Extend Your Agent

Before installing anything, understand the categories. All three extension types run inside the gateway you started in Lesson 2.

| Extension | What It Is | Code Required? | Purpose |
| --- | --- | --- | --- |
| **Skill** | A folder with a `SKILL.md` file | No | Knowledge: teaches the agent *how* to handle a task |
| **Bundle Plugin** | A `.claude-plugin/` directory of files | No | Capability: packages domain workflows, no code |
| **Native Plugin** | TypeScript running in-process in the gateway | Yes (TypeScript) | Infrastructure: channels, model providers, voice |

There is a fourth extension type — **MCP servers** — which connect the agent to external services via the Model Context Protocol. That is Lesson 7. This lesson covers what runs inside the gateway.

---

## 2. The Bundled Ecosystem You Already Have

Before searching for anything new, look at what shipped with your install:

```bash
openclaw plugins list --verbose
```

The output shows every plugin with these fields:

| Field | What It Tells You |
| --- | --- |
| `loaded` / `disabled` | Whether the plugin is active right now |
| `format` | `openclaw` = native plugin; `bundle` = file-based |
| `origin` | `bundled` = shipped with your install |
| `providers` | For model plugins, which providers it registers |
| `error` | Why it is disabled (usually missing credentials) |

Scroll through the output. You will see three categories:

| Category | Loaded by Default | Disabled by Default |
| --- | --- | --- |
| **Model providers** | Google, Anthropic, OpenAI, DeepSeek, Mistral, Ollama, NVIDIA | Groq |
| **Channels** | WhatsApp (the one you set up) | Discord, Telegram, Slack, Signal, Matrix, IRC, Line, MS Teams |
| **Utilities** | Browser, DuckDuckGo, Memory Core, Talk Voice | ElevenLabs, Brave, Firecrawl, OpenShell Sandbox |

**The insight:** Most model providers are loaded automatically when the gateway detects a valid API key. Most channels are disabled because each needs its own credentials. The infrastructure was always there — you just had not looked.

### Enabling a Disabled Plugin

```
1. Plugin exists      (bundled, in your install)
2. Disabled by default (nothing auto-activates without credentials)
3. Enable             (openclaw config set plugins.entries.<id>.enabled true)
4. Configure          (set plugin-specific settings)
5. Restart            (openclaw gateway restart)
```

Try enabling the Brave search plugin:

```bash
openclaw config set plugins.entries.brave.enabled true
openclaw gateway restart
openclaw plugins list --verbose | grep brave
```

If it shows as loaded, ask your agent:

```
Search the web using Brave for the latest OpenClaw release notes.
```

If it shows an error (missing API key), that is expected — some plugins need credentials before they work. The pattern is what matters: find the plugin ID in the list, enable it, restart, verify.

---

## 3. Skills: Knowledge via SKILL.md

A skill is a folder containing a `SKILL.md` file that teaches your agent how to handle a specific task. The format follows the [Agent Skills specification](https://agentskills.io/specification) — a **cross-platform standard** that works in OpenClaw, Claude Code, and other agent platforms.

### Skill Folder Structure

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code (Python, Bash, JS)
└── references/       # Optional: documentation loaded on demand
```

### The SKILL.md Format

YAML frontmatter followed by markdown instructions:

```yaml
---
name: campaign-plan
description: "Generate a 10-section campaign brief using the OAMCM framework
  when the user asks for a marketing plan, campaign strategy, or go-to-market brief."
---
```

The `name` field is used for invocation matching. The `description` is matched against user requests so the agent knows *when* this skill applies. The markdown body below the frontmatter contains conversational patterns, decision frameworks, domain workflows, and tool usage instructions.

### Progressive Disclosure: Why You Can Install Many Skills

At gateway startup, only the `name` and `description` of every installed skill load into the agent's context. The full body of `SKILL.md`, plus any `scripts/` and `references/`, only loads when the agent decides the skill is relevant.

```
Session start:  name + description for every skill  (tiny, cheap)
        ↓
Agent sees relevant request
        ↓
Full SKILL.md body loads  (only for that skill)
        ↓
scripts/ and references/ loaded on demand within the skill
```

You can install a hundred skills without burning context. Only the ones actually needed get fully read.

---

## 4. ClawHub: The Skill Marketplace

[ClawHub](https://clawhub.ai) is the public registry for Agent Skills bundles. Think of it as npm for agent capabilities — search it by semantic meaning, not just keywords.

### Install a Skill

```bash
# Search for skills in your domain
openclaw skills search booking

# Install one
openclaw skills install service-booking

# Update all installed skills
openclaw skills update --all
```

The skill downloads into `~/.openclaw/workspace/skills/` (created automatically on first install).

> ⚠️ **Restart required.** Skills are snapshotted when a session starts. After installing, restart the gateway:
> 

```bash
openclaw gateway restart

openclaw skills list  # verify it appears
```

### Use the Installed Skill

```
Use the service-booking skill to help me find a plumber near me.
The skill is installed in my workspace skills directory at
~/.openclaw/workspace/skills/service-booking/.
```

Check the dashboard. The agent loads the skill's instructions and follows its workflow: asking what service you need, your location, your preferred time. If the skill connects to an MCP server, the agent calls real tools to search for available providers.

**Why include the path in your prompt?** 

> Your agent searches for files the way any assistant does — it may check system directories first and miss your workspace. A better long-term fix is adding to `AGENTS.md`
> 

```bash
Skills are installed in ~/.openclaw/workspace/skills/
```

Now every session knows where to look without you repeating it.

### Security: Dangerous Code Detection

If a skill contains code patterns flagged as dangerous, installation fails with a security warning. As of v2026.3.31, critical findings fail closed by default — the install is blocked, not just warned. If you trust the author and have reviewed the code:

```bash
openclaw skills install <skill-name> --dangerously-force-unsafe-install
```

Do not use this flag without reviewing the skill's source.

### Model Quality and Skills

Skill invocation depends on your model's capability. The free-tier model (`gemini-3.1-flash-lite-preview`) may not reliably follow skill instructions. If your agent ignores an installed skill:

1. Check dashboard → Skills tab → confirm it shows as "Ready"
2. If Ready, the issue is model quality, not configuration
3. Switch to a more capable model (`gemini-2.5-flash` or higher)

---

## 5. Two Plugin Formats

Look at the `format` column in `openclaw plugins list --verbose`. Every bundled plugin shows `openclaw` (native). But OpenClaw supports a second format: **bundle**.

|  | Native (`openclaw`) | Bundle (`.claude-plugin/`) |
| --- | --- | --- |
| **Contains** | TypeScript + `openclaw.plugin.json` | Markdown skills + JSON commands + MCP connectors |
| **Code required?** | Yes | No |
| **Runs where** | Inside the gateway process | Loaded as file-based extensions |
| **Used for** | Channels, model providers, voice, gateway hooks | Domain workflows, knowledge packages |
| **Example** | WhatsApp adapter, Brave search | Marketing plugin, finance plugin |

The `.claude-plugin/` directory format is the **same one Claude Code and Cowork use**. Any Claude plugin works in OpenClaw as a bundle. This opens a large ecosystem beyond what ships bundled.

---

## 6. Install a Bundle Plugin

Two open-source plugin collections work with OpenClaw out of the box:

- [**Anthropic's knowledge-work plugins](https://github.com/anthropics/knowledge-work-plugins):** productivity, sales, customer support, product management, marketing, legal, finance, data analysis
- [**Panaversity's business plugins](https://github.com/panaversity/agentfactory-business-plugins):** Islamic finance, banking, legal operations, financial modeling

### Install the Marketing Plugin

```bash
# Clone the repo (or download ZIP and extract)
git clone https://github.com/anthropics/knowledge-work-plugins

# Install the marketing plugin
openclaw plugins install ./knowledge-work-plugins/marketing

# Restart and verify
openclaw gateway restart
openclaw plugins list
```

Look for `marketing` in the output with `Format: bundle`. Bundle plugins may start disabled:

```bash
openclaw plugins enable marketing
```

### Verify the Plugin Loaded

```
List all skills from the marketing extension at
~/.openclaw/extensions/marketing/skills/.
```

You should see eight skills: `campaign-plan`, `content-creation`, `brand-review`, `competitive-brief`, `draft-content`, `email-sequence`, `performance-report`, and `seo-audit`. Also visible in the dashboard under your agent's **Skills** tab as "Extra Skills."

### Use the Campaign Planning Skill

The `campaign-plan` skill follows the OAMCM framework (Objective, Audience, Message, Channel, Measure) and produces a 10-section brief:

```
Generate a full campaign brief with objectives, audience, messaging,
channel strategy, content calendar, and success metrics for
https://agentfactory.panaversity.org/
The goal is brand awareness in the US.
```

If the plugin is working, the output follows the OAMCM structure: campaign overview, target audience, key messages, channel strategy, week-by-week content calendar, success metrics. If the output is generic with no structured sections, the plugin did not load correctly — check `openclaw plugins list`.

### Published Plugins (Even Simpler)

Plugins on ClawHub or npm do not require cloning:

```bash
openclaw plugins install @openclaw/voice-call
```

The command checks ClawHub first and falls back to npm automatically. The GitHub repos require a local clone because they are not yet published on npm or ClawHub.

---

## 7. The Decision Tree

When your agent needs something new, work through this hierarchy:

| Your agent needs to... | Use this | What it is | Code? |
| --- | --- | --- | --- |
| **Know** something new | Skill | SKILL.md (Agent Skills spec) | No |
| **Access** an external service or API | MCP server | Tool connection via protocol | JSON config (Lesson 7) |
| **Gain** a domain workflow capability | Bundle plugin | `.claude-plugin/` directory | No |
| **Extend the gateway itself** | Native plugin | TypeScript, in-process | Yes |

**The default:** Start with a skill. Most agent capability needs are skills. If a skill is not enough because the agent needs real tool access (not just instructions), escalate to MCP. If MCP is not enough, try a bundle plugin before writing TypeScript. Native plugins are for platform developers extending the gateway infrastructure.

### Bundled-First Discovery

Before searching ClawHub, always check what you already have:

```bash
openclaw plugins list --verbose
```

Dozens of plugins ship with OpenClaw. Most are disabled by default — they need credentials, not installation. Enabling a bundled plugin is faster and more reliable than installing a new one.

---

## 8. Practical Exercises

### Exercise 1 — Audit Your Bundled Ecosystem

```bash
openclaw plugins list --verbose
```

For each plugin in the output, classify it:

- Is it loaded or disabled?
- Is it a native or bundle format?
- If disabled, what does it need to become active? (credentials, API key, manual enable?)

Then pick one disabled utility plugin (not a channel or model provider) and enable it:

```bash
openclaw config set plugins.entries.<id>.enabled true
openclaw gateway restart
openclaw plugins list --verbose | grep <id>
```

**What you are learning:** The bundled ecosystem is large and mostly dormant. Most "missing capabilities" are already installed, just disabled. Check before searching ClawHub.

---

### Exercise 2 — Search, Install, and Test a Skill

```bash
# Search for something relevant to your work
openclaw skills search <your-domain>

# Install one
openclaw skills install <skill-name>

# Restart
openclaw gateway restart
openclaw skills list
```

Then ask your agent to use it:

```
I just installed the [skill-name] skill in my workspace skills
directory at ~/.openclaw/workspace/skills/. What can you help
me with now that you couldn't before?
```

After testing, read the skill's SKILL.md directly:

```
Read the SKILL.md file in ~/.openclaw/workspace/skills/[skill-name]/.
Explain what the name and description fields do, and what the
instructions tell you to do differently.
```

**What you are learning:** The full marketplace workflow and how the Agent Skills spec works in practice. The agent can read and explain its own skills, just as it read its own workspace files in Lesson 4.

---

### Exercise 3 — Classify Five Capability Needs

Think of five things you want your agent to do that it cannot do right now. For each one, classify it:

1. Does the agent need to *know* something? → Skill
2. Does the agent need to *access* an external API or service with live data? → MCP server
3. Does the agent need a new no-code gateway capability? → Bundle plugin
4. Does the agent need to extend the gateway's runtime behavior? → Native plugin

For each one, write down:

- What the capability is
- Which extension type it requires
- Why it is not a lower-level extension (i.e., why a skill would not be enough if you chose MCP)

**What you are learning:** The escalation hierarchy as a decision framework. Classifying correctly before building saves you from writing a TypeScript plugin when a markdown file would have worked.

---

### Exercise 4 — Install and Use the Marketing Bundle Plugin

Follow Section 6 to install the marketing plugin from Anthropic's knowledge-work repo.

After installing and enabling:

1. Verify the eight skills appear in the dashboard's Skills tab
2. Run the campaign brief prompt from Section 6 on a real project you are working on
3. Compare the output structure to what you would get without the plugin (ask your agent for a marketing plan *without* mentioning the skill)

Is there a structural difference in the output? Can you identify which OAMCM sections appear when the skill is active?

**What you are learning:** Bundle plugins package domain expertise without code. The difference between a generic model response and a skill-guided response is the structured framework — the OAMCM sections that the skill enforces.

---

### Exercise 5 — Skill vs Plugin vs MCP: The Edge Cases

Ask any AI assistant (Claude, ChatGPT) to help you reason through these three scenarios. For each one, decide the correct extension type and explain why:

1. You want your agent to know how to write ISO 27001 compliance reports in a specific format your company uses
2. You want your agent to check your company's live inventory database before answering stock questions
3. You want your agent to receive and process incoming emails as a new message channel

**What you are learning:** The boundary cases between the extension types. Scenario 1 is a skill (knowledge, format). Scenario 2 is MCP (live data access). Scenario 3 is a native plugin (new channel = new gateway capability). If you reasoned your way to those answers, you understand the hierarchy.

---

## Key Takeaways

**Three extension types inside the gateway:**

- **Skill** — SKILL.md, Agent Skills spec, cross-platform (works in OpenClaw + Claude Code), no code, knowledge only, install from ClawHub
- **Bundle plugin** — `.claude-plugin/` directory, no code, domain workflows + skills + MCP connectors, Claude-compatible
- **Native plugin** — TypeScript, in-process, infrastructure (channels, model providers, voice), already running as your bundled plugins

**The escalation path:**

```
Skill → MCP server → Bundle plugin → Native plugin
```

Start with the simplest. Escalate only when the simpler type cannot do the job.

**Progressive disclosure:** Only skill names and descriptions load at session start. Full skill bodies load on demand. Install many skills without burning context.

**Bundled-first:** Run `openclaw plugins list --verbose` before searching ClawHub. Most capabilities are already installed, just disabled.

**Restart required:** Every new skill or plugin install requires `openclaw gateway restart` before the next session picks it up.

**ClawHub:** The public skill registry. Search with `openclaw skills search`, install with `openclaw skills install`. Skills, plugins, and MCP servers all require a gateway restart after installation.

**Skills ≠ tool access:** A skill teaches the agent *how* to do something. It does not give the agent the *ability* to access external systems. If the agent needs real tool access, that is an MCP server.

---

## Up Next

**Lesson 7 — MCP Servers:** Skills give knowledge. MCP servers give access. In Lesson 7 you connect your agent to an external service via the Model Context Protocol — live data, real APIs, tools that reach outside the gateway.