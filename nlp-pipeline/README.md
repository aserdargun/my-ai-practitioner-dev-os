# NLP Pipeline

Text preprocessing and embedding pipeline for NLP.

## Setup

```bash
cd nlp-pipeline
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

### Tokenization

```python
from nlp_pipeline import Tokenizer

tokenizer = Tokenizer()

# Word tokenization
words = tokenizer.tokenize_words("Hello world!")
# ['hello', 'world', '!']

# Sentence tokenization
sentences = tokenizer.tokenize_sentences("First sentence. Second sentence.")
# ['first sentence.', 'second sentence.']

# Preserve case
tokenizer = Tokenizer(lowercase=False)
words = tokenizer.tokenize_words("Hello World")
# ['Hello', 'World']
```

### Stopword Removal

```python
from nlp_pipeline import StopwordRemover, Tokenizer

remover = StopwordRemover()

# Remove from token list
tokens = ["the", "quick", "brown", "fox"]
filtered = remover.remove(tokens)
# ['quick', 'brown', 'fox']

# Check if word is stopword
remover.is_stopword("the")  # True
remover.is_stopword("fox")  # False

# Remove directly from text (with tokenizer)
tokenizer = Tokenizer()
result = remover.remove_from_text("The quick brown fox", tokenizer)
# ['quick', 'brown', 'fox']

# Add custom stopwords
remover = StopwordRemover(extra_stopwords=["fox", "dog"])

# Keep specific words that would normally be removed
remover = StopwordRemover(keep_words=["the"])
```

### Stemming

```python
from nlp_pipeline import Stemmer

# Porter stemmer (default)
stemmer = Stemmer()
stemmer.stem("running")  # 'run'
stemmer.stem("cats")     # 'cat'

# Stem a list of tokens
tokens = ["running", "jumps", "easily"]
stemmer.stem_tokens(tokens)  # ['run', 'jump', 'easili']

# Stem text directly
stemmer.stem_text("The cats are running")  # ['the', 'cat', 'are', 'run']

# Snowball stemmer (supports multiple languages)
stemmer = Stemmer(algorithm="snowball", language="english")

# Spanish
stemmer = Stemmer(algorithm="snowball", language="spanish")
stemmer.stem("gatos")  # 'gat'

# Check available languages
print(Stemmer.SNOWBALL_LANGUAGES)
```

### Lemmatization

```python
from nlp_pipeline import Lemmatizer

lemmatizer = Lemmatizer()

# Lemmatize nouns (default)
lemmatizer.lemmatize("cats")      # 'cat'
lemmatizer.lemmatize("children")  # 'child'

# Lemmatize verbs (specify POS)
lemmatizer.lemmatize("running", pos="verb")  # 'run'
lemmatizer.lemmatize("ran", pos="verb")      # 'run'

# Lemmatize adjectives
lemmatizer.lemmatize("better", pos="adj")  # 'good'

# Lemmatize a list of tokens
tokens = ["cats", "dogs", "mice"]
lemmatizer.lemmatize_tokens(tokens)  # ['cat', 'dog', 'mouse']

# Set default POS to verb
lemmatizer = Lemmatizer(default_pos="verb")
lemmatizer.lemmatize("running")  # 'run'

# With Penn Treebank POS tags
tagged = [("cats", "NNS"), ("running", "VBG")]
lemmatizer.lemmatize_with_pos_tags(tagged)  # ['cat', 'run']
```

### Pipeline (Unified Preprocessing)

```python
from nlp_pipeline import Pipeline

# Default: lowercase + stopword removal + lemmatization
pipeline = Pipeline()
pipeline.process("The cats are running quickly")
# ['cat', 'running', 'quickly']

# Call directly
pipeline("The quick brown fox")
# ['quick', 'brown', 'fox']

# With stemming instead of lemmatization
pipeline = Pipeline(normalizer="stem")
pipeline("The cats are running")
# ['cat', 'run']

# No normalization (just tokenize + remove stopwords)
pipeline = Pipeline(normalizer=None)

# Keep all words (no stopword removal)
pipeline = Pipeline(remove_stopwords=False)

# Custom stopwords
pipeline = Pipeline(
    extra_stopwords=["custom", "words"],
    keep_stopwords=["the"],
)

# Batch processing
texts = ["First document", "Second document"]
pipeline.process_batch(texts)

# sklearn-style API
pipeline.fit_transform(texts)

# View configuration
print(pipeline.config)
print(pipeline)  # Pipeline(tokenize(lowercase) -> remove_stopwords -> lemmatize)
```

### Word Embeddings

```python
from nlp_pipeline import WordEmbeddings

# Load pre-trained Word2Vec format
embeddings = WordEmbeddings()
embeddings.load_word2vec_format("path/to/vectors.txt")

# Or GloVe format (no header line)
embeddings.load_glove_format("path/to/glove.txt")

# Load with vocabulary limit (for large files)
embeddings.load_word2vec_format("vectors.txt", limit=50000)

# Create from dictionary (for testing/custom vectors)
embeddings = WordEmbeddings.from_dict({
    "king": [0.9, 0.1, 0.0, 0.5],
    "queen": [0.85, 0.15, 0.0, 0.5],
})

# Check vocabulary
"king" in embeddings  # True
embeddings.vocab_size  # 2
embeddings.dimension   # 4

# Get vector
vec = embeddings["king"]

# Similarity between words
embeddings.similarity("king", "queen")  # ~0.99

# Find most similar words
embeddings.most_similar("king", topn=5)
# [('queen', 0.99), ('prince', 0.95), ...]

# Word analogies (king - man + woman = queen)
embeddings.analogy(positive=["king", "woman"], negative=["man"])
# [('queen', 0.89), ...]

# Find the outlier
embeddings.doesnt_match(["king", "queen", "prince", "car"])
# 'car'
```

### Text Classification

#### Naive Bayes Classifier

```python
from nlp_pipeline import NaiveBayesClassifier

# Training data
texts = [
    "I love this movie",
    "Great film, highly recommend",
    "Terrible movie, waste of time",
    "Awful film, do not watch",
]
labels = ["positive", "positive", "negative", "negative"]

# Train classifier
clf = NaiveBayesClassifier()
clf.fit(texts, labels)

# Predict
clf.predict(["This movie is amazing"])  # ['positive']

# Get probabilities
clf.predict_proba(["Good movie"])
# [{'positive': 0.85, 'negative': 0.15}]

# Evaluate accuracy
clf.score(test_texts, test_labels)  # 0.92

# Access properties
clf.classes      # ['positive', 'negative']
clf.vocab_size   # 24
```

#### Embedding-based Classifier

```python
from nlp_pipeline import EmbeddingClassifier, WordEmbeddings

# Load embeddings
embeddings = WordEmbeddings()
embeddings.load_word2vec_format("vectors.txt")

# Centroid classifier (default)
clf = EmbeddingClassifier(embeddings, strategy="centroid")
clf.fit(texts, labels)
clf.predict(["Amazing movie"])  # ['positive']

# KNN classifier
clf = EmbeddingClassifier(embeddings, strategy="knn", k=5)
clf.fit(texts, labels)
clf.predict(["Terrible film"])  # ['negative']

# Evaluate
clf.score(test_texts, test_labels)
```

### Dashboard

Interactive visualization for exploring word embeddings.

```bash
# Install dashboard dependencies
pip install -e ".[dashboard]"

# Run with sample embeddings
python scripts/run_dashboard.py

# Run with custom Word2Vec embeddings
python scripts/run_dashboard.py --embeddings path/to/vectors.txt

# Run with GloVe embeddings
python scripts/run_dashboard.py --embeddings path/to/glove.txt --format glove

# Limit vocabulary size (for large files)
python scripts/run_dashboard.py --embeddings vectors.txt --limit 10000
```

Then open http://localhost:8050

**Features:**
- t-SNE visualization of embedding space
- Similarity search — find words similar to a query
- Word analogies — solve "king - man + woman = ?" style queries

**Programmatic usage:**

```python
from nlp_pipeline import WordEmbeddings
from nlp_pipeline.dashboard import run_dashboard

# Load your embeddings
embeddings = WordEmbeddings()
embeddings.load_word2vec_format("vectors.txt")

# Launch dashboard
run_dashboard(embeddings, port=8050)
```

### GraphQL API

Query word embeddings via GraphQL.

```bash
# Install GraphQL dependencies
pip install -e ".[graphql]"

# Run with sample embeddings
python scripts/run_graphql.py

# Run with custom embeddings
python scripts/run_graphql.py --embeddings path/to/vectors.txt

# Run on different port
python scripts/run_graphql.py --port 8080
```

Then open http://localhost:8081/graphql for the GraphiQL interface.

**Available Queries:**

```graphql
# Get embedding info
{ info { vocabSize dimension } }

# Check if word exists
{ hasWord(word: "king") }

# Get word vector
{ wordVector(word: "king") { word vector dimension } }

# Calculate similarity between words
{ similarity(word1: "king", word2: "queen") }

# Find similar words
{ mostSimilar(word: "king", topN: 5) { word similarity } }

# Solve word analogies (king - man + woman = ?)
{
  analogy(
    positive: ["king", "woman"],
    negative: ["man"],
    topN: 3
  ) { word similarity }
}

# Find the word that doesn't match
{ doesntMatch(words: ["king", "queen", "prince", "car"]) }

# Search vocabulary by prefix
{ searchVocab(prefix: "ki", limit: 10) }
```

**Programmatic usage:**

```python
from nlp_pipeline import WordEmbeddings
from nlp_pipeline.graphql import create_app

# Load embeddings
embeddings = WordEmbeddings()
embeddings.load_word2vec_format("vectors.txt")

# Create and run Flask app
app = create_app(embeddings)
app.run(port=8081)
```

**Example curl request:**

```bash
curl -X POST http://localhost:8081/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ mostSimilar(word: \"king\", topN: 3) { word similarity } }"}'
```

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=nlp_pipeline
```

### Jupyter Notebook

Explore embeddings interactively in the notebook.

```bash
# Install Jupyter
pip install jupyter

# Launch notebook
jupyter notebook notebooks/embedding_exploration.ipynb
```

**Topics covered:**
- Loading and inspecting embeddings
- Similarity search
- Word analogies (king - man + woman = queen)
- t-SNE visualization
- Text classification with embeddings
- Vector arithmetic exploration
- Similarity matrices

## Project Structure

```
nlp-pipeline/
├── pyproject.toml
├── README.md
├── notebooks/
│   └── embedding_exploration.ipynb
├── scripts/
│   ├── run_dashboard.py
│   ├── run_graphql.py
│   └── pytorch_foundations.py
├── src/
│   └── nlp_pipeline/
│       ├── __init__.py
│       ├── tokenizer.py
│       ├── stopwords.py
│       ├── stemmer.py
│       ├── lemmatizer.py
│       ├── pipeline.py
│       ├── embeddings.py
│       ├── classifier.py
│       ├── dashboard/
│       │   ├── __init__.py
│       │   └── app.py
│       └── graphql/
│           ├── __init__.py
│           ├── schema.py
│           └── app.py
└── tests/
    ├── test_tokenizer.py
    ├── test_stopwords.py
    ├── test_stemmer.py
    ├── test_lemmatizer.py
    ├── test_pipeline.py
    ├── test_embeddings.py
    ├── test_classifier.py
    ├── test_dashboard.py
    └── test_graphql.py
```

## Roadmap

- [x] Basic tokenization (word, sentence)
- [x] Stopword removal
- [x] Stemming (Porter, Snowball)
- [x] Lemmatization
- [x] Unified Pipeline
- [x] Word embeddings (Word2Vec, GloVe)
- [x] Text classification (Naive Bayes, Embedding-based)
- [x] Interactive dashboard (t-SNE visualization, similarity search, analogies)
- [x] GraphQL API for embeddings
- [x] Jupyter notebook for embedding exploration
