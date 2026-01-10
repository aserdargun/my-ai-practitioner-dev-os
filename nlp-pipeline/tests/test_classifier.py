"""Tests for the text classifier module."""

import pytest

from nlp_pipeline import (
    EmbeddingClassifier,
    NaiveBayesClassifier,
    Pipeline,
    WordEmbeddings,
)

# Sample training data for sentiment classification
TRAIN_TEXTS = [
    "I love this movie, it's amazing",
    "This film is wonderful and great",
    "Absolutely fantastic, loved every minute",
    "Best movie I've ever seen",
    "This movie is terrible and boring",
    "I hate this film, waste of time",
    "Awful movie, do not watch",
    "Worst film ever, very disappointing",
]
TRAIN_LABELS = [
    "positive",
    "positive",
    "positive",
    "positive",
    "negative",
    "negative",
    "negative",
    "negative",
]

TEST_TEXTS = [
    "Great film, highly recommend",
    "Terrible movie, very bad",
]
TEST_LABELS = ["positive", "negative"]


def create_sample_embeddings() -> WordEmbeddings:
    """Create sample embeddings for testing."""
    # Simple embeddings that capture some sentiment
    embeddings = WordEmbeddings.from_dict({
        "love": [0.9, 0.1, 0.0],
        "great": [0.85, 0.15, 0.0],
        "amazing": [0.9, 0.05, 0.05],
        "wonderful": [0.88, 0.12, 0.0],
        "fantastic": [0.92, 0.08, 0.0],
        "best": [0.85, 0.1, 0.05],
        "good": [0.7, 0.2, 0.1],
        "recommend": [0.75, 0.15, 0.1],
        "hate": [0.1, 0.9, 0.0],
        "terrible": [0.05, 0.95, 0.0],
        "awful": [0.08, 0.92, 0.0],
        "bad": [0.15, 0.85, 0.0],
        "boring": [0.2, 0.7, 0.1],
        "worst": [0.05, 0.9, 0.05],
        "disappointing": [0.1, 0.85, 0.05],
        "waste": [0.1, 0.8, 0.1],
        "movie": [0.5, 0.5, 0.0],
        "film": [0.5, 0.5, 0.0],
        "watch": [0.5, 0.4, 0.1],
        "time": [0.4, 0.4, 0.2],
        "highly": [0.7, 0.2, 0.1],
    })
    return embeddings


class TestNaiveBayesClassifier:
    """Test suite for NaiveBayesClassifier."""

    def test_fit_and_predict(self):
        """Test basic fit and predict."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        predictions = clf.predict(TEST_TEXTS)
        assert len(predictions) == 2
        assert all(p in ["positive", "negative"] for p in predictions)

    def test_predict_positive(self):
        """Test predicting positive sentiment."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        prediction = clf.predict(["This movie is great and amazing"])[0]
        assert prediction == "positive"

    def test_predict_negative(self):
        """Test predicting negative sentiment."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        prediction = clf.predict(["This movie is terrible and awful"])[0]
        assert prediction == "negative"

    def test_predict_proba(self):
        """Test probability predictions."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        proba = clf.predict_proba(["Great amazing movie"])[0]
        assert "positive" in proba
        assert "negative" in proba
        assert abs(sum(proba.values()) - 1.0) < 0.01  # Probabilities sum to 1

    def test_score(self):
        """Test accuracy scoring."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        # Test on training data (should be high)
        train_score = clf.score(TRAIN_TEXTS, TRAIN_LABELS)
        assert train_score >= 0.5

    def test_classes_property(self):
        """Test classes property."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        classes = clf.classes
        assert "positive" in classes
        assert "negative" in classes

    def test_vocab_size(self):
        """Test vocabulary size property."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        assert clf.vocab_size > 0

    def test_custom_pipeline(self):
        """Test with custom preprocessing pipeline."""
        pipeline = Pipeline(normalizer="stem")
        clf = NaiveBayesClassifier(pipeline=pipeline)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        predictions = clf.predict(TEST_TEXTS)
        assert len(predictions) == 2

    def test_smoothing_parameter(self):
        """Test different smoothing parameters."""
        clf1 = NaiveBayesClassifier(alpha=0.1)
        clf2 = NaiveBayesClassifier(alpha=10.0)

        clf1.fit(TRAIN_TEXTS, TRAIN_LABELS)
        clf2.fit(TRAIN_TEXTS, TRAIN_LABELS)

        # Both should produce valid predictions
        pred1 = clf1.predict(TEST_TEXTS)
        pred2 = clf2.predict(TEST_TEXTS)
        assert len(pred1) == len(pred2) == 2

    def test_method_chaining(self):
        """Test that fit returns self for chaining."""
        clf = NaiveBayesClassifier()
        result = clf.fit(TRAIN_TEXTS, TRAIN_LABELS)
        assert result is clf

    def test_mismatched_lengths_error(self):
        """Test error on mismatched texts and labels."""
        clf = NaiveBayesClassifier()
        with pytest.raises(ValueError, match="same length"):
            clf.fit(["text1", "text2"], ["label1"])

    def test_empty_text(self):
        """Test prediction on empty text."""
        clf = NaiveBayesClassifier()
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        # Should still return a prediction (based on priors)
        prediction = clf.predict([""])[0]
        assert prediction in ["positive", "negative"]

    def test_multiclass(self):
        """Test with more than two classes."""
        texts = [
            "I love cats",
            "Dogs are great",
            "Birds can fly",
            "Cats are cute",
            "Dogs are loyal",
            "Birds sing beautifully",
        ]
        labels = ["cat", "dog", "bird", "cat", "dog", "bird"]

        clf = NaiveBayesClassifier()
        clf.fit(texts, labels)

        assert len(clf.classes) == 3
        prediction = clf.predict(["I love my cat"])[0]
        assert prediction in ["cat", "dog", "bird"]


class TestEmbeddingClassifier:
    """Test suite for EmbeddingClassifier."""

    def test_fit_and_predict_centroid(self):
        """Test centroid-based classification."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings, strategy="centroid")
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        predictions = clf.predict(TEST_TEXTS)
        assert len(predictions) == 2
        assert all(p in ["positive", "negative"] for p in predictions)

    def test_fit_and_predict_knn(self):
        """Test KNN-based classification."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings, strategy="knn", k=3)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        predictions = clf.predict(TEST_TEXTS)
        assert len(predictions) == 2

    def test_predict_positive(self):
        """Test predicting positive sentiment."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        prediction = clf.predict(["love great amazing"])[0]
        assert prediction == "positive"

    def test_predict_negative(self):
        """Test predicting negative sentiment."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        prediction = clf.predict(["hate terrible awful"])[0]
        assert prediction == "negative"

    def test_score(self):
        """Test accuracy scoring."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        score = clf.score(TEST_TEXTS, TEST_LABELS)
        assert 0 <= score <= 1

    def test_classes_property(self):
        """Test classes property."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        classes = clf.classes
        assert "positive" in classes
        assert "negative" in classes

    def test_custom_pipeline(self):
        """Test with custom preprocessing pipeline."""
        embeddings = create_sample_embeddings()
        pipeline = Pipeline(normalizer=None)  # No normalization
        clf = EmbeddingClassifier(embeddings, pipeline=pipeline)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        predictions = clf.predict(TEST_TEXTS)
        assert len(predictions) == 2

    def test_method_chaining(self):
        """Test that fit returns self for chaining."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        result = clf.fit(TRAIN_TEXTS, TRAIN_LABELS)
        assert result is clf

    def test_mismatched_lengths_error(self):
        """Test error on mismatched texts and labels."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        with pytest.raises(ValueError, match="same length"):
            clf.fit(["text1", "text2"], ["label1"])

    def test_unknown_words(self):
        """Test prediction with words not in embeddings."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        # "xyz" is not in embeddings, but "love" is
        prediction = clf.predict(["xyz xyz love"])[0]
        assert prediction in ["positive", "negative"]

    def test_all_unknown_words(self):
        """Test prediction when all words are unknown."""
        embeddings = create_sample_embeddings()
        clf = EmbeddingClassifier(embeddings)
        clf.fit(TRAIN_TEXTS, TRAIN_LABELS)

        # Should fall back to most common class
        prediction = clf.predict(["xyz abc def"])[0]
        assert prediction in ["positive", "negative"]

    def test_different_k_values(self):
        """Test KNN with different k values."""
        embeddings = create_sample_embeddings()

        for k in [1, 3, 5]:
            clf = EmbeddingClassifier(embeddings, strategy="knn", k=k)
            clf.fit(TRAIN_TEXTS, TRAIN_LABELS)
            predictions = clf.predict(TEST_TEXTS)
            assert len(predictions) == 2
