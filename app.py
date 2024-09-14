import chainlit as cl

# Define the system prompt
system_prompt = "You are a helpful assistant."


# Define the Chainlit app
@cl.on_message
def main(message: str):
    response = cl.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    )
    cl.send_message(response.choices[0].message["content"])


if __name__ == "__main__":
    cl.run(host="0.0.0.0", port=8000)
