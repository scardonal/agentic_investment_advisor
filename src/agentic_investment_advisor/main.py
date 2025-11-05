#!/usr/bin/env python
import os
import sys
import uuid
import warnings

import opik
from dotenv import load_dotenv
from opik.integrations.crewai import track_crewai

from agentic_investment_advisor.crew import AgenticInvestmentAdvisor

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
opik.configure(api_key=os.getenv("OPIK_API_KEY"))

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    inputs = {
        "user_profile": "Hi. I'm John. I'm 30 years and I want to plan my"
        " retirement portfolio. I want to retire at 65. What do you recommend?",
    }

    try:
        crew = AgenticInvestmentAdvisor().crew()

        # Enable tracking with the crew instance (required for v1.0.0+)
        track_crewai(project_name=os.getenv("OPIK_PROJECT_NAME"))
        # Pass thread_id via opik_args
        args_dict = {
            "trace": {
                "thread_id": str(uuid.uuid4()),
            },
        }

        crew.kickoff(inputs=inputs, opik_args=args_dict)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}") from e


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "user_profile": "Hi, I'm Alex, 42 years old, and I'm planning for retirement in"
        " 20 years. I want to invest in low-risk ETFs. What do you recommend?",
    }
    try:
        AgenticInvestmentAdvisor().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}") from e


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgenticInvestmentAdvisor().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}") from e


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "user_profile": "Hi, I'm Alex, 42 years old, and I'm planning for retirement in"
        " 20 years. I want to invest in low-risk ETFs. What do you recommend?",
    }

    try:
        AgenticInvestmentAdvisor().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}") from e


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as exc:
        raise Exception("Invalid JSON payload provided as argument") from exc

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": "",
    }

    try:
        result = AgenticInvestmentAdvisor().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(
            f"An error occurred while running the crew with trigger: {e}"
        ) from e
