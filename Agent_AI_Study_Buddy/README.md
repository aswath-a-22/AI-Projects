# 🎓 Study Buddy

Study Buddy is an AI-powered learning assistant that helps users study content from Wikipedia and documentation websites.

### What it does

* 📄 Fetches and summarizes webpage content
* 🧠 Creates 5 flashcards for revision
* ❓ Quizzes the user one question at a time
* 💬 Maintains conversation history during the chat
* 🔗 Uses an AI tool to fetch webpage content so responses are grounded in the provided source

### Chosen Flavor

**Tool-using AI Agent**

The application uses an LLM that can decide when to call a Python tool (`fetch_url_content`) to retrieve webpage content before answering the user.

### Tech Stack

* Python
* Gradio — user interface
* Groq — LLM API
* OpenAI Python client — used with Groq's OpenAI-compatible API
* BeautifulSoup — webpage text extraction
* Requests — fetching webpages

### How to Run

1. Install the required packages:

```bash
pip install gradio requests beautifulsoup4 python-dotenv openai
```

2. Create a `.env` file and add your Groq API key:

```text
GROQ_API_KEY=your_api_key_here
```

3. Run the application:

```bash
python app.py
```

4. Open the Gradio link shown in the terminal.

### Example

Paste a URL such as:

```text
https://en.wikipedia.org/wiki/Machine_learning
```

Then ask:

```text
Summarize this
```

or:

```text
Make 5 flashcards from this
```

or:

```text
Test me on what we just studied
```

### What I'd Add Next

I would add **persistent source memory/state**, so Study Buddy can remember the webpage content being studied and use the same source when answering follow-up questions without needing to fetch the page again.
