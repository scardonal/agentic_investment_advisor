import os
import warnings

from fastapi import FastAPI
from opik.integrations.crewai import track_crewai
from pydantic import BaseModel

from agentic_investment_advisor.crew import (
    AgenticInvestmentAdvisor,
    check_guardrail_input,
)


class Query(BaseModel):
    user_query: str


app = FastAPI()


@app.post("/crew/run")
async def run_crew(query: Query):
    user_query = query.user_query
    inputs = {"query": user_query}
    try:
        check_guardrail_input(inputs)
    except Exception as e:
        return {"error": str(e)}
    try:
        advisor_crew = AgenticInvestmentAdvisor().crew()
        track_crewai(project_name=os.getenv("OPIK_PROJECT_NAME"))
        result = await advisor_crew.kickoff_async(inputs=inputs)
        return {"result": result.raw}
    except Exception as e:
        return {"error": f"An error occurred while running the crew: {e}"}


if __name__ == "__main__":
    import uvicorn

    warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
    uvicorn.run(
        "agentic_investment_advisor.main:app", host="0.0.0.0", port=8000, reload=True
    )
