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