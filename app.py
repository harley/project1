import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import logging
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from prompts import SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set up LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if not langchain_api_key:
    logging.warning(
        "LANGCHAIN_API_KEY is not set. LangSmith tracing will not be available."
    )

# Set your OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
client = wrap_openai(AsyncOpenAI(api_key=openai_api_key))

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-4o-mini",
    "temperature": 1,
    # ... more settings
}

# Add this at the global scope
conversation_history = []


@cl.on_message
@traceable
async def on_message(message: cl.Message):
    global conversation_history

    # Add the user's message to the conversation history
    conversation_history.append({"content": message.content, "role": "user"})

    # Prepare the messages for the API request
    messages = [
        {
            "content": SYSTEM_PROMPT,
            "role": "system",
        },
    ] + conversation_history

    request_payload = {
        "messages": messages,
        **settings,
    }

    logging.debug(f"Request payload: {request_payload}")

    response = await client.chat.completions.create(**request_payload)

    response_content = response.choices[0].message.content
    logging.debug(f"Response content: {response_content}")

    # Add the AI's response to the conversation history
    conversation_history.append({"content": response_content, "role": "assistant"})

    await cl.Message(content=response_content).send()
