# Lesson 15 — Isolate with NemoClaw

## Lesson Overview

Your Docker Compose deployment from Lesson 14 has a real security gap: the API keys live in the same container as the agent. This lesson explains why that matters, how NemoClaw closes the gap architecturally (not procedurally), and when the $10/month upgrade is the right call.

> *Your Lesson 14 deployment is live on a Hetzner VPS. An attacker sends a prompt injection that tricks the agent into running `printenv`. What information is exposed? What could the attacker do with it?*

Write 2-3 sentences. You will revisit this at the end of the lesson.

## 1. The Gap in Docker Compose

In the Lesson 14 Docker Compose deployment:

```yaml
environment:
  - ANTHROPIC_API_KEY=sk-ant-...
  - GOOGLE_API_KEY=AIza...
```

The agent process, the tool execution engine, and the API keys all live in the same container. The messaging tool profile blocks `exec`. But tool profiles are in-process checks in the same Node.js runtime. If an attacker bypasses the runtime through a native module vulnerability, a V8 exploit, or a container escape to the Docker socket, the tool profile is irrelevant and the keys are exposed.

**The security model is:** the agent promises to follow the rules.

**NemoClaw's model is:** the agent physically cannot break the rules.

This is not more rules. It is moving the rules to a place the agent cannot reach.

---

## 2. What NemoClaw Is

NemoClaw is not a new product, not a fork, not a competitor to OpenClaw.

```
NemoClaw = OpenClaw + OpenShell + Privacy Router + Policy Engine
```

One install command. What comes up is a K3s cluster (a lightweight Kubernetes distribution) running inside a single Docker container, with four pods that create something no single-process deployment can achieve: **out-of-process policy enforcement**.

OpenShell is NVIDIA's agent sandbox framework. When you wrap OpenClaw in OpenShell, the agent gets all of its tools — browse, execute commands, write files. But the guardrails are in a different process, on a different network namespace, enforced by a different binary that the agent cannot modify, restart, or see.

---

## 3. The 4-Pod Architecture

Four pods. Four separate processes. Four separate trust boundaries.

| Pod | Purpose | Has API Keys? | Has Agent? |
| --- | --- | --- | --- |
| **Gateway** | Channel adapters, auth, routing, Control UI | No | No |
| **Sandbox** | OpenClaw runtime, agent loop, tools, skills | **No** | **Yes** |
| **Privacy Router** | API key vault, provider fallback, rate limiting | **Yes** | No |
| **Policy Engine** | Landlock (fs), seccomp (syscalls), netns (network) | No | No |

**The critical observation:** No arrow carries API keys into the Sandbox pod. The thing that holds the keys and the thing that holds the agent are in different pods, different processes, different network namespaces.

---

## 4. The Privacy Router: The Most Important Piece

The agent's model configuration points to `inference.local`:

```json
{
  "model": {
    "provider": "openshell-inference",
    "endpoint": "http://inference.local:8080",
    "model": "claude-sonnet-4-20250514"
  }
}
```

**When the agent makes an inference call:**

1. Agent sends a request to `inference.local:8080` with the model name but **no API key**
2. Request crosses a network namespace boundary (Sandbox pod → Router pod)
3. Privacy Router looks up the appropriate provider and API key
4. Router adds the `Authorization` header with the real key
5. Router forwards the request to the actual provider (`api.anthropic.com`)
6. Response comes back through the router, stripped of authentication headers
7. Agent receives a standard model response

At no point does the agent see the API key. At no point does the key exist in the sandbox's memory, environment, filesystem, or network traffic. The key exists only in the router pod's process memory.

---

## 5. The Prompt Injection Scenario: Revisited

Now revisit the answer you wrote at the start of this lesson.

**In Docker Compose:** `printenv` exposes `ANTHROPIC_API_KEY=sk-ant-...` and every other secret in the container. The attacker has your key.

**In NemoClaw:** The worst case is an attacker with full root access inside the sandbox. They have root. They can run any command, read any file, inspect any environment variable, sniff any network traffic.

What can they get?

| Attack Vector | Result |
| --- | --- |
| `printenv` | No API keys in environment |
| Read config files | Model endpoint is `inference.local`, no credentials |
| Sniff network traffic | Traffic to `inference.local` has no Authorization header |
| Scan filesystem | No credential files, no secret mounts |
| Call API directly | Network namespace only routes to `inference.local`, not `api.anthropic.com` |

The attacker has full control of the sandbox and zero access to the API keys. They could abuse the privacy router by making excessive calls (running up the bill), but they cannot steal the keys. Rate limiting on the router handles the abuse case.

**You cannot steal what is not there.**

---

## 6. Kernel-Level Enforcement

The Policy Engine uses Linux kernel primitives, not application-level checks.

**Landlock** restricts filesystem access. The sandbox can read and write its own workspace directory. It cannot read the operator's home directory, the host system's configuration, or other pods' filesystems.

**seccomp** restricts system calls. The sandbox cannot call `ptrace` (inspect other processes), cannot mount filesystems (escape the container), and cannot perform raw socket operations (bypass network policy).

**Network namespaces** control routing. The sandbox does not know the route to `api.anthropic.com`. The route does not exist in the sandbox's network stack. It is not that the request is intercepted and blocked — the route is simply not there.

**The attack chain required to break NemoClaw:** Escape the sandbox pod, gain root in the K3s cluster, modify the policy engine pod's configuration, restart the policy engine. Practically impossible from inside a sandboxed agent process.

---

## 7. The Three-Tier Security Model: Complete

This lesson completes the three-tier security model introduced in Lesson 3 and expanded in Lesson 13:

| Tier | Mechanism | Where | Enforces | Lesson |
| --- | --- | --- | --- | --- |
| **1** | Tool profiles | In-process | Which tools the agent can use | L3 |
| **2** | `requireApproval` hooks | Plugin-level | Operator gates on sensitive ops | L13 |
| **3** | NemoClaw sandbox | Out-of-process | Kernel-level isolation + key separation | L15 |

Each tier builds on the previous. Tier 1 is the baseline. Tier 2 adds human-in-the-loop for specific operations. Tier 3 makes the entire isolation model architectural instead of procedural.

They are independent. Tier 3 does not replace Tier 1 or Tier 2. A NemoClaw deployment still benefits from tool profiles and approval hooks. Defense in depth: each layer is independently sufficient for its threat category.

---

## 8. Policy Presets: Default Deny

By default, the sandbox pod cannot reach any external endpoint. Not Google. Not Anthropic. Not PyPI. Nothing. The only endpoints the sandbox can reach are `inference.local` (the privacy router) and the gateway pod's internal service endpoint.

Operators add presets to allow specific services:

| Preset | What It Allows |
| --- | --- |
| `discord` | Outbound to Discord gateway and API |
| `telegram` | Outbound to Telegram Bot API |
| `slack` | Outbound to Slack API |
| `pypi` | Outbound to [pypi.org](http://pypi.org) (pip install) |
| `npm` | Outbound to [registry.npmjs.org](http://registry.npmjs.org) |
| `dockerhub` | Outbound to Docker Hub |

Custom policies add specific domains and CIDR ranges. When the agent tries to reach an unapproved endpoint, the connection is dropped.

**The agent cannot approve its own network access. The agent cannot modify the policy. The policy engine is in a different pod.**

---

## 9. When to Upgrade

Docker Compose is sufficient for many deployments. NemoClaw is the upgrade when the trust model changes, not when scale changes.

| Signal | What It Means |
| --- | --- |
| A customer asks "where are the API keys stored?" | You need an answer better than "environment variable" |
| A second operator joins | They should not have direct key access |
| A compliance audit requires evidence | Default-deny network policy is audit evidence |
| You serve paying customers whose data is your liability | $10/month is a liability decision, not a cost decision |

### Cost Comparison

| Item | Docker Compose | NemoClaw |
| --- | --- | --- |
| VPS | $5/mo (CX21) | $15/mo (CX31, min 4 vCPU / 8 GB RAM) |
| Model provider | ~$50/mo | ~$50/mo |
| Voice (optional) | $11/mo | $11/mo |
| **Total** | **~$66/mo** | **~$76/mo** |

The security delta is $10/month. NemoClaw requires at minimum 4 vCPU and 8 GB RAM (the K3s cluster, sandbox images, and privacy router add overhead). For any deployment serving paying customers, this is not a cost decision.

---

## 10. The Alpha Reality

Honest assessment: NemoClaw is v0.1.0. OpenShell is v0.0.16. The architecture is sound. The software is alpha.

**What works:** K3s deployment via `nemoclaw setup-spark`. Inference routing. Policy presets. Sandbox creation. Agent execution (tools, skills, heartbeats, crons all function inside the sandbox).

**What does not work yet:**

- **Recovery after crash is manual.** If the internal K3s cluster (the lightweight Kubernetes NemoClaw runs inside Docker) crashes or stops, it won’t automatically heal back to a working agent runtime. You may need to recreate the sandbox pod (the pod that runs the agent/tools) to get unstuck.
- **No sandbox image caching.** When a sandbox is created, NemoClaw needs a sandbox image. Right now it doesn’t cache that image efficiently, so it ends up pushing/pulling a large image (~1142 MiB) each time. If you delete and recreate a sandbox, expect 3–7 minutes just waiting for the image transfer.
- **Log aggregation is split.** Because NemoClaw is four pods (Gateway, Sandbox, Privacy Router, Policy Engine), logs are not centralized. To debug an issue, you may need to run `kubectl logs` for multiple pods and correlate timestamps yourself. There isn’t yet a single unified log view by default.
- **Documentation gaps.** Some important operational details aren’t fully documented yet. For example, you might hit a cgroup v2 Linux/container compatibility issue that’s only mentioned in troubleshooting (not setup), and how to configure provider fallback chains isn’t clearly documented.

**The recommendation:** Start with Docker Compose (Lesson 14). Move to NemoClaw when your first customer asks about API key security and you want a better answer than "environment variable."

---

## 11. Practical Exercises

### Exercise 1 — Draw the Architecture from Memory

On paper or in a text file, draw the 4-pod architecture:

```
Draw four boxes labeled: Gateway, Sandbox, Privacy Router,
Policy Engine. For each, label:
- What it does
- Whether it has API keys
- Whether it has the agent

Draw the connections between pods. Label what data flows
on each connection.
```

Then verify: does any arrow in your diagram carry API keys into the Sandbox? If yes, the diagram is wrong.

**What you are learning:** The architecture is the security argument. If you can draw it and explain why the sandbox pod cannot access the privacy router's credentials, you understand the fundamental difference between in-process and out-of-process security.

---

### Exercise 2 — The Compromise Scenario

```
Assume an attacker has full root access inside the sandbox pod.
List every action they CAN take and every action they CANNOT take.
What is the worst damage they can cause?
How does rate limiting on the privacy router contain that worst case?
```

Compare this to the Docker Compose worst case (full API key access, ability to impersonate the operator on any provider).

**What you are learning:** The worst case in NemoClaw (abuse inference through `inference.local`, run up the bill) is dramatically better than the worst case in Docker Compose. Rate limiting on the router contains even the worst case by capping the financial damage.

---

### Exercise 3 — The Upgrade Decision

```
A friend deploys an AI agent for their small business using
Docker Compose. They ask: "When should I switch to NemoClaw?"
Write three specific triggers that would tell them it's time.
```

Make each trigger concrete and testable. "When it feels less secure" is not a trigger. "When a second operator joins who should not have direct key access" is a trigger.

**What you are learning:** The upgrade decision is about trust boundaries, not scale. Docker Compose with a single operator is fine. When the threat model includes external users, second operators, or compliance requirements, the trust model changes and the architecture should follow.

---

### Exercise 4 — Compare the Three Tiers

For each of these threat scenarios, identify which tier(s) of the security model address it and which tiers do not:

1. An attacker sends a prompt injection trying to read `/etc/passwd`
2. An attacker sends a prompt injection trying to send an email from the agent's account
3. An attacker gains access to the VPS and reads the Docker environment variables
4. A malicious skill attempts to call the Anthropic API directly with stolen credentials
5. A user in `open` DM mode tries to run a shell command

For each, identify: which tier blocks it, and what the attacker gets if that tier fails.

**What you are learning:** Each tier addresses a different threat category. Understanding which tier handles which threat tells you where your actual risk is in your current deployment.

---

### Exercise 5 — Revisit Your Opening Answer

Go back to the answer you wrote at the start of this lesson (the `printenv` prompt injection scenario against your Docker Compose deployment).

Rewrite it for a NemoClaw deployment. Same attack, different architecture.

- What does `printenv` return in the sandbox?
- What is the route to `api.anthropic.com` in the sandbox network?
- What can the attacker do with access to `inference.local`?
- What does rate limiting on the router do to the worst-case damage?

**What you are learning:** The same attack has different outcomes in different architectures. The architectural decision is made before the attack, not during it.

---

## Key Takeaways

**Promises vs Physics:**

- Docker Compose: the agent promises to follow the rules (in-process tool profiles)
- NemoClaw: the agent physically cannot break the rules (out-of-process, kernel-level enforcement)
- The distinction matters when the threat is prompt injection, not misconfiguration

**4-Pod Architecture:**

- Gateway (routing), Sandbox (agent runtime), Privacy Router (holds API keys), Policy Engine (enforcement)
- No arrow carries API keys into the Sandbox
- Each pod is a separate trust boundary

**The Privacy Router:**

- Agent calls `inference.local` without credentials
- Router intercepts, adds real API key, forwards to provider
- Response comes back clean
- Even full sandbox compromise cannot steal the key because it is not there

**Kernel-Level Enforcement:**

- Landlock: filesystem access restriction
- seccomp: system call restriction
- Network namespaces: route-level isolation (the route to `api.anthropic.com` does not exist in the sandbox)

**Default Deny:**

- Sandbox reaches only `inference.local` and approved endpoints
- Policy presets explicitly allow specific services
- The agent cannot approve its own network access

**When to Upgrade (trust boundaries, not scale):**

- Customer asks where keys are stored
- Second operator joins
- Compliance audit requires evidence
- Paying customers whose data is your liability

**Alpha reality:** Architecture is sound. Software is v0.1.0. Start with Docker Compose. Upgrade when the trust model demands it.

**The three-tier model is now complete:**

- Tier 1 (tool profiles): binary access, in-process
- Tier 2 (approval hooks): human gates on sensitive ops, plugin-level
- Tier 3 (NemoClaw): credential isolation + kernel enforcement, out-of-process

---

## The Honest Assessment: What Ships, What Does Not

Fifteen lessons. A working deployment. Three security tiers. What is actually ready for production?

**Known limitations you must mitigate before shipping to real users:**

- WhatsApp credentials corrupt on reconnect (use a dedicated phone number, monitor for reconnection events)
- Memory is per-agent, not per-customer (no isolation of conversation history between customers in the same agent)
- The gateway is a single point of failure (no hot standby in v0.1.0)
- MCP tools bypass approval hooks (Lesson 13, Exercise 3 — MCP servers must protect themselves)
- Silent failures are everywhere (log monitoring is not optional)

None of these are showstoppers. All of them need mitigation. A zero-critical security audit, a capable model, a dedicated phone number, and log monitoring are the minimum bar for serving real users.

**The answer to "can we ship this?" is:** yes, with those conditions in place.

---

## Course Complete: What You Built

Across 15 lessons, you built and deployed a production Personal AI Employee:

| Lesson | What You Built |
| --- | --- |
| 1 | Architecture mental model: 6 dimensions, Agent OS |
| 2 | Install, connect channel, survive the crash loop |
| 3 | Agent loop, tool profiles, dashboard diagnostics |
| 4 | Workspace files, session caching, SOUL.md optimization |
| 5 | Memory system, MEMORY.md, slash commands |
| 6 | Skills, ClawHub, bundle plugins, escalation path |
| 7 | MCP servers, silent failure, two config scopes |
| 8 | Heartbeats, cron jobs, HEARTBEAT_OK suppression |
| 9 | TTS providers, four modes, modality design |
| 10 | Multi-agent routing, session cache, workspace split |
| 11 | Google Workspace OAuth, least privilege, untrusted content |
| 12 | Orchestration, two-layer concurrency, ACP |
| 13 | Plugin hooks, three-tier security, constraint-driven specification |
| 14 | Production deployment, SSH tunnel, security hardening |
| 15 | NemoClaw, privacy router, out-of-process isolation |

Congratulations 🎉