# Skill: API Shipping Checklist

Ship production-ready APIs with proper structure, documentation, testing, and deployment.

## Trigger

Use this skill when:
- Building a REST or GraphQL API
- Preparing a service for production deployment
- Need to expose ML models or data services
- Creating microservices

## Prerequisites

- Python with FastAPI (or Flask/Django)
- Docker installed
- Basic understanding of HTTP/REST
- Database or model ready to serve

## Steps

### 1. Project Structure (15 min)

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── models.py         # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints.py
│   └── services/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_endpoints.py
├── Dockerfile
├── pyproject.toml
├── README.md
└── .env.example
```

### 2. Core Implementation (30 min)

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="My API",
    description="API for serving predictions",
    version="1.0.0",
    lifespan=lifespan
)

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Include routers
from app.routes.v1 import router as v1_router
app.include_router(v1_router, prefix="/v1")
```

```python
# app/models.py
from pydantic import BaseModel, Field
from typing import Optional

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    options: Optional[dict] = None

    model_config = {"json_schema_extra": {
        "example": {
            "text": "Sample input text",
            "options": {"temperature": 0.7}
        }
    }}

class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    metadata: dict
```

```python
# app/routes/v1/endpoints.py
from fastapi import APIRouter, HTTPException
from app.models import PredictRequest, PredictResponse
from app.services.core import predict

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def make_prediction(request: PredictRequest):
    try:
        result = await predict(request.text, request.options)
        return PredictResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 3. Configuration (15 min)

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "My API"
    debug: bool = False
    model_path: str = "models/v1"
    max_batch_size: int = 32
    api_key: str = ""  # For authentication

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

```bash
# .env.example
APP_NAME=My API
DEBUG=false
MODEL_PATH=models/v1
MAX_BATCH_SIZE=32
API_KEY=your-secret-key
```

### 4. Testing (30 min)

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_request():
    return {"text": "Test input"}
```

```python
# tests/test_endpoints.py
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_success(client, sample_request):
    response = client.post("/v1/predict", json=sample_request)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data

def test_predict_empty_text(client):
    response = client.post("/v1/predict", json={"text": ""})
    assert response.status_code == 422  # Validation error

def test_predict_missing_text(client):
    response = client.post("/v1/predict", json={})
    assert response.status_code == 422
```

### 5. Docker Setup (20 min)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application
COPY app/ app/

# Create non-root user
RUN useradd --create-home appuser
USER appuser

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```toml
# pyproject.toml
[project]
name = "my-api"
version = "1.0.0"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.22.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "httpx>=0.24.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### 6. Documentation (15 min)

```markdown
# README.md

## My API

REST API for serving predictions.

### Quick Start

```bash
# Install
pip install -e ".[dev]"

# Run locally
uvicorn app.main:app --reload

# Run tests
pytest

# Build Docker
docker build -t my-api .
docker run -p 8000:8000 my-api
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /v1/predict | Make prediction |

### Environment Variables

See `.env.example` for configuration options.
```

### 7. Pre-Deploy Checklist (15 min)

```markdown
## Pre-Deploy Checklist

### Code Quality
- [ ] All tests passing (`pytest`)
- [ ] Linting clean (`ruff check .`)
- [ ] Type hints on public functions
- [ ] Docstrings on endpoints

### Security
- [ ] No secrets in code
- [ ] Input validation on all endpoints
- [ ] Rate limiting configured (if needed)
- [ ] CORS configured properly
- [ ] Authentication in place (if needed)

### Operations
- [ ] Health endpoint works
- [ ] Logging configured
- [ ] Error handling returns safe messages
- [ ] Docker builds successfully
- [ ] Docker runs and health check passes

### Documentation
- [ ] README updated
- [ ] API docs accessible
- [ ] Example requests documented
- [ ] Environment variables documented
```

## Artifacts Produced

1. **Working API** — FastAPI application
2. **Test Suite** — pytest tests with coverage
3. **Docker Image** — Production container
4. **Documentation** — README + OpenAPI specs
5. **Configuration** — Environment-based settings

## Quality Bar

Your API is ready to ship when:

- [ ] All tests pass
- [ ] Health endpoint returns 200
- [ ] Error responses are consistent
- [ ] Docker image builds and runs
- [ ] API docs are accessible
- [ ] No secrets in code
- [ ] Logging is in place
- [ ] Response times are acceptable

## Common Pitfalls

1. **No health check** — Can't monitor service status
2. **Secrets in code** — Use environment variables
3. **No input validation** — Security vulnerability
4. **Inconsistent errors** — Hard to debug
5. **No versioning** — Breaking changes for clients
