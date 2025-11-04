"""
Module for defining models used in the agentic investment advisor application.
"""

import os

from crewai import LLM
from dotenv import load_dotenv
from portkey_ai import createHeaders

load_dotenv()

PORTKEY_URL = os.getenv("PORTKEY_URL", "")
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY", "")

# ToDo: Define LLM for final report generation

financial_advisor_llm = LLM(
    model="gpt-4o",
    temperature=0.1,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@azure-openai",
    ),
)

sentiment_llm = LLM(
    model="gpt-4o-mini",
    temperature=0.1,
    max_tokens=2048,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@azure-openai",
    ),
)
