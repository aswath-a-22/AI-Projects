import requests
from bs4 import BeautifulSoup


def fetch_url_content(url: str) -> str:
    """
    Fetches a webpage and extracts readable text content.
    Intended for Wikipedia pages and documentation pages.
    """

    try:
        headers = {
            "User-Agent": "StudyBuddy/1.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that usually don't contain useful study content
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator="\n")

        # Clean empty lines
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        content = "\n".join(lines)

        # Prevent sending an extremely large webpage to the model
        max_chars = 16000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[Content truncated]"

        return content

    except requests.exceptions.RequestException as e:
        return f"ERROR: Could not fetch the URL. Details: {str(e)}"


# This is the schema the LLM sees.
# It tells the model WHAT tool is available and HOW to call it.
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_url_content",
            "description": (
                "Fetch and read the content of a Wikipedia or documentation URL. "
                "Use this tool whenever the user provides a URL or asks to summarize, "
                "create flashcards, or test them based on a webpage."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The complete URL of the Wikipedia page or "
                            "documentation page to read."
                        )
                    }
                },
                "required": ["url"]
            }
        }
    }
]


# Mapping between the tool name the model requests
# and the actual Python function we execute.
available_tools = {
    "fetch_url_content": fetch_url_content
}