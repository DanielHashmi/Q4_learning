# Integrating Groq with OpenAI Agents SDK

This guide explains how to integrate Groq's models with the **OpenAI Agents SDK**, specifically utilizing the **OpenAI GPT-OSS 20B** model hosted on Groq.


## Prerequisites

1.  **Groq API Key**: Obtain a free key from [console.groq.com](https://console.groq.com).
2.  **Installation**:
    ```bash
    pip install openai-agents openai python-dotenv
    ```

## Step 1: Configuration

Create a `.env` file to store your credentials.

```bash
# .env
GROQ_API_KEY=gsk_your_key_here
```

## Step 2: The Factory Pattern

To use Groq with the Agents SDK, you need to create an `OpenAIChatCompletionsModel` that uses a custom `AsyncOpenAI` client pointed at Groq's base URL.

Create a file named `model_factory.py`:

```python
import os
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from dotenv import load_dotenv

load_dotenv()

# Groq's OpenAI-compatible base URL
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

def create_groq_model(model_name: str = "openai/gpt-oss-20b"):
    """
    Creates an OpenAI Agents SDK model backed by Groq.
    
    Args:
        model_name: The model ID to use. Defaults to 'openai/gpt-oss-20b'.
                    Other options include 'llama-3.3-70b-versatile'.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is required")

    # 1. Create a standard OpenAI client pointing to Groq
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=GROQ_BASE_URL,
    )

    # 2. Wrap it in the Agents SDK model class
    return OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=client,
    )
```

## Step 3: Creating and Running an Agent

Now you can build an agent that uses this model. The agent will function exactly like a standard OpenAI agent but will run on Groq's infrastructure.

Create a file named `main.py`:

```python
import asyncio
from agents import Agent, Runner
from model_factory import create_groq_model

# 1. Define a simple tool
def get_weather(location: str) -> str:
    """Get the current weather for a specific location."""
    # Mock response
    return f"The weather in {location} is sunny and 72°F."

async def main():
    # 2. Initialize the model (defaults to openai/gpt-oss-20b)
    model = create_groq_model()

    # 3. Create the Agent
    agent = Agent(
        name="Fast Assistant",
        instructions="You are a helpful assistant. Use the available tools to answer questions.",
        model=model,
        tools=[get_weather],
    )

    # 4. Run the Agent
    print("Agent: Processing request...")
    result = await Runner.run(agent, "What is the weather in San Francisco?")
    
    # 5. Output the result
    print(f"Agent: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Why `openai/gpt-oss-20b`?

While Groq supports Llama models, **`openai/gpt-oss-20b`** is an open-weights model from OpenAI specifically hosted on Groq. It is often a better fit for the Agents SDK because:

1.  **Tool Calling Alignment**: It is trained with similar function-calling patterns as GPT-4, making it highly compatible with the SDK's internal prompts.
2.  **Performance**: On Groq, it runs with extremely low latency.
3.  **Cost**: It is currently available for free on the Groq API.

💡 Note: This guide can be given to any Agent, like (Claude Code, Cursor, Gemini), so they can easily integrate this setup.
