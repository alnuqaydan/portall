#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Main Application
Main entry point for the Dash application

Author: Hudhud Team
Date: 2024
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import logging
import os
from pathlib import Path

# Import custom components
from hudhud.utils.config import Config
from hudhud.utils.logger import setup_logger
from hudhud.utils.data_loader import DataLoader
from hudhud.utils.cache_manager import CacheManager
from hudhud.components.layout import create_layout
from hudhud.components.navigation import create_navigation
from hudhud.components.filters import (
    create_filters, create_advanced_filters, create_quick_filters,
    create_filter_summary, create_search_box, create_filter_presets
)
from hudhud.components.callbacks import (
    register_filter_callbacks, register_navigation_callbacks,
    register_data_callbacks, register_export_callbacks,
    register_quick_filter_callbacks, register_preset_callbacks
)
from hudhud.components.ui_components import (
    create_metric_card, create_chart_card, create_data_table,
    create_loading_spinner, create_alert
)

class HudhudApp:
    """
    Main application class for the Hudhud KPI System
    """
    
    def __init__(self):
        """Initialize the application"""
        # Setup configuration
        self.config = Config()
        self.config.load_environment_variables()
        
        # Setup logging
        self.logger = setup_logger(
            log_file=self.config.logging.log_file,
            level=self.config.logging.level
        )
        
        # Initialize data components
        self.data_loader = DataLoader(self.config)
        self.cache_manager = CacheManager(self.config)
        
        # Initialize Dash app
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
                "https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap"
            ],
            suppress_callback_exceptions=True
        )
        
        # Configure app
        self.app.title = "Hudhud KPI System"
        self.app.config.suppress_callback_exceptions = True
        
        # Setup layout
        self.setup_layout()
        
        # Register callbacks
        self.register_callbacks()
        
        self.logger.info("Hudhud KPI System initialized successfully")
    
    def setup_layout(self):
        """Setup the application layout"""
        self.app.layout = create_layout()
        
        # Add health check endpoint for Render
        @self.app.server.route('/health')
        def health_check():
            return {'status': 'healthy', 'service': 'Hudhud KPI System'}, 200
        
        # Add Render-compatible health check endpoint
        @self.app.server.route('/healthz')
        def health_check_render():
            return {'status': 'healthy', 'service': 'Hudhud KPI System'}, 200
        
        self.logger.info("Application layout configured")
    
    def register_callbacks(self):
        """Register all application callbacks"""
        try:
            # Register filter callbacks
            register_filter_callbacks(self.app)
            
            # Register navigation callbacks
            register_navigation_callbacks(self.app)
            
            # Register data callbacks
            register_data_callbacks(self.app)
            
            # Register export callbacks
            register_export_callbacks(self.app)
            
            # Register quick filter callbacks
            register_quick_filter_callbacks(self.app)
            
            # Register preset callbacks
            register_preset_callbacks(self.app)
            
            self.logger.info("All callbacks registered successfully")
            
        except Exception as e:
            self.logger.error(f"Error registering callbacks: {e}")
            raise
    
    def run(self, debug: bool = False, host: str = "0.0.0.0", port: int = 8050):
        """
        Run the application
        
        Args:
            debug: Enable debug mode
            host: Host address to bind to
            port: Port number to bind to
        """
        try:
            self.logger.info(f"Starting Hudhud KPI System on {host}:{port}")
            self.app.run_server(
                debug=debug,
                host=host,
                port=port
            )
        except Exception as e:
            self.logger.error(f"Error starting application: {e}")
            raise

def create_sample_data():
    """Create sample data for demonstration"""
    import pandas as pd
    from datetime import datetime, timedelta
    import random
    
    # Sample cities and territories
    cities = ["Riyadh", "Jeddah", "Dammam", "Mecca", "Medina"]
    territories = {
        "Riyadh": ["North", "South", "East", "West", "Central"],
        "Jeddah": ["North", "South", "East", "West"],
        "Dammam": ["North", "South", "East", "West"],
        "Mecca": ["Central", "Outer"],
        "Medina": ["Central", "Outer"]
    }
    
    # Generate sample data
    data = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(100):
        city = random.choice(cities)
        territory = random.choice(territories[city])
        date = start_date + timedelta(days=random.randint(0, 30))
        
        data.append({
            "id": i + 1,
            "name": f"Business {i + 1}",
            "city": city,
            "territory": territory,
            "status": random.choice(["Pending", "Approved", "Rejected"]),
            "created_at": date.strftime("%Y-%m-%d"),
            "confidence": round(random.uniform(0.5, 1.0), 2),
            "media_count": random.randint(0, 5)
        })
    
    return pd.DataFrame(data)

def main():
    """Main entry point"""
    try:
        # Create and run application
        app = HudhudApp()
        app.run(debug=True, port=8050)
        
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")
        logging.error(f"Application error: {e}")

# Create global app instance for production deployment (gunicorn)
app = HudhudApp()

if __name__ == "__main__":
    main()
