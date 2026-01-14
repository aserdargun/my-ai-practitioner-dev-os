"""Tests for training utilities."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from sequence_models.training import train_epoch, evaluate, Trainer, TrainConfig


class SimpleModel(nn.Module):
    """Simple model for testing."""

    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)


def make_dataloader(n_samples=100, batch_size=16):
    """Create a simple dataloader for testing."""
    X = torch.randn(n_samples, 10)
    y = torch.randint(0, 2, (n_samples,)).float()
    dataset = TensorDataset(X, y)
    return DataLoader(dataset, batch_size=batch_size)


class TestTrainEpoch:
    """Tests for train_epoch function."""

    def test_returns_metrics(self):
        model = SimpleModel()
        loader = make_dataloader()
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(model.parameters())

        metrics = train_epoch(
            model, loader, criterion, optimizer,
            device=torch.device("cpu"),
            log_interval=0,
        )

        assert "loss" in metrics
        assert "num_samples" in metrics
        assert metrics["num_samples"] == 100

    def test_loss_decreases(self):
        model = SimpleModel()
        loader = make_dataloader()
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

        # Train multiple epochs
        losses = []
        for _ in range(5):
            metrics = train_epoch(
                model, loader, criterion, optimizer,
                device=torch.device("cpu"),
                log_interval=0,
            )
            losses.append(metrics["loss"])

        # Loss should generally decrease
        assert losses[-1] < losses[0]


class TestEvaluate:
    """Tests for evaluate function."""

    def test_returns_metrics(self):
        model = SimpleModel()
        loader = make_dataloader()
        criterion = nn.BCEWithLogitsLoss()

        metrics = evaluate(model, loader, criterion, torch.device("cpu"))

        assert "loss" in metrics
        assert "accuracy" in metrics
        assert "num_samples" in metrics
        assert 0 <= metrics["accuracy"] <= 1

    def test_no_gradient_tracking(self):
        model = SimpleModel()
        loader = make_dataloader()
        criterion = nn.BCEWithLogitsLoss()

        # Clear any existing gradients
        for p in model.parameters():
            p.grad = None

        evaluate(model, loader, criterion, torch.device("cpu"))

        # Should not have accumulated gradients
        for p in model.parameters():
            assert p.grad is None


class TestTrainer:
    """Tests for Trainer class."""

    def test_train_runs(self):
        model = SimpleModel()
        train_loader = make_dataloader(n_samples=50)
        val_loader = make_dataloader(n_samples=20)

        config = TrainConfig(epochs=2, log_interval=0)
        trainer = Trainer(model, train_loader, val_loader, config)

        history = trainer.train()

        assert len(history["train_loss"]) == 2
        assert len(history["val_loss"]) == 2
        assert len(history["val_accuracy"]) == 2

    def test_history_populated(self):
        model = SimpleModel()
        train_loader = make_dataloader(n_samples=50)

        config = TrainConfig(epochs=3, log_interval=0)
        trainer = Trainer(model, train_loader, config=config)

        history = trainer.train()

        assert len(history["train_loss"]) == 3
