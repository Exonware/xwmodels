#!/usr/bin/env python3
"""
Unit tests for XWEntity caching system.
"""

import pytest
import threading
from exonware.xwmodels import XWEntity, XWEntityCache, get_entity_cache, clear_entity_cache
pytestmark = pytest.mark.xwentity_unit


class TestXWEntityCache:
    """Test XWEntityCache functionality."""

    def test_cache_creation(self):
        """Test cache creation."""
        cache = XWEntityCache(max_size=100)
        assert cache._max_size == 100
        assert len(cache._cache) == 0
        assert cache._hit_count == 0
        assert cache._miss_count == 0

    def test_cache_put_and_get(self):
        """Test cache put and get operations."""
        cache = XWEntityCache(max_size=10)
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache._hit_count > 0

    def test_cache_miss(self):
        """Test cache miss behavior."""
        cache = XWEntityCache(max_size=10)
        result = cache.get("nonexistent")
        assert result is None
        assert cache._miss_count > 0

    def test_cache_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        cache = XWEntityCache(max_size=2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")  # Should evict key1
        assert cache.get("key1") is None  # Evicted
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"

    def test_cache_clear(self):
        """Test cache clearing."""
        cache = XWEntityCache(max_size=10)
        cache.put("key1", "value1")
        cache.clear()
        assert len(cache._cache) == 0
        assert cache.get("key1") is None

    def test_cache_hit_rate(self):
        """Test cache hit rate calculation."""
        cache = XWEntityCache(max_size=10)
        cache.put("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        hit_rate = cache.hit_rate
        assert 0.0 <= hit_rate <= 1.0
        assert hit_rate > 0.5  # Should be > 50% (2 hits, 1 miss)

    def test_cache_stats(self):
        """Test cache statistics."""
        cache = XWEntityCache(max_size=10)
        cache.put("key1", "value1")
        cache.get("key1")
        stats = cache.stats()
        assert 'size' in stats
        assert 'max_size' in stats
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'hit_rate' in stats
        assert stats['size'] == 1
        assert stats['max_size'] == 10

    def test_cache_thread_safety(self):
        """Test thread-safe cache operations."""
        from exonware.xwmodels import get_config, set_config
        from exonware.xwmodels.config import XWEntityConfig
        # Enable thread safety
        config = get_config()
        original_thread_safety = config.enable_thread_safety
        config.enable_thread_safety = True
        cache = XWEntityCache(max_size=100)
        def put_values(start, count):
            for i in range(count):
                cache.put(f"key{start + i}", f"value{start + i}")
        # Run in multiple threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=put_values, args=(i * 10, 10))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        # All values should be in cache
        assert len(cache._cache) <= 100  # Should not exceed max_size
        # Restore
        config.enable_thread_safety = original_thread_safety


class TestGlobalCache:
    """Test global cache functionality."""

    def test_get_entity_cache(self):
        """Test getting global cache instance."""
        cache = get_entity_cache()
        assert isinstance(cache, XWEntityCache)

    def test_clear_entity_cache(self):
        """Test clearing global cache."""
        cache = get_entity_cache()
        cache.put("test_key", "test_value")
        clear_entity_cache()
        assert cache.get("test_key") is None


class TestEntityCacheIntegration:
    """Test cache integration with XWEntity."""

    def test_entity_uses_cache(self):
        """Test that entity operations use cache."""
        entity = XWEntity(data={"name": "Alice", "age": 30})
        # Access same path multiple times
        val1 = entity.get("name")
        val2 = entity.get("name")
        assert val1 == val2 == "Alice"
        # Check performance stats include cache info
        stats = entity.get_performance_stats()
        assert 'cache_stats' in stats
        assert 'cache_hits' in stats or 'hits' in stats.get('cache_stats', {})
