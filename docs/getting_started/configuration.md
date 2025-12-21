# ⚙️ Configuration Guide

This guide explains how to configure the Premier League Match Predictor for different use cases.

## 📋 Table of Contents

- [Data Configuration](#data-configuration)
- [Model Configuration](#model-configuration)
- [Dashboard Configuration](#dashboard-configuration)
- [API Configuration](#api-configuration)
- [Docker Configuration](#docker-configuration)

## 🗃️ Data Configuration

### Using Sample Data

By default, `get_data.py` generates realistic sample data:

```python
# In get_data.py - Using default settings
fetcher = PremierLeagueDataFetcher(data_dir="data")
matches_df = fetcher.fetch_data(seasons=["2021-2022", "2022-2023", "2023-2024"])
```

### Using Real Data

To use real Premier League data from FBref:

1. **Install soccerdata**:
```bash
pip install soccerdata
```

2. **Run the fetcher**:
```bash
python get_data.py
```

The script will automatically try to fetch real data first, falling back to sample data if unavailable.

### Customize Data Generation

Edit `get_data.py` to customize:

```python
# Change data directory
fetcher = PremierLeagueDataFetcher(data_dir="custom_data")

# Change seasons
matches_df = fetcher.fetch_data(seasons=["2020-2021", "2021-2022"])

# Modify team list for sample data
teams = [
    "Arsenal", "Manchester City", "Liverpool",
    # Add or remove teams as needed
]
```

## 🤖 Model Configuration

### Basic Model Parameters

Edit `model_trainer.py` to adjust model parameters:

```python
trainer = PremierLeagueModelTrainer(
    n_estimators=150,      # Number of trees (default: 150)
    max_depth=12,          # Maximum tree depth (default: 12)
    random_state=42        # Random seed for reproducibility
)
```

### Advanced Model Configuration

For more control, modify the model initialization in `model_trainer.py`:

```python
self.model = RandomForestClassifier(
    n_estimators=self.n_estimators,
    max_depth=self.max_depth,
    min_samples_split=20,    # Minimum samples to split node
    min_samples_leaf=10,     # Minimum samples in leaf
    random_state=self.random_state,
    class_weight="balanced", # Handle class imbalance
    n_jobs=-1,              # Use all CPU cores
)
```

### Feature Engineering

To add or modify features, edit the `_create_single_match_features` method in `model_trainer.py`:

```python
def _create_single_match_features(self, idx, row):
    features = {}
    
    # Existing features
    features["possession_diff"] = row["home_possession"] - row["away_possession"]
    features["shots_diff"] = row["home_shots_on_target"] - row["away_shots_on_target"]
    
    # Add new features here
    features["possession_ratio"] = row["home_possession"] / (row["away_possession"] + 1)
    features["shots_efficiency"] = row["home_shots_on_target"] / (row["home_corners"] + 1)
    
    return features
```

### Model Persistence

Change where models are saved:

```python
# In model_trainer.py
trainer.save_model("path/to/custom/model.pkl")
```

## 🎨 Dashboard Configuration

### Port and Host

Run dashboard on different port or host:

```bash
# Different port
streamlit run dashboard.py --server.port 8502

# Different host
streamlit run dashboard.py --server.address 0.0.0.0

# Both
streamlit run dashboard.py --server.port 8502 --server.address 0.0.0.0
```

### Streamlit Configuration File

Create `.streamlit/config.toml` for persistent settings:

```toml
[server]
port = 8501
address = "localhost"
headless = false

[theme]
primaryColor = "#10b981"
backgroundColor = "#1e293b"
secondaryBackgroundColor = "#334155"
textColor = "#ffffff"

[browser]
gatherUsageStats = false
```

### Dashboard Customization

Edit `dashboard.py` to customize:

```python
# Page configuration
st.set_page_config(
    page_title="Custom Title",
    page_icon="⚽",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Your custom styles here */
    .stButton>button {
        background-color: #your-color;
    }
</style>
""", unsafe_allow_html=True)
```

### Default Input Values

Modify default game statistics in dashboard:

```python
# In create_game_inputs function
possession = st.number_input(
    "Possession %",
    value=60.0,  # Change default value
    step=0.1
)
```

## 🚀 API Configuration

### Server Settings

Edit `main.py` or use command line:

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### CORS Configuration

Edit CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Specific methods
    allow_headers=["*"],
)
```

### API Documentation

Customize API metadata in `main.py`:

```python
app = FastAPI(
    title="Your Custom Title",
    description="Your custom description",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)
```

### Rate Limiting

Add rate limiting (requires additional package):

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("10/minute")
async def predict_match(request: Request, prediction_request: PredictionRequest):
    # Your prediction logic
    pass
```

## 🐳 Docker Configuration

### Dockerfile Customization

Edit `Dockerfile` to customize:

```dockerfile
# Change Python version
FROM python:3.11-slim

# Add system dependencies
RUN apt-get update && apt-get install -y \
    your-package \
    && rm -rf /var/lib/apt/lists/*

# Change working directory
WORKDIR /app

# Expose different port
EXPOSE 8000
```

### Docker Compose Configuration

Edit `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"  # Change host port
    environment:
      - MODEL_PATH=/app/models/match_predictor.joblib
      - LOG_LEVEL=info  # Add environment variables
    volumes:
      - ./data:/app/data
      - ./models:/app/models
  
  dashboard:
    build: .
    command: streamlit run dashboard.py --server.address=0.0.0.0
    ports:
      - "8501:8501"
```

### Environment Variables

Create `.env` file:

```bash
# Model settings
MODEL_PATH=models/random_forest_model.pkl
N_ESTIMATORS=150
MAX_DEPTH=12

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# Dashboard settings
DASHBOARD_PORT=8501
```

Load in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

model_path = os.getenv("MODEL_PATH", "models/random_forest_model.pkl")
```

## 📝 Logging Configuration

### Python Logging

Add logging to your scripts:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.info("Training model...")
logger.error("An error occurred")
```

### Dashboard Logging

Streamlit has built-in logging:

```bash
# Run with debug logging
streamlit run dashboard.py --logger.level=debug
```

## 🔒 Security Configuration

### API Security

Add API key authentication:

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.post("/predict")
async def predict_match(
    request: PredictionRequest,
    api_key: str = Security(verify_api_key)
):
    # Your logic here
    pass
```

### HTTPS Configuration

For production, use HTTPS:

```bash
# With Let's Encrypt certificate
uvicorn main:app --host 0.0.0.0 --port 443 \
  --ssl-keyfile /path/to/key.pem \
  --ssl-certfile /path/to/cert.pem
```

## 🎯 Performance Tuning

### Model Performance

```python
# Use fewer features for faster predictions
features_subset = ["possession_diff", "shots_diff"]

# Reduce number of trees for faster training
trainer = PremierLeagueModelTrainer(n_estimators=50)

# Enable parallel processing
model = RandomForestClassifier(n_jobs=-1)  # Use all cores
```

### API Performance

```bash
# Run with multiple workers
uvicorn main:app --workers 4

# Use gunicorn for production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Caching

Add caching to expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_prediction(home_stats_tuple, away_stats_tuple):
    # Convert tuples back to lists
    home_stats = list(home_stats_tuple)
    away_stats = list(away_stats_tuple)
    
    # Your prediction logic
    return result
```

## 📊 Monitoring

### Application Monitoring

Add monitoring endpoints:

```python
from datetime import datetime

@app.get("/metrics")
async def get_metrics():
    return {
        "total_predictions": prediction_count,
        "uptime": datetime.now() - start_time,
        "model_accuracy": model_accuracy
    }
```

### Resource Monitoring

Use Docker stats:

```bash
docker stats pl-predictor-api
```

## 🔧 Troubleshooting

Common configuration issues:

1. **Port conflicts**: Change port in configuration
2. **Memory issues**: Reduce `n_estimators` or batch size
3. **Import errors**: Ensure virtual environment is activated
4. **Model not found**: Check `MODEL_PATH` configuration

For more help, see [README.md](README.md) or open an issue on GitHub.