import os
from http.client import responses

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def test_groq_connection():
    print("Testing Groq API connection...")
    print(f"Using model: llama-3.3-70b-versatile")
    print("-" * 40)

    chat = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a cybersecurity assistant."},
            {"role": "user", "content": "In one sentence, what is a security incident?"}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=60,
    )
    #print(chat)
    response = chat.choices[0].message.content
    print("SUCCESS — Groq API is working!")
    print(f"Response: {response}")
    print("-" * 40)
    print(f"Model used   : {chat.model}")
    print(f"Prompt tokens: {chat.usage.prompt_tokens}")
    print(f"Output tokens: {chat.usage.completion_tokens}")
    print(f"Total tokens : {chat.usage.total_tokens}")


if __name__ == "__main__":
    test_groq_connection()

