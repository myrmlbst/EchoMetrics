#!/bin/bash

# exit on error
set -e

# colors for output
GREEN='\033[0;32m'
NC='\033[0m' # no color

# check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# check if virtual environment exists, if not create one
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
    
    # activate virtual environment
    source venv/bin/activate
    
    # upgrade pip
    echo -e "${GREEN}Upgrading pip...${NC}"
    pip install --upgrade pip
    
    # install dependencies
    echo -e "${GREEN}Installing dependencies...${NC}"
    pip install -r requirements.txt
else
    # activate existing virtual environment
    source venv/bin/activate
fi

# create necessary directories if they don't exist
mkdir -p artifacts/models
mkdir -p artifacts/plots

# run the application
echo -e "${GREEN}Starting EchoMetrics...${NC}"
python main.py

echo -e "${GREEN}EchoMetrics has finished running.${NC}"
echo -e "You can access the web interface at ${GREEN}http://localhost:5000${NC}"
