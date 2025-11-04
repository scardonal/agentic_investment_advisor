import os

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import TavilyExtractorTool, TavilySearchTool
from dotenv import load_dotenv

from agentic_investment_advisor.models import (
    financial_advisor_llm,
    sentiment_llm,
)
from agentic_investment_advisor.tools.calculator import CalculatorTool

load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

### Prebuilt Tools ###
tavily_tool = TavilySearchTool(api_key=os.getenv("TAVILY_API_KEY", ""), max_results=4)
scrape_tool = TavilyExtractorTool(api_key=os.getenv("TAVILY_API_KEY", ""))


@CrewBase
class AgenticInvestmentAdvisor:
    """AgenticInvestmentAdvisor crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    # ToDo: Add mcp tools to agents as needed
    # ToDo: Create params yaml file for dynamic tasks and LLM parameters

    @agent
    def customer_support_representative(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_support_representative"],  # type: ignore[index]
            verbose=True,
            llm=financial_advisor_llm,
            tools=[tavily_tool, scrape_tool],
            inject_date=True,
        )

    @agent
    def market_data_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_data_researcher"],  # type: ignore[index]
            verbose=True,
            llm=financial_advisor_llm,
            tools=[tavily_tool, scrape_tool, CalculatorTool()],
            allow_delegation=False,
            inject_date=True,
        )

    @agent
    def sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["sentiment_analyst"],  # type: ignore[index]
            verbose=True,
            llm=sentiment_llm,
            tools=[tavily_tool, scrape_tool],
            allow_delegation=False,
            inject_date=True,
        )

    @agent
    def financial_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_advisor"],  # type: ignore[index]
            verbose=True,
            llm=financial_advisor_llm,
            tools=[tavily_tool, scrape_tool, CalculatorTool()],
            allow_delegation=True,
            inject_date=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
        # To learn how to add knowledge sources to your crew, check out the
        # documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
