# Sequence Models

Month 2 project: RNN and LSTM sequence models with PyTorch.

## Goals

- Master PyTorch fundamentals (tensors, autograd, training loops)
- Implement RNN for sentiment classification
- Upgrade to LSTM and compare performance
- Build text generation model

## Setup

```bash
cd sequence-models
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev,data,notebook]"
```

## Structure

```
sequence-models/
├── src/sequence_models/
│   ├── __init__.py
│   ├── data/           # Data loading (Week 1)
│   ├── models/         # RNN, LSTM (Weeks 2-3)
│   ├── training/       # Training loop (Week 1)
│   └── generation/     # Text generation (Week 4)
├── tests/
├── notebooks/
└── checkpoints/
```

## Weekly Progress

### Week 1: PyTorch Foundations
- [ ] Project setup
- [ ] Tensors and autograd
- [ ] DataLoader patterns
- [ ] Training loop
- [ ] Feedforward baseline

### Week 2: RNN Implementation
- [ ] RNN architecture
- [ ] Sentiment classification
- [ ] Training and evaluation

### Week 3: LSTM Deep Dive
- [ ] LSTM cell mechanics
- [ ] Performance comparison
- [ ] Hyperparameter tuning

### Week 4: Generation & Polish
- [ ] Text generation model
- [ ] Sampling strategies
- [ ] Documentation and demo

## Run Tests

```bash
pytest
```

## Verify Setup

```bash
python -c "import torch; print(f'PyTorch {torch.__version__}')"
```
