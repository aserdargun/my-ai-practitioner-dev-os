# Command: /publish

## Purpose

Prepare your completed project for demo and write-up. This command guides you through creating a compelling presentation of your work for your portfolio.

## Inputs

- **Project to publish**: The completed deliverable
- **Target audience**: Technical peers, hiring managers, general
- **Format preference**: Demo video, blog post, README showcase

## Outputs

1. **Demo Script**
   - Key points to highlight
   - Flow of demonstration
   - Talking points

2. **Write-up Draft**
   - Problem statement
   - Solution approach
   - Technical highlights
   - Results and learnings

3. **Portfolio Entry**
   - One-paragraph summary
   - Key technologies used
   - Link to repo/demo

## When to Use

- End of each month after completing deliverables
- When adding to portfolio
- Before sharing on LinkedIn/Twitter
- When preparing for job interviews

## Agent Routing

**Builder Agent** handles this command.

The Builder uses:
- [how-to-demo.md](../../docs/publishing/how-to-demo.md)
- [how-to-write-medium-post.md](../../docs/publishing/how-to-write-medium-post.md)
- [portfolio-checklist.md](../../docs/publishing/portfolio-checklist.md)

## Example Usage

Basic publish prep:
```
/publish
```

With audience:
```
/publish — Prepare for technical hiring manager audience.
```

With format:
```
/publish — I want to write a Medium post about this RAG project.
```

## Sample Output

```markdown
## Publish Preparation — RAG Embedding Pipeline

### Demo Script (5 minutes)

#### Opening (30 sec)
"I built a production-ready RAG embedding pipeline that processes 1000+ documents and enables semantic search. Let me show you how it works."

#### Architecture Overview (1 min)
- Show system diagram
- Highlight: ingestion → embedding → Pinecone → retrieval
- Mention key design decisions (batching, retry logic)

#### Live Demo (2.5 min)
1. Ingest sample documents (show logs)
2. Query the system (show results)
3. Show evaluation metrics

#### Technical Highlights (1 min)
- Batch processing for scale
- Configurable chunking strategies
- Evaluation harness for quality metrics

#### Closing (30 sec)
- What I learned
- What I'd do differently
- Links to repo

### Write-up Draft

#### Title
"Building a Production-Ready RAG Pipeline: Lessons from 1000 Documents"

#### Outline

1. **The Problem**
   - Need to make documentation searchable
   - Traditional keyword search fails for semantic queries

2. **The Solution**
   - Embedding pipeline with batch processing
   - Vector store (Pinecone) for similarity search
   - Evaluation harness to measure quality

3. **Technical Deep Dive**
   - Chunking strategy decisions
   - Handling rate limits and retries
   - Measuring retrieval quality

4. **Results**
   - Processes 1000 docs in X minutes
   - Retrieval accuracy: X%
   - Latency: Xms p95

5. **Learnings**
   - What worked well
   - What I'd do differently
   - Next steps

### Portfolio Entry

```markdown
### RAG Embedding Pipeline
Built a production-ready retrieval-augmented generation (RAG) pipeline
that ingests 1000+ documents, creates embeddings using OpenAI, stores
them in Pinecone, and enables semantic search with sub-100ms latency.

**Tech**: Python, FastAPI, OpenAI Embeddings, Pinecone, pytest

**Links**: [GitHub](link) | [Demo Video](link) | [Blog Post](link)
```

### Pre-Publish Checklist

- [ ] README is polished and has clear setup instructions
- [ ] Code is clean (ran ruff, no obvious issues)
- [ ] Tests pass (`pytest` green)
- [ ] Demo recording captured (if doing video)
- [ ] Write-up reviewed for typos
- [ ] Sensitive data/keys removed

### Hook Integration

Run pre-publish checks:
```bash
bash .claude/hooks/pre_publish_check.sh
```

---
**Ready to publish?** Complete the checklist and let me know if you need help with any item.
```

## Related Commands

- `/harden` — Polish before publishing
- `/retro` — Reflect on what you learned
- `/add-best-practice` — Capture key learnings
