import os

from dotenv import load_dotenv
from groq import Groq


def main() -> None:
    load_dotenv()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Explain phishing attack in one line"}
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
