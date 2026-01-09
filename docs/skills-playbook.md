# Skills Playbook

Reusable playbooks for common AI/ML tasks.

---

## Overview

Skills are step-by-step guides for completing specific types of work. Each skill includes:

- **Trigger**: When to use it
- **Steps**: Detailed walkthrough
- **Artifacts**: What you produce
- **Quality bar**: How to know you're done

---

## Available Skills

### All Levels

| Skill | Description |
|-------|-------------|
| [EDA to Insight](../.claude/skills/eda-to-insight.md) | Exploratory data analysis workflow |
| [Baseline Model and Card](../.claude/skills/baseline-model-and-card.md) | Create baseline with documentation |
| [Experiment Plan](../.claude/skills/experiment-plan.md) | Design ML experiments systematically |
| [Forecasting Checklist](../.claude/skills/forecasting-checklist.md) | Time series forecasting workflow |

### Intermediate+

| Skill | Description |
|-------|-------------|
| [RAG with Evals](../.claude/skills/rag-with-evals.md) | Build and evaluate RAG systems |
| [API Shipping Checklist](../.claude/skills/api-shipping-checklist.md) | Deploy production APIs |
| [Observability Starter](../.claude/skills/observability-starter.md) | Set up monitoring and logging |

### Advanced Only

| Skill | Description |
|-------|-------------|
| [K8s Deploy Checklist](../.claude/skills/k8s-deploy-checklist.md) | Kubernetes deployment workflow |

---

## Using Skills

### In Claude Code

Ask Claude to apply a skill:

```
Use the RAG with Evals skill to help me build my retrieval system.
```

### Reference Directly

Point to the skill file:

```
Follow the steps in .claude/skills/api-shipping-checklist.md for my FastAPI service.
```

### With Commands

Skills are often invoked through commands:

```
/ship-mvp  →  Uses api-shipping-checklist
/harden    →  Uses quality bars from relevant skills
```

---

## Skill Summaries

### EDA to Insight

**When**: Starting a new dataset, preparing for ML

**Key Steps**:
1. Load and inspect data
2. Assess data quality
3. Univariate analysis
4. Bivariate analysis
5. Document insights

**Artifacts**: EDA notebook, data quality report, insights document

### Baseline Model and Card

**When**: Starting an ML project, need a benchmark

**Key Steps**:
1. Define the problem
2. Create train/val/test splits
3. Establish trivial baselines
4. Build simple model
5. Write model card

**Artifacts**: Trained model, model card, evaluation report

### Experiment Plan

**When**: Comparing approaches, tuning hyperparameters

**Key Steps**:
1. Define the question
2. Design experiment matrix
3. Set up tracking
4. Run experiments
5. Analyze and document

**Artifacts**: Experiment log, analysis notebook, conclusions

### Forecasting Checklist

**When**: Predicting future time-indexed values

**Key Steps**:
1. Prepare data
2. Visual exploration
3. Train/test split (temporal)
4. Baseline models
5. Statistical/ML models
6. Evaluate and document

**Artifacts**: Clean dataset, model comparison, best model

### RAG with Evals

**When**: Building Q&A or knowledge base systems

**Key Steps**:
1. Prepare documents
2. Create embeddings and index
3. Implement retrieval
4. Implement generation
5. Create golden test set
6. Evaluate retrieval and generation

**Artifacts**: Chunked docs, vector index, golden set, evaluation report

### API Shipping Checklist

**When**: Building production APIs

**Key Steps**:
1. Project structure
2. Core implementation
3. Configuration
4. Testing
5. Docker setup
6. Documentation

**Artifacts**: Working API, test suite, Docker image, README

### Observability Starter

**When**: Deploying to production

**Key Steps**:
1. Define key metrics
2. Implement structured logging
3. Add Prometheus metrics
4. Set up health checks
5. Configure alerting
6. Create dashboards

**Artifacts**: Metrics endpoint, health checks, alerts, dashboard, runbook

### K8s Deploy Checklist

**When**: Deploying to Kubernetes (Advanced only)

**Key Steps**:
1. Create namespace
2. ConfigMap and secrets
3. Deployment manifest
4. Service and ingress
5. HPA and PDB
6. Network policies
7. Deploy and verify

**Artifacts**: K8s manifests, deployment runbook

---

## Quality Bars

Each skill has a quality bar — criteria for knowing you're done.

Example from EDA to Insight:
- [ ] Every column has been examined
- [ ] Missing values are quantified
- [ ] Distributions are understood
- [ ] Key relationships identified
- [ ] Insights written in plain language

Use these checklists to self-evaluate before moving on.

---

## Adding Skills

To add a new skill:

1. Create `.claude/skills/your-skill.md`
2. Follow the template structure
3. Update this playbook
4. Update the skills README

See [.claude/skills/README.md](../.claude/skills/README.md) for details.
