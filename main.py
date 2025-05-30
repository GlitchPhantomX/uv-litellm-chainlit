import os
from dotenv import load_dotenv
from litellm import completion
import chainlit as cl
import json

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    history = cl.user_session.get("chat_history") or []

    history.append({"role": "user", "content": message.content})

    try:
        response = completion(
            model="gemini/gemini-2.0-flash",
            api_key=gemini_api_key,
            messages=history  # ✅ Fixed this line
        )

        response_content = response.choices[0].message.content

        msg.content = response_content
        await msg.update()

        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat_history") or []
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
    print("Chat history saved.")
