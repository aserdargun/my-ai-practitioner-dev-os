# Mini Example: Sentiment Classifier

A complete, runnable example showing "done looks like this" for the AI Practitioner curriculum.

## What This Example Demonstrates

- Simple ML pipeline from data to prediction
- Clean project structure
- Working tests
- Documentation

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run training
python src/train.py

# Run inference
python src/predict.py "This movie was amazing!"

# Run tests
pytest
```

## Project Structure

```
mini-example/
├── src/
│   ├── README.md       # Source code docs
│   ├── train.py        # Training script
│   ├── predict.py      # Inference script
│   └── model.py        # Model definition
├── tests/
│   ├── README.md       # Test docs
│   └── test_model.py   # Unit tests
├── data/
│   └── sample.csv      # Sample dataset
├── pyproject.toml      # Dependencies
└── README.md           # This file
```

## The Model

This example implements a simple sentiment classifier using a bag-of-words approach:

1. **Preprocessing**: Tokenize and normalize text
2. **Features**: Word frequency vectors
3. **Classification**: Threshold-based positive/negative

This is intentionally simple to focus on project structure rather than ML complexity.

## Expected Output

### Training
```
$ python src/train.py
Loading data...
Training model...
Accuracy: 0.85
Model saved to model.json
```

### Prediction
```
$ python src/predict.py "This product is great!"
Sentiment: positive (confidence: 0.82)

$ python src/predict.py "Terrible experience, would not recommend"
Sentiment: negative (confidence: 0.75)
```

### Tests
```
$ pytest
tests/test_model.py::test_tokenize PASSED
tests/test_model.py::test_train PASSED
tests/test_model.py::test_predict_positive PASSED
tests/test_model.py::test_predict_negative PASSED
```

## Learning Outcomes

After studying this example, you should understand:

1. **Project Structure**: How to organize ML code
2. **Separation of Concerns**: Train vs predict vs model
3. **Testing**: How to test ML code
4. **Documentation**: README and code comments

## Next Steps

1. Replace the simple model with a neural network
2. Add more sophisticated preprocessing
3. Implement cross-validation
4. Add metrics tracking with MLflow
5. Create a FastAPI service (see templates/)

## Curriculum Connection

This example is relevant for:
- **Month 01**: NLP Foundations
- **Month 02**: Sequence Models (upgrade to RNN)
- **Month 06**: API Development (add FastAPI)
