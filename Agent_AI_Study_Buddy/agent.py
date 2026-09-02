import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import tools, available_tools


load_dotenv()


# Groq provides an OpenAI-compatible API.
# So we use the OpenAI client but point it to Groq's server.
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


MODEL = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """
You are Study Buddy, a friendly AI learning assistant.

Your specific job is to help users study content from Wikipedia pages
and documentation websites.

You can:
- Summarize source material clearly.
- Create flashcards for revision.
- Quiz the user and test their understanding.
- Answer follow-up questions about previously discussed material.

IMPORTANT RULES:
1. When a user provides a URL, use the fetch_url_content tool to read it.
2. When answering questions about a source, rely primarily on the source
   content that was retrieved.
3. Do not invent facts that are not supported by the source.
4. If the source does not contain the answer, clearly say so.
5. Keep explanations beginner-friendly unless the user asks for more detail.
6. For flashcards, use a clear Question → Answer format.
7. When testing the user, ask one question at a time and wait for their answer.
8. Be encouraging and act like a helpful study partner.
"""


def run_agent(user_message, history=None):
    """
    Runs the Study Buddy agent.

    Parameters:
        user_message: The latest message from the user.
        history: Previous conversation messages.

    Returns:
        The assistant's final response.
    """

    if history is None:
        history = []

    # -----------------------------
    # STEP 1: Build conversation
    # -----------------------------
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous conversation history
    for message in history:
        messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    # Add the latest user message
    messages.append({
        "role": "user",
        "content": user_message
    })


    # ----------------------------------------
    # STEP 2: AGENT LOOP
    # Think → Tool → Observe → Answer
    # ----------------------------------------

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message


        # --------------------------------
        # STEP 3: Did the model call a tool?
        # --------------------------------

        if not message.tool_calls:

            # No tool call means the model is ready
            # to give its final answer.
            return message.content


        # Add the model's tool-call message to memory
        messages.append(message)


        # --------------------------------
        # STEP 4: Execute requested tools
        # --------------------------------

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            function_args = json.loads(
                tool_call.function.arguments
            )

            print(f"\nTool requested: {function_name}")
            print(f"Arguments: {function_args}")


            # Find the actual Python function
            function_to_call = available_tools.get(
                function_name
            )

            if function_to_call is None:
                tool_result = (
                    f"ERROR: Tool '{function_name}' "
                    "is not available."
                )

            else:
                # Execute the Python function
                tool_result = function_to_call(
                    **function_args
                )


            # --------------------------------
            # STEP 5: Send tool result back
            # --------------------------------

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })


        # The loop continues.
        # The model now observes the tool result and decides:
        #
        # - Do I need another tool?
        # - Or am I ready to answer?