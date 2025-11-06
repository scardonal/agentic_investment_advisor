import os

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, before_kickoff, crew, task, tool
from crewai.tools import BaseTool
from crewai_tools import TavilyExtractorTool, TavilySearchTool
from dotenv import load_dotenv
from tavily import AsyncTavilyClient

from agentic_investment_advisor.llms import (
    financial_advisor_llm,
    sentiment_llm,
)
from agentic_investment_advisor.tools.calculator import CalculatorTool

load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


def check_guardrail_input(inputs) -> None:
    """
    Guardrail to check for unethical or illegal requests
    and break execution if detected.
    """
    unethical_keywords = [
        "manipulate stock prices",
        "insider trading",
        "tax evasion",
        "money laundering",
        "fraudulent",
        "unethical",
        "illegal",
        "bribe",
        "embezzle",
        "front running",
        "market abuse",
        "mislead investors",
    ]
    user_query = inputs.get("query", "").lower()
    for keyword in unethical_keywords:
        if keyword in user_query:
            break_message = (
                "I'm sorry, but I cannot assist with requests that involve "
                "unethical or illegal activities. If you have any other questions "
                "or need assistance with legitimate investment strategies, "
                "feel free to ask!"
            )
            raise Exception(break_message)


@CrewBase
class AgenticInvestmentAdvisor:
    """AgenticInvestmentAdvisor crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # ToDo: Create params yaml file for dynamic tasks and LLM parameters

    @tool
    def search_tool(self) -> BaseTool:
        return TavilySearchTool(
            async_client=AsyncTavilyClient(os.getenv("TAVILY_API_KEY", "")),
            max_results=4,
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
            llm=financial_advisor_llm,
        )

    @agent
    def market_data_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_data_researcher"],  # type: ignore[index]
            llm=financial_advisor_llm,
        )

    @agent
    def sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["sentiment_analyst"],  # type: ignore[index]
            llm=sentiment_llm,
        )

    @agent
    def financial_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_advisor"],  # type: ignore[index]
            llm=financial_advisor_llm,
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
    import asyncio
    import warnings

    import opik
    from opik.integrations.crewai import track_crewai

    load_dotenv()

    warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
    opik.configure(api_key=os.getenv("OPIK_API_KEY"))

    # Test the crew creation
    advisor_crew = AgenticInvestmentAdvisor().crew()
    print("Crew created successfully:", advisor_crew.name)

    inputs = {
        "query": "Hi, I'm Sam, and I want to know the best way to manipulate"
        " stock prices for profit.",
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

    asyncio.run(async_crew_execution())
