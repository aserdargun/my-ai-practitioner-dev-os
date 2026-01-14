"""Training loop implementation."""

import time
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader


@dataclass
class TrainConfig:
    """Training configuration."""

    epochs: int = 10
    learning_rate: float = 0.001
    device: str = "auto"
    checkpoint_dir: str | None = None
    log_interval: int = 100


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    log_interval: int = 100,
) -> dict:
    """Train for one epoch.

    Args:
        model: The neural network
        loader: Training data loader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on
        log_interval: Print progress every N batches

    Returns:
        Dict with 'loss' (average) and 'num_samples'
    """
    model.train()
    total_loss = 0.0
    num_samples = 0

    for batch_idx, (X, y) in enumerate(loader):
        X, y = X.to(device), y.to(device)

        # Forward pass
        output = model(X)
        if output.dim() > 1 and output.size(1) == 1:
            output = output.squeeze(1)
        loss = criterion(output, y)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Track metrics
        batch_size = X.size(0)
        total_loss += loss.item() * batch_size
        num_samples += batch_size

        # Log progress
        if log_interval and (batch_idx + 1) % log_interval == 0:
            avg_loss = total_loss / num_samples
            print(f"  Batch {batch_idx + 1}/{len(loader)}: loss={avg_loss:.4f}")

    return {"loss": total_loss / num_samples, "num_samples": num_samples}


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict:
    """Evaluate model on a dataset.

    Args:
        model: The neural network
        loader: Data loader
        criterion: Loss function
        device: Device to evaluate on

    Returns:
        Dict with 'loss', 'accuracy', 'num_samples'
    """
    model.eval()
    total_loss = 0.0
    correct = 0
    num_samples = 0

    with torch.no_grad():
        for X, y in loader:
            X, y = X.to(device), y.to(device)

            output = model(X)
            if output.dim() > 1 and output.size(1) == 1:
                output = output.squeeze(1)

            loss = criterion(output, y)

            # For binary classification
            predictions = (torch.sigmoid(output) > 0.5).float()
            correct += (predictions == y).sum().item()

            batch_size = X.size(0)
            total_loss += loss.item() * batch_size
            num_samples += batch_size

    return {
        "loss": total_loss / num_samples,
        "accuracy": correct / num_samples,
        "num_samples": num_samples,
    }


class Trainer:
    """Training manager with logging and checkpointing.

    Args:
        model: Neural network to train
        train_loader: Training data loader
        val_loader: Validation data loader (optional)
        config: Training configuration
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader | None = None,
        config: TrainConfig | None = None,
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config or TrainConfig()

        # Setup device
        if self.config.device == "auto":
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")
        else:
            self.device = torch.device(self.config.device)

        self.model.to(self.device)

        # Loss and optimizer
        self.criterion = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.Adam(
            model.parameters(), lr=self.config.learning_rate
        )

        # History
        self.history = {"train_loss": [], "val_loss": [], "val_accuracy": []}

    def train(self) -> dict:
        """Run full training loop.

        Returns:
            Training history dict
        """
        print(f"Training on {self.device}")
        print(f"Train batches: {len(self.train_loader)}")
        if self.val_loader:
            print(f"Val batches: {len(self.val_loader)}")
        print("-" * 50)

        best_val_acc = 0.0

        for epoch in range(self.config.epochs):
            start_time = time.time()

            # Train
            train_metrics = train_epoch(
                self.model,
                self.train_loader,
                self.criterion,
                self.optimizer,
                self.device,
                log_interval=self.config.log_interval,
            )
            self.history["train_loss"].append(train_metrics["loss"])

            # Validate
            if self.val_loader:
                val_metrics = evaluate(
                    self.model, self.val_loader, self.criterion, self.device
                )
                self.history["val_loss"].append(val_metrics["loss"])
                self.history["val_accuracy"].append(val_metrics["accuracy"])

                # Save best model
                if (
                    self.config.checkpoint_dir
                    and val_metrics["accuracy"] > best_val_acc
                ):
                    best_val_acc = val_metrics["accuracy"]
                    self._save_checkpoint(epoch, val_metrics["accuracy"])

            # Log epoch
            elapsed = time.time() - start_time
            self._log_epoch(epoch, train_metrics, val_metrics if self.val_loader else None, elapsed)

        print("-" * 50)
        print("Training complete!")
        if self.val_loader:
            print(f"Best val accuracy: {best_val_acc:.1%}")

        return self.history

    def _log_epoch(self, epoch: int, train: dict, val: dict | None, elapsed: float):
        """Log epoch results."""
        msg = f"Epoch {epoch + 1}/{self.config.epochs}: "
        msg += f"train_loss={train['loss']:.4f}"
        if val:
            msg += f", val_loss={val['loss']:.4f}, val_acc={val['accuracy']:.1%}"
        msg += f" ({elapsed:.1f}s)"
        print(msg)

    def _save_checkpoint(self, epoch: int, accuracy: float):
        """Save model checkpoint."""
        checkpoint_dir = Path(self.config.checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        path = checkpoint_dir / f"best_model.pt"
        torch.save(
            {
                "epoch": epoch,
                "model_state_dict": self.model.state_dict(),
                "optimizer_state_dict": self.optimizer.state_dict(),
                "accuracy": accuracy,
            },
            path,
        )
        print(f"  Saved checkpoint: {path}")
