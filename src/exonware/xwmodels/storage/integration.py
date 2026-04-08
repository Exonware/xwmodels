#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/storage/integration.py
XWEntity Storage Integration
This module provides entity-specific storage operations for groups and collections.
These operations know how to handle XWGroup, XWModelCollection, and XWEntity instances.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.8
Generation Date: 27-Jan-2026
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Any

from exonware.xwaction import XWAction
from exonware.xwschema import XWSchema
from exonware.xwentity import XWEntity
from exonware.xwsystem import get_logger

from .contracts import ICollectionStorage, IGroupStorage

if TYPE_CHECKING:
    from ..collection import XWModelCollection
    from ..group import XWGroup


def _get_group() -> type:
    from ..group import XWGroup
    return XWGroup


def _get_collection() -> type:
    from ..collection import XWModelCollection
    return XWModelCollection


logger = get_logger(__name__)


class XWEntityStorageGroup:
    """
    XWGroup wrapper with storage connection support.
    This class wraps an XWGroup and adds storage connection functionality,
    allowing groups to automatically save collections to storage.
    This is an entity-specific operation that knows about XWGroup structure.
    Example:
        >>> from exonware.xwmodels.storage.integration import XWEntityStorageGroup
        >>> # Get IGroupStorage implementation from your storage provider
        >>> storage = your_storage_provider.get_group_storage()  # IGroupStorage instance
        >>> group = XWEntityStorageGroup("Chat App", storage=storage)
    """

    def __init__(
        self,
        id: str,  # noqa: A002  # mandatory
        storage: IGroupStorage | None = None,
        auth: Any | None = None,  # IGroupAuth
        base_path: Path | None = None,
        title: str | None = None,
        description: str | None = None,
        group: Any | None = None,
    ):
        """
        Initialize storage-enabled group.
        Args:
            id: Group identifier (mandatory)
            storage: Optional IGroupStorage implementation
            auth: Optional IGroupAuth implementation
            base_path: Optional base path (used if no storage)
            title: Optional display title
            description: Optional group description
            group: Optional XWGroup instance (if not provided, creates a new XWGroup)
        """
        XWGroup = _get_group()
        if group is None:
            self._group = XWGroup(
                id,
                base_path=base_path,
                title=title,
                description=description,
                storage=storage,
                auth=auth,
            )
        else:
            self._group = group
            # Update storage/auth if provided
            if storage:
                self._group._storage_provider = storage
            if auth:
                self._group._auth_provider = auth
        self._storage = storage
        self._auth = auth
        if storage:
            logger.info(f"Attached storage to group '{id}'")
    @property

    def id(self) -> str:
        """Get group ID."""
        return self._group.group_id
    @property

    def group(self) -> Any:
        """Get underlying XWGroup instance."""
        return self._group
    @property

    def storage(self) -> IGroupStorage | None:
        """Get storage provider."""
        return self._storage

    def create_collection(
        self,
        id: str,  # noqa: A002  # mandatory
        entity_type: str | type,
        entity_class: type | None = None,
        storage: ICollectionStorage | None = None,
    ) -> Any:
        """
        Create collection with auto-save support.
        This is an entity-specific operation that knows about XWModelCollection structure.
        Args:
            id: Collection identifier (mandatory)
            entity_type: Entity type string or class
            entity_class: Optional entity class
            storage: Optional ICollectionStorage implementation
        Returns:
            XWModelCollection instance with auto-save support
        """
        return create_entity_storage_collection(
            id,
            entity_type,
            self._group,
            entity_class,
            storage=storage,
        )

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to underlying group."""
        return getattr(self._group, name)


def create_entity_storage_group(
    id: str,  # noqa: A002  # mandatory
    storage: IGroupStorage | None = None,
    auth: Any | None = None,  # IGroupAuth
    base_path: Path | None = None,
    title: str | None = None,
    description: str | None = None,
    group: Any | None = None,
) -> XWEntityStorageGroup:
    """
    Create XWGroup with storage connection support.
    This function creates an XWEntityStorageGroup that wraps an XWGroup and adds
    storage connection functionality.
    This is an entity-specific operation that knows about XWGroup structure.
    Args:
        id: Group identifier (mandatory)
        storage: Optional IGroupStorage implementation
        auth: Optional IGroupAuth implementation
        base_path: Optional base path (used if no storage)
        title: Optional display title
        description: Optional group description
        group: Optional XWGroup instance
    Returns:
        XWEntityStorageGroup instance with storage support
    """
    return XWEntityStorageGroup(
        id,
        storage=storage,
        auth=auth,
        base_path=base_path,
        title=title,
        description=description,
        group=group,
    )
@XWAction(
    profile="command",
    audit=True,
    idempotent=True,
    in_types={
        "id": XWSchema({"type": "string"}),
        "entity_type": XWSchema({"anyOf": [{"type": "string"}, {"type": "any"}]}),
        "group": XWSchema({"type": "any"}),
        "entity_class": XWSchema({"anyOf": [{"type": "any"}, {"type": "null"}]}),
        "storage": XWSchema({"anyOf": [{"type": "any"}, {"type": "null"}]}),
    }
)

def create_entity_storage_collection(
    id: str,  # noqa: A002  # mandatory
    entity_type: str | type,
    group: Any,
    entity_class: type | None = None,
    storage: ICollectionStorage | None = None,
) -> Any:
    """
    Create XWModelCollection with automatic storage on add.
    This function creates an XWModelCollection that automatically saves
    entities when they are added.
    This is an entity-specific operation that knows about:
    - XWModelCollection structure and methods
    - XWEntity structure (to_native, to_dict, id, etc.)
    - How to integrate with ICollectionStorage
    REUSES xwaction for command profile with audit logging and idempotency.
    Args:
        id: Collection identifier (mandatory)
        entity_type: Entity type string or class
        group: XWGroup instance (may have storage connection)
        entity_class: Optional entity class (for type checking)
        storage: Optional ICollectionStorage implementation
    Returns:
        XWModelCollection instance with auto-save support
    """
    if isinstance(entity_type, type):
        entity_type_str = entity_type.__name__.lower()
    else:
        entity_type_str = str(entity_type)
    # Create collection using XWGroup's method
    # Note: XWGroup.create_collection only accepts id and entity_type, not entity_class
    collection = group.create_collection(id, entity_type_str)
    # Determine which storage to use
    collection_storage = storage
    if collection_storage is None and hasattr(group, '_storage_provider') and group._storage_provider:
        # Try to get collection storage from group storage
        # IGroupStorage implementations should provide a way to get ICollectionStorage
        group_storage = group._storage_provider
        # Store the group storage reference
        # IGroupStorage implementations should provide collection storage access
        collection._storage_provider = group_storage
        logger.debug(f"Collection '{id}' will use group's storage provider")
    # If collection storage provided, enable auto-save
    if collection_storage:
        # Store storage reference
        collection._storage_provider = collection_storage
        # Wrap the add method to auto-save
        original_add = collection.add
        def add_with_save(entity: XWEntity) -> None:
            """Add entity and save collection to storage."""
            try:
                # Add entity first (synchronous operation)
                original_add(entity)
                # Save collection using storage provider (synchronous)
                # Note: ICollectionStorage.save_collection is synchronous
                collection_storage.save_collection(collection, base_path=group._base_path)
                logger.debug(f"Auto-saved collection '{id}' to storage")
            except Exception as e:
                logger.error(f"Failed to auto-save collection to storage: {e}")
                # Don't raise - entity was already added, just log the error
                # This ensures the add operation succeeds even if save fails
        collection.add = add_with_save
        logger.info(f"Enabled auto-save for collection '{id}'")
    return collection
__all__ = [
    "XWEntityStorageGroup",
    "create_entity_storage_group",
    "create_entity_storage_collection",
]
