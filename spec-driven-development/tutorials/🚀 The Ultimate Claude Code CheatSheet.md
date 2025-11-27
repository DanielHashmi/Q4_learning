# 🚀 The Ultimate Claude Code CheatSheet

![image.png](image.png)

## **Complete Reference - Every Feature, Command & Configuration**

---

## **📦 INSTALLATION**

```bash
# Homebrew (macOS, Linux)
brew install --cask claude-code

# macOS, Linux, WSL
curl -fsSL <https://claude.ai/install.sh> | bash

# Windows PowerShell
irm <https://claude.ai/install.ps1> | iex

# Windows CMD
curl -fsSL <https://claude.ai/install.cmd> -o install.cmd && install.cmd && del install.cmd

# NPM (Node.js 18+)
npm install -g @anthropic-ai/claude-code

# Update to latest version
claude update

```

---

## **🔐 AUTHENTICATION & LOGIN**

```bash
# Start Claude Code (prompts login on first use)
claude

# Login/switch accounts
/login

# Logout
/logout

# Supported account types:
# - Claude.ai (subscription plans - recommended)
# - Claude Console (API access with pre-paid credits)

```

---

## **💬 SLASH COMMANDS (Complete List)**

### **Core Commands**

```bash
/help                    # Show all available commands
/exit                    # Exit Claude Code
/clear                   # Clear conversation history
/resume                  # Resume a previous session
/continue                # Continue most recent conversation
/export [filename]       # Export conversation to file or clipboard
/compact [instructions]  # Compact conversation with optional focus
/rewind                  # Rewind code and/or conversation
/status                  # Show version, model, account, connectivity
/doctor                  # Check Claude Code installation health

```

### **Configuration & Settings**

```bash
/config                  # Open Settings interface (Config tab)
/permissions             # View/update tool permissions
/settings                # Manage settings
/privacy-settings        # View/update privacy settings
/terminal-setup          # Install Shift+Enter binding (iTerm2/VSCode)
/statusline              # Configure Claude Code status line
/vim                     # Enter vim mode
/output-style [style]    # Set output style

```

### **Model & Context**

```bash
/model                   # Select or change AI model
/context                 # View current context usage as colored grid
/cost                    # Show token usage statistics
/usage                   # Show plan limits and rate limit status

```

### **Memory & Project**

```bash
/memory                  # Edit CLAUDE.md memory files
/init                    # Initialize project with CLAUDE.md guide
/add-dir                 # Add additional working directories

```

### **Agents & Tasks**

```bash
/agents                  # Manage custom AI subagents
/todos                   # List current todo items

```

### **Tools & Extensions**

```bash
/mcp                     # Manage MCP server connections and OAuth
/plugin                  # Manage plugins interactively
/hooks                   # Manage hook configurations
/sandbox                 # Enable sandboxed bash tool
/bashes                  # List and manage background tasks

```

### **Development & Debugging**

```bash
/bug                     # Report bugs (sends conversation to Anthropic)
/review                  # Request code review
/pr_comments             # Show pull request comments

```

---

## **⌨️ KEYBOARD SHORTCUTS**

### **General Controls**

```
Ctrl+C                   # Cancel current input/generation
Ctrl+D                   # Exit Claude Code session
Ctrl+L                   # Clear terminal screen (keeps history)
Ctrl+O                   # Toggle verbose output
Ctrl+R                   # Reverse search command history
Ctrl+V (macOS/Linux)     # Paste image from clipboard
Alt+V (Windows)          # Paste image from clipboard
Up/Down arrows           # Navigate command history
Esc + Esc                # Rewind code/conversation
Tab                      # Toggle extended thinking mode
Shift+Tab or Alt+M       # Toggle permission modes
?                        # Show available keyboard shortcuts

```

### **Multiline Input**

```
\\ + Enter                # Quick escape (all terminals)
Option+Enter             # macOS default
Shift+Enter              # After /terminal-setup
Ctrl+J                   # Line feed character
Paste directly           # For code blocks, logs

```

### **Quick Commands**

```
# at start               # Memory shortcut - add to CLAUDE.md
/ at start               # Slash command
! at start               # Bash mode - run commands directly
@                        # File path mention (autocomplete)

```

### **Vim Mode** (after `/vim`)

```
# Mode Switching
Esc                      # Enter NORMAL mode
i                        # Insert before cursor
I                        # Insert at beginning of line
a                        # Insert after cursor
A                        # Insert at end of line
o                        # Open line below
O                        # Open line above

# Navigation (NORMAL mode)
h/j/k/l                  # Move left/down/up/right
w                        # Next word
e                        # End of word
b                        # Previous word
0                        # Beginning of line
$                        # End of line
^                        # First non-blank character
gg                       # Beginning of input
G                        # End of input

# Editing (NORMAL mode)
x                        # Delete character
dd                       # Delete line
D                        # Delete to end of line
dw/de/db                 # Delete word/to end/back
cc                       # Change line
C                        # Change to end of line
cw/ce/cb                 # Change word/to end/back
.                        # Repeat last change

```

---

## **🎯 CLI COMMANDS & FLAGS**

### **Basic Commands**

```bash
claude                           # Start interactive REPL
claude "query"                   # Start REPL with initial prompt
claude -p "query"                # Query via SDK, then exit
cat file | claude -p "query"     # Process piped content
claude -c                        # Continue most recent conversation
claude -c -p "query"             # Continue via SDK
claude -r "<session-id>" "query" # Resume session by ID
claude update                    # Update to latest version
claude mcp                       # Configure MCP servers
claude --debug                   # Show plugin loading details

```

### **Complete CLI Flags**

```bash
--add-dir <paths>                      # Add additional working directories
--agents <json>                        # Define custom subagents via JSON
--allowedTools <tools>                 # Tools allowed without prompting
--disallowedTools <tools>              # Tools disallowed without prompting
--print, -p                            # Print response without interactive mode
--system-prompt <text>                 # Replace entire system prompt
--system-prompt-file <path>            # Load system prompt from file
--append-system-prompt <text>          # Append to default system prompt
--output-format <format>               # Output format: text, json, stream-json
--input-format <format>                # Input format: text, stream-json
--json-schema <schema>                 # Get validated JSON output
--include-partial-messages             # Include partial streaming events
--verbose                              # Enable verbose logging
--max-turns <number>                   # Limit agentic turns
--model <name>                         # Set model (sonnet/opus/haiku or full name)
--permission-mode <mode>               # Start in permission mode
--permission-prompt-tool <tool>        # MCP tool for permission prompts
--resume <session-id>                  # Resume specific session
--continue                             # Load most recent conversation
--dangerously-skip-permissions         # Skip permission prompts (use with caution)

```

---

## **🤖 AI MODELS**

```bash
# Model Tiers
claude-opus-4                    # Most capable
claude-sonnet-4.5                # Balanced (default)
claude-haiku-4.5                 # Fastest

# Switch models
/model                           # Interactive selection
claude --model claude-opus-4     # CLI flag

# Environment Variables
ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4.5
ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4.5
CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-4.5

```

---

## **🧠 THINKING MODES**

```bash
# In your prompt
"think"                          # Normal thinking
"think harder"                   # Increased thinking budget
"ultrathink"                     # Maximum thinking budget

# Toggle with Tab key (sticky)
Tab                              # Toggle thinking mode on/off

# Environment Variable
MAX_THINKING_TOKENS=<number>     # Set thinking token budget

```

---

## **📁 @-MENTIONS (Context Inclusion)**

```bash
@file.ts                         # Include file (truncated to 2000 lines)
@src/components/                 # Include entire directory
@my-agent                        # Invoke custom agent
@mcp-server::uri                 # Reference MCP resource

```

---

## **🔧 CUSTOM SLASH COMMANDS**

### **Location**

```
.claude/commands/*.md            # Project-level
~/.claude/commands/*.md          # User-level

```

### **Command Template**

```markdown
---
description: "Command description"
argument-hint: "[arg]"
model: "claude-opus-4"
allowed-tools: ["Bash(git:*)", "Write(*)"]
thinking: true
---

Your prompt here.
Execute bash: !`git branch --show-current`
Include file: @README.md

```

### **Namespacing**

```
commands/
├── deploy.md                    # /deploy
└── git/
    ├── status.md                # /git:status
    └── commit.md                # /git:commit

```

---

## **🔌 PLUGINS**

### **Plugin Management**

```bash
/plugin                          # Open plugin management interface
/plugin marketplace add <source> # Add marketplace
/plugin install <name>@<marketplace> # Install plugin
/plugin enable <name>@<marketplace>  # Enable plugin
/plugin disable <name>@<marketplace> # Disable plugin
/plugin uninstall <name>@<marketplace> # Uninstall plugin

```

### **Plugin Structure**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # Required: plugin manifest
├── commands/                    # Custom slash commands
│   └── hello.md
├── agents/                      # Custom agents
│   └── helper.md
├── skills/                      # Agent Skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/                       # Event handlers
│   └── hooks.json
└── .mcp.json                    # MCP server definitions

```

### **Plugin Manifest (plugin.json)**

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "homepage": "<https://docs.example.com>",
  "repository": "<https://github.com/author/plugin>",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json"
}

```

---

## **🤖 SUBAGENTS**

### **Define via CLI**

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'

```

### **Define via File**

```
# Project-level: .claude/agents/*.md
# User-level: ~/.claude/agents/*.md

```

### **Agent File Format**

```markdown
---
description: What this agent specializes in
capabilities: ["task1", "task2"]
model: "sonnet"
tools: ["Read", "Edit", "Bash"]
---

# Agent Name

Detailed description of agent's role and expertise.

```

### **Manage Agents**

```bash
/agents                          # Interactive agent management

```

---

## **🎓 AGENT SKILLS**

### **Location**

```
skills/
├── pdf-processor/
│   ├── SKILL.md                 # Required
│   ├── reference.md             # Optional
│   └── scripts/                 # Optional
└── code-reviewer/
    └── SKILL.md

```

### [**SKILL.md](http://skill.md/) Format**

```markdown
---
name: skill-name
description: What this skill does
---

# Skill Name

Detailed instructions for Claude on how to use this skill.

```

---

## **🪝 HOOKS SYSTEM**

### **Location**

```
hooks/hooks.json                 # Project-level
~/.claude/hooks/hooks.json       # User-level

```

### **Hook Events**

```
SessionStart                     # Session begins
UserPromptSubmit                 # User submits prompt
PreToolUse                       # Before tool execution
PostToolUse                      # After tool execution
PermissionRequest                # Permission dialog shown
Notification                     # Notification sent
Stop                             # Claude attempts to stop
SubagentStop                     # Subagent attempts to stop
PreCompact                       # Before conversation compact
SessionEnd                       # Session ends

```

### **Hook Configuration**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}

```

---

## **🔗 MCP (Model Context Protocol)**

### **Configuration Location**

```
~/.config/mcp/mcp-servers.json   # User-level
.mcp.json                        # Project-level

```

### **MCP Server Configuration**

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "mcp-server-github"],
      "transport": "stdio",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    }
  }
}

```

### **MCP Commands**

```bash
/mcp                             # List servers & tools
/mcp add                         # Interactive setup
/mcp add-from-claude-desktop     # Import from Claude Desktop
claude mcp list                  # CLI: Server health status

```

### **MCP Environment Variables**

```bash
MCP_TIMEOUT=30000                # Server startup timeout (ms)
MCP_TOOL_TIMEOUT=60000           # Tool execution timeout (ms)
MAX_MCP_OUTPUT_TOKENS=25000      # Max tokens in MCP responses

```

---

## **🔒 PERMISSIONS & IAM**

### **Permission Modes**

```bash
default                          # Prompts for permission on first use
acceptEdits                      # Auto-accepts file edits for session
plan                             # Plan Mode - analyze only, no modifications
bypassPermissions                # Skips all prompts (requires safe environment)

# Set via CLI
claude --permission-mode plan

# Set in settings.json
{
  "permissionMode": "plan"
}

```

### **Permission Rules**

### **Tool Patterns**

```bash
# Bash
Bash(npm run build)              # Exact match
Bash(npm run test:*)             # Prefix match with wildcard
Bash(curl <http://site.com/:*>)    # URL prefix match

# Read & Edit (gitignore patterns)
//path                           # Absolute path from filesystem root
~/path                           # Path from home directory
/path                            # Path relative to settings file
path or ./path                   # Path relative to current directory

Edit(/docs/**)                   # Edits in <project>/docs/
Read(~/.zshrc)                   # Reads home directory's .zshrc
Edit(//tmp/scratch.txt)          # Edits absolute path /tmp/scratch.txt
Read(src/**)                     # Reads from <current-directory>/src/

# WebFetch
WebFetch(domain:example.com)     # Fetch requests to example.com

# MCP
mcp__puppeteer                   # Any tool from puppeteer server
mcp__puppeteer__puppeteer_navigate # Specific tool from server

# SlashCommand
SlashCommand:/commit             # Exact match (no arguments)
SlashCommand:/review-pr:*        # Prefix match (any arguments)

```

### **Settings Files (Precedence Order)**

```
1. Enterprise policies            # Highest precedence
   - macOS: /Library/Application Support/ClaudeCode/managed-settings.json
   - Linux/WSL: /etc/claude-code/managed-settings.json
   - Windows: C:\\ProgramData\\ClaudeCode\\managed-settings.json

2. Command line arguments

3. Local project settings
   - .claude/settings.local.json

4. Shared project settings
   - .claude/settings.json

5. User settings                  # Lowest precedence
   - ~/.claude/settings.json

```

### **Settings.json Structure**

```json
{
  "allowedTools": [
    "Bash(git:*)",
    "Bash(npm:*)",
    "Read(**/*.ts)",
    "Write(src/**/*)",
    "Search(*)"
  ],
  "disallowedTools": [
    "Bash(rm:*)",
    "Bash(eval:*)",
    "Edit(//.env)"
  ],
  "permissionMode": "ask",
  "additionalDirectories": [
    "../shared-lib",
    "../docs"
  ],
  "env": {
    "NODE_ENV": "development"
  },
  "apiKeyHelper": "~/scripts/get-api-key.sh",
  "autoUpdates": true,
  "marketplaces": [
    {
      "source": "your-org/claude-plugins",
      "autoInstall": ["formatter", "linter"]
    }
  ],
  "plugins": {
    "enabled": ["formatter@your-org", "linter@your-org"]
  }
}

```

---

## **📝 [CLAUDE.md](http://claude.md/) (Project Guidelines)**

### **Location**

```
CLAUDE.md                        # Root level
path/to/CLAUDE.md                # Directory-level

```

### **Import Syntax**

```markdown
# Project Guidelines

@docs/architecture.md
@docs/coding-standards.md

Follow the patterns in imported docs.

## Code Style
- Use TypeScript
- Follow ESLint rules
- Write tests for all features

## Architecture
- Use MVC pattern
- Keep components small
- Document public APIs

```

### **Memory Management**

```bash
/memory                          # Edit memory files
/init                            # Initialize project with CLAUDE.md guide

# Start message with # to add to memory
#Remember: API rate limit is 100 req/min

```

---

## **💾 SESSION MANAGEMENT**

```bash
# Resume sessions
claude --continue                # Resume last session
claude --resume                  # Select from history
claude -r <session-id>           # Resume specific session

# Print mode (non-interactive)
claude --print "query"           # Execute and exit
claude -p --output-format json "query" # JSON output

# Storage location
~/.claude/
├── sessions/                    # Session transcripts
├── shell-snapshot               # Bash state
└── claude.db                    # SQLite database (session history)

# Session cleanup (after 30 days by default)

```

---

## **🛠️ TOOLS AVAILABLE TO CLAUDE**

| Tool | Description | Permission Required |
| --- | --- | --- |
| **AskUserQuestion** | Ask multiple choice questions | No |
| **Bash** | Execute shell commands | Yes |
| **BashOutput** | Retrieve background bash output | No |
| **Edit** | Make targeted file edits | Yes |
| **ExitPlanMode** | Prompt user to exit plan mode | Yes |
| **Glob** | Find files by pattern | No |
| **Grep** | Search file contents | No |
| **KillShell** | Kill background bash shell | No |
| **NotebookEdit** | Modify Jupyter notebook cells | Yes |
| **Read** | Read file contents | No |
| **Skill** | Execute a skill | Yes |
| **SlashCommand** | Run custom slash command | Yes |
| **Task** | Run sub-agent | No |
| **TodoWrite** | Create/manage task lists | No |
| **WebFetch** | Fetch URL content | Yes |
| **WebSearch** | Perform web searches | Yes |
| **Write** | Create/overwrite files | Yes |

---

## **🌐 ENVIRONMENT VARIABLES (Complete List)**

### **Authentication & API**

```bash
ANTHROPIC_API_KEY                # API key for SDK
ANTHROPIC_AUTH_TOKEN             # Custom Authorization header value
ANTHROPIC_CUSTOM_HEADERS         # Custom headers (Name: Value format)
AWS_BEARER_TOKEN_BEDROCK         # Bedrock API key

```

### **Model Configuration**

```bash
ANTHROPIC_MODEL                  # Model parameter name
ANTHROPIC_DEFAULT_HAIKU_MODEL    # Haiku model override
ANTHROPIC_DEFAULT_OPUS_MODEL     # Opus model override
ANTHROPIC_DEFAULT_SONNET_MODEL   # Sonnet model override
ANTHROPIC_SMALL_FAST_MODEL       # [DEPRECATED] Haiku class model
ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION # AWS region for Haiku on Bedrock
CLAUDE_CODE_SUBAGENT_MODEL       # Subagent model
CLAUDE_CODE_MAX_OUTPUT_TOKENS    # Max output tokens for most requests
MAX_THINKING_TOKENS              # Extended thinking token budget

```

### **Bash Tool**

```bash
BASH_DEFAULT_TIMEOUT_MS=60000    # Default timeout for bash commands
BASH_MAX_TIMEOUT_MS=300000       # Maximum timeout for bash commands
BASH_MAX_OUTPUT_LENGTH           # Max characters in bash output
CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR # Return to original dir after each command
CLAUDE_CODE_SHELL_PREFIX=""      # Shell prefix
USE_BUILTIN_RIPGREP=1            # Use built-in rg (0 for system rg)

```

### **Network & Proxy**

```bash
HTTP_PROXY                       # HTTP proxy server
HTTPS_PROXY                      # HTTPS proxy server
NO_PROXY                         # Domains to bypass proxy
NODE_EXTRA_CA_CERTS              # Additional CA certificates
CLAUDE_CODE_CLIENT_CERT          # Client certificate for mTLS
CLAUDE_CODE_CLIENT_KEY           # Client private key for mTLS
CLAUDE_CODE_CLIENT_KEY_PASSPHRASE # Passphrase for encrypted key

```

### **Cloud Providers**

```bash
CLAUDE_CODE_USE_BEDROCK          # Use AWS Bedrock
CLAUDE_CODE_SKIP_BEDROCK_AUTH    # Skip Bedrock auth (for LLM gateway)
CLAUDE_CODE_USE_VERTEX           # Use Google Vertex
CLAUDE_CODE_SKIP_VERTEX_AUTH     # Skip Vertex auth (for LLM gateway)
VERTEX_REGION_CLAUDE_3_5_HAIKU   # Vertex region override
VERTEX_REGION_CLAUDE_3_7_SONNET  # Vertex region override
VERTEX_REGION_CLAUDE_4_0_OPUS    # Vertex region override
VERTEX_REGION_CLAUDE_4_0_SONNET  # Vertex region override
VERTEX_REGION_CLAUDE_4_1_OPUS    # Vertex region override

```

### **MCP**

```bash
MCP_TIMEOUT=30000                # MCP server startup timeout (ms)
MCP_TOOL_TIMEOUT=60000           # MCP tool execution timeout (ms)
MAX_MCP_OUTPUT_TOKENS=25000      # Max tokens in MCP responses

```

### **Configuration**

```bash
CLAUDE_CONFIG_DIR=~/.claude      # Config directory location
CLAUDE_CODE_AUTO_CONNECT_IDE=false # Auto-connect to IDE
CLAUDE_CODE_API_KEY_HELPER_TTL_MS # Credential refresh interval
CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL # Skip IDE extension auto-install

```

### **Prompt Caching**

```bash
DISABLE_PROMPT_CACHING           # Disable for all models
DISABLE_PROMPT_CACHING_HAIKU     # Disable for Haiku
DISABLE_PROMPT_CACHING_OPUS      # Disable for Opus
DISABLE_PROMPT_CACHING_SONNET    # Disable for Sonnet

```

### **Privacy & Telemetry**

```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC # Disable all non-essential traffic
DISABLE_AUTOUPDATER=1            # Disable auto-updates
DISABLE_BUG_COMMAND=1            # Disable /bug command
DISABLE_ERROR_REPORTING=1        # Disable Sentry error reporting
DISABLE_TELEMETRY=1              # Disable Statsig telemetry
DISABLE_COST_WARNINGS=1          # Disable cost warning messages
DISABLE_NON_ESSENTIAL_MODEL_CALLS=1 # Disable non-critical model calls

```

### **UI & Display**

```bash
CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1 # Disable terminal title updates
SLASH_COMMAND_TOOL_CHAR_BUDGET=15000 # Max chars for slash command metadata

```

---

## **🎨 OUTPUT FORMATS**

```bash
# Text output (default)
claude -p "query"

# JSON output
claude -p --output-format json "query"

# Streaming JSON
claude -p --output-format stream-json "query"

# Include partial messages
claude -p --output-format stream-json --include-partial-messages "query"

# Structured output with JSON Schema
claude -p --json-schema '{"type":"object","properties":{...}}' "query"

```

---

## **🔄 CHECKPOINTING & REWIND**

```bash
# Rewind options
Esc + Esc                        # Open rewind menu
/rewind                          # Open rewind menu

# Rewind choices:
# - Conversation only: Rewind to user message, keep code changes
# - Code only: Revert file changes, keep conversation
# - Both: Restore both to prior point

# Limitations:
# - Bash command changes NOT tracked
# - External changes NOT tracked
# - Not a replacement for version control

```

---

## **🐛 DEBUGGING & TROUBLESHOOTING**

```bash
# Debug mode
claude --debug                   # Show plugin loading details

# Verbose logging
claude --verbose                 # Full turn-by-turn output

# Health check
/doctor                          # Check installation health

# View context usage
/context                         # Colored grid of context usage

# View cost/usage
/cost                            # Token usage statistics
/usage                           # Plan limits and rate limit status

# Status information
/status                          # Version, model, account, connectivity

```

---

## **🔥 PRO TIPS & ADVANCED FEATURES**

### **Auto-Compact**

- Triggers at 80% token usage for infinite conversations
- Use `/compact [instructions]` for manual compaction with focus

### **Background Commands**

```bash
Ctrl+B                           # Move bash command to background
# (Tmux users: press Ctrl+B twice)

# Long commands auto-background after timeout

```

### **Bash Mode**

```bash
! npm test                       # Run directly without Claude
! git status                     # Adds command + output to context
! ls -la                         # Shows real-time progress

```

### **Sandbox Mode**

```bash
/sandbox                         # Enable isolated bash execution
# - Filesystem isolation
# - Network isolation
# - Safer autonomous execution

```

### **Thinking Toggle**

```bash
Tab                              # Enable/disable thinking mode
# Sticky across prompts

```

### **File Truncation**

- @-mentions truncate to 2000 lines automatically

### **Parallel Agents**

- Code review uses 5 parallel Sonnet agents
- Only issues ≥80 confidence posted

### **Confidence Threshold**

- Built-in quality filtering for agent outputs

---

## **📊 COMMON WORKFLOWS**

### **Git Workflow**

```bash
/commit                          # Auto-generate commit message
/commit-push-pr                  # Commit + push + create PR
/clean_gone                      # Clean stale branches

```

### **Code Review**

```bash
/code-review                     # Multi-agent PR review
/review                          # Request code review
/pr_comments                     # Show PR comments

```

### **Feature Development**

```bash
/feature-dev                     # 7-phase guided development

```

### **Agent SDK**

```bash
/new-sdk-app                     # Interactive SDK project setup

```

---

## **📚 DIRECTORY STRUCTURE**

```
project/
├── .claude/
│   ├── settings.json            # Project settings
│   ├── settings.local.json      # Local overrides (gitignored)
│   ├── commands/                # Custom slash commands
│   │   └── deploy.md
│   ├── agents/                  # Custom agents
│   │   └── reviewer.md
│   └── hooks/
│       └── hooks.json           # Hook configurations
├── CLAUDE.md                    # Project guidelines
├── skills/                      # Agent Skills
│   └── my-skill/
│       └── SKILL.md
└── .mcp.json                    # MCP server config

~/.claude/                       # User-level config
├── settings.json                # User settings
├── commands/                    # User commands
├── agents/                      # User agents
├── hooks/
│   └── hooks.json
├── sessions/                    # Session transcripts
└── claude.db                    # Session database

```

---

## **🚨 SECURITY BEST PRACTICES**

### **Permission Management**

```bash
# Use specific permission rules
"Bash(git:*)"                    # Allow git commands only
"Edit(src/**/*)"                 # Allow edits in src/ only
"Read(~/.env)"                   # Deny reading .env files (in disallowedTools)

# Use Plan Mode for analysis
claude --permission-mode plan    # Analyze without modifications

```

### **Hooks Security**

```bash
# Always review hooks before registering
# Hooks run with your credentials
# Malicious hooks can exfiltrate data

```

### **Enterprise Policies**

```bash
# Deploy managed settings for organization
# Cannot be overridden by users
# Enforce security policies

```

---

## **🎓 LEARNING RESOURCES**

```bash
# In Claude Code
/help                            # Show all commands
"what can Claude Code do?"       # Ask Claude about capabilities
"how do I use slash commands?"   # Ask for guidance

# Documentation
# - Quickstart: /en/quickstart
# - CLI Reference: /en/cli-reference
# - Common Workflows: /en/common-workflows
# - Settings: /en/settings

# Community
# - Discord: <https://www.anthropic.com/discord>

```

---

## **📦 PLUGIN DEVELOPMENT**

### **Create Plugin**

```bash
mkdir my-plugin
cd my-plugin
mkdir .claude-plugin commands agents skills hooks

# Create plugin.json
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "author": {"name": "Your Name"}
}
EOF

```

### **Test Locally**

```bash
# Create local marketplace
mkdir dev-marketplace
cd dev-marketplace
mkdir .claude-plugin

# Add marketplace.json
# Add plugin to marketplace
# Install and test
/plugin marketplace add ./dev-marketplace
/plugin install my-plugin@dev-marketplace

```

---

## **🔗 QUICK REFERENCE LINKS**

- **Quickstart**: `/en/quickstart`
- **CLI Reference**: `/en/cli-reference`
- **Interactive Mode**: `/en/interactive-mode`
- **Slash Commands**: `/en/slash-commands`
- **Subagents**: `/en/sub-agents`
- **Skills**: `/en/skills`
- **Hooks**: `/en/hooks-guide`
- **Hooks Reference**: `/en/hooks`
- **MCP**: `/en/mcp`
- **Plugins**: `/en/plugins`
- **Plugin Reference**: `/en/plugins-reference`
- **Plugin Marketplaces**: `/en/plugin-marketplaces`
- **Settings**: `/en/settings`
- **IAM**: `/en/iam`
- **Checkpointing**: `/en/checkpointing`
- **Common Workflows**: `/en/common-workflows`

---

## **💡 FINAL NOTES**

- **Session Storage**: ~/.claude/ (SQLite database + transcripts)
- **Auto-cleanup**: Sessions cleaned after 30 days (configurable)
- **Credential Storage**: macOS Keychain (encrypted)
- **Version Control**: Use Git alongside checkpointing
- **Token Limits**: Auto-compact at 80% usage
- **Background Tasks**: Long commands auto-background
- **Sandbox**: Available on Linux/Mac (v2.0.24+)
- **File Access**: Default = launch directory + additional dirs
- **Permission Persistence**: Bash = permanent, Edits = session

---

**This is the most comprehensive Claude Code cheatsheet available, covering every command, feature, configuration option, and advanced capability in the system.**