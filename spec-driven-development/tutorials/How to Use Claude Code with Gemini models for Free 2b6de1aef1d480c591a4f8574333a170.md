# How to Use Claude Code with Gemini models for Free on Windows

<p align="center">
  <img src="https://iili.io/fqRL25b.md.png" alt="claude-and-gemini" width="100%">
</p>

**Note:** This guide is specifically for **Windows PowerShell.**

### **Prerequisite: Check Node.js**

Open your **PowerShell** (search "PowerShell" in the start menu) and type:

```powershell
node --version
```

- **If you see `v18.x.x` (or higher):** You are good.
- **If you see an error:** Go to [nodejs.org](https://nodejs.org/), download the "LTS" version, install it, and restart your computer.

---

### **Step 1: Get Your Free Google API Key**

1. Go to: [**Google AI Studio**](https://aistudio.google.com/)
2. Click **"Get API Key"**.
3. Sign in with your Google Account.
4. Click **"Create API Key"**.
5. **Copy the key** (It looks like `AIzaSyAaBbCcDd...`). Keep this safe for Step 4.

---

### **Step 2: Install the Tools**

Open **PowerShell** and paste this command to install the required software:

```powershell
npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router
```

---

### **Step 3: Create the Config File**

1. **Create the folders** by pasting this into PowerShell:
    
    ```powershell
    mkdir $HOME\\.claude-code-router
    
    mkdir $HOME\\.claude
    ```
    
2. **Open a new config file** in Notepad by pasting this:
    
    ```powershell
    notepad $HOME\\.claude-code-router\\config.json
    ```
    
3. **Paste the exact code below** into the Notepad window that just opened:
    
    ```json
    {
      "LOG": true,
      "LOG_LEVEL": "info",
      "HOST": "127.0.0.1",
      "PORT": 3456,
      "API_TIMEOUT_MS": 600000,
      "Providers": [
        {
          "name": "gemini",
          "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/",
          "api_key": "$GOOGLE_API_KEY",
          "models": [
            "gemini-2.5-pro",
            "gemini-2.5-flash"
          ],
          "transformer": {
            "use": ["gemini"]
          }
        }
      ],
      "Router": {
        "default": "gemini,gemini-2.5-pro",
        "background": "gemini,gemini-2.5-pro",
        "think": "gemini,gemini-2.5-pro",
        "longContext": "gemini,gemini-2.5-pro",
        "longContextThreshold": 60000
      }
    }
    ```
    
4. **Save** the file in Notepad (Ctrl+S) and **Close** Notepad.

---

### **Step 4: Set Your API Key**

*Replace `YOUR_KEY_HERE` below with the key you copied in Step 1.*

Paste this into PowerShell:

```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'YOUR_KEY_HERE', 'User')
```

⚠️ **CRITICAL:** Close your PowerShell window now. Open a **new** PowerShell window. The key won't work until you restart the terminal.

---

### **Step 5: Verify Everything**

In your **new** PowerShell window, paste these checks one by one:

1. Check the Key:
    
    ```powershell
    echo $env:GOOGLE_API_KEY
    ```
    
    *(If this is empty, redo Step 4).*
    
2. Check Claude version:
    
    ```powershell
    claude --version
    ```
    
3. Check the Router version:
    
    ```powershell
    ccr version
    ```
    

---

### **Step 6: How to use it? (Daily Workflow)**

To use this tool, you need **two** PowerShell windows open.

**Window 1: The Server (Keep this running)**

Type this and hit enter. Leave this window open in the background.

```powershell
ccr start
```

**Window 2: Your Coding Window**

Open a second PowerShell window, go to your project folder, and run:

```powershell
ccr code
```

**Test it:**

Once `ccr code` is running, type:

> hi
> 

If it replies, you have successfully hacked Claude Code to run for free on Windows.
