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

manager_llm = LLM(
    model="gemini-2.5-pro",
    temperature=0,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@dsvertex",
    ),
)

agent_llm = LLM(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    temperature=0.1,
    max_tokens=2048,
    base_url=PORTKEY_URL,
    api_key="dummy_key",
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider="@aws-bedrock-use2",
    ),
)
