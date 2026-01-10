"""Tests for the StopwordRemover class."""

import pytest

from nlp_pipeline import StopwordRemover, Tokenizer


class TestStopwordRemover:
    """Test suite for StopwordRemover."""

    def test_remove_basic_stopwords(self):
        """Test removal of common English stopwords."""
        remover = StopwordRemover()
        tokens = ["the", "quick", "brown", "fox", "is", "a", "animal"]
        result = remover.remove(tokens)
        assert "the" not in result
        assert "is" not in result
        assert "a" not in result
        assert "quick" in result
        assert "brown" in result
        assert "fox" in result

    def test_is_stopword(self):
        """Test stopword checking."""
        remover = StopwordRemover()
        assert remover.is_stopword("the") is True
        assert remover.is_stopword("The") is True  # Case insensitive
        assert remover.is_stopword("fox") is False

    def test_extra_stopwords(self):
        """Test adding custom stopwords."""
        remover = StopwordRemover(extra_stopwords=["fox", "dog"])
        tokens = ["the", "quick", "fox", "jumps"]
        result = remover.remove(tokens)
        assert "fox" not in result
        assert "quick" in result
        assert "jumps" in result

    def test_keep_words(self):
        """Test keeping specific words that would normally be removed."""
        remover = StopwordRemover(keep_words=["the", "a"])
        tokens = ["the", "quick", "is", "a", "fox"]
        result = remover.remove(tokens)
        assert "the" in result
        assert "a" in result
        assert "is" not in result

    def test_stopwords_property(self):
        """Test accessing the stopword set."""
        remover = StopwordRemover()
        stopwords = remover.stopwords
        assert "the" in stopwords
        assert "and" in stopwords
        assert isinstance(stopwords, set)

    def test_empty_list(self):
        """Test handling of empty token list."""
        remover = StopwordRemover()
        assert remover.remove([]) == []

    def test_all_stopwords(self):
        """Test when all tokens are stopwords."""
        remover = StopwordRemover()
        tokens = ["the", "a", "is", "are", "was"]
        result = remover.remove(tokens)
        assert result == []

    def test_no_stopwords(self):
        """Test when no tokens are stopwords."""
        remover = StopwordRemover()
        tokens = ["quick", "brown", "fox"]
        result = remover.remove(tokens)
        assert result == tokens

    def test_case_insensitive_removal(self):
        """Test that removal is case insensitive."""
        remover = StopwordRemover()
        tokens = ["The", "QUICK", "Brown", "IS", "Fox"]
        result = remover.remove(tokens)
        assert "The" not in result
        assert "IS" not in result
        assert "QUICK" in result
        assert "Brown" in result

    def test_remove_from_text_with_tokenizer(self):
        """Test removing stopwords directly from text using tokenizer."""
        remover = StopwordRemover()
        tokenizer = Tokenizer()
        result = remover.remove_from_text("The quick brown fox", tokenizer)
        assert "the" not in result
        assert "quick" in result
        assert "brown" in result
        assert "fox" in result

    def test_remove_from_text_without_tokenizer(self):
        """Test removing stopwords with basic split."""
        remover = StopwordRemover()
        result = remover.remove_from_text("The quick brown fox")
        assert "the" not in result
        assert "quick" in result
