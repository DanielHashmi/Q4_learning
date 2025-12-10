# How to Use Claude Code with Qwen models for Free on PowerShell (Windows)

![claude-code-with-qwen.png](claude-code-with-qwen.png)

## Prerequisites
*   **Node.js (v18+):** Ensure Node.js is installed.
*   **Qwen CLI:** Installed and authenticated.

---

### 1. Install Required Packages
Open PowerShell and run the following command to install the Qwen Code, Claude Code, and the Claude Code Router:

```powershell
npm install -g @qwen-code/qwen-code@latest @anthropic-ai/claude-code @musistudio/claude-code-router
```

### 2. Configure the Router
Run the command below to create the necessary directories and generate the configuration file.

Create directories
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude-code-router", "$env:USERPROFILE\.claude" | Out-Null
```

Write the configuration file
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

### 3. Add Your Access Token
You must retrieve your Qwen access token and add it to the configuration file created above.

**A. Retrieve the Token**
Run this command to display your current Qwen credentials:
```powershell
Get-Content "$env:USERPROFILE\.qwen\oauth_creds.json"
```
*Copy the value inside the `access_token` field (excluding quotes).*

**B. Update the Config File**
Open the configuration file in Notepad:
```powershell
notepad "$env:USERPROFILE\.claude-code-router\config.json"
```
1.  Locate `"api_key": "YOUR_QWEN_ACCESS_TOKEN_HERE"`.
2.  Replace `YOUR_QWEN_ACCESS_TOKEN_HERE` with the token you copied.
3.  Save and close the file.

### 4. Run Claude Code
Start the router and launch the application.

```powershell
ccr restart
ccr code
```

You can now test the connection by typing `> hi`.

---

## Troubleshooting: Token Expiry (401 Errors)
If you receive a 401 Unauthorized error, your Qwen token has likely expired. Follow these steps to refresh it.

**1. Reset Credentials**
Delete the old credentials file and re-authenticate via the Qwen CLI:
```powershell
Remove-Item "$env:USERPROFILE\.qwen\oauth_creds.json"
qwen
```

**2. Retrieve New Token**
Display the new token:
```powershell
Get-Content "$env:USERPROFILE\.qwen\oauth_creds.json"
```

**3. Update Configuration**
Open the config file and paste the new token into the `api_key` field:
```powershell
notepad "$env:USERPROFILE\.claude-code-router\config.json"
```

**4. Restart Router**
Apply the changes:
```powershell
ccr restart
ccr code
```

---
*For WSL setups, refer to the [Linux/macOS guide](https://github.com/DanielHashmi/Q4_learning/blob/main/spec-driven-development/tutorials/How%20to%20Use%20Claude%20Code%20with%20Qwen%20models%20for%20Free%20on%20Linux%20and%20macOS%20(sh%20and%20bash).md).*
