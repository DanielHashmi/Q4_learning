# Basic MCP Server + OpenAI Agents SDK

A minimal working example of an MCP server connected to an AI agent via the OpenAI Agents SDK.

## How it works

```
client.py → MCPServerStdio → server.py (subprocess) → tool executes → Groq LLM → response
```

The client launches `server.py` as a subprocess and communicates over **stdio**. The agent automatically discovers all tools defined on the server and can call them during a run.

## Setup

```bash
pip install mcp openai-agents python-dotenv openai
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=openai/gpt-oss-20b
```

## Run

```bash
python client.py
```

## Files

| File | Role |
|---|---|
| `server.py` | MCP server,  defines tool (`get_weather`) |
| `client.py` | Launches the server, creates the agent, runs a query |

## Key lessons

1. `server.py` uses the official anthropic `from mcp.server.fastmcp import FastMCP`,  not the standalone `fastmcp` package

2. `client.py` uses `sys.executable` in `MCPServerStdio` params,  ensures the subprocess uses the same venv

3. With stdio transport, **never print to stdout in server.py**,  stdout is the protocol channel

4. `result.new_items` shows every step: `ToolCallItem` → `ToolCallOutputItem` → `MessageOutputItem`

5. Make sure to add keys to the `.env` file and call `set_tracing_disabled(True)` to suppress the `OPENAI_API_KEY is not set` warning when using Groq

6. The agent can call any tool defined on the server. Just add a new function with `@mcp.tool()` and it will be available to the agent.

Good luck!👋🏻