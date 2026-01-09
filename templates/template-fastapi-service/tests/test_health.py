"""Tests for FastAPI ML Service."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data


def test_predict_valid_input():
    """Test prediction with valid input."""
    response = client.post(
        "/predict",
        json={"features": [1.0, 2.0, 3.0, 4.0]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_empty_features():
    """Test prediction with empty features fails validation."""
    response = client.post(
        "/predict",
        json={"features": []},
    )
    assert response.status_code == 422  # Validation error


def test_predict_invalid_input():
    """Test prediction with invalid input type."""
    response = client.post(
        "/predict",
        json={"features": "not_a_list"},
    )
    assert response.status_code == 422


def test_predict_missing_features():
    """Test prediction with missing features field."""
    response = client.post(
        "/predict",
        json={},
    )
    assert response.status_code == 422
