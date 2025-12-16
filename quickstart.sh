#!/bin/bash

# Premier League Match Predictor - Quick Start Script
# This script sets up the project and runs initial data collection

set -e  # Exit on error

echo "Premier League Match Predictor - Quick Start"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install package in editable mode
echo ""
echo "Installing package and dependencies..."
pip install -e ".[all]" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Package installed successfully"
else
    print_error "Failed to install package"
    exit 1
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p src/server/data
mkdir -p src/server/model
mkdir -p data
mkdir -p models
mkdir -p logs
print_success "Directories created"

# Check if data exists
echo ""
echo "Checking for training data..."
if [ ! -f "src/server/data/real_training_data.csv" ]; then
    print_warning "Training data not found"
    
    read -p "Would you like to fetch training data now? (This may take 5-10 minutes) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Fetching training data from Premier League matches..."
        python src/server/data/getdata/fetch_real_matches.py
        
        if [ $? -eq 0 ]; then
            print_success "Training data fetched successfully"
        else
            print_error "Failed to fetch training data"
            print_warning "You can try again later by running:"
            echo "  python src/server/data/getdata/fetch_real_matches.py"
        fi
    else
        print_warning "Skipping data fetch. You'll need to do this before training."
    fi
else
    print_success "Training data already exists"
fi

# Check if model exists
echo ""
echo "Checking for trained model..."
if [ ! -f "src/server/model/match_predictor.joblib" ]; then
    print_warning "Trained model not found"
    
    if [ -f "src/server/data/real_training_data.csv" ]; then
        read -p "Would you like to train the model now? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo ""
            echo "Training model..."
            python src/server/model/modelbuild/predictor.py
            
            if [ $? -eq 0 ]; then
                print_success "Model trained successfully"
            else
                print_error "Failed to train model"
            fi
        else
            print_warning "Skipping model training"
        fi
    else
        print_warning "Cannot train model without data. Fetch data first."
    fi
else
    print_success "Trained model already exists"
fi

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v --cov=src --cov-report=term-missing

if [ $? -eq 0 ]; then
    print_success "All tests passed!"
else
    print_warning "Some tests failed. Check the output above."
fi

# Summary
echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the API server:"
echo "   uvicorn src.server.api.main:app --reload"
echo "   Then visit: http://localhost:8000/docs"
echo ""
echo "3. Make a prediction:"
echo "   python src/server/model/modelbuild/make_prediction.py"
echo ""
echo "4. Run the GUI (optional):"
echo "   python src/app/app.py"
echo ""
echo "5. Build Docker image:"
echo "   docker build -t pl-predictor ."
echo ""
echo "For more information, see the documentation:"
echo "   mkdocs serve"
echo "   Then visit: http://localhost:8000"
echo ""
print_success "Enjoy predicting Premier League matches!"
