#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Startup Script
Simple script to run the application

Author: Hudhud Team
Date: 2024
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app import HudhudApp
    
    def main():
        """Main startup function"""
        print("🚀 Starting Hudhud KPI System...")
        print("📊 Field Survey Dashboard")
        print("=" * 50)
        
        # Create and run application
        app = HudhudApp()
        
        print("✅ Application initialized successfully")
        print("🌐 Starting web server...")
        print("📱 Open your browser and navigate to: http://localhost:8050")
        print("⏹️  Press Ctrl+C to stop the application")
        print("=" * 50)
        
        # Run the application
        app.run(debug=True, port=8050)
        
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error starting application: {e}")
    print("💡 Check the logs for more details")
    sys.exit(1)
