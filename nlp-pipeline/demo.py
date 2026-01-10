#!/usr/bin/env python3
"""Demo script showcasing the NLP Pipeline capabilities."""

from nlp_pipeline import (
    EmbeddingClassifier,
    Lemmatizer,
    NaiveBayesClassifier,
    Pipeline,
    Stemmer,
    StopwordRemover,
    Tokenizer,
    WordEmbeddings,
)


def section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    sample_text = "The quick brown foxes are jumping over the lazy dogs."

    # 1. Tokenization
    section("1. TOKENIZATION")
    tokenizer = Tokenizer()

    words = tokenizer.tokenize_words(sample_text)
    print(f"Input: {sample_text!r}")
    print(f"Words: {words}")

    sentences = tokenizer.tokenize_sentences(
        "First sentence. Second sentence! Third one?"
    )
    print(f"\nSentences: {sentences}")

    # 2. Stopword Removal
    section("2. STOPWORD REMOVAL")
    remover = StopwordRemover()

    tokens = ["the", "quick", "brown", "fox", "is", "jumping"]
    filtered = remover.remove(tokens)
    print(f"Input:    {tokens}")
    print(f"Filtered: {filtered}")

    # 3. Stemming
    section("3. STEMMING")
    stemmer = Stemmer()

    words_to_stem = ["running", "jumps", "easily", "cats", "fishing"]
    stemmed = stemmer.stem_tokens(words_to_stem)
    print(f"Input:   {words_to_stem}")
    print(f"Stemmed: {stemmed}")

    # 4. Lemmatization
    section("4. LEMMATIZATION")
    lemmatizer = Lemmatizer()

    print("Nouns:")
    for word in ["cats", "children", "mice", "geese"]:
        print(f"  {word} -> {lemmatizer.lemmatize(word)}")

    print("\nVerbs:")
    for word in ["running", "ran", "better"]:
        print(f"  {word} -> {lemmatizer.lemmatize(word, pos='verb')}")

    # 5. Unified Pipeline
    section("5. UNIFIED PIPELINE")

    # Default: lowercase + stopwords + lemmatize
    pipeline = Pipeline()
    result = pipeline(sample_text)
    print(f"Input:  {sample_text!r}")
    print(f"Output: {result}")
    print(f"Config: {pipeline}")

    # With stemming instead
    pipeline_stem = Pipeline(normalizer="stem")
    result_stem = pipeline_stem(sample_text)
    print(f"\nWith stemming: {result_stem}")

    # 6. Word Embeddings
    section("6. WORD EMBEDDINGS")

    # Create embeddings from dictionary (for demo)
    embeddings = WordEmbeddings.from_dict({
        "king": [0.9, 0.1, 0.0, 0.5],
        "queen": [0.85, 0.15, 0.0, 0.5],
        "man": [0.5, 0.0, 0.9, 0.1],
        "woman": [0.45, 0.05, 0.85, 0.15],
        "prince": [0.8, 0.2, 0.1, 0.4],
        "princess": [0.75, 0.25, 0.05, 0.45],
        "cat": [0.1, 0.8, 0.1, 0.0],
        "dog": [0.15, 0.75, 0.15, 0.0],
    })

    print(f"Vocabulary size: {embeddings.vocab_size}")
    print(f"Dimension: {embeddings.dimension}")

    sim = embeddings.similarity("king", "queen")
    print(f"\nSimilarity(king, queen): {sim:.3f}")

    similar = embeddings.most_similar("king", topn=3)
    print(f"Most similar to 'king': {similar}")

    # 7. Text Classification
    section("7. TEXT CLASSIFICATION")

    # Training data
    train_texts = [
        "I love this movie, it was amazing",
        "Great film, highly recommend it",
        "Best movie I have ever seen",
        "Wonderful acting and story",
        "Terrible movie, waste of time",
        "Awful film, do not watch",
        "Worst movie ever made",
        "Boring and poorly acted",
    ]
    train_labels = ["positive", "positive", "positive", "positive",
                    "negative", "negative", "negative", "negative"]

    # Naive Bayes
    print("Naive Bayes Classifier:")
    nb_clf = NaiveBayesClassifier()
    nb_clf.fit(train_texts, train_labels)

    test_texts = ["This movie is fantastic", "I hated this film"]
    predictions = nb_clf.predict(test_texts)

    for text, pred in zip(test_texts, predictions):
        print(f"  '{text}' -> {pred}")

    # Embedding Classifier (needs embeddings with training vocab)
    # Create embeddings with sentiment words for demo
    sentiment_embeddings = WordEmbeddings.from_dict({
        "love": [0.9, 0.1], "amazing": [0.85, 0.15], "great": [0.8, 0.2],
        "best": [0.9, 0.1], "wonderful": [0.85, 0.15], "fantastic": [0.88, 0.12],
        "terrible": [0.1, 0.9], "awful": [0.15, 0.85], "worst": [0.1, 0.9],
        "boring": [0.2, 0.8], "hated": [0.1, 0.9], "bad": [0.15, 0.85],
    })
    print("\nEmbedding Classifier (centroid):")
    emb_clf = EmbeddingClassifier(sentiment_embeddings, strategy="centroid")
    emb_clf.fit(train_texts, train_labels)

    predictions = emb_clf.predict(test_texts)
    for text, pred in zip(test_texts, predictions):
        print(f"  '{text}' -> {pred}")

    # Summary
    section("SUMMARY")
    print("NLP Pipeline provides:")
    print("  - Tokenization (word & sentence)")
    print("  - Stopword removal (customizable)")
    print("  - Stemming (Porter & Snowball)")
    print("  - Lemmatization (WordNet)")
    print("  - Unified Pipeline (sklearn-compatible)")
    print("  - Word Embeddings (Word2Vec & GloVe)")
    print("  - Text Classification (Naive Bayes & Embedding-based)")
    print("\nRun: pytest --cov=nlp_pipeline")
    print("     114 tests, 93% coverage")


if __name__ == "__main__":
    main()
