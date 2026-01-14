"""Neural network models."""

from .feedforward import FeedforwardClassifier
from .embedding_classifier import EmbeddingClassifier

__all__ = ["FeedforwardClassifier", "EmbeddingClassifier"]
