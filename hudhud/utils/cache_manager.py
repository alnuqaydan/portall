#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hudhud KPI System - Cache Management
Cache management for the system

Author: Hudhud Team
Date: 2024
"""

import json
import pickle
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Union
from datetime import datetime, timedelta
import logging
import os

from .logger import get_logger

logger = get_logger("cache_manager")

class CacheManager:
    """
    Cache management manager for the system
    """
    
    def __init__(self, config):
        """Initialize cache manager"""
        self.config = config
        self.project_root = Path(config.project_root)
        self.cache_dir = self.project_root / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache
        self._memory_cache = {}
        self._memory_timestamps = {}
        
        # Cache configuration
        self.enabled = config.cache.enabled
        self.ttl = config.cache.ttl
        self.max_size = config.cache.max_size
        self.backend = config.cache.backend
        
        logger.info(f"Cache manager initialized with backend: {self.backend}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache
        
        Args:
            key: Value key
            default: Default value
            
        Returns:
            Stored value or default value
        """
        if not self.enabled:
            return default
        
        try:
            # Try memory cache first
            if key in self._memory_cache:
                if self._is_valid(key):
                    logger.debug(f"Cache hit (memory): {key}")
                    return self._memory_cache[key]
                else:
                    # Remove expired key
                    del self._memory_cache[key]
                    del self._memory_timestamps[key]
            
            # Try file cache
            if self.backend in ["file", "hybrid"]:
                value = self._get_from_file(key)
                if value is not None:
                    # Store in memory cache
                    self._memory_cache[key] = value
                    self._memory_timestamps[key] = datetime.now()
                    logger.debug(f"Cache hit (file): {key}")
                    return value
            
            logger.debug(f"Cache miss: {key}")
            return default
            
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Store value in cache
        
        Args:
            key: Value key
            value: Value to store
            ttl: Time to live (in seconds)
            
        Returns:
            True if stored successfully
        """
        if not self.enabled:
            return False
        
        try:
            # Set TTL
            if ttl is None:
                ttl = self.ttl
            
            # Store in memory cache
            self._memory_cache[key] = value
            self._memory_timestamps[key] = datetime.now()
            
            # Store in file cache if enabled
            if self.backend in ["file", "hybrid"]:
                self._set_to_file(key, value, ttl)
            
            # Check cache size limit
            self._enforce_size_limit()
            
            logger.debug(f"Stored in cache: {key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        
        Args:
            key: Value key
            
        Returns:
            True if deleted successfully
        """
        try:
            # Remove from memory cache
            if key in self._memory_cache:
                del self._memory_cache[key]
                del self._memory_timestamps[key]
            
            # Remove from file cache
            if self.backend in ["file", "hybrid"]:
                self._delete_from_file(key)
            
            logger.debug(f"Deleted from cache: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear(self) -> bool:
        """
        Clear all cache
        
        Returns:
            True if cleared successfully
        """
        try:
            # Clear memory cache
            self._memory_cache.clear()
            self._memory_timestamps.clear()
            
            # Clear file cache
            if self.backend in ["file", "hybrid"]:
                self._clear_file_cache()
            
            logger.info("Cache cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache
        
        Args:
            key: Key to search
            
        Returns:
            True if key exists
        """
        if not self.enabled:
            return False
        
        try:
            # Check memory cache
            if key in self._memory_cache:
                return self._is_valid(key)
            
            # Check file cache
            if self.backend in ["file", "hybrid"]:
                return self._exists_in_file(key)
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking cache existence: {e}")
            return False
    
    def get_keys(self, pattern: str = "*") -> list:
        """
        Get list of keys
        
        Args:
            pattern: Search pattern
            
        Returns:
            List of keys
        """
        try:
            keys = []
            
            # Get from memory cache
            keys.extend(list(self._memory_cache.keys()))
            
            # Get from file cache
            if self.backend in ["file", "hybrid"]:
                file_keys = self._get_file_keys(pattern)
                keys.extend(file_keys)
            
            # Remove duplicates and filter by pattern
            unique_keys = list(set(keys))
            if pattern != "*":
                import fnmatch
                unique_keys = [k for k in unique_keys if fnmatch.fnmatch(k, pattern)]
            
            return unique_keys
            
        except Exception as e:
            logger.error(f"Error getting cache keys: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            memory_size = len(self._memory_cache)
            file_size = 0
            
            if self.backend in ["file", "hybrid"]:
                file_size = self._get_file_cache_size()
            
            # Calculate memory usage
            memory_usage = 0
            for key, value in self._memory_cache.items():
                try:
                    memory_usage += len(pickle.dumps(value))
                except:
                    memory_usage += 100  # Estimate
            
            stats = {
                "enabled": self.enabled,
                "backend": self.backend,
                "memory_items": memory_size,
                "memory_usage_bytes": memory_usage,
                "file_items": file_size,
                "total_items": memory_size + file_size,
                "ttl_seconds": self.ttl,
                "max_size": self.max_size
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}
    
    def _is_valid(self, key: str) -> bool:
        """Check if key is valid in memory"""
        if key not in self._memory_timestamps:
            return False
        
        timestamp = self._memory_timestamps[key]
        age = datetime.now() - timestamp
        
        return age.total_seconds() < self.ttl
    
    def _enforce_size_limit(self):
        """Enforce cache size limit"""
        if len(self._memory_cache) <= self.max_size:
            return
        
        # Remove oldest items
        sorted_keys = sorted(
            self._memory_timestamps.keys(),
            key=lambda k: self._memory_timestamps[k]
        )
        
        keys_to_remove = sorted_keys[:len(self._memory_cache) - self.max_size]
        
        for key in keys_to_remove:
            del self._memory_cache[key]
            del self._memory_timestamps[key]
        
        logger.debug(f"Removed {len(keys_to_remove)} old cache items")
    
    def _get_cache_file_path(self, key: str) -> Path:
        """Get cache file path"""
        # Create a safe filename from the key
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.cache"
    
    def _set_to_file(self, key: str, value: Any, ttl: int):
        """Store value in file"""
        try:
            cache_file = self._get_cache_file_path(key)
            
            # Prepare cache data
            cache_data = {
                "key": key,
                "value": value,
                "timestamp": datetime.now().isoformat(),
                "ttl": ttl
            }
            
            # Serialize and save
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
                
        except Exception as e:
            logger.error(f"Error setting file cache: {e}")
    
    def _get_from_file(self, key: str) -> Optional[Any]:
        """Get value from file"""
        try:
            cache_file = self._get_cache_file_path(key)
            
            if not cache_file.exists():
                return None
            
            # Load and deserialize
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check if expired
            timestamp = datetime.fromisoformat(cache_data["timestamp"])
            age = datetime.now() - timestamp
            
            if age.total_seconds() > cache_data["ttl"]:
                # Remove expired file
                cache_file.unlink()
                return None
            
            return cache_data["value"]
            
        except Exception as e:
            logger.error(f"Error getting from file cache: {e}")
            return None
    
    def _delete_from_file(self, key: str):
        """Delete cache file"""
        try:
            cache_file = self._get_cache_file_path(key)
            if cache_file.exists():
                cache_file.unlink()
        except Exception as e:
            logger.error(f"Error deleting file cache: {e}")
    
    def _exists_in_file(self, key: str) -> bool:
        """Check if key exists in file"""
        try:
            cache_file = self._get_cache_file_path(key)
            if not cache_file.exists():
                return False
            
            # Check if expired
            cache_data = self._get_from_file(key)
            return cache_data is not None
            
        except Exception as e:
            logger.error(f"Error checking file cache existence: {e}")
            return False
    
    def _get_file_keys(self, pattern: str = "*") -> list:
        """Get list of file keys"""
        try:
            keys = []
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        cache_data = pickle.load(f)
                    
                    # Check if expired
                    timestamp = datetime.fromisoformat(cache_data["timestamp"])
                    age = datetime.now() - timestamp
                    
                    if age.total_seconds() <= cache_data["ttl"]:
                        keys.append(cache_data["key"])
                    else:
                        # Remove expired file
                        cache_file.unlink()
                        
                except Exception as e:
                    logger.debug(f"Error reading cache file {cache_file}: {e}")
                    continue
            
            return keys
            
        except Exception as e:
            logger.error(f"Error getting file cache keys: {e}")
            return []
    
    def _get_file_cache_size(self) -> int:
        """Get file cache size"""
        try:
            count = 0
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        cache_data = pickle.load(f)
                    
                    # Check if expired
                    timestamp = datetime.fromisoformat(cache_data["timestamp"])
                    age = datetime.now() - timestamp
                    
                    if age.total_seconds() <= cache_data["ttl"]:
                        count += 1
                    else:
                        # Remove expired file
                        cache_file.unlink()
                        
                except Exception as e:
                    logger.debug(f"Error reading cache file {cache_file}: {e}")
                    continue
            
            return count
            
        except Exception as e:
            logger.error(f"Error getting file cache size: {e}")
            return 0
    
    def _clear_file_cache(self):
        """Clear file cache"""
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    cache_file.unlink()
                except Exception as e:
                    logger.debug(f"Error deleting cache file {cache_file}: {e}")
                    
        except Exception as e:
            logger.error(f"Error clearing file cache: {e}")
    
    def cleanup_expired(self):
        """Clean up expired items"""
        try:
            # Clean memory cache
            expired_keys = [
                key for key in self._memory_cache.keys()
                if not self._is_valid(key)
            ]
            
            for key in expired_keys:
                del self._memory_cache[key]
                del self._memory_timestamps[key]
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired memory cache items")
            
            # Clean file cache
            if self.backend in ["file", "hybrid"]:
                self._get_file_keys()  # This will clean expired files
                
        except Exception as e:
            logger.error(f"Error cleaning up expired cache: {e}")
