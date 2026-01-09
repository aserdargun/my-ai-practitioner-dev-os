# Month 08 — MLOps

Build production ML systems with proper operations.

---

## Why It Matters

MLOps bridges the gap between ML experiments and production systems. Companies need engineers who can deploy, monitor, and maintain ML models at scale. This month covers the full lifecycle from training to production operations.

---

## Prerequisites

- Month 07: Data Engineering (Airflow, pipelines)
- Month 06: API Development (Docker, CI/CD)
- Kubernetes basics (or willingness to learn)
- Understanding of ML model training

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 2 Focus
- **MLflow**: Experiment tracking and model registry
- **Docker**: Containerization for ML
- **Prometheus/Grafana**: Monitoring stack
- **Datadog/CloudWatch**: Cloud monitoring

### Tier 3 Focus
- **Kubernetes**: Container orchestration
- **Kubeflow**: ML on Kubernetes
- **AKS/ECS**: Managed container services

### Concepts
- ML lifecycle management
- Model versioning and registry
- Feature stores
- A/B testing for models
- Model monitoring and drift detection
- Automated retraining

---

## Main Project: Production ML Platform

Deploy a complete ML system with monitoring.

### Deliverables

1. **Model Training Pipeline**
   - Reproducible training
   - Hyperparameter tracking
   - Model versioning
   - Automated evaluation

2. **Model Serving**
   - Kubernetes deployment
   - Auto-scaling configuration
   - Health checks
   - Canary deployments

3. **Monitoring Dashboard**
   - Prometheus metrics
   - Grafana dashboards
   - Alerting rules
   - Model performance tracking

4. **CI/CD for ML**
   - Automated testing
   - Model validation gates
   - Deployment automation
   - Rollback procedures

### Definition of Done

- [ ] Model deploys to Kubernetes automatically
- [ ] Prometheus collects prediction metrics
- [ ] Grafana shows real-time performance
- [ ] Alerts fire on model degradation
- [ ] CI/CD pipeline validates model before deploy
- [ ] Documentation covers operational runbook

---

## Stretch Goals

- [ ] Implement feature store
- [ ] Add A/B testing framework
- [ ] Build automated retraining trigger
- [ ] Deploy to multiple clouds (AKS + ECS)
- [ ] Add Kubeflow pipelines

---

## Weekly Breakdown

### Week 1: MLflow Deep Dive
- Experiment tracking
- Model registry
- Model serving
- Integration patterns

### Week 2: Kubernetes for ML
- K8s fundamentals
- Deploying ML models
- Resource management
- Auto-scaling

### Week 3: Monitoring Stack
- Prometheus setup
- Custom metrics
- Grafana dashboards
- Alerting

### Week 4: Production Operations
- CI/CD for ML
- Canary deployments
- Incident response
- Documentation

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 8 focusing on MLOps. Help me plan a week setting up Kubernetes and model serving.
```

### Building
```
As the Builder agent, help me create a Kubernetes deployment for my ML model with proper health checks and auto-scaling.
```

### Skill Usage
```
Use the K8s Deploy Checklist skill to guide my production Kubernetes deployment.
```

### Monitoring
```
As the Builder, help me set up Prometheus and Grafana for monitoring ML model predictions. Include custom metrics.
```

### Observability
```
Use the Observability Starter skill to help me implement comprehensive monitoring for my ML system.
```

---

## How to Publish

### Demo
- Kubernetes deployment in action
- Grafana dashboards with live metrics
- CI/CD pipeline run
- Canary deployment demo

### Write-up Topics
- Why MLOps matters
- Kubernetes for ML engineers
- Model monitoring best practices
- CI/CD for ML systems

---

## Resources

### Documentation
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Kubeflow Docs](https://www.kubeflow.org/docs/)
- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)

### Books
- "Designing Machine Learning Systems" by Chip Huyen
- "Reliable Machine Learning" by Cathy Chen et al.

### Tools
- kubectl, helm
- MLflow 2.x
- Prometheus + Grafana
- GitHub Actions for ML

---

## Next Month Preview

**Month 09**: Distributed Systems — Event-driven architectures with Kafka, message queues, and real-time processing.
