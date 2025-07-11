from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, ItemHelpers
import os
import dotenv
import asyncio

dotenv.load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai'
)

model = OpenAIChatCompletionsModel(
    model='gemini-1.5-flash',
    openai_client=client
)

config = RunConfig(
    model=model,
    tracing_disabled=True
)

dramatic_agent = Agent(
    name='dramatic_agent',
    instructions='You are a dramatic poetry analyst agent. Analyze dramatic poems and explain their meaning (tashree).'
)

lyric_agent = Agent(
    name='lyric_agent',
    instructions='You are a lyric poetry analyst agent. Analyze lyric poems and explain their meaning (tashree).'
)

narrative_agent = Agent(
    name='narrative_agent',
    instructions='You are a narrative poetry analyst agent. Analyze narrative poems and explain their meaning (tashree).'
)

poet_agent = Agent(
    name='poet_agent',
    instructions='You are a creative poet agent. Given a topic or a prompt, generate an original poem in a dramatic, lyric, or narrative style as appropriate.'
)

triage_agent = Agent(
    name='triage_agent',
    instructions="""
        You are a poetry triage agent. Your task is to analyze the input poem and decide whether it is:
        - Dramatic (contains monologue/dialogue)
        - Lyric (expresses emotions, feelings)
        - Narrative (tells a story)

        Choose the appropriate agent to handle it. Then pass the input poem to that agent.
    """,
    handoffs=[dramatic_agent, lyric_agent, narrative_agent]
)

async def main():
    poem = (await Runner.run(poet_agent, 'Create a poem!', run_config=config)).final_output
    
    print(f"Generated Poem: {poem}")
    
    result = Runner.run_streamed(triage_agent, poem, run_config=config)
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types
    
if __name__ == '__main__':
    asyncio.run(main())
