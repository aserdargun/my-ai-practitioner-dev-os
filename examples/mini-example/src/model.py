"""Sentiment Model Module."""

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PredictionResult:
    """Result of sentiment prediction."""

    label: str  # "positive" or "negative"
    confidence: float
    score: float  # Raw score before thresholding


class SentimentModel:
    """Simple bag-of-words sentiment classifier."""

    def __init__(self):
        """Initialize model."""
        self.positive_words: set[str] = set()
        self.negative_words: set[str] = set()
        self.threshold: float = 0.0
        self.is_trained: bool = False

    def tokenize(self, text: str) -> list[str]:
        """Tokenize text into words."""
        # Lowercase and extract words
        text = text.lower()
        words = re.findall(r"\b[a-z]+\b", text)
        return words

    def train(self, texts: list[str], labels: list[str]) -> float:
        """Train the model on labeled data.

        Args:
            texts: List of text samples
            labels: List of labels ("positive" or "negative")

        Returns:
            Training accuracy
        """
        # Count word frequencies by label
        positive_counts: dict[str, int] = {}
        negative_counts: dict[str, int] = {}

        for text, label in zip(texts, labels):
            words = self.tokenize(text)
            counts = positive_counts if label == "positive" else negative_counts

            for word in words:
                counts[word] = counts.get(word, 0) + 1

        # Select discriminative words
        all_words = set(positive_counts.keys()) | set(negative_counts.keys())

        for word in all_words:
            pos_count = positive_counts.get(word, 0)
            neg_count = negative_counts.get(word, 0)

            # Word is positive if it appears more in positive texts
            if pos_count > neg_count * 1.5:
                self.positive_words.add(word)
            elif neg_count > pos_count * 1.5:
                self.negative_words.add(word)

        self.is_trained = True

        # Calculate training accuracy
        correct = 0
        for text, label in zip(texts, labels):
            result = self.predict(text)
            if result.label == label:
                correct += 1

        return correct / len(texts) if texts else 0.0

    def predict(self, text: str) -> PredictionResult:
        """Predict sentiment of text."""
        words = self.tokenize(text)

        # Count positive and negative words
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)

        total = pos_count + neg_count
        if total == 0:
            # No signal, return neutral
            return PredictionResult(
                label="positive",
                confidence=0.5,
                score=0.0,
            )

        # Score: positive proportion
        score = (pos_count - neg_count) / total

        if score > self.threshold:
            label = "positive"
            confidence = 0.5 + (score * 0.5)
        else:
            label = "negative"
            confidence = 0.5 + (abs(score) * 0.5)

        return PredictionResult(
            label=label,
            confidence=min(confidence, 0.99),
            score=score,
        )

    def save(self, path: str) -> None:
        """Save model to file."""
        data = {
            "positive_words": list(self.positive_words),
            "negative_words": list(self.negative_words),
            "threshold": self.threshold,
        }

        Path(path).write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: str) -> "SentimentModel":
        """Load model from file."""
        data = json.loads(Path(path).read_text())

        model = cls()
        model.positive_words = set(data["positive_words"])
        model.negative_words = set(data["negative_words"])
        model.threshold = data["threshold"]
        model.is_trained = True

        return model
