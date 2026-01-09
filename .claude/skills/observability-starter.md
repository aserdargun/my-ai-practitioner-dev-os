# Skill: Observability Starter

Set up monitoring, logging, and alerting for production services.

## Trigger

Use this skill when:
- Deploying a service to production
- Need visibility into service health
- Debugging production issues
- Setting up SLOs and alerting

## Prerequisites

- Running service (API, pipeline, etc.)
- Access to monitoring tools (Prometheus, Grafana, DataDog, or CloudWatch)
- Basic understanding of metrics and logs
- Production environment access

## Steps

### 1. Define Key Metrics (20 min)

```markdown
## Service Metrics

### The Four Golden Signals
1. **Latency**: How long requests take
2. **Traffic**: How many requests per second
3. **Errors**: Rate of failed requests
4. **Saturation**: How "full" the service is

### Custom Metrics for ML Services
- Prediction latency (p50, p95, p99)
- Model inference time
- Input/output sizes
- Cache hit rate
- Queue depth (if applicable)
```

### 2. Implement Structured Logging (30 min)

```python
# app/logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'latency_ms'):
            log_record['latency_ms'] = record.latency_ms

        return json.dumps(log_record)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger()
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)

    return logger

# Usage
logger = setup_logging()
logger.info("Request processed", extra={
    "request_id": "abc-123",
    "latency_ms": 45
})
```

### 3. Add Prometheus Metrics (30 min)

```python
# app/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

INFERENCE_LATENCY = Histogram(
    'model_inference_duration_seconds',
    'Model inference latency',
    ['model_name'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0]
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

# Decorator for timing
def track_latency(histogram, **labels):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                histogram.labels(**labels).observe(time.time() - start)
        return wrapper
    return decorator

# FastAPI integration
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start = time.time()

    response = await call_next(request)

    latency = time.time() - start
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    ACTIVE_REQUESTS.dec()
    return response

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

### 4. Set Up Health Checks (15 min)

```python
# app/health.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import asyncio

router = APIRouter()

class HealthCheck(BaseModel):
    status: str
    checks: Dict[str, Any]

async def check_database():
    """Check database connectivity"""
    try:
        # Your DB check logic
        await asyncio.sleep(0.1)  # Simulate check
        return {"status": "healthy", "latency_ms": 10}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def check_model():
    """Check model is loaded"""
    try:
        # Your model check logic
        return {"status": "healthy", "model_version": "v1.0"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/health", response_model=HealthCheck)
async def health():
    checks = await asyncio.gather(
        check_database(),
        check_model()
    )

    results = {
        "database": checks[0],
        "model": checks[1]
    }

    overall = "healthy" if all(
        c["status"] == "healthy" for c in checks
    ) else "unhealthy"

    return HealthCheck(status=overall, checks=results)

@router.get("/ready")
async def ready():
    """Kubernetes readiness probe"""
    return {"ready": True}

@router.get("/live")
async def live():
    """Kubernetes liveness probe"""
    return {"live": True}
```

### 5. Configure Alerting Rules (20 min)

```yaml
# prometheus/alerts.yml
groups:
  - name: service_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: Error rate is {{ $value | humanizePercentage }}

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High p95 latency
          description: p95 latency is {{ $value }}s

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: Service is down
```

### 6. Create Dashboards (30 min)

```json
// grafana/dashboard.json (simplified)
{
  "title": "Service Dashboard",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[5m]))",
          "legendFormat": "requests/s"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
          "legendFormat": "error rate"
        }
      ]
    },
    {
      "title": "Latency Percentiles",
      "type": "graph",
      "targets": [
        {
          "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
          "legendFormat": "p50"
        },
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
          "legendFormat": "p95"
        },
        {
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
          "legendFormat": "p99"
        }
      ]
    }
  ]
}
```

### 7. Document Runbook (20 min)

```markdown
# Service Runbook

## Alerts and Response

### HighErrorRate
**Trigger**: Error rate > 5% for 5 minutes

**Investigation**:
1. Check logs for error patterns: `kubectl logs -l app=myservice --tail=100`
2. Check dependent services health
3. Review recent deployments

**Mitigation**:
1. If bad deploy: rollback `kubectl rollout undo deployment/myservice`
2. If dependency issue: check upstream service
3. If overload: scale up `kubectl scale deployment/myservice --replicas=5`

### HighLatency
**Trigger**: p95 latency > 1s for 5 minutes

**Investigation**:
1. Check CPU/memory usage
2. Check database query times
3. Check external API latencies

**Mitigation**:
1. Scale up if CPU-bound
2. Add caching if repeated queries
3. Implement timeouts for external calls
```

## Artifacts Produced

1. **Logging Configuration** — Structured JSON logging
2. **Metrics Endpoint** — Prometheus-compatible `/metrics`
3. **Health Endpoints** — `/health`, `/ready`, `/live`
4. **Alert Rules** — Prometheus alerting configuration
5. **Dashboard** — Grafana dashboard JSON
6. **Runbook** — Incident response documentation

## Quality Bar

Your observability is complete when:

- [ ] Logs are structured JSON
- [ ] Metrics endpoint is exposed
- [ ] Health checks cover dependencies
- [ ] Alert rules are configured
- [ ] Dashboard shows golden signals
- [ ] Runbook documents alert responses
- [ ] Can answer "is the service healthy?" in 30 seconds

## Common Pitfalls

1. **Too many metrics** — Focus on actionable metrics
2. **Alert fatigue** — Tune thresholds to avoid noise
3. **No context in logs** — Include request IDs
4. **Missing labels** — Can't slice by endpoint/status
5. **No runbook** — Team doesn't know how to respond
