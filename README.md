# ⚽ Premier League Match Predictor

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/yourusername/pl-match-predictor/workflows/CI/badge.svg)](https://github.com/yourusername/pl-match-predictor/actions)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://yourusername.github.io/pl-match-predictor)

Predict Premier League match outcomes using Machine Learning! This project uses a Random Forest classifier trained on 500+ real matches to predict Home Win, Draw, or Away Win based on team statistics.

![Demo](docs/images/demo.gif)

## Features

- **ML-Powered Predictions**: Random Forest with 70%+ accuracy
- **Real Data**: Trained on 500+ actual Premier League matches (2020-2024)
- **REST API**: FastAPI-powered endpoints with Swagger docs
- **Docker Support**: Containerized for easy deployment
- **Data Versioning**: DVC integration for reproducibility
- **Well Tested**: 80%+ code coverage with pytest
- **Documented**: Complete documentation with MkDocs
- **Type Safe**: Full type hints throughout

## Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API](#-api)
- [Model](#-model)
- [Development](#-development)
- [Docker](#-docker)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## Installation

### Quick Install

```bash
pip install pl-match-predictor
```

### From Source

```bash
# Clone repository
git clone https://github.com/yourusername/pl-match-predictor.git
cd pl-match-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with all dependencies
pip install -e ".[all]"
```

### Installation Options

```bash
# Minimal (core only)
pip install pl-match-predictor

# With API
pip install "pl-match-predictor[api]"

# With development tools
pip install "pl-match-predictor[dev]"

# Everything
pip install "pl-match-predictor[all]"
```

## ⚡ Quick Start

### 1. Fetch Training Data

```bash
python src/server/data/getdata/fetch_real_matches.py
```

This fetches 500+ real Premier League matches from 2020-2024.

### 2. Train Model

```bash
python src/server/model/modelbuild/predictor.py
```

### 3. Make Predictions

#### Python API

```python
from src.server.model.modelbuild.make_prediction import predict_from_recent_form

# Last 5 games for each team
home_games = [
    {'possession': 55.0, 'shots_on_target': 5, 'corners': 6, 'fouls': 10},
    {'possession': 52.0, 'shots_on_target': 4, 'corners': 5, 'fouls': 11},
    {'possession': 58.0, 'shots_on_target': 6, 'corners': 7, 'fouls': 9},
    {'possession': 50.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 12},
    {'possession': 60.0, 'shots_on_target': 7, 'corners': 8, 'fouls': 8},
]

away_games = [
    {'possession': 45.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 13},
    {'possession': 48.0, 'shots_on_target': 4, 'corners': 5, 'fouls': 12},
    {'possession': 42.0, 'shots_on_target': 2, 'corners': 3, 'fouls': 15},
    {'possession': 50.0, 'shots_on_target': 5, 'corners': 6, 'fouls': 11},
    {'possession': 40.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 14},
]

result = predict_from_recent_form(home_games, away_games)

print(f" Prediction: {result['prediction']}")
print(f" Confidence: {result['confidence']:.1f}%")
```

#### REST API

```bash
# Start API
uvicorn src.server.api.main:app --reload

# Make prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

Visit **http://localhost:8000/docs** for interactive API documentation.

## Usage

### Python Library

```python
from src.server.model import predict_from_recent_form, predict_with_custom_weights

# Simple prediction
result = predict_from_recent_form(home_games, away_games)

# Weighted prediction (recent games more important)
weights = [0.10, 0.15, 0.20, 0.25, 0.30]
result = predict_with_custom_weights(home_games, away_games, weights=weights)

# Access results
print(f"Prediction: {result['prediction']}")  # 'Home Win', 'Draw', or 'Away Win'
print(f"Confidence: {result['confidence']}")  # 0-100
print(f"Probabilities: {result['probabilities']}")  # Dict with all outcomes
```

### Command Line

```bash
# Fetch data
make fetch-data

# Train model
make train-model

# Run tests
make test

# Start API
make run-api
```

## API

### Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Make prediction
- `POST /predict/weighted` - Weighted prediction

### Example Request

```json
{
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
}
```

### Example Response

```json
{
  "prediction": "Home Win",
  "prediction_code": 1,
  "confidence": 65.5,
  "probabilities": {
    "Home Win": 0.655,
    "Draw": 0.235,
    "Away Win": 0.110
  },
  "home_team_averages": {
    "avg_possession": 55.0,
    "avg_shots_on_target": 5.0,
    "avg_corners": 6.0,
    "avg_fouls": 10.0
  },
  "away_team_averages": {
    "avg_possession": 45.0,
    "avg_shots_on_target": 3.4,
    "avg_corners": 4.4,
    "avg_fouls": 13.0
  }
}
```

## Model

### Architecture

- **Algorithm**: Random Forest Classifier
- **Trees**: 200 estimators
- **Features**: 8 (4 per team)
  - Possession (%)
  - Shots on Target
  - Corners
  - Fouls Committed
- **Classes**: 3 outcomes
  - Home Win (1)
  - Draw (0)
  - Away Win (-1)

### Performance

| Metric | Value |
|--------|-------|
| Accuracy | 70%+ |
| Training Data | 500+ matches |
| Data Period | 2020-2024 |
| Update Frequency | Weekly |

### Training

```bash
# Fetch fresh data
python src/server/data/getdata/fetch_real_matches.py

# Train new model
python src/server/model/modelbuild/predictor.py

# Evaluate performance
python src/server/model/modelbuild/model_evaluation.py
```

## Development

### Setup

```bash
# Clone and install
git clone https://github.com/yourusername/pl-match-predictor.git
cd pl-match-predictor
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install

# Run tests
make test
```

### Project Structure

```
pl-match-predictor/
├── src/
│   ├── server/
│   │   ├── data/          # Data fetching and processing
│   │   │   ├── getdata/   # Fetch from APIs
│   │   │   └── processdata/ # Feature engineering
│   │   ├── model/         # ML model
│   │   │   └── modelbuild/ # Training and prediction
│   │   └── api/           # REST API
│   ├── app/               # GUI application
│   └── client/            # CLI client
├── tests/                 # Test suite
├── docs/                  # Documentation
├── notebooks/             # Jupyter notebooks
├── .github/workflows/     # CI/CD
├── Dockerfile             # Container
├── Makefile              # Common commands
├── setup.py              # Package config
└── README.md             # This file
```

### Testing

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Quick tests
pytest tests/ -m "not slow"

# Specific test
pytest tests/test_api.py::test_predict_success
```

### Code Quality

```bash
# Format code
make format

# Lint
make lint

# Type check
make type-check

# All checks
make ci
```

## Docker

### Build & Run

```bash
# Build image
docker build -t pl-predictor .

# Run container
docker run -p 8000:8000 pl-predictor

# Using docker-compose
docker-compose up -d
```

### Services

- **API**: http://localhost:8000
- **Docs**: http://localhost:8001
- **Jupyter**: http://localhost:8888

## Documentation

Full documentation available at: **https://yourusername.github.io/pl-match-predictor**

### Local Docs

```bash
# Serve docs
mkdocs serve

# Build docs
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Data Sources

- **FBref** (https://fbref.com/) - Primary data source
- **WhoScored** (https://www.whoscored.com/) - Fallback source
- Via **soccerdata** library (https://github.com/probberechts/soccerdata)

## Roadmap

- [ ] Add more features (xG, team form, injuries)
- [ ] Deep learning models
- [ ] Real-time predictions
- [ ] Mobile app
- [ ] Multi-league support
- [ ] Advanced statistics
- [ ] Player-level analysis

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [soccerdata](https://github.com/probberechts/soccerdata) for data access
- [scikit-learn](https://scikit-learn.org/) for ML tools
- [FastAPI](https://fastapi.tiangolo.com/) for API framework
- Football analytics community for inspiration

## Contact

**Miguel Vila**

- GitHub: [@miguelvila02](https://github.com/miguelvila02)
- Email: luismiguelvila@gmail.com

