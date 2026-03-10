from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("Basic MCP Server")

@mcp_server.tool()
def get_weather(city: str) -> str:
    """Get city weather"""
    return f"The weather in {city} is very hot."

if __name__ == "__main__":
    mcp_server.run()