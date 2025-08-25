#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Basic Tests
Simple tests to verify system components

Author: Hudhud Team
Date: 2024
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        # Test utility imports
        from hudhud.utils.config import Config
        print("✅ Config module imported successfully")
        
        from hudhud.utils.logger import setup_logger
        print("✅ Logger module imported successfully")
        
        from hudhud.utils.data_loader import DataLoader
        print("✅ DataLoader module imported successfully")
        
        from hudhud.utils.cache_manager import CacheManager
        print("✅ CacheManager module imported successfully")
        
        # Test component imports
        from hudhud.components.layout import create_layout
        print("✅ Layout module imported successfully")
        
        from hudhud.components.navigation import create_navigation
        print("✅ Navigation module imported successfully")
        
        from hudhud.components.filters import create_filters
        print("✅ Filters module imported successfully")
        
        from hudhud.components.callbacks import register_filter_callbacks
        print("✅ Callbacks module imported successfully")
        
        from hudhud.components.ui_components import create_metric_card
        print("✅ UI Components module imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("\n🧪 Testing configuration system...")
    
    try:
        from hudhud.utils.config import Config
        
        config = Config()
        print("✅ Config object created successfully")
        
        # Test default values
        assert config.database.host == "localhost"
        assert config.database.port == 5432
        print("✅ Default configuration values correct")
        
        print("🎉 Configuration system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        return False

def test_ui_components():
    """Test UI component creation"""
    print("\n🧪 Testing UI components...")
    
    try:
        from hudhud.components.ui_components import create_metric_card
        
        # Test metric card creation
        card = create_metric_card(
            title="Test Metric",
            value="100",
            subtitle="Test Subtitle",
            color="primary"
        )
        
        print("✅ Metric card created successfully")
        print(f"   Card type: {type(card)}")
        
        print("🎉 UI components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ UI Components Error: {e}")
        return False

def test_filters():
    """Test filter components"""
    print("\n🧪 Testing filter components...")
    
    try:
        from hudhud.components.filters import create_filters, create_quick_filters
        
        # Test filter creation
        filters = create_filters()
        print("✅ Main filters created successfully")
        
        quick_filters = create_quick_filters()
        print("✅ Quick filters created successfully")
        
        print("🎉 Filter components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Filter Components Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Hudhud KPI System - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_ui_components,
        test_filters
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
