# Docker Setup for Agentic Investment Advisor

This document provides instructions for running the Agentic Investment Advisor application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system
- A valid `.env` file with the required API keys

## Environment Variables

The application requires the following environment variables to be set in your `.env` file:

```
PORTKEY_URL=https://api.portkey.com/v1
PORTKEY_API_KEY=your_api_key_here

OPIK_API_KEY=your_opik_api_key_here
OPIK_PROJECT_NAME=your_opik_project_name_here

TAVILY_API_KEY=your_tavily_api_key_here

CREW_TIMEOUT=780
```

Make sure your `.env` file is in the root directory of the project.

## Building and Running the Container

### Using Docker Compose (Recommended)

1. Build and start the container:

```bash
docker-compose up --build
```

2. To run in detached mode (in the background):

```bash
docker-compose up --build -d
```

3. To stop the container:

```bash
docker-compose down
```

### Using Docker CLI

1. Build the Docker image:

```bash
docker build -t agentic-investment-advisor .
```

2. Run the container:

```bash
docker run -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/knowledge:/app/knowledge \
  -v $(pwd)/.env:/app/.env \
  agentic-investment-advisor
```

## Accessing the Application

Once the container is running, you can access:

- FastAPI application: http://localhost:8000
- API documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Health Check

You can verify the application is running correctly by accessing the health check endpoint:

```bash
curl http://localhost:8000/health
```

## Using the API

To use the investment advisor API, send a POST request to the `/crew/run` endpoint:

```bash
curl -X POST http://localhost:8000/crew/run \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Compare SPY and QQQ for long-term growth"}'
```

## Volumes

The Docker setup mounts the following volumes:

- `./logs:/app/logs`: For application logs
- `./output:/app/output`: For output files
- `./knowledge:/app/knowledge`: For knowledge base files
- `./.env:/app/.env`: For environment variables

This ensures that data persists between container restarts and is accessible from the host system.
