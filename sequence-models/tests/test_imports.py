"""Test that core imports work."""

import torch


def test_torch_available():
    """Verify PyTorch is installed and accessible."""
    assert torch.__version__ is not None


def test_cuda_check():
    """Check CUDA availability (informational, doesn't fail)."""
    cuda_available = torch.cuda.is_available()
    mps_available = torch.backends.mps.is_available()
    print(f"CUDA available: {cuda_available}")
    print(f"MPS available: {mps_available}")
    # Always passes - just informational
    assert True


def test_sequence_models_import():
    """Verify our package imports correctly."""
    import sequence_models

    assert sequence_models.__version__ == "0.1.0"
