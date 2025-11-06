"""
Module for defining LLM models used in the agentic investment advisor application.
"""

# ToDo: Create custom LLM wrapper for Portkey AI to handle async calls and streaming
import os

from crewai import LLM
from dotenv import load_dotenv
from portkey_ai import createHeaders

load_dotenv()

PORTKEY_URL = os.getenv("PORTKEY_URL", "")
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY", "")


financial_advisor_llm = LLM(
    model="gemini-2.5-pro",
    temperature=0.1,
    api_key="dummy_key",
    stream=True,
    base_url=PORTKEY_URL,
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@dsvertex",
    ),
)

sentiment_llm = LLM(
    model="gemini-2.5-flash",
    temperature=0.1,
    api_key="dummy_key",
    stream=True,
    base_url=PORTKEY_URL,
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@dsvertex",
    ),
)

if main := __name__ == "__main__":
    # Test the LLMs
    test_prompt = "What is the current market sentiment for technology stocks?"
    response = financial_advisor_llm.call(test_prompt)
    print(response)
