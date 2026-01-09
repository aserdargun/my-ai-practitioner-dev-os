# Source Code

This directory contains the core ML code for the mini-example.

## Files

| File | Purpose |
|------|---------|
| `model.py` | Model definition and utilities |
| `train.py` | Training script |
| `predict.py` | Inference script |

## Model Architecture

The sentiment classifier uses a simple bag-of-words approach:

```
Input Text
    ↓
Tokenization (lowercase, split)
    ↓
Feature Extraction (word frequencies)
    ↓
Scoring (positive - negative word counts)
    ↓
Classification (threshold-based)
```

## Usage

### Training
```python
from model import SentimentModel

model = SentimentModel()
model.train(texts, labels)
model.save("model.json")
```

### Inference
```python
model = SentimentModel.load("model.json")
result = model.predict("Some text to classify")
print(f"Sentiment: {result.label} ({result.confidence:.2f})")
```

## Extending

To improve this model:

1. **Better Tokenization**: Use NLTK or spaCy
2. **Word Embeddings**: Use Word2Vec or GloVe
3. **Neural Network**: Replace with RNN/LSTM
4. **Transformers**: Fine-tune BERT
