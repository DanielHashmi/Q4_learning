# How to Use Claude Code with Gemini models for Free on Linux/macOS (sh/bash)

<p align="center">
  <img src="https://iili.io/fqRL25b.md.png" alt="claude-and-gemini" width="100%">
</p>

**Note:** This guide is specifically for **sh/bash** shells on Linux/macOS.

---

### **Prerequisite: Check Node.js**

Open your **Terminal** and type:

```sh
node --version
```

- **If you see `v18.x.x` (or higher):** You are good.
- **If you see an error:** Go to [nodejs.org](https://nodejs.org/), download the "LTS" version, install it, and restart your terminal.

---

### **Step 1: Get Your Free Google API Key**

1. Go to: [**Google AI Studio**](https://aistudio.google.com/)
2. Click **"Get API Key"**.
3. Sign in with your Google Account.
4. Click **"Create API Key"**.
5. **Copy the key** (It looks like `AIzaSyAaBbCcDd...`). Keep this safe for Step 4.

---

### **Step 2: Install the Tools**

Open **Terminal** and paste this command to install the required software:

```sh
npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router
```

---

### **Step 3: Create the Folders**

Paste this into Terminal:

```sh
mkdir -p ~/.claude-code-router ~/.claude
```

---

### **Step 4: Create the Config File**

Paste this command to create and populate the config file:

```sh
cat > ~/.claude-code-router/config.json << 'EOF'
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
        "gemini-2.5-flash",
        "gemini-2.0-flash"
      ],
      "transformer": {
        "use": ["gemini"]
      }
    }
  ],
  "Router": {
    "default": "gemini,gemini-2.5-flash",
    "background": "gemini,gemini-2.5-flash",
    "think": "gemini,gemini-2.5-flash",
    "longContext": "gemini,gemini-2.5-flash",
    "longContextThreshold": 60000
  }
}
EOF
```

---

### **Step 5: Set Your API Key**

*Replace `YOUR_KEY_HERE` below with the key you copied in Step 1.*

Paste this into Terminal:

```sh
echo 'export GOOGLE_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
```

**Reload your shell configuration:**

```sh
source ~/.bashrc
```

⚠️ **Note:** If the above doesn't work, close your Terminal and open a **new** Terminal window.

## Restart the Router

```sh
ccr stop
ccr start
```

### **Step 6: Verify Everything**

In your Terminal, paste these checks one by one:

1. Check the Key:
    
    ```sh
    echo $GOOGLE_API_KEY
    ```
    
    *(If this is empty, redo Step 5).*
    
2. Check Claude version:
    
    ```sh
    claude --version
    ```
    
3. Check the Router version:
    
    ```sh
    ccr version
    ```

---

### **Step 7: How to use it? (Daily Workflow)**

To use this tool, you need **two** Terminal windows open.

**Window 1: The Server (Keep this running)**

Type this and hit enter. Leave this window open in the background.

```sh
ccr start
```

**Window 2: Your Coding Window**

Open a second Terminal window, go to your project folder, and run:

```sh
ccr code
```

**Test it:**

Once `ccr code` is running, type:

> hi

If it replies, you have successfully set up Claude Code to run for free on Linux/macOS.