import os

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.tools import BaseTool
from crewai_tools import TavilyExtractorTool, TavilySearchTool
from dotenv import load_dotenv

from agentic_investment_advisor.llms import (
    financial_advisor_llm,
    sentiment_llm,
)
from agentic_investment_advisor.tools.calculator import CalculatorTool

load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class AgenticInvestmentAdvisor:
    """AgenticInvestmentAdvisor crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # ToDo: Add mcp tools to agents as needed
    # ToDo: Create params yaml file for dynamic tasks and LLM parameters

    @tool
    def search_tool(self) -> BaseTool:
        return TavilySearchTool(api_key=os.getenv("TAVILY_API_KEY", ""), max_results=4)

    @tool
    def scrape_tool(self) -> BaseTool:
        return TavilyExtractorTool(api_key=os.getenv("TAVILY_API_KEY", ""))

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
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
