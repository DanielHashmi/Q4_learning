# Production MCP Server,  Week 3 Hands-On

A production-style MCP server demonstrating all Week 3 concepts: lifespan, logging, progress, error handling, and Streamable HTTP transport.

## Concepts Covered

| Concept | Where | What it does |
|---|---|---|
| **Lifespan** | `server.py` → `lifespan()` | Initializes `fake_db` once at startup, shared across all tool calls via `ctx` |
| **Logging** | `get_user` → `ctx.debug/info/warning` | Server sends log messages to the client over MCP protocol,  not stdout |
| **Progress** | `batch_process` → `ctx.report_progress()` | Reports per-item progress live as the tool executes |
| **Error handling** | `get_user` → `CallToolResult(isError=True)` | LLM receives the error as readable text and responds meaningfully |
| **Streamable HTTP** | `mcp_server.run(transport="streamable-http")` | Server runs standalone on port 8000, client connects over HTTP |

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

## Run,  Streamable HTTP (production)

Terminal 1,  start the server:
```bash
python server_streamable_http.py
```

Terminal 2,  run the client:
```bash
python client_streamable_http.py
```

## Run,  stdio (subprocess)

Remove `transport="streamable-http"` from `mcp_server.run()`:
```python
mcp_server.run()  # defaults to stdio
```

Change `client_streamable_http.py`,  replace `MCPServerStreamableHttp` with `MCPServerStdio`:
```python
from agents.mcp import MCPServerStdio # Import First

mcp_server = MCPServerStdio(
    params={"command": sys.executable, "args": ["server_stdio.py"]},
    message_handler=handle_message,
    client_session_timeout_seconds=30,
)
```

Then run only the client,  it launches the server as a subprocess automatically:
```bash
python client_stdio.py
```

## stdio vs Streamable HTTP

| | stdio | Streamable HTTP |
|---|---|---|
| **How server runs** | Subprocess launched by client | Standalone process |
| **Transport** | stdin/stdout | POST/GET/DELETE `/mcp` |
| **Session ID** | Not used | Assigned on connect, sent on every request |
| **Use for** | Local dev, Claude Desktop | Production, remote servers |
| **Key rule** | Never `print()` to stdout,  it corrupts the protocol | No such restriction |

## Key Lessons

1. `ctx.request_context.lifespan_context` is how tools access shared resources initialized in `lifespan()`

2. Logs go to the client via MCP protocol,  use `message_handler` to intercept and print them

3. `isError=True` in `CallToolResult` lets the LLM read and react to errors,  raising an exception becomes a protocol error the LLM cannot read

4. Progress notifications require `client_session_timeout_seconds` to be higher than total tool execution time

5. `sys.executable` in `MCPServerStdio` params ensures the subprocess uses the same venv as the client

6. MCP Sampling, Elicitation and Roots feature are not supported in OpenAI Agents SDK and are out-of-scope as of March 2026

Good luck!👋🏻