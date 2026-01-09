"""FastAPI ML Service - Main Application."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="ML Model Service",
    description="Production-ready ML model serving API",
    version="1.0.0",
)


class PredictionInput(BaseModel):
    """Input schema for predictions."""

    features: list[float] = Field(
        ...,
        description="List of feature values for prediction",
        min_length=1,
        max_length=100,
    )


class PredictionOutput(BaseModel):
    """Output schema for predictions."""

    prediction: float
    confidence: float = Field(ge=0.0, le=1.0)


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool


# Mock model - replace with actual model loading
class MockModel:
    """Mock model for demonstration."""

    def __init__(self):
        self.loaded = True

    def predict(self, features: list[float]) -> tuple[float, float]:
        """Return mock prediction and confidence."""
        # Simple mock: sum of features as prediction
        prediction = sum(features) / len(features)
        confidence = 0.85
        return prediction, confidence


# Initialize model at startup
model = MockModel()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health and model status."""
    return HealthResponse(
        status="healthy",
        model_loaded=model.loaded,
    )


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """Generate prediction for input features."""
    if not model.loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        prediction, confidence = model.predict(input_data.features)
        return PredictionOutput(
            prediction=prediction,
            confidence=confidence,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "ML Model Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
