# 9️⃣ Lesson 9 — Give It a Voice (TTS)

## Lesson Overview

Your agent sends text. This lesson teaches it to speak. Three commands and a restart are all it takes to enable voice. The real lesson is what comes after: understanding why `always` mode gets annoying fast, and how to configure the agent to choose voice or text for itself.

> **Before you start:** Terminal open, WhatsApp active, dashboard open. This lesson is the fastest install in the course. The decision-making is where the depth is.
> 

---

## 1. Four Providers, One Interface

OpenClaw bundles four TTS providers behind a unified interface. All produce Opus-encoded OGG audio (48kHz, 64kbps) — the exact format WhatsApp uses for push-to-talk voice messages. Replies appear as playable voice notes, not file attachments.

| Provider | API Key Required | Quality | Cost | Voices |
| --- | --- | --- | --- | --- |
| **Microsoft Edge** | No | Good | Free | 300+ neural |
| **OpenAI TTS** | Yes (`OPENAI_API_KEY`) | Excellent | ~$15/M chars | 6 |
| **ElevenLabs** | Yes (`ELEVENLABS_API_KEY`) | Premium | Free tier available | Thousands |
| **MiniMax** | Yes (`MINIMAX_API_KEY`) | Good | Free tier available | Multiple |

**Start with Microsoft Edge TTS.** It uses the same backend as Edge browser's "Read Aloud" feature. No API key. No signup. No cost. Prove the pipeline first, upgrade quality later.

**One important limit:** Replies longer than 1,500 characters are either auto-summarized before synthesis or skipped entirely. If you hear silence after a long reply, the text exceeded this limit. Check with `/tts status` and adjust with `/tts limit 3000`.

---

## 2. Enable Voice Output

Three config commands and a restart:

**What each line does:**

```bash
openclaw config set messages.tts.auto always
openclaw config set messages.tts.provider microsoft
openclaw config set plugins.entries.microsoft.enabled true
openclaw gateway restart
```

- `messages.tts.auto always` — sets the mode (every reply becomes audio)
- `messages.tts.provider microsoft` — selects the TTS provider
- `plugins.entries.microsoft.enabled true` — activates the bundled Microsoft TTS plugin (disabled by default)
- `gateway restart` — required; config changes do not apply mid-session

### Verify Before Testing

Before sending a test message, check the pipeline:

```
/tts status
```

You should see: `State: enabled`, `Provider: microsoft (configured)`.

If the provider shows `(not configured)`, the plugin did not load. Run `openclaw gateway restart` and recheck.

```bash
# Also verify the plugin loaded
openclaw plugins list --verbose | grep microsoft
# Should show: loaded
```

Now send any message on WhatsApp. Your agent's reply arrives as a playable voice note.

### If No Voice Note Arrives

With `always` mode, every reply must go through TTS conversion. If the TTS pipeline is not ready, replies are silently dropped (not sent as text). Debug in this order:

```bash
# Step 1: Check TTS status in chat
/tts status

# Step 2: Stream the gateway log
openclaw logs --follow
# Look for TTS errors
# File: /tmp/openclaw/openclaw-YYYY-MM-DD.log

# Step 3: Check channel status
openclaw channels status --probe
```

Silent failure applies to TTS the same way it applies to MCP servers (Lesson 7). The agent does not tell you in chat when TTS fails. The log tells you.

---

## 3. Four TTS Modes

The `messages.tts.auto` setting controls who decides when the agent speaks:

| Mode | Who Decides | Behavior |
| --- | --- | --- |
| `off` | Nobody | Text only (default) |
| `always` | Config | Every reply becomes a voice note |
| `inbound` | Customer | Voice reply only when the customer sends a voice message |
| `tagged` | The Agent | TTS fires only when the model includes `[[tts]]` in its reply |

### Why `always` Gets Annoying Fast

With `always` mode:

- A one-word confirmation ("Done.") becomes a voice note
- A list with reference numbers the customer needs to copy becomes a voice note — that they cannot copy from audio
- Every heartbeat message (Lesson 8) becomes audio

`always` mode proves the pipeline. It is not a production setting.

### Why `inbound` Is the Smart Production Default

In `inbound` mode, the agent matches the customer's modality automatically:

- Customer sends text → agent replies with text
- Customer sends a voice note → agent replies with a voice note

No SOUL.md configuration needed. The gateway handles it. This is the safe production default for customer-facing agents.

### Switch to Inbound Mode

```bash
openclaw config set messages.tts.auto inbound
```

> No gateway restart needed for this change. The `messages.tts` config applies dynamically.
> 

Send a text message. You get text back. Record and send a voice note. You get a voice note back.

### Tagged Mode:

In `tagged` mode, the agent decides per-message whether to use voice or text by including `[[tts]]` in its reply. The agent evaluates its own response and picks the modality that serves the content.

To use it effectively, add voice guidelines to SOUL.md:

```
## Voice Output Rules
Use [[tts]] at the end of your reply when giving descriptions,
explanations, or detailed answers. Use text only for confirmations,
short answers, and anything containing numbers or links the user
might need to copy.
```

Switch mode:

```bash
openclaw config set messages.tts.auto tagged
```

> ⚠️ **Caution:** In testing, `[[tts]]` tags sometimes appear as literal text in chat instead of triggering synthesis. Until this is fully resolved, `inbound` is the more reliable production choice. Use `tagged` for internal or single-agent setups where you can test the behavior directly.
> 

---

## 4. The Modality Design Principle

Voice and text are not interchangeable. Each has strengths:

| Voice Works Best For | Text Works Best For |
| --- | --- |
| Descriptions, summaries | Reference numbers, links, code |
| Emotional, persuasive content | Lists the customer needs to copy |
| Hands-busy users (driving, cooking) | Search-friendly content |
| Long-form explanations | Short confirmations |

The `inbound` mode handles this automatically by matching the customer's modality. `tagged` mode gives the agent full control, choosing voice for descriptions and text for functional replies.

**The design question is not "should the agent speak?" It is "when should it speak?"**

---

## 5. Upgrading to OpenAI TTS

Microsoft Edge proves the pipeline. For production voice quality, switch providers:

```bash
openclaw config set messages.tts.provider openai
```

OpenAI TTS supports a `voice` and `instructions` field for voice character. Add to `~/.openclaw/openclaw.json`:

```json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "openai",
      "providers": {
        "openai": {
          "model": "gpt-4o-mini-tts",
          "voice": "coral",
          "instructions": "Speak in a warm, professional tone"
        }
      }
    }
  }
}
```

At roughly $0.015 per 1,000 characters, a typical reply costs less than a tenth of a cent to voice.

**Available voices for OpenAI TTS:** alloy, echo, fable, onyx, nova, shimmer, coral. Each has a distinct character. Test them with short messages before committing to a production voice.

---

## 6. Practical Exercises

### Exercise 1 — Hear Your Agent Speak

Enable Microsoft Edge TTS with `always` mode:

```bash
openclaw config set messages.tts.auto always
openclaw config set messages.tts.provider microsoft
openclaw config set plugins.entries.microsoft.enabled true
openclaw gateway restart
```

Verify with `/tts status`. Then send any message. Confirm the reply arrives as a playable voice note.

**Then check the plugin list:**

```bash
openclaw plugins list --verbose | grep microsoft
```

Confirm it shows `loaded`, not `disabled`.

---

### Exercise 2 — Experience the Annoyance

With `always` mode active, send these three messages in sequence:

```
1. Tell me about the benefits of AI agents for small businesses
2. OK
3. What is 2 + 2?
```

All three arrive as voice notes. Message 1 makes sense as audio. Messages 2 and 3 do not.

Record:

- Which replies felt natural as voice?
- Which felt wrong?
- What would a customer need to copy that they cannot copy from audio?

**What you are learning:** Blanket voice output degrades UX for short, functional replies. This is the lived version of the modality design principle.

---

### Exercise 3 — Switch to Inbound Mode

```bash
openclaw config set messages.tts.auto inbound
```

Send a text message. Confirm the reply is text.

Record a voice note on WhatsApp and send it to your agent. Confirm the reply is a voice note.

Send a text message asking for a booking reference number. Confirm the reply is text (so you can copy the number).

**What you are learning:** `inbound` mode handles the modality decision automatically without any SOUL.md configuration. It is the zero-configuration production default.

---

### Exercise 4 — Configure Tagged Mode

Switch to tagged mode:

```bash
openclaw config set messages.tts.auto tagged
```

Add voice rules to SOUL.md (via dashboard or terminal):

```
## Voice Output Rules
Use [[tts]] at the end of your reply when giving descriptions,
explanations, or detailed answers. Use text only for confirmations,
short answers, and anything containing numbers or links the user
might need to copy.
```

Then send the same three messages from Exercise 2. Does the agent choose voice for the description and text for "OK" and "4"?

If the `[[tts]]` tag appears as literal text instead of triggering synthesis, note it and switch back to `inbound` mode. This is the known behavior issue documented in Section 3.

**What you are learning:** Tagged mode delegates the modality decision to the agent. The quality of those decisions depends on SOUL.md instructions and model capability. You are now designing the agent's communication style, not just its knowledge.

---

### Exercise 5 — The 1,500-Character Limit

Ask your agent for a detailed, multi-paragraph response (e.g., "Explain how neural networks work") with `always` mode active.

If the response exceeds 1,500 characters:

- Does the agent send audio (auto-summarized)?
- Or does it send silence?

Check:

```
/tts status
```

Then adjust the limit:

```
/tts limit 3000
```

Ask the same question again. Does behavior change?

**What you are learning:** TTS has a character limit that affects long responses. This is relevant for heartbeat summaries (Lesson 8) and any agent that produces detailed reports. Know the limit before it surprises you in production.

---

## Key Takeaways

**Start free, upgrade later:** Microsoft Edge TTS is free, requires no API key, and proves the pipeline. Upgrade to OpenAI or ElevenLabs when voice quality matters for production.

**Four modes:**

- `off` — text only (default)
- `always` — every reply is audio (proves the pipeline, not for production)
- `inbound` — match the customer's modality (safe production default)
- `tagged` — agent decides per-message using `[[tts]]` (best UX, requires SOUL.md instructions)

**The 1,500-character limit:** Replies exceeding this are auto-summarized or skipped. Check `/tts status`, adjust with `/tts limit`.

---

## Up Next

**Lesson 10 — Multi-Agent Architecture:** One agent handles everything right now — customer questions and internal operations in the same queue. In Lesson 10 you add a second agent, configure routing, and give each agent its own context, tools, and personality.