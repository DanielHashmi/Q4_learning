from agents import OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled, AsyncOpenAI, function_tool
import dotenv
import os
import asyncio
import requests

dotenv.load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
set_tracing_disabled(True)

client = AsyncOpenAI(
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/.',
    api_key=GEMINI_API_KEY
)

model = OpenAIChatCompletionsModel('gemini-2.0-flash', openai_client=client)

@function_tool
def get_crypto_price(name: str):
    """
    This tool provides real time information for coins
    args: name: str
    """
    print(f"Getting {name} Price...")
    coins = requests.get("https://api.coinlore.net/api/tickers/").json()["data"]

    for coin in coins:
        if coin['name'].lower() == name.lower() or \
           coin['symbol'].lower() == name.lower() or \
           coin['nameid'] == name.lower():
                price = coin['price_usd']
                print(f"Fetched Price: {price}")
                return {"name": coin["name"], "symbol": coin["symbol"], "price_usd": price}

    return {"error": f"Coin '{name}' not found."}

CryptoDataAgent = Agent(
    name='CryptoDataAgent',
    instructions='You are a Crypto Agent. You provide real time rates using get_crypto_price tool. EXPECT the user always asks about coins. NEVER respond to any other TOPIC.',
    model=model,
    tools=[get_crypto_price]
)

async def main():
    results = await Runner.run(CryptoDataAgent, 'What is the price of btc?')
    print(results.final_output)

asyncio.run(main())
