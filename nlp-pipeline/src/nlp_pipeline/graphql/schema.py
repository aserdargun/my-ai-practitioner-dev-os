"""GraphQL schema for word embeddings API."""

import graphene

from nlp_pipeline.embeddings import WordEmbeddings

# Global embeddings instance (set via set_embeddings)
_embeddings: WordEmbeddings | None = None


def set_embeddings(embeddings: WordEmbeddings) -> None:
    """Set the embeddings instance for the API."""
    global _embeddings
    _embeddings = embeddings


def get_embeddings() -> WordEmbeddings:
    """Get the embeddings instance."""
    if _embeddings is None:
        raise RuntimeError("Embeddings not initialized. Call set_embeddings() first.")
    return _embeddings


class SimilarWord(graphene.ObjectType):
    """A word with its similarity score."""

    word = graphene.String(required=True, description="The similar word")
    similarity = graphene.Float(required=True, description="Cosine similarity score")


class EmbeddingInfo(graphene.ObjectType):
    """Information about the loaded embeddings."""

    vocab_size = graphene.Int(required=True, description="Number of words in vocabulary")
    dimension = graphene.Int(required=True, description="Embedding vector dimension")


class WordVector(graphene.ObjectType):
    """A word and its embedding vector."""

    word = graphene.String(required=True, description="The word")
    vector = graphene.List(graphene.Float, required=True, description="Embedding vector")
    dimension = graphene.Int(required=True, description="Vector dimension")


class Query(graphene.ObjectType):
    """Root query for embeddings API."""

    # Embedding info
    info = graphene.Field(
        EmbeddingInfo,
        description="Get information about loaded embeddings",
    )

    # Check if word exists
    has_word = graphene.Boolean(
        word=graphene.String(required=True),
        description="Check if a word exists in the vocabulary",
    )

    # Get word vector
    word_vector = graphene.Field(
        WordVector,
        word=graphene.String(required=True),
        description="Get the embedding vector for a word",
    )

    # Similarity between two words
    similarity = graphene.Float(
        word1=graphene.String(required=True),
        word2=graphene.String(required=True),
        description="Calculate cosine similarity between two words",
    )

    # Most similar words
    most_similar = graphene.List(
        SimilarWord,
        word=graphene.String(required=True),
        top_n=graphene.Int(default_value=10),
        description="Find words most similar to the given word",
    )

    # Word analogy
    analogy = graphene.List(
        SimilarWord,
        positive=graphene.List(graphene.String, required=True),
        negative=graphene.List(graphene.String, required=True),
        top_n=graphene.Int(default_value=10),
        description="Solve word analogies (e.g., king - man + woman = queen)",
    )

    # Doesn't match
    doesnt_match = graphene.String(
        words=graphene.List(graphene.String, required=True),
        description="Find the word that doesn't match the others",
    )

    # Search vocabulary
    search_vocab = graphene.List(
        graphene.String,
        prefix=graphene.String(required=True),
        limit=graphene.Int(default_value=20),
        description="Search vocabulary for words starting with prefix",
    )

    def resolve_info(self, info) -> EmbeddingInfo:
        """Resolve embedding info query."""
        emb = get_embeddings()
        return EmbeddingInfo(
            vocab_size=emb.vocab_size,
            dimension=emb.dimension,
        )

    def resolve_has_word(self, info, word: str) -> bool:
        """Check if word exists in vocabulary."""
        emb = get_embeddings()
        return word in emb

    def resolve_word_vector(self, info, word: str) -> WordVector | None:
        """Get embedding vector for a word."""
        emb = get_embeddings()
        if word not in emb:
            return None
        vector = emb[word]
        return WordVector(
            word=word,
            vector=vector.tolist(),
            dimension=len(vector),
        )

    def resolve_similarity(self, info, word1: str, word2: str) -> float | None:
        """Calculate similarity between two words."""
        emb = get_embeddings()
        if word1 not in emb or word2 not in emb:
            return None
        return emb.similarity(word1, word2)

    def resolve_most_similar(
        self, info, word: str, top_n: int = 10
    ) -> list[SimilarWord]:
        """Find most similar words."""
        emb = get_embeddings()
        if word not in emb:
            return []
        results = emb.most_similar(word, topn=top_n)
        return [SimilarWord(word=w, similarity=s) for w, s in results]

    def resolve_analogy(
        self,
        info,
        positive: list[str],
        negative: list[str],
        top_n: int = 10,
    ) -> list[SimilarWord]:
        """Solve word analogies."""
        emb = get_embeddings()
        # Check all words exist
        for word in positive + negative:
            if word not in emb:
                return []
        results = emb.analogy(positive=positive, negative=negative, topn=top_n)
        return [SimilarWord(word=w, similarity=s) for w, s in results]

    def resolve_doesnt_match(self, info, words: list[str]) -> str | None:
        """Find the word that doesn't match."""
        emb = get_embeddings()
        # Check all words exist
        for word in words:
            if word not in emb:
                return None
        return emb.doesnt_match(words)

    def resolve_search_vocab(
        self, info, prefix: str, limit: int = 20
    ) -> list[str]:
        """Search vocabulary by prefix."""
        emb = get_embeddings()
        matches = [w for w in emb.vocab if w.startswith(prefix)]
        return sorted(matches)[:limit]


schema = graphene.Schema(query=Query)
