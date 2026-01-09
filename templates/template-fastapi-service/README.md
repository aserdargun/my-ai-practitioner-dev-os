# FastAPI ML Service Template

A production-ready template for serving ML models via FastAPI.

## Features

- Health check endpoint
- Model inference endpoint
- Input validation with Pydantic
- Async support
- Docker-ready
- Test suite included

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the service
uvicorn app.main:app --reload

# Run tests
pytest
```

## Project Structure

```
template-fastapi-service/
├── app/
│   └── main.py          # FastAPI application
├── tests/
│   └── test_health.py   # Test suite
├── Dockerfile           # Container definition
├── pyproject.toml       # Dependencies and config
└── README.md            # This file
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Predict
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
```

## Docker Usage

```bash
# Build
docker build -t ml-service .

# Run
docker run -p 8000:8000 ml-service
```

## Customization

1. Replace the mock model in `app/main.py` with your actual model
2. Update the `PredictionInput` schema for your input format
3. Add authentication if needed
4. Configure environment variables for production

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to model file | `./model.pkl` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_health.py -v
```

## Production Checklist

- [ ] Replace mock model with real model
- [ ] Add proper error handling
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Add authentication
- [ ] Configure CORS if needed
- [ ] Set resource limits in Docker
