"""Embedding-based text classifier."""

import torch
import torch.nn as nn


class EmbeddingClassifier(nn.Module):
    """Simple embedding classifier using mean pooling.

    Architecture: Embedding → Mean Pool → FC layers → Output

    Args:
        vocab_size: Size of vocabulary
        embed_dim: Embedding dimension
        hidden_dim: Hidden layer dimension
        output_dim: Output dimension (1 for binary)
        padding_idx: Index used for padding (excluded from mean)
        dropout: Dropout probability
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 128,
        hidden_dim: int = 64,
        output_dim: int = 1,
        padding_idx: int = 0,
        dropout: float = 0.3,
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size, embed_dim, padding_idx=padding_idx
        )
        self.dropout = nn.Dropout(dropout)

        self.fc = nn.Sequential(
            nn.Linear(embed_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Token indices of shape (batch_size, seq_len)

        Returns:
            Logits of shape (batch_size, output_dim)
        """
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        embedded = self.dropout(embedded)

        # Mean pooling (ignore padding)
        mask = (x != self.embedding.padding_idx).unsqueeze(-1).float()
        summed = (embedded * mask).sum(dim=1)
        lengths = mask.sum(dim=1).clamp(min=1)
        pooled = summed / lengths  # (batch, embed_dim)

        return self.fc(pooled)
