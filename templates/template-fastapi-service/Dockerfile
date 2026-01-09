# Multi-stage build for production ML service

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir build

# Copy project files
COPY pyproject.toml .
COPY app/ app/

# Build wheel
RUN python -m build --wheel

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy wheel from builder
COPY --from=builder /app/dist/*.whl .

# Install the package
RUN pip install --no-cache-dir *.whl && rm *.whl

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
