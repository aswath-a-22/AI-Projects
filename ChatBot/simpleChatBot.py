import os
from openai import OpenAI #OpenAI library is required to use the OpenAI API and Groq's LLMs.
from dotenv import load_dotenv #Library required to load environment variables from a .env file

load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1", #Need the support of OPENAI to use Groq's LLMs. This is the base URL for the Groq API endpoint.
)

# Conversation memory
messages = [
    {
        "role": "system",
        "content": "You are a funny joker."
    }
]

while True:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chat ended.")
        break

    # Add user message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Send full conversation
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    assistant_reply = response.choices[0].message.content

    print(f"\nAI: {assistant_reply}\n")

    # Add assistant reply to memory
    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )