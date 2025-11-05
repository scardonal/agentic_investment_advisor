"""
Module for defining LLM models used in the agentic investment advisor application.
"""

import os

from crewai import LLM
from dotenv import load_dotenv
from portkey_ai import createHeaders

load_dotenv()

PORTKEY_URL = os.getenv("PORTKEY_URL", "")
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY", "")


financial_advisor_llm = LLM(
    model="gpt-5",
    max_completion_tokens=2048,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@azure-openai",
    ),
)

sentiment_llm = LLM(
    model="gpt-5-mini",
    max_completion_tokens=2048,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@azure-openai",
    ),
)

if main := __name__ == "__main__":
    # Test the LLMs
    test_prompt = "What is the current market sentiment for technology stocks?"
    response = financial_advisor_llm.call(test_prompt)
    print(response)
