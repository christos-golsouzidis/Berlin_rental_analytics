# Use Python 3.13 slim image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy pyproject.toml first for better caching
COPY pyproject.toml README.md ./

# Install dependencies located in pyproject.toml using uv
RUN uv sync

# Copy application code
COPY berlin_housing_api.py .
COPY berlin_housing.py .

EXPOSE 12345

# Command to run the application
CMD ["uv", "run", "berlin_housing_api.py"]


