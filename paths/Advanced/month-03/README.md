# Month 03 — Transformers & LLMs

Master the attention mechanism and modern language models.

---

## Why It Matters

Transformers power modern AI: ChatGPT, BERT, and virtually every state-of-the-art NLP system. Understanding attention, transformer architecture, and how to use pre-trained models is essential for any AI engineer. This knowledge is critical for building LLM applications.

---

## Prerequisites

- Month 02: Sequence Models (RNN/LSTM fundamentals)
- PyTorch proficiency
- Understanding of embeddings
- Basic understanding of neural network training

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 2 Focus
- **BERT**: Bidirectional encoder representations
- **GPT**: Generative pre-trained transformers
- **T5**: Text-to-text framework
- **Hugging Face**: Transformers library and ecosystem
- **PEFT**: Parameter-efficient fine-tuning
- **LoRA/QLoRA**: Low-rank adaptation techniques

### Concepts
- Self-attention mechanism
- Multi-head attention
- Positional encoding
- Encoder vs. decoder architectures
- Fine-tuning strategies
- Prompt engineering

---

## Main Project: Fine-tuned Language Model

Fine-tune a transformer model for a specific task.

### Deliverables

1. **Attention Explainer**
   - Implement attention from scratch
   - Visualize attention patterns
   - Interactive demo

2. **BERT Classifier**
   - Fine-tune BERT for classification
   - Proper training/validation split
   - Evaluation metrics

3. **LoRA Fine-tuning**
   - Apply LoRA to reduce training costs
   - Compare with full fine-tuning
   - Parameter efficiency analysis

4. **Documentation**
   - Architecture explanations
   - Training configurations
   - Results comparison

### Definition of Done

- [ ] Attention mechanism implemented and visualized
- [ ] BERT classifier achieves > 85% accuracy
- [ ] LoRA fine-tuning working with measured speedup
- [ ] Comparison table: full vs LoRA fine-tuning
- [ ] Model can be loaded and used for inference
- [ ] Documentation covers key concepts

---

## Stretch Goals

- [ ] Implement transformer from scratch
- [ ] Try T5 for text-to-text tasks
- [ ] QLoRA with quantization
- [ ] Compare BERT, RoBERTa, DistilBERT
- [ ] Build a simple chatbot interface

---

## Weekly Breakdown

### Week 1: Attention Mechanism
- Self-attention math
- Implementation from scratch
- Attention visualization
- Multi-head attention

### Week 2: Transformer Architecture
- Encoder architecture
- Positional encoding
- Using Hugging Face transformers
- Loading pre-trained models

### Week 3: Fine-tuning
- BERT classification fine-tuning
- Training best practices
- Evaluation and metrics
- Hyperparameter tuning

### Week 4: Efficient Fine-tuning
- PEFT concepts
- LoRA implementation
- Comparison experiments
- Documentation and demo

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 3 focusing on transformers. Help me plan a week understanding attention and Hugging Face.
```

### Building
```
As the Builder agent, help me fine-tune BERT for text classification using Hugging Face Transformers.
```

### Understanding
```
As the Researcher, explain the self-attention mechanism step by step. Include the Q, K, V transformations.
```

### Debugging
```
/debug-learning — I'm confused about the difference between BERT and GPT architectures. When do I use which?
```

### Efficient Training
```
As the Builder, help me set up LoRA fine-tuning using the PEFT library. I want to reduce memory usage.
```

---

## How to Publish

### Demo
- Visualize attention patterns on sample text
- Run classification on new examples
- Compare inference speed: full model vs LoRA
- Show fine-tuning with limited resources

### Write-up Topics
- Attention is all you need
- BERT vs GPT: encoder vs decoder
- Why fine-tuning works
- Making fine-tuning affordable with LoRA

---

## Resources

### Documentation
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [PEFT Library](https://huggingface.co/docs/peft/)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

### Papers
- "Attention Is All You Need" (Vaswani et al., 2017)
- "BERT: Pre-training of Deep Bidirectional Transformers"
- "LoRA: Low-Rank Adaptation of Large Language Models"

### Models
- `bert-base-uncased`
- `gpt2`
- `t5-small`

---

## Next Month Preview

**Month 04**: Computer Vision — CNN, YOLO, and visual understanding with PyTorch and OpenCV.
