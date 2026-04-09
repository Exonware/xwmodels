#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/2.integration/test_end_to_end.py
Integration tests for xwmodels end-to-end flows.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
"""

import tempfile
from pathlib import Path

import pytest

from exonware.xwmodels import (
    XWEntity,
    XWModelCollection,
    XWGroup,
    SimpleFileCollectionStorage,
    SimpleFileGroupStorage,
)
from exonware.xwschema import XWSchema
from exonware.xwaction import XWAction

pytestmark = pytest.mark.xwmodels_integration


class UserEntity(XWEntity):
    @XWAction(profile="query", roles=["*"])

    def get_name(self) -> str:
        return self.get("name")


def test_entity_schema_validation_and_action_execution_roundtrip():
    schema = XWSchema(
        {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
    )
    e = UserEntity(schema=schema, data={"name": "Alice"})
    assert e.validate() is True
    result = e.execute_action("get_name")
    # Core may return the raw value or an ActionResult-like object
    if isinstance(result, str):
        assert result == "Alice"
    else:
        assert getattr(result, "success", False) is True
        assert getattr(result, "data", None) == "Alice"


def test_group_collection_entity_flow_with_storage():
    """Integration: create group, add collection, add entities, save."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        storage = SimpleFileGroupStorage(SimpleFileCollectionStorage())
        group = XWGroup("test_group", base_path=path, storage=storage)
        schema = XWSchema({"type": "object", "properties": {"name": {"type": "string"}}})
        coll = group.create_collection("users", entity_type="user")
        e1 = XWEntity(schema=schema, data={"name": "Alice"}, entity_type="user")
        e2 = XWEntity(schema=schema, data={"name": "Bob"}, entity_type="user")
        coll.add(e1)
        coll.add(e2)
        assert coll.size == 2
        group.save_all()
        assert (path / "test_group.xwjson").exists()
        assert (path / "test_group" / "users.data.xwjson").exists()
