#!/usr/bin/env python
"""Run the NLP Pipeline Dashboard.

This script launches the interactive dashboard for exploring word embeddings.

Usage:
    # With sample embeddings (default):
    python scripts/run_dashboard.py

    # With custom Word2Vec embeddings:
    python scripts/run_dashboard.py --embeddings path/to/embeddings.txt

    # With GloVe embeddings:
    python scripts/run_dashboard.py --embeddings path/to/glove.txt --format glove
"""

import argparse
import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nlp_pipeline import WordEmbeddings
from nlp_pipeline.dashboard import run_dashboard


def main():
    parser = argparse.ArgumentParser(
        description="Run the NLP Pipeline Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--embeddings", "-e",
        type=str,
        help="Path to embeddings file (optional, uses sample data if not provided)"
    )
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["word2vec", "glove"],
        default="word2vec",
        help="Embeddings format (default: word2vec)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=5000,
        help="Maximum number of words to load (default: 5000)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8050,
        help="Port to run dashboard on (default: 8050)"
    )
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )

    args = parser.parse_args()

    embeddings = None

    if args.embeddings:
        path = Path(args.embeddings)
        if not path.exists():
            print(f"Error: Embeddings file not found: {path}")
            sys.exit(1)

        print(f"Loading embeddings from {path}...")
        embeddings = WordEmbeddings()

        if args.format == "glove":
            embeddings.load_glove_format(path, limit=args.limit)
        else:
            embeddings.load_word2vec_format(path, limit=args.limit)

        print(f"Loaded {embeddings.vocab_size} words ({embeddings.dimension}D)")
    else:
        print("Using sample embeddings (28 words)")
        print("Tip: Use --embeddings to load your own Word2Vec or GloVe file")

    print()
    run_dashboard(embeddings, debug=not args.no_debug, port=args.port)


if __name__ == "__main__":
    main()
