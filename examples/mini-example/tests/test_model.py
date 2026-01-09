"""Tests for sentiment model."""

import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from model import PredictionResult, SentimentModel


@pytest.fixture
def trained_model():
    """Create a trained model for testing."""
    model = SentimentModel()

    texts = [
        "This is great and wonderful",
        "I love this amazing product",
        "Excellent quality, highly recommend",
        "This is terrible and awful",
        "I hate this bad product",
        "Poor quality, do not buy",
    ]
    labels = [
        "positive",
        "positive",
        "positive",
        "negative",
        "negative",
        "negative",
    ]

    model.train(texts, labels)
    return model


def test_tokenize():
    """Test tokenization."""
    model = SentimentModel()

    tokens = model.tokenize("Hello, World! This is a TEST.")
    assert tokens == ["hello", "world", "this", "is", "a", "test"]


def test_tokenize_empty():
    """Test tokenization of empty string."""
    model = SentimentModel()
    tokens = model.tokenize("")
    assert tokens == []


def test_train(trained_model):
    """Test that training sets up the model."""
    assert trained_model.is_trained
    assert len(trained_model.positive_words) > 0
    assert len(trained_model.negative_words) > 0


def test_train_accuracy():
    """Test training returns reasonable accuracy."""
    model = SentimentModel()

    texts = ["good great excellent"] * 5 + ["bad terrible awful"] * 5
    labels = ["positive"] * 5 + ["negative"] * 5

    accuracy = model.train(texts, labels)
    assert accuracy >= 0.8  # Should achieve high accuracy on clear data


def test_predict_positive(trained_model):
    """Test prediction of positive sentiment."""
    result = trained_model.predict("This is great and wonderful!")

    assert isinstance(result, PredictionResult)
    assert result.label == "positive"
    assert result.confidence > 0.5


def test_predict_negative(trained_model):
    """Test prediction of negative sentiment."""
    result = trained_model.predict("This is terrible and awful!")

    assert isinstance(result, PredictionResult)
    assert result.label == "negative"
    assert result.confidence > 0.5


def test_predict_neutral():
    """Test prediction on neutral/unknown text."""
    model = SentimentModel()
    model.is_trained = True  # Empty model

    result = model.predict("The quick brown fox jumps over the lazy dog")

    assert result.confidence == 0.5  # No signal


def test_save_load(trained_model):
    """Test model serialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "model.json"

        # Save
        trained_model.save(str(path))
        assert path.exists()

        # Load
        loaded = SentimentModel.load(str(path))

        assert loaded.is_trained
        assert loaded.positive_words == trained_model.positive_words
        assert loaded.negative_words == trained_model.negative_words


def test_confidence_bounds(trained_model):
    """Test confidence is always in valid range."""
    test_texts = [
        "amazing wonderful great excellent",
        "terrible horrible awful bad",
        "neutral ordinary regular normal",
        "",
        "x",
    ]

    for text in test_texts:
        result = trained_model.predict(text)
        assert 0.0 <= result.confidence <= 1.0
