#!/usr/bin/env python3
"""PyTorch Foundations — Month 2 Preview.

This script covers the essential PyTorch concepts you'll need for
building RNNs and LSTMs in Month 2.

Topics:
1. Tensors — the fundamental data structure
2. Autograd — automatic differentiation
3. Neural Networks — building blocks with nn.Module
4. Training Loop — the core pattern for learning

Run with: python scripts/pytorch_foundations.py
"""

import torch
import torch.nn as nn
import torch.optim as optim

# =============================================================================
# DEVICE SETUP — Use MPS on Apple Silicon, CUDA on NVIDIA, else CPU
# =============================================================================

def get_device():
    """Get the best available device."""
    if torch.backends.mps.is_available():
        return torch.device("mps")  # Apple Silicon (M1/M2/M3/M4)
    elif torch.cuda.is_available():
        return torch.device("cuda")  # NVIDIA GPU
    else:
        return torch.device("cpu")

DEVICE = get_device()
print(f"Using device: {DEVICE}")
print("=" * 60)


# =============================================================================
# PART 1: TENSORS
# =============================================================================

def explore_tensors():
    """Explore PyTorch tensors — the fundamental data structure."""
    print("\n📦 PART 1: TENSORS")
    print("-" * 40)

    # Creating tensors
    # ----------------

    # From Python lists
    t1 = torch.tensor([1, 2, 3, 4])
    print(f"From list: {t1}")

    # Zeros and ones
    zeros = torch.zeros(2, 3)
    ones = torch.ones(2, 3)
    print(f"Zeros (2x3):\n{zeros}")
    print(f"Ones (2x3):\n{ones}")

    # Random tensors (common for weight initialization)
    rand = torch.randn(2, 3)  # Normal distribution
    print(f"Random (2x3):\n{rand}")

    # Tensor properties
    # -----------------
    print("\nTensor properties:")
    print(f"  Shape: {rand.shape}")
    print(f"  Dtype: {rand.dtype}")
    print(f"  Device: {rand.device}")

    # Moving to GPU (MPS on M4 Pro)
    # -----------------------------
    t_gpu = rand.to(DEVICE)
    print(f"  After .to(device): {t_gpu.device}")

    # Tensor operations
    # -----------------
    a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
    b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)

    print("\nTensor operations:")
    print(f"  a + b = \n{a + b}")
    print(f"  a * b (element-wise) = \n{a * b}")
    print(f"  a @ b (matrix multiply) = \n{a @ b}")

    # Reshaping
    # ---------
    c = torch.arange(12)
    print("\nReshaping:")
    print(f"  Original: {c}")
    print(f"  Reshaped (3x4): \n{c.reshape(3, 4)}")
    print(f"  View (2x6): \n{c.view(2, 6)}")

    return t_gpu


# =============================================================================
# PART 2: AUTOGRAD (Automatic Differentiation)
# =============================================================================

def explore_autograd():
    """Explore autograd — PyTorch's automatic differentiation engine."""
    print("\n🔄 PART 2: AUTOGRAD")
    print("-" * 40)

    # Tensors with gradients
    # ----------------------
    # requires_grad=True tells PyTorch to track operations for backprop
    x = torch.tensor([2.0, 3.0], requires_grad=True)
    print(f"x (requires_grad=True): {x}")

    # Forward pass — build computation graph
    y = x ** 2  # y = x^2
    z = y.sum()  # z = sum(x^2) = scalar
    print(f"y = x^2: {y}")
    print(f"z = sum(y): {z}")

    # Backward pass — compute gradients
    z.backward()

    # Gradient: dz/dx = 2x
    print(f"Gradient dz/dx: {x.grad}")  # Should be [4.0, 6.0]
    print(f"Expected (2*x): {2 * x.detach()}")

    # Gradient accumulation
    # ---------------------
    print("\nGradient accumulation (common gotcha!):")
    w = torch.tensor([1.0], requires_grad=True)

    for i in range(3):
        loss = w * 2
        loss.backward()
        print(f"  Iteration {i+1}: grad = {w.grad}")

    print("  ⚠️  Gradients accumulate! Always zero them before backward().")

    # Correct pattern
    print("\nCorrect pattern with zero_grad():")
    w = torch.tensor([1.0], requires_grad=True)

    for i in range(3):
        if w.grad is not None:
            w.grad.zero_()  # Zero gradients!
        loss = w * 2
        loss.backward()
        print(f"  Iteration {i+1}: grad = {w.grad}")

    # No grad context
    # ---------------
    print("\nUsing torch.no_grad() for inference:")
    x = torch.tensor([1.0, 2.0], requires_grad=True)

    with torch.no_grad():
        y = x * 2
        print(f"  In no_grad: y.requires_grad = {y.requires_grad}")


# =============================================================================
# PART 3: NEURAL NETWORKS (nn.Module)
# =============================================================================

class SimpleNet(nn.Module):
    """A simple feedforward neural network.

    Architecture:
        Input (4) -> Hidden (8) -> ReLU -> Output (2)
    """

    def __init__(self, input_size=4, hidden_size=8, output_size=2):
        super().__init__()

        # Define layers
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """Forward pass through the network."""
        x = self.fc1(x)      # Linear: (batch, 4) -> (batch, 8)
        x = self.relu(x)      # Activation
        x = self.fc2(x)       # Linear: (batch, 8) -> (batch, 2)
        return x


def explore_neural_networks():
    """Explore nn.Module — the building block for neural networks."""
    print("\n🧠 PART 3: NEURAL NETWORKS")
    print("-" * 40)

    # Create model
    model = SimpleNet()
    print(f"Model architecture:\n{model}")

    # Move to device (MPS on M4 Pro)
    model = model.to(DEVICE)
    print(f"\nModel device: {next(model.parameters()).device}")

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params}")
    print(f"Trainable parameters: {trainable_params}")

    # Inspect layers
    print("\nLayer details:")
    for name, param in model.named_parameters():
        print(f"  {name}: shape={param.shape}, requires_grad={param.requires_grad}")

    # Forward pass
    print("\nForward pass:")
    batch_size = 3
    x = torch.randn(batch_size, 4, device=DEVICE)
    print(f"  Input shape: {x.shape}")

    output = model(x)
    print(f"  Output shape: {output.shape}")
    print(f"  Output:\n{output}")

    return model


# =============================================================================
# PART 4: TRAINING LOOP
# =============================================================================

def explore_training_loop():
    """Explore the training loop — the core pattern for learning."""
    print("\n🏋️ PART 4: TRAINING LOOP")
    print("-" * 40)

    # Create synthetic dataset
    # Binary classification: points inside/outside a circle
    torch.manual_seed(42)

    n_samples = 200
    X = torch.randn(n_samples, 2)
    # Label: 1 if inside unit circle, 0 otherwise
    y = (X[:, 0]**2 + X[:, 1]**2 < 1).float().unsqueeze(1)

    print(f"Dataset: {n_samples} samples")
    print(f"  X shape: {X.shape}")
    print(f"  y shape: {y.shape}")
    print(f"  Class balance: {y.mean().item():.2%} positive")

    # Move to device
    X = X.to(DEVICE)
    y = y.to(DEVICE)

    # Create model
    model = nn.Sequential(
        nn.Linear(2, 16),
        nn.ReLU(),
        nn.Linear(16, 8),
        nn.ReLU(),
        nn.Linear(8, 1),
        nn.Sigmoid()  # Output probability [0, 1]
    ).to(DEVICE)

    print(f"\nModel:\n{model}")

    # Loss function and optimizer
    criterion = nn.BCELoss()  # Binary Cross Entropy
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # Training loop
    print("\nTraining:")
    n_epochs = 100

    for epoch in range(n_epochs):
        # Forward pass
        outputs = model(X)
        loss = criterion(outputs, y)

        # Backward pass
        optimizer.zero_grad()  # Zero gradients (important!)
        loss.backward()        # Compute gradients
        optimizer.step()       # Update weights

        # Log progress
        if (epoch + 1) % 20 == 0:
            # Calculate accuracy
            with torch.no_grad():
                predictions = (outputs > 0.5).float()
                accuracy = (predictions == y).float().mean()
            print(f"  Epoch {epoch+1:3d}: Loss={loss.item():.4f}, Accuracy={accuracy.item():.2%}")

    # Final evaluation
    print("\nFinal evaluation:")
    model.eval()  # Set to evaluation mode
    with torch.no_grad():
        outputs = model(X)
        predictions = (outputs > 0.5).float()
        accuracy = (predictions == y).float().mean()
        print(f"  Final Accuracy: {accuracy.item():.2%}")

    return model


# =============================================================================
# PREVIEW: RNN BUILDING BLOCKS (Month 2)
# =============================================================================

def preview_rnn_concepts():
    """Preview RNN concepts for Month 2."""
    print("\n🔮 PREVIEW: RNN BUILDING BLOCKS (Month 2)")
    print("-" * 40)

    # Sequences in NLP
    print("In Month 2, you'll work with sequences:")
    print("  - Text: 'The cat sat' -> [token1, token2, token3]")
    print("  - Each token becomes an embedding vector")
    print("  - RNN processes sequence step by step")

    # Simple RNN layer
    print("\nSimple RNN layer:")
    rnn = nn.RNN(input_size=10, hidden_size=20, num_layers=1, batch_first=True)
    rnn = rnn.to(DEVICE)

    # Input: (batch, sequence_length, input_size)
    batch_size = 2
    seq_length = 5
    input_size = 10

    x = torch.randn(batch_size, seq_length, input_size, device=DEVICE)
    print(f"  Input shape: {x.shape}")
    print(f"    (batch={batch_size}, seq_len={seq_length}, input_size={input_size})")

    # RNN output
    output, hidden = rnn(x)
    print(f"  Output shape: {output.shape}")
    print(f"    (batch={batch_size}, seq_len={seq_length}, hidden_size=20)")
    print(f"  Hidden shape: {hidden.shape}")
    print(f"    (num_layers=1, batch={batch_size}, hidden_size=20)")

    # LSTM layer
    print("\nLSTM layer (Month 2 focus):")
    lstm = nn.LSTM(input_size=10, hidden_size=20, num_layers=1, batch_first=True)
    lstm = lstm.to(DEVICE)

    output, (hidden, cell) = lstm(x)
    print("  LSTM has TWO hidden states:")
    print(f"    hidden (h): {hidden.shape}")
    print(f"    cell (c): {cell.shape}")
    print("  The cell state is what makes LSTM better at long sequences!")

    print("\n✅ You're ready for Month 2: Sequence Models!")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all PyTorch foundations explorations."""
    print("=" * 60)
    print("🔥 PyTorch Foundations — Month 2 Preview")
    print("=" * 60)

    explore_tensors()
    explore_autograd()
    explore_neural_networks()
    explore_training_loop()
    preview_rnn_concepts()

    print("\n" + "=" * 60)
    print("🎉 PyTorch Foundations Complete!")
    print("=" * 60)
    print("\nKey takeaways:")
    print("  1. Tensors: Like NumPy arrays, but GPU-accelerated")
    print("  2. Autograd: Automatic gradients via .backward()")
    print("  3. nn.Module: Building blocks for neural networks")
    print("  4. Training: forward -> loss -> backward -> step")
    print(f"\nYour M4 Pro is ready with MPS acceleration: {DEVICE}")


if __name__ == "__main__":
    main()
