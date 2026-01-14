"""Tests for data loading utilities."""

import pytest
import torch

from sequence_models.data import IMDBDataset, build_vocab, clean_text


class TestCleanText:
    """Tests for text cleaning."""

    def test_removes_html(self):
        text = "Hello <br> World <p>Test</p>"
        assert "<" not in clean_text(text)
        assert ">" not in clean_text(text)

    def test_lowercase(self):
        text = "HELLO World"
        result = clean_text(text)
        assert result == result.lower()

    def test_normalizes_whitespace(self):
        text = "hello    world\n\ntest"
        result = clean_text(text)
        assert "  " not in result
        assert "\n" not in result


class TestBuildVocab:
    """Tests for vocabulary building."""

    def test_includes_special_tokens(self):
        texts = ["hello world", "world test"]
        vocab = build_vocab(texts, max_vocab_size=100, min_freq=1)
        assert "<pad>" in vocab
        assert "<unk>" in vocab
        assert vocab["<pad>"] == 0
        assert vocab["<unk>"] == 1

    def test_respects_max_size(self):
        texts = ["a b c d e f g h i j k l m n o"]
        vocab = build_vocab(texts, max_vocab_size=5, min_freq=1)
        assert len(vocab) <= 5

    def test_respects_min_freq(self):
        texts = ["hello hello world"]
        vocab = build_vocab(texts, max_vocab_size=100, min_freq=2)
        assert "hello" in vocab
        assert "world" not in vocab  # Only appears once


class TestIMDBDataset:
    """Tests for IMDB dataset."""

    @pytest.fixture
    def sample_data(self):
        texts = ["great movie loved it", "terrible film hated it", "amazing performance"]
        labels = [1, 0, 1]
        vocab = {"<pad>": 0, "<unk>": 1, "great": 2, "movie": 3, "loved": 4, "it": 5}
        return texts, labels, vocab

    def test_len(self, sample_data):
        texts, labels, vocab = sample_data
        dataset = IMDBDataset(texts, labels, vocab, max_len=10)
        assert len(dataset) == 3

    def test_getitem_shape(self, sample_data):
        texts, labels, vocab = sample_data
        dataset = IMDBDataset(texts, labels, vocab, max_len=10)
        x, y = dataset[0]
        assert x.shape == torch.Size([10])
        assert y.shape == torch.Size([])

    def test_padding(self, sample_data):
        texts, labels, vocab = sample_data
        dataset = IMDBDataset(texts, labels, vocab, max_len=10)
        x, _ = dataset[0]
        # Should have padding at the end
        assert x[-1].item() == vocab["<pad>"]

    def test_truncation(self, sample_data):
        texts, labels, vocab = sample_data
        dataset = IMDBDataset(texts, labels, vocab, max_len=2)
        x, _ = dataset[0]
        assert x.shape == torch.Size([2])

    def test_unknown_tokens(self, sample_data):
        texts, labels, vocab = sample_data
        dataset = IMDBDataset(texts, labels, vocab, max_len=10)
        # "terrible" is not in vocab, should map to <unk>=1
        x, _ = dataset[1]
        assert vocab["<unk>"] in x.tolist()
