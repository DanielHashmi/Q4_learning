from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Extended MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two integers together and returns the result."""
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
    """Returns the current weather for a given city."""
    mock_data = {
        "karachi":  "Sunny, 34°C, humidity 65%",
        "london":   "Cloudy, 12°C, light rain expected",
        "new york": "Clear, 22°C, light breeze",
        "tokyo":    "Partly cloudy, 18°C",
    }
    return mock_data.get(city.lower(), f"Weather data not available for '{city}'.")


@mcp.resource("weather://cities/catalog")
def get_city_catalog() -> str:
    """A catalog of all cities supported by this weather server.
    Returns a plain-text list with city names and their time zones."""

    return """
    Supported Cities — Weather Assistant Server
    ============================================
    City        | Time Zone         | Country
    ------------|-------------------|----------
    Karachi     | Asia/Karachi      | Pakistan
    London      | Europe/London     | UK
    New York    | America/New_York  | USA
    Tokyo       | Asia/Tokyo        | Japan
    ============================================
    Use get_weather(city) to retrieve live conditions.""".strip()


@mcp.resource("weather://cities/{city}/current")
def get_city_weather_resource(city: str) -> str:
    """Returns current weather details for a specific city as a resource.
    URI: weather://cities/{city}/current"""

    mock_data = {
        "karachi": {"temp": "34°C", "condition": "Sunny", "humidity": "65%", "wind": "12 km/h SW"},
        "london": {"temp": "12°C", "condition": "Cloudy", "humidity": "80%", "wind": "20 km/h W"},
        "new york": {"temp": "22°C", "condition": "Clear", "humidity": "55%", "wind": "15 km/h NE"},
        "tokyo": {"temp": "18°C", "condition": "Partly Cloudy", "humidity": "70%", "wind": "8 km/h E"},
    }
    
    data = mock_data.get(city.lower())
    
    if not data:
        return f"No weather data available for '{city}'."

    return f"""
    City: {city.title()}
    Temperature: {data['temp']}
    Condition:   {data['condition']}
    Humidity:    {data['humidity']}
    Wind:        {data['wind']}
    """.strip()


if __name__ == "__main__":
    mcp.run()
