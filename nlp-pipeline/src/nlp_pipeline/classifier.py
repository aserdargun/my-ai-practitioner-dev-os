"""Text classification module with Naive Bayes and embedding-based classifiers."""

from collections import Counter, defaultdict
from typing import Literal

import numpy as np

from nlp_pipeline.embeddings import WordEmbeddings
from nlp_pipeline.pipeline import Pipeline


class NaiveBayesClassifier:
    """Multinomial Naive Bayes text classifier.

    Uses bag-of-words representation with optional preprocessing pipeline.
    """

    def __init__(
        self,
        pipeline: Pipeline | None = None,
        alpha: float = 1.0,
    ):
        """Initialize classifier.

        Args:
            pipeline: Preprocessing pipeline. If None, uses default.
            alpha: Smoothing parameter (Laplace smoothing).
        """
        self.pipeline = pipeline or Pipeline()
        self.alpha = alpha

        # Learned parameters
        self._classes: list[str] = []
        self._class_priors: dict[str, float] = {}
        self._word_probs: dict[str, dict[str, float]] = {}
        self._vocab: set[str] = set()

    def fit(self, texts: list[str], labels: list[str]) -> "NaiveBayesClassifier":
        """Train the classifier.

        Args:
            texts: Training texts.
            labels: Labels for each text.

        Returns:
            Self for method chaining.
        """
        if len(texts) != len(labels):
            raise ValueError("texts and labels must have same length")

        # Preprocess all texts
        processed = [self.pipeline.process(text) for text in texts]

        # Build vocabulary
        self._vocab = set()
        for tokens in processed:
            self._vocab.update(tokens)

        # Count classes
        class_counts = Counter(labels)
        self._classes = list(class_counts.keys())
        total_docs = len(labels)

        # Calculate class priors: P(class)
        self._class_priors = {
            cls: count / total_docs for cls, count in class_counts.items()
        }

        # Count word occurrences per class
        word_counts: dict[str, Counter] = defaultdict(Counter)
        class_word_totals: dict[str, int] = defaultdict(int)

        for tokens, label in zip(processed, labels):
            for token in tokens:
                word_counts[label][token] += 1
                class_word_totals[label] += 1

        # Calculate word probabilities with Laplace smoothing: P(word|class)
        vocab_size = len(self._vocab)
        self._word_probs = {}

        for cls in self._classes:
            self._word_probs[cls] = {}
            total = class_word_totals[cls]
            for word in self._vocab:
                count = word_counts[cls][word]
                # Laplace smoothing
                prob = (count + self.alpha) / (total + self.alpha * vocab_size)
                self._word_probs[cls][word] = prob

        return self

    def predict(self, texts: list[str]) -> list[str]:
        """Predict labels for texts.

        Args:
            texts: Texts to classify.

        Returns:
            Predicted labels.
        """
        return [self._predict_one(text) for text in texts]

    def _predict_one(self, text: str) -> str:
        """Predict label for a single text."""
        tokens = self.pipeline.process(text)

        best_class = self._classes[0]
        best_score = float("-inf")

        for cls in self._classes:
            # Start with log prior
            score = np.log(self._class_priors[cls])

            # Add log probabilities for each word
            for token in tokens:
                if token in self._vocab:
                    score += np.log(self._word_probs[cls][token])
                # Words not in vocab are ignored (could use unknown word prob)

            if score > best_score:
                best_score = score
                best_class = cls

        return best_class

    def predict_proba(self, texts: list[str]) -> list[dict[str, float]]:
        """Predict class probabilities for texts.

        Args:
            texts: Texts to classify.

        Returns:
            List of {class: probability} dictionaries.
        """
        return [self._predict_proba_one(text) for text in texts]

    def _predict_proba_one(self, text: str) -> dict[str, float]:
        """Predict class probabilities for a single text."""
        tokens = self.pipeline.process(text)

        log_scores = {}
        for cls in self._classes:
            score = np.log(self._class_priors[cls])
            for token in tokens:
                if token in self._vocab:
                    score += np.log(self._word_probs[cls][token])
            log_scores[cls] = score

        # Convert log scores to probabilities using log-sum-exp trick
        max_score = max(log_scores.values())
        exp_scores = {cls: np.exp(score - max_score) for cls, score in log_scores.items()}
        total = sum(exp_scores.values())

        return {cls: score / total for cls, score in exp_scores.items()}

    def score(self, texts: list[str], labels: list[str]) -> float:
        """Calculate accuracy on test data.

        Args:
            texts: Test texts.
            labels: True labels.

        Returns:
            Accuracy (0-1).
        """
        predictions = self.predict(texts)
        correct = sum(p == l for p, l in zip(predictions, labels))
        return correct / len(labels) if labels else 0.0

    @property
    def classes(self) -> list[str]:
        """Get list of classes."""
        return self._classes.copy()

    @property
    def vocab_size(self) -> int:
        """Get vocabulary size."""
        return len(self._vocab)


class EmbeddingClassifier:
    """Text classifier using word embeddings.

    Represents text as average of word vectors, then uses
    nearest centroid classification.
    """

    def __init__(
        self,
        embeddings: WordEmbeddings,
        pipeline: Pipeline | None = None,
        strategy: Literal["centroid", "knn"] = "centroid",
        k: int = 5,
    ):
        """Initialize classifier.

        Args:
            embeddings: Pre-trained word embeddings.
            pipeline: Preprocessing pipeline. If None, uses default.
            strategy: Classification strategy ('centroid' or 'knn').
            k: Number of neighbors for KNN strategy.
        """
        self.embeddings = embeddings
        self.pipeline = pipeline or Pipeline()
        self.strategy = strategy
        self.k = k

        # Learned parameters
        self._classes: list[str] = []
        self._centroids: dict[str, np.ndarray] = {}
        self._training_vectors: list[np.ndarray] = []
        self._training_labels: list[str] = []

    def _text_to_vector(self, text: str) -> np.ndarray | None:
        """Convert text to embedding vector by averaging word vectors."""
        tokens = self.pipeline.process(text)

        vectors = []
        for token in tokens:
            if token in self.embeddings:
                vectors.append(self.embeddings[token])

        if not vectors:
            return None

        return np.mean(vectors, axis=0)

    def fit(self, texts: list[str], labels: list[str]) -> "EmbeddingClassifier":
        """Train the classifier.

        Args:
            texts: Training texts.
            labels: Labels for each text.

        Returns:
            Self for method chaining.
        """
        if len(texts) != len(labels):
            raise ValueError("texts and labels must have same length")

        self._classes = list(set(labels))

        # Convert texts to vectors
        self._training_vectors = []
        self._training_labels = []

        for text, label in zip(texts, labels):
            vec = self._text_to_vector(text)
            if vec is not None:
                self._training_vectors.append(vec)
                self._training_labels.append(label)

        # Calculate centroids for each class
        if self.strategy == "centroid":
            class_vectors: dict[str, list[np.ndarray]] = defaultdict(list)
            for vec, label in zip(self._training_vectors, self._training_labels):
                class_vectors[label].append(vec)

            self._centroids = {
                cls: np.mean(vecs, axis=0) for cls, vecs in class_vectors.items()
            }

        return self

    def predict(self, texts: list[str]) -> list[str]:
        """Predict labels for texts.

        Args:
            texts: Texts to classify.

        Returns:
            Predicted labels.
        """
        return [self._predict_one(text) for text in texts]

    def _predict_one(self, text: str) -> str:
        """Predict label for a single text."""
        vec = self._text_to_vector(text)

        if vec is None:
            # Return most common class if no embedding coverage
            return max(set(self._training_labels), key=self._training_labels.count)

        if self.strategy == "centroid":
            return self._predict_centroid(vec)
        else:
            return self._predict_knn(vec)

    def _predict_centroid(self, vec: np.ndarray) -> str:
        """Predict using nearest centroid."""
        best_class = self._classes[0]
        best_sim = float("-inf")

        for cls, centroid in self._centroids.items():
            sim = self._cosine_similarity(vec, centroid)
            if sim > best_sim:
                best_sim = sim
                best_class = cls

        return best_class

    def _predict_knn(self, vec: np.ndarray) -> str:
        """Predict using K-nearest neighbors."""
        similarities = []
        for train_vec, label in zip(self._training_vectors, self._training_labels):
            sim = self._cosine_similarity(vec, train_vec)
            similarities.append((sim, label))

        # Get top k neighbors
        similarities.sort(reverse=True)
        top_k = similarities[: self.k]

        # Vote
        votes = Counter(label for _, label in top_k)
        return votes.most_common(1)[0][0]

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity."""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

    def score(self, texts: list[str], labels: list[str]) -> float:
        """Calculate accuracy on test data.

        Args:
            texts: Test texts.
            labels: True labels.

        Returns:
            Accuracy (0-1).
        """
        predictions = self.predict(texts)
        correct = sum(p == l for p, l in zip(predictions, labels))
        return correct / len(labels) if labels else 0.0

    @property
    def classes(self) -> list[str]:
        """Get list of classes."""
        return self._classes.copy()
