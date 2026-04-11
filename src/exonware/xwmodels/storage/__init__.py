#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/storage/__init__.py
XWModels Storage Contracts and Implementations
This module provides storage contracts and abstract base classes for entity persistence.
Storage implementations are provided by external storage providers that satisfy these contracts.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.12
Generation Date: 27-Jan-2026
"""

from .contracts import (
    IEntityStorage,
    ICollectionStorage,
    IGroupStorage,
)
from .base import (
    AEntityStorage,
    ACollectionStorage,
    AGroupStorage,
)
from .integration import (
    XWEntityStorageGroup,
    create_entity_storage_group,
    create_entity_storage_collection,
)
from .file_storage import (
    SimpleFileCollectionStorage,
    SimpleFileGroupStorage,
)
__all__ = [
    "IEntityStorage",
    "ICollectionStorage",
    "IGroupStorage",
    "AEntityStorage",
    "ACollectionStorage",
    "AGroupStorage",
    "XWEntityStorageGroup",
    "create_entity_storage_group",
    "create_entity_storage_collection",
    "SimpleFileCollectionStorage",
    "SimpleFileGroupStorage",
]
