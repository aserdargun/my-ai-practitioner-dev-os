# Skills

This folder contains reusable playbooks for common AI/ML tasks. Each skill is a structured guide that helps you complete specific types of work.

## Overview

Skills are like recipes—step-by-step guides for accomplishing common tasks. They include:

- **Trigger**: When to use this skill
- **Prerequisites**: What you need before starting
- **Steps**: Detailed walkthrough
- **Artifacts**: What you produce
- **Quality Bar**: How to know you're done

## Available Skills

| Skill | Description | Tier |
|-------|-------------|------|
| [EDA to Insight](eda-to-insight.md) | Exploratory data analysis workflow | All |
| [Baseline Model and Card](baseline-model-and-card.md) | Create a baseline model with documentation | All |
| [Experiment Plan](experiment-plan.md) | Design ML experiments systematically | All |
| [Forecasting Checklist](forecasting-checklist.md) | Time series forecasting workflow | All |
| [RAG with Evals](rag-with-evals.md) | Build and evaluate RAG systems | Intermediate+ |
| [API Shipping Checklist](api-shipping-checklist.md) | Deploy production APIs | Intermediate+ |
| [Observability Starter](observability-starter.md) | Set up monitoring and logging | Intermediate+ |
| [K8s Deploy Checklist](k8s-deploy-checklist.md) | Kubernetes deployment workflow | **Advanced only** |

## Using Skills

### In Claude Code

Ask Claude to apply a skill:

```
Use the RAG with Evals skill to help me build my retrieval system.
```

Or reference directly:

```
Follow the steps in .claude/skills/api-shipping-checklist.md for deploying my FastAPI service.
```

### With Commands

Skills are often invoked through commands:

| Command | Uses Skills |
|---------|-------------|
| `/ship-mvp` | api-shipping-checklist, relevant domain skill |
| `/harden` | Quality bars from all relevant skills |
| `/evaluate` | Completion criteria from skills |

## Skill Structure

Each skill file follows this format:

```markdown
# Skill: [Name]

## Trigger
When to use this skill

## Prerequisites
What you need before starting

## Steps
1. Step one
2. Step two
...

## Artifacts Produced
- Artifact 1
- Artifact 2

## Quality Bar
How to know you're done

## Common Pitfalls
What to avoid

## Examples
Sample outputs or code
```

## Adding New Skills

To add a new skill:

1. Create a new `.md` file in this folder
2. Follow the skill structure template
3. Update this README
4. Update `docs/skills-playbook.md`

## Tier Restrictions

Some skills are gated by learner level:

- **All levels**: EDA, baseline model, experiment plan, forecasting
- **Intermediate+**: RAG, API shipping, observability
- **Advanced only**: Kubernetes deployment

These restrictions are documented in each skill and enforced through curriculum design.
