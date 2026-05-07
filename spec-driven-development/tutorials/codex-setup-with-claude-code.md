## Use Codex Free Quota with Claude Code

### Step 1: Install CLIProxyAPI

Download the Windows binary from the [CLIProxyAPI GitHub releases](https://github.com/router-for-me/CLIProxyAPI/releases), extract it somewhere like `C:\CLIProxyAPI\`.

### Step 2: Configure CLIProxyAPI

Create/edit `config.yaml` in the same folder:

```yaml
port: 8317
auth-dir: "C:\\CLIProxyAPI\\auths"
request-retry: 3
quota-exceeded:
  switch-project: true
api-keys:
  - "my-local-key"   # you choose this, used by ccr
```

### Step 3: Login to Codex via OAuth

```powershell
cd C:\CLIProxyAPI
.\cli-proxy-api.exe --codex-login
```

A browser window opens → sign in with your ChatGPT account → done. Codex caches the login details locally in `~/.codex/auth.json`; it refreshes tokens automatically during use. CLIProxyAPI will store its own copy in `C:\CLIProxyAPI\auths\`.

### Step 4: Start CLIProxyAPI

```powershell
.\cli-proxy-api.exe
```

Leave this terminal running. It's now listening at `http://127.0.0.1:8317` and handles all Responses API ↔ Chat Completions translation automatically.

### Step 5: Configure claude-code-router

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude-code-router"
```

Paste this into a new file at `%USERPROFILE%\.claude-code-router\config.json`:

```json
{
  "LOG": true,
  "LOG_LEVEL": "info",
  "HOST": "127.0.0.1",
  "PORT": 3456,
  "API_TIMEOUT_MS": 600000,
  "Providers": [
    {
      "name": "codex",
      "api_base_url": "http://127.0.0.1:8317/v1/chat/completions",
      "api_key": "my-local-key",
      "models": [
        "gpt-5.4",
        "gpt-5.3-codex",
        "gpt-5.2-codex"
      ],
      "transformer": {
        "use": ["openai"]
      }
    }
  ],
  "Router": {
    "default": "codex,gpt-5.4",
    "background": "codex,gpt-5.4",
    "think": "codex,gpt-5.4",
    "longContext": "codex,gpt-5.4",
    "longContextThreshold": 60000
  }
}
```

### Step 6: Start claude-code-router

In a **second terminal**:

```powershell
ccr start
```

### Step 7: Launch Claude Code

In a **third terminal**:

```powershell
ccr code
```

Type `hi` to test — Codex should respond through Claude Code's interface.