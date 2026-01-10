"""Tests for the Lemmatizer class."""

import pytest

from nlp_pipeline import Lemmatizer, Tokenizer


class TestLemmatizer:
    """Test suite for Lemmatizer."""

    def test_lemmatize_noun(self):
        """Test lemmatizing nouns."""
        lemmatizer = Lemmatizer()
        assert lemmatizer.lemmatize("cats") == "cat"
        assert lemmatizer.lemmatize("dogs") == "dog"
        assert lemmatizer.lemmatize("children") == "child"

    def test_lemmatize_verb(self):
        """Test lemmatizing verbs."""
        lemmatizer = Lemmatizer()
        assert lemmatizer.lemmatize("running", pos="verb") == "run"
        assert lemmatizer.lemmatize("ran", pos="verb") == "run"
        assert lemmatizer.lemmatize("goes", pos="verb") == "go"

    def test_lemmatize_adjective(self):
        """Test lemmatizing adjectives."""
        lemmatizer = Lemmatizer()
        assert lemmatizer.lemmatize("better", pos="adj") == "good"
        assert lemmatizer.lemmatize("best", pos="adj") == "best"

    def test_lemmatize_adverb(self):
        """Test lemmatizing adverbs."""
        lemmatizer = Lemmatizer()
        # Adverbs often don't change much
        assert lemmatizer.lemmatize("quickly", pos="adv") == "quickly"

    def test_default_pos_noun(self):
        """Test that default POS is noun."""
        lemmatizer = Lemmatizer()
        # Without verb POS, "running" treated as noun
        assert lemmatizer.lemmatize("running") == "running"
        # With verb POS
        assert lemmatizer.lemmatize("running", pos="verb") == "run"

    def test_custom_default_pos(self):
        """Test setting custom default POS."""
        lemmatizer = Lemmatizer(default_pos="verb")
        assert lemmatizer.lemmatize("running") == "run"

    def test_lemmatize_tokens(self):
        """Test lemmatizing a list of tokens."""
        lemmatizer = Lemmatizer()
        tokens = ["cats", "dogs", "mice"]
        result = lemmatizer.lemmatize_tokens(tokens)
        assert result == ["cat", "dog", "mouse"]

    def test_lemmatize_tokens_with_pos(self):
        """Test lemmatizing tokens with POS."""
        lemmatizer = Lemmatizer()
        tokens = ["running", "jumping", "swimming"]
        result = lemmatizer.lemmatize_tokens(tokens, pos="verb")
        assert result == ["run", "jump", "swim"]

    def test_lemmatize_text_with_tokenizer(self):
        """Test lemmatizing text with tokenizer."""
        lemmatizer = Lemmatizer()
        tokenizer = Tokenizer()
        result = lemmatizer.lemmatize_text("The cats are sleeping", tokenizer=tokenizer)
        assert "cat" in result
        assert "the" in result

    def test_lemmatize_text_without_tokenizer(self):
        """Test lemmatizing text with basic split."""
        lemmatizer = Lemmatizer()
        result = lemmatizer.lemmatize_text("cats dogs mice")
        assert result == ["cat", "dog", "mouse"]

    def test_empty_word(self):
        """Test lemmatizing empty string."""
        lemmatizer = Lemmatizer()
        assert lemmatizer.lemmatize("") == ""

    def test_empty_token_list(self):
        """Test lemmatizing empty list."""
        lemmatizer = Lemmatizer()
        assert lemmatizer.lemmatize_tokens([]) == []

    def test_case_handling(self):
        """Test that lemmatizer handles case correctly."""
        lemmatizer = Lemmatizer()
        assert lemmatizer.lemmatize("CATS") == "cat"
        assert lemmatizer.lemmatize("Dogs") == "dog"

    def test_lemmatize_with_pos_tags(self):
        """Test lemmatizing with Penn Treebank POS tags."""
        lemmatizer = Lemmatizer()
        tagged = [
            ("cats", "NNS"),
            ("running", "VBG"),
            ("quickly", "RB"),
        ]
        result = lemmatizer.lemmatize_with_pos_tags(tagged)
        assert result[0] == "cat"
        assert result[1] == "run"
        assert result[2] == "quickly"

    def test_penn_to_wordnet_verb(self):
        """Test Penn to WordNet POS conversion for verbs."""
        lemmatizer = Lemmatizer()
        tagged = [("running", "VBG"), ("ran", "VBD"), ("runs", "VBZ")]
        result = lemmatizer.lemmatize_with_pos_tags(tagged)
        assert all(r == "run" for r in result)

    def test_penn_to_wordnet_adjective(self):
        """Test Penn to WordNet POS conversion for adjectives."""
        lemmatizer = Lemmatizer()
        tagged = [("better", "JJR")]
        result = lemmatizer.lemmatize_with_pos_tags(tagged)
        assert result[0] == "good"

    def test_stemmer_vs_lemmatizer(self):
        """Compare stemmer and lemmatizer outputs."""
        from nlp_pipeline import Stemmer

        lemmatizer = Lemmatizer()
        stemmer = Stemmer()

        # Lemmatizer produces real words
        assert lemmatizer.lemmatize("better", pos="adj") == "good"
        # Stemmer just removes suffixes
        assert stemmer.stem("better") == "better"

        # Both reduce plurals
        assert lemmatizer.lemmatize("cats") == "cat"
        assert stemmer.stem("cats") == "cat"
