# Lesson 13 — Gate Your Agent's Tools

## Lesson Overview

Tool profiles (Lesson 3) are binary: the tool is allowed or denied. This lesson builds Tier 2: a custom gate that intercepts tool calls and asks a human operator to approve or deny before the tool runs. You will not write the plugin code. You will write a specification precise enough that your agent builds it correctly.

> **The key insight:** The skill is not writing TypeScript. The skill is specifying constraints precisely enough that the agent does not get them wrong.
> 

---

## 1. The Three-Tier Safety Model

Before building anything, understand where this lesson sits in the full security stack:

| Tier | Mechanism | Enforcement Level | What It Prevents |
| --- | --- | --- | --- |
| **1** | Tool profiles (coding/messaging/minimal) | In-process, same Node.js runtime | Agent accessing unauthorized tools |
| **2** | Plugin hooks with `requireApproval` | In-process, plugin intercepts before execution | Sensitive operations running without operator approval |
| **3** | NemoClaw sandboxing | Out-of-process, kernel-level (Landlock, seccomp, netns) | API key exfiltration, network escape |

**Tier 1** is the door lock: open or closed. Binary.

**Tier 2** is the doorbell: the door stays open, but you are notified before anyone walks through.

**Tier 3** is the vault: kernel-level isolation regardless of what the agent or plugin does.

This lesson builds Tier 2. Tier 3 (NemoClaw) comes in Lesson 15.

**The gap Tier 2 fills:** A booking agent needs the calling tool to confirm appointments. But it should not call a customer without a human checking first. Tool profiles cannot express this — you either have the tool or you do not. A plugin hook can express it: you have the tool, but each use requires approval.

---

## 2. Six Plugin Constraints That Cause Silent Failures

OpenClaw plugins fail silently when these constraints are violated. The code compiles. The plugin loads. Nothing happens. No error message. No warning.

**Constraint 1: `api.on()` NOT `api.registerHook()`**

OpenClaw has two hook systems. Both compile. `api.registerHook()` is the legacy untyped system that silently skips registration without special config. `api.on()` is the typed system that actually works. Always use `api.on()`.

**Constraint 2: Discovery is not activation**

`plugins.load.paths` tells the gateway where to find the plugin. `plugins.entries.<id>.enabled = true` activates it. Without both, the plugin appears loaded but never runs.

**Constraint 3: Hook name requirement (legacy only)**

The legacy `registerHook` system requires `{ name: "my-hook" }` in options. `api.on()` does not have this requirement. Another reason not to use the legacy system.

**Constraint 4: Tool name normalization**

The display name is `bash`. The internal name is `exec`. A hook checking for `"bash"` never fires. Always include `console.log("[plugin-name] tool call:", event.toolName)` to verify which name you are actually seeing.

**Constraint 5: MCP tools bypass `before_tool_call` hooks**

MCP tools are appended after hook wrapping. The approval gate does not intercept MCP tool calls. MCP servers must protect themselves. This is why Google Workspace (Lesson 11) and any MCP server you build in Chapter 57 need their own access controls.

**Constraint 6: Approval routing config required**

The plugin returns `requireApproval`, but the gateway needs routing instructions to deliver the prompt. Add `approvals.plugin` to `openclaw.json` with `enabled: true` and `mode: "session"`. Without this, the hook fires, the tool call blocks, but no approval prompt reaches the operator. The agent receives a "blocked" signal and responds with confused text instead of the formatted approval prompt appearing in chat.

---

## 3. Build the Plugin by Specification

You write the specification. Your agent writes the code.

### Step 1: Copy This Page's URL

Copy the URL of the original lesson page from your browser:

```
https://agentfactory.panaversity.org/docs/Building-OpenClaw-Apps/meet-your-personal-ai-employee/gate-your-agents-tools
```

Your agent will read the Technical Reference section at the bottom of that page to get the six constraints and the reference implementation.

### Step 2: Send the Prompt

Send this to Claude Code or your agent on WhatsApp:

```
Build me an OpenClaw plugin called "my-approval-gate" that requires
my approval on WhatsApp before any shell command runs.

Read the technical reference at the bottom of this page before building:
https://agentfactory.panaversity.org/docs/Building-OpenClaw-Apps/meet-your-personal-ai-employee/gate-your-agents-tools

After creating the plugin files in ~/.openclaw/plugins/my-approval-gate/,
register the plugin:
- Set plugins.load.paths to include ~/.openclaw/plugins
- Enable plugins.entries.my-approval-gate
- Add approvals.plugin config with enabled: true and mode: "session"
- Restart the gateway
- Run openclaw plugins list --verbose to confirm it loaded
```

Your agent reads the page, finds the constraints and reference code, builds the plugin, registers it, and verifies the load. You did not write TypeScript. You wrote a specification with a link to the right constraints.

### Step 3: Verify the Plugin Loaded

```bash
openclaw plugins list --verbose
```

Your plugin should appear as loaded and enabled.

| What you see | What it means | Fix |
| --- | --- | --- |
| Plugin loaded and enabled | ✅ Working | Continue to testing |
| Plugin loaded but disabled | Agent missed `plugins.entries` config | Ask agent to add the enable config |
| Plugin does not appear | `plugins.load.paths` wrong | Ask agent to check the path config |

---

## 4. The Approval Flow

With the plugin loaded, trigger it:

```
Run ls in bash
```

**What happens:**

1. Agent decides to call the `exec` tool
2. Plugin's `before_tool_call` hook fires
3. Hook returns `requireApproval`
4. Gateway sends the approval prompt to you on WhatsApp
5. You see:

```
Shell Command Approval Required
Description: Command: ls -F
Tool: exec | Plugin: my-approval-gate | Agent: main
ID: plugin:83b5035e-faa4-495b-8ed3-8da725a8a327
Expires in: 120s
Reply with: /approve <id> allow-once|allow-always|deny
```

**Three decisions:**

| Decision | Effect |
| --- | --- |
| `allow-once` | This call runs. Future calls still require approval. |
| `allow-always` | This and all future calls from this plugin run without asking. |
| `deny` | This call is blocked. The agent receives a denial. |

Respond:

```
/approve plugin:83b5035e-faa4-495b-8ed3-8da725a8a327 allow-once
```

The tool runs. The agent returns the output. Entire flow through WhatsApp: agent requested a tool, you approved on your phone, tool executed.

**Timeout behavior:** If you do not respond within 120 seconds, `timeoutBehavior: "deny"` blocks the call automatically. **Fail closed.** The agent does not get to try again.

---

## 5. Reference Implementation

Your agent reads this from the lesson URL. Included here for reference.

Three files in `~/.openclaw/plugins/my-approval-gate/`:

**package.json:**

```json
{
  "name": "my-approval-gate",
  "version": "1.0.0",
  "type": "module",
  "main": "index.ts"
}
```

**openclaw.plugin.json:**

```json
{
  "id": "my-approval-gate",
  "name": "My Approval Gate",
  "description": "Requires operator approval before exec calls",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

**index.ts:**

```tsx
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "my-approval-gate",
  name: "My Approval Gate",
  description: "Requires operator approval before exec calls",
  register(api) {
    api.on(
      "before_tool_call",
      async (event) => {
        console.log("[my-approval-gate] tool call:", event.toolName);
        if (event.toolName !== "exec") return {};
        return {
          requireApproval: {
            title: "Shell Command Approval Required",
            description: `Command: ${event.params?.command}`,
            severity: "warning",
            timeoutMs: 120_000,
            timeoutBehavior: "deny",
          },
        };
      },
      { priority: 100 },
    );
  },
});
```

**openclaw.json addition (top level):**

```json
{
  "approvals": {
    "plugin": {
      "enabled": true,
      "mode": "session"
    }
  }
}
```

Three `mode` options: 

- `"session"` (approval prompt appears in same chat)
- `"targets"` (routes to specific channels/users)
- `"both"` (enables both paths)

Use `"session"` for WhatsApp same-chat approval

With `both` approval prompt is sent to **both** the originating chat session and the designated target channels/users at the same time. Whichever party responds first would handle the approval

The `requireApproval` fields: 

- `title`
- `description`
- `severity` (info/warning/critical)
- `timeoutMs` (120000 = 2 minutes)
- `timeoutBehavior` ("deny" = fail closed, "allow" = fail open)

---

## 6. When It Does Not Work

If the approval prompt never appears, check in this order:

```bash
# Step 1: Is the plugin loaded and enabled?
openclaw plugins list --verbose

# Step 2: Is the hook firing at all?
openclaw logs --follow
# Look for: [my-approval-gate] tool call: exec

# Step 3: Is the tool name right?
# Log should show "exec" not "bash"
# If you see "bash", Constraint 4 (tool name normalization) is the issue

# Step 4: Is approval routing configured?
# Ask your agent: "Check whether openclaw.json has approvals.plugin
# with enabled: true and mode: session. Add it if missing."

# Step 5: Is the hook system right?
# Ask your agent: "Check whether the plugin uses api.on() or
# api.registerHook(). It must use api.on()."
```

Send your agent the specific symptom you see. It has the constraints URL. It can diagnose and fix.

---

## 7. Practical Exercises

### Exercise 1 — Test All Three Decisions

Trigger the approval prompt three times:

1. Respond with `allow-once` → verify the command output appears in chat
2. Respond with `deny` → verify the agent receives a denial message
3. Wait for the timeout (2 minutes) → verify the call is blocked without your input

For deny and timeout: do the outputs look the same to the agent? (They should — both produce a block signal.)

**What you are learning:** The three approval decisions and the fail-closed timeout behavior. The agent cannot distinguish between a deny and a timeout — both paths result in the same blocking signal being delivered to the agent. The agent is not provided with metadata indicating why the tool was blocked — whether it was an explicit denial or an automated timeout.

---

### Exercise 2 — Gate a Different Tool

Send your agent:

```
Modify the approval gate to also require approval for file_write
operations. Use severity "critical" for file_write (it is more
dangerous than exec). Keep the exec gate at severity "warning".
```

After the agent modifies the plugin, test:

```
Write 'hello' to /tmp/test.txt
```

Verify the approval prompt appears with the critical severity icon. Then approve and verify the file was written.

**What you are learning:** Extending a plugin through conversational refinement. You did not read the TypeScript to modify it. You described the change in plain language, your agent applied it, you verified the result. This is the constraint-driven specification pattern applied to iteration.

---

### Exercise 3 — Discover the MCP Bypass

If you have any MCP servers configured (like mcp-server-time from Lesson 7), ask:

```
What time is it in Tokyo?
```

Does the approval prompt appear? (No. MCP tools bypass `before_tool_call` hooks.)

Then ask your agent:

```
Why did the approval gate not fire for the time tool?
Explain Constraint 5 from the gate-your-agents-tools lesson
and what this means for any MCP server I build in Chapter 57.
```

**What you are learning:** The MCP bypass is the design constraint that shapes Chapter 57. When you build your own MCP server, you cannot rely on gateway hooks to gate operations. The server must protect itself. Security must be implemented at the layer where it can actually intercept.

---

### Exercise 4 — Constraint Violation Test

Ask your agent to deliberately violate Constraint 4 (tool name normalization):

```
Modify the approval gate to check for tool name "bash" instead
of "exec". Restart the gateway and test by asking me to run ls.
```

Then ask: `Run ls in bash`.

Does the approval prompt appear? (No — because the tool is called `exec` internally, not `bash`.)

Now check the log:

```bash
openclaw logs --follow
```

You should see `[my-approval-gate] tool call: exec` — the console.log confirms the hook is firing, but checking for `"bash"` means the condition never matches.

Fix it:

```
Change the tool name check back to "exec". Restart and verify
the approval prompt returns.
```

**What you are learning:** Silent failure in practice. The plugin loads, the hook fires, the log shows activity — but the condition check is wrong. This is why Constraint 4 exists and why the console.log is not optional during development.

---

### Exercise 5 — Design an Approval Policy

Think about your own use case from Lessons 10-12. You have two agents and access to Google Workspace.

Write a plain-language approval policy covering:

1. Which tools should require approval (exec, file_write, email send, calendar create, etc.)
2. Which severity level each gets (info/warning/critical)
3. Which tools should be approved once vs. always vs. denied by default
4. Which tools are MCP-based (and therefore need protection at the MCP server level, not the plugin level)

Then send this policy to your agent and ask it to modify `my-approval-gate` to implement it.

**What you are learning:** Approval policy design is architecture, not configuration. The decisions you make here determine what your agent can do autonomously vs. what requires a human in the loop.

---

## Key Takeaways

**Six constraints for silent failure prevention:**

1. Use `api.on()` not `api.registerHook()`
2. Both `plugins.load.paths` (discovery) AND `plugins.entries.<id>.enabled` (activation)
3. Hook name only required for legacy system
4. Internal tool name is `exec`, not `bash`
5. MCP tools bypass `before_tool_call` hooks entirely
6. `approvals.plugin` config required in `openclaw.json`

**The MCP bypass is architectural:** Plugin hooks only intercept native gateway tools. MCP tools must implement their own access controls. This is not a bug — it is a design boundary. Know where each security layer applies.

**Approval decisions:**

- `allow-once`: single use, future calls still prompt
- `allow-always`: permanent pass for this plugin's approvals
- `deny`: blocked, agent receives denial signal
- Timeout (120s default): same as deny — fail closed

---

## Up Next

**Lesson 14 — Production Deployment:** Everything you have built runs on your laptop. Close the lid and the agent goes silent. Lesson 14 covers deploying to a server, setting up uptime monitoring, configuring production security, and the honest assessment of what is truly ready for real users.