"""Tokenization module with multiple strategies."""

from typing import Literal

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


class Tokenizer:
    """Configurable text tokenizer using NLTK."""

    def __init__(
        self,
        lowercase: bool = True,
        language: str = "english",
    ):
        """Initialize tokenizer.

        Args:
            lowercase: Convert text to lowercase before tokenizing.
            language: Language for sentence tokenization.
        """
        self.lowercase = lowercase
        self.language = language
        self._ensure_nltk_data()

    def _ensure_nltk_data(self) -> None:
        """Download required NLTK data if not present."""
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)

    def tokenize(
        self,
        text: str,
        level: Literal["word", "sentence"] = "word",
    ) -> list[str]:
        """Tokenize text at word or sentence level.

        Args:
            text: Input text to tokenize.
            level: Tokenization level - 'word' or 'sentence'.

        Returns:
            List of tokens (words or sentences).
        """
        if not text or not text.strip():
            return []

        processed = text.lower() if self.lowercase else text

        if level == "sentence":
            return sent_tokenize(processed, language=self.language)
        return word_tokenize(processed, language=self.language)

    def tokenize_words(self, text: str) -> list[str]:
        """Tokenize text into words.

        Args:
            text: Input text.

        Returns:
            List of word tokens.
        """
        return self.tokenize(text, level="word")

    def tokenize_sentences(self, text: str) -> list[str]:
        """Tokenize text into sentences.

        Args:
            text: Input text.

        Returns:
            List of sentences.
        """
        return self.tokenize(text, level="sentence")
