"""Stopword removal module."""

import nltk
from nltk.corpus import stopwords


class StopwordRemover:
    """Remove stopwords from tokenized text."""

    def __init__(
        self,
        language: str = "english",
        extra_stopwords: list[str] | None = None,
        keep_words: list[str] | None = None,
    ):
        """Initialize stopword remover.

        Args:
            language: Language for stopword list (default: english).
            extra_stopwords: Additional words to treat as stopwords.
            keep_words: Words to exclude from stopword removal.
        """
        self.language = language
        self._ensure_nltk_data()

        self._stopwords = set(stopwords.words(language))

        if extra_stopwords:
            self._stopwords.update(word.lower() for word in extra_stopwords)

        if keep_words:
            self._stopwords -= set(word.lower() for word in keep_words)

    def _ensure_nltk_data(self) -> None:
        """Download required NLTK data if not present."""
        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            nltk.download("stopwords", quiet=True)

    @property
    def stopwords(self) -> set[str]:
        """Get the current stopword set."""
        return self._stopwords.copy()

    def is_stopword(self, word: str) -> bool:
        """Check if a word is a stopword.

        Args:
            word: Word to check.

        Returns:
            True if word is a stopword.
        """
        return word.lower() in self._stopwords

    def remove(self, tokens: list[str]) -> list[str]:
        """Remove stopwords from a list of tokens.

        Args:
            tokens: List of word tokens.

        Returns:
            List with stopwords removed.
        """
        return [token for token in tokens if token.lower() not in self._stopwords]

    def remove_from_text(self, text: str, tokenizer=None) -> list[str]:
        """Tokenize text and remove stopwords.

        Args:
            text: Input text.
            tokenizer: Optional Tokenizer instance. Uses basic split if None.

        Returns:
            List of tokens with stopwords removed.
        """
        if tokenizer:
            tokens = tokenizer.tokenize_words(text)
        else:
            tokens = text.lower().split()

        return self.remove(tokens)
