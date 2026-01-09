# Month 02 — Sequence Models

Master RNN and LSTM architectures for sequential data.

---

## Why It Matters

Sequence models are fundamental to understanding how deep learning processes sequential data. While transformers have largely replaced RNNs for many tasks, understanding RNNs and LSTMs provides crucial intuition for sequence modeling and is still relevant for time-series, embedded systems, and interpretable models.

---

## Prerequisites

- Month 01: NLP Foundations (embeddings, text processing)
- Python programming
- Basic PyTorch or TensorFlow (we'll learn as we go)
- Linear algebra fundamentals

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 1 Focus
- **RNN**: Recurrent neural network architecture, backprop through time
- **LSTM**: Long short-term memory, gating mechanisms
- **PyTorch**: Deep learning framework fundamentals

### Tier 2 Integration
- **PyTorch**: Building and training neural networks
- **TensorFlow**: Alternative implementation

### Concepts
- Sequence-to-sequence modeling
- Vanishing/exploding gradients
- LSTM cell mechanics
- Bidirectional RNNs
- Sequence classification and generation

---

## Main Project: Sequence Classifier & Generator

Build models for sequence classification and text generation.

### Deliverables

1. **RNN Classifier**
   - Sentiment classification using RNN
   - Training loop with proper validation
   - Performance metrics

2. **LSTM Improvements**
   - Upgrade RNN to LSTM
   - Compare performance
   - Analyze gradient flow

3. **Text Generator**
   - Character-level or word-level generation
   - Temperature-based sampling
   - Interactive generation

4. **Documentation**
   - Model architecture diagrams
   - Training curves
   - Comparison analysis

### Definition of Done

- [ ] RNN classifier achieves > 75% accuracy
- [ ] LSTM shows improvement over RNN
- [ ] Generator produces coherent text samples
- [ ] Training is reproducible (seeds, logging)
- [ ] Model checkpoints saved properly
- [ ] Documentation explains architecture choices

---

## Stretch Goals

- [ ] Implement bidirectional LSTM
- [ ] Add attention mechanism (preview of Month 03)
- [ ] Build sequence-to-sequence model
- [ ] Compare PyTorch and TensorFlow implementations
- [ ] Visualize hidden states with Dash

---

## Weekly Breakdown

### Week 1: PyTorch Foundations
- PyTorch tensors and autograd
- Building simple neural networks
- Dataset and DataLoader
- Training loop basics

### Week 2: RNN Implementation
- RNN architecture from scratch
- Sentiment classification task
- Training and evaluation
- Debugging gradient issues

### Week 3: LSTM Deep Dive
- LSTM cell mechanics
- Implementing LSTM layer
- Performance comparison
- Hyperparameter tuning

### Week 4: Generation & Polish
- Text generation model
- Sampling strategies
- Documentation and demo
- Blog post

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 2 focusing on sequence models. Help me plan a week learning PyTorch and building an RNN.
```

### Building
```
As the Builder agent, help me implement an LSTM classifier in PyTorch. Start with the model architecture.
```

### Understanding
```
As the Researcher, explain how LSTM gates work. I understand basic RNNs but the forget/input/output gates confuse me.
```

### Debugging
```
/debug-learning — My RNN loss isn't decreasing. Help me diagnose the issue.
```

### Review
```
/harden — Review my PyTorch training loop for best practices and potential issues.
```

---

## How to Publish

### Demo
- Show training progress curves
- Run classification on new examples
- Generate text samples with different temperatures
- Compare RNN vs LSTM performance

### Write-up Topics
- Why sequence modeling matters
- RNN vanishing gradient problem
- How LSTM solves it
- Results and learnings

---

## Resources

### Documentation
- [PyTorch RNN Tutorial](https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html)
- [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [PyTorch LSTM](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

### Papers
- "Long Short-Term Memory" (Hochreiter & Schmidhuber, 1997)
- "Learning Phrase Representations using RNN Encoder-Decoder"

### Datasets
- IMDB Sentiment Dataset
- Shakespeare Text for Generation
- Penn Treebank

---

## Next Month Preview

**Month 03**: Transformers & LLMs — BERT, GPT, and the attention mechanism that revolutionized NLP.
