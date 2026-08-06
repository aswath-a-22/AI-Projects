import os
from openai import OpenAI #OpenAI library is required to use the OpenAI API and Groq's LLMs.
from dotenv import load_dotenv #Library required to load environment variables from a .env file

load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1", #Need the support of OPENAI to use Groq's LLMs. This is the base URL for the Groq API endpoint.
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",       # a free Llama model on Groq
    messages=[
        {"role": "system", "content": "You are a funny joker."}, #Telling the groq model, this is the way it should behave.  
        {"role": "user",   "content": "Tell me a joke."}, #User query which is passed to the model and solved by the groq API.
    ],
)

print(response.choices[0].message.content) #Printing the response from the model.   