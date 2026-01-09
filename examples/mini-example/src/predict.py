"""Prediction Script."""

import argparse
import sys
from pathlib import Path

from model import SentimentModel


def main():
    """Run sentiment prediction."""
    parser = argparse.ArgumentParser(description="Predict sentiment of text")
    parser.add_argument("text", nargs="?", help="Text to classify")
    parser.add_argument(
        "--model",
        default=str(Path(__file__).parent.parent / "model.json"),
        help="Path to model file",
    )
    args = parser.parse_args()

    # Load model
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        print("Run 'python train.py' first to create the model.")
        sys.exit(1)

    model = SentimentModel.load(str(model_path))

    if args.text:
        # Single prediction
        result = model.predict(args.text)
        print(f"Sentiment: {result.label} (confidence: {result.confidence:.2f})")
    else:
        # Interactive mode
        print("Sentiment Classifier")
        print("Enter text to classify (Ctrl+C to exit)")
        print("-" * 40)

        while True:
            try:
                text = input("\n> ")
                if not text.strip():
                    continue

                result = model.predict(text)
                print(f"Sentiment: {result.label} (confidence: {result.confidence:.2f})")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break


if __name__ == "__main__":
    main()
