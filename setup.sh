#!/bin/bash

# setup script for pl match predictor

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "setting up pl match predictor..."
echo ""

# check python
echo "checking python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}python 3 not found. install it first.${NC}"
    exit 1
fi

PYTHON_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}found python $PYTHON_VER${NC}"

# venv
echo ""
if [ ! -d "venv" ]; then
    echo "creating venv..."
    python3 -m venv venv
    echo -e "${GREEN}done${NC}"
else
    echo -e "${YELLOW}venv exists already${NC}"
fi

# activate
echo ""
echo "activating venv..."
source venv/bin/activate
echo -e "${GREEN}done${NC}"

# upgrade pip
echo ""
echo "upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}done${NC}"

# install deps
echo ""
echo "installing dependencies (might take a bit)..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}installed${NC}"
else
    echo -e "${RED}install failed${NC}"
    exit 1
fi

# make dirs
echo ""
echo "creating dirs..."
mkdir -p data models logs
echo -e "${GREEN}done${NC}"

# check data
echo ""
if [ ! -f "data/premier_league_matches.csv" ]; then
    echo -e "${YELLOW}no training data found${NC}"
    
    read -p "generate sample data? [Y/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo "generating data..."
        python3 get_data.py
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}data generated${NC}"
        else
            echo -e "${RED}failed${NC}"
            echo "try manually: python get_data.py"
        fi
    else
        echo "skipped. run 'python get_data.py' later"
    fi
else
    echo -e "${GREEN}training data exists${NC}"
fi

# check model
echo ""
if [ ! -f "models/random_forest_model.pkl" ]; then
    echo -e "${YELLOW}no model found${NC}"
    
    if [ -f "data/premier_league_matches.csv" ]; then
        read -p "train model now? [Y/n]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            echo "training (takes ~30 sec)..."
            python3 model_trainer.py
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}model trained${NC}"
            else
                echo -e "${RED}training failed${NC}"
            fi
        else
            echo "skipped"
        fi
    else
        echo "need data first. run get_data.py"
    fi
else
    echo -e "${GREEN}model exists${NC}"
fi

# tests
echo ""
read -p "run tests? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "running tests..."
    pytest tests/ -v
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}tests passed${NC}"
    else
        echo -e "${YELLOW}some tests failed${NC}"
    fi
fi

# done
echo ""
echo "========================"
echo "    setup complete"
echo "========================"
echo ""
echo "next steps:"
echo ""
echo "1. activate venv:"
echo "   source venv/bin/activate"
echo ""
echo "2. run dashboard:"
echo "   streamlit run dashboard.py"
echo ""
echo "3. or api:"
echo "   uvicorn main:app --reload"
echo ""
echo "see README.md for more info"
echo ""