"""Lemmatization module using WordNet."""

from typing import Literal

import nltk
from nltk.stem import WordNetLemmatizer


POS = Literal["noun", "verb", "adj", "adv"]


class Lemmatizer:
    """Word lemmatizer using WordNet."""

    def __init__(self, default_pos: POS = "noun"):
        """Initialize lemmatizer.

        Args:
            default_pos: Default part-of-speech for lemmatization.
                Options: 'noun', 'verb', 'adj', 'adv'.
        """
        self._ensure_nltk_data()
        self._lemmatizer = WordNetLemmatizer()
        self.default_pos = default_pos

    def _ensure_nltk_data(self) -> None:
        """Download required NLTK data if not present."""
        for resource in ["wordnet", "omw-1.4"]:
            try:
                nltk.data.find(f"corpora/{resource}")
            except LookupError:
                nltk.download(resource, quiet=True)

    def _get_wordnet_pos(self, pos: POS) -> str:
        """Convert POS string to WordNet POS constant."""
        from nltk.corpus import wordnet

        pos_map = {
            "noun": wordnet.NOUN,
            "verb": wordnet.VERB,
            "adj": wordnet.ADJ,
            "adv": wordnet.ADV,
        }
        return pos_map.get(pos, wordnet.NOUN)

    def lemmatize(self, word: str, pos: POS | None = None) -> str:
        """Lemmatize a single word.

        Args:
            word: Word to lemmatize.
            pos: Part-of-speech ('noun', 'verb', 'adj', 'adv').
                Uses default_pos if not specified.

        Returns:
            Lemmatized word.
        """
        if not word:
            return word

        pos = pos or self.default_pos
        wordnet_pos = self._get_wordnet_pos(pos)
        return self._lemmatizer.lemmatize(word.lower(), pos=wordnet_pos)

    def lemmatize_tokens(
        self,
        tokens: list[str],
        pos: POS | None = None,
    ) -> list[str]:
        """Lemmatize a list of tokens.

        Args:
            tokens: List of words to lemmatize.
            pos: Part-of-speech for all tokens.

        Returns:
            List of lemmatized words.
        """
        return [self.lemmatize(token, pos) for token in tokens]

    def lemmatize_text(
        self,
        text: str,
        pos: POS | None = None,
        tokenizer=None,
    ) -> list[str]:
        """Tokenize text and lemmatize all words.

        Args:
            text: Input text.
            pos: Part-of-speech for all tokens.
            tokenizer: Optional Tokenizer instance. Uses basic split if None.

        Returns:
            List of lemmatized tokens.
        """
        if tokenizer:
            tokens = tokenizer.tokenize_words(text)
        else:
            tokens = text.lower().split()

        return self.lemmatize_tokens(tokens, pos)

    def lemmatize_with_pos_tags(
        self,
        tagged_tokens: list[tuple[str, str]],
    ) -> list[str]:
        """Lemmatize tokens with their POS tags.

        Args:
            tagged_tokens: List of (word, pos_tag) tuples.
                POS tags should be Penn Treebank tags (NN, VB, JJ, RB).

        Returns:
            List of lemmatized words.
        """
        result = []
        for word, tag in tagged_tokens:
            pos = self._penn_to_wordnet(tag)
            result.append(self._lemmatizer.lemmatize(word.lower(), pos=pos))
        return result

    def _penn_to_wordnet(self, tag: str) -> str:
        """Convert Penn Treebank POS tag to WordNet POS."""
        from nltk.corpus import wordnet

        if tag.startswith("V"):
            return wordnet.VERB
        elif tag.startswith("J"):
            return wordnet.ADJ
        elif tag.startswith("R"):
            return wordnet.ADV
        else:
            return wordnet.NOUN
