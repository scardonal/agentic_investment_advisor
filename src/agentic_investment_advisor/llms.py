"""
Module for defining LLM models used in the agentic investment advisor application.
"""

# ToDo: Create custom LLM wrapper for Portkey AI to handle async calls and streaming
import os

import yaml
from crewai import LLM
from dotenv import load_dotenv
from portkey_ai import createHeaders

load_dotenv()

PORTKEY_URL = os.getenv("PORTKEY_URL", "")
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY", "")

params_path = os.path.join(os.path.dirname(__file__), "config", "params.yaml")
with open(params_path) as f:
    params = yaml.safe_load(f)

llms_config = params.get("llm_models", {})

gemini_pro_llm = LLM(
    model=llms_config.get("gemini_pro").get("model", "gemini-2.5-pro"),
    temperature=llms_config.get("gemini_pro").get("temperature", 0),
    api_key=llms_config.get("gemini_pro").get("api_key", ""),
    stream=llms_config.get("gemini_pro").get("stream", False),
    base_url=PORTKEY_URL,
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider=llms_config.get("gemini_pro").get("provider", "@dsvertex"),
    ),
)

gemini_flash_llm = LLM(
    model=llms_config.get("gemini_flash").get("model", "gemini-2.5-flash"),
    temperature=llms_config.get("gemini_flash").get("temperature", 0),
    api_key=llms_config.get("gemini_flash").get("api_key", ""),
    stream=llms_config.get("gemini_flash").get("stream", False),
    base_url=PORTKEY_URL,
    extra_headers=createHeaders(
        api_key=PORTKEY_API_KEY,
        provider=llms_config.get("gemini_flash").get("provider", "@dsvertex"),
    ),
)

if main := __name__ == "__main__":
    # Test the LLMs
    test_prompt = "What is the current market sentiment for technology stocks?"
    gemini_pro_llm.call(test_prompt)
