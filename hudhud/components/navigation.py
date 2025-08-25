#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Navigation Components
Navigation and link components for the system

Author: Hudhud Team
Date: 2024
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Any, List

def create_navigation() -> dbc.Nav:
    """
    Create main navigation bar
    
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

def create_breadcrumb(items: List[Dict[str, str]]) -> dbc.Breadcrumb:
    """
    Create breadcrumb navigation
    
    Args:
        items: List of items [{"label": "Title", "href": "Link"}]
        
    Returns:
        Breadcrumb navigation
    """
    breadcrumb_items = []
    
    for i, item in enumerate(items):
        if i == len(items) - 1:
            # Last item (active)
            breadcrumb_items.append(
                dbc.BreadcrumbItem(item["label"], active=True)
            )
        else:
            # Regular item
            breadcrumb_items.append(
                dbc.BreadcrumbItem(item["label"], href=item["href"])
            )
    
    return dbc.Breadcrumb(breadcrumb_items, className="mb-3")

def create_tab_navigation(tabs: List[Dict[str, Any]]) -> dbc.Tabs:
    """
    Create tab navigation
    
    Args:
        tabs: List of tabs [{"label": "Title", "tab_id": "id", "content": "Content"}]
        
    Returns:
        Tabs
    """
    tab_items = []
    
    for tab in tabs:
        tab_items.append(
            dbc.Tab(
                tab["content"],
                label=tab["label"],
                tab_id=tab["tab_id"]
            )
        )
    
    return dbc.Tabs(tab_items, id="main-tabs", active_tab=tabs[0]["tab_id"] if tabs else None)

def create_sidebar_navigation(items: List[Dict[str, Any]]) -> html.Div:
    """
    Create sidebar navigation
    
    Args:
        items: List of items
        
    Returns:
        Sidebar
    """
    nav_items = []
    
    for item in items:
        nav_items.append(
            html.Li([
                dbc.NavLink([
                    html.I(className=f"fas fa-{item.get('icon', 'circle')} me-2"),
                    item["label"]
                ], href=item["href"], id=item.get("id", ""))
            ], className="nav-item")
        )
    
    return html.Div([
        html.Ul(nav_items, className="nav flex-column")
    ], className="sidebar-nav")

def create_pagination(total_pages: int, current_page: int = 1, page_size: int = 10) -> dbc.Pagination:
    """
    Create page pagination
    
    Args:
        total_pages: Total number of pages
        current_page: Current page
        page_size: Page size
        
    Returns:
        Pagination
    """
    return dbc.Pagination(
        id="pagination",
        active_page=current_page,
        total=total_pages,
        max_value=total_pages,
        first_last=True,
        previous_next=True,
        size="sm",
        className="justify-content-center"
    )

def create_page_size_selector(page_sizes: List[int] = None) -> dbc.Select:
    """
    Create page size selector
    
    Args:
        page_sizes: Available page sizes
        
    Returns:
        Size selector
    """
    if page_sizes is None:
        page_sizes = [10, 25, 50, 100]
    
    options = [{"label": str(size), "value": size} for size in page_sizes]
    
    return dbc.Select(
        id="page-size-selector",
        options=options,
        value=page_sizes[0],
        size="sm",
        style={"width": "100px"}
    )

def create_sort_controls(columns: List[Dict[str, str]]) -> html.Div:
    """
    Create sort controls
    
    Args:
        columns: List of columns [{"key": "key", "label": "Title"}]
        
    Returns:
        Sort controls
    """
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("Sort by:", className="me-2"),
                dbc.Select(
                    id="sort-column",
                    options=[{"label": col["label"], "value": col["key"]} for col in columns],
                    value=columns[0]["key"] if columns else None,
                    size="sm"
                )
            ], width=4),
            dbc.Col([
                dbc.Label("Direction:", className="me-2"),
                dbc.Select(
                    id="sort-direction",
                    options=[
                        {"label": "Ascending", "value": "asc"},
                        {"label": "Descending", "value": "desc"}
                    ],
                    value="asc",
                    size="sm"
                )
            ], width=4),
            dbc.Col([
                dbc.Button("Apply Sort", id="apply-sort", color="primary", size="sm")
            ], width=4)
        ])
    ], className="mb-3")

def create_view_controls(view_types: List[str] = None) -> dbc.ButtonGroup:
    """
    Create view controls
    
    Args:
        view_types: Available view types
        
    Returns:
        Button group
    """
    if view_types is None:
        view_types = ["table", "cards", "chart"]
    
    buttons = []
    for view_type in view_types:
        icon_map = {
            "table": "table",
            "cards": "th-large",
            "chart": "chart-bar"
        }
        
        buttons.append(
            dbc.Button(
                html.I(className=f"fas fa-{icon_map.get(view_type, 'circle')}"),
                id=f"view-{view_type}",
                color="outline-secondary",
                size="sm",
                className="me-1"
            )
        )
    
    return dbc.ButtonGroup(buttons, className="mb-3")

def create_filter_summary(active_filters: Dict[str, Any]) -> html.Div:
    """
    Create active filters summary
    
    Args:
        active_filters: Active filters
        
    Returns:
        Filter summary
    """
    if not active_filters:
        return html.Div()
    
    filter_chips = []
    for key, value in active_filters.items():
        if value is not None and value != "":
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
