# 🚀 Hudhud KPI System

A comprehensive **Field Survey System** built as a **Dynamic KPI Dashboard** for field surveyors and reviewers. Monitor and analyze field survey data with real-time KPIs, dynamic filtering, and comprehensive reporting capabilities.

## ✨ Key Features

- **Dynamic Reviewers System** - Configurable reviewer list with automatic KPI calculation
- **Advanced Filtering** - Date-based, geographic, and user-based filtering
- **Real-time Analytics** - Live KPI updates with interactive charts and tables
- **Comprehensive Export** - Multiple formats (CSV, Parquet, XLSX) with smart naming
- **Automated Reporting** - Daily and weekly automated reports
- **Modular KPI System** - Easy to extend with new KPIs
- **Modern UI** - Bootstrap-based interface with responsive design

## 🏗️ Architecture

### Core Components
- **Main Application** (`app.py`) - Dash-based web interface
- **KPI Engine** (`hudhud/`) - Modular KPI computation system
- **Data Processing** - CSV data ingestion and normalization
- **Reporting System** - Automated daily and weekly reports

### Technology Stack
- **Frontend**: Dash (Python web framework)
- **Backend**: Python with Pandas for data processing
- **Database**: SQLite with CSV data ingestion
- **UI**: Bootstrap + FontAwesome icons
- **Charts**: Plotly for interactive visualizations

## 📁 Project Structure

```
hudhud/
├── utils/                 # Utility modules
│   ├── config.py         # Configuration management
│   ├── logger.py         # Logging utilities
│   ├── data_loader.py    # Data loading and caching
│   └── cache_manager.py  # Cache management
├── components/            # UI components
│   ├── layout.py         # Main application layout
│   ├── navigation.py     # Navigation components
│   ├── filters.py        # Filter components
│   ├── callbacks.py      # Interactive callbacks
│   └── ui_components.py  # Reusable UI widgets
├── pages/                 # Page-specific components
│   └── [page_name]/      # Page-specific KPI modules
└── data/                  # Data management
    ├── input/            # Raw data files
    ├── cache/            # Processed data cache
    ├── output/           # Generated reports
    └── exports/          # User exports
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd field_survey_system/portal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8050`

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# Core settings
REVIEWERS=malngedan,aalbwardi,fahad,naif
CACHE_ENABLED=true
LOG_LEVEL=INFO

# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=field_survey_production

# Thresholds
MIN_CONFIDENCE=0.7
MAX_REVIEW_TIME=24

# Export settings
EXPORT_FORMATS=csv,parquet,xlsx
MAX_EXPORT_SIZE=10000
```

### Configuration Classes
The system uses structured configuration with dataclasses:

```python
from hudhud.utils.config import Config

config = Config()
config.load_environment_variables()

# Access configuration
print(config.database.host)
print(config.cache.enabled)
```

## 📊 Adding New KPIs

### 1. Create KPI Structure
```
hudhud/pages/[page_name]/kpis/[kpi_name]/
├── compute.py    # Business logic & calculations
├── view.py       # Dash UI components
└── README.md     # Documentation
```

### 2. Implement KPI Logic
```python
# compute.py
from hudhud.kpi_base import require_cols, apply_filters

@require_cols(['id', 'created_at', 'status'])
def compute_reviewer_performance(df, filters=None):
    """Compute reviewer performance metrics"""
    if filters:
        df = apply_filters(df, filters)
    
    # Your KPI calculation logic here
    return {
        'total_reviews': len(df),
        'approval_rate': len(df[df['status'] == 'approved']) / len(df)
    }
```

### 3. Create UI Components
```python
# view.py
from hudhud.components.ui_components import create_metric_card

def create_kpi_view(kpi_data):
    """Create KPI visualization"""
    return create_metric_card(
        title="Reviewer Performance",
        value=f"{kpi_data['approval_rate']:.1%}",
        subtitle=f"Total Reviews: {kpi_data['total_reviews']}"
    )
```

## 🔧 Available Filters

### Date Filters
- **Single Date**: Specific date selection
- **Date Range**: Start and end date selection
- **Quick Filters**: Today, This Week, This Month, Last 30/90 Days

### Geographic Filters
- **City**: Filter by specific cities
- **Territory/District**: Filter by territories within cities
- **Location-based**: Geographic coordinate filtering

### User Filters
- **Starred Users**: Priority users with special filtering
- **Specific Reviewers**: Filter by individual reviewer
- **Role-based**: Reviewers vs. Surveyors

### Data Filters
- **Operation Type**: Create, Update, Delete operations
- **Review Status**: Pending, Approved, Rejected
- **Confidence Level**: Data quality confidence (0-1)
- **Media Count**: Number of attached media files

## 📤 Export System

### Supported Formats
- **CSV**: Comma-separated values
- **Parquet**: Columnar storage format
- **XLSX**: Excel spreadsheet format

### Export Features
- **Smart Naming**: Automatic filename generation with filter context
- **Filtered Exports**: Respects active filter selections
- **Size Limits**: Configurable maximum export sizes
- **Batch Processing**: Export multiple formats simultaneously

## 📈 Reporting

### Daily Reports
- **Automatic Generation**: Runs daily at scheduled time
- **Performance Metrics**: Reviewer performance summaries
- **Data Quality**: Data validation and consistency reports
- **Export**: Multiple format support

### Weekly Reports
- **Tuesday Generation**: Weekly summaries for specific users
- **Trend Analysis**: Performance trends over time
- **Comparative Metrics**: Reviewer performance comparison
- **Cached Data**: Optimized for performance

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd field_survey_system/portal
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(debug=True, port=8051)
   ```

3. **Data Loading Issues**
   - Check data file paths in configuration
   - Verify file permissions
   - Check log files for detailed error messages

### Logging
The system provides comprehensive logging:

```python
from hudhud.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Application started")
logger.error("Error occurred", exc_info=True)
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Quality
- Use `black` for code formatting
- Run `flake8` for linting
- Ensure type hints with `mypy`
- Write comprehensive docstrings

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=hudhud

# Run specific test file
pytest tests/test_kpi_base.py
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Hudhud Team** - Development and maintenance
- **Field Survey Specialists** - Domain expertise and requirements
- **Data Analysts** - KPI design and validation

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation and examples

---

**Built with ❤️ by the Hudhud Team**
