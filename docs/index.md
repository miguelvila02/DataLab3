# Premier League Match Predictor

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

Predicts Premier League match outcomes using Machine Learning based on team statistics from their last 5 games.

## 🎯 Overview

This project uses a Random Forest classifier to predict match outcomes (Home Win, Draw, Away Win) based on four key features:

- **Possession** (%)
- **Shots on Target**
- **Corners**
- **Fouls Committed**

The model is trained on **500+ real Premier League matches** from seasons 2020-2024.

## Features

- **ML Prediction**: Random Forest classifier with 70%+ accuracy
- **Real Data**: Trained on actual Premier League match statistics
- **Data Versioning**: DVC integration for data and model tracking
- **REST API**: FastAPI-powered endpoints for easy integration
- **Docker Support**: Containerized for easy deployment
- **Well Tested**: 80%+ code coverage with pytest
- **Documented**: Full API documentation with MkDocs
- **Type Safe**: Complete type hints throughout codebase

## Quick Start

### Installation

```bash
pip install pl-match-predictor
```

### Basic Usage

```python
from pl_predictor import predict_from_recent_form

# Last 5 games for home team
home_team_games = [
    {'possession': 55.0, 'shots_on_target': 5, 'corners': 6, 'fouls': 10},
    {'possession': 52.0, 'shots_on_target': 4, 'corners': 5, 'fouls': 11},
    {'possession': 58.0, 'shots_on_target': 6, 'corners': 7, 'fouls': 9},
    {'possession': 50.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 12},
    {'possession': 60.0, 'shots_on_target': 7, 'corners': 8, 'fouls': 8},
]

# Last 5 games for away team
away_team_games = [
    {'possession': 45.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 13},
    {'possession': 48.0, 'shots_on_target': 4, 'corners': 5, 'fouls': 12},
    {'possession': 42.0, 'shots_on_target': 2, 'corners': 3, 'fouls': 15},
    {'possession': 50.0, 'shots_on_target': 5, 'corners': 6, 'fouls': 11},
    {'possession': 40.0, 'shots_on_target': 3, 'corners': 4, 'fouls': 14},
]

# Make prediction
result = predict_from_recent_form(home_team_games, away_team_games)

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.1f}%")
print(f"\nWin Probabilities:")
for outcome, prob in result['probabilities'].items():
    print(f"   {outcome}: {prob*100:.1f}%")
```

### Using the REST API

Start the API server:

```bash
uvicorn pl_predictor.api.main:app --reload
```

Make predictions via HTTP:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "home_team_last_5": [
      {"possession": 55, "shots_on_target": 5, "corners": 6, "fouls": 10},
      ...
    ],
    "away_team_last_5": [
      {"possession": 45, "shots_on_target": 3, "corners": 4, "fouls": 13},
      ...
    ]
  }'
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### Using Docker

```bash
# Build the image
docker build -t pl-predictor .

# Run the API
docker run -p 8000:8000 pl-predictor

# Access at http://localhost:8000
```

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 70%+ |
| Training Data | 500+ matches |
| Features | 8 (4 per team) |
| Model Type | Random Forest (200 trees) |
| Data Source | FBref / WhoScored |

## Project Structure

```
pl-match-predictor/
├── src/
│   ├── server/
│   │   ├── data/          # Data fetching and processing
│   │   ├── model/         # ML model code
│   │   └── api/           # REST API
│   ├── app/               # GUI application
│   └── client/            # CLI client
├── tests/                 # Pytest test suite
├── docs/                  # MkDocs documentation
├── notebooks/             # Jupyter notebooks
├── .github/workflows/     # CI/CD pipelines
├── Dockerfile             # Container definition
└── setup.py               # Package configuration
```

## Data Pipeline

1. **Fetch**: Collect real match data from Premier League (2020-2024)
2. **Process**: Extract relevant features and clean data
3. **Version**: Track with DVC and S3
4. **Train**: Build Random Forest classifier
5. **Evaluate**: Test on hold-out dataset
6. **Deploy**: Serve via REST API or use directly

## Documentation

Full documentation is available at: [https://yourusername.github.io/pl-match-predictor](https://yourusername.github.io/pl-match-predictor)

- [Installation Guide](getting-started/installation.md)
- [API Reference](api/data.md)
- [User Guide](guide/predictions.md)
- [Development Guide](development/contributing.md)

## Testing

Run the test suite:

```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report:

```bash
open htmlcov/index.html
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](development/contributing.md).

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](about/license.md) file for details.

## Acknowledgments

- Data sourced from [soccerdata](https://github.com/probberechts/soccerdata)
- Inspired by the football analytics community
- Built with scikit-learn, FastAPI, and modern Python tools

## Creators

**Miguel Vila**

- GitHub: [@miguelvila02](https://github.com/miguelvila02)
- Email: luismiguelvila@gmail.com

---
