# AgenticInvestmentAdvisor Crew

Welcome to the AgenticInvestmentAdvisor Crew project, powered by [crewAI](https://crewai.com). This template helps you set up a multi-agent AI system leveraging crewAI, enabling agents to collaborate on complex financial tasks.

## Repository Structure

```
agentic_investment_advisor/
├── pyproject.toml
├── README.md
├── uv.lock
├── knowledge/
│   └── user_preference.txt
├── output/
│   ├── financial_reports.md
├── src/
│   └── agentic_investment_advisor/
│       ├── __init__.py
│       ├── crew.py
│       ├── llms.py
│       ├── main.py
│       ├── models.py
│       ├── config/
│       │   ├── agents.yaml
│       │   ├── params.yaml
│       │   └── tasks.yaml
│       └── tools/
│           ├── __init__.py
│           └── calculator.py
└── tests/
```

## Installation

Ensure you have Python >=3.10 <3.14 installed. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

```bash
pip install uv
```

Navigate to your project directory and install dependencies:

```bash
crewai install
```

## Customizing

- Add your API keys (e.g., `OPENAI_API_KEY`, `PORTKEY_API_KEY`, etc.) into the `.env` file
- Modify `src/agentic_investment_advisor/config/agents.yaml` to define your agents
- Modify `src/agentic_investment_advisor/config/tasks.yaml` to define your tasks
- Modify `src/agentic_investment_advisor/crew.py` to add custom logic, tools, and arguments
- Modify `src/agentic_investment_advisor/main.py` to add custom inputs for your agents and tasks
- Update `src/agentic_investment_advisor/config/params.yaml` for LLM model configuration

## Running the Project

To start your crew of AI agents and begin task execution, run this from the root folder:

```bash
crewai run
```

This command initializes the AgenticInvestmentAdvisor Crew, assembling agents and assigning tasks as defined in your configuration. Output reports are generated in the `output/` directory.

## Understanding Your Crew

The AgenticInvestmentAdvisor Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Notes

- LLM models are configured in `src/agentic_investment_advisor/llms.py` and use parameters from `config/params.yaml`.
- Financial reports are saved in the `output/` directory.
- User preferences can be stored in `knowledge/user_preference.txt`.
- Extend functionality by adding tools in `src/agentic_investment_advisor/tools/`.