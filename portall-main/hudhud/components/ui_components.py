#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - UI Components
Reusable UI components and widgets for the system

Author: Hudhud Team
Date: 2024
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import dash_table

def create_metric_card(title: str, value: Union[str, int, float], 
                      subtitle: str = "", color: str = "primary",
                      icon: str = "fas fa-chart-line") -> dbc.Card:
    """
    Create a metric card with title, value, and optional subtitle
    
    Args:
        title: Card title
        value: Main metric value
        subtitle: Optional subtitle text
        color: Bootstrap color theme
        icon: FontAwesome icon class
        
    Returns:
        Metric card component
    """
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H4(title, className="text-muted mb-1"),
                    html.H2(value, className=f"text-{color} mb-1"),
                    html.Small(subtitle, className="text-muted")
                ], width=8),
                dbc.Col([
                    html.I(className=f"{icon} fa-2x text-{color}")
                ], width=4, className="text-end")
            ])
        ])
    ], className="mb-3")

def create_chart_card(title: str, chart: go.Figure, 
                     height: int = 400) -> dbc.Card:
    """
    Create a card containing a chart
    
    Args:
        title: Card title
        chart: Plotly figure object
        height: Chart height in pixels
        
    Returns:
        Chart card component
    """
    return dbc.Card([
        dbc.CardHeader([
            html.H5(title, className="mb-0")
        ]),
        dbc.CardBody([
            dcc.Graph(
                figure=chart,
                config={'displayModeBar': False},
                style={'height': height}
            )
        ])
    ], className="mb-3")

def create_data_table(data: List[Dict], columns: List[Dict],
                     id: str = "data-table", page_size: int = 10) -> dbc.Card:
    """
    Create a data table card
    
    Args:
        data: Table data as list of dictionaries
        columns: Table columns configuration
        id: Table component ID
        page_size: Number of rows per page
        
    Returns:
        Data table card component
    """
    return dbc.Card([
        dbc.CardHeader([
            html.H5("Data Table", className="mb-0"),
            html.Small(f"Showing {len(data)} records", className="text-muted")
        ]),
        dbc.CardBody([
            dash_table.DataTable(
                id=id,
                data=data,
                columns=columns,
                page_size=page_size,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'minWidth': '100px'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi"
            )
        ])
    ], className="mb-3")

def create_loading_spinner(id: str = "loading-spinner") -> dbc.Spinner:
    """
    Create a loading spinner component
    
    Args:
        id: Spinner component ID
        
    Returns:
        Loading spinner component
    """
    return dbc.Spinner(
        html.Div(id=id),
        color="primary",
        size="lg"
    )

def create_alert(message: str, alert_type: str = "info",
                 dismissable: bool = True, id: str = "alert") -> dbc.Alert:
    """
    Create an alert component
    
    Args:
        message: Alert message text
        alert_type: Bootstrap alert type (success, warning, danger, info)
        dismissable: Whether alert can be dismissed
        id: Alert component ID
        
    Returns:
        Alert component
    """
    return dbc.Alert(
        message,
        color=alert_type,
        dismissable=dismissable,
        id=id,
        className="mb-3"
    )

def create_progress_bar(value: float, label: str = "",
                       color: str = "primary", striped: bool = True,
                       animated: bool = True) -> dbc.Progress:
    """
    Create a progress bar component
    
    Args:
        value: Progress value (0-100)
        label: Progress label text
        color: Bootstrap color theme
        striped: Whether to show stripes
        animated: Whether to animate the progress
        
    Returns:
        Progress bar component
    """
    return dbc.Progress([
        dbc.Progress(value, color=color, striped=striped, animated=animated)
    ], label=label, className="mb-3")

def create_badge(text: str, color: str = "primary",
                pill: bool = False) -> dbc.Badge:
    """
    Create a badge component
    
    Args:
        text: Badge text
        color: Bootstrap color theme
        pill: Whether to use pill shape
        
    Returns:
        Badge component
    """
    return dbc.Badge(text, color=color, pill=pill, className="me-2")

def create_button_group(buttons: List[Dict], size: str = "md") -> dbc.ButtonGroup:
    """
    Create a button group component
    
    Args:
        buttons: List of button configurations
        size: Button size (sm, md, lg)
        
    Returns:
        Button group component
    """
    button_components = []
    for button in buttons:
        btn = dbc.Button(
            button.get("text", ""),
            id=button.get("id", ""),
            color=button.get("color", "secondary"),
            size=size,
            className=button.get("className", "")
        )
        button_components.append(btn)
    
    return dbc.ButtonGroup(button_components, className="mb-3")

def create_tabs(tabs: List[Dict], id: str = "tabs") -> dbc.Tabs:
    """
    Create a tabs component
    
    Args:
        tabs: List of tab configurations
        id: Tabs component ID
        
    Returns:
        Tabs component
    """
    tab_list = []
    for tab in tabs:
        tab_item = dbc.Tab(
            tab.get("content", ""),
            label=tab.get("label", ""),
            tab_id=tab.get("id", ""),
            className=tab.get("className", "")
        )
        tab_list.append(tab_item)
    
    return dbc.Tabs(tab_list, id=id, className="mb-3")

def create_accordion(items: List[Dict], id: str = "accordion") -> dbc.Accordion:
    """
    Create an accordion component
    
    Args:
        items: List of accordion item configurations
        id: Accordion component ID
        
    Returns:
        Accordion component
    """
    accordion_items = []
    for item in items:
        accordion_item = dbc.AccordionItem(
            item.get("content", ""),
            title=item.get("title", ""),
            item_id=item.get("id", ""),
            className=item.get("className", "")
        )
        accordion_items.append(accordion_item)
    
    return dbc.Accordion(accordion_items, id=id, className="mb-3")

def create_modal(title: str, body: str, id: str = "modal",
                size: str = "lg") -> dbc.Modal:
    """
    Create a modal component
    
    Args:
        title: Modal title
        body: Modal body content
        id: Modal component ID
        size: Modal size (sm, lg, xl)
        
    Returns:
        Modal component
    """
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(title)),
        dbc.ModalBody(body),
        dbc.ModalFooter([
            dbc.Button("Close", id=f"{id}-close", className="ms-auto")
        ])
    ], id=id, size=size, is_open=False)

def create_tooltip(target_id: str, text: str, placement: str = "top") -> dbc.Tooltip:
    """
    Create a tooltip component
    
    Args:
        target_id: ID of the element to attach tooltip to
        text: Tooltip text
        placement: Tooltip placement (top, bottom, left, right)
        
    Returns:
        Tooltip component
    """
    return dbc.Tooltip(text, target=target_id, placement=placement)

def create_popover(target_id: str, title: str, body: str,
                  placement: str = "top") -> dbc.Popover:
    """
    Create a popover component
    
    Args:
        target_id: ID of the element to attach popover to
        title: Popover title
        body: Popover body content
        placement: Popover placement (top, bottom, left, right)
        
    Returns:
        Popover component
    """
    return dbc.Popover([
        dbc.PopoverHeader(title),
        dbc.PopoverBody(body)
    ], target=target_id, placement=placement, trigger="click")

def create_line_chart(data: pd.DataFrame, x_col: str, y_col: str,
                     title: str = "", color_col: str = None) -> go.Figure:
    """
    Create a line chart
    
    Args:
        data: DataFrame containing chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color_col: Column name for color grouping
        
    Returns:
        Plotly figure object
    """
    if color_col:
        fig = px.line(data, x=x_col, y=y_col, color=color_col, title=title)
    else:
        fig = px.line(data, x=x_col, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        hovermode='x unified'
    )
    
    return fig

def create_bar_chart(data: pd.DataFrame, x_col: str, y_col: str,
                     title: str = "", color_col: str = None,
                     orientation: str = "v") -> go.Figure:
    """
    Create a bar chart
    
    Args:
        data: DataFrame containing chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color_col: Column name for color grouping
        orientation: Chart orientation (v for vertical, h for horizontal)
        
    Returns:
        Plotly figure object
    """
    if color_col:
        fig = px.bar(data, x=x_col, y=y_col, color=color_col, title=title, orientation=orientation)
    else:
        fig = px.bar(data, x=x_col, y=y_col, title=title, orientation=orientation)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )
    
    return fig

def create_pie_chart(data: pd.DataFrame, names_col: str, values_col: str,
                     title: str = "") -> go.Figure:
    """
    Create a pie chart
    
    Args:
        data: DataFrame containing chart data
        names_col: Column name for slice names
        values_col: Column name for slice values
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.pie(data, names=names_col, values=values_col, title=title)
    
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_scatter_plot(data: pd.DataFrame, x_col: str, y_col: str,
                        title: str = "", color_col: str = None,
                        size_col: str = None) -> go.Figure:
    """
    Create a scatter plot
    
    Args:
        data: DataFrame containing chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color_col: Column name for color grouping
        size_col: Column name for point size
        
    Returns:
        Plotly figure object
    """
    if color_col and size_col:
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col, size=size_col, title=title)
    elif color_col:
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col, title=title)
    elif size_col:
        fig = px.scatter(data, x=x_col, y=y_col, size=size_col, title=title)
    else:
        fig = px.scatter(data, x=x_col, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        hovermode='closest'
    )
    
    return fig

def create_heatmap(data: pd.DataFrame, x_col: str, y_col: str,
                   values_col: str, title: str = "") -> go.Figure:
    """
    Create a heatmap
    
    Args:
        data: DataFrame containing chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        values_col: Column name for color values
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    # Pivot data for heatmap
    pivot_data = data.pivot(index=y_col, columns=x_col, values=values_col)
    
    fig = px.imshow(
        pivot_data,
        title=title,
        aspect="auto",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )
    
    return fig
