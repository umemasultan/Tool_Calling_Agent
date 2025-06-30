from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled,function_tool
import os 
from dotenv import load_dotenv
import requests
import random

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model= OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

@function_tool
def how_many_joakes():
    """
    Get Random Nmber for jokes
    """
    return random.randint(1,10)
@function_tool
def get_weather(city:str)->str:
    
    """
    Get the weather for a given city
    """
    try :
        result=requests.get(
        f"// https://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}."
        )
        data = result.json()

        return f"The current weather in{city} is {data["current"]["temp_C"]}C with {data["current"]["condition"]["text"]}"

    except Exception as e :
        return f"Could not fetch weather due to {e}"

agent =Agent(
    name="Assistant",
    instructions="""
if the user asks for jokes, first call 'how_many_jokes', than tell that jokes with nimbers .
if the user asks for weather, call the 'get_weather' funtion with city name
""",
    model=model,
    tools=[get_weather,how_many_joakes]
)
result =Runner.run_sync(
    agent,
    input="tell me jokes",
)
print(result.final_output)