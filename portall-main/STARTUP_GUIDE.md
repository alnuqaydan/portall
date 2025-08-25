# 🚀 Hudhud KPI System - Startup Guide

This guide will help you get the Hudhud KPI System up and running quickly.

## 📋 Prerequisites

- **Python 3.8 or higher** installed on your system
- **pip** package manager
- **Git** (for cloning the repository)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Navigate to the portal directory
cd field_survey_system/portal

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
copy env_example.txt .env

# Edit .env file with your settings
# Use any text editor to modify the values
```

### Step 3: Test the System

```bash
# Run basic tests to verify everything works
python test_basic.py
```

### Step 4: Start the Application

```bash
# Option 1: Use the main app
python app.py

# Option 2: Use the startup script
python run.py
```

### Step 5: Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:8050
```

## 🔧 Configuration

### Essential Settings

The following settings are required for basic operation:

```bash
# Database (SQLite is used by default)
DB_HOST=localhost
DB_NAME=field_survey_production

# Application
API_PORT=8050
LOG_LEVEL=INFO

# Reviewers (comma-separated list)
REVIEWERS=malngedan,aalbwardi,fahad,naif
```

### Optional Settings

```bash
# Cache settings
CACHE_ENABLED=true
CACHE_TTL=3600

# Export settings
EXPORT_FORMATS=csv,parquet,xlsx
MAX_EXPORT_SIZE=10000
```

## 📁 Directory Structure

```
portal/
├── app.py                 # Main application
├── run.py                 # Startup script
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── env_example.txt       # Environment configuration example
├── test_basic.py         # Basic system tests
├── hudhud/               # Core system modules
│   ├── utils/            # Utility functions
│   └── components/       # UI components
└── data/                 # Data directories
    ├── input/            # Raw data files
    ├── cache/            # Processed data cache
    ├── output/           # Generated reports
    ├── exports/          # User exports
    └── logs/             # Application logs
```

## 🧪 Testing

### Run Basic Tests

```bash
python test_basic.py
```

This will test:
- ✅ Module imports
- ✅ Configuration system
- ✅ UI components
- ✅ Filter components

### Expected Output

```
🚀 Hudhud KPI System - Basic Tests
==================================================
🧪 Testing module imports...
✅ Config module imported successfully
✅ Logger module imported successfully
✅ DataLoader module imported successfully
✅ CacheManager module imported successfully
✅ Layout module imported successfully
✅ Navigation module imported successfully
✅ Filters module imported successfully
✅ Callbacks module imported successfully
✅ UI Components module imported successfully

🎉 All modules imported successfully!

🧪 Testing configuration system...
✅ Config object created successfully
✅ Default configuration values correct
🎉 Configuration system working correctly!

🧪 Testing UI components...
✅ Metric card created successfully
   Card type: <class 'dash_bootstrap_components._components.Card'>
🎉 UI components working correctly!

🧪 Testing filter components...
✅ Main filters created successfully
✅ Quick filters created successfully
🎉 Filter components working correctly!

==================================================
📊 Test Results: 4/4 tests passed
🎉 All tests passed! System is ready to run.
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Error: No module named 'hudhud'
# Solution: Ensure you're in the correct directory
cd field_survey_system/portal
```

#### 2. Missing Dependencies

```bash
# Error: ModuleNotFoundError
# Solution: Install requirements
pip install -r requirements.txt
```

#### 3. Port Already in Use

```bash
# Error: Address already in use
# Solution: Change port in app.py or .env
API_PORT=8051
```

#### 4. Permission Errors

```bash
# Error: Permission denied
# Solution: Check file permissions and run as administrator if needed
```

### Getting Help

1. **Check the logs**: Look in `data/logs/` for error messages
2. **Run tests**: Use `python test_basic.py` to identify issues
3. **Check configuration**: Verify your `.env` file settings
4. **Review documentation**: Check `README.md` for detailed information

## 🔄 Development Mode

### Enable Debug Mode

```bash
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG
```

### Hot Reload

The application automatically reloads when you make changes to Python files.

### Logging

```bash
# View logs in real-time
tail -f data/logs/hudhud.log
```

## 📊 Next Steps

After successful startup:

1. **Explore the Dashboard**: Navigate through different sections
2. **Configure Data Sources**: Set up your data files in `data/input/`
3. **Customize KPIs**: Add new KPI modules as needed
4. **Set Up Reporting**: Configure automated reports
5. **User Management**: Add reviewers and configure permissions

## 🆘 Support

If you encounter issues:

1. Check this startup guide
2. Review the main `README.md`
3. Check the logs in `data/logs/`
4. Run the test suite with `python test_basic.py`
5. Create an issue in the repository

---

**Happy surveying! 🎯**
