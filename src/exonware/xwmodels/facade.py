#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/facade.py
XWEntity Facade - Main Public API
This module provides the main public API for xwentity following GUIDE_DEV.md facade pattern.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.9
Generation Date: 07-Jan-2025
"""
# Re-export main facade class from xwmodels compatibility layer

from .entity_compat import XWEntity
from .collection import XWModelCollection
from .group import XWGroup
from .config import XWEntityConfig, get_config
from .errors import (
    XWEntityError,
    XWEntityValidationError,
    XWEntityStateError,
    XWEntityActionError,
)
# Main facade class
__all__ = [
    "XWEntity",
    "XWModelCollection",
    "XWGroup",
    "XWEntityConfig",
    "get_config",
    "XWEntityError",
    "XWEntityValidationError",
    "XWEntityStateError",
    "XWEntityActionError",
]
