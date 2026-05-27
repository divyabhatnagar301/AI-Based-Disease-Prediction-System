#!/bin/bash

echo "============================================================"
echo "MediLedger API - Starting Server"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

# Check if virtual environment exists, if not create one
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Start the API server
echo ""
echo "============================================================"
echo "Starting API Server on http://localhost:3000"
echo "============================================================"
echo ""
python app.py
