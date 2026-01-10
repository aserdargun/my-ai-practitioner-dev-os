"""Tests for the Pipeline class."""


from nlp_pipeline import Pipeline


class TestPipeline:
    """Test suite for Pipeline."""

    def test_default_pipeline(self):
        """Test default pipeline configuration."""
        pipeline = Pipeline()
        result = pipeline.process("The cats are running quickly")
        # Default: lowercase, remove stopwords, lemmatize
        assert "cat" in result
        assert "run" not in result  # "running" as noun stays "running"
        assert "the" not in result  # stopword removed
        assert "are" not in result  # stopword removed

    def test_pipeline_with_stemming(self):
        """Test pipeline with stemming instead of lemmatization."""
        pipeline = Pipeline(normalizer="stem")
        result = pipeline.process("The cats are running quickly")
        assert "cat" in result
        assert "run" in result
        assert "quickli" in result  # Porter stemmer output

    def test_pipeline_no_normalization(self):
        """Test pipeline without normalization."""
        pipeline = Pipeline(normalizer=None)
        result = pipeline.process("The cats are running")
        assert "cats" in result  # not normalized
        assert "running" in result  # not normalized
        assert "the" not in result  # stopwords still removed

    def test_pipeline_no_stopword_removal(self):
        """Test pipeline without stopword removal."""
        pipeline = Pipeline(remove_stopwords=False)
        result = pipeline.process("The cats are here")
        assert "the" in result
        assert "are" in result

    def test_pipeline_no_lowercase(self):
        """Test pipeline without lowercasing."""
        pipeline = Pipeline(lowercase=False, normalizer=None, remove_stopwords=False)
        result = pipeline.process("Hello World")
        assert "Hello" in result
        assert "World" in result

    def test_pipeline_callable(self):
        """Test that pipeline can be called directly."""
        pipeline = Pipeline()
        result = pipeline("The quick brown fox")
        assert isinstance(result, list)
        assert "quick" in result
        assert "brown" in result
        assert "fox" in result

    def test_pipeline_batch_processing(self):
        """Test processing multiple texts."""
        pipeline = Pipeline()
        texts = ["The cats sleep", "Dogs run fast"]
        results = pipeline.process_batch(texts)
        assert len(results) == 2
        assert "cat" in results[0]
        assert "dog" in results[1]

    def test_pipeline_empty_text(self):
        """Test processing empty text."""
        pipeline = Pipeline()
        result = pipeline.process("")
        assert result == []

    def test_pipeline_sklearn_api(self):
        """Test sklearn-style fit/transform API."""
        pipeline = Pipeline()
        texts = ["Cats running", "Dogs jumping"]

        # fit returns self
        assert pipeline.fit(texts) is pipeline

        # transform works
        results = pipeline.transform(texts)
        assert len(results) == 2

        # fit_transform works
        results = pipeline.fit_transform(texts)
        assert len(results) == 2

    def test_pipeline_extra_stopwords(self):
        """Test adding extra stopwords."""
        pipeline = Pipeline(extra_stopwords=["cat", "dog"])
        result = pipeline.process("The cat and dog play")
        assert "cat" not in result
        assert "dog" not in result
        assert "play" in result

    def test_pipeline_keep_stopwords(self):
        """Test keeping specific stopwords."""
        pipeline = Pipeline(keep_stopwords=["the"])
        result = pipeline.process("The cat is here")
        assert "the" in result
        assert "is" not in result

    def test_pipeline_snowball_stemmer(self):
        """Test pipeline with Snowball stemmer."""
        pipeline = Pipeline(normalizer="stem", stemmer_algorithm="snowball")
        result = pipeline.process("running jumping")
        assert "run" in result
        assert "jump" in result

    def test_pipeline_verb_lemmatization(self):
        """Test pipeline with verb lemmatization."""
        pipeline = Pipeline(normalizer="lemmatize", lemmatizer_pos="verb")
        result = pipeline.process("running jumping swimming")
        assert "run" in result
        assert "jump" in result
        assert "swim" in result

    def test_pipeline_config(self):
        """Test getting pipeline configuration."""
        pipeline = Pipeline(
            lowercase=True,
            remove_stopwords=True,
            normalizer="stem",
            language="english",
        )
        config = pipeline.config
        assert config["lowercase"] is True
        assert config["remove_stopwords"] is True
        assert config["normalizer"] == "stem"
        assert config["language"] == "english"

    def test_pipeline_repr(self):
        """Test string representation."""
        pipeline = Pipeline()
        repr_str = repr(pipeline)
        assert "Pipeline" in repr_str
        assert "tokenize" in repr_str
        assert "remove_stopwords" in repr_str
        assert "lemmatize" in repr_str

    def test_pipeline_repr_minimal(self):
        """Test repr with minimal pipeline."""
        pipeline = Pipeline(
            lowercase=False,
            remove_stopwords=False,
            normalizer=None,
        )
        repr_str = repr(pipeline)
        assert "tokenize" in repr_str
        assert "remove_stopwords" not in repr_str
        assert "lemmatize" not in repr_str

    def test_pipeline_full_flow(self):
        """Test complete pipeline flow with real text."""
        pipeline = Pipeline(
            lowercase=True,
            remove_stopwords=True,
            normalizer="lemmatize",
        )
        text = "The quick brown foxes are jumping over the lazy dogs."
        result = pipeline.process(text)

        # Stopwords removed
        assert "the" not in result
        assert "are" not in result
        assert "over" not in result

        # Lemmatized
        assert "fox" in result
        assert "dog" in result
        assert "lazy" in result

    def test_pipeline_punctuation_handling(self):
        """Test that punctuation is handled correctly."""
        pipeline = Pipeline()
        result = pipeline.process("Hello, world! How are you?")
        # Punctuation becomes separate tokens, stopwords removed
        assert "hello" in result
        assert "world" in result
