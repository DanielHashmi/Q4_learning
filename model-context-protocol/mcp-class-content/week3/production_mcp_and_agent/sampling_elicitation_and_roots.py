from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent
from pydantic import BaseModel

class DeleteConfirmation(BaseModel):
    confirmed: bool
    reason: str = ""

mcp_server = FastMCP("Feature Test MCP Server")

# (Sampling) The server asks the client "please run an LLM call for me and return the result." The server stays LLM-agnostic; the client controls which model is used
@mcp_server.tool()
async def ai_summarize(text: str, ctx: Context) -> str:
    """Summarize text using LLM sampling"""
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=f"Summarize in 2 sentences:\n\n{text}")
            )
        ],
        max_tokens=200,
    )
    return result.content.text

# (Elicitation) The server asks the client "please collect some input from the human and return it to me." The server pauses mid-execution waiting for a human response
@mcp_server.tool()
async def delete_files(pattern: str, ctx: Context) -> str:
    """Delete files matching a pattern — asks human for confirmation first"""
    all_files = ["report_q1.csv", "report_q2.csv", "notes.txt", "archive.zip"]
    matched = [f for f in all_files if pattern.lower() in f.lower()]
    if not matched:
        return f"No files match pattern '{pattern}'."
    await ctx.info(f"Found {len(matched)} file(s) — requesting human confirmation")
    response = await ctx.elicit(
        message=(
            f"About to delete {len(matched)} file(s):\n"
            + "\n".join(f"  • {f}" for f in matched)
            + "\n\nConfirm?"
        ),
        schema=DeleteConfirmation,
    )
    if response.action != "accept" or not response.data.confirmed:
        return "Deletion cancelled by user."
    return f"Deleted {len(matched)} file(s): {matched}. Reason: {response.data.reason or 'none'}"


# (Roots) The client tells the server "these are the filesystem paths you're allowed to work with." It's the client declaring its boundaries to the server
@mcp_server.tool()
async def list_roots(ctx: Context) -> str:
    """List filesystem roots declared by the client"""
    result = await ctx.session.list_roots()
    if not result.roots:
        return "No roots declared by client."
    return "Roots:\n" + "\n".join(f"  • {r.uri}" for r in result.roots)

if __name__ == "__main__":
    mcp_server.run()
    
# Test with inspector