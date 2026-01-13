"""Feedforward neural network for classification."""

import torch.nn as nn


class FeedforwardClassifier(nn.Module):
    """Simple feedforward classifier.

    Architecture: input → hidden layers with ReLU → output

    Args:
        input_size: Number of input features
        hidden_sizes: List of hidden layer sizes (e.g., [64, 32])
        output_size: Number of output classes (1 for binary)
        dropout: Dropout probability (default 0.0)
    """

    def __init__(
        self,
        input_size: int,
        hidden_sizes: list[int],
        output_size: int = 1,
        dropout: float = 0.0,
    ):
        super().__init__()

        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            if dropout > 0:
                layers.append(nn.Dropout(dropout))
            prev_size = hidden_size

        layers.append(nn.Linear(prev_size, output_size))

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        """Forward pass.

        Args:
            x: Input tensor of shape (batch_size, input_size)

        Returns:
            Logits of shape (batch_size, output_size)
        """
        return self.net(x)
