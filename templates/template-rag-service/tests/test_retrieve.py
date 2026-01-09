"""Tests for retrieval module."""

import pytest

from rag.ingest import DocumentChunk, DocumentIngester
from rag.retrieve import MockEmbedder, RetrievalResult, Retriever


@pytest.fixture
def sample_chunks():
    """Create sample chunks for testing."""
    return [
        DocumentChunk(
            id="chunk1",
            content="Machine learning is a subset of artificial intelligence.",
            source="ml.txt",
            metadata={},
        ),
        DocumentChunk(
            id="chunk2",
            content="Deep learning uses neural networks with many layers.",
            source="dl.txt",
            metadata={},
        ),
        DocumentChunk(
            id="chunk3",
            content="Natural language processing handles text data.",
            source="nlp.txt",
            metadata={},
        ),
    ]


@pytest.fixture
def retriever(sample_chunks):
    """Create retriever with sample chunks."""
    return Retriever(chunks=sample_chunks)


def test_mock_embedder():
    """Test mock embedder generates consistent embeddings."""
    embedder = MockEmbedder(dimension=64)

    # Same text should give same embedding
    emb1 = embedder.embed("test text")
    emb2 = embedder.embed("test text")
    assert emb1 == emb2

    # Different text should give different embedding
    emb3 = embedder.embed("different text")
    assert emb1 != emb3


def test_mock_embedder_dimension():
    """Test mock embedder respects dimension."""
    embedder = MockEmbedder(dimension=128)
    embedding = embedder.embed("test")
    assert len(embedding) == 128


def test_retriever_search(retriever):
    """Test retriever returns results."""
    results = retriever.search("machine learning", top_k=2)

    assert len(results) == 2
    assert all(isinstance(r, RetrievalResult) for r in results)
    assert all(r.score is not None for r in results)


def test_retriever_search_order(retriever):
    """Test results are ordered by score descending."""
    results = retriever.search("test query", top_k=3)

    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_retriever_result_properties(sample_chunks):
    """Test RetrievalResult properties."""
    chunk = sample_chunks[0]
    result = RetrievalResult(chunk=chunk, score=0.9)

    assert result.content == chunk.content
    assert result.source == chunk.source


def test_document_ingester_chunking():
    """Test document chunking."""
    ingester = DocumentIngester(chunk_size=100, chunk_overlap=20)

    text = "This is a test. " * 20  # ~320 characters
    chunks = ingester.chunk_text(text, source="test.txt")

    assert len(chunks) > 1
    assert all(len(c.content) <= 120 for c in chunks)  # Allow some flexibility


def test_document_ingester_id_generation():
    """Test chunk IDs are unique and deterministic."""
    ingester = DocumentIngester()

    chunks1 = ingester.chunk_text("Test content", "file1.txt")
    chunks2 = ingester.chunk_text("Test content", "file1.txt")

    # Same content should give same ID
    assert chunks1[0].id == chunks2[0].id

    # Different source should give different ID
    chunks3 = ingester.chunk_text("Test content", "file2.txt")
    assert chunks1[0].id != chunks3[0].id


def test_retriever_empty_query(retriever):
    """Test retriever handles empty query."""
    results = retriever.search("", top_k=2)
    assert len(results) == 2  # Should still return results
