from agents import Agent, RunContextWrapper, Runner, function_tool
from config import config
import rich


# Tool 1: Get current location
@function_tool
def get_current_location(ctx: RunContextWrapper[None]) -> str:
    """Returns the user's current location."""
    # Dummy location for demonstration
    return "New York, USA"


# Tool 2: Get breaking news
@function_tool
def get_breaking_news(ctx: RunContextWrapper[None]) -> list[str]:
    """Returns a list of breaking news headlines."""
    return [
        "Global markets rally amid economic optimism.",
        "Major breakthrough in renewable energy announced.",
    ]


# Tool 3: Explain photosynthesis
@function_tool
def explain_photosynthesis(ctx: RunContextWrapper[None]) -> str:
    """Explains the process of photosynthesis."""
    return "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water."


agent = Agent[None](
    name="multi_query_agent",
    instructions="Answer each query using the appropriate tools. MUST call TOOLS",
    tools=[get_current_location, get_breaking_news, explain_photosynthesis],
)

config.tracing_disabled = False

result = Runner.run_sync(
    agent,
    """
    1. What is my current location?
    2. Any breaking news?
    3. What is photosynthesis
    """,
    run_config=config,
)

print("=" * 50)
print("Result: ", result.last_agent.name)
rich.print(result.new_items)
print("Result: ", result.final_output)
