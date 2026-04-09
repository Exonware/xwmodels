#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/1.unit/test_collection_group.py
Unit tests for XWModelCollection and XWGroup.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from exonware.xwmodels import (
    XWEntity,
    XWModelCollection,
    XWGroup,
    XWEntityError,
    SimpleFileCollectionStorage,
    SimpleFileGroupStorage,
)
from exonware.xwschema import XWSchema


@pytest.mark.xwmodels_unit
class TestXWModelCollection:
    """Unit tests for XWModelCollection."""

    def test_create_collection(self):
        """Test creating a collection with id and entity_type."""
        coll = XWModelCollection("users", entity_type="entity")
        assert coll.id == "users"
        assert coll.entity_type == "entity"
        assert coll.size == 0

    def test_add_entity(self):
        """Test adding entities to collection."""
        schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}}})
        coll = XWModelCollection("users", entity_type="entity")
        e1 = XWEntity(schema=schema, data={"name": "Alice"})
        e2 = XWEntity(schema=schema, data={"name": "Bob"})
        coll.add(e1)
        coll.add(e2)
        assert coll.size == 2

    def test_remove_entity(self):
        """Test removing entity by id."""
        schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}}})
        coll = XWModelCollection("users", entity_type="entity")
        e = XWEntity(schema=schema, data={"name": "Alice"})
        coll.add(e)
        assert coll.size == 1
        result = coll.remove(e.id)
        assert result is True
        assert coll.size == 0

    def test_find_entities(self):
        """Test finding entities with predicate."""
        schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}, "active": {"type": "boolean"}}})
        coll = XWModelCollection("users", entity_type="entity")
        e1 = XWEntity(schema=schema, data={"name": "Alice", "active": True})
        e2 = XWEntity(schema=schema, data={"name": "Bob", "active": False})
        coll.add(e1)
        coll.add(e2)
        found = coll.find(lambda ent: ent.get("active") is True)
        assert len(found) == 1
        assert found[0].get("name") == "Alice"

    def test_to_dict(self):
        """Test collection to_dict export."""
        schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}}})
        coll = XWModelCollection("users", entity_type="entity")
        e = XWEntity(schema=schema, data={"name": "Alice"})
        coll.add(e)
        d = coll.to_dict()
        assert "collection_id" in d
        assert "entities" in d
        assert len(d["entities"]) == 1

    def test_save_load_roundtrip(self):
        """Test save and load with SimpleFileCollectionStorage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            storage = SimpleFileCollectionStorage()
            schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}}})
            coll1 = XWModelCollection("test", entity_type="entity", base_path=path)
            e = XWEntity(schema=schema, data={"name": "Alice"})
            coll1.add(e)
            coll1.save(storage=storage)
            assert (path / "test.data.xwjson").exists()
            coll2 = XWModelCollection("test", entity_type="entity", base_path=path)
            coll2.load(storage=storage)
            assert len(coll2._entities) == 1


@pytest.mark.xwmodels_unit
class TestXWGroup:
    """Unit tests for XWGroup."""

    def test_create_group(self):
        """Test creating a group with id."""
        group = XWGroup("my_group")
        assert group.id == "my_group"

    def test_create_collection(self):
        """Test creating collection in group."""
        group = XWGroup("my_group")
        coll = group.create_collection("users", entity_type="entity")
        assert coll is not None
        assert coll.id == "users"
        assert "users" in group._collections

    def test_create_subgroup(self):
        """Test creating subgroup."""
        group = XWGroup("parent")
        sub = group.create_subgroup("child", title="Child Group")
        assert sub.id == "child"
        assert "child" in group._subgroups

    def test_create_group_alias(self):
        """Test create_group is alias for create_subgroup."""
        group = XWGroup("parent")
        sub = group.create_group("child")
        assert sub.id == "child"

    def test_duplicate_collection_raises(self):
        """Test duplicate collection id raises error."""
        group = XWGroup("my_group")
        group.create_collection("users", entity_type="entity")
        with pytest.raises(XWEntityError, match="already exists"):
            group.create_collection("users", entity_type="entity")

    def test_to_dict(self):
        """Test group to_dict export."""
        group = XWGroup("my_group")
        schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}}})
        coll = group.create_collection("users", entity_type="entity")
        coll.add(XWEntity(schema=schema, data={"name": "Alice"}))
        d = group.to_dict()
        assert "group_id" in d
        assert "collections" in d
        assert "users" in d["collections"]
