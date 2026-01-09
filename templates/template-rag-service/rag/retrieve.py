"""Retrieval Module."""

from dataclasses import dataclass

from rag.ingest import DocumentChunk, DocumentIngester


@dataclass
class RetrievalResult:
    """Result of a retrieval query."""

    chunk: DocumentChunk
    score: float

    @property
    def content(self) -> str:
        return self.chunk.content

    @property
    def source(self) -> str:
        return self.chunk.source


class MockEmbedder:
    """Mock embedder for demonstration.

    Replace with real embeddings:
    - sentence-transformers
    - OpenAI embeddings
    - Cohere embeddings
    """

    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        """Generate mock embedding based on text hash."""
        import hashlib

        # Create deterministic embedding from text
        hash_bytes = hashlib.sha256(text.encode()).digest()
        embedding = []

        for i in range(self.dimension):
            byte_idx = i % len(hash_bytes)
            embedding.append((hash_bytes[byte_idx] - 128) / 128.0)

        return embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        return [self.embed(text) for text in texts]


class Retriever:
    """Vector-based document retriever."""

    def __init__(
        self,
        chunks: list[DocumentChunk],
        embedder: MockEmbedder | None = None,
    ):
        """Initialize retriever with chunks."""
        self.chunks = chunks
        self.embedder = embedder or MockEmbedder()
        self._index: list[list[float]] | None = None

    def _build_index(self) -> None:
        """Build embedding index."""
        texts = [chunk.content for chunk in self.chunks]
        self._index = self.embedder.embed_batch(texts)

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        """Search for relevant chunks."""
        if self._index is None:
            self._build_index()

        query_embedding = self.embedder.embed(query)

        # Compute similarities
        scores = []
        for i, chunk_embedding in enumerate(self._index):
            score = self._cosine_similarity(query_embedding, chunk_embedding)
            scores.append((i, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Return top-k results
        results = []
        for idx, score in scores[:top_k]:
            results.append(
                RetrievalResult(
                    chunk=self.chunks[idx],
                    score=score,
                )
            )

        return results

    @classmethod
    def load(cls, index_path: str) -> "Retriever":
        """Load retriever from index path."""
        chunks = DocumentIngester.load_chunks(index_path)
        return cls(chunks=chunks)
