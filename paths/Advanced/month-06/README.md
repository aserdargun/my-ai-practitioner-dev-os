# Month 06 — API Development

Build and deploy production-ready APIs.

---

## Why It Matters

APIs are how AI models get into production. Knowing how to build robust, well-tested, containerized APIs is essential for any ML engineer. This month bridges the gap between "model in a notebook" and "model in production."

---

## Prerequisites

- Python proficiency
- Basic understanding of HTTP/REST
- Some Docker experience (or willingness to learn)
- Understanding of software testing

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 1 Focus
- **Flask/Django**: Web framework fundamentals
- **GraphQL**: Query language for APIs

### Tier 2 Focus
- **FastAPI**: Modern async Python API framework
- **Docker**: Containerization
- **CI/CD**: GitHub Actions, automated testing
- **PostgreSQL**: Production database

### Concepts
- REST API design principles
- Request/response validation
- Authentication and authorization
- Error handling
- API documentation (OpenAPI)
- Container best practices

---

## Main Project: ML Model API Service

Build a production-ready API serving an ML model.

### Deliverables

1. **FastAPI Service**
   - Model serving endpoint
   - Health checks
   - Input validation
   - Error handling

2. **Docker Container**
   - Multi-stage build
   - Security best practices
   - Optimized image size

3. **CI/CD Pipeline**
   - Automated testing
   - Linting and formatting
   - Docker build and push
   - Deployment automation

4. **Documentation**
   - API documentation (auto-generated)
   - Deployment guide
   - Architecture diagram

### Definition of Done

- [ ] API serves model predictions correctly
- [ ] All endpoints have validation and error handling
- [ ] Docker image builds and runs
- [ ] CI pipeline passes on every PR
- [ ] API docs accessible at /docs
- [ ] Health endpoint works for monitoring

---

## Stretch Goals

- [ ] Add GraphQL endpoint alongside REST
- [ ] Implement rate limiting
- [ ] Add authentication (JWT)
- [ ] Blue-green deployment setup
- [ ] Load testing with results

---

## Weekly Breakdown

### Week 1: FastAPI Fundamentals
- Project structure
- Endpoints and routing
- Pydantic models
- Request validation

### Week 2: Model Integration
- Loading ML model
- Prediction endpoint
- Batch predictions
- Error handling

### Week 3: Docker & Database
- Dockerfile creation
- Multi-stage builds
- PostgreSQL integration
- Environment configuration

### Week 4: CI/CD & Polish
- GitHub Actions setup
- Automated testing
- Documentation
- Demo and write-up

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 6 focusing on API development. Help me plan a week building a FastAPI service.
```

### Building
```
As the Builder agent, help me structure a FastAPI project for serving an ML model. Use best practices.
```

### Skill Usage
```
Use the API Shipping Checklist skill to guide my production API development.
```

### Docker Help
```
As the Builder, help me create an optimized Dockerfile for my FastAPI ML service.
```

### CI/CD
```
As the Builder, help me set up GitHub Actions for testing and building my Docker image.
```

---

## How to Publish

### Demo
- Live API queries with curl/Postman
- Docker container startup
- CI/CD pipeline run
- API documentation tour

### Write-up Topics
- FastAPI vs Flask for ML
- Docker best practices for ML
- CI/CD for ML projects
- API design patterns

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Docs](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

### Templates
- Use `templates/template-fastapi-service/` in this repo

### Best Practices
- 12-Factor App methodology
- REST API design guidelines
- Container security practices

---

## Next Month Preview

**Month 07**: Data Engineering — Building data pipelines with Airflow, dbt, and Spark.
