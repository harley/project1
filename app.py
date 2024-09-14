import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=openai_api_key)

# Instrument the OpenAI client
cl.instrument_openai()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

settings = {
    "model": "gpt-4o-mini",
    "temperature": 1,
    # ... more settings
}


@cl.on_message
async def on_message(message: cl.Message):
    logging.debug(f"Received message: {message.content}")

    request_payload = {
        "messages": [
            {
                "content": "You are a language coach. Help me learn German as someone who has done a month on Duolingo. My goal is to pass the A1 exam in 2 months.",
                "role": "system",
            },
            {"content": message.content, "role": "user"},
        ],
        **settings,
    }

    logging.debug(f"Request payload: {request_payload}")

    response = await client.chat.completions.create(**request_payload)

    response_content = response.choices[0].message.content
    logging.debug(f"Response content: {response_content}")

    await cl.Message(content=response_content).send()
