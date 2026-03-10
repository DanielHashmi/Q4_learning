import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from openai import AsyncOpenAI

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
    async def handle_message(message):
        if hasattr(message, 'root'):
            msg = message.root
            if hasattr(msg, 'method'):
                if msg.method == "notifications/message":
                    log = msg.params
                    print(f"  [SERVER LOG] [{log.level.upper()}] {log.data}")
                elif msg.method == "notifications/progress":
                    p = msg.params
                    print(f"  [PROGRESS] {p.progress}/{p.total}")
    
    # (Streamable HTTP)
    mcp_server = MCPServerStreamableHttp(
        params={"url": "http://localhost:8000/mcp"},
        message_handler=handle_message,
        client_session_timeout_seconds=30,
    )

    async with mcp_server:
        assistant = Agent(
            name="assistant",
            instructions="You are a helpful assistant",
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(model=GROQ_MODEL, openai_client=client),
        )
        
        result = await Runner.run(assistant, "Process this batch: ['apple', 'banana', 'cherry', 'date', 'elderberry']")
            
        print(f"AGENT RESPONSE: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())