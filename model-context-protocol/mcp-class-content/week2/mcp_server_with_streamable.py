from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name="Basic Streamable HTTP Server")


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather for a Pakistani city."""
    weather_data = {
        "karachi": "40°C ☀️ Stay hydrated!",
        "lahore": "38°C 🌤️ Hot but manageable",
        "islamabad": "28°C 🌥️ Perfect weather!",
    }
    return weather_data.get(city.lower(), f"No data for {city} 🤷")


mcp_app = mcp.streamable_http_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp_app, host="0.0.0.0", port=8000)


# Testing with inspector needs:
# Transport Type: Streamable HTTP
# URL: http://localhost:8000/mcp
# Connection Type: Via Proxy