# Extend MCP Server #6


## MCP Example with Tools, Resources and Prompts


```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Assistant Server")


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
    """A catalog of all cities supported by this weather server."""
    return """
Supported Cities — Weather Assistant Server
============================================
City        | Time Zone         | Country
------------|-------------------|----------
Karachi     | Asia/Karachi      | Pakistan
London      | Europe/London     | UK
New York    | America/New_York  | USA
Tokyo       | Asia/Tokyo        | Japan
""".strip()


@mcp.resource("weather://cities/{city}/current")
def get_city_weather_resource(city: str) -> str:
    """Returns current weather details for a specific city as a resource."""
    mock_data = {
        "karachi":  {"temp": "34°C", "condition": "Sunny",         "humidity": "65%", "wind": "12 km/h SW"},
        "london":   {"temp": "12°C", "condition": "Cloudy",        "humidity": "80%", "wind": "20 km/h W"},
        "new york": {"temp": "22°C", "condition": "Clear",         "humidity": "55%", "wind": "15 km/h NE"},
        "tokyo":    {"temp": "18°C", "condition": "Partly Cloudy", "humidity": "70%", "wind": "8 km/h E"},
    }
    data = mock_data.get(city.lower())
    if not data:
        return f"No weather data available for '{city}'."
    return (
        f"City: {city.title()}\n"
        f"Temperature: {data['temp']}\n"
        f"Condition:   {data['condition']}\n"
        f"Humidity:    {data['humidity']}\n"
        f"Wind:        {data['wind']}"
    )


@mcp.prompt()
def weather_briefing(city: str, include_recommendations: bool = True) -> str:
    """Generates a weather briefing prompt for a given city."""
    base = f"Please give me a detailed weather briefing for {city}."
    if include_recommendations:
        base += (
            " Include what to wear, whether to carry an umbrella, "
            "and any outdoor activity recommendations based on the conditions."
        )
    return base


if __name__ == "__main__":
    mcp.run()
```


## Exercise Configure Claude Desktop


1. Update your Claude Desktop Config "C:\Users\<user_name>\AppData\Roaming\Claude\claude_desktop_config.json":
    ```json
    {
        "mcpServers": {
            "weather-assistant": {
            "command": "uv",
            "args": ["run", "python", "/absolute/path/to/server.py"]
            }
        }
    }
    ```
2. Restart Claude Desktop, Demonstrate three things live:

3. Tool: Ask "What's the weather in Tokyo? use MCP", Claude calls get_weather automatically

4. Resource: Click + icon and hover over your MCP and fine Get city catalog to attach into context

5. Prompt: Click the + icon hover over your MCP and find Weather Briefing click and fill in the inputs, it populates the message input automatically

6. Do some disco...

Good Luck👋🏻