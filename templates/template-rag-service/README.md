# RAG Service Template

A template for building Retrieval-Augmented Generation systems.

## Features

- Document ingestion pipeline
- Vector-based retrieval
- Answer generation with sources
- Evaluation framework
- Test suite included

## Quick Start

```bash
# Install dependencies
pip install -e .

# Ingest documents
python rag/ingest.py --input docs/ --output index/

# Query the system
python rag/answer.py --query "What is RAG?"

# Run tests
pytest
```

## Project Structure

```
template-rag-service/
├── rag/
│   ├── ingest.py        # Document ingestion
│   ├── retrieve.py      # Vector retrieval
│   └── answer.py        # Answer generation
├── eval/
│   └── golden_set.jsonl # Evaluation dataset
├── tests/
│   └── test_retrieve.py # Test suite
├── pyproject.toml       # Dependencies and config
└── README.md            # This file
```

## Usage

### Ingest Documents

```python
from rag.ingest import DocumentIngester

ingester = DocumentIngester(chunk_size=500, chunk_overlap=50)
chunks = ingester.ingest_directory("./docs")
ingester.save_index(chunks, "./index")
```

### Retrieve Documents

```python
from rag.retrieve import Retriever

retriever = Retriever.load("./index")
results = retriever.search("What is machine learning?", top_k=5)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.content[:200]}...")
```

### Generate Answers

```python
from rag.answer import RAGPipeline

rag = RAGPipeline(retriever=retriever)
answer = rag.answer("What is machine learning?")
print(f"Answer: {answer.text}")
print(f"Sources: {answer.sources}")
```

## Customization

1. Replace mock embeddings with real model (OpenAI, sentence-transformers)
2. Add your documents to the ingestion pipeline
3. Configure chunking strategy
4. Add LLM for answer generation

## Evaluation

```bash
# Run evaluation on golden set
python -m pytest tests/ -v

# Custom evaluation
python rag/answer.py --eval eval/golden_set.jsonl
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=rag

# Run specific test
pytest tests/test_retrieve.py -v
```
