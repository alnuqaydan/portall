#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Configuration Management
Configuration and settings management for the system

Author: Hudhud Team
Date: 2024
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import pytz

@dataclass
class DatabaseConfig:
    """Database settings"""
    host: str = "localhost"
    port: int = 5432
    name: str = "hudhud_kpis"
    user: str = "username"
    password: str = "password"
    ssl_mode: str = "prefer"
    pool_size: int = 10
    max_overflow: int = 20

@dataclass
class APIConfig:
    """API settings"""
    base_url: str = "https://poi.api.hudhud.cloud"
    timeout: int = 30
    retry_attempts: int = 3
    rate_limit: int = 100
    rate_limit_window: int = 60

@dataclass
class CacheConfig:
    """Cache settings"""
    enabled: bool = True
    ttl: int = 3600
    max_size: int = 1000
    backend: str = "memory"  # memory, redis, file
    redis_url: str = "redis://localhost:6379"

@dataclass
class ExportConfig:
    """Export settings"""
    formats: List[str] = None
    batch_size: int = 10000
    directory: str = "data/exports"
    compression: bool = True
    include_metadata: bool = True
    
    def __post_init__(self):
        if self.formats is None:
            self.formats = ["csv", "parquet", "xlsx"]

@dataclass
class NotificationConfig:
    """Notification settings"""
    email_enabled: bool = False
    slack_enabled: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    slack_webhook: str = ""
    slack_channel: str = "#hudhud-kpis"

@dataclass
class SecurityConfig:
    """Security settings"""
    secret_key: str = "your-secret-key-here"
    session_timeout: int = 3600
    max_login_attempts: int = 5
    password_min_length: int = 8
    require_2fa: bool = False

@dataclass
class PerformanceConfig:
    """Performance settings"""
    max_concurrent_requests: int = 10
    request_delay: float = 0.1
    timeout_multiplier: float = 1.5
    batch_processing: bool = True
    memory_limit: str = "2GB"

@dataclass
class LoggingConfig:
    """Logging settings"""
    level: str = "INFO"
    file: str = "data/logs/app.log"
    max_size: str = "10MB"
    backup_count: int = 5
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

@dataclass
class DashConfig:
    """Dash settings"""
    refresh_interval: int = 300000  # 5 minutes in milliseconds
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8050
    suppress_callback_exceptions: bool = True

class Config:
    """Main configuration management for the system"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration"""
        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = config_file or (self.project_root / ".env")
        
        # Default configurations
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.cache = CacheConfig()
        self.export = ExportConfig()
        self.notification = NotificationConfig()
        self.security = SecurityConfig()
        self.performance = PerformanceConfig()
        self.logging = LoggingConfig()
        self.dash = DashConfig()
        
        # Load configurations
        self.load_environment_variables()
        self.load_config_file()
        
    def load_environment_variables(self):
        """Load environment variables"""
        # Database
        if os.getenv("DB_HOST"):
            self.database.host = os.getenv("DB_HOST")
        if os.getenv("DB_PORT"):
            self.database.port = int(os.getenv("DB_PORT"))
        if os.getenv("DB_NAME"):
            self.database.name = os.getenv("DB_NAME")
        if os.getenv("DB_USER"):
            self.database.user = os.getenv("DB_USER")
        if os.getenv("DB_PASSWORD"):
            self.database.password = os.getenv("DB_PASSWORD")
            
        # API
        if os.getenv("API_BASE_URL"):
            self.api.base_url = os.getenv("API_BASE_URL")
        if os.getenv("API_TIMEOUT"):
            self.api.timeout = int(os.getenv("API_TIMEOUT"))
            
        # Cache
        if os.getenv("CACHE_ENABLED"):
            self.cache.enabled = os.getenv("CACHE_ENABLED").lower() == "true"
        if os.getenv("CACHE_TTL"):
            self.cache.ttl = int(os.getenv("CACHE_TTL"))
            
        # Export
        if os.getenv("EXPORT_DIRECTORY"):
            self.export.directory = os.getenv("EXPORT_DIRECTORY")
        if os.getenv("EXPORT_BATCH_SIZE"):
            self.export.batch_size = int(os.getenv("EXPORT_BATCH_SIZE"))
            
        # Security
        if os.getenv("SECRET_KEY"):
            self.security.secret_key = os.getenv("SECRET_KEY")
        if os.getenv("SESSION_TIMEOUT"):
            self.security.session_timeout = int(os.getenv("SESSION_TIMEOUT"))
            
        # Logging
        if os.getenv("LOG_LEVEL"):
            self.logging.level = os.getenv("LOG_LEVEL")
        if os.getenv("LOG_FILE"):
            self.logging.file = os.getenv("LOG_FILE")
            
        # Dash
        if os.getenv("DASH_REFRESH_INTERVAL"):
            self.dash.refresh_interval = int(os.getenv("DASH_REFRESH_INTERVAL"))
        if os.getenv("DASH_DEBUG"):
            self.dash.debug = os.getenv("DASH_DEBUG").lower() == "true"
        if os.getenv("DASH_HOST"):
            self.dash.host = os.getenv("DASH_HOST")
        if os.getenv("DASH_PORT"):
            self.dash.port = int(os.getenv("DASH_PORT"))
    
    def load_config_file(self):
        """Load configuration file"""
        if self.config_file.exists():
            try:
                # Load .env file using python-dotenv
                from dotenv import load_dotenv
                load_dotenv(self.config_file)
                self.load_environment_variables()
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        # Try to get from nested config objects
        keys = key.split('.')
        value = self
        
        try:
            for k in keys:
                value = getattr(value, k)
            return value
        except AttributeError:
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        obj = self
        
        # Navigate to the parent object
        for k in keys[:-1]:
            obj = getattr(obj, k)
        
        # Set the value
        setattr(obj, keys[-1], value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "database": asdict(self.database),
            "api": asdict(self.api),
            "cache": asdict(self.cache),
            "export": asdict(self.export),
            "notification": asdict(self.notification),
            "security": asdict(self.security),
            "performance": asdict(self.performance),
            "logging": asdict(self.logging),
            "dash": asdict(self.dash)
        }
    
    def save_to_env(self, env_file: Optional[str] = None):
        """Save configuration to .env file"""
        if env_file is None:
            env_file = self.config_file
            
        env_content = []
        
        # Database
        env_content.append(f"DB_HOST={self.database.host}")
        env_content.append(f"DB_PORT={self.database.port}")
        env_content.append(f"DB_NAME={self.database.name}")
        env_content.append(f"DB_USER={self.database.user}")
        env_content.append(f"DB_PASSWORD={self.database.password}")
        
        # API
        env_content.append(f"API_BASE_URL={self.api.base_url}")
        env_content.append(f"API_TIMEOUT={self.api.timeout}")
        
        # Cache
        env_content.append(f"CACHE_ENABLED={str(self.cache.enabled).lower()}")
        env_content.append(f"CACHE_TTL={self.cache.ttl}")
        
        # Export
        env_content.append(f"EXPORT_DIRECTORY={self.export.directory}")
        env_content.append(f"EXPORT_BATCH_SIZE={self.export.batch_size}")
        
        # Security
        env_content.append(f"SECRET_KEY={self.security.secret_key}")
        env_content.append(f"SESSION_TIMEOUT={self.security.session_timeout}")
        
        # Logging
        env_content.append(f"LOG_LEVEL={self.logging.level}")
        env_content.append(f"LOG_FILE={self.logging.file}")
        
        # Dash
        env_content.append(f"DASH_REFRESH_INTERVAL={self.dash.refresh_interval}")
        env_content.append(f"DASH_DEBUG={str(self.dash.debug).lower()}")
        env_content.append(f"DASH_HOST={self.dash.host}")
        env_content.append(f"DASH_PORT={self.dash.port}")
        
        # Write to file
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(env_content))
    
    def validate(self) -> bool:
        """Validate configuration"""
        try:
            # Check required fields
            if not self.database.name:
                print("Error: Database name is required")
                return False
                
            if not self.security.secret_key or self.security.secret_key == "your-secret-key-here":
                print("Warning: Using default secret key. Consider changing it for production.")
                
            # Check file paths
            log_file = Path(self.logging.file)
            if not log_file.parent.exists():
                log_file.parent.mkdir(parents=True, exist_ok=True)
                
            export_dir = Path(self.export.directory)
            if not export_dir.exists():
                export_dir.mkdir(parents=True, exist_ok=True)
                
            return True
            
        except Exception as e:
            print(f"Error validating configuration: {e}")
            return False

# Global configuration instance
config = Config()
