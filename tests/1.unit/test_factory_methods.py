#!/usr/bin/env python3
"""
Unit tests for XWEntity factory methods.
"""

import pytest
import tempfile
from pathlib import Path
from exonware.xwmodels import XWEntity
from exonware.xwschema import XWSchema
pytestmark = pytest.mark.xwentity_unit


class TestFactoryMethods:
    """Test factory method functionality."""

    def test_from_dict_basic(self):
        """Test from_dict with basic data."""
        data = {"name": "Alice", "age": 30}
        entity = XWEntity.from_dict(data)
        assert entity.get("name") == "Alice"
        assert entity.get("age") == 30

    def test_from_dict_with_schema(self):
        """Test from_dict with schema."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        })
        data = {"name": "Alice", "age": 30}
        entity = XWEntity.from_dict(data, schema=schema)
        assert entity.schema == schema
        assert entity.get("name") == "Alice"

    def test_from_dict_with_entity_type(self):
        """Test from_dict with entity type."""
        data = {"name": "Alice"}
        entity = XWEntity.from_dict(data, entity_type="user")
        assert entity.type == "user"

    def test_from_dict_invalid_data(self):
        """Test from_dict with invalid data type."""
        with pytest.raises(Exception):  # Should raise XWEntityError
            XWEntity.from_dict("not a dict")

    def test_from_file_json(self):
        """Test from_file with JSON format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump({"name": "Alice", "age": 30}, f)
            temp_path = f.name
        try:
            entity = XWEntity.from_file(temp_path)
            assert entity.get("name") == "Alice"
            assert entity.get("age") == 30
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_from_file_with_format(self):
        """Test from_file with explicit format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump({"name": "Alice"}, f)
            temp_path = f.name
        try:
            entity = XWEntity.from_file(temp_path, format="json")
            assert entity.get("name") == "Alice"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_from_file_nonexistent(self):
        """Test from_file with non-existent file."""
        with pytest.raises(Exception):  # Should raise XWEntityError
            XWEntity.from_file("nonexistent_file.json")

    def test_from_schema_basic(self):
        """Test from_schema with basic schema."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        })
        entity = XWEntity.from_schema(schema)
        assert entity.schema == schema
        assert entity.data is not None

    def test_from_schema_with_initial_data(self):
        """Test from_schema with initial data."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        })
        initial_data = {"name": "Alice"}
        entity = XWEntity.from_schema(schema, initial_data=initial_data)
        assert entity.schema == schema
        assert entity.get("name") == "Alice"

    def test_from_data_with_dict(self):
        """Test from_data with dictionary."""
        data = {"name": "Alice", "age": 30}
        entity = XWEntity.from_data(data)
        assert entity.get("name") == "Alice"
        assert entity.get("age") == 30

    def test_from_data_with_xwdata(self):
        """Test from_data with XWData instance."""
        from exonware.xwdata import XWData
        xwdata = XWData({"name": "Alice", "age": 30})
        entity = XWEntity.from_data(xwdata)
        assert entity.get("name") == "Alice"
        assert entity.get("age") == 30

    def test_from_data_with_schema(self):
        """Test from_data with schema."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        })
        data = {"name": "Alice"}
        entity = XWEntity.from_data(data, schema=schema)
        assert entity.schema == schema
        assert entity.get("name") == "Alice"

    def test_factory_methods_with_config(self):
        """Test factory methods with custom config."""
        from exonware.xwmodels import XWEntityConfig
        config = XWEntityConfig(cache_size=256)
        data = {"name": "Alice"}
        entity = XWEntity.from_dict(data, config=config)
        assert entity._config.cache_size == 256

    def test_factory_methods_with_node_options(self):
        """Test factory methods with node options."""
        data = {"name": "Alice"}
        entity = XWEntity.from_dict(data, node_mode="HASH_MAP")
        assert entity._config.node_mode == "HASH_MAP"
