#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Layout Components
Layout and interface components for the system

Author: Hudhud Team
Date: 2024
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Any, List

def create_layout() -> html.Div:
    """
    Create main application layout
    
    Returns:
        Main layout
    """
    return html.Div([
        # Header
        create_header(),
        
        # Navigation
        create_navigation(),
        
        # Main content area
        html.Div([
            # Filters section
            create_filters(),
            
            # Content area
            html.Div(id="page-content", className="content-area"),
            
        ], className="main-content"),
        
        # Footer
        create_footer(),
        
        # Download component
        dcc.Download(id="download-dataframe"),
        
        # Store components
        dcc.Store(id="session-store"),
        dcc.Store(id="data-store"),
        dcc.Store(id="filters-store"),
        
        # Interval for auto-refresh
        dcc.Interval(
            id="interval-component",
            interval=300000,  # 5 minutes
            n_intervals=0
        ),
        
    ], className="app-container")

def create_header() -> dbc.Navbar:
    """
    Create application header
    
    Returns:
        Top navigation bar
    """
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand([
                html.I(className="fas fa-chart-line me-2"),
                "Hudhud KPI System",
                html.Span("KPI Monitoring System", className="ms-2 text-muted")
            ], className="fw-bold"),
            
            dbc.Nav([
                dbc.NavItem(dbc.Button("Refresh Data", id="refresh-btn", color="primary", size="sm")),
                dbc.NavItem(dbc.Button("Settings", id="settings-btn", color="outline-secondary", size="sm")),
                dbc.NavItem(dbc.Button("Help", id="help-btn", color="outline-info", size="sm")),
            ], className="ms-auto"),
            
        ]),
        color="dark",
        dark=True,
        className="mb-3"
    )

def create_navigation() -> dbc.Nav:
    """
    Create navigation bar
    
    Returns:
        Navigation bar
    """
    return dbc.Nav([
        dbc.NavItem(dbc.NavLink("Dashboard", href="/", id="nav-dashboard")),
        dbc.NavItem(dbc.NavLink("Reviewers", href="/reviewers", id="nav-reviewers")),
        dbc.NavItem(dbc.NavLink("Transactions", href="/transactions", id="nav-transactions")),
        dbc.NavItem(dbc.NavLink("Logs", href="/logs", id="nav-logs")),
        dbc.NavItem(dbc.NavLink("Reports", href="/reports", id="nav-reports")),
    ], className="mb-3")

def create_filters() -> dbc.Card:
    """
    Create filters section
    
    Returns:
        Filters card
    """
    return dbc.Card([
        dbc.CardHeader([
            html.H5("Filters", className="mb-0"),
            html.Small("Select criteria to display data", className="text-muted")
        ]),
        
        dbc.CardBody([
            dbc.Row([
                # Date filter
                dbc.Col([
                    dbc.Label("Date", html_for="date-filter"),
                    dcc.DatePickerSingle(
                        id="date-filter",
                        date=datetime.now().date(),
                        display_format="DD/MM/YYYY",
                        className="w-100"
                    )
                ], width=3),
                
                # City filter
                dbc.Col([
                    dbc.Label("City", html_for="city-filter"),
                    dcc.Dropdown(
                        id="city-filter",
                        placeholder="Select City",
                        clearable=True,
                        className="w-100"
                    )
                ], width=3),
                
                # Territory filter
                dbc.Col([
                    dbc.Label("District/Territory", html_for="territory-filter"),
                    dcc.Dropdown(
                        id="territory-filter",
                        placeholder="Select District",
                        clearable=True,
                        className="w-100"
                    )
                ], width=3),
                
                # Starred users filter
                dbc.Col([
                    dbc.Label("Starred Users", html_for="starred-filter"),
                    dbc.Checkbox(
                        id="starred-filter",
                        label="Show starred users only",
                        className="mt-2"
                    )
                ], width=3),
            ]),
            
            # Action buttons
            dbc.Row([
                dbc.Col([
                    dbc.Button("Apply Filters", id="apply-filters", color="primary", className="me-2"),
                    dbc.Button("Reset", id="reset-filters", color="outline-secondary"),
                ], className="mt-3")
            ])
        ])
    ], className="mb-3")

def create_footer() -> dbc.Footer:
    """
    Create application footer
    
    Returns:
        Application footer
    """
    return dbc.Footer([
        dbc.Container([
            html.Div([
                html.Span("© 2024 Hudhud Team", className="me-3"),
                html.Span("•", className="me-3"),
                html.Span("Comprehensive monitoring system for reviewers and surveyors", className="me-3"),
                html.Span("•", className="me-3"),
                html.Span("Version 1.0.0", className="me-3"),
            ], className="text-center text-muted")
        ])
    ], className="mt-5 py-3 bg-light")

def create_page_layout(page_title: str, page_description: str = "", children: List = None) -> html.Div:
    """
    Create page layout
    
    Args:
        page_title: Page title
        page_description: Page description
        children: Page content
        
    Returns:
        Page layout
    """
    if children is None:
        children = []
    
    return html.Div([
        # Page header
        dbc.Row([
            dbc.Col([
                html.H2(page_title, className="mb-2"),
                html.P(page_description, className="text-muted mb-4") if page_description else None
            ])
        ], className="mb-4"),
        
        # Page content
        html.Div(children, className="page-content")
        
    ], className="page-container")

def create_loading_spinner() -> dbc.Spinner:
    """
    Create loading spinner
    
    Returns:
        Loading spinner
    """
    return dbc.Spinner(
        html.Div("Loading...", className="text-center text-muted"),
        color="primary",
        size="lg"
    )

def create_error_message(message: str) -> dbc.Alert:
    """
    Create error message
    
    Args:
        message: Error message
        
    Returns:
        Error alert
    """
    return dbc.Alert([
        html.I(className="fas fa-exclamation-triangle me-2"),
        message
    ], color="danger", className="mb-3")

def create_success_message(message: str) -> dbc.Alert:
    """
    Create success message
    
    Args:
        message: Success message
        
    Returns:
        Success alert
    """
    return dbc.Alert([
        html.I(className="fas fa-check-circle me-2"),
        message
    ], color="success", className="mb-3")

def create_info_card(title: str, value: Any, subtitle: str = "", icon: str = "info-circle", color: str = "primary") -> dbc.Card:
    """
    Create information card
    
    Args:
        title: Title
        value: Value
        subtitle: Subtitle
        icon: Icon
        color: Color
        
    Returns:
        Information card
    """
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.I(className=f"fas fa-{icon} fa-2x text-{color}")
                ], width="auto"),
                dbc.Col([
                    html.H4(value, className="mb-1"),
                    html.H6(title, className="text-muted mb-1"),
                    html.Small(subtitle, className="text-muted") if subtitle else None
                ])
            ], className="align-items-center")
        ])
    ], className="h-100")

def create_metric_row(metrics: List[Dict[str, Any]]) -> dbc.Row:
    """
    Create row of metrics
    
    Args:
        metrics: List of metrics
        
    Returns:
        Metrics row
    """
    cols = []
    for metric in metrics:
        cols.append(
            dbc.Col(
                create_info_card(
                    title=metric.get("title", ""),
                    value=metric.get("value", ""),
                    subtitle=metric.get("subtitle", ""),
                    icon=metric.get("icon", "info-circle"),
                    color=metric.get("color", "primary")
                ),
                width=12 // len(metrics)
            )
        )
    
    return dbc.Row(cols, className="mb-4")

# Import datetime for date picker
from datetime import datetime
