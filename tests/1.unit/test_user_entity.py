#!/usr/bin/env python3
"""User-entity smoke tests for the current xwmodels facade."""

import pytest

from exonware.xwmodels import XWEntity


pytestmark = pytest.mark.xwmodels_unit


class TestUserEntitySmoke:
    """Basic user-entity behaviors expected by downstream callers."""

    def test_user_entity_data_first_constructor(self):
        entity = XWEntity({"id": "user_1", "name": "Alice"})
        assert entity.get("id") == "user_1"
        assert entity.get("name") == "Alice"
