# Lesson 14 — Deploy to Production

## Lesson Overview

Everything you have built runs on your laptop. Close the lid and your agent stops responding. This lesson moves it to a server that runs 24/7. By the end, your agent responds from a datacenter, and you access its Control UI through an encrypted SSH tunnel.

> **Not ready to deploy?** Read through the steps and understand the process. The exercises at the end work either way.

---

## 1. Choose Your Deployment Path

Three paths, same result: an agent that runs when you sleep. Pick by the learner you are right now, not by which sounds most "production."

| Your situation | Pick | Why |
| --- | --- | --- |
| New to servers, want the free path with fewest gotchas | **Managed** | Pre-installed image, free LLM tokens, no SSH, no firewall config |
| Finished Lesson 2, comfortable with SSH, want CLI practice | **VPS Native** | Same wizard as Lesson 2 |
| Already run Docker Compose for other services | **VPS Docker** | Same isolation model as your existing containers |

**For beginners and the zero-cost path: pick Managed.** Alibaba Cloud's Simple Application Server ships with OpenClaw pre-installed, pre-wired to Model Studio's Singapore region (1 million free tokens per model), Your only cost is the server instance ($0.99-$8/month).

**Pick VPS Native if you finished Lesson 2 and want hands-on learning**.

**Pick VPS Docker only if you already run Docker Compose.** It works but adds `docker compose exec openclaw-gateway` to every command.

---

## 2. Path A: Managed Server (Easiest, Near-Zero Cost)

Alibaba Cloud's Simple Application Server comes with OpenClaw pre-installed. No Docker, no SSH, no manual configuration.

**Pricing:** Starting at $0.99/month (promotional). With the Singapore region free token tier, LLM cost can be $0.

**Steps:**

1. Go to the [OpenClaw on Alibaba Cloud setup page](https://int.alibabacloud.com/m/1000410030/)
2. Select a **Simple Application Server** with the **OpenClaw image** (2 GB+ memory)
3. Choose your region and subscription duration
4. Complete payment
5. In the SAS Console, open your instance and run the firewall configuration command
6. Set up your API key through Model Studio:
    - Open Model Studio and **select the Singapore region** from the region dropdown
    - Generate your API key in the Singapore region
    - Select a model from the Singapore region's model list (avoid Qwen Max — it is expensive)
    - Enable the **free quota limit** option to restrict usage to the 1 million free tokens per model
7. Access the dashboard URL shown in your instance details

> ⚠️ **Select Singapore Region in Model Studio.** Every model listed in Singapore includes 1 million free tokens. If you skip this and use the default region, Alibaba charges for all token usage immediately. With a zero-credit account, Alibaba sends an overdue notice and **suspends your account within 24 hours**, blocking all Model Studio access.

**After provisioning:** Connect a messaging channel. For WhatsApp, follow the [Alibaba Cloud WhatsApp integration guide](https://www.alibabacloud.com/help/en/simple-application-server/use-cases/openclaw-integrated-whatsapp). For Telegram or Discord, SSH into your instance and configure the channel using the same flow from Lesson 2.

Send a test message. If the agent responds, you are deployed.

---

## 3. Path B: VPS Native Install

This is the same flow you ran in Lesson 2, with one extra step: SSH to a server first.

**You need:** A Linux server with at least 2 vCPUs and 4 GB RAM, and basic experience with SSH and the terminal.

**Provider options:**

| Provider | Monthly Cost | Notes |
| --- | --- | --- |
| Hetzner CX21 | $5/mo | Cheapest paid option, 2 vCPU / 4 GB RAM / 40 GB SSD |
| Alibaba ECS | Free 1 year | Zero-cost free trial, then ~$8/mo after |
| DigitalOcean | $6/mo | Familiar if you already have an account |
| Oracle Cloud | Free | Always-Free ARM, 4 vCPU / 24 GB (slower provisioning) |

### Provision a Hetzner Server ($5/month)

1. Sign up at [hetzner.com/cloud](http://hetzner.com/cloud)
2. Create a new project, click **Add Server**
3. Select **Ubuntu 24.04**, **CX21**
4. Add your SSH key (or let Hetzner email you the root password)
5. Click **Create & Buy Now** and note the public IP address

### SSH In and Install

```bash
ssh root@YOUR_VPS_IP

apt-get update
curl -fsSL https://openclaw.ai/install.sh | bash
```

Verify the CLI is on your PATH:

```bash
openclaw --version
```

If `command not found`, reload your shell config:

```bash
source ~/.bashrc   # or ~/.zshrc
```

### Run Onboarding

```bash
openclaw onboard
```

Same wizard as Lesson 2: choose model provider, authenticate, select a model. When prompted for channel, pick Telegram or Discord, or skip and add one next.

> ⚠️ **Do not skip onboarding.** If you cancel the wizard, the gateway runs but no model is configured. Nothing responds. Reconfigure with `openclaw onboard` or manually:

```bash
openclaw config set model.provider google

openclaw config set model.model gemini-2.5-flash
```

**Using Alibaba Model Studio for zero cost?** Select **Custom Provider** in the wizard. Base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`. Paste your Singapore-region API key. Pick `qwen-plus` or `qwen3-coder-next` as the model. **Never pick `qwen-max`** — it is the most expensive model and will burn through the free tier on one long conversation.

### Connect a Channel

**First: Create your Telegram bot** (one-time setup)

1. Open Telegram, search for **@BotFather** (blue checkmark)
2. Send `/newbot`
3. Pick a display name (e.g., "Daniel AI Employee")
4. Pick a username ending in `bot` (e.g., `daniel_ai_employee_bot`)
5. Copy the bot token BotFather provides

**Then connect the channel:**

```bash
# Telegram (easiest for production)
openclaw channels add --channel telegram
# Paste the bot token when prompted

# Discord
openclaw channels add --channel discord

# WhatsApp (requires a dedicated phone number)
openclaw channels add --channel whatsapp
openclaw channels login --channel whatsapp
```

```bash
openclaw gateway restart
```

Send a test message. If the agent responds, you are deployed.

### Verify Health

```bash
openclaw doctor
```

`openclaw doctor` is your first stop for any problem. It checks model provider, channel credentials, file permissions, and daemon status in one command. Run it before reading any logs.

Tail the gateway log:

```bash
journalctl -u openclaw-gateway -f
```

---

## 4. Path C: VPS Docker Compose

> Pick this only if you already run Docker Compose on this VPS and want OpenClaw to fit your existing fleet. For a fresh single-agent deployment, VPS Native is simpler.

### SSH In and Install Docker

```bash
ssh root@YOUR_VPS_IP

apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh

docker --version
docker compose version
```

### Clone and Configure

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw

mkdir -p /root/.openclaw/workspace
chown -R 1000:1000 /root/.openclaw
```

> `chown` gives ownership to user 1000 (the user your agent runs as inside Docker). Skip this and you get "permission denied" errors.

```bash
GATEWAY_TOKEN=$(openssl rand -hex 32)
cat > .env << EOF
OPENCLAW_IMAGE=ghcr.io/openclaw/openclaw:latest
OPENCLAW_GATEWAY_TOKEN=$GATEWAY_TOKEN
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789
OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace
EOF

# Save your gateway token NOW
echo $GATEWAY_TOKEN
```

### Pull, Launch, and Onboard

```bash
docker compose up -d
docker compose ps
```

If it shows `Restarting`, check `docker compose logs -f openclaw-gateway`. If you see `Gateway start blocked — gateway.mode not configured`:

```bash
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set gateway.mode local
docker compose restart openclaw-gateway
```

Run onboarding inside the container:

```bash
docker compose exec openclaw-gateway openclaw onboard --no-install-daemon
```

The `--no-install-daemon` flag tells it Docker manages the process lifecycle.

Connect a channel:

```bash
# Telegram
docker compose exec openclaw-gateway openclaw channels add --channel telegram

# WhatsApp
docker compose exec -it openclaw-gateway openclaw channels add --channel whatsapp
docker compose exec -it openclaw-gateway openclaw channels login --channel whatsapp

docker compose restart openclaw-gateway
```

> ⚠️ **Why not Kubernetes?** WhatsApp is a single-connection protocol. You cannot load-balance it across multiple pods. The linked-device session is stateful, tied to one gateway process. Docker Compose on a single VPS is the correct architecture for one AI Employee.

---

## 5. Access the Control UI

The gateway binds to `127.0.0.1` — not accessible from the public internet. To reach the Control UI from your laptop, open an SSH tunnel:

```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Open `http://127.0.0.1:18789/` in your browser and paste the gateway token.

If your local gateway is already using port 18789, use a different local port:

```bash
ssh -N -L 19000:127.0.0.1:18789 root@YOUR_VPS_IP
# Then open: http://localhost:19000
```

If the page loads but shows no data, fix the allowed origins:

```bash
# Native or Managed:
openclaw config set gateway.controlUi.allowedOrigins \
  '["http://localhost:18789","http://127.0.0.1:18789","http://localhost:19000","http://127.0.0.1:19000"]' \
  --strict-json

# Docker:
docker compose exec openclaw-gateway openclaw config set \
  gateway.controlUi.allowedOrigins \
  '["http://localhost:18789","http://127.0.0.1:18789","http://localhost:19000","http://127.0.0.1:19000"]' \
  --strict-json
```

### The Security Model

| Component | Role |
| --- | --- |
| Loopback bind | Gateway only on `127.0.0.1` — nothing external can reach it |
| SSH tunnel | Encrypted point-to-point from your laptop to the VPS |
| Gateway token | Authentication for the Control UI once tunnel is open |

The SSH key IS the authentication. The tunnel IS the encryption. The loopback binding IS the access control. For a single-operator deployment, this is the correct security posture. No TLS certificate, no reverse proxy, no API gateway needed.

---

## 6. Production Security Hardening

Before any customer touches your agent, run the security audit:

```bash
# Native or Managed:
openclaw security audit

# Docker:
docker compose exec openclaw-gateway openclaw security audit
```

On a default installation, expect critical findings from `groupPolicy` set to `open` and warn findings for credential directory permissions.

### DM Access Policies

Lesson 2 used pairing mode for onboarding. For production, choose deliberately:

| Mode | Behavior when a stranger DMs | Use case |
| --- | --- | --- |
| `pairing` | Bot replies with a one-time code; operator approves via CLI | Personal use, small team onboarding |
| `allowlist` | Silently blocked. Only numbers in `allowFrom` can DM. | **Production with a known contact list** |
| `open` | Anyone can DM (requires `allowFrom: ["*"]`) | Public support or community bots |
| `disabled` | All DMs ignored | Announcement channels, group utilities |

Change mode:

```bash
openclaw configure --section channels
```

Pick WhatsApp, choose **Modify settings**, and select the new policy. The `allowFrom` list accepts E.164 numbers (e.g., `["+15551234567", "+442071838750"]`).

**For production, pick `allowlist`.** It is the only mode that blocks unknown senders without generating pairing codes that expire or hit caps.

> ⚠️ **Open mode is an attack surface.** `dmPolicy: "open"` combined with tool access is how "a bad prompt tricks the agent into doing unsafe things." Only use `open` for bots with no tool access, or with a minimal tool profile.

### Two Commands to Zero Criticals

```bash
# Native or Managed:
openclaw config set groupPolicy allowlist
chmod 700 ~/.openclaw/credentials/

# Docker:
docker compose exec openclaw-gateway openclaw config set groupPolicy allowlist
chmod 700 /root/.openclaw/credentials/
```

Run the audit again. Zero criticals.

---

## 7. Practical Exercises

### Exercise 1 — Deploy or Trace

If you have a VPS, deploy using the steps above. If you do not, trace the deployment:

```
For each of the deployment steps, write one sentence describing
what it does and what breaks if you skip it.
```

Key steps to trace: install → onboard → connect channel → restart → verify health → SSH tunnel → security audit.

**What you are learning:** Production deployment is sequential. Skipping onboarding leaves a running gateway that never responds. Skipping channel setup means the VPS has no way to receive messages. Each step has a specific failure mode.

---

### Exercise 2 — Map the Security Model

```
Draw a diagram showing: your laptop, the SSH tunnel, the VPS,
and the gateway bound to 127.0.0.1. Label where authentication
happens and where encryption happens. Why is no TLS certificate
needed?
```

The SSH tunnel replaces three components (reverse proxy, TLS termination, API gateway) with one. The attack surface is small: SSH key authentication plus loopback binding.

**What you are learning:** The security model is correct because it is simple. Simple security models have fewer failure modes than complex ones. The SSH key is the credential, the tunnel is the transport, and the loopback binding ensures nothing external can even attempt a connection.

---

### Exercise 3 — Calculate Your Costs

```
Calculate the monthly cost of running your AI Employee in production.
Include: VPS, model provider at your expected message volume,
and any optional services. Compare this to the cost of a human
performing the same tasks.
```

For the comparison: a part-time human assistant at minimum wage for equivalent coverage typically costs $800-2,000/month. Your agent at $67-117/month (or $0.99/month on the managed free tier) handles the same tasks 24/7.

**What you are learning:** The infrastructure cost is not the constraint. The value question is whether the agent handles enough volume to justify even a paid model provider. For most use cases, the break-even is a handful of automated tasks per day.

---

### Exercise 4 — The Paper Cut List

Document the ones you hit:

- Was `openclaw` not on your PATH after install? (Reload shell config)
- Did the CORS error appear when tunneling to port 19000? (Add port to `allowedOrigins`)
- Did the crash loop appear? (Same fix as Lesson 2: `openclaw config set gateway.mode local`)
- Did you get "permission denied" errors in Docker? (Check `chown -R 1000:1000`)

For each paper cut, record the symptom, what you ran to diagnose it, and the fix.

**What you are learning:** The paper cuts are the same across every deployment. Thirteen lessons on your laptop were not just about features — they built the debugging instincts you need when the same problems appear on a server with no one else around to ask.

---

### Exercise 5 — Security Audit and Harden

After deploying:

```bash
openclaw security audit
```

Document every finding (critical, warning, info). For each:

1. What is the finding?
2. Why is it a risk?
3. What is the fix command?

Then apply all critical fixes, re-run the audit, and confirm zero criticals.

Finally, set the DM policy:

```bash
openclaw configure --section channels
```

Choose `allowlist` and add the numbers that should have access.

**What you are learning:** Security audit is not a one-time task. Every time you add a new integration (Google Workspace from Lesson 11, a new plugin from Lesson 13), re-run the audit. New integrations introduce new attack surfaces.

---

## Key Takeaways

**The right deployment for one AI Employee:**

- A $5/month VPS (2 vCPU, 4 GB RAM) or $0.99/month managed server
- Single gateway, single agent
- Not Kubernetes, not serverless, not multi-region
- If new: Alibaba managed (fewest gotchas, potentially free)
- If experienced with SSH: VPS Native

**SSH tunnel security:**

- Gateway binds to `127.0.0.1` (not public internet)
- SSH tunnel encrypts traffic from your laptop to VPS
- SSH key = authentication, tunnel = encryption, loopback = access control
- No TLS certificate, no reverse proxy, no API gateway needed

## Up Next

**Chapter 57 — Building Your Own MCP Server:** Your agent is deployed and running 24/7. The next chapter teaches you to build the external tools your agent connects to — MCP servers that give your agent live access to systems you build yourself.