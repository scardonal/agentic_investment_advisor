# Agentic Investment Advisor

Welcome to the Agentic Investment Advisor, a sophisticated multi-agent AI system powered by [crewAI](https://crewai.com). This application leverages a team of specialized AI agents that collaborate to provide comprehensive investment recommendations based on financial data analysis, market sentiment, and user preferences.

## Key Features

- **Multi-Agent Collaboration**: Specialized agents work together to analyze financial data and provide investment recommendations
- **Financial Data Analysis**: Comprehensive analysis of quantitative financial data and market trends
- **Market Sentiment Analysis**: Evaluation of news, social media, and public perception of securities
- **User Profile Extraction**: Intelligent inference of user financial goals and risk tolerance
- **Detailed Investment Reports**: Generation of comprehensive reports with clear recommendations
- **FastAPI REST Interface**: Easy-to-use API for integrating with other applications
- **Docker Support**: Simple deployment using Docker containers

## System Architecture

The Agentic Investment Advisor consists of four specialized agents that work together in a sequential workflow:

1. **Customer Support Representative**: Extracts user financial goals, risk profile, and potential securities of interest
2. **Financial Data Researcher**: Analyzes quantitative financial data and trends for the identified securities
3. **Market Sentiment Analyst**: Researches financial news, rumors, and social media sentiment
4. **Investment Advisor**: Creates detailed reports with clear recommendations based on all gathered information

These agents utilize various tools:
- Web Search (Tavily)
- Web Scraper (Tavily)
- Calculator (for financial calculations)

## Installation

### Prerequisites

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) for dependency management
- API keys for required services (see Configuration section)

### Standard Installation

1. Install UV:
```bash
pip install uv
```

2. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/yourusername/agentic_investment_advisor.git
cd agentic_investment_advisor
```

3. Install dependencies:
```bash
uv pip install -e .
```

### Docker Installation

1. Ensure Docker and Docker Compose are installed on your system

2. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic_investment_advisor.git
cd agentic_investment_advisor
```

3. Create a `.env` file with your API keys (see Configuration section)

4. Build and run the Docker container:
```bash
docker-compose up --build
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
PORTKEY_URL=https://api.portkey.com/v1
PORTKEY_API_KEY=your_api_key_here

OPIK_API_KEY=your_opik_api_key_here
OPIK_PROJECT_NAME=your_opik_project_name_here

TAVILY_API_KEY=your_tavily_api_key_here

CREW_TIMEOUT=780
```

### Configuration Files

The application uses YAML configuration files located in `src/agentic_investment_advisor/config/`:

- `agents.yaml`: Defines agent roles, goals, and capabilities
- `tasks.yaml`: Specifies tasks for each agent and their workflow
- `params.yaml`: Contains LLM model configurations and other parameters

## Usage

### Running Locally

Start the FastAPI application:

```bash
python -m agentic_investment_advisor.main
```

The API will be available at http://localhost:8000

### Using Docker

Start the container:

```bash
docker-compose up
```

Access the API at http://localhost:8000

### API Endpoints

#### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status":"healthy","timestamp":"2025-11-10T22:07:11.221761"}
```

#### Run Investment Advisor

```bash
curl -X POST http://localhost:8000/crew/run \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Compare SPY and QQQ for long-term growth"}'
```

Response:
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-11-10T22:10:15.123456",
  "processing_time_ms": 45678.9,
  "result": "# Investment Analysis: SPY vs QQQ for Long-Term Growth\n\n## Executive Summary\n\n[Detailed investment report content...]"
}
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Agentic System

![Agentic Investment Advisor Architecture](Agentic%20Advisor.png)

1. **User Query Processing**:
   - The Customer Support Representative agent extracts the user's financial goals, risk profile, and potential securities of interest from the query.

2. **Parallel Research**:
   - The Financial Data Researcher analyzes quantitative financial data for the identified securities.
   - The Market Sentiment Analyst researches news and social media sentiment related to these securities.

3. **Investment Recommendation**:
   - The Investment Advisor synthesizes all gathered information and creates a detailed report with clear recommendations.

4. **Report Generation**:
   - A comprehensive investment report is generated in markdown format and saved to the `output/` directory.

## Project Structure

```
agentic_investment_advisor/
├── pyproject.toml         # Project dependencies and configuration
├── README.md              # This file
├── uv.lock                # UV dependency lock file
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── knowledge/             # Knowledge base files
│   └── user_preference.txt
├── output/                # Generated reports
│   ├── financial_reports.md
├── src/
│   └── agentic_investment_advisor/
│       ├── __init__.py
│       ├── crew.py        # Main crew definition
│       ├── llms.py        # LLM configurations
│       ├── main.py        # FastAPI application
│       ├── config/        # Configuration files
│       │   ├── agents.yaml
│       │   ├── params.yaml
│       │   └── tasks.yaml
│       └── tools/         # Custom tools
│           ├── __init__.py
│           └── calculator.py
└── tests/                 # Test files
```

## Docker Details

The Docker setup includes:

- Python 3.12 base image
- Installation of build dependencies and UV
- Configuration of necessary directories
- Exposure of port 8000 for the FastAPI application
- Volume mounts for logs, output, and knowledge directories
- Environment variable configuration via .env file

## Development

### Adding New Tools

1. Create a new tool in `src/agentic_investment_advisor/tools/`
2. Implement the tool following the BaseTool interface from crewAI
3. Register the tool in `crew.py`
4. Update agent configurations in `agents.yaml` to use the new tool

### Customizing Agents

Modify the `agents.yaml` file to:
- Change agent roles and goals
- Adjust agent backstories
- Configure which LLM each agent uses
- Assign tools to specific agents

### Customizing Tasks

Modify the `tasks.yaml` file to:
- Define new tasks
- Change task descriptions and expected outputs
- Configure task dependencies and context
- Adjust task execution flow
