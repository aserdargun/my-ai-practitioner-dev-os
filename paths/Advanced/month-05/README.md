# Month 05 — RAG Systems

Build production-ready retrieval-augmented generation systems.

---

## Why It Matters

RAG is the foundation of most practical LLM applications. From chatbots to knowledge management, RAG enables grounding LLM responses in your own data. This is one of the most in-demand skills in AI engineering today.

---

## Prerequisites

- Month 03: Transformers & LLMs
- Understanding of embeddings (Month 01)
- Python API development basics
- Familiarity with databases

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 2 Focus
- **Embedding Models**: Creating and using embeddings
- **RAG Systems**: Architecture and implementation
- **LangChain**: Orchestrating LLM applications
- **LangGraph**: Building agentic workflows
- **LlamaIndex**: Data framework for LLMs
- **Vector Databases**: Pinecone, Qdrant, Weaviate, Milvus, FAISS

### Concepts
- Document chunking strategies
- Semantic search and retrieval
- Context window management
- Evaluation of RAG systems
- Hybrid search (dense + sparse)
- Reranking strategies

---

## Main Project: Knowledge Base RAG

Build a complete RAG system over a document corpus.

### Deliverables

1. **Document Ingestion Pipeline**
   - Multi-format document loading
   - Chunking with overlap
   - Embedding generation

2. **Vector Store Integration**
   - At least 2 vector DBs compared
   - Indexing and retrieval
   - Metadata filtering

3. **RAG Pipeline**
   - LangChain orchestration
   - Prompt engineering
   - Source citation

4. **Evaluation Harness**
   - Golden set creation
   - Retrieval metrics (MRR, Recall)
   - Generation quality scoring

### Definition of Done

- [ ] Ingests 100+ documents reliably
- [ ] Retrieval MRR@10 > 0.7
- [ ] Answers cite sources correctly
- [ ] Two vector DBs compared with metrics
- [ ] Evaluation harness with 20+ test queries
- [ ] Sub-second query latency

---

## Stretch Goals

- [ ] Implement hybrid search (BM25 + dense)
- [ ] Add reranking with cross-encoder
- [ ] Build conversational memory
- [ ] Create LangGraph agent workflow
- [ ] Compare LangChain vs LlamaIndex

---

## Weekly Breakdown

### Week 1: Embeddings & Chunking
- Embedding model selection
- Chunking strategies
- Document preprocessing
- Initial ingestion pipeline

### Week 2: Vector Databases
- Pinecone setup
- FAISS local option
- Indexing and querying
- Metadata and filtering

### Week 3: RAG Pipeline
- LangChain setup
- Prompt engineering
- Source citation
- Error handling

### Week 4: Evaluation & Polish
- Golden set creation
- Metrics implementation
- Performance optimization
- Documentation and demo

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 5 focusing on RAG systems. Help me plan a week setting up document ingestion and vector stores.
```

### Building
```
As the Builder agent, help me implement a RAG pipeline using LangChain and Pinecone. Start with document ingestion.
```

### Skill Usage
```
Use the RAG with Evals skill to help me build and evaluate my retrieval system.
```

### Debugging
```
/debug-learning — My retrieval is returning irrelevant documents. How do I debug and improve this?
```

### Evaluation
```
As the Builder, help me create a golden set for evaluating my RAG system. I have 100 documents about [topic].
```

---

## How to Publish

### Demo
- Query the system live
- Show source citations
- Compare vector DB performance
- Display evaluation metrics

### Write-up Topics
- Why RAG matters
- Chunking strategies that work
- Vector DB comparison
- Evaluation methodology

---

## Resources

### Documentation
- [LangChain Docs](https://python.langchain.com/)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [Pinecone Docs](https://docs.pinecone.io/)
- [Qdrant Docs](https://qdrant.tech/documentation/)

### Tutorials
- "Building Production RAG Applications"
- "Evaluating RAG Systems"
- "Chunking Strategies for RAG"

### Models
- `text-embedding-3-small` (OpenAI)
- `bge-base-en` (open source)
- `all-MiniLM-L6-v2` (sentence-transformers)

---

## Next Month Preview

**Month 06**: API Development — Building production APIs with FastAPI, Docker, and CI/CD pipelines.
