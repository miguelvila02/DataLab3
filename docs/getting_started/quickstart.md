# Quick Start Guide

Get up and running with Premier League Match Predictor in 5 minutes!

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## 1. Installation

```bash
# Clone repository
git clone https://github.com/miguelvila02/pl-match-predictor.git
cd pl-match-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e ".[all]"
```

Or use the quick start script:

```bash
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh
```

## 2. Fetch Training Data

Collect 500+ real Premier League matches:

```bash
python src/server/data/getdata/fetch_real_matches.py
```

This will:
- Fetch matches from seasons 2020-2024
- Extract possession, shots, corners, and fouls
- Save to `src/server/data/real_training_data.csv`

**Expected time:** 5-10 minutes

## 3. Train the Model

```bash
python src/server/model/modelbuild/predictor.py
```

This will:
- Load training data
- Train Random Forest classifier
- Save model to `src/server/model/match_predictor.joblib`
- Show accuracy metrics

**Expected time:** 1-2 minutes

## 4. Make Your First Prediction

### Python API

```python
from src.server.model.modelbuild.make_prediction import predict_from_recent_form

# Home team's last 5 games
home_games = [
    {'possession': 55.0, 'shots_on_target': 5, 'corners': 6, 'fouls': 10},
    {'possession': 52.0, 'shots_on_target': 4, 'corners': 5, 'fouls': 11},
    {'possession': 58.0, 'shots_on_target': 6, 'corners': 7, 'fouls': 9},
    {'possession': 50.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 12},
    {'possession': 60.0, 'shots_on_target': 7, 'corners': 8, 'fouls': 8},
]

# Away team's last 5 games
away_games = [
    {'possession': 45.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 13},
    {'possession': 48.0, 'shots_on_target': 4, 'corners': 5, 'fouls': 12},
    {'possession': 42.0, 'shots_on_target': 2, 'corners': 3, 'fouls': 15},
    {'possession': 50.0, 'shots_on_target': 5, 'corners': 6, 'fouls': 11},
    {'possession': 40.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 14},
]

# Make prediction
result = predict_from_recent_form(home_games, away_games)

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.1f}%")
print(f"\nProbabilities:")
for outcome, prob in result['probabilities'].items():
    print(f"   {outcome}: {prob*100:.1f}%")
```

### REST API

Start the API server:

```bash
uvicorn src.server.api.main:app --reload
```

Visit the interactive docs: **http://localhost:8000/docs**

Make a request:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "home_team_last_5": [
      {"possession": 55, "shots_on_target": 5, "corners": 6, "fouls": 10},
      {"possession": 52, "shots_on_target": 4, "corners": 5, "fouls": 11},
      {"possession": 58, "shots_on_target": 6, "corners": 7, "fouls": 9},
      {"possession": 50, "shots_on_target": 3, "corners": 4, "fouls": 12},
      {"possession": 60, "shots_on_target": 7, "corners": 8, "fouls": 8}
    ],
    "away_team_last_5": [
      {"possession": 45, "shots_on_target": 3, "corners": 4, "fouls": 13},
      {"possession": 48, "shots_on_target": 4, "corners": 5, "fouls": 12},
      {"possession": 42, "shots_on_target": 2, "corners": 3, "fouls": 15},
      {"possession": 50, "shots_on_target": 5, "corners": 6, "fouls": 11},
      {"possession": 40, "shots_on_target": 3, "corners": 4, "fouls": 14}
    ]
  }'
```

## 5. Run Tests

Verify everything works:

```bash
pytest tests/ -v --cov=src
```

Expected output:
```
tests/test_api.py ✓✓✓✓✓
tests/test_predictor.py ✓✓✓✓✓

Coverage: 85%
```

## 6. Docker (Optional)

Build and run with Docker:

```bash
# Build image
docker build -t pl-predictor .

# Run container
docker run -p 8000:8000 pl-predictor

# Access API
open http://localhost:8000/docs
```

## Common Use Cases

### Predict Multiple Matches

```python
matches = [
    {
        'home': 'Manchester City',
        'away': 'Liverpool',
        'home_games': [...],
        'away_games': [...]
    },
    # ... more matches
]

for match in matches:
    result = predict_from_recent_form(
        match['home_games'],
        match['away_games']
    )
    print(f"{match['home']} vs {match['away']}: {result['prediction']}")
```

### Weighted Prediction

Give more importance to recent games:

```python
from src.server.model.modelbuild.make_prediction import predict_with_custom_weights

# More weight to recent games
weights = [0.10, 0.15, 0.20, 0.25, 0.30]

result = predict_with_custom_weights(
    home_games,
    away_games,
    weights=weights
)
```

### Batch Predictions via API

```python
import requests

url = "http://localhost:8000/predict"
matches = [...]  # List of match data

for match in matches:
    response = requests.post(url, json=match)
    prediction = response.json()
    print(f"Prediction: {prediction['prediction']}")
```

## Next Steps

- **[API Documentation](../guide/api-usage.md)** - Detailed API guide
- **[Data Fetching](../guide/data-fetching.md)** - How to collect match data
- **[Model Training](../api/model.md)** - Customize the model
- **[Docker Guide](../guide/docker.md)** - Deploy with Docker

## Troubleshooting

### Model not found

```bash
# Train the model first
python src/server/model/modelbuild/predictor.py
```

### Import errors

```bash
# Make sure package is installed
pip install -e .
```

### API won't start

```bash
# Install API dependencies
pip install ".[api]"
```

### Data fetch fails

```bash
# Check internet connection
# Try alternative data source in fetch_real_matches.py
```

## Getting Help

- [Full Documentation](https://miguelvila02.github.io/pl-match-predictor)
- [Report Issues](https://github.com/miguelvila02/pl-match-predictor/issues)
- [Discussions](https://github.com/miguelvila02/pl-match-predictor/discussions)

---

**Ready to predict some matches?**