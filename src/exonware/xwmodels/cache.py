#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/cache.py
XWEntity Caching System
This module provides thread-safe caching for entity operations with performance
monitoring. Migrated from MIGRAT xEntity implementation.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.11
Generation Date: 08-Nov-2025
"""

import threading
from collections import OrderedDict
from typing import Any
from exonware.xwsystem import get_logger
from .config import get_config
logger = get_logger(__name__)


class XWEntityCache:
    """
    A thread-safe cache for entity operations with performance monitoring.
    Uses LRU (Least Recently Used) eviction policy when cache size is exceeded.
    Tracks cache hits and misses for performance analysis.
    """
    __slots__ = ('_cache', '_lock', '_max_size', '_hit_count', '_miss_count')

    def __init__(self, max_size: int = 1024):
        """
        Initialize entity cache.
        Args:
            max_size: Maximum number of items to cache (default: 1024)
        """
        self._cache: OrderedDict[str, Any] = OrderedDict()
        config = get_config()
        self._lock = threading.RLock() if config.enable_thread_safety else None
        self._max_size = max_size
        self._hit_count = 0
        self._miss_count = 0

    def get(self, key: str) -> Any | None:
        """
        Get value from cache.
        Args:
            key: Cache key
        Returns:
            Cached value or None if not found
        """
        if self._lock:
            with self._lock:
                return self._get_impl(key)
        return self._get_impl(key)

    def _get_impl(self, key: str) -> Any | None:
        """Internal cache get implementation."""
        if key in self._cache:
            self._hit_count += 1
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return self._cache[key]
        self._miss_count += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """
        Put value in cache.
        Args:
            key: Cache key
            value: Value to cache
        """
        if self._lock:
            with self._lock:
                self._put_impl(key, value)
        else:
            self._put_impl(key, value)

    def _put_impl(self, key: str, value: Any) -> None:
        """Internal cache put implementation."""
        self._cache[key] = value
        self._cache.move_to_end(key)
        # Evict oldest item if cache is full
        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

    def clear(self) -> None:
        """Clear the entire cache."""
        if self._lock:
            with self._lock:
                self._cache.clear()
        else:
            self._cache.clear()

    def clear_by_prefix(self, prefix: str) -> int:
        """
        Clear cache entries that start with the given prefix.
        Args:
            prefix: Prefix to match (e.g., "get:entity-id:")
        Returns:
            Number of entries cleared
        """
        if self._lock:
            with self._lock:
                return self._clear_by_prefix_impl(prefix)
        return self._clear_by_prefix_impl(prefix)

    def _clear_by_prefix_impl(self, prefix: str) -> int:
        """Internal prefix-based clear implementation."""
        keys_to_remove = [key for key in self._cache.keys() if key.startswith(prefix)]
        for key in keys_to_remove:
            del self._cache[key]
        return len(keys_to_remove)
    @property

    def hit_rate(self) -> float:
        """
        Get cache hit rate.
        Returns:
            Hit rate as float between 0.0 and 1.0
        """
        total = self._hit_count + self._miss_count
        return self._hit_count / total if total > 0 else 0.0

    def stats(self) -> dict[str, int | float]:
        """
        Get cache statistics.
        Returns:
            Dictionary with cache statistics
        """
        return {
            'size': len(self._cache),
            'max_size': self._max_size,
            'hits': self._hit_count,
            'misses': self._miss_count,
            'hit_rate': self.hit_rate
        }
# ==============================================================================
# GLOBAL CACHE INSTANCE
# ==============================================================================
_entity_cache_instance: XWEntityCache | None = None


def get_entity_cache() -> XWEntityCache:
    """
    Get global entity cache instance.
    Returns:
        Global XWEntityCache instance
    """
    global _entity_cache_instance
    if _entity_cache_instance is None:
        config = get_config()
        _entity_cache_instance = XWEntityCache(config.cache_size)
    return _entity_cache_instance


def clear_entity_cache() -> None:
    """Clear the global entity cache."""
    global _entity_cache_instance
    if _entity_cache_instance is not None:
        _entity_cache_instance.clear()
# ==============================================================================
# EXPORTS
# ==============================================================================
__all__ = [
    "XWEntityCache",
    "get_entity_cache",
    "clear_entity_cache",
]
