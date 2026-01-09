# Month 01 — NLP Foundations

Master text processing fundamentals and word embeddings.

---

## Why It Matters

NLP is foundational for modern AI systems. Understanding text preprocessing, tokenization, and word embeddings is essential for building chatbots, search systems, and language models. These skills are highly sought after in AI engineering roles.

---

## Prerequisites

- Python fundamentals
- Basic linear algebra (vectors, matrices)
- Command line / Bash basics

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 1 Focus
- **NLTK**: Text preprocessing, tokenization, stemming, lemmatization
- **Word2Vec**: Dense word embeddings, semantic similarity
- **GloVe**: Pre-trained embeddings, word relationships
- **FastText**: Subword embeddings, handling OOV words
- **Bash/Shell Scripting**: Automation for data processing

### Concepts
- Tokenization strategies
- Stopword removal and text normalization
- Word vectors and embedding spaces
- Semantic similarity and analogy tasks
- Text classification basics

---

## Main Project: Text Processing Pipeline

Build a complete text preprocessing and embedding pipeline.

### Deliverables

1. **Text Preprocessor**
   - Tokenization with multiple strategies
   - Stopword removal, stemming, lemmatization
   - Configurable pipeline

2. **Embedding Explorer**
   - Load Word2Vec, GloVe, FastText embeddings
   - Similarity search
   - Analogy solver (king - man + woman = queen)

3. **Simple Classifier**
   - Text classification using embeddings
   - Sentiment or topic classification

4. **Documentation**
   - README with usage examples
   - Notebook with exploration

### Definition of Done

- [ ] Text preprocessor handles multiple input formats
- [ ] At least 2 embedding models integrated
- [ ] Similarity search returns relevant results
- [ ] Classifier achieves > 70% accuracy on test set
- [ ] Tests cover core functionality
- [ ] README documents usage

---

## Stretch Goals

- [ ] Build a Dash dashboard for embedding visualization
- [ ] Implement custom Word2Vec training
- [ ] Add GraphQL API for embeddings
- [ ] Compare embedding models quantitatively

---

## Weekly Breakdown

### Week 1: Text Preprocessing
- Set up project structure
- Implement tokenization
- Add stemming/lemmatization
- Write tests

### Week 2: Word Embeddings
- Load pre-trained Word2Vec
- Implement GloVe loading
- Add FastText support
- Build similarity search

### Week 3: Building the Pipeline
- Integrate preprocessor + embeddings
- Build simple classifier
- Evaluate on test data
- Optimize performance

### Week 4: Polish & Publish
- Complete documentation
- Add visualization
- Record demo
- Write blog post

---

## Claude Prompts

Copy-paste these prompts to get help:

### Planning
```
/plan-week — I'm starting Month 1 focusing on NLP foundations. Help me plan my first week with text preprocessing.
```

### Building
```
As the Builder agent, help me implement a text preprocessing pipeline using NLTK. Start with tokenization.
```

### Embedding Help
```
As the Researcher, explain the differences between Word2Vec, GloVe, and FastText. Which should I use for my text classification task?
```

### Debugging
```
/debug-learning — I'm confused about how word embeddings capture semantic meaning. Help me understand.
```

### Review
```
/harden — Review my text preprocessing code for quality and edge cases.
```

### Publish
```
/publish — I've completed my embedding pipeline. Help me prepare a demo and write-up.
```

---

## How to Publish

### Demo
- Show loading different embedding models
- Demonstrate similarity search
- Run classification on sample texts
- Show analogy solving

### Write-up
- Problem: Why text processing matters
- Solution: Your pipeline architecture
- Results: Classification accuracy, example outputs
- Learnings: What you discovered about embeddings

### Portfolio Entry
```markdown
### Text Embedding Pipeline
Built an NLP preprocessing and embedding pipeline supporting Word2Vec,
GloVe, and FastText. Includes text classification achieving 75% accuracy
on sentiment analysis.

**Tech**: Python, NLTK, Gensim, pytest

**Links**: [GitHub](link) | [Demo](link) | [Blog](link)
```

---

## Resources

### Documentation
- [NLTK Documentation](https://www.nltk.org/)
- [Gensim Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)
- [GloVe Project](https://nlp.stanford.edu/projects/glove/)
- [FastText](https://fasttext.cc/)

### Tutorials
- Word2Vec paper: "Efficient Estimation of Word Representations"
- GloVe paper: "GloVe: Global Vectors for Word Representation"
- FastText paper: "Enriching Word Vectors with Subword Information"

### Pre-trained Models
- `word2vec-google-news-300`
- `glove-wiki-gigaword-100`
- `fasttext-wiki-news-subwords-300`

---

## Evaluation Focus

This month emphasizes:

| Dimension | Focus |
|-----------|-------|
| Completion | Ship all 4 deliverables |
| Quality | Tests pass, code is clean |
| Consistency | Daily progress logged |
| Depth | Try at least one stretch goal |
| Reflection | Weekly retros, capture learnings |

---

## Next Month Preview

**Month 02**: Sequence Models — RNN, LSTM, and sequence-to-sequence learning with PyTorch.
