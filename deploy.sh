#!/bin/bash

# AI Contract Leakage Detection - Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting deployment of AI Contract Leakage Detection System..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists pip3; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads/{azure-nadcomms,nadcomms-customerA,nadcomms-customerB,nadcomms-customerC}
mkdir -p models analysis_results

# Set proper permissions
echo "🔒 Setting permissions..."
chmod -R 755 uploads/ models/ analysis_results/

# Generate sample contracts (optional)
read -p "🎯 Generate sample contracts for testing? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📄 Generating sample contracts..."
    python sample_contracts.py
fi

# Check if Gunicorn should be used for production
read -p "🏭 Deploy for production with Gunicorn? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏭 Installing Gunicorn..."
    pip install gunicorn
    
    echo "🚀 Starting application with Gunicorn..."
    echo "📍 Application will be available at http://localhost:5000"
    echo "🛑 Press Ctrl+C to stop the server"
    
    # Start with Gunicorn
    gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
else
    echo "🧪 Starting development server..."
    echo "📍 Application will be available at http://localhost:5000"
    echo "🛑 Press Ctrl+C to stop the server"
    
    # Start development server
    python app.py
fi
