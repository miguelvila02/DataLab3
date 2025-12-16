"""
Tests for the FastAPI REST API.
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
from src.server.api.main import app

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# Create test client
client = TestClient(app)


class TestRootEndpoints:
    """Test root and info endpoints."""
    
    def test_root(self):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    def test_health(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "degraded"]
        assert "version" in data
        assert "model_loaded" in data


class TestPredictionEndpoint:
    """Test the main prediction endpoint."""
    
    @pytest.fixture
    def valid_request(self):
        """Valid prediction request."""
        return {
            "home_team_last_5": [
                {"possession": 55.0, "shots_on_target": 5, "corners": 6, "fouls": 10},
                {"possession": 52.0, "shots_on_target": 4, "corners": 5, "fouls": 11},
                {"possession": 58.0, "shots_on_target": 6, "corners": 7, "fouls": 9},
                {"possession": 50.0, "shots_on_target": 3, "corners": 4, "fouls": 12},
                {"possession": 60.0, "shots_on_target": 7, "corners": 8, "fouls": 8}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13},
                {"possession": 48.0, "shots_on_target": 4, "corners": 5, "fouls": 12},
                {"possession": 42.0, "shots_on_target": 2, "corners": 3, "fouls": 15},
                {"possession": 50.0, "shots_on_target": 5, "corners": 6, "fouls": 11},
                {"possession": 40.0, "shots_on_target": 3, "corners": 4, "fouls": 14}
            ]
        }
    
    def test_predict_success(self, valid_request):
        """Test successful prediction."""
        response = client.post("/predict", json=valid_request)
        
        # May be 200 (success) or 503 (model not loaded)
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert data["prediction"] in ["Home Win", "Draw", "Away Win"]
            assert "confidence" in data
            assert 0 <= data["confidence"] <= 100
            assert "probabilities" in data
            assert "home_team_averages" in data
            assert "away_team_averages" in data
    
    def test_predict_invalid_possession(self, valid_request):
        """Test with invalid possession value."""
        invalid_request = valid_request.copy()
        invalid_request["home_team_last_5"][0]["possession"] = 150.0
        
        response = client.post("/predict", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_predict_negative_stats(self, valid_request):
        """Test with negative stat values."""
        invalid_request = valid_request.copy()
        invalid_request["home_team_last_5"][0]["shots_on_target"] = -5
        
        response = client.post("/predict", json=invalid_request)
        assert response.status_code == 422
    
    def test_predict_missing_games(self):
        """Test with missing games data."""
        invalid_request = {
            "home_team_last_5": [],
            "away_team_last_5": []
        }
        
        response = client.post("/predict", json=invalid_request)
        assert response.status_code == 422
    
    def test_predict_single_game(self):
        """Test with single game (minimum)."""
        request = {
            "home_team_last_5": [
                {"possession": 55.0, "shots_on_target": 5, "corners": 6, "fouls": 10}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13}
            ]
        }
        
        response = client.post("/predict", json=request)
        assert response.status_code in [200, 503]


class TestWeightedPredictionEndpoint:
    """Test weighted prediction endpoint."""
    
    @pytest.fixture
    def valid_weighted_request(self):
        """Valid weighted prediction request."""
        return {
            "home_team_last_5": [
                {"possession": 55.0, "shots_on_target": 5, "corners": 6, "fouls": 10},
                {"possession": 52.0, "shots_on_target": 4, "corners": 5, "fouls": 11},
                {"possession": 58.0, "shots_on_target": 6, "corners": 7, "fouls": 9},
                {"possession": 50.0, "shots_on_target": 3, "corners": 4, "fouls": 12},
                {"possession": 60.0, "shots_on_target": 7, "corners": 8, "fouls": 8}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13},
                {"possession": 48.0, "shots_on_target": 4, "corners": 5, "fouls": 12},
                {"possession": 42.0, "shots_on_target": 2, "corners": 3, "fouls": 15},
                {"possession": 50.0, "shots_on_target": 5, "corners": 6, "fouls": 11},
                {"possession": 40.0, "shots_on_target": 3, "corners": 4, "fouls": 14}
            ],
            "weights": [0.1, 0.15, 0.2, 0.25, 0.3]
        }
    
    def test_weighted_predict_success(self, valid_weighted_request):
        """Test successful weighted prediction."""
        response = client.post("/predict/weighted", json=valid_weighted_request)
        
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "confidence" in data
    
    def test_weighted_predict_without_weights(self):
        """Test weighted endpoint without explicit weights."""
        request = {
            "home_team_last_5": [
                {"possession": 55.0, "shots_on_target": 5, "corners": 6, "fouls": 10},
                {"possession": 52.0, "shots_on_target": 4, "corners": 5, "fouls": 11},
                {"possession": 58.0, "shots_on_target": 6, "corners": 7, "fouls": 9},
                {"possession": 50.0, "shots_on_target": 3, "corners": 4, "fouls": 12},
                {"possession": 60.0, "shots_on_target": 7, "corners": 8, "fouls": 8}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13},
                {"possession": 48.0, "shots_on_target": 4, "corners": 5, "fouls": 12},
                {"possession": 42.0, "shots_on_target": 2, "corners": 3, "fouls": 15},
                {"possession": 50.0, "shots_on_target": 5, "corners": 6, "fouls": 11},
                {"possession": 40.0, "shots_on_target": 3, "corners": 4, "fouls": 14}
            ]
        }
        
        response = client.post("/predict/weighted", json=request)
        assert response.status_code in [200, 503]


class TestInputValidation:
    """Test input validation."""
    
    def test_possession_out_of_range_high(self):
        """Test possession > 100."""
        request = {
            "home_team_last_5": [
                {"possession": 150.0, "shots_on_target": 5, "corners": 6, "fouls": 10}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13}
            ]
        }
        
        response = client.post("/predict", json=request)
        assert response.status_code == 422
    
    def test_possession_negative(self):
        """Test negative possession."""
        request = {
            "home_team_last_5": [
                {"possession": -10.0, "shots_on_target": 5, "corners": 6, "fouls": 10}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13}
            ]
        }
        
        response = client.post("/predict", json=request)
        assert response.status_code == 422
    
    def test_negative_shots(self):
        """Test negative shots on target."""
        request = {
            "home_team_last_5": [
                {"possession": 55.0, "shots_on_target": -5, "corners": 6, "fouls": 10}
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13}
            ]
        }
        
        response = client.post("/predict", json=request)
        assert response.status_code == 422
    
    def test_too_many_games(self):
        """Test with more than 10 games."""
        request = {
            "home_team_last_5": [
                {"possession": 55.0, "shots_on_target": 5, "corners": 6, "fouls": 10}
                for _ in range(11)
            ],
            "away_team_last_5": [
                {"possession": 45.0, "shots_on_target": 3, "corners": 4, "fouls": 13}
                for _ in range(11)
            ]
        }
        
        response = client.post("/predict", json=request)
        assert response.status_code == 422


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers(self):
        """Test that CORS headers are present."""
        response = client.options("/predict")
        
        # CORS headers should be present
        assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]


class TestDocumentation:
    """Test API documentation endpoints."""
    
    def test_openapi_schema(self):
        """Test OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_swagger_docs(self):
        """Test Swagger UI is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_docs(self):
        """Test ReDoc is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
