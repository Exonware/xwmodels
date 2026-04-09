#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/auth/__init__.py
XWEntity Auth Contracts and Base Classes
This module provides auth contracts and abstract base classes for entity authorization.
Auth implementations are provided by external auth providers that satisfy these contracts.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.10
Generation Date: 27-Jan-2026
"""

from .contracts import (
    IEntityAuth,
    ICollectionAuth,
    IGroupAuth,
)
from .base import (
    AEntityAuth,
    ACollectionAuth,
    AGroupAuth,
)
__all__ = [
    "IEntityAuth",
    "ICollectionAuth",
    "IGroupAuth",
    "AEntityAuth",
    "ACollectionAuth",
    "AGroupAuth",
]
