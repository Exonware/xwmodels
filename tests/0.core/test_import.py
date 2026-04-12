#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/0.core/test_import.py
Core Import Tests
This module tests that all core imports work correctly.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.1
Generation Date: 08-Nov-2025
"""

import pytest


def test_import_main_classes():
    """Test that main classes can be imported."""
    from exonware.xwmodels import XWEntity, AEntity
    assert XWEntity is not None
    assert AEntity is not None


def test_import_interfaces():
    """Test that interfaces can be imported."""
    from exonware.xwmodels import (
        IEntity,
        IEntityActions,
        IEntityState,
        IEntitySerialization,
    )
    assert IEntity is not None
    assert IEntityActions is not None
    assert IEntityState is not None
    assert IEntitySerialization is not None


def test_import_config():
    """Test that configuration can be imported."""
    from exonware.xwmodels import XWEntityConfig, get_config, set_config
    assert XWEntityConfig is not None
    assert get_config is not None
    assert set_config is not None


def test_import_defs():
    """Test that type definitions can be imported."""
    from exonware.xwmodels import (
        EntityState,
        EntityType,
        EntityID,
        EntityData,
        DEFAULT_ENTITY_TYPE,
        DEFAULT_STATE,
    )
    assert EntityState is not None
    assert DEFAULT_ENTITY_TYPE is not None
    assert DEFAULT_STATE is not None


def test_import_errors():
    """Test that errors can be imported."""
    from exonware.xwmodels import (
        XWEntityError,
        XWEntityValidationError,
        XWEntityStateError,
        XWEntityActionError,
        XWEntityNotFoundError,
    )
    assert XWEntityError is not None
    assert XWEntityValidationError is not None
    assert XWEntityStateError is not None
    assert XWEntityActionError is not None
    assert XWEntityNotFoundError is not None


def test_import_version():
    """Test that version can be imported."""
    from exonware.xwmodels import (
        __version__,
        get_version,
        get_version_info,
    )
    assert __version__ is not None
    assert get_version is not None
    assert get_version_info is not None


def test_import_all():
    """Test that __all__ exports are available."""
    import exonware.xwmodels as xwm
    assert hasattr(xwm, "__all__")
    assert isinstance(xwm.__all__, list)
    assert len(xwm.__all__) > 0
    assert "XWEntity" in xwm.__all__
    assert "XWModelCollection" in xwm.__all__
    assert "XWGroup" in xwm.__all__
