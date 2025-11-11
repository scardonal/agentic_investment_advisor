# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install build dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Create necessary directories
RUN mkdir -p logs output knowledge

# Install dependencies using uv
RUN uv pip install --system -r pyproject.toml .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "agentic_investment_advisor.main"]
