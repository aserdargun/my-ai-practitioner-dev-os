# Portfolio Checklist

Ensure your projects are portfolio-ready.

---

## Overview

A portfolio-ready project:
- Works as documented
- Has clear documentation
- Shows your skills
- Is easy to explore

---

## Repository Checklist

### README

- [ ] **Title and description** — What it is in one sentence
- [ ] **Problem statement** — What problem it solves
- [ ] **Features** — Key capabilities
- [ ] **Demo** — Screenshot, GIF, or video link
- [ ] **Quick start** — How to run it (< 5 steps)
- [ ] **Architecture** — System overview or diagram
- [ ] **Tech stack** — Technologies used
- [ ] **Installation** — Full setup instructions
- [ ] **Usage** — How to use it with examples
- [ ] **Testing** — How to run tests
- [ ] **Contributing** — (Optional) How to contribute
- [ ] **License** — License information

### Code Quality

- [ ] **Clean code** — No debug prints, commented code, or TODOs
- [ ] **Consistent style** — Formatted with ruff/black/prettier
- [ ] **Type hints** — On public functions (Python)
- [ ] **Docstrings** — On public functions
- [ ] **No secrets** — API keys removed, .env.example provided
- [ ] **Reasonable structure** — Logical file organization

### Testing

- [ ] **Tests exist** — At least core functionality tested
- [ ] **Tests pass** — `pytest` runs green
- [ ] **CI configured** — GitHub Actions or similar

### Documentation

- [ ] **API docs** — If applicable
- [ ] **Configuration docs** — All options explained
- [ ] **Troubleshooting** — Common issues addressed

---

## Project Summary

Create a one-paragraph summary for your portfolio:

```markdown
### [Project Name]

[One sentence: what it is and why it matters]

[One sentence: key technical highlight]

[One sentence: results/impact]

**Tech**: [Tech 1], [Tech 2], [Tech 3]

**Links**: [GitHub](url) | [Demo](url) | [Blog](url)
```

### Example

```markdown
### RAG Embedding Pipeline

Built a production-ready retrieval-augmented generation (RAG) pipeline
that ingests 1000+ documents, creates embeddings using OpenAI, stores
them in Pinecone, and enables semantic search with sub-100ms latency.

Implemented batch processing for scale and created an evaluation
harness with 50 golden queries to measure retrieval quality.

Achieved MRR@10 of 0.78, enabling the team to find answers 3x faster.

**Tech**: Python, FastAPI, OpenAI Embeddings, Pinecone, pytest

**Links**: [GitHub](link) | [Demo Video](link) | [Blog Post](link)
```

---

## Visual Assets

### Screenshot/GIF

- [ ] Shows the product working
- [ ] Clear and high resolution
- [ ] Annotated if helpful
- [ ] At the top of README

### Architecture Diagram

- [ ] Shows main components
- [ ] Data flow is clear
- [ ] Not overly complex
- [ ] Uses standard notation

### Demo Video

- [ ] Under 5 minutes
- [ ] Clear audio
- [ ] Shows key features
- [ ] Uploaded (YouTube/Loom/etc.)

---

## Pre-Publish Checks

### Works Locally

```bash
# Clone fresh
git clone <repo> temp-test
cd temp-test

# Follow README instructions
pip install -e .
pytest
python run.py  # or whatever your entry point is
```

### Links Work

- [ ] All README links resolve
- [ ] Demo links work
- [ ] Documentation links work

### Clean History

- [ ] No sensitive data in history
- [ ] Reasonable commit messages
- [ ] Main branch is stable

---

## GitHub Profile Integration

### Pin the Repo

Go to your GitHub profile and pin important projects.

### Add Topics

Add relevant topics to make it discoverable:
- `python`
- `machine-learning`
- `rag`
- `llm`
- `fastapi`

### Set Social Preview

Add a social preview image (Settings → Social Preview).

---

## LinkedIn/Resume Entry

```markdown
**[Project Name]** | [Role] | [Date]

- Built [what] using [technologies]
- Achieved [metric/result]
- [Link to project]
```

### Example

```markdown
**RAG Embedding Pipeline** | Personal Project | Jan 2026

- Built production-ready semantic search over 1000+ documents using
  Python, FastAPI, OpenAI, and Pinecone
- Achieved 0.78 MRR@10 with sub-100ms query latency
- github.com/username/rag-pipeline
```

---

## Interview Prep

Be ready to discuss:

1. **Why you built it** — The problem and motivation
2. **How it works** — Architecture and data flow
3. **Key decisions** — Why you chose specific technologies
4. **Challenges** — What was hard and how you solved it
5. **Results** — Metrics and impact
6. **Next steps** — What you'd add or change

---

## Monthly Review

Each month, after completing a project:

1. [ ] Run through this checklist
2. [ ] Update portfolio summary
3. [ ] Share on LinkedIn (optional)
4. [ ] Write blog post (optional)
5. [ ] Record demo video (optional)

---

## Links

- [How to demo](how-to-demo.md)
- [How to write Medium post](how-to-write-medium-post.md)
- [/publish command](../../.claude/commands/publish.md)
