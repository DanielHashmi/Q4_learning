# How to use Kiro Free Tier with Claude Code 🎉

<p align="center">
  <img src="claude-code-with-kiro.png" alt="claude-and-kiro" width="100%">
</p>

Below is the step-by-step guide.

### **Phase 1: Get Your Free Kiro Credits**

1. **Download Kiro IDE**: Go to [kiro.dev](https://kiro.dev) (or search for Kiro IDE) and download the application.
2. **Sign Up & Login**: Open Kiro IDE and sign in.
* *Note:* Just by signing up and logging in, you typically receive **500 free credits** as a trial/bonus.
* Keep Kiro IDE logged in for the next steps.

### **Phase 2: Set Up the Kiro OpenAI Gateway**

This tool creates a local server that looks like OpenAI to other apps, but secretly talks to Kiro using your free credits.

1. **Install Python**: Ensure you have Python (3.10 or newer) installed.
2. **Clone the Gateway Repository**:
Open your terminal/command prompt and run:
```bash
git clone https://github.com/DanielHashmi/kiro-openai-gateway.git
cd kiro-openai-gateway
```


3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```


4. **Setup Your Kiro Credentials**:

```bash
cp .env.example .env
```
```bash
python main.py
```

* You should see a message that the server is running at `http://localhost:8000`. **Keep this terminal window open.**


### **Phase 3: Set Up Claude Code Router**

This tool wraps the official Claude CLI and redirects its requests to your local Kiro gateway.

1. **Install Node.js**: Ensure you have Node.js installed.
2. **Install the Tools**:
Run these commands to install the official Claude Code CLI and the Router:
```bash
npm install -g @anthropic-ai/claude-code
npm install -g @musistudio/claude-code-router
```


3. **Configure the Router**:
Create (or edit) the configuration file at `~/.claude-code-router/config.json`.
Paste this configuration:
```json
{
  "LOG": true,
  "LOG_LEVEL": "debug",
  "Providers": [
    {
      "name": "kiro",
      "api_base_url": "http://localhost:8000/v1/chat/completions",
      "api_key": "my-super-secret-password-123",
      "models": [
        "claude-sonnet-4-5",
        "claude-haiku-4-5",
        "claude-opus-4-5"
      ],
      "transformer": {
        "use": ["openrouter"]
      }
    }
  ],
  "Router": {
    "default": "kiro,claude-sonnet-4-5",
    "think": "kiro,claude-sonnet-4-5",
    "background": "kiro,claude-sonnet-4-5",
    "longContext": "kiro,claude-sonnet-4-5",
    "webSearch": "kiro,claude-sonnet-4-5"
  }
}
```


* *Note:* Ensure the `api_key` matches the `PROXY_API_KEY` you set in Phase 2. The model name `claude-sonnet-4-5` corresponds to the models provided by the Kiro Gateway.



### **Phase 4: Launch**

1. **Start the Router Service**:
In a new terminal window, start the router background service:
```bash
ccr start
```


2. **Run Claude Code**:
Now, instead of running `claude`, run:
```bash
ccr code
```

3. Test it out by typing a prompt, for example:
```plaintext
Hi!
```
Once your Kiro IDE credits are used up, you can install the Kiro CLI with the same account to get more 500 free credits, But you need to setup some stuff to start using Kiro CLI credits now with Claude Code Router.

To install Kiro CLI, go to: https://kiro.dev/docs/cli/installation/

Once you have Kiro CLI installed and logged in, you need to commit out or remove the `KIRO_CREDS_FILE="~/.aws/sso/cache/kiro-auth-token.json"` environment variable in your `.env` file and add `KIRO_CLI_DB_FILE="~/.local/share/kiro-cli/data.sqlite3"`

Use IDE codebase find and replace feature to replace `KIRO_CREDS_FILE` with `KIRO_CLI_DB_FILE` in the whole codebase of Kiro OpenAI Gateway.

Run the server again using:
```bash
python main.py
```

Your Kiro CLI credits should now be used when you run Claude Code via the router.