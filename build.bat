@echo off
REM Render Build Script for Hudhud KPI System (Windows Version)
REM Optimized for Render's deployment environment

echo 🚀 Starting Render build process...

REM Update pip to latest version
echo 📦 Updating pip...
python -m pip install --upgrade pip

REM Install dependencies with optimizations
echo 📚 Installing Python dependencies...
pip install --no-cache-dir -r requirements.txt

REM Create necessary directories
echo 📁 Setting up directories...
if not exist logs mkdir logs
if not exist cache mkdir cache

REM Set environment variables for Render
set PYTHONPATH=%PYTHONPATH%;%CD%
set PYTHONUNBUFFERED=1

REM Verify installation
echo ✅ Verifying installation...
python -c "import dash, flask, gunicorn; print('Core dependencies installed successfully')"

echo 🎉 Build completed successfully!
pause
