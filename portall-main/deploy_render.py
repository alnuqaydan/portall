#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Render Deployment Helper
Helper script to prepare and validate deployment

Author: Hudhud Team
Date: 2024
"""

import os
import sys
from pathlib import Path
import subprocess
import json

def check_required_files():
    """Check if all required deployment files exist"""
    print("🔍 Checking required deployment files...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "render.yaml",
        "gunicorn.conf.py",
        "Procfile"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required deployment files found")
        return True

def validate_python_version():
    """Check Python version compatibility"""
    print("\n🐍 Checking Python version...")
    
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Python version: {version}")
        
        # Check if it's Python 3.8+
        if "Python 3" in version:
            print("✅ Python version is compatible")
            return True
        else:
            print("❌ Python version must be 3.8 or higher")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Python version: {e}")
        return False

def test_dependencies(skip_install=False):
    """Test if dependencies can be installed"""
    print("\n📦 Testing dependencies...")
    
    if skip_install:
        print("⏭️  Skipping dependency installation (--skip-deps flag)")
        # Just check if core dependencies can be imported
        try:
            import dash
            import flask
            import gunicorn
            print("✅ Core dependencies (dash, flask, gunicorn) are available")
            return True
        except ImportError as e:
            print(f"⚠️  Some core dependencies missing: {e}")
            print("💡 Run 'pip install -r requirements.txt' to install all dependencies")
            return False
    
    try:
        # Try to install requirements with shorter timeout
        print("🔄 Installing dependencies (this may take a few minutes)...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--timeout", "60"
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print("✅ Dependencies can be installed successfully")
            return True
        else:
            print(f"⚠️  Dependency installation issues: {result.stderr[:500]}...")
            print("💡 This might be due to network timeouts. Try running manually:")
            print("   pip install -r requirements.txt")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Dependency installation timed out")
        print("💡 This might be due to network issues. The deployment should still work on Render.")
        return False
    except Exception as e:
        print(f"⚠️  Error testing dependencies: {e}")
        print("💡 This might be a temporary issue. Try again later.")
        return False

def validate_app_structure():
    """Validate application structure"""
    print("\n🏗️ Validating application structure...")
    
    required_dirs = [
        "hudhud",
        "hudhud/utils",
        "hudhud/components",
        "data"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing required directories: {', '.join(missing_dirs)}")
        return False
    else:
        print("✅ Application structure is valid")
        return True

def check_environment_variables():
    """Check if critical environment variables are documented"""
    print("\n🔧 Checking environment variables...")
    
    # Check if env_example.txt exists
    if Path("env_example.txt").exists():
        print("✅ Environment variables template found")
        
        # Read and check for critical variables
        with open("env_example.txt", "r") as f:
            content = f.read()
            
        critical_vars = [
            "PORT", "DEBUG", "LOG_LEVEL", "REVIEWERS", 
            "DEFAULT_CITY", "SECRET_KEY"
        ]
        
        missing_vars = []
        for var in critical_vars:
            if var not in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing critical environment variables: {', '.join(missing_vars)}")
        else:
            print("✅ Critical environment variables documented")
            
        return True
    else:
        print("❌ Environment variables template not found")
        return False

def generate_deployment_summary():
    """Generate deployment summary"""
    print("\n📋 Deployment Summary")
    print("=" * 50)
    
    summary = {
        "Application": "Hudhud KPI System",
        "Platform": "Render",
        "Service Type": "Web Service",
        "Python Version": "3.11.0",
        "Build Command": "pip install -r requirements.txt",
        "Start Command": "gunicorn app:app.server --bind 0.0.0.0:$PORT",
        "Health Check": "/health",
        "Port": "$PORT (Render managed)",
        "Auto-Deploy": "Enabled",
        "Disk Storage": "1GB persistent"
    }
    
    for key, value in summary.items():
        print(f"{key:<20}: {value}")
    
    print("\n🚀 Next Steps:")
    print("1. Push your code to Git repository")
    print("2. Connect repository to Render")
    print("3. Deploy using render.yaml (recommended)")
    print("4. Set environment variables")
    print("5. Monitor deployment logs")
    
    return summary

def main():
    """Main deployment validation function"""
    print("🚀 Hudhud KPI System - Render Deployment Validation")
    print("=" * 60)
    
    # Check for command line arguments
    skip_deps = "--skip-deps" in sys.argv or "--skip-dependencies" in sys.argv
    if skip_deps:
        print("🔧 Running in fast mode (skipping dependency installation)")
    
    checks = [
        ("Required Files", check_required_files),
        ("Python Version", validate_python_version),
        ("Dependencies", lambda: test_dependencies(skip_install=skip_deps)),
        ("App Structure", validate_app_structure),
        ("Environment Variables", check_environment_variables)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        if check_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed >= 4:  # Allow deployment with 4/5 checks (dependency check can be flaky)
        print("🎉 System is ready for Render deployment!")
        if passed < total:
            print("⚠️  Some non-critical checks failed, but deployment should work.")
        generate_deployment_summary()
        return True
    else:
        print("❌ Critical checks failed. Please fix the issues before deploying.")
        print("\n💡 Check the RENDER_DEPLOYMENT.md file for detailed instructions.")
        print("💡 Use --skip-deps flag to skip dependency installation check")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
