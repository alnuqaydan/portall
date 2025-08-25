#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Data Loading and Management
Data loading and management for the system

Author: Hudhud Team
Date: 2024
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import logging
from datetime import datetime, timedelta
import json
import sqlite3
import os

from .logger import get_logger, LogContext
from ..schema import COL_LOGS, COL_TRX, normalize_columns

logger = get_logger("data_loader")

class DataLoader:
    """
    Data loading and management manager
    """
    
    def __init__(self, config):
        """Initialize data manager"""
        self.config = config
        self.project_root = Path(config.project_root)
        self.data_dir = self.project_root / "data"
        self.cache_dir = self.data_dir / "cache"
        self.input_dir = self.data_dir / "input"
        
        # Ensure directories exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.input_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache for loaded data
        self._cache = {}
        self._cache_timestamps = {}
        
    def load_logs_data(self, force_reload: bool = False) -> Optional[pd.DataFrame]:
        """
        Load logs data
        
        Args:
            force_reload: Force reload data
            
        Returns:
            DataFrame with data or None if failed
        """
        with LogContext("load_logs_data"):
            try:
                # Check cache first
                if not force_reload and "logs" in self._cache:
                    cache_age = datetime.now() - self._cache_timestamps.get("logs", datetime.min)
                    if cache_age.total_seconds() < self.config.cache.ttl:
                        logger.info("Using cached logs data")
                        return self._cache["logs"].copy()
                
                # Try to load from CSV files
                df = self._load_logs_from_csv()
                if df is not None and not df.empty:
                    # Normalize columns
                    df = normalize_columns(df, COL_LOGS)
                    
                    # Add derived fields
                    df = self._add_derived_fields_logs(df)
                    
                    # Cache the data
                    self._cache["logs"] = df.copy()
                    self._cache_timestamps["logs"] = datetime.now()
                    
                    logger.info(f"Successfully loaded {len(df)} logs records")
                    return df
                
                # Try to load from database
                df = self._load_logs_from_db()
                if df is not None and not df.empty:
                    # Normalize columns
                    df = normalize_columns(df, COL_LOGS)
                    
                    # Add derived fields
                    df = self._add_derived_fields_logs(df)
                    
                    # Cache the data
                    self._cache["logs"] = df.copy()
                    self._cache_timestamps["logs"] = datetime.now()
                    
                    logger.info(f"Successfully loaded {len(df)} logs records from database")
                    return df
                
                logger.warning("No logs data found")
                return None
                
            except Exception as e:
                logger.error(f"Error loading logs data: {e}")
                return None
    
    def load_transactions_data(self, force_reload: bool = False) -> Optional[pd.DataFrame]:
        """
        Load transactions data
        
        Args:
            force_reload: Force reload data
            
        Returns:
            DataFrame with data or None if failed
        """
        with LogContext("load_transactions_data"):
            try:
                # Check cache first
                if not force_reload and "transactions" in self._cache:
                    cache_age = datetime.now() - self._cache_timestamps.get("transactions", datetime.min)
                    if cache_age.total_seconds() < self.config.cache.ttl:
                        logger.info("Using cached transactions data")
                        return self._cache["transactions"].copy()
                
                # Try to load from CSV files
                df = self._load_transactions_from_csv()
                if df is not None and not df.empty:
                    # Normalize columns
                    df = normalize_columns(df, COL_TRX)
                    
                    # Add derived fields
                    df = self._add_derived_fields_transactions(df)
                    
                    # Cache the data
                    self._cache["transactions"] = df.copy()
                    self._cache_timestamps["transactions"] = datetime.now()
                    
                    logger.info(f"Successfully loaded {len(df)} transaction records")
                    return df
                
                # Try to load from database
                df = self._load_transactions_from_db()
                if df is not None and not df.empty:
                    # Normalize columns
                    df = normalize_columns(df, COL_TRX)
                    
                    # Add derived fields
                    df = self._add_derived_fields_transactions(df)
                    
                    # Cache the data
                    self._cache["transactions"] = df.copy()
                    self._cache_timestamps["transactions"] = datetime.now()
                    
                    logger.info(f"Successfully loaded {len(df)} transaction records from database")
                    return df
                
                logger.warning("No transactions data found")
                return None
                
            except Exception as e:
                logger.error(f"Error loading transactions data: {e}")
                return None
    
    def _load_logs_from_csv(self) -> Optional[pd.DataFrame]:
        """Load logs data from CSV files"""
        try:
            csv_files = list(self.input_dir.glob("*logs*.csv"))
            if not csv_files:
                return None
            
            # Load and combine all CSV files
            dfs = []
            for csv_file in csv_files:
                logger.info(f"Loading logs from {csv_file}")
                df = pd.read_csv(csv_file)
                dfs.append(df)
            
            if not dfs:
                return None
            
            # Combine all dataframes
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Convert date columns
            if "created_at" in combined_df.columns:
                combined_df["created_at"] = pd.to_datetime(combined_df["created_at"], errors="coerce")
            
            return combined_df
            
        except Exception as e:
            logger.error(f"Error loading logs from CSV: {e}")
            return None
    
    def _load_transactions_from_csv(self) -> Optional[pd.DataFrame]:
        """Load transactions data from CSV files"""
        try:
            csv_files = list(self.input_dir.glob("*trx*.csv")) + list(self.input_dir.glob("*poi*.csv"))
            if not csv_files:
                return None
            
            # Load and combine all CSV files
            dfs = []
            for csv_file in csv_files:
                logger.info(f"Loading transactions from {csv_file}")
                df = pd.read_csv(csv_file)
                dfs.append(df)
            
            if not dfs:
                return None
            
            # Combine all dataframes
            combined_df = pd.concat(dfs, ignore_index=True)
            
            return combined_df
            
        except Exception as e:
            logger.error(f"Error loading transactions from CSV: {e}")
            return None
    
    def _load_logs_from_db(self) -> Optional[pd.DataFrame]:
        """Load logs data from database"""
        try:
            # Look for SQLite database files
            db_files = list(self.project_root.glob("*.db")) + list(self.data_dir.glob("*.db"))
            
            for db_file in db_files:
                try:
                    logger.info(f"Trying to load logs from database: {db_file}")
                    
                    # Try to connect and query
                    conn = sqlite3.connect(db_file)
                    
                    # Check if logs table exists
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
                    
                    if "collected_pois" in tables["name"].values:
                        # Load from collected_pois table
                        query = "SELECT * FROM collected_pois"
                        df = pd.read_sql_query(query, conn)
                        conn.close()
                        
                        if not df.empty:
                            # Map columns to our schema
                            column_mapping = {
                                "id": "id",
                                "transaction_id": "transaction_id",
                                "review_status": "review_status",
                                "created_at": "created_at",
                                "created_by": "created_by",
                                "name_ar": "name_ar",
                                "name_en": "name_en",
                                "latitude": "latitude",
                                "longitude": "longitude",
                                "operation": "operation"
                            }
                            
                            df = df.rename(columns=column_mapping)
                            return df
                    
                    conn.close()
                    
                except Exception as e:
                    logger.debug(f"Could not load from {db_file}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error loading logs from database: {e}")
            return None
    
    def _load_transactions_from_db(self) -> Optional[pd.DataFrame]:
        """Load transactions data from database"""
        try:
            # Look for SQLite database files
            db_files = list(self.project_root.glob("*.db")) + list(self.data_dir.glob("*.db"))
            
            for db_file in db_files:
                try:
                    logger.info(f"Trying to load transactions from database: {db_file}")
                    
                    # Try to connect and query
                    conn = sqlite3.connect(db_file)
                    
                    # Check if transactions table exists
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
                    
                    if "collected_pois" in tables["name"].values:
                        # Load from collected_pois table (this contains transaction data)
                        query = "SELECT * FROM collected_pois"
                        df = pd.read_sql_query(query, conn)
                        conn.close()
                        
                        if not df.empty:
                            # Map columns to our schema
                            column_mapping = {
                                "id": "poi_id",
                                "name_ar": "name_ar",
                                "name_en": "name_en",
                                "latitude": "latitude",
                                "longitude": "longitude"
                            }
                            
                            df = df.rename(columns=column_mapping)
                            
                            # Add default values for missing columns
                            df["city_ar"] = "Unknown"
                            df["city_en"] = "Unknown"
                            df["district"] = "Unknown"
                            df["category"] = "Unknown"
                            df["confidence"] = 1.0
                            df["media_count"] = 0
                            
                            return df
                    
                    conn.close()
                    
                except Exception as e:
                    logger.debug(f"Could not load from {db_file}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error loading transactions from database: {e}")
            return None
    
    def _add_derived_fields_logs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived fields to logs data"""
        try:
            df = df.copy()
            
            # Add operation flags
            if "operation" in df.columns:
                df["New"] = (df["operation"] == "create").astype(int)
                df["Updated"] = (df["operation"] == "update").astype(int)
                df["Deleted"] = (df["operation"] == "delete").astype(int)
            
            # Add date fields
            if "created_at" in df.columns:
                df["date"] = pd.to_datetime(df["created_at"]).dt.date
                df["hour"] = pd.to_datetime(df["created_at"]).dt.hour
                df["day_of_week"] = pd.to_datetime(df["created_at"]).dt.day_name()
            
            # Add location fields
            if "latitude" in df.columns and "longitude" in df.columns:
                df["has_location"] = (df["latitude"].notna() & df["longitude"].notna()).astype(int)
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding derived fields to logs: {e}")
            return df
    
    def _add_derived_fields_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived fields to transactions data"""
        try:
            df = df.copy()
            
            # Add location fields
            if "latitude" in df.columns and "longitude" in df.columns:
                df["has_location"] = (df["latitude"].notna() & df["longitude"].notna()).astype(int)
            
            # Add category fields
            if "category" in df.columns:
                df["category_group"] = df["category"].fillna("Unknown")
            
            # Add confidence fields
            if "confidence" in df.columns:
                df["confidence_level"] = pd.cut(
                    df["confidence"],
                    bins=[0, 0.5, 0.8, 1.0],
                    labels=["Low", "Medium", "High"],
                    include_lowest=True
                )
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding derived fields to transactions: {e}")
            return df
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get data summary"""
        try:
            logs_df = self.load_logs_data()
            trx_df = self.load_transactions_data()
            
            summary = {
                "logs": {
                    "total_records": len(logs_df) if logs_df is not None else 0,
                    "columns": list(logs_df.columns) if logs_df is not None else [],
                    "date_range": None
                },
                "transactions": {
                    "total_records": len(trx_df) if trx_df is not None else 0,
                    "columns": list(trx_df.columns) if trx_df is not None else [],
                    "categories": None
                },
                "last_updated": datetime.now().isoformat()
            }
            
            # Add date range for logs
            if logs_df is not None and "created_at" in logs_df.columns:
                dates = pd.to_datetime(logs_df["created_at"], errors="coerce").dropna()
                if not dates.empty:
                    summary["logs"]["date_range"] = {
                        "start": dates.min().isoformat(),
                        "end": dates.max().isoformat()
                    }
            
            # Add categories for transactions
            if trx_df is not None and "category" in trx_df.columns:
                categories = trx_df["category"].value_counts().head(10).to_dict()
                summary["transactions"]["categories"] = categories
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting data summary: {e}")
            return {"error": str(e)}
    
    def clear_cache(self):
        """Clear cache"""
        self._cache.clear()
        self._cache_timestamps.clear()
        logger.info("Data cache cleared")
    
    def reload_all_data(self):
        """Reload all data"""
        logger.info("Reloading all data...")
        self.clear_cache()
        
        logs_df = self.load_logs_data(force_reload=True)
        trx_df = self.load_transactions_data(force_reload=True)
        
        if logs_df is not None or trx_df is not None:
            logger.info("Data reload completed successfully")
        else:
            logger.warning("No data could be loaded during reload")
