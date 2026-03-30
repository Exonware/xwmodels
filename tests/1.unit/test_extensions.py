#!/usr/bin/env python3
"""
Unit tests for XWEntity extension system.
"""

import pytest
from exonware.xwmodels import XWEntity
pytestmark = pytest.mark.xwentity_unit


class TestExtensionSystem:
    """Test extension system functionality."""

    def test_register_extension(self):
        """Test registering an extension."""
        entity = XWEntity(data={"name": "Alice"})
        class TestExtension:
            def test_method(self):
                return "test"
        result = entity.register_extension("test_ext", TestExtension())
        assert result is entity  # Should return self for chaining
        assert entity.has_extension("test_ext")

    def test_get_extension(self):
        """Test getting an extension."""
        entity = XWEntity(data={"name": "Alice"})
        ext_obj = {"data": "test"}
        entity.register_extension("test_ext", ext_obj)
        retrieved = entity.get_extension("test_ext")
        assert retrieved == ext_obj

    def test_get_nonexistent_extension(self):
        """Test getting non-existent extension."""
        entity = XWEntity(data={"name": "Alice"})
        result = entity.get_extension("nonexistent")
        assert result is None

    def test_has_extension(self):
        """Test checking if extension exists."""
        entity = XWEntity(data={"name": "Alice"})
        assert not entity.has_extension("test_ext")
        entity.register_extension("test_ext", "value")
        assert entity.has_extension("test_ext")

    def test_list_extensions(self):
        """Test listing all extensions."""
        entity = XWEntity(data={"name": "Alice"})
        entity.register_extension("ext1", "value1")
        entity.register_extension("ext2", "value2")
        entity.register_extension("ext3", "value3")
        extensions = entity.list_extensions()
        assert isinstance(extensions, list)
        assert "ext1" in extensions
        assert "ext2" in extensions
        assert "ext3" in extensions
        assert len(extensions) == 3

    def test_remove_extension(self):
        """Test removing an extension."""
        entity = XWEntity(data={"name": "Alice"})
        entity.register_extension("test_ext", "value")
        assert entity.has_extension("test_ext")
        result = entity.remove_extension("test_ext")
        assert result is True
        assert not entity.has_extension("test_ext")

    def test_remove_nonexistent_extension(self):
        """Test removing non-existent extension."""
        entity = XWEntity(data={"name": "Alice"})
        result = entity.remove_extension("nonexistent")
        assert result is False

    def test_has_extension_type(self):
        """Test checking for extension type."""
        entity = XWEntity(data={"name": "Alice"})
        class TestExtension:
            pass
        class AnotherExtension:
            pass
        entity.register_extension("test1", TestExtension())
        entity.register_extension("test2", AnotherExtension())
        assert entity.has_extension_type("TestExtension")
        assert entity.has_extension_type("AnotherExtension")
        assert not entity.has_extension_type("NonExistentExtension")

    def test_extension_chaining(self):
        """Test extension method chaining."""
        entity = XWEntity(data={"name": "Alice"})
        result = (
            entity
            .register_extension("ext1", "value1")
            .register_extension("ext2", "value2")
            .register_extension("ext3", "value3")
        )
        assert result is entity
        assert len(entity.list_extensions()) == 3
