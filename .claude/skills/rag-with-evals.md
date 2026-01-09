# Skill: RAG with Evals

Build a Retrieval-Augmented Generation system with proper evaluation methodology.

## Trigger

Use this skill when:
- Building a Q&A system over documents
- Creating a chatbot with knowledge base
- Need to ground LLM responses in source documents
- Evaluating retrieval and generation quality

## Prerequisites

- Document corpus prepared
- Vector database access (Pinecone, Qdrant, etc.)
- LLM API access (OpenAI, Anthropic, etc.)
- Python with langchain or equivalent
- Golden set of test questions with expected answers

## Steps

### 1. Prepare Documents (30 min)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

# Load documents
docs = []
for file in Path("documents").glob("*.md"):
    docs.append({
        "content": file.read_text(),
        "source": file.name
    })

# Chunk documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

chunks = []
for doc in docs:
    for i, chunk in enumerate(splitter.split_text(doc["content"])):
        chunks.append({
            "text": chunk,
            "source": doc["source"],
            "chunk_id": f"{doc['source']}_{i}"
        })

print(f"Created {len(chunks)} chunks from {len(docs)} documents")
```

### 2. Create Embeddings and Index (20 min)

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embeddings(texts, model="text-embedding-3-small"):
    response = client.embeddings.create(input=texts, model=model)
    return [e.embedding for e in response.data]

# Batch embed chunks
batch_size = 100
embeddings = []
for i in range(0, len(chunks), batch_size):
    batch = [c["text"] for c in chunks[i:i+batch_size]]
    embeddings.extend(get_embeddings(batch))
    print(f"Embedded {min(i+batch_size, len(chunks))}/{len(chunks)}")

# Index in vector store (example: using local FAISS)
import faiss

dimension = len(embeddings[0])
index = faiss.IndexFlatIP(dimension)  # Inner product for cosine sim
index.add(np.array(embeddings).astype('float32'))
```

### 3. Implement Retrieval (20 min)

```python
def retrieve(query, k=5):
    query_embedding = get_embeddings([query])[0]
    query_vec = np.array([query_embedding]).astype('float32')

    scores, indices = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            **chunks[idx],
            "score": float(score)
        })

    return results

# Test retrieval
results = retrieve("What is the refund policy?")
for r in results:
    print(f"[{r['score']:.3f}] {r['source']}: {r['text'][:100]}...")
```

### 4. Implement Generation (20 min)

```python
def generate_answer(query, contexts, model="gpt-4o-mini"):
    context_text = "\n\n".join([
        f"[Source: {c['source']}]\n{c['text']}"
        for c in contexts
    ])

    prompt = f"""Answer the question based on the provided context.
If the context doesn't contain the answer, say "I don't have enough information."

Context:
{context_text}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content

def rag_query(query, k=5):
    contexts = retrieve(query, k)
    answer = generate_answer(query, contexts)
    return {
        "query": query,
        "answer": answer,
        "sources": contexts
    }

# Test RAG
result = rag_query("What is the refund policy?")
print(f"Answer: {result['answer']}")
print(f"Sources: {[s['source'] for s in result['sources']]}")
```

### 5. Create Golden Test Set (30 min)

```python
# golden_set.jsonl - create manually or with LLM assistance
golden_set = [
    {
        "query": "What is the refund policy?",
        "expected_answer": "Full refund within 30 days of purchase",
        "relevant_docs": ["policies.md"],
        "category": "policy"
    },
    {
        "query": "How do I reset my password?",
        "expected_answer": "Click 'Forgot Password' on the login page",
        "relevant_docs": ["faq.md", "account.md"],
        "category": "how-to"
    },
    # ... more test cases
]

# Save golden set
import json
with open("eval/golden_set.jsonl", "w") as f:
    for item in golden_set:
        f.write(json.dumps(item) + "\n")
```

### 6. Evaluate Retrieval (30 min)

```python
def evaluate_retrieval(golden_set, k=5):
    metrics = {
        "mrr": [],
        "recall_at_k": [],
        "precision_at_k": []
    }

    for item in golden_set:
        results = retrieve(item["query"], k)
        retrieved_sources = [r["source"] for r in results]
        relevant = set(item["relevant_docs"])

        # MRR
        for i, source in enumerate(retrieved_sources):
            if source in relevant:
                metrics["mrr"].append(1.0 / (i + 1))
                break
        else:
            metrics["mrr"].append(0.0)

        # Recall@k
        retrieved_relevant = len(set(retrieved_sources) & relevant)
        metrics["recall_at_k"].append(retrieved_relevant / len(relevant))

        # Precision@k
        metrics["precision_at_k"].append(retrieved_relevant / k)

    return {k: np.mean(v) for k, v in metrics.items()}

retrieval_metrics = evaluate_retrieval(golden_set)
print(f"Retrieval Metrics: {retrieval_metrics}")
```

### 7. Evaluate Generation (30 min)

```python
def evaluate_answer(expected, generated, model="gpt-4o-mini"):
    """Use LLM to judge answer quality"""

    prompt = f"""Compare the generated answer to the expected answer.
Score from 1-5:
- 5: Perfect match, complete and accurate
- 4: Mostly correct, minor omissions
- 3: Partially correct, some key info missing
- 2: Somewhat relevant but largely incorrect
- 1: Completely wrong or irrelevant

Expected: {expected}
Generated: {generated}

Return only the numeric score."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return int(response.choices[0].message.content.strip())

def evaluate_generation(golden_set):
    scores = []
    results = []

    for item in golden_set:
        response = rag_query(item["query"])
        score = evaluate_answer(item["expected_answer"], response["answer"])
        scores.append(score)
        results.append({
            **item,
            "generated": response["answer"],
            "score": score
        })

    return {
        "mean_score": np.mean(scores),
        "score_distribution": {i: scores.count(i) for i in range(1, 6)},
        "results": results
    }

generation_metrics = evaluate_generation(golden_set)
print(f"Generation Score: {generation_metrics['mean_score']:.2f}")
```

### 8. Document Results (20 min)

```markdown
## RAG Evaluation Report

### Retrieval Performance
| Metric | Score |
|--------|-------|
| MRR@5 | 0.78 |
| Recall@5 | 0.85 |
| Precision@5 | 0.34 |

### Generation Performance
| Metric | Score |
|--------|-------|
| Mean Quality | 4.2/5 |
| Perfect (5) | 60% |
| Acceptable (4+) | 85% |

### Error Analysis
- Common failures: Multi-hop questions
- Improvement areas: Chunk boundaries, context window
```

## Artifacts Produced

1. **Chunked Documents** — Preprocessed corpus
2. **Vector Index** — Embedded and indexed chunks
3. **Golden Set** — `eval/golden_set.jsonl`
4. **Evaluation Report** — Retrieval and generation metrics
5. **RAG Service** — Functional retrieval + generation pipeline

## Quality Bar

Your RAG system is complete when:

- [ ] Documents are properly chunked
- [ ] Embeddings are indexed efficiently
- [ ] Retrieval returns relevant results
- [ ] Generation is grounded in sources
- [ ] Golden set has 20+ diverse questions
- [ ] MRR@5 > 0.7 (or your target)
- [ ] Generation quality > 4.0 average (or your target)
- [ ] Error cases are documented

## Common Pitfalls

1. **Chunks too small/large** — Affects retrieval relevance
2. **No overlap** — Splits context at bad boundaries
3. **Hallucination** — LLM ignores context
4. **No citation** — Can't verify answers
5. **Evaluation on training data** — Use held-out test set
