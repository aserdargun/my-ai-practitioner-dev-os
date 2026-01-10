"""Tests for the WordEmbeddings class."""

import tempfile

import numpy as np
import pytest

from nlp_pipeline import WordEmbeddings


def create_sample_embeddings() -> WordEmbeddings:
    """Create sample embeddings for testing."""
    # Simple embeddings where similar concepts have similar vectors
    embeddings = WordEmbeddings.from_dict({
        "king": [0.9, 0.1, 0.0, 0.5],
        "queen": [0.85, 0.15, 0.0, 0.5],
        "man": [0.5, 0.1, 0.0, 0.9],
        "woman": [0.45, 0.15, 0.0, 0.9],
        "prince": [0.8, 0.2, 0.0, 0.6],
        "princess": [0.75, 0.25, 0.0, 0.6],
        "dog": [0.0, 0.9, 0.1, 0.0],
        "cat": [0.0, 0.85, 0.15, 0.0],
        "puppy": [0.0, 0.8, 0.2, 0.0],
        "car": [0.0, 0.0, 0.9, 0.1],
    })
    return embeddings


class TestWordEmbeddings:
    """Test suite for WordEmbeddings."""

    def test_from_dict(self):
        """Test creating embeddings from dictionary."""
        embeddings = create_sample_embeddings()
        assert embeddings.vocab_size == 10
        assert embeddings.dimension == 4

    def test_contains(self):
        """Test word membership check."""
        embeddings = create_sample_embeddings()
        assert "king" in embeddings
        assert "notaword" not in embeddings

    def test_getitem(self):
        """Test getting vector by word."""
        embeddings = create_sample_embeddings()
        vec = embeddings["king"]
        assert isinstance(vec, np.ndarray)
        assert len(vec) == 4

    def test_get_with_default(self):
        """Test get with default value."""
        embeddings = create_sample_embeddings()
        assert embeddings.get("king") is not None
        assert embeddings.get("notaword") is None
        default = np.zeros(4)
        assert np.array_equal(embeddings.get("notaword", default), default)

    def test_len(self):
        """Test vocabulary length."""
        embeddings = create_sample_embeddings()
        assert len(embeddings) == 10

    def test_vocab(self):
        """Test getting vocabulary list."""
        embeddings = create_sample_embeddings()
        vocab = embeddings.vocab
        assert "king" in vocab
        assert "queen" in vocab
        assert len(vocab) == 10

    def test_similarity(self):
        """Test similarity calculation."""
        embeddings = create_sample_embeddings()
        # King and queen should be similar
        sim_royals = embeddings.similarity("king", "queen")
        # King and car should be dissimilar
        sim_diff = embeddings.similarity("king", "car")
        assert sim_royals > sim_diff
        assert sim_royals > 0.9

    def test_most_similar(self):
        """Test finding most similar words."""
        embeddings = create_sample_embeddings()
        similar = embeddings.most_similar("king", topn=3)
        assert len(similar) == 3
        # Queen should be most similar to king
        words = [w for w, _ in similar]
        assert "queen" in words
        # Check that similarity scores are in descending order
        scores = [s for _, s in similar]
        assert scores == sorted(scores, reverse=True)

    def test_most_similar_to_vector(self):
        """Test finding similar words to a vector."""
        embeddings = create_sample_embeddings()
        vec = np.array([0.9, 0.1, 0.0, 0.5])
        similar = embeddings.most_similar_to_vector(vec, topn=2)
        assert len(similar) == 2
        # King should be closest to this vector
        assert similar[0][0] == "king"

    def test_analogy(self):
        """Test word analogy (king - man + woman = queen)."""
        embeddings = create_sample_embeddings()
        results = embeddings.analogy(
            positive=["king", "woman"],
            negative=["man"],
            topn=3,
        )
        words = [w for w, _ in results]
        # Queen should be in top results
        assert "queen" in words

    def test_doesnt_match(self):
        """Test finding outlier word."""
        embeddings = create_sample_embeddings()
        # Car doesn't match royalty
        outlier = embeddings.doesnt_match(["king", "queen", "prince", "car"])
        assert outlier == "car"

    def test_doesnt_match_single_word(self):
        """Test doesnt_match with single word."""
        embeddings = create_sample_embeddings()
        assert embeddings.doesnt_match(["king"]) == "king"

    def test_doesnt_match_empty(self):
        """Test doesnt_match with empty list."""
        embeddings = create_sample_embeddings()
        assert embeddings.doesnt_match([]) == ""

    def test_add_word(self):
        """Test adding a new word."""
        embeddings = create_sample_embeddings()
        new_vec = np.array([0.1, 0.2, 0.3, 0.4])
        embeddings.add_word("newword", new_vec)
        assert "newword" in embeddings
        assert np.allclose(embeddings["newword"], new_vec)

    def test_add_word_wrong_dimension(self):
        """Test adding word with wrong dimension."""
        embeddings = create_sample_embeddings()
        with pytest.raises(ValueError, match="dimension"):
            embeddings.add_word("bad", np.array([0.1, 0.2]))

    def test_repr(self):
        """Test string representation."""
        embeddings = create_sample_embeddings()
        repr_str = repr(embeddings)
        assert "WordEmbeddings" in repr_str
        assert "10" in repr_str
        assert "4" in repr_str


class TestWordEmbeddingsFileLoading:
    """Test file loading functionality."""

    def test_load_word2vec_format(self):
        """Test loading Word2Vec text format."""
        content = """3 4
king 0.9 0.1 0.0 0.5
queen 0.85 0.15 0.0 0.5
man 0.5 0.1 0.0 0.9
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(content)
            f.flush()

            embeddings = WordEmbeddings()
            embeddings.load_word2vec_format(f.name)

            assert embeddings.vocab_size == 3
            assert embeddings.dimension == 4
            assert "king" in embeddings
            assert "queen" in embeddings

    def test_load_glove_format(self):
        """Test loading GloVe format (no header)."""
        content = """king 0.9 0.1 0.0 0.5
queen 0.85 0.15 0.0 0.5
man 0.5 0.1 0.0 0.9
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(content)
            f.flush()

            embeddings = WordEmbeddings()
            embeddings.load_glove_format(f.name)

            assert embeddings.vocab_size == 3
            assert embeddings.dimension == 4
            assert "king" in embeddings

    def test_load_with_limit(self):
        """Test loading with vocabulary limit."""
        content = """5 4
word1 0.1 0.2 0.3 0.4
word2 0.1 0.2 0.3 0.4
word3 0.1 0.2 0.3 0.4
word4 0.1 0.2 0.3 0.4
word5 0.1 0.2 0.3 0.4
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(content)
            f.flush()

            embeddings = WordEmbeddings()
            embeddings.load_word2vec_format(f.name, limit=2)

            assert embeddings.vocab_size == 2

    def test_load_method_chaining(self):
        """Test that load methods return self for chaining."""
        content = """1 4
test 0.1 0.2 0.3 0.4
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(content)
            f.flush()

            embeddings = WordEmbeddings().load_word2vec_format(f.name)
            assert embeddings.vocab_size == 1

    def test_empty_embeddings(self):
        """Test empty embeddings object."""
        embeddings = WordEmbeddings()
        assert embeddings.vocab_size == 0
        assert embeddings.dimension == 0
        assert len(embeddings) == 0
