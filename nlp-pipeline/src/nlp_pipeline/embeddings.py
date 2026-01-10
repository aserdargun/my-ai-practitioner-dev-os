"""Word embedding module supporting Word2Vec, GloVe, and FastText formats."""

from pathlib import Path

import numpy as np


class WordEmbeddings:
    """Load and query word embeddings.

    Supports loading from:
    - Word2Vec text format (.txt, .vec)
    - GloVe text format (.txt)
    - Binary Word2Vec format (.bin) - limited support

    All formats are loaded into a common interface for querying.
    """

    def __init__(self):
        """Initialize empty embeddings."""
        self._vectors: dict[str, np.ndarray] = {}
        self._dimension: int = 0
        self._source: str | None = None

    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return self._dimension

    @property
    def vocab_size(self) -> int:
        """Get vocabulary size."""
        return len(self._vectors)

    @property
    def vocab(self) -> list[str]:
        """Get list of words in vocabulary."""
        return list(self._vectors.keys())

    def __len__(self) -> int:
        """Get vocabulary size."""
        return len(self._vectors)

    def __contains__(self, word: str) -> bool:
        """Check if word is in vocabulary."""
        return word in self._vectors

    def __getitem__(self, word: str) -> np.ndarray:
        """Get embedding vector for word."""
        return self._vectors[word]

    def get(self, word: str, default: np.ndarray | None = None) -> np.ndarray | None:
        """Get embedding vector for word with default.

        Args:
            word: Word to look up.
            default: Default value if word not found.

        Returns:
            Embedding vector or default.
        """
        return self._vectors.get(word, default)

    def load_word2vec_format(
        self,
        path: str | Path,
        binary: bool = False,
        limit: int | None = None,
    ) -> "WordEmbeddings":
        """Load embeddings from Word2Vec format.

        Args:
            path: Path to embeddings file.
            binary: Whether file is binary format.
            limit: Maximum number of words to load.

        Returns:
            Self for method chaining.
        """
        path = Path(path)
        self._source = str(path)

        if binary:
            self._load_binary(path, limit)
        else:
            self._load_text(path, limit, has_header=True)

        return self

    def load_glove_format(
        self,
        path: str | Path,
        limit: int | None = None,
    ) -> "WordEmbeddings":
        """Load embeddings from GloVe format (no header line).

        Args:
            path: Path to embeddings file.
            limit: Maximum number of words to load.

        Returns:
            Self for method chaining.
        """
        path = Path(path)
        self._source = str(path)
        self._load_text(path, limit, has_header=False)
        return self

    def _load_text(
        self,
        path: Path,
        limit: int | None,
        has_header: bool,
    ) -> None:
        """Load embeddings from text format."""
        with open(path, encoding="utf-8", errors="ignore") as f:
            if has_header:
                header = f.readline()
                parts = header.strip().split()
                if len(parts) == 2:
                    _, dim = int(parts[0]), int(parts[1])
                    self._dimension = dim

            count = 0
            for line in f:
                if limit and count >= limit:
                    break

                parts = line.rstrip().split(" ")
                if len(parts) < 3:
                    continue

                word = parts[0]
                try:
                    vector = np.array([float(x) for x in parts[1:]], dtype=np.float32)
                except ValueError:
                    continue

                if self._dimension == 0:
                    self._dimension = len(vector)
                elif len(vector) != self._dimension:
                    continue

                self._vectors[word] = vector
                count += 1

    def _load_binary(self, path: Path, limit: int | None) -> None:
        """Load embeddings from binary Word2Vec format."""
        with open(path, "rb") as f:
            header = f.readline().decode("utf-8")
            vocab_size, dim = map(int, header.split())
            self._dimension = dim

            count = 0
            for _ in range(vocab_size):
                if limit and count >= limit:
                    break

                word_bytes = []
                while True:
                    ch = f.read(1)
                    if ch == b" ":
                        break
                    if ch == b"\n":
                        continue
                    word_bytes.append(ch)

                word = b"".join(word_bytes).decode("utf-8", errors="ignore")
                vector = np.frombuffer(f.read(dim * 4), dtype=np.float32)

                if len(vector) == dim:
                    self._vectors[word] = vector.copy()
                    count += 1

    def similarity(self, word1: str, word2: str) -> float:
        """Calculate cosine similarity between two words.

        Args:
            word1: First word.
            word2: Second word.

        Returns:
            Cosine similarity (-1 to 1).

        Raises:
            KeyError: If either word not in vocabulary.
        """
        vec1 = self._vectors[word1]
        vec2 = self._vectors[word2]
        return self._cosine_similarity(vec1, vec2)

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

    def most_similar(
        self,
        word: str,
        topn: int = 10,
    ) -> list[tuple[str, float]]:
        """Find most similar words.

        Args:
            word: Query word.
            topn: Number of results to return.

        Returns:
            List of (word, similarity) tuples.

        Raises:
            KeyError: If word not in vocabulary.
        """
        query_vec = self._vectors[word]
        return self._most_similar_to_vector(query_vec, topn, exclude={word})

    def most_similar_to_vector(
        self,
        vector: np.ndarray,
        topn: int = 10,
    ) -> list[tuple[str, float]]:
        """Find most similar words to a vector.

        Args:
            vector: Query vector.
            topn: Number of results to return.

        Returns:
            List of (word, similarity) tuples.
        """
        return self._most_similar_to_vector(vector, topn, exclude=set())

    def _most_similar_to_vector(
        self,
        vector: np.ndarray,
        topn: int,
        exclude: set[str],
    ) -> list[tuple[str, float]]:
        """Internal method to find similar words."""
        similarities = []
        for word, vec in self._vectors.items():
            if word in exclude:
                continue
            sim = self._cosine_similarity(vector, vec)
            similarities.append((word, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:topn]

    def analogy(
        self,
        positive: list[str],
        negative: list[str],
        topn: int = 10,
    ) -> list[tuple[str, float]]:
        """Solve word analogies using vector arithmetic.

        Example: king - man + woman = queen
            analogy(positive=["king", "woman"], negative=["man"])

        Args:
            positive: Words to add.
            negative: Words to subtract.
            topn: Number of results to return.

        Returns:
            List of (word, similarity) tuples.
        """
        # Build result vector
        result = np.zeros(self._dimension, dtype=np.float32)

        exclude = set()
        for word in positive:
            result += self._vectors[word]
            exclude.add(word)

        for word in negative:
            result -= self._vectors[word]
            exclude.add(word)

        # Normalize
        norm = np.linalg.norm(result)
        if norm > 0:
            result /= norm

        return self._most_similar_to_vector(result, topn, exclude)

    def doesnt_match(self, words: list[str]) -> str:
        """Find the word that doesn't match the others.

        Args:
            words: List of words.

        Returns:
            The word that is least similar to the others.
        """
        if len(words) < 2:
            return words[0] if words else ""

        # Calculate mean vector
        vectors = [self._vectors[w] for w in words]
        mean_vec = np.mean(vectors, axis=0)

        # Find word furthest from mean
        min_sim = float("inf")
        outlier = words[0]
        for word in words:
            sim = self._cosine_similarity(self._vectors[word], mean_vec)
            if sim < min_sim:
                min_sim = sim
                outlier = word

        return outlier

    def add_word(self, word: str, vector: np.ndarray) -> None:
        """Add a word and its vector to the embeddings.

        Args:
            word: Word to add.
            vector: Embedding vector.

        Raises:
            ValueError: If vector dimension doesn't match.
        """
        if self._dimension == 0:
            self._dimension = len(vector)
        elif len(vector) != self._dimension:
            raise ValueError(
                f"Vector dimension {len(vector)} doesn't match "
                f"embedding dimension {self._dimension}"
            )
        self._vectors[word] = np.array(vector, dtype=np.float32)

    @classmethod
    def from_dict(
        cls,
        vectors: dict[str, list[float] | np.ndarray],
    ) -> "WordEmbeddings":
        """Create embeddings from a dictionary.

        Args:
            vectors: Dictionary mapping words to vectors.

        Returns:
            WordEmbeddings instance.
        """
        embeddings = cls()
        for word, vector in vectors.items():
            embeddings.add_word(word, np.array(vector, dtype=np.float32))
        return embeddings

    def __repr__(self) -> str:
        """String representation."""
        return f"WordEmbeddings(vocab_size={self.vocab_size}, dimension={self.dimension})"
