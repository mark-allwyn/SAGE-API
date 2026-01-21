FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Copy application code
COPY . .

# Install dependencies (no dev dependencies for production)
RUN uv sync --frozen --no-dev

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "sage.main:app", "--host", "0.0.0.0", "--port", "8000"]
