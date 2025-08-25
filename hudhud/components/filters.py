#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Filter Components
Filter and search components for the system

Author: Hudhud Team
Date: 2024
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

def create_filters() -> dbc.Card:
    """
    Create main filters section
    
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

def create_advanced_filters() -> dbc.Card:
    """
    Create advanced filters section
    
    Returns:
        Advanced filters card
    """
    return dbc.Card([
        dbc.CardHeader([
            html.H5("Advanced Filters", className="mb-0"),
            html.Small("Additional filtering options", className="text-muted")
        ]),
        
        dbc.CardBody([
            dbc.Row([
                # Date range filter
                dbc.Col([
                    dbc.Label("Date Range", html_for="date-range-filter"),
                    dcc.DatePickerRange(
                        id="date-range-filter",
                        start_date=(datetime.now() - timedelta(days=30)).date(),
                        end_date=datetime.now().date(),
                        display_format="DD/MM/YYYY",
                        className="w-100"
                    )
                ], width=4),
                
                # Operation type filter
                dbc.Col([
                    dbc.Label("Operation Type", html_for="operation-filter"),
                    dcc.Dropdown(
                        id="operation-filter",
                        options=[
                            {"label": "All", "value": "all"},
                            {"label": "Create", "value": "create"},
                            {"label": "Update", "value": "update"},
                            {"label": "Delete", "value": "delete"}
                        ],
                        value="all",
                        className="w-100"
                    )
                ], width=4),
                
                # Review status filter
                dbc.Col([
                    dbc.Label("Review Status", html_for="status-filter"),
                    dcc.Dropdown(
                        id="status-filter",
                        options=[
                            {"label": "All", "value": "all"},
                            {"label": "Pending", "value": "pending"},
                            {"label": "Approved", "value": "approved"},
                            {"label": "Rejected", "value": "rejected"}
                        ],
                        value="all",
                        className="w-100"
                    )
                ], width=4),
            ]),
            
            dbc.Row([
                # Confidence filter
                dbc.Col([
                    dbc.Label("Confidence Level", html_for="confidence-filter"),
                    dcc.RangeSlider(
                        id="confidence-filter",
                        min=0,
                        max=1,
                        step=0.1,
                        value=[0, 1],
                        marks={i/10: str(i/10) for i in range(0, 11, 2)},
                        className="w-100"
                    )
                ], width=6),
                
                # Media count filter
                dbc.Col([
                    dbc.Label("Media Count", html_for="media-filter"),
                    dcc.RangeSlider(
                        id="media-filter",
                        min=0,
                        max=10,
                        step=1,
                        value=[0, 10],
                        marks={i: str(i) for i in range(0, 11, 2)},
                        className="w-100"
                    )
                ], width=6),
            ], className="mt-3"),
            
            # Action buttons
            dbc.Row([
                dbc.Col([
                    dbc.Button("Apply Advanced Filters", id="apply-advanced-filters", color="primary", className="me-2"),
                    dbc.Button("Reset Advanced", id="reset-advanced-filters", color="outline-secondary"),
                ], className="mt-3")
            ])
        ])
    ], className="mb-3")

def create_quick_filters() -> dbc.ButtonGroup:
    """
    Create quick filter buttons
    
    Returns:
        Quick filter button group
    """
    return dbc.ButtonGroup([
        dbc.Button("Today", id="filter-today", color="outline-primary", size="sm"),
        dbc.Button("This Week", id="filter-week", color="outline-primary", size="sm"),
        dbc.Button("This Month", id="filter-month", color="outline-primary", size="sm"),
        dbc.Button("Last 30 Days", id="filter-30days", color="outline-primary", size="sm"),
        dbc.Button("Last 90 Days", id="filter-90days", color="outline-primary", size="sm"),
    ], className="mb-3")

def create_filter_summary(active_filters: Dict[str, Any]) -> html.Div:
    """
    Create active filters summary
    
    Args:
        active_filters: Active filters dictionary
        
    Returns:
        Filter summary component
    """
    if not active_filters:
        return html.Div()
    
    filter_chips = []
    for key, value in active_filters.items():
        if value is not None and value != "" and value != "all":
            if isinstance(value, list):
                if len(value) == 2 and isinstance(value[0], (int, float)) and isinstance(value[1], (int, float)):
                    # Range filter
                    filter_chips.append(
                        dbc.Badge([
                            f"{key}: {value[0]} - {value[1]}",
                            dbc.Button(
                                html.I(className="fas fa-times"),
                                color="light",
                                size="sm",
                                className="ms-2",
                                id=f"remove-filter-{key}"
                            )
                        ], color="info", className="me-2 mb-2")
                    )
                else:
                    # List filter
                    filter_chips.append(
                        dbc.Badge([
                            f"{key}: {', '.join(map(str, value))}",
                            dbc.Button(
                                html.I(className="fas fa-times"),
                                color="light",
                                size="sm",
                                className="ms-2",
                                id=f"remove-filter-{key}"
                            )
                        ], color="info", className="me-2 mb-2")
                    )
            else:
                # Single value filter
                filter_chips.append(
                    dbc.Badge([
                        f"{key}: {value}",
                        dbc.Button(
                            html.I(className="fas fa-times"),
                            color="light",
                            size="sm",
                            className="ms-2",
                            id=f"remove-filter-{key}"
                        )
                    ], color="info", className="me-2 mb-2")
                )
    
    if not filter_chips:
        return html.Div()
    
    return html.Div([
        html.H6("Active Filters:", className="mb-2"),
        html.Div(filter_chips),
        dbc.Button("Clear All Filters", id="clear-all-filters", color="outline-secondary", size="sm")
    ], className="mb-3 p-3 bg-light rounded")

def create_search_box(placeholder: str = "Search...", id: str = "search-box") -> dbc.InputGroup:
    """
    Create search input box
    
    Args:
        placeholder: Search placeholder text
        id: Input ID
        
    Returns:
        Search input group
    """
    return dbc.InputGroup([
        dbc.InputGroupText(html.I(className="fas fa-search")),
        dbc.Input(
            type="text",
            placeholder=placeholder,
            id=id,
            className="form-control"
        ),
        dbc.Button("Search", id=f"{id}-btn", color="primary")
    ], className="mb-3")

def create_filter_presets() -> dbc.Card:
    """
    Create filter presets
    
    Returns:
        Filter presets card
    """
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Filter Presets", className="mb-0"),
            html.Small("Save and load common filter combinations", className="text-muted")
        ]),
        
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Select(
                        id="preset-selector",
                        options=[
                            {"label": "Select Preset", "value": ""},
                            {"label": "High Priority Items", "value": "high-priority"},
                            {"label": "Recent Activity", "value": "recent"},
                            {"label": "Quality Issues", "value": "quality"},
                            {"label": "Performance Review", "value": "performance"}
                        ],
                        value="",
                        size="sm"
                    )
                ], width=6),
                dbc.Col([
                    dbc.Button("Load Preset", id="load-preset", color="primary", size="sm", className="me-2"),
                    dbc.Button("Save Current", id="save-preset", color="outline-secondary", size="sm")
                ], width=6)
            ])
        ])
    ], className="mb-3")
