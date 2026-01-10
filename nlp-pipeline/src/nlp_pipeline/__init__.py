"""NLP Pipeline - Text preprocessing and embedding utilities."""

from nlp_pipeline.classifier import EmbeddingClassifier, NaiveBayesClassifier
from nlp_pipeline.embeddings import WordEmbeddings
from nlp_pipeline.lemmatizer import Lemmatizer
from nlp_pipeline.pipeline import Pipeline
from nlp_pipeline.stemmer import Stemmer
from nlp_pipeline.stopwords import StopwordRemover
from nlp_pipeline.tokenizer import Tokenizer

__all__ = [
    "Tokenizer",
    "StopwordRemover",
    "Stemmer",
    "Lemmatizer",
    "Pipeline",
    "WordEmbeddings",
    "NaiveBayesClassifier",
    "EmbeddingClassifier",
]
__version__ = "0.1.0"
