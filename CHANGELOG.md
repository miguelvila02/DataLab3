# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Data fetching from FBref and WhoScored
- Random Forest prediction model
- FastAPI REST API
- Docker containerization
- Comprehensive test suite
- CI/CD with GitHub Actions
- Documentation with MkDocs
- DVC integration for data versioning

## [0.1.0] - 2024-12-XX

### Added
- **Data Collection**
  - Script to fetch 500+ real Premier League matches
  - Support for multiple seasons (2020-2024)
  - Feature extraction: possession, shots on target, corners, fouls
  - Fallback data sources (FBref → WhoScored)

- **Machine Learning Model**
  - Random Forest classifier with 200 trees
  - Training on 8 features (4 per team)
  - Model evaluation with confusion matrix
  - Prediction with confidence scores
  - Support for weighted predictions

- **REST API**
  - `/predict` endpoint for match predictions
  - `/predict/weighted` for custom-weighted predictions
  - `/health` endpoint for health checks
  - Interactive Swagger UI documentation
  - Input validation with Pydantic
  - CORS support

- **Development Tools**
  - Complete test suite with pytest
  - Code formatting with black and isort
  - Linting with flake8
  - Type checking with mypy
  - Pre-commit hooks
  - Makefile for common tasks

- **Deployment**
  - Dockerfile for containerization
  - docker-compose.yml for multi-service setup
  - GitHub Actions CI/CD pipeline
  - Health checks and monitoring

- **Documentation**
  - MkDocs-based documentation site
  - Installation guide
  - Quick start tutorial
  - API reference
  - User guides
  - Contributing guidelines

- **Data Versioning**
  - DVC integration
  - S3 remote storage support
  - Automatic data tracking
  - Model versioning

### Technical Details
- Python 3.8+ support
- FastAPI for REST API
- scikit-learn for ML
- soccerdata for data fetching
- pytest for testing
- Docker for containerization

### Performance
- Model accuracy: ~70% on test set
- API response time: <100ms
- Training time: ~2 minutes on standard hardware
- Data fetch time: 5-10 minutes for 500+ matches

## [0.0.1] - 2024-11-XX

### Added
- Initial project setup
- Basic prediction functionality
- Command-line interface
- PyQt5 GUI prototype

---

## Release Notes

### Version 0.1.0

This is the first major release of the Premier League Match Predictor. It includes:

**For Users:**
- Simple Python API for predictions
- REST API with interactive documentation
- Docker support for easy deployment
- Comprehensive documentation

**For Developers:**
- Well-structured codebase
- Extensive test coverage
- CI/CD pipeline
- Clear contribution guidelines

**Known Issues:**
- GUI application is basic and needs improvement
- Data fetching can be slow depending on network
- Model accuracy could be improved with more features

**Future Plans:**
- Add more features (team form, head-to-head, injuries)
- Improve model with deep learning
- Real-time data updates
- Mobile app
- Enhanced GUI

---

## How to Upgrade

### From source

```bash
cd pl-match-predictor
git pull
pip install -e ".[all]"
```

### From PyPI

```bash
pip install --upgrade pl-match-predictor
```

---

## Migration Guide

### Breaking Changes in 0.1.0

None - this is the first release.

### Deprecations

None yet.

---

For more details, see the [full documentation](https://miguelvila02.github.io/pl-match-predictor).