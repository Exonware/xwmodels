#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/0.core/conftest.py
Core-specific test fixtures for xwmodels.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create temporary directory for file-based tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_schema():
    """Create a sample schema for testing."""
    from exonware.xwschema import XWSchema
    return XWSchema({
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
        },
        "required": ["name"],
    })


@pytest.fixture
def sample_entity(sample_schema):
    """Create a sample XWEntity for testing."""
    from exonware.xwmodels import XWEntity
    return XWEntity(schema=sample_schema, data={"name": "Alice", "age": 30})


@pytest.fixture
def file_collection_storage():
    """Create SimpleFileCollectionStorage for tests."""
    from exonware.xwmodels import SimpleFileCollectionStorage
    return SimpleFileCollectionStorage()


@pytest.fixture
def file_group_storage():
    """Create SimpleFileGroupStorage for tests."""
    from exonware.xwmodels import SimpleFileGroupStorage
    return SimpleFileGroupStorage()
