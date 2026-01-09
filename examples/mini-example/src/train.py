"""Training Script."""

import csv
from pathlib import Path

from model import SentimentModel


def load_data(path: str) -> tuple[list[str], list[str]]:
    """Load training data from CSV."""
    texts = []
    labels = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["text"])
            labels.append(row["label"])

    return texts, labels


def main():
    """Train the sentiment model."""
    print("Loading data...")

    # Use sample data if available, otherwise use built-in examples
    data_path = Path(__file__).parent.parent / "data" / "sample.csv"

    if data_path.exists():
        texts, labels = load_data(str(data_path))
    else:
        # Built-in sample data
        texts = [
            "This movie was amazing and wonderful!",
            "I loved every moment of this film",
            "Great acting and beautiful cinematography",
            "A masterpiece of modern cinema",
            "Highly recommend this movie",
            "This was terrible and boring",
            "I hated this movie so much",
            "Waste of time, do not watch",
            "Poor acting and bad script",
            "The worst movie I have ever seen",
        ]
        labels = [
            "positive",
            "positive",
            "positive",
            "positive",
            "positive",
            "negative",
            "negative",
            "negative",
            "negative",
            "negative",
        ]

    print(f"Loaded {len(texts)} samples")

    print("Training model...")
    model = SentimentModel()
    accuracy = model.train(texts, labels)

    print(f"Accuracy: {accuracy:.2f}")

    # Save model
    model_path = Path(__file__).parent.parent / "model.json"
    model.save(str(model_path))
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    main()
