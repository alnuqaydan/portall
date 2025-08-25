#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Callback Components
Interactive callbacks and event handlers for the system

Author: Hudhud Team
Date: 2024
"""

import dash
from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
import pandas as pd
from typing import Dict, Any, List, Optional
import logging

# Setup logging
logger = logging.getLogger(__name__)

def register_filter_callbacks(app: dash.Dash):
    """
    Register filter-related callbacks
    
    Args:
        app: Dash application instance
    """
    
    @app.callback(
        Output("city-filter", "options"),
        Input("date-filter", "date")
    )
    def update_city_options(selected_date):
        """Update city options based on selected date"""
        if not selected_date:
            raise PreventUpdate
        
        try:
            # Get cities available for the selected date
            # This would typically query your data source
            cities = ["Riyadh", "Jeddah", "Dammam", "Mecca", "Medina"]
            return [{"label": city, "value": city} for city in cities]
        except Exception as e:
            logger.error(f"Error updating city options: {e}")
            return []
    
    @app.callback(
        Output("territory-filter", "options"),
        [Input("city-filter", "value"),
         Input("date-filter", "date")]
    )
    def update_territory_options(selected_city, selected_date):
        """Update territory options based on selected city and date"""
        if not selected_city or not selected_date:
            raise PreventUpdate
        
        try:
            # Get territories available for the selected city and date
            # This would typically query your data source
            territories = {
                "Riyadh": ["North", "South", "East", "West", "Central"],
                "Jeddah": ["North", "South", "East", "West"],
                "Dammam": ["North", "South", "East", "West"],
                "Mecca": ["Central", "Outer"],
                "Medina": ["Central", "Outer"]
            }
            
            city_territories = territories.get(selected_city, [])
            return [{"label": territory, "value": territory} for territory in city_territories]
        except Exception as e:
            logger.error(f"Error updating territory options: {e}")
            return []
    
    @app.callback(
        Output("filter-summary", "children"),
        [Input("date-filter", "date"),
         Input("city-filter", "value"),
         Input("territory-filter", "value"),
         Input("starred-filter", "value"),
         Input("operation-filter", "value"),
         Input("status-filter", "value"),
         Input("confidence-filter", "value"),
         Input("media-filter", "value")]
    )
    def update_filter_summary(date, city, territory, starred, operation, status, confidence, media):
        """Update active filters summary"""
        active_filters = {}
        
        if date:
            active_filters["Date"] = date
        if city:
            active_filters["City"] = city
        if territory:
            active_filters["Territory"] = territory
        if starred:
            active_filters["Starred Users"] = "Yes"
        if operation and operation != "all":
            active_filters["Operation"] = operation
        if status and status != "all":
            active_filters["Status"] = status
        if confidence and confidence != [0, 1]:
            active_filters["Confidence"] = confidence
        if media and media != [0, 10]:
            active_filters["Media Count"] = media
        
        return active_filters

def register_navigation_callbacks(app: dash.Dash):
    """
    Register navigation-related callbacks
    
    Args:
        app: Dash application instance
    """
    
    @app.callback(
        Output("page-content", "children"),
        [Input("nav-dashboard", "n_clicks"),
         Input("nav-reviewers", "n_clicks"),
         Input("nav-transactions", "n_clicks"),
         Input("nav-logs", "n_clicks"),
         Input("nav-reports", "n_clicks")]
    )
    def navigate_to_page(dashboard_clicks, reviewers_clicks, transactions_clicks, logs_clicks, reports_clicks):
        """Handle navigation between pages"""
        ctx = callback_context
        
        if not ctx.triggered:
            # Default to dashboard
            return create_dashboard_content()
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id == "nav-dashboard":
            return create_dashboard_content()
        elif button_id == "nav-reviewers":
            return create_reviewers_content()
        elif button_id == "nav-transactions":
            return create_transactions_content()
        elif button_id == "nav-logs":
            return create_logs_content()
        elif button_id == "nav-reports":
            return create_reports_content()
        else:
            return create_dashboard_content()

def register_data_callbacks(app: dash.Dash):
    """
    Register data-related callbacks
    
    Args:
        app: Dash application instance
    """
    
    @app.callback(
        Output("data-table", "data"),
        Output("data-table", "columns"),
        [Input("apply-filters", "n_clicks"),
         Input("apply-advanced-filters", "n_clicks")],
        [State("date-filter", "date"),
         State("city-filter", "value"),
         State("territory-filter", "value"),
         State("starred-filter", "value"),
         State("operation-filter", "value"),
         State("status-filter", "value"),
         State("confidence-filter", "value"),
         State("media-filter", "value")]
    )
    def update_data_table(apply_clicks, advanced_clicks, date, city, territory, starred, operation, status, confidence, media):
        """Update data table based on applied filters"""
        if not callback_context.triggered:
            raise PreventUpdate
        
        try:
            # Apply filters to data
            filtered_data = apply_filters_to_data({
                "date": date,
                "city": city,
                "territory": territory,
                "starred": starred,
                "operation": operation,
                "status": status,
                "confidence": confidence,
                "media": media
            })
            
            # Create columns for the table
            columns = [
                {"name": "ID", "id": "id"},
                {"name": "Name", "id": "name"},
                {"name": "City", "id": "city"},
                {"name": "Territory", "id": "territory"},
                {"name": "Status", "id": "status"},
                {"name": "Created", "id": "created_at"}
            ]
            
            return filtered_data.to_dict("records"), columns
            
        except Exception as e:
            logger.error(f"Error updating data table: {e}")
            return [], []

def register_export_callbacks(app: dash.Dash):
    """
    Register export-related callbacks
    
    Args:
        app: Dash application instance
    """
    
    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("export-csv", "n_clicks"),
        [State("data-table", "data"),
         State("date-filter", "date"),
         State("city-filter", "value")]
    )
    def export_csv(n_clicks, data, date, city):
        """Export data to CSV"""
        if not n_clicks:
            raise PreventUpdate
        
        if not data:
            raise PreventUpdate
        
        try:
            df = pd.DataFrame(data)
            
            # Create filename with filter context
            filename_parts = ["export"]
            if date:
                filename_parts.append(f"date_{date}")
            if city:
                filename_parts.append(f"city_{city}")
            
            filename = "_".join(filename_parts) + ".csv"
            
            return dcc.send_data_frame(df.to_csv, filename)
            
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
            raise PreventUpdate

def register_quick_filter_callbacks(app: dash.Dash):
    """
    Register quick filter callbacks
    
    Args:
        app: Dash application instance
    """
    
    @app.callback(
        Output("date-filter", "date"),
        [Input("filter-today", "n_clicks"),
         Input("filter-week", "n_clicks"),
         Input("filter-month", "n_clicks"),
         Input("filter-30days", "n_clicks"),
         Input("filter-90days", "n_clicks")]
    )
    def apply_quick_filters(today_clicks, week_clicks, month_clicks, days30_clicks, days90_clicks):
        """Apply quick date filters"""
        if not callback_context.triggered:
            raise PreventUpdate
        
        button_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        if button_id == "filter-today":
            return today
        elif button_id == "filter-week":
            # Start of current week (Monday)
            days_since_monday = today.weekday()
            return today - timedelta(days=days_since_monday)
        elif button_id == "filter-month":
            # Start of current month
            return today.replace(day=1)
        elif button_id == "filter-30days":
            return today - timedelta(days=30)
        elif button_id == "filter-90days":
            return today - timedelta(days=90)
        else:
            return today

def register_preset_callbacks(app: dash.Dash):
    """
    Register filter preset callbacks
    
    Args:
        app: Dash application instance
    """
    
    @app.callback(
        [Output("date-filter", "date"),
         Output("city-filter", "value"),
         Output("territory-filter", "value"),
         Output("operation-filter", "value"),
         Output("status-filter", "value")],
        Input("load-preset", "n_clicks"),
        State("preset-selector", "value")
    )
    def load_filter_preset(n_clicks, preset_value):
        """Load filter preset"""
        if not n_clicks or not preset_value:
            raise PreventUpdate
        
        try:
            presets = {
                "high-priority": {
                    "date": datetime.now().date(),
                    "city": None,
                    "territory": None,
                    "operation": "all",
                    "status": "pending"
                },
                "recent": {
                    "date": (datetime.now() - timedelta(days=7)).date(),
                    "city": None,
                    "territory": None,
                    "operation": "all",
                    "status": "all"
                },
                "quality": {
                    "date": datetime.now().date(),
                    "city": None,
                    "territory": None,
                    "operation": "all",
                    "status": "rejected"
                },
                "performance": {
                    "date": (datetime.now() - timedelta(days=30)).date(),
                    "city": None,
                    "territory": None,
                    "operation": "all",
                    "status": "all"
                }
            }
            
            preset = presets.get(preset_value, {})
            return (
                preset.get("date"),
                preset.get("city"),
                preset.get("territory"),
                preset.get("operation"),
                preset.get("status")
            )
            
        except Exception as e:
            logger.error(f"Error loading preset: {e}")
            raise PreventUpdate

# Helper functions for content creation
def create_dashboard_content():
    """Create dashboard page content"""
    return html.Div([
        html.H2("Dashboard", className="mb-4"),
        html.P("Welcome to the Hudhud KPI System Dashboard")
    ])

def create_reviewers_content():
    """Create reviewers page content"""
    return html.Div([
        html.H2("Reviewers", className="mb-4"),
        html.P("Reviewer performance and metrics")
    ])

def create_transactions_content():
    """Create transactions page content"""
    return html.Div([
        html.H2("Transactions", className="mb-4"),
        html.P("Transaction data and analytics")
    ])

def create_logs_content():
    """Create logs page content"""
    return html.Div([
        html.H2("Logs", className="mb-4"),
        html.P("System logs and activity tracking")
    ])

def create_reports_content():
    """Create reports page content"""
    return html.Div([
        html.H2("Reports", className="mb-4"),
        html.P("Generated reports and analytics")
    ])

def apply_filters_to_data(filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply filters to data
    
    Args:
        filters: Dictionary of filter values
        
    Returns:
        Filtered DataFrame
    """
    # This would typically load data from your data source
    # and apply the filters
    # For now, return empty DataFrame
    return pd.DataFrame()
