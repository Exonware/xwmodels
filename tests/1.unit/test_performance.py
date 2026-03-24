#!/usr/bin/env python3
"""
Unit tests for XWEntity performance optimizations.
"""

import pytest
from exonware.xwmodels import XWEntity, PerformanceMode
pytestmark = pytest.mark.xwentity_unit


class TestPerformanceOptimization:
    """Test performance optimization methods."""

    def test_optimize_for_access(self):
        """Test optimize_for_access method."""
        entity = XWEntity(data={"name": "Alice", "age": 30})
        result = entity.optimize_for_access()
        assert result is entity  # Should return self for chaining
        # Should pre-cache schema
        assert hasattr(entity, '_schema_cache') or entity._schema_cache is None

    def test_optimize_for_validation(self):
        """Test optimize_for_validation method."""
        from exonware.xwschema import XWSchema
        schema = XWSchema({
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        })
        entity = XWEntity(schema=schema, data={"name": "Alice", "age": 30})
        result = entity.optimize_for_validation()
        assert result is entity
        # Should cache schema
        assert hasattr(entity, '_schema_cache')

    def test_optimize_memory(self):
        """Test optimize_memory method."""
        entity = XWEntity(data={"name": "Alice", "age": 30})
        # Add some cache entries
        entity._cache["test"] = "value"
        result = entity.optimize_memory()
        assert result is entity
        # Cache should be cleared
        assert len(entity._cache) == 0

    def test_get_memory_usage(self):
        """Test get_memory_usage method."""
        entity = XWEntity(data={"name": "Alice", "age": 30})
        usage = entity.get_memory_usage()
        assert isinstance(usage, int)
        assert usage > 0

    def test_get_performance_stats(self):
        """Test get_performance_stats method."""
        entity = XWEntity(data={"name": "Alice", "age": 30})
        # Perform some operations
        entity.get("name")
        entity.get("age")
        stats = entity.get_performance_stats()
        assert isinstance(stats, dict)
        assert 'access_count' in stats
        assert 'validation_count' in stats
        assert 'cache_hits' in stats
        assert 'cache_misses' in stats
        assert 'cache_stats' in stats
        assert stats['access_count'] >= 2


class TestPerformanceModes:
    """Test different performance modes."""

    def test_performance_mode_enum(self):
        """Test PerformanceMode enum."""
        assert PerformanceMode.PERFORMANCE.value == "performance"
        assert PerformanceMode.MEMORY.value == "memory"
        assert PerformanceMode.BALANCED.value == "balanced"
        assert PerformanceMode.AUTO.value == "auto"

    def test_performance_mode_config(self):
        """Test performance mode in config."""
        from exonware.xwmodels import get_config, set_config
        from exonware.xwmodels.config import XWEntityConfig
        config = get_config()
        original_mode = config.performance_mode
        config.performance_mode = PerformanceMode.PERFORMANCE
        assert config.performance_mode == PerformanceMode.PERFORMANCE
        config.performance_mode = PerformanceMode.MEMORY
        assert config.performance_mode == PerformanceMode.MEMORY
        # Restore
        config.performance_mode = original_mode
