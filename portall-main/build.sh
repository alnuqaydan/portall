#!/bin/bash
set -e

echo "🚀 Starting Hudhud KPI System build..."

# Ensure Python 3.11 is used
echo "🐍 Setting Python version to 3.11.0..."
python --version

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify key packages
echo "✅ Verifying key packages..."
python -c "import dash, pandas, numpy; print(f'Dash: {dash.__version__}, Pandas: {pandas.__version__}, NumPy: {numpy.__version__}')"

echo "🎉 Build completed successfully!"
