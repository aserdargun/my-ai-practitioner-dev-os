"""Tests for the Tokenizer class."""


from nlp_pipeline.tokenizer import Tokenizer


class TestTokenizer:
    """Test suite for Tokenizer."""

    def test_word_tokenize_simple(self):
        """Test basic word tokenization."""
        tokenizer = Tokenizer()
        result = tokenizer.tokenize_words("Hello world")
        assert result == ["hello", "world"]

    def test_word_tokenize_with_punctuation(self):
        """Test word tokenization handles punctuation."""
        tokenizer = Tokenizer()
        result = tokenizer.tokenize_words("Hello, world!")
        assert "hello" in result
        assert "world" in result

    def test_sentence_tokenize(self):
        """Test sentence tokenization."""
        tokenizer = Tokenizer()
        text = "First sentence. Second sentence. Third one!"
        result = tokenizer.tokenize_sentences(text)
        assert len(result) == 3

    def test_empty_string(self):
        """Test handling of empty string."""
        tokenizer = Tokenizer()
        assert tokenizer.tokenize_words("") == []
        assert tokenizer.tokenize_sentences("") == []

    def test_whitespace_only(self):
        """Test handling of whitespace-only string."""
        tokenizer = Tokenizer()
        assert tokenizer.tokenize_words("   ") == []

    def test_lowercase_option(self):
        """Test lowercase option."""
        tokenizer_lower = Tokenizer(lowercase=True)
        tokenizer_preserve = Tokenizer(lowercase=False)

        text = "Hello World"
        assert tokenizer_lower.tokenize_words(text) == ["hello", "world"]
        assert "Hello" in tokenizer_preserve.tokenize_words(text)

    def test_tokenize_level_parameter(self):
        """Test the level parameter in tokenize method."""
        tokenizer = Tokenizer()
        text = "Hello world. How are you?"

        words = tokenizer.tokenize(text, level="word")
        sentences = tokenizer.tokenize(text, level="sentence")

        assert len(words) > len(sentences)
        assert len(sentences) == 2
