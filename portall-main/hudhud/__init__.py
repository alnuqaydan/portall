#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Main Package
Field Survey Data Collection and Analysis System

Author: Hudhud Team
Date: 2024
"""

__version__ = "1.0.0"
__author__ = "Hudhud Team"
__description__ = "Field Survey Data Collection and Analysis System"

# Import main components
from .utils.config import Config
from .utils.logger import setup_logger, get_logger
from .utils.data_loader import DataLoader
from .utils.cache_manager import CacheManager

from .components.layout import create_layout
from .components.navigation import create_navigation
from .components.filters import create_filters
from .components.ui_components import create_metric_card, create_chart_card, create_data_table

from .schema import COL_LOGS, COL_TRX, normalize_columns, validate_schema, get_sample_data

__all__ = [
    "Config",
    "setup_logger", 
    "get_logger",
    "DataLoader",
    "CacheManager",
    "create_layout",
    "create_navigation", 
    "create_filters",
    "create_metric_card",
    "create_chart_card",
    "create_data_table",
    "COL_LOGS",
    "COL_TRX", 
    "normalize_columns",
    "validate_schema",
    "get_sample_data"
]
