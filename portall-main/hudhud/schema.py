#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Data Schema Definitions
Schema definitions for data columns and normalization

Author: Hudhud Team
Date: 2024
"""

from typing import List, Dict, Any
import pandas as pd

# Log data columns
COL_LOGS = {
    'id': 'id',
    'name': 'name', 
    'city': 'city',
    'territory': 'territory',
    'status': 'status',
    'created_at': 'created_at',
    'confidence': 'confidence',
    'media_count': 'media_count'
}

# Transaction data columns
COL_TRX = {
    'transaction_id': 'transaction_id',
    'business_id': 'business_id',
    'amount': 'amount',
    'timestamp': 'timestamp',
    'type': 'type',
    'status': 'status'
}

# Standard column mappings
COLUMN_MAPPINGS = {
    'business_name': 'name',
    'business_id': 'id',
    'location': 'city',
    'area': 'territory',
    'approval_status': 'status',
    'date_created': 'created_at',
    'confidence_score': 'confidence',
    'media_files': 'media_count'
}

def normalize_columns(df: pd.DataFrame, column_mapping: Dict[str, str] = None) -> pd.DataFrame:
    """
    Normalize DataFrame column names according to schema
    
    Args:
        df: Input DataFrame
        column_mapping: Optional custom column mapping
        
    Returns:
        DataFrame with normalized columns
    """
    if df is None or df.empty:
        return df
        
    # Use provided mapping or default
    mapping = column_mapping or COLUMN_MAPPINGS
    
    # Create a copy to avoid modifying original
    normalized_df = df.copy()
    
    # Apply column name normalization
    for old_name, new_name in mapping.items():
        if old_name in normalized_df.columns:
            normalized_df = normalized_df.rename(columns={old_name: new_name})
    
    # Ensure standard columns exist with defaults
    for col_name in COL_LOGS.values():
        if col_name not in normalized_df.columns:
            if col_name == 'id':
                normalized_df[col_name] = range(1, len(normalized_df) + 1)
            elif col_name == 'status':
                normalized_df[col_name] = 'Pending'
            elif col_name == 'confidence':
                normalized_df[col_name] = 0.5
            elif col_name == 'media_count':
                normalized_df[col_name] = 0
            elif col_name == 'created_at':
                normalized_df[col_name] = pd.Timestamp.now().strftime('%Y-%m-%d')
            else:
                normalized_df[col_name] = ''
    
    return normalized_df

def validate_schema(df: pd.DataFrame, schema_type: str = 'logs') -> bool:
    """
    Validate DataFrame against schema
    
    Args:
        df: DataFrame to validate
        schema_type: Type of schema ('logs' or 'trx')
        
    Returns:
        True if valid, False otherwise
    """
    if df is None or df.empty:
        return False
        
    required_cols = COL_LOGS if schema_type == 'logs' else COL_TRX
    
    # Check if all required columns exist
    missing_cols = set(required_cols.values()) - set(df.columns)
    
    if missing_cols:
        return False
        
    return True

def get_sample_data(schema_type: str = 'logs', size: int = 10) -> pd.DataFrame:
    """
    Generate sample data for testing
    
    Args:
        schema_type: Type of schema ('logs' or 'trx')
        size: Number of records to generate
        
    Returns:
        DataFrame with sample data
    """
    import random
    from datetime import datetime, timedelta
    
    if schema_type == 'logs':
        cities = ["Riyadh", "Jeddah", "Dammam", "Mecca", "Medina"]
        territories = {
            "Riyadh": ["North", "South", "East", "West", "Central"],
            "Jeddah": ["North", "South", "East", "West"],
            "Dammam": ["North", "South", "East", "West"],
            "Mecca": ["Central", "Outer"],
            "Medina": ["Central", "Outer"]
        }
        
        data = []
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(size):
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
    
    else:  # transactions
        data = []
        start_date = datetime.now() - timedelta(days=7)
        
        for i in range(size):
            data.append({
                "transaction_id": f"TXN{i+1:04d}",
                "business_id": random.randint(1, 100),
                "amount": round(random.uniform(10.0, 1000.0), 2),
                "timestamp": (start_date + timedelta(hours=random.randint(0, 168))).isoformat(),
                "type": random.choice(["Sale", "Refund", "Payment"]),
                "status": random.choice(["Completed", "Pending", "Failed"])
            })
        
        return pd.DataFrame(data)
