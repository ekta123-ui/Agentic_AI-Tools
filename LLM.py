import streamlit as st
from openai import OpenAI, APITimeoutError

API_KEY = st.secrets["API_KEY"]
BASE_URL = st.secrets["BASE_URL"]
MODEL_NAME = st.secrets["MODEL_NAME"]

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)
import sys
print(sys.executable)

from openai import OpenAI, APITimeoutError

from config import API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def chat(messages: list) -> str:
    """
    Send messages to the LLM and return the response.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0,
            timeout=60,   # Wait up to 60 seconds
        )

        return response.choices[0].message.content.strip()

    except APITimeoutError:
        return "LLM Error: Request timed out. Please try again."

    except Exception as e:
        return f"LLM Error: {e}"


if __name__ == "__main__":

    print("=" * 50)
    print("LLM Test")
    print("=" * 50)

    messages = [
        {
            "role": "user",
            "content": "Tell me the current date and time."
        }
    ]

    response = chat(messages)

    print("\nResponse:\n")
    print(response)