import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI
import sys

_: bool = load_dotenv(find_dotenv())
set_tracing_disabled(True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
GROQ_MODEL = os.getenv("GROQ_MODEL")

client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL,
)

async def main():
    mcp_server = MCPServerStdio(
        params={
            "command": sys.executable,
            "args": ["server.py"],
        }
    )

    async with mcp_server:
        assistant = Agent(
            name="assistant",
            instructions="You are a helpful assistant",
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(model=GROQ_MODEL, openai_client=client),
        )
        result = await Runner.run(assistant, "What is the weather in New York?")
        
        print(f"AGENT RESPONSE: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
    
# client.py → MCPServerStdio → server.py subprocess → get_weather tool → Groq LLM → response