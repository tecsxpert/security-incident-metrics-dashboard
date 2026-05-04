# ai-service/test_groq_API.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def test_groq_connection():
    print("Testing Groq API connection...")
    print(f"Using model: llama-3.3-70b-versatile")
    print("-" * 40)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role":    "user",
                "content": (
                    "You are a cybersecurity assistant. "
                    "In one sentence, what is a security incident?"
                )
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_tokens=100,
    )

    response = chat_completion.choices[0].message.content
    print("SUCCESS — Groq API is working!")
    print(f"Response     : {response}")
    print("-" * 40)
    print(f"Model used   : {chat_completion.model}")
    print(f"Prompt tokens: {chat_completion.usage.prompt_tokens}")
    print(f"Output tokens: {chat_completion.usage.completion_tokens}")
    print(f"Total tokens : {chat_completion.usage.total_tokens}")

if __name__ == "__main__":
    test_groq_connection()