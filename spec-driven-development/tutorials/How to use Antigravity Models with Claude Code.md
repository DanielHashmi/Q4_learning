# Antigravity → Claude Code

## WINDOWS (PowerShell)

### 1. Install proxy

```powershell
npm install -g antigravity-claude-proxy
```

### 2. Add Google account(s)

```powershell
antigravity-claude-proxy accounts add
```

(Optional)

```powershell
antigravity-claude-proxy accounts list
```

### 3. Start proxy

```powershell
$env:PORT=3005
antigravity-claude-proxy start
```

Leave this terminal open.

### 4. Install Claude Code

```powershell
irm https://claude.ai/install.ps1 | iex
```

### 5. Set environment variables

```powershell
setx ANTHROPIC_BASE_URL "http://localhost:3005"
setx ANTHROPIC_API_KEY "dummy"
```

Close **all** terminals.

### 6. Claude Code config

```powershell
mkdir $env:USERPROFILE\.claude -Force
```

```powershell
@'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "dummy",
    "ANTHROPIC_BASE_URL": "http://localhost:3005",
    "ANTHROPIC_MODEL": "claude-opus-4-6-thinking",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6-thinking",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6-thinking",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-6",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-4-6-thinking"
  }
}
'@ | Set-Content $env:USERPROFILE\.claude\settings.json -Encoding UTF8
```

### 7. Skip onboarding

```powershell
@'
{
  "hasCompletedOnboarding": true
}
'@ | Set-Content $env:USERPROFILE\.claude.json -Encoding UTF8
```

### 8. Run Claude Code

```powershell
claude
```

## WSL (Ubuntu)

### 1. Install Node.js 18+

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Install proxy

```bash
npm install -g antigravity-claude-proxy
```

### 3. Add Google account(s)

```bash
antigravity-claude-proxy accounts add
```

### 4. Start proxy

```bash
PORT=3005 antigravity-claude-proxy start
```

Leave running.

### 5. Install Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Restart shell.

### 6. Environment variables

```bash
echo 'export ANTHROPIC_BASE_URL="http://localhost:3005"' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="dummy"' >> ~/.bashrc
source ~/.bashrc
```

### 7. Claude Code config

```bash
mkdir -p ~/.claude
```

```bash
cat <<'EOF' > ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "dummy",
    "ANTHROPIC_BASE_URL": "http://localhost:3005",
    "ANTHROPIC_MODEL": "claude-opus-4-6-thinking",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6-thinking",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6-thinking",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-6",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-4-6-thinking"
  }
}
EOF
```

### 8. Skip onboarding

```bash
cat <<'EOF' > ~/.claude.json
{
  "hasCompletedOnboarding": true
}
EOF
```

### 9. Run Claude Code

```bash
claude
```

## Quick sanity checks (both)

```bash
curl http://localhost:3005/health
curl http://localhost:3005/v1/models
```

## Final reality check

* Proxy must be running **before** Claude Code
* Model names **will change again**
* If Claude errors → update strings, not your soul
* This is a dev setup, not a religion

You’re done.

Note: I encountered some issues where Claude got stuck in loops and was performing poorly, so this is never a replacement for Claude's paid plans, it's just something to try for fun if it works.
