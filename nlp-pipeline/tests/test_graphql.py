"""Tests for GraphQL API."""

import json

import pytest

from nlp_pipeline.embeddings import WordEmbeddings
from nlp_pipeline.graphql import create_app, schema
from nlp_pipeline.graphql.schema import set_embeddings


@pytest.fixture
def sample_embeddings():
    """Create sample embeddings for testing."""
    return WordEmbeddings.from_dict({
        "king": [0.5, 0.7, -0.2, 0.1, 0.3],
        "queen": [0.5, 0.6, 0.3, 0.1, 0.3],
        "man": [0.2, 0.3, -0.5, 0.4, 0.1],
        "woman": [0.2, 0.2, 0.4, 0.4, 0.1],
        "dog": [-0.3, 0.1, 0.0, -0.5, 0.6],
        "cat": [-0.2, 0.1, 0.1, -0.5, 0.5],
        "apple": [-0.5, -0.3, 0.1, 0.2, -0.4],
        "banana": [-0.4, -0.3, 0.0, 0.2, -0.3],
    })


@pytest.fixture
def app(sample_embeddings):
    """Create Flask test app."""
    app = create_app(sample_embeddings)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def graphql_query(client, query: str) -> dict:
    """Execute a GraphQL query and return the result."""
    response = client.post(
        "/graphql",
        json={"query": query},
        content_type="application/json",
    )
    return json.loads(response.data)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_returns_ok(self, client):
        """Health endpoint returns OK status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_returns_api_info(self, client):
        """Root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "NLP Pipeline GraphQL API"
        assert "endpoints" in data
        assert "example_queries" in data


class TestInfoQuery:
    """Tests for info query."""

    def test_info_returns_vocab_size_and_dimension(self, client):
        """Info query returns vocabulary size and dimension."""
        result = graphql_query(client, "{ info { vocabSize dimension } }")
        assert "errors" not in result
        assert result["data"]["info"]["vocabSize"] == 8
        assert result["data"]["info"]["dimension"] == 5


class TestHasWordQuery:
    """Tests for hasWord query."""

    def test_has_word_returns_true_for_existing_word(self, client):
        """hasWord returns true for existing word."""
        result = graphql_query(client, '{ hasWord(word: "king") }')
        assert "errors" not in result
        assert result["data"]["hasWord"] is True

    def test_has_word_returns_false_for_missing_word(self, client):
        """hasWord returns false for missing word."""
        result = graphql_query(client, '{ hasWord(word: "unknown") }')
        assert "errors" not in result
        assert result["data"]["hasWord"] is False


class TestWordVectorQuery:
    """Tests for wordVector query."""

    def test_word_vector_returns_vector(self, client):
        """wordVector returns the embedding vector."""
        result = graphql_query(
            client, '{ wordVector(word: "king") { word vector dimension } }'
        )
        assert "errors" not in result
        data = result["data"]["wordVector"]
        assert data["word"] == "king"
        assert len(data["vector"]) == 5
        assert data["dimension"] == 5

    def test_word_vector_returns_null_for_missing_word(self, client):
        """wordVector returns null for missing word."""
        result = graphql_query(
            client, '{ wordVector(word: "unknown") { word } }'
        )
        assert "errors" not in result
        assert result["data"]["wordVector"] is None


class TestSimilarityQuery:
    """Tests for similarity query."""

    def test_similarity_returns_float(self, client):
        """Similarity query returns a float value."""
        result = graphql_query(
            client, '{ similarity(word1: "king", word2: "queen") }'
        )
        assert "errors" not in result
        sim = result["data"]["similarity"]
        assert isinstance(sim, float)
        assert -1 <= sim <= 1

    def test_similarity_high_for_similar_words(self, client):
        """Similar words have high similarity."""
        result = graphql_query(
            client, '{ similarity(word1: "king", word2: "queen") }'
        )
        assert result["data"]["similarity"] > 0.8

    def test_similarity_returns_null_for_missing_word(self, client):
        """Similarity returns null if word not found."""
        result = graphql_query(
            client, '{ similarity(word1: "king", word2: "unknown") }'
        )
        assert "errors" not in result
        assert result["data"]["similarity"] is None


class TestMostSimilarQuery:
    """Tests for mostSimilar query."""

    def test_most_similar_returns_list(self, client):
        """mostSimilar returns a list of similar words."""
        result = graphql_query(
            client, '{ mostSimilar(word: "king", topN: 3) { word similarity } }'
        )
        assert "errors" not in result
        similar = result["data"]["mostSimilar"]
        assert isinstance(similar, list)
        assert len(similar) == 3

    def test_most_similar_ordered_by_similarity(self, client):
        """Results are ordered by similarity descending."""
        result = graphql_query(
            client, '{ mostSimilar(word: "king", topN: 5) { word similarity } }'
        )
        similar = result["data"]["mostSimilar"]
        similarities = [s["similarity"] for s in similar]
        assert similarities == sorted(similarities, reverse=True)

    def test_most_similar_excludes_query_word(self, client):
        """Query word is not in results."""
        result = graphql_query(
            client, '{ mostSimilar(word: "king", topN: 10) { word } }'
        )
        words = [s["word"] for s in result["data"]["mostSimilar"]]
        assert "king" not in words

    def test_most_similar_returns_empty_for_missing_word(self, client):
        """Returns empty list for missing word."""
        result = graphql_query(
            client, '{ mostSimilar(word: "unknown", topN: 5) { word } }'
        )
        assert "errors" not in result
        assert result["data"]["mostSimilar"] == []


class TestAnalogyQuery:
    """Tests for analogy query."""

    def test_analogy_returns_list(self, client):
        """Analogy query returns a list of words."""
        result = graphql_query(
            client,
            '{ analogy(positive: ["king", "woman"], negative: ["man"], topN: 3) { word similarity } }',
        )
        assert "errors" not in result
        analogy = result["data"]["analogy"]
        assert isinstance(analogy, list)
        assert len(analogy) <= 3

    def test_analogy_queen_example(self, client):
        """Classic king - man + woman = queen analogy."""
        result = graphql_query(
            client,
            '{ analogy(positive: ["king", "woman"], negative: ["man"], topN: 1) { word } }',
        )
        assert "errors" not in result
        words = [a["word"] for a in result["data"]["analogy"]]
        # Queen should be top result for this analogy
        assert "queen" in words

    def test_analogy_returns_empty_for_missing_word(self, client):
        """Returns empty list if any word is missing."""
        result = graphql_query(
            client,
            '{ analogy(positive: ["king", "unknown"], negative: ["man"], topN: 3) { word } }',
        )
        assert "errors" not in result
        assert result["data"]["analogy"] == []


class TestDoesntMatchQuery:
    """Tests for doesntMatch query."""

    def test_doesnt_match_returns_outlier(self, client):
        """doesntMatch identifies the outlier."""
        result = graphql_query(
            client, '{ doesntMatch(words: ["king", "queen", "dog"]) }'
        )
        assert "errors" not in result
        assert result["data"]["doesntMatch"] == "dog"

    def test_doesnt_match_returns_null_for_missing_word(self, client):
        """Returns null if any word is missing."""
        result = graphql_query(
            client, '{ doesntMatch(words: ["king", "queen", "unknown"]) }'
        )
        assert "errors" not in result
        assert result["data"]["doesntMatch"] is None


class TestSearchVocabQuery:
    """Tests for searchVocab query."""

    def test_search_vocab_returns_matches(self, client):
        """searchVocab returns matching words."""
        result = graphql_query(client, '{ searchVocab(prefix: "k") }')
        assert "errors" not in result
        words = result["data"]["searchVocab"]
        assert "king" in words

    def test_search_vocab_respects_limit(self, client):
        """searchVocab respects limit parameter."""
        result = graphql_query(client, '{ searchVocab(prefix: "", limit: 3) }')
        assert "errors" not in result
        words = result["data"]["searchVocab"]
        assert len(words) <= 3

    def test_search_vocab_returns_sorted(self, client):
        """searchVocab returns sorted results."""
        result = graphql_query(client, '{ searchVocab(prefix: "") }')
        words = result["data"]["searchVocab"]
        assert words == sorted(words)


class TestSchemaDirectly:
    """Tests for schema without Flask app."""

    def test_schema_executes_query(self, sample_embeddings):
        """Schema can execute queries directly."""
        set_embeddings(sample_embeddings)
        result = schema.execute("{ info { vocabSize } }")
        assert result.errors is None
        assert result.data["info"]["vocabSize"] == 8


class TestCreateAppWithoutEmbeddings:
    """Tests for app creation without embeddings."""

    def test_create_app_without_embeddings_succeeds(self):
        """App can be created without embeddings."""
        app = create_app()
        assert app is not None

    def test_query_fails_without_embeddings_set(self):
        """Queries fail if embeddings not set."""
        # Reset embeddings using the set_embeddings function
        import sys

        # Get a fresh module without cached embeddings
        schema_module = sys.modules["nlp_pipeline.graphql.schema"]
        original = getattr(schema_module, "_embeddings", None)
        setattr(schema_module, "_embeddings", None)

        try:
            app = create_app()
            app.config["TESTING"] = True
            client = app.test_client()

            result = graphql_query(client, "{ info { vocabSize } }")
            assert "errors" in result
        finally:
            # Restore original embeddings
            setattr(schema_module, "_embeddings", original)
