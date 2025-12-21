"""
FastAPI REST API for Premier League Match Predictor.

This module provides REST endpoints for making match predictions.

Example:
    Start the server:
    $ uvicorn src.server.api.main:app --reload

    Access docs:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
import sys
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.server.model.modelbuild.make_prediction import (
        predict_from_recent_form,
        predict_with_custom_weights,
    )
except ImportError:
    logger.warning("Could not import prediction functions. Using mock mode.")
    predict_from_recent_form = None
    predict_with_custom_weights = None

# Create FastAPI app
app = FastAPI(
    title="Premier League Match Predictor API",
    description="""
    🏆 Predict Premier League match outcomes using ML!
    
    This API uses a Random Forest classifier trained on 500+ real matches
    to predict match outcomes based on team statistics from their last 5 games.
    
    ## Features
    
    * **Home Win / Draw / Away Win** predictions
    * **Confidence scores** for each outcome
    * **Flexible weighting** of recent games
    * **Team performance averages**
    
    ## Usage
    
    1. Collect statistics from each team's last 5 games
    2. POST to `/predict` endpoint
    3. Get prediction with probabilities
    """,
    version="1.0.0",
    contact={
        "name": "Miguel Vila",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class GameStats(BaseModel):
    """Statistics from a single game."""

    possession: float = Field(
        ..., ge=0.0, le=100.0, description="Possession percentage (0-100)", example=55.0
    )
    shots_on_target: int = Field(
        ..., ge=0, le=30, description="Number of shots on target", example=5
    )
    corners: int = Field(..., ge=0, le=20, description="Number of corners", example=6)
    fouls: int = Field(..., ge=0, le=30, description="Number of fouls committed", example=10)

    @validator("possession")
    def validate_possession(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Possession must be between 0 and 100")
        return v

    class Config:
        schema_extra = {
            "example": {
                "possession": 55.0,
                "shots_on_target": 5,
                "corners": 6,
                "fouls": 10,
            }
        }


class PredictionRequest(BaseModel):
    """Request body for match prediction."""

    home_team_last_5: List[GameStats] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="Statistics from home team's last 5 games (oldest to newest)",
    )
    away_team_last_5: List[GameStats] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="Statistics from away team's last 5 games (oldest to newest)",
    )

    @validator("home_team_last_5", "away_team_last_5")
    def validate_game_count(cls, v):
        if len(v) < 1:
            raise ValueError("Must provide at least 1 game")
        return v

    class Config:
        schema_extra = {
            "example": {
                "home_team_last_5": [
                    {
                        "possession": 55.0,
                        "shots_on_target": 5,
                        "corners": 6,
                        "fouls": 10,
                    },
                    {
                        "possession": 52.0,
                        "shots_on_target": 4,
                        "corners": 5,
                        "fouls": 11,
                    },
                    {
                        "possession": 58.0,
                        "shots_on_target": 6,
                        "corners": 7,
                        "fouls": 9,
                    },
                    {
                        "possession": 50.0,
                        "shots_on_target": 3,
                        "corners": 4,
                        "fouls": 12,
                    },
                    {
                        "possession": 60.0,
                        "shots_on_target": 7,
                        "corners": 8,
                        "fouls": 8,
                    },
                ],
                "away_team_last_5": [
                    {
                        "possession": 45.0,
                        "shots_on_target": 3,
                        "corners": 4,
                        "fouls": 13,
                    },
                    {
                        "possession": 48.0,
                        "shots_on_target": 4,
                        "corners": 5,
                        "fouls": 12,
                    },
                    {
                        "possession": 42.0,
                        "shots_on_target": 2,
                        "corners": 3,
                        "fouls": 15,
                    },
                    {
                        "possession": 50.0,
                        "shots_on_target": 5,
                        "corners": 6,
                        "fouls": 11,
                    },
                    {
                        "possession": 40.0,
                        "shots_on_target": 3,
                        "corners": 4,
                        "fouls": 14,
                    },
                ],
            }
        }


class WeightedPredictionRequest(PredictionRequest):
    """Request body for weighted prediction."""

    weights: Optional[List[float]] = Field(
        None,
        description="Custom weights for each game (must sum to 1). If not provided, recent games are weighted higher.",
        example=[0.1, 0.15, 0.2, 0.25, 0.3],
    )


class PredictionResponse(BaseModel):
    """Response from match prediction."""

    prediction: str = Field(..., description="Predicted outcome: 'Home Win', 'Draw', or 'Away Win'")
    prediction_code: int = Field(..., description="Numeric code: 1=Home Win, 0=Draw, -1=Away Win")
    confidence: float = Field(..., description="Confidence level (0-100)")
    probabilities: Dict[str, float] = Field(..., description="Probability for each outcome")
    home_team_averages: Dict[str, float] = Field(..., description="Home team's averaged statistics")
    away_team_averages: Dict[str, float] = Field(..., description="Away team's averaged statistics")

    class Config:
        schema_extra = {
            "example": {
                "prediction": "Home Win",
                "prediction_code": 1,
                "confidence": 65.5,
                "probabilities": {"Home Win": 0.655, "Draw": 0.235, "Away Win": 0.110},
                "home_team_averages": {
                    "avg_possession": 55.0,
                    "avg_shots_on_target": 5.0,
                    "avg_corners": 6.0,
                    "avg_fouls": 10.0,
                },
                "away_team_averages": {
                    "avg_possession": 45.0,
                    "avg_shots_on_target": 3.4,
                    "avg_corners": 4.4,
                    "avg_fouls": 13.0,
                },
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    model_loaded: bool


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: Optional[str] = None


# API Endpoints
@app.get("/", summary="API Root", description="Welcome endpoint with API information")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "⚽ Premier League Match Predictor API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {"predict": "/predict", "predict_weighted": "/predict/weighted"},
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API and model are working",
)
async def health_check():
    """Health check endpoint."""
    model_loaded = predict_from_recent_form is not None

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        version="1.0.0",
        model_loaded=model_loaded,
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Match Outcome",
    description="""
    Predict match outcome based on team statistics from their last games.
    
    The prediction uses equal weighting for all provided games.
    For custom weighting, use the `/predict/weighted` endpoint.
    """,
    responses={
        200: {"description": "Prediction successful"},
        400: {"description": "Invalid input data"},
        500: {"description": "Prediction failed", "model": ErrorResponse},
    },
)
async def predict_match(request: PredictionRequest):
    """
    Predict match outcome based on recent team performance.

    Args:
        request: Match prediction request with team statistics

    Returns:
        Prediction with probabilities and confidence

    Raises:
        HTTPException: If prediction fails
    """
    if predict_from_recent_form is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please ensure the model file exists.",
        )

    try:
        # Convert Pydantic models to dictionaries
        home_games = [game.dict() for game in request.home_team_last_5]
        away_games = [game.dict() for game in request.away_team_last_5]

        # Make prediction
        result = predict_from_recent_form(home_games, away_games)

        logger.info(f"Prediction made: {result['prediction']} ({result['confidence']:.1f}%)")

        return PredictionResponse(**result)

    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model file not found: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )


@app.post(
    "/predict/weighted",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict with Custom Weights",
    description="""
    Predict match outcome with custom weighting for each game.
    
    This allows you to give more importance to recent games or specific matches.
    If weights are not provided, recent games are weighted higher by default.
    """,
    responses={
        200: {"description": "Prediction successful"},
        400: {"description": "Invalid input data"},
        500: {"description": "Prediction failed", "model": ErrorResponse},
    },
)
async def predict_match_weighted(request: WeightedPredictionRequest):
    """
    Predict match outcome with custom weighting for each game.

    Args:
        request: Weighted prediction request with team statistics and optional weights

    Returns:
        Prediction with probabilities and confidence

    Raises:
        HTTPException: If prediction fails
    """
    if predict_with_custom_weights is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please ensure the model file exists.",
        )

    try:
        # Convert Pydantic models to dictionaries
        home_games = [game.dict() for game in request.home_team_last_5]
        away_games = [game.dict() for game in request.away_team_last_5]

        # Make weighted prediction
        result = predict_with_custom_weights(home_games, away_games, weights=request.weights)

        logger.info(
            f"Weighted prediction made: {result['prediction']} ({result['confidence']:.1f}%)"
        )

        # Convert response format
        response_data = {
            "prediction": result["prediction"],
            "prediction_code": result["prediction_code"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "home_team_averages": result["home_team_weighted_avg"],
            "away_team_averages": result["away_team_weighted_avg"],
        }

        return PredictionResponse(**response_data)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model file not found: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid input", "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)},
    )


# Startup event
@app.lifespan("startup")
async def startup_event():
    """Run on API startup."""
    logger.info("Starting Premier League Match Predictor API")
    logger.info("Docs available at: /docs")
    logger.info(f"Model loaded: {predict_from_recent_form is not None}")


# Shutdown event
@app.lifespan("shutdown")
async def shutdown_event():
    """Run on API shutdown."""
    logger.info("Shutting down Premier League Match Predictor API")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
