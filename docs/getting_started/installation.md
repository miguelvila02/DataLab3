# Installation Guide

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git
- 2GB+ free disk space (for data and models)

## Quick Install

### From PyPI (when published)

```bash
pip install pl-match-predictor
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/pl-match-predictor.git
cd pl-match-predictor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with all dependencies
pip install -e ".[all]"
```

## Installation Options

### Minimal Installation

Only core prediction functionality:

```bash
pip install pl-match-predictor
```

### With API Support

Include FastAPI for REST API:

```bash
pip install "pl-match-predictor[api]"
```

### With Data Versioning

Include DVC for data/model versioning:

```bash
pip install "pl-match-predictor[dvc]"
```

### With Visualization

Include matplotlib and seaborn:

```bash
pip install "pl-match-predictor[viz]"
```

### With GUI

Include PyQt5 for desktop application:

```bash
pip install "pl-match-predictor[gui]"
```

### Development Installation

All dependencies including testing and docs:

```bash
pip install -e ".[all]"
```

## Verify Installation

```bash
# Check package is installed
python -c "import src.server.model; print('✓ Package installed')"

# Run tests
pytest tests/

# Start API (if installed with [api])
uvicorn src.server.api.main:app --reload
```

## Docker Installation

### Pull from GitHub Container Registry

```bash
docker pull ghcr.io/yourusername/pl-match-predictor:latest
```

### Build Locally

```bash
# Build image
docker build -t pl-predictor .

# Run container
docker run -p 8000:8000 pl-predictor

# Access API at http://localhost:8000/docs
```

## System-Specific Instructions

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv git

# Install package
pip3 install pl-match-predictor
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install package
pip3 install pl-match-predictor
```

### Windows

```bash
# Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH"

# Open Command Prompt or PowerShell
pip install pl-match-predictor
```

## Troubleshooting

### ImportError: No module named 'src'

Make sure you've installed the package:

```bash
pip install -e .
```

### Model file not found

Download or train the model:

```bash
# Train new model
python src/server/model/modelbuild/predictor.py

# Or download pre-trained (if available)
dvc pull
```

### API won't start

Check if all API dependencies are installed:

```bash
pip install "pl-match-predictor[api]"
```

### Tests failing

Ensure dev dependencies are installed:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Updating

### Update from PyPI

```bash
pip install --upgrade pl-match-predictor
```

### Update from Source

```bash
cd pl-match-predictor
git pull
pip install -e ".[all]"
```

## Uninstalling

```bash
pip uninstall pl-match-predictor
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration](configuration.md)
- [API Usage](../guide/api-usage.md)