"""Tests for neural network models."""

import torch
from sequence_models.models import FeedforwardClassifier


class TestFeedforwardClassifier:
    """Tests for FeedforwardClassifier."""

    def test_forward_shape(self):
        """Output shape matches expected."""
        model = FeedforwardClassifier(
            input_size=10,
            hidden_sizes=[32, 16],
            output_size=1,
        )
        x = torch.randn(8, 10)  # batch of 8
        out = model(x)
        assert out.shape == (8, 1)

    def test_forward_multiclass(self):
        """Multi-class output shape."""
        model = FeedforwardClassifier(
            input_size=10,
            hidden_sizes=[32],
            output_size=5,  # 5 classes
        )
        x = torch.randn(4, 10)
        out = model(x)
        assert out.shape == (4, 5)

    def test_dropout(self):
        """Dropout is applied in training mode."""
        model = FeedforwardClassifier(
            input_size=10,
            hidden_sizes=[32],
            output_size=1,
            dropout=0.5,
        )
        x = torch.randn(4, 10)

        # In eval mode, outputs should be deterministic
        model.eval()
        out1 = model(x)
        out2 = model(x)
        assert torch.equal(out1, out2)

    def test_gradient_flow(self):
        """Gradients flow through the model."""
        model = FeedforwardClassifier(
            input_size=10,
            hidden_sizes=[32, 16],
            output_size=1,
        )
        x = torch.randn(4, 10)
        y = torch.ones(4, 1)

        out = model(x)
        loss = ((out - y) ** 2).mean()
        loss.backward()

        # Check gradients exist
        for param in model.parameters():
            assert param.grad is not None
            assert param.grad.shape == param.shape

    def test_parameter_count(self):
        """Parameter count is correct."""
        model = FeedforwardClassifier(
            input_size=2,
            hidden_sizes=[16, 8],
            output_size=1,
        )
        # layer1: 2*16 + 16 = 48
        # layer2: 16*8 + 8 = 136
        # layer3: 8*1 + 1 = 9
        # total = 193
        total = sum(p.numel() for p in model.parameters())
        assert total == 193
