"""Tests for the dashboard module."""

import numpy as np
import pandas as pd

from nlp_pipeline import WordEmbeddings
from nlp_pipeline.dashboard.app import (
    _compute_tsne,
    _create_sample_embeddings,
    _create_tsne_figure,
    create_app,
)


class TestDashboardApp:
    """Test suite for dashboard application."""

    def test_create_app(self):
        """Test that create_app returns a Dash app."""
        app = create_app()
        assert app is not None
        assert app.title == "NLP Pipeline Dashboard"

    def test_create_app_with_custom_embeddings(self):
        """Test create_app with custom embeddings."""
        embeddings = WordEmbeddings.from_dict({
            "test": [0.1, 0.2, 0.3],
            "word": [0.4, 0.5, 0.6],
        })
        app = create_app(embeddings)
        assert app is not None

    def test_app_has_required_components(self):
        """Test that app layout contains required components."""
        app = create_app()
        layout = app.layout

        # Check layout is not None
        assert layout is not None

        # Convert to string to check for component IDs
        layout_str = str(layout)
        assert "tsne-plot" in layout_str
        assert "search-input" in layout_str
        assert "search-button" in layout_str
        assert "analogy-button" in layout_str


class TestSampleEmbeddings:
    """Test suite for sample embeddings."""

    def test_create_sample_embeddings(self):
        """Test sample embeddings creation."""
        embeddings = _create_sample_embeddings()

        assert embeddings is not None
        assert embeddings.vocab_size > 0
        assert embeddings.dimension > 0

    def test_sample_embeddings_contains_expected_words(self):
        """Test that sample embeddings contain expected words."""
        embeddings = _create_sample_embeddings()

        # Check for royalty words
        assert "king" in embeddings
        assert "queen" in embeddings

        # Check for sentiment words
        assert "happy" in embeddings
        assert "sad" in embeddings

    def test_sample_embeddings_similarity(self):
        """Test that similar words have high similarity."""
        embeddings = _create_sample_embeddings()

        # King should be more similar to queen than to sad
        sim_king_queen = embeddings.similarity("king", "queen")
        sim_king_sad = embeddings.similarity("king", "sad")

        assert sim_king_queen > sim_king_sad


class TestTSNE:
    """Test suite for t-SNE computation."""

    def test_compute_tsne(self):
        """Test t-SNE computation."""
        embeddings = _create_sample_embeddings()
        df = _compute_tsne(embeddings)

        assert isinstance(df, pd.DataFrame)
        assert "word" in df.columns
        assert "x" in df.columns
        assert "y" in df.columns

    def test_compute_tsne_dimensions(self):
        """Test t-SNE output dimensions."""
        embeddings = _create_sample_embeddings()
        df = _compute_tsne(embeddings)

        # Should have same number of rows as words
        assert len(df) <= embeddings.vocab_size

        # x and y should be numeric
        assert df["x"].dtype in [np.float32, np.float64]
        assert df["y"].dtype in [np.float32, np.float64]

    def test_compute_tsne_max_words(self):
        """Test t-SNE respects max_words limit."""
        embeddings = _create_sample_embeddings()
        df = _compute_tsne(embeddings, max_words=5)

        assert len(df) == 5

    def test_compute_tsne_small_dataset(self):
        """Test t-SNE with very small dataset."""
        embeddings = WordEmbeddings.from_dict({
            "a": [0.1, 0.2],
            "b": [0.3, 0.4],
            "c": [0.5, 0.6],
            "d": [0.7, 0.8],
            "e": [0.9, 1.0],
            "f": [0.2, 0.3],
        })
        df = _compute_tsne(embeddings, max_words=6)

        assert len(df) == 6


class TestVisualization:
    """Test suite for visualization functions."""

    def test_create_tsne_figure(self):
        """Test t-SNE figure creation."""
        embeddings = _create_sample_embeddings()
        df = _compute_tsne(embeddings)
        fig = _create_tsne_figure(df)

        assert fig is not None
        assert hasattr(fig, "data")
        assert len(fig.data) > 0

    def test_tsne_figure_has_scatter_trace(self):
        """Test that figure contains scatter trace."""
        embeddings = _create_sample_embeddings()
        df = _compute_tsne(embeddings)
        fig = _create_tsne_figure(df)

        # First trace should be scatter
        assert fig.data[0].type == "scatter"

    def test_tsne_figure_has_correct_title(self):
        """Test figure has correct title."""
        embeddings = _create_sample_embeddings()
        df = _compute_tsne(embeddings)
        fig = _create_tsne_figure(df)

        assert fig.layout.title.text == "Word Embeddings Visualization"


class TestEmbeddingOperations:
    """Test embedding operations used by dashboard."""

    def test_most_similar(self):
        """Test most_similar functionality."""
        embeddings = _create_sample_embeddings()
        similar = embeddings.most_similar("king", topn=5)

        assert len(similar) == 5
        assert all(isinstance(item, tuple) for item in similar)
        assert all(len(item) == 2 for item in similar)

    def test_analogy(self):
        """Test analogy functionality."""
        embeddings = _create_sample_embeddings()
        results = embeddings.analogy(
            positive=["king", "woman"],
            negative=["man"],
            topn=3
        )

        assert len(results) == 3
        assert all(isinstance(item, tuple) for item in results)

    def test_word_not_in_vocab(self):
        """Test handling of unknown words."""
        embeddings = _create_sample_embeddings()

        assert "nonexistent_word" not in embeddings
