#!/bin/bash

# Jan-Gana-Drishti Dashboard Launcher
# Quick start script for the UIDAI Analytics Dashboard

echo "======================================================================"
echo "🇮🇳 Jan-Gana-Drishti | Predictive Governance Dashboard"
echo "Government of India - UIDAI Hackathon 2026"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null
then
    echo "⚠️  Dependencies not found. Installing from requirements.txt..."
    pip install -r requirements.txt
    echo ""
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "❌ Error: 'data' directory not found!"
    echo "Please ensure the following structure exists:"
    echo "  data/"
    echo "  ├── api_data_aadhar_biometric/"
    echo "  ├── api_data_aadhar_demographic/"
    echo "  └── api_data_aadhar_enrolment/"
    exit 1
fi

echo "✅ Data directory found"
echo ""

# Launch Streamlit
echo "🚀 Launching Jan-Gana-Drishti Dashboard..."
echo "📊 Dashboard will open in your browser at: http://localhost:8501"
echo ""
echo "⏳ Initial load may take 1-2 minutes for data processing..."
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================================================"
echo ""

streamlit run app.py
