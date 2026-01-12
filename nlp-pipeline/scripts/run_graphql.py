#!/usr/bin/env python3
"""Run the GraphQL API server.

Usage:
    python scripts/run_graphql.py [--port PORT] [--embeddings PATH]

Examples:
    # Run with sample embeddings
    python scripts/run_graphql.py

    # Run with custom embeddings file
    python scripts/run_graphql.py --embeddings data/glove.6B.50d.txt

    # Run on different port
    python scripts/run_graphql.py --port 8080
"""

import argparse
import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nlp_pipeline.embeddings import WordEmbeddings
from nlp_pipeline.graphql import create_app


def create_sample_embeddings() -> WordEmbeddings:
    """Create sample embeddings for demo."""
    embeddings = WordEmbeddings.from_dict({
        # Royalty
        "king": [0.5, 0.7, -0.2, 0.1, 0.3],
        "queen": [0.5, 0.6, 0.3, 0.1, 0.3],
        "prince": [0.4, 0.6, -0.1, 0.2, 0.2],
        "princess": [0.4, 0.5, 0.2, 0.2, 0.2],
        # Gender
        "man": [0.2, 0.3, -0.5, 0.4, 0.1],
        "woman": [0.2, 0.2, 0.4, 0.4, 0.1],
        "boy": [0.1, 0.2, -0.4, 0.3, 0.0],
        "girl": [0.1, 0.1, 0.3, 0.3, 0.0],
        # Animals
        "dog": [-0.3, 0.1, 0.0, -0.5, 0.6],
        "cat": [-0.2, 0.1, 0.1, -0.5, 0.5],
        "puppy": [-0.3, 0.0, -0.1, -0.4, 0.5],
        "kitten": [-0.2, 0.0, 0.0, -0.4, 0.4],
        # Food
        "apple": [-0.5, -0.3, 0.1, 0.2, -0.4],
        "banana": [-0.4, -0.3, 0.0, 0.2, -0.3],
        "orange": [-0.5, -0.2, 0.0, 0.2, -0.3],
        # Actions
        "run": [0.0, -0.5, -0.2, -0.2, 0.1],
        "walk": [0.0, -0.4, -0.1, -0.1, 0.0],
        "jump": [0.1, -0.5, -0.3, -0.2, 0.2],
        # Adjectives
        "good": [0.3, 0.1, 0.2, 0.0, -0.2],
        "bad": [-0.3, -0.1, -0.2, 0.0, 0.2],
        "happy": [0.4, 0.2, 0.3, 0.1, -0.1],
        "sad": [-0.4, -0.2, -0.3, -0.1, 0.1],
    })
    return embeddings


def load_embeddings(path: str) -> WordEmbeddings:
    """Load embeddings from file."""
    embeddings = WordEmbeddings()
    path_obj = Path(path)

    if path_obj.suffix in (".txt", ".vec"):
        # Try Word2Vec format first (has header)
        try:
            embeddings.load_word2vec_format(path, limit=50000)
        except (ValueError, IndexError):
            # Fall back to GloVe format (no header)
            embeddings = WordEmbeddings()
            embeddings.load_glove_format(path, limit=50000)
    else:
        raise ValueError(f"Unsupported file format: {path_obj.suffix}")

    return embeddings


def main():
    parser = argparse.ArgumentParser(description="Run GraphQL API server")
    parser.add_argument(
        "--port",
        type=int,
        default=8081,
        help="Port to run server on (default: 8081)",
    )
    parser.add_argument(
        "--embeddings",
        type=str,
        default=None,
        help="Path to embeddings file (default: use sample embeddings)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode",
    )
    args = parser.parse_args()

    # Load embeddings
    if args.embeddings:
        print(f"Loading embeddings from {args.embeddings}...")
        embeddings = load_embeddings(args.embeddings)
        print(f"Loaded {embeddings.vocab_size} words, {embeddings.dimension} dimensions")
    else:
        print("Using sample embeddings (23 words, 5 dimensions)")
        embeddings = create_sample_embeddings()

    # Create and run app
    app = create_app(embeddings)
    print(f"\nGraphQL API running at http://localhost:{args.port}/graphql")
    print(f"GraphiQL interface at http://localhost:{args.port}/graphql")
    print("\nExample queries:")
    print('  { info { vocabSize dimension } }')
    print('  { similarity(word1: "king", word2: "queen") }')
    print('  { mostSimilar(word: "king", topN: 5) { word similarity } }')
    print('  { analogy(positive: ["king", "woman"], negative: ["man"]) { word similarity } }')
    print("\nPress Ctrl+C to stop")

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
