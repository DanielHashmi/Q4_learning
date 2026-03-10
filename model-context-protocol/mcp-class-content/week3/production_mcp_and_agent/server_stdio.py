from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import CallToolResult, TextContent
import sys
import asyncio

# (Lifespan) Lifespan is how you set up shared resources that get passed through context
@asynccontextmanager
async def lifespan(server):
    fake_db = {
        "u001": {"name": "Alice", "score": 95},
        "u002": {"name": "Bob",   "score": 72},
    }

    yield {"fake_db": fake_db}

mcp_server = FastMCP("Production MCP Server", lifespan=lifespan)

@mcp_server.tool()
def get_weather(city: str) -> str:
    """Get city weather"""
    return f"The weather in {city} is very hot."

@mcp_server.tool()
async def get_user(user_id: str, ctx: Context) -> CallToolResult:
    """Get a user from the database by ID"""
    await ctx.debug(f"get_user called with user_id={user_id!r}") # (Logging) These logs go to the client/host via MCP protocol, not to stdout

    db = ctx.request_context.lifespan_context["fake_db"]
    user = db.get(user_id)

    if user is None:
        await ctx.warning(f"User not found: {user_id}")
        return CallToolResult(
            isError=True, # (Error Handling) LLM can read this error msg and see the Valid IDs
            content=[TextContent(type="text", text=f"User '{user_id}' not found. Valid IDs: {list(db.keys())}")]
        )

    await ctx.info(f"User found: {user}")
    return str(user)

# (Progress) Each item prints live with half-second gaps as the tool executes
@mcp_server.tool()
async def batch_process(items: list[str], ctx: Context) -> str:
    """Process a list of items one by one, reporting progress after each"""
    total = len(items)
    await ctx.info(f"Starting batch of {total} items")

    results = []
    for i, item in enumerate(items):
        await asyncio.sleep(0.5)
        processed = item.strip().upper()
        results.append(processed)
        await ctx.report_progress(progress=i + 1, total=total)
        await ctx.info(f"[PROGRESS] {i+1}/{total},  {item} → {processed}")

    return f"Processed {total} items: {results}"

if __name__ == "__main__":
    mcp_server.run()