#!/usr/bin/env python3
"""Architecture smoke tests for current exonware.xwmodels layout."""

import pytest

from exonware.xwmodels import XWEntity


pytestmark = pytest.mark.xwmodels_unit


class TestArchitectureSmoke:
    """Validate that the current package architecture is importable and usable."""

    def test_xwmodels_entity_facade_is_usable(self):
        entity = XWEntity({"name": "architecture"})
        assert entity.get("name") == "architecture"
