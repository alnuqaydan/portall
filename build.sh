#!/bin/bash
set -e

echo "🚀 Starting Hudhud KPI System build..."

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
python -m venv venv
source venv/bin/activate

echo "🐍 Activated virtual environment, Python version:"
python --version

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify key packages
echo "✅ Verifying key packages..."
python -c "import dash, pandas, numpy; print(f'Dash: {dash.__version__}, Pandas: {pandas.__version__}, NumPy: {numpy.__version__}')"

echo "🎉 Build completed successfully!"
