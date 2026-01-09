# How to Write a Medium Post

Guide for writing technical blog posts about your projects.

---

## Overview

A good technical post:
- Teaches something useful
- Shows your thought process
- Includes working examples
- Is well-structured and scannable

---

## Post Structure

### Title

Make it specific and benefit-oriented.

**Good**:
- "Building a Production-Ready RAG Pipeline: Lessons from 1000 Documents"
- "How I Reduced Embedding Latency by 80% with Batching"
- "A Practical Guide to LLM Evaluation with Golden Sets"

**Avoid**:
- "My RAG Project" (too vague)
- "RAG Tutorial" (too generic)
- "Everything About Embeddings" (too broad)

### Subtitle

Add context or a hook.

```
"What I learned building semantic search for a 10,000-document knowledge base"
```

### Introduction (2-3 paragraphs)

Hook the reader, state the problem, preview the solution.

```markdown
Finding information in a large document collection is hard. Traditional
keyword search fails when users ask questions in natural language.

I built a RAG (Retrieval-Augmented Generation) pipeline that enables
semantic search over 1000+ documents with sub-100ms latency.

In this post, I'll share the architecture, key decisions, and lessons
learned—including the mistakes I made along the way.
```

### The Problem (1-2 paragraphs)

Explain what you were solving.

```markdown
## The Problem

Our team had 10,000 pages of documentation spread across wikis, PDFs,
and markdown files. Users would ask questions like "How do I configure
SSO?" but keyword search would return hundreds of irrelevant results.

We needed a system that understood the *meaning* of questions and
could find relevant answers even when the exact words didn't match.
```

### The Solution (Main Body)

Walk through your approach. Use sections and code.

```markdown
## Architecture Overview

[Diagram or description]

## Step 1: Document Ingestion

The first challenge was ingesting documents from multiple sources...

```python
# Code example
def ingest_document(path: str) -> List[Chunk]:
    ...
```

## Step 2: Chunking Strategy

I experimented with several chunking approaches...

## Step 3: Embedding and Indexing

For embeddings, I compared three models...

[Continue with each major step]
```

### Results

Show what you achieved.

```markdown
## Results

After optimization, the pipeline achieved:
- **MRR@10**: 0.78 (up from 0.45 with keyword search)
- **Latency**: 95ms p95
- **Throughput**: 100 queries/second

The team now finds answers 3x faster than before.
```

### Lessons Learned

Share insights and mistakes.

```markdown
## What I Learned

1. **Chunk boundaries matter more than chunk size**
   I spent days tuning chunk size, but the real gains came from
   smart boundary detection (splitting on paragraphs, not characters).

2. **Evaluation is essential**
   Without a golden set, I was flying blind. Building the eval
   harness took time but saved me from shipping a broken system.

3. **Start simple**
   My first approach was too complex. The simple batch pipeline
   outperformed my over-engineered async solution.
```

### Conclusion

Summarize and provide next steps.

```markdown
## Conclusion

Building a production RAG pipeline taught me that the fundamentals
matter: clean data, smart chunking, and rigorous evaluation.

If you're building something similar, start with evaluation and
work backwards. It's the only way to know if you're making progress.

**Resources**:
- [GitHub repo](link)
- [Demo video](link)
- [Evaluation framework we used](link)
```

---

## Writing Tips

### Be Specific

**Generic**: "I improved performance"
**Specific**: "I reduced p95 latency from 500ms to 95ms"

### Show Your Work

Include:
- Code snippets
- Configuration examples
- Screenshots/diagrams
- Metrics before/after

### Be Honest

Share mistakes and dead ends. Readers appreciate authenticity.

### Make It Scannable

- Use headers
- Use bullet points
- Keep paragraphs short
- Add visual breaks

### Tell a Story

Structure as a journey:
- Where you started
- What you tried
- What worked/didn't
- Where you ended up

---

## Code in Posts

### Keep It Simple

```python
# Good: focused, minimal
def embed_text(text: str) -> List[float]:
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding
```

```python
# Bad: too much boilerplate
import os
import logging
from typing import Optional, List, Dict, Any
from openai import OpenAI

logger = logging.getLogger(__name__)

def embed_text(
    text: str,
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
    retry_count: int = 3,
    ...
```

### Explain Non-Obvious Parts

```python
# Use overlap to avoid splitting context at chunk boundaries
chunks = text_splitter.split(text, chunk_size=512, overlap=50)
```

### Provide Context

```python
# After getting embeddings, we normalize for cosine similarity
embeddings = normalize(embeddings)
```

---

## Formatting

### Images and Diagrams

- Architecture diagrams
- Before/after comparisons
- Metrics visualizations
- Screenshots of the product

### Code Blocks

Use language hints for syntax highlighting:

````markdown
```python
def example():
    pass
```
````

### Links

Link to:
- Your GitHub repo
- Documentation you referenced
- Tools you mentioned
- Related posts

---

## Publishing Checklist

- [ ] Title is specific and compelling
- [ ] Introduction hooks the reader
- [ ] Problem is clearly stated
- [ ] Solution is well-structured
- [ ] Code examples are clean
- [ ] Results are quantified
- [ ] Lessons are honest
- [ ] Links work
- [ ] Images load
- [ ] Proofread for typos
- [ ] Read aloud for flow

---

## Example Outline

```markdown
# Building a Production-Ready RAG Pipeline

## Introduction
- Hook: The search problem
- What I built
- What you'll learn

## The Problem
- Context: 10K docs
- Why keyword search failed

## Architecture Overview
- Diagram
- Component overview

## Implementation
### Document Ingestion
### Chunking Strategy
### Embedding
### Indexing
### Retrieval
### Generation

## Evaluation
- Golden set creation
- Metrics used
- Results

## Lessons Learned
1. Lesson 1
2. Lesson 2
3. Lesson 3

## Conclusion
- Summary
- Resources
```

---

## Links

- [How to demo](how-to-demo.md)
- [Portfolio checklist](portfolio-checklist.md)
- [/publish command](../../.claude/commands/publish.md)
