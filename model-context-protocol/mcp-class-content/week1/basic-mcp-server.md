# Basic MCP Server #4

## Installation and Setup


```powershell
uv venv
```

```powershell
.venv/Scripts/activate
```

```powershell
uv pip install "fastmcp[cli]"
```

```powershell
cd .\mcp-class-content\week1
```

```powershell
New-Item mcp_server.py
```

## Basic MCP Server Example

```python
from fastmcp import FastMCP

mcp = FastMCP("Basic MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """Get city weather"""
    return f"The weather in city {city} is sunny."

if __name__ == "__main__":
    mcp.run()
```

## Exercise Test with Inspector

```powershell
npx @modelcontextprotocol/inspector uv run python mcp_server.py
```

This opens a browser at http://localhost:6274. Walk students through:

1. Connect: Inspector performs the initialize handshake, see the raw JSON in the logs panel

2. Tools tab: Click "List Tools" see add and get_weather with their schemas

3. Call add: Enter a: 5, b: 7S, run tool and see the result in JSON format

4. Call get_weather: Enter city: Karachi, run tool and see the result

5. Show a failure: Call add with a missing argument, see the error response structure and message

6. Notice: Resources and Prompts next to the Tools

Good Luck👋🏻