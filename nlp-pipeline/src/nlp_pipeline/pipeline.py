"""Unified preprocessing pipeline."""

from typing import Literal

from nlp_pipeline.lemmatizer import Lemmatizer
from nlp_pipeline.stemmer import Stemmer
from nlp_pipeline.stopwords import StopwordRemover
from nlp_pipeline.tokenizer import Tokenizer

NormalizerType = Literal["stem", "lemmatize", None]


class Pipeline:
    """Unified text preprocessing pipeline.

    Chains together tokenization, stopword removal, and normalization
    (stemming or lemmatization) into a single configurable pipeline.
    """

    def __init__(
        self,
        lowercase: bool = True,
        remove_stopwords: bool = True,
        normalizer: NormalizerType = "lemmatize",
        language: str = "english",
        stemmer_algorithm: Literal["porter", "snowball"] = "porter",
        lemmatizer_pos: Literal["noun", "verb", "adj", "adv"] = "noun",
        extra_stopwords: list[str] | None = None,
        keep_stopwords: list[str] | None = None,
    ):
        """Initialize preprocessing pipeline.

        Args:
            lowercase: Convert text to lowercase.
            remove_stopwords: Remove stopwords from tokens.
            normalizer: Normalization method - 'stem', 'lemmatize', or None.
            language: Language for stopwords and Snowball stemmer.
            stemmer_algorithm: Stemming algorithm ('porter' or 'snowball').
            lemmatizer_pos: Default POS for lemmatization.
            extra_stopwords: Additional stopwords to remove.
            keep_stopwords: Words to keep (not remove as stopwords).
        """
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.normalizer = normalizer
        self.language = language

        # Initialize components
        self._tokenizer = Tokenizer(lowercase=lowercase, language=language)

        if remove_stopwords:
            self._stopword_remover = StopwordRemover(
                language=language,
                extra_stopwords=extra_stopwords,
                keep_words=keep_stopwords,
            )
        else:
            self._stopword_remover = None

        if normalizer == "stem":
            self._normalizer = Stemmer(
                algorithm=stemmer_algorithm,
                language=language,
            )
        elif normalizer == "lemmatize":
            self._normalizer = Lemmatizer(default_pos=lemmatizer_pos)
        else:
            self._normalizer = None

    def process(self, text: str) -> list[str]:
        """Process text through the full pipeline.

        Args:
            text: Input text to process.

        Returns:
            List of processed tokens.
        """
        # Step 1: Tokenize
        tokens = self._tokenizer.tokenize_words(text)

        # Step 2: Remove stopwords (if enabled)
        if self._stopword_remover:
            tokens = self._stopword_remover.remove(tokens)

        # Step 3: Normalize (if enabled)
        if self._normalizer:
            if isinstance(self._normalizer, Stemmer):
                tokens = self._normalizer.stem_tokens(tokens)
            else:
                tokens = self._normalizer.lemmatize_tokens(tokens)

        return tokens

    def __call__(self, text: str) -> list[str]:
        """Allow pipeline to be called directly.

        Args:
            text: Input text to process.

        Returns:
            List of processed tokens.
        """
        return self.process(text)

    def process_batch(self, texts: list[str]) -> list[list[str]]:
        """Process multiple texts.

        Args:
            texts: List of texts to process.

        Returns:
            List of processed token lists.
        """
        return [self.process(text) for text in texts]

    def fit(self, texts: list[str]) -> "Pipeline":
        """Placeholder for sklearn-style API (no-op for now).

        Args:
            texts: Training texts (unused).

        Returns:
            Self for method chaining.
        """
        return self

    def transform(self, texts: list[str]) -> list[list[str]]:
        """Transform texts (sklearn-style API).

        Args:
            texts: Texts to transform.

        Returns:
            List of processed token lists.
        """
        return self.process_batch(texts)

    def fit_transform(self, texts: list[str]) -> list[list[str]]:
        """Fit and transform (sklearn-style API).

        Args:
            texts: Texts to process.

        Returns:
            List of processed token lists.
        """
        return self.fit(texts).transform(texts)

    @property
    def config(self) -> dict:
        """Get current pipeline configuration."""
        return {
            "lowercase": self.lowercase,
            "remove_stopwords": self.remove_stopwords,
            "normalizer": self.normalizer,
            "language": self.language,
        }

    def __repr__(self) -> str:
        """String representation of pipeline."""
        steps = ["tokenize"]
        if self.lowercase:
            steps[0] = "tokenize(lowercase)"
        if self.remove_stopwords:
            steps.append("remove_stopwords")
        if self.normalizer:
            steps.append(self.normalizer)
        return f"Pipeline({' -> '.join(steps)})"
