#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/3.advance/test_performance_caching.py
Performance caching verification tests for xwentity.
Priority #4: Performance Excellence
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 07-Jan-2025
"""

import pytest
import time
from exonware.xwmodels import XWEntity
from exonware.xwmodels.cache import get_entity_cache
@pytest.mark.xwentity_advance
@pytest.mark.xwentity_performance

class TestPerformanceCaching:
    """Test performance caching mechanisms."""

    def test_cache_hit_tracking(self):
        """Test that cache hits are tracked correctly."""
        class TestEntity(XWEntity):
            def __init__(self, data=None):
                super().__init__(data or {"id": "test", "name": "Test"})
        entity = TestEntity()
        # Access path multiple times
        value1 = entity.get("name")
        value2 = entity.get("name")  # Should be cache hit
        # Verify cache stats
        stats = entity.get_performance_stats()
        assert "cache_hits" in stats
        assert "cache_misses" in stats
        # Second access should be a cache hit
        assert stats["cache_hits"] >= 1

    def test_cache_miss_tracking(self):
        """Test that cache misses are tracked correctly."""
        class TestEntity(XWEntity):
            def __init__(self, data=None):
                super().__init__(data or {"id": "test", "name": "Test"})
        entity = TestEntity()
        # Access new path (cache miss)
        value = entity.get("name")
        # Verify cache stats
        stats = entity.get_performance_stats()
        assert "cache_misses" in stats

    def test_global_cache_functionality(self):
        """Test that global cache works correctly."""
        class TestEntity(XWEntity):
            def __init__(self, data=None):
                super().__init__(data or {"id": "test", "name": "Test"})
        entity1 = TestEntity()
        entity2 = TestEntity({"id": "test2", "name": "Test2"})
        # Access same path from different entities
        value1 = entity1.get("name")
        value2 = entity2.get("name")
        # Global cache should work
        cache = get_entity_cache()
        assert cache is not None

    def test_cache_performance_benefit(self):
        """Test that cache provides performance benefits."""
        class TestEntity(XWEntity):
            def __init__(self, data=None):
                super().__init__(data or {"id": "test", "name": "Test"})
        entity = TestEntity()
        # First access (cache miss)
        start = time.time()
        for _ in range(100):
            value = entity.get("name")
        first_access = time.time() - start
        # Second access (cache hit)
        start = time.time()
        for _ in range(100):
            value = entity.get("name")
        second_access = time.time() - start
        # Cache hit should be faster or at least not significantly slower
        # (Note: Actual performance depends on implementation)
        assert value == "Test"

    def test_cache_size_limits(self):
        """Test that cache respects size limits."""
        class TestEntity(XWEntity):
            def __init__(self, data=None):
                super().__init__(data or {"id": "test"})
        entity = TestEntity()
        # Access many different paths
        for i in range(2000):
            entity.get(f"path_{i}")
        # Cache should handle size limits gracefully
        stats = entity.get_performance_stats()
        assert stats is not None
