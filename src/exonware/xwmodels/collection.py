#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/collection.py
XWModelCollection - Persistence-aware collection of entities.
This module provides the main public API for entity collections.
A collection is a container that holds multiple entities of the same type.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.13
Generation Date: 08-Nov-2025
"""

from __future__ import annotations
from typing import Any
from pathlib import Path
from datetime import datetime
from exonware.xwsystem import get_logger
from exonware.xwdata import XWData
from .base import ACollection
from exonware.xwsystem.shared import XWObject
from .contracts import IEntity, ICollection
from .defs import EntityType, EntityID
from .errors import XWEntityError
# Import core XWEntity from unified xwentity package (required dependency)
from exonware.xwentity import XWEntity
from .storage.contracts import ICollectionStorage
logger = get_logger(__name__)


class XWModelCollection[TEntity: XWEntity](ACollection[TEntity], XWObject):
    """
    Collection of entities with file-based persistence.
    A collection holds multiple entities of the same type and provides
    operations for managing, querying, and persisting them.
    File structure:
    - group_id/collection_id.data.xwjson (entity data)
    - group_id/collection_id.schemas.xwjson (entity schemas)
    - group_id/collection_id.actions.xwjson (entity actions)
        Example:
        >>> collection = XWModelCollection("users", User, group_id="my_group")
        >>> collection.add(user1)
        >>> collection.add(user2)
        >>> collection.save()
        >>> users = collection.find(lambda u: u.get("status") == "active")
    """

    def __init__(
        self,
        id: str,  # noqa: A002  # mandatory
        entity_type: EntityType,
        group_id: str | None = None,
        base_path: Path | None = None,
    ):
        """
        Initialize collection.
        Reuses XWObject init for identity (id → object_id).
        Args:
            id: Unique identifier for this collection (mandatory)
            entity_type: Type of entities in this collection
            group_id: Optional group identifier this collection belongs to
            base_path: Optional base path for storage (defaults to current directory)
        """
        ACollection.__init__(self, id, entity_type, group_id)
        XWObject.__init__(self, object_id=id)
        # Normalize base_path to relative if it's absolute
        if base_path is None:
            self._base_path = Path.cwd()
        elif base_path.is_absolute():
            try:
                self._base_path = base_path.relative_to(Path.cwd())
            except ValueError:
                # Can't make relative, store as-is but log warning
                logger.warning(
                    f"Base path {base_path} is absolute and cannot be made relative to cwd. "
                    f"This may cause path validation errors."
                )
                self._base_path = base_path
        else:
            # Already relative, store as-is
            self._base_path = base_path
        self._created_at = datetime.now()
        self._updated_at = self._created_at
    @property

    def id(self) -> str:
        """Get the collection identifier (XWObject interface)."""
        return self._collection_id
    @property

    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at
    @property

    def updated_at(self) -> datetime:
        """Get last update timestamp."""
        return self._updated_at

    def _update_timestamp(self) -> None:
        """Update the updated_at timestamp (XWObject helper)."""
        self._updated_at = datetime.now()

    def add(self, entity: TEntity) -> None:
        """Add an entity to the collection."""
        # Call parent implementation for validation
        ACollection.add(self, entity)
        # Update timestamp
        self._update_timestamp()

    def remove(self, entity_id: EntityID) -> bool:
        """Remove an entity from the collection by ID."""
        result = ACollection.remove(self, entity_id)
        if result:
            self._update_timestamp()
        return result

    def clear(self) -> None:
        """Clear all entities from the collection."""
        ACollection.clear(self)
        self._update_timestamp()

    def save(self, base_path: Path | None = None, storage: ICollectionStorage | None = None) -> None:
        """
        Save collection to storage.
        Requires ICollectionStorage implementation. Use storage.save_collection() directly.
        Args:
            base_path: Optional base path override
            storage: ICollectionStorage implementation (required)
        """
        if storage is None:
            raise XWEntityError(
                "XWModelCollection.save() requires ICollectionStorage implementation. "
                "Use storage.save_collection() directly."
            )
        storage.save_collection(self, base_path=base_path)

    def load(self, base_path: Path | None = None, storage: ICollectionStorage | None = None) -> None:
        """
        Load collection from storage.
        Requires ICollectionStorage implementation. Use storage.load_collection() directly.
        Args:
            base_path: Optional base path override
            storage: ICollectionStorage implementation (required)
        Raises:
            XWEntityError: If storage is not provided or collection cannot be loaded
        """
        if storage is None:
            raise XWEntityError(
                "XWModelCollection.load() requires ICollectionStorage implementation. "
                "Use storage.load_collection() directly."
            )
        storage.load_collection(self, base_path=base_path)

    def to_dict(self) -> dict[str, Any]:
        """Export collection as dictionary."""
        return {
            "collection_id": self._collection_id,
            "group_id": self._group_id,
            "entity_type": self._entity_type,
            "size": self.size,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "entities": [
                entity.to_native() if hasattr(entity, "to_native") else (entity.to_dict() if hasattr(entity, "to_dict") else entity)
                for entity in self._entities.values()
            ]
        }

    def to_native(self) -> Any:
        """Get collection as native representation (XWObject interface)."""
        return self.to_dict()


# ==============================================================================
# EXPORTS
# ==============================================================================
__all__ = [
    "XWModelCollection",
]
