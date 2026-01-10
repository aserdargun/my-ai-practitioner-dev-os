"""Stemming module with Porter and Snowball stemmers."""

from typing import Literal

from nltk.stem import PorterStemmer, SnowballStemmer


class Stemmer:
    """Word stemmer supporting multiple algorithms."""

    SUPPORTED_ALGORITHMS = ("porter", "snowball")
    SNOWBALL_LANGUAGES = SnowballStemmer.languages

    def __init__(
        self,
        algorithm: Literal["porter", "snowball"] = "porter",
        language: str = "english",
    ):
        """Initialize stemmer.

        Args:
            algorithm: Stemming algorithm - 'porter' or 'snowball'.
            language: Language for Snowball stemmer (ignored for Porter).

        Raises:
            ValueError: If algorithm is not supported or language is invalid.
        """
        if algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(
                f"Algorithm '{algorithm}' not supported. "
                f"Choose from: {self.SUPPORTED_ALGORITHMS}"
            )

        self.algorithm = algorithm
        self.language = language

        if algorithm == "porter":
            self._stemmer = PorterStemmer()
        else:
            if language not in self.SNOWBALL_LANGUAGES:
                raise ValueError(
                    f"Language '{language}' not supported by Snowball. "
                    f"Choose from: {self.SNOWBALL_LANGUAGES}"
                )
            self._stemmer = SnowballStemmer(language)

    def stem(self, word: str) -> str:
        """Stem a single word.

        Args:
            word: Word to stem.

        Returns:
            Stemmed word.
        """
        if not word:
            return word
        return self._stemmer.stem(word)

    def stem_tokens(self, tokens: list[str]) -> list[str]:
        """Stem a list of tokens.

        Args:
            tokens: List of words to stem.

        Returns:
            List of stemmed words.
        """
        return [self.stem(token) for token in tokens]

    def stem_text(self, text: str, tokenizer=None) -> list[str]:
        """Tokenize text and stem all words.

        Args:
            text: Input text.
            tokenizer: Optional Tokenizer instance. Uses basic split if None.

        Returns:
            List of stemmed tokens.
        """
        if tokenizer:
            tokens = tokenizer.tokenize_words(text)
        else:
            tokens = text.split()

        return self.stem_tokens(tokens)
