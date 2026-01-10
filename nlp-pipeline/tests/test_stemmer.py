"""Tests for the Stemmer class."""

import pytest

from nlp_pipeline import Stemmer, Tokenizer


class TestStemmer:
    """Test suite for Stemmer."""

    def test_porter_stem_single_word(self):
        """Test Porter stemmer on single words."""
        stemmer = Stemmer(algorithm="porter")
        assert stemmer.stem("running") == "run"
        assert stemmer.stem("jumps") == "jump"
        assert stemmer.stem("easily") == "easili"

    def test_snowball_stem_single_word(self):
        """Test Snowball stemmer on single words."""
        stemmer = Stemmer(algorithm="snowball", language="english")
        assert stemmer.stem("running") == "run"
        assert stemmer.stem("jumps") == "jump"

    def test_stem_tokens(self):
        """Test stemming a list of tokens."""
        stemmer = Stemmer()
        tokens = ["running", "jumps", "easily", "cats"]
        result = stemmer.stem_tokens(tokens)
        assert result == ["run", "jump", "easili", "cat"]

    def test_stem_text_with_tokenizer(self):
        """Test stemming text with tokenizer."""
        stemmer = Stemmer()
        tokenizer = Tokenizer()
        result = stemmer.stem_text("The cats are running", tokenizer)
        assert "cat" in result
        assert "run" in result

    def test_stem_text_without_tokenizer(self):
        """Test stemming text with basic split."""
        stemmer = Stemmer()
        result = stemmer.stem_text("cats running quickly")
        assert "cat" in result
        assert "run" in result

    def test_empty_word(self):
        """Test stemming empty string."""
        stemmer = Stemmer()
        assert stemmer.stem("") == ""

    def test_empty_token_list(self):
        """Test stemming empty list."""
        stemmer = Stemmer()
        assert stemmer.stem_tokens([]) == []

    def test_invalid_algorithm(self):
        """Test that invalid algorithm raises error."""
        with pytest.raises(ValueError, match="not supported"):
            Stemmer(algorithm="invalid")

    def test_invalid_snowball_language(self):
        """Test that invalid Snowball language raises error."""
        with pytest.raises(ValueError, match="not supported by Snowball"):
            Stemmer(algorithm="snowball", language="klingon")

    def test_snowball_spanish(self):
        """Test Snowball stemmer with Spanish."""
        stemmer = Stemmer(algorithm="snowball", language="spanish")
        assert stemmer.stem("corriendo") == "corr"
        assert stemmer.stem("gatos") == "gat"

    def test_snowball_german(self):
        """Test Snowball stemmer with German."""
        stemmer = Stemmer(algorithm="snowball", language="german")
        # German stemmer handles common suffixes
        assert stemmer.stem("katzen") == "katz"

    def test_porter_vs_snowball(self):
        """Test that Porter and Snowball can give different results."""
        porter = Stemmer(algorithm="porter")
        snowball = Stemmer(algorithm="snowball")
        # Both should handle common cases similarly
        assert porter.stem("running") == snowball.stem("running")

    def test_preserves_case_behavior(self):
        """Test stemmer behavior with different cases."""
        stemmer = Stemmer()
        # Porter stemmer lowercases internally
        result_lower = stemmer.stem("running")
        result_upper = stemmer.stem("RUNNING")
        # Both should produce lowercase output
        assert result_lower == "run"
        assert result_upper == "run"

    def test_supported_algorithms_attribute(self):
        """Test that supported algorithms are accessible."""
        assert "porter" in Stemmer.SUPPORTED_ALGORITHMS
        assert "snowball" in Stemmer.SUPPORTED_ALGORITHMS

    def test_snowball_languages_attribute(self):
        """Test that Snowball languages are accessible."""
        assert "english" in Stemmer.SNOWBALL_LANGUAGES
        assert "spanish" in Stemmer.SNOWBALL_LANGUAGES
        assert "german" in Stemmer.SNOWBALL_LANGUAGES
