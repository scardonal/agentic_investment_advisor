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
    # model="gpt-4o",
    model="gpt-5",
    # temperature=0.15,
    # max_tokens=2048,
    max_completion_tokens=2048,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@azure-openai",
    ),
)

sentiment_llm = LLM(
    # model="gpt-4o-mini",
    model="gpt-5-mini",
    # temperature=0.15,
    # max_tokens=2048,
    max_completion_tokens=2048,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@azure-openai",
    ),
)
