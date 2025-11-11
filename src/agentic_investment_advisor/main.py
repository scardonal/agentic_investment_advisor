"""
Agentic Investment Advisor API

This module implements a FastAPI-based REST API that serves as the interface to the
Agentic Investment Advisor system. The API allows users to submit investment queries
which are processed by an AI-powered crew of specialized agents that analyze financial
data and provide investment recommendations.

The API includes input validation, error handling, and logging to ensure
reliable and secure operation.
"""

# Standard library imports
import asyncio
import logging
import os
import time
import uuid
import warnings
from datetime import datetime
from typing import Any

from dotenv import load_dotenv

# Third-party imports
from fastapi import Body, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from opik.integrations.crewai import track_crewai
from pydantic import BaseModel, Field, field_validator

# Local application imports
from agentic_investment_advisor.crew import (
    AgenticInvestmentAdvisor,
    check_guardrail_input,
)

load_dotenv()

# Define module-level constants for FastAPI Body configurations
QUERY_BODY = Body(
    ..., example={"user_query": "Compare SPY and QQQ for long-term growth"}
)

# Configure logging to output to both file and console
# This ensures we have persistent logs for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/api.log"), logging.StreamHandler()],
)
logger = logging.getLogger("agentic_investment_advisor")


# Pydantic models for request validation, error handling, and response formatting


class Query(BaseModel):
    """
    Represents a user investment query.

    This model validates that the query meets minimum requirements:
    - Not empty
    - Between 3 and 1000 characters
    """

    user_query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The user's investment query or request",
    )

    @field_validator("user_query", mode="after")
    def validate_query(cls, v):
        """Ensure the query isn't just whitespace"""
        if v.strip() == "":
            raise ValueError("Query cannot be empty")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {"user_query": "Compare SPY and QQQ for long-term growth"}
        }
    }


class ErrorDetail(BaseModel):
    """
    Structured error information for API responses.

    Attributes:
        type: The category or type of error
        message: A human-readable error description
    """

    type: str
    message: str


class ResponseModel(BaseModel):
    """
    Standardized API response format.

    Attributes:
        request_id: Unique identifier for the request for tracking
        timestamp: When the response was generated
        processing_time_ms: How long the request took to process
        result: The successful response data (if no error)
        error: Error details (if an error occurred)
    """

    request_id: str
    timestamp: datetime
    processing_time_ms: float
    result: Any | None = None
    error: ErrorDetail | None = None


# Initialize FastAPI with documentation endpoints
# This configures the API server and enables automatic OpenAPI documentation
app = FastAPI(
    title="Agentic Investment Advisor API",
    description="API for interacting with an AI-powered investment advisor crew",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc",  # ReDoc documentation
)


# Exception handlers for graceful error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc) -> JSONResponse:
    """
    Handle validation errors from request parsing.

    This provides a consistent error response format when request data
    doesn't match the expected schema.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "details": str(exc)},
    )


# API endpoints
@app.post(
    "/crew/run",
    response_model=ResponseModel,
    summary="Run the investment advisor crew",
    description="""
    Process a user query through the Agentic Investment Advisor crew.
    The crew analyzes the query, researches relevant financial data,
    and provides investment recommendations.
    """,
    response_description="Investment advice and analysis based on the user query",
    tags=["Crew Operations"],
)
async def run_crew(query: Query = QUERY_BODY) -> ResponseModel:
    """
    Main endpoint for processing investment queries.

    This function:
    1. Validates the incoming query
    2. Checks guardrails to prevent misuse
    3. Initializes and runs the AI advisor crew
    4. Handles timeouts and errors
    5. Returns structured results

    The function includes detailed logging for monitoring and debugging.
    """
    # Generate unique ID for request tracking
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Log the incoming request (truncated to avoid excessive logging)
    logger.info(f"Request {request_id}: Processing query: {query.user_query[:50]}...")

    # Prepare input for the crew
    user_query = query.user_query
    inputs = {"query": user_query}

    # Check guardrails to prevent misuse or harmful queries
    try:
        check_guardrail_input(inputs)
    except Exception as e:
        # If guardrail check fails, return error without processing
        error_msg = str(e)
        logger.warning(f"Request {request_id}: Guardrail check failed - {error_msg}")

        processing_time = (time.time() - start_time) * 1000
        return ResponseModel(
            request_id=request_id,
            timestamp=datetime.now(),
            processing_time_ms=processing_time,
            error=ErrorDetail(type="guardrail_violation", message=error_msg),
        )

    # Process the query with the AI crew
    try:
        # Initialize the investment advisor crew
        advisor_crew = AgenticInvestmentAdvisor().crew()

        # Enable tracking for analytics if configured
        track_crewai(project_name=os.getenv("OPIK_PROJECT_NAME"))

        # Run the crew with a configurable timeout to prevent hanging requests
        result = await asyncio.wait_for(
            advisor_crew.kickoff_async(inputs=inputs),
            timeout=float(os.getenv("CREW_TIMEOUT", "780.0")),
        )

        # Calculate processing time and log success
        processing_time = (time.time() - start_time) * 1000
        logger.info(
            f"Request {request_id}: Processing completed in {processing_time:.2f}ms"
        )

        # Return successful response with results
        return ResponseModel(
            request_id=request_id,
            timestamp=datetime.now(),
            processing_time_ms=processing_time,
            result=result.raw,
        )
    except asyncio.TimeoutError:
        # Handle timeout case
        processing_time = (time.time() - start_time) * 1000
        logger.error(
            f"Request {request_id}: Processing timed out after {processing_time:.2f}ms"
        )

        return ResponseModel(
            request_id=request_id,
            timestamp=datetime.now(),
            processing_time_ms=processing_time,
            error=ErrorDetail(
                type="timeout_error", message="The request took too long to process"
            ),
        )
    except Exception as e:
        # Handle any other exceptions
        error_msg = str(e)
        processing_time = (time.time() - start_time) * 1000
        logger.error(f"Request {request_id}: Processing error - {error_msg}")

        return ResponseModel(
            request_id=request_id,
            timestamp=datetime.now(),
            processing_time_ms=processing_time,
            error=ErrorDetail(
                type="processing_error",
                message=f"An error occurred while running the crew: {error_msg}",
            ),
        )


# Health check endpoint for monitoring and infrastructure integration
@app.get(
    "/health",
    summary="API health check",
    description="Check if the API is running properly",
    tags=["System"],
)
async def health_check():
    """
    Simple endpoint to verify the API is operational.

    This is used by monitoring systems, load balancers, and container orchestration
    platforms to determine if the service is healthy.
    """
    return {"status": "healthy", "timestamp": datetime.now()}


if __name__ == "__main__":
    """
    Entry point when running the module directly.

    This allows the API to be started with `python -m agentic_investment_advisor.main`
    and configures the uvicorn ASGI server with appropriate settings.
    """
    import uvicorn

    # Suppress known warnings from dependencies
    warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

    # Start the uvicorn ASGI server
    uvicorn.run(
        "agentic_investment_advisor.main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=int(os.getenv("PORT", "8000")),  # Use PORT env var or default to 8000
        reload=True,  # Enable auto-reload during development
    )
