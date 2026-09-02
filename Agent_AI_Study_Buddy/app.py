import gradio as gr

from agent import run_agent


WELCOME_MESSAGE = """
# 🎓 Study Buddy

Hi! I'm your personal AI Study Buddy 👋

Paste a Wikipedia or documentation URL and I can help you:

📄 **Summarize it**  
🧠 **Create 5 flashcards**  
❓ **Test your understanding**

I use the source content from the URL to help keep my answers grounded.

### Try something like:
- Summarize https://en.wikipedia.org/wiki/Machine_learning
- Make 5 flashcards from this URL
- Test me on what we just studied
"""


def respond(message, history):

    # If history is empty, initialize it
    if history is None:
        history = []

    # Don't process empty messages
    if not message.strip():
        return "", history

    # Send the previous conversation history to the agent
    response = run_agent(
        user_message=message,
        history=history
    )

    # Add the user's message to memory
    history.append({
        "role": "user",
        "content": message
    })

    # Add Study Buddy's response to memory
    history.append({
        "role": "assistant",
        "content": response
    })

    return "", history


with gr.Blocks(title="Study Buddy") as demo:

    gr.Markdown(WELCOME_MESSAGE)

    chatbot = gr.Chatbot(
        label="Study Buddy",
        height=500
    )

    textbox = gr.Textbox(
        placeholder=(
            "Paste a Wikipedia/docs URL or ask me something "
            "about what we're studying..."
        ),
        label="Your message"
    )

    textbox.submit(
        respond,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot]
    )


if __name__ == "__main__":
    demo.launch(share=True)