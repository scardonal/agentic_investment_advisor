import asyncio
import os
import time
import warnings

import opik
import yaml
from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, llm, task, tool
from crewai.tools import BaseTool
from crewai_tools import TavilyExtractorTool, TavilySearchTool
from dotenv import load_dotenv
from opik.integrations.crewai import track_crewai
from tavily import AsyncTavilyClient

from agentic_investment_advisor.llms import (
    gemini_flash_llm,
    gemini_pro_llm,
)
from agentic_investment_advisor.tools.calculator import CalculatorTool

load_dotenv()

params_path = os.path.join(os.path.dirname(__file__), "config", "params.yaml")
with open(params_path) as f:
    params = yaml.safe_load(f)


def check_guardrail_input(inputs) -> None:
    """
    Guardrail to check for unethical or illegal requests
    and break execution if detected.
    """
    unethical_keywords = params.get("guardrails", {}).get("prohibited_keywords", [])
    user_query = inputs.get("query", "").lower()
    for keyword in unethical_keywords:
        if keyword in user_query:
            break_message = params.get("guardrails", {}).get(
                "break_message", "Request contains prohibited content."
            )
            raise Exception(break_message)


@CrewBase
class AgenticInvestmentAdvisor:
    """AgenticInvestmentAdvisor crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @llm
    def gemini_pro(self) -> LLM:
        return gemini_pro_llm

    @llm
    def gemini_flash(self) -> LLM:
        return gemini_flash_llm

    @tool
    def search_tool(self) -> BaseTool:
        return TavilySearchTool(
            async_client=AsyncTavilyClient(os.getenv("TAVILY_API_KEY", "")),
            max_results=params.get("tools", {})
            .get("tavily_search_tool", {})
            .get("max_results", 5),
        )

    @tool
    def scrape_tool(self) -> BaseTool:
        return TavilyExtractorTool(
            async_client=AsyncTavilyClient(os.getenv("TAVILY_API_KEY", ""))
        )

    @tool
    def calculator(self) -> BaseTool:
        return CalculatorTool()

    @agent
    def customer_support_representative(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_support_representative"],  # type: ignore[index]
            llm=gemini_pro_llm,
        )

    @agent
    def market_data_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_data_researcher"],  # type: ignore[index]
            llm=gemini_pro_llm,
        )

    @agent
    def sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["sentiment_analyst"],  # type: ignore[index]
            llm=gemini_flash_llm,
        )

    @agent
    def financial_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_advisor"],  # type: ignore[index]
            llm=gemini_pro_llm,
        )

    @task
    def user_profile_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["user_profile_extraction_task"],  # type: ignore[index]
        )

    @task
    def research_market_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_market_data_task"],  # type: ignore[index]
        )

    @task
    def market_sentiment_task(self) -> Task:
        return Task(
            config=self.tasks_config["market_sentiment_task"],  # type: ignore[index]
        )

    @task
    def financial_advisement_task(self) -> Task:
        return Task(
            config=self.tasks_config["financial_advisement_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgenticInvestmentAdvisor crew"""

        return Crew(
            # Automatically created by the @agent decorator
            agents=self.agents,  # type: ignore
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            name="Agentic Investment Advisor",
        )


if __name__ == "__main__":

    warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
    opik.configure(api_key=os.getenv("OPIK_API_KEY"))

    # Test the crew creation
    advisor_crew = AgenticInvestmentAdvisor().crew()
    print("Crew created successfully:", advisor_crew.name)

    inputs = {
        "query": "Hi, I'm Priya, 45, and I'm evaluating SPY and QQQ for long-term growth. Which one should I choose?",
    }

    async def async_crew_execution():
        """
        Run the crew.
        """
        try:
            # Run guardrail check first
            check_guardrail_input(inputs)
        except Exception as e:
            print(f"Request blocked: {e}")
            return
        try:
            crew = AgenticInvestmentAdvisor().crew()
            # Enable tracking with the crew instance (required for v1.0.0+)
            track_crewai(project_name=os.getenv("OPIK_PROJECT_NAME"))
            await crew.kickoff_async(inputs=inputs)  # type: ignore
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}") from e

    start_time = time.time()
    asyncio.run(async_crew_execution())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
