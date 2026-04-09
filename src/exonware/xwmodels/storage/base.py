#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/storage/base.py
Storage Abstract Base Classes for XWEntity
Provides abstract base classes with common helpers for storage implementations.
Implementations are provided by external storage providers that satisfy the contracts.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.10
Generation Date: 27-Jan-2026
"""

from __future__ import annotations
from typing import Any
from exonware.xwsystem import get_logger
from .contracts import (
    IEntityStorage,
    ICollectionStorage,
    IGroupStorage,
)
logger = get_logger(__name__)


class AEntityStorage(IEntityStorage):
    """
    Abstract base class for entity storage implementations.
    Provides common helpers for converting entities to dicts/native,
    shared error handling, and logging hooks.
    """

    def __init__(self):
        """Initialize abstract entity storage."""
        pass

    def _entity_to_dict(self, entity: Any) -> dict[str, Any]:
        """
        Convert entity to dictionary (helper method).
        Args:
            entity: Entity instance
        Returns:
            Entity as dictionary
        """
        if hasattr(entity, 'to_dict'):
            return entity.to_dict()
        elif hasattr(entity, 'to_native'):
            return entity.to_native()
        else:
            logger.warning(f"Entity {type(entity).__name__} does not support to_dict/to_native")
            return {}

    def _entity_from_dict(self, entity_class: type, data: dict[str, Any]) -> Any:
        """
        Create entity from dictionary (helper method).
        Args:
            entity_class: Entity class to instantiate
            data: Entity data dictionary
        Returns:
            Entity instance
        """
        if hasattr(entity_class, 'from_dict'):
            return entity_class.from_dict(data)
        elif hasattr(entity_class, 'from_native'):
            return entity_class.from_native(data)
        else:
            raise ValueError(f"Entity class {entity_class.__name__} does not support from_dict/from_native")


class ACollectionStorage(ICollectionStorage):
    """
    Abstract base class for collection storage implementations.
    Provides common helpers for iterating collections and composing
    entity storage for per-entity operations.
    """

    def __init__(self, entity_storage: IEntityStorage | None = None):
        """
        Initialize abstract collection storage.
        Args:
            entity_storage: Optional entity storage for per-entity operations
        """
        self._entity_storage = entity_storage

    def _iterate_entities(self, collection: Any) -> list[Any]:
        """
        Iterate over entities in collection (helper method).
        Args:
            collection: Collection instance
        Returns:
            List of entities
        """
        if hasattr(collection, 'list_all'):
            return collection.list_all()
        elif hasattr(collection, '_entities'):
            return list(collection._entities.values())
        else:
            logger.warning(f"Collection {type(collection).__name__} does not support list_all")
            return []


class AGroupStorage(IGroupStorage):
    """
    Abstract base class for group storage implementations.
    Provides common helpers for traversing group/collection hierarchies
    and composing collection/entity storage.
    """

    def __init__(
        self,
        collection_storage: ICollectionStorage | None = None,
        entity_storage: IEntityStorage | None = None
    ):
        """
        Initialize abstract group storage.
        Args:
            collection_storage: Optional collection storage for per-collection operations
            entity_storage: Optional entity storage for per-entity operations
        """
        self._collection_storage = collection_storage
        self._entity_storage = entity_storage

    def _iterate_collections(self, group: Any) -> list[Any]:
        """
        Iterate over collections in group (helper method).
        Args:
            group: Group instance
        Returns:
            List of collections
        """
        if hasattr(group, 'list_collections'):
            collection_ids = group.list_collections()
            return [group.get_collection(cid) for cid in collection_ids if group.get_collection(cid)]
        elif hasattr(group, '_collections'):
            return list(group._collections.values())
        else:
            logger.warning(f"Group {type(group).__name__} does not support list_collections")
            return []

    def _iterate_subgroups(self, group: Any) -> list[Any]:
        """
        Iterate over subgroups (helper method).
        Args:
            group: Group instance
        Returns:
            List of subgroups
        """
        if hasattr(group, '_subgroups'):
            return list(group._subgroups.values())
        else:
            return []
__all__ = [
    "AEntityStorage",
    "ACollectionStorage",
    "AGroupStorage",
]
