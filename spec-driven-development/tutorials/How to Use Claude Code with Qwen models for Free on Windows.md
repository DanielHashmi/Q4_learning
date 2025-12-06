# How to Use Claude Code with Qwen models for Free on PowerShell (Windows)

![claude-code-with-qwen.png](claude-code-with-qwen.png)

## Prerequisites
- Qwen CLI installed and authenticated
- Node.js v18+ installed

---

### Step 1: Install Claude Code Router and Qwen Code

```powershell
npm install -g @qwen-code/qwen-code@latest
```

```powershell
npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router
```

### Step 2: Extract Your Access Token

Replace `PC_USER` with your Windows username.

Open `C:\Users\PC_USER\.qwen\oauth_creds.json`:

It should look something like this:

```json
{
  "access_token": "YOUR_QWEN_ACCESS_TOKEN_HERE",
  "token_type": "Bearer",
  "refresh_token": "YOUR_QWEN_REFRESH_TOKEN_HERE",
  "resource_url": "portal.qwen.ai",
  "expiry_date": 1764876220290
}
```

Copy the `access_token` value.

---

### Step 3: Create the Folders

Paste this into PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude-code-router", "$env:USERPROFILE\.claude"
```

---

### Step 4: Create the Config File

Paste this command to create and populate the config file:

```powershell
@"
{  
  "LOG": true,  
  "LOG_LEVEL": "info",  
  "HOST": "127.0.0.1",  
  "PORT": 3456,  
  "API_TIMEOUT_MS": 600000,  
  "Providers": [  
    {  
      "name": "qwen",  
      "api_base_url": "https://portal.qwen.ai/v1/chat/completions",  
      "api_key": "YOUR_QWEN_ACCESS_TOKEN_HERE",  
      "models": [  
        "qwen3-coder-plus",  
        "qwen3-coder-plus",  
        "qwen3-coder-plus"  
      ]  
    }  
  ],  
  "Router": {  
    "default": "qwen,qwen3-coder-plus",  
    "background": "qwen,qwen3-coder-plus",  
    "think": "qwen,qwen3-coder-plus",  
    "longContext": "qwen,qwen3-coder-plus",  
    "longContextThreshold": 60000,  
    "webSearch": "qwen,qwen3-coder-plus"  
  }  
}
"@ | Out-File -FilePath "$env:USERPROFILE\.claude-code-router\config.json" -Encoding UTF8
```

To open the config file, use the following command:
```powershell
notepad "$env:USERPROFILE\.claude-code-router\config.json"
```
Replace `YOUR_QWEN_ACCESS_TOKEN_HERE` with your actual access token from Step 2:

---

### Step 5: Start Using

Restart the router server:

```powershell
ccr restart
```

Run Claude Code with Qwen models:

```powershell
ccr code
```

Test with:

```
> hi
```

---

## Token Refresh (When you get 401 errors)

Your OAuth token expires. Refresh it by:
1. Re-authenticating your QWEN CODE CLI: If already logged in and the access_token matches in both `config.json` and `oauth_creds.json`, delete the oauth_creds.json file and run `qwen` to initiate re-authentication.
2. Update the `api_key` in your config.json with the new access_token:
   ```powershell
   notepad "$env:USERPROFILE\.claude-code-router\config.json"
   ```
3. Restart: `ccr restart`
