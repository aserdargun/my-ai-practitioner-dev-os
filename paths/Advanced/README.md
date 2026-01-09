# Advanced Learning Dashboard

**Your Level**: Advanced (Tier 1 + Tier 2 + Tier 3)

Welcome to your AI Practitioner Booster 2026 dashboard. This is your main control center for the 12-month learning journey.

---

## Current Position

**Month**: 1 of 12
**Week**: 1 of 4
**Overall Progress**: 0%

[View Tracker](tracker.md) | [View Journal](journal/)

---

## This Month: Foundations & NLP Basics

**Focus**: Python mastery, NLP fundamentals, and sequence models

### Learning Goals
- Master Python and shell scripting for ML workflows
- Understand word embeddings (Word2Vec, GloVe, FastText)
- Build foundation for sequence modeling (RNN, LSTM)
- Create a text processing pipeline

### Deliverables
- [ ] Text preprocessing pipeline with NLTK
- [ ] Word embedding exploration notebook
- [ ] Simple sequence classifier
- [ ] Documentation and tests

[Go to Month 1 →](month-01/README.md)

---

## This Week Plan

Use `/plan-week` to create a detailed plan, or fill in manually:

| Day | Focus | Tasks | Hours |
|-----|-------|-------|-------|
| Mon | Setup | Environment setup, project scaffold | 2 |
| Tue | Learn | Word embeddings theory | 2 |
| Wed | Build | Word2Vec implementation | 3 |
| Thu | Build | Text preprocessing pipeline | 2 |
| Fri | Review | Tests, documentation, retro | 2 |

**Total planned hours**: 11

---

## Commands Cheat-Sheet

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/status` | Quick progress check | Start of day |
| `/plan-week` | Create week plan | Monday |
| `/start-week` | Initialize week | After plan approved |
| `/ship-mvp` | Ship minimal version | When ready to ship |
| `/harden` | Add tests, polish | Before publishing |
| `/publish` | Prepare demo/write-up | End of month |
| `/retro` | Weekly reflection | Friday |
| `/evaluate` | Compute scores | End of week |
| `/adapt-path` | Get path proposals | After evaluation |
| `/add-best-practice` | Capture insight | When you learn |
| `/debug-learning` | Troubleshoot blocks | When stuck |

[Full Commands Guide →](../../docs/commands.md)

---

## Evaluation Snapshot

Run `/evaluate` to get fresh scores.

### How to Interpret

| Score | Status |
|-------|--------|
| 9.0+ | Excellent — Consider level upgrade |
| 7.5-8.9 | Strong — On track |
| 6.5-7.4 | Good — Minor adjustments may help |
| 5.0-6.4 | Needs attention — Consider remediation |
| < 5.0 | At risk — Level downgrade may help |

### Running Evaluation

```bash
python .claude/path-engine/evaluate.py
```

Or use the command:
```
/evaluate
```

---

## If You're Stuck

### Step 1: Identify the Block

What type of block?
- **Knowledge gap**: Missing prerequisite understanding
- **Skill gap**: Know theory, need practice
- **Motivation**: Energy or interest issues
- **Environment**: Tools, time, or setup problems
- **Clarity**: Unclear requirements

### Step 2: Get Help

```
/debug-learning — I'm stuck on [describe the issue]
```

### Step 3: Adjust Plan

If needed:
```
/plan-week — I need to adjust my plan because [reason]
```

### Step 4: Document

When you overcome the block:
```
/add-best-practice — I learned that [insight]
```

---

## Upgrade/Downgrade Rules

### Conditions for Level Change

| Condition | Trigger | Action |
|-----------|---------|--------|
| Consistently high scores | > 9.0 for 2+ months | Propose upgrade |
| Consistently struggling | < 5.0 for 2+ months | Propose downgrade |
| User request | Explicit request | Evaluate and propose |

### What Changes

| Direction | Effect |
|-----------|--------|
| Upgrade to Advanced | Already at Advanced |
| Downgrade to Intermediate | Remove Tier 3 from scope |
| Downgrade to Beginner | Focus on Tier 1 only |

### Level Change Process

1. `/evaluate` shows sustained trend
2. `/adapt-path` proposes level change
3. You review and decide
4. If approved, curriculum adjusts

Level changes only happen at month boundaries (unless you override).

---

## 12-Month Overview

| Month | Focus | Key Technologies |
|-------|-------|------------------|
| [1](month-01/README.md) | NLP Foundations | Word2Vec, GloVe, FastText, NLTK |
| [2](month-02/README.md) | Sequence Models | RNN, LSTM, PyTorch |
| [3](month-03/README.md) | Transformers & LLMs | BERT, GPT, Hugging Face |
| [4](month-04/README.md) | Computer Vision | CNN, YOLO, OpenCV |
| [5](month-05/README.md) | RAG Systems | LangChain, Vector DBs, Embeddings |
| [6](month-06/README.md) | API Development | FastAPI, Docker, CI/CD |
| [7](month-07/README.md) | Data Engineering | Airflow, dbt, Spark |
| [8](month-08/README.md) | MLOps | MLflow, Kubernetes, Monitoring |
| [9](month-09/README.md) | Distributed Systems | Kafka, Event-Driven Architecture |
| [10](month-10/README.md) | Cloud & Scale | Multi-cloud, Scaling Patterns |
| [11](month-11/README.md) | Performance | CUDA, ONNX, TensorRT |
| [12](month-12/README.md) | Advanced ML | GNNs, RL, Federated Learning |

---

## Quick Links

- [How to Use](../../docs/how-to-use.md)
- [Stack Tiers](../../stacks/tiers.md)
- [Commands Reference](../../docs/commands.md)
- [Evaluation Rubric](../../docs/evaluation/rubric.md)
- [Path Engine Report](../../.claude/path-engine/report.py)
- [Best Practices](../../.claude/memory/best_practices.md)

---

## Daily Checklist

- [ ] Check `/status`
- [ ] Work on today's planned tasks
- [ ] Log progress
- [ ] Ask for help if stuck (`/debug-learning`)

## Weekly Checklist

- [ ] Monday: `/plan-week` → `/start-week`
- [ ] Tue-Thu: Build and learn
- [ ] Friday: `/retro` → `/evaluate`

## Monthly Checklist

- [ ] Complete deliverables
- [ ] Run `/harden` for quality
- [ ] Run `/publish` for demo/write-up
- [ ] Run `/evaluate` → `/adapt-path`
- [ ] Start next month

---

*Last updated: Generated by Claude Code*
