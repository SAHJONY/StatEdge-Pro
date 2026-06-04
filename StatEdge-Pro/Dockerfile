# StatEdge Pro - Dockerfile

# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Copy application code
COPY src/ ./src/
COPY main.py .
COPY .env.example .env

# Create data directories
RUN mkdir -p /app/data/chroma

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]