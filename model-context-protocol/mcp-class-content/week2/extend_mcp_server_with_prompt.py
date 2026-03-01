from mcp.server.fastmcp import FastMCP
import logging


logging.basicConfig(level=logging.DEBUG) # Additional for Debugging

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