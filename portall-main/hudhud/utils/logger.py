#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Logging Management
Logging and record management for the system

Author: Hudhud Team
Date: 2024
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import os

def setup_logger(
    log_file: Optional[str] = None,
    level: str = "INFO",
    max_size: str = "10MB",
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup logging system
    
    Args:
        log_file: Log file path
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        max_size: Maximum file size
        backup_count: Number of backup files
        format_string: Log format
    
    Returns:
        Logger instance
    """
    
    # Create logger
    logger = logging.getLogger("hudhud")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Default format
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Parse max_size
            max_bytes = parse_size(max_size)
            
            # Rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            print(f"Warning: Could not setup file logging to {log_file}: {e}")
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

def parse_size(size_string: str) -> int:
    """
    Parse file size from text
    
    Args:
        size_string: Size text (e.g., "10MB", "1GB")
    
    Returns:
        Size in bytes
    """
    size_string = size_string.upper().strip()
    
    # Default to MB if no unit specified
    if size_string.isdigit():
        size_string += "MB"
    
    # Parse units
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    for unit, multiplier in units.items():
        if size_string.endswith(unit):
            try:
                number = float(size_string[:-len(unit)])
                return int(number * multiplier)
            except ValueError:
                break
    
    # Default to 10MB if parsing fails
    print(f"Warning: Could not parse size '{size_string}', using 10MB default")
    return 10 * 1024**2

def get_logger(name: str = None) -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"hudhud.{name}")
    return logging.getLogger("hudhud")

def log_function_call(func):
    """
    Decorator to log function calls
    
    Usage:
        @log_function_call
        def my_function():
            pass
    """
    def wrapper(*args, **kwargs):
        logger = get_logger("function_calls")
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} failed with error: {e}")
            raise
    
    return wrapper

def log_performance(func):
    """
    Decorator to log function performance
    
    Usage:
        @log_performance
        def my_function():
            pass
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger("performance")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    
    return wrapper

class LogContext:
    """
    Log context manager for complex operations
    
    Usage:
        with LogContext("data_processing"):
            # operations
            pass
    """
    
    def __init__(self, operation_name: str, logger: Optional[logging.Logger] = None):
        self.operation_name = operation_name
        self.logger = logger or get_logger("context")
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        execution_time = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info(f"Operation {self.operation_name} completed successfully in {execution_time:.4f} seconds")
        else:
            self.logger.error(f"Operation {self.operation_name} failed after {execution_time:.4f} seconds: {exc_val}")
        
        return False  # Don't suppress exceptions

# Convenience functions
def info(message: str, logger_name: str = None):
    """Log info message"""
    get_logger(logger_name).info(message)

def warning(message: str, logger_name: str = None):
    """Log warning message"""
    get_logger(logger_name).warning(message)

def error(message: str, logger_name: str = None):
    """Log error message"""
    get_logger(logger_name).error(message)

def debug(message: str, logger_name: str = None):
    """Log debug message"""
    get_logger(logger_name).debug(message)

def critical(message: str, logger_name: str = None):
    """Log critical message"""
    get_logger(logger_name).critical(message)
