#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/group.py
XWGroup Facade - Group Management
This module provides the main public API for entity groups.
A group contains multiple collections and manages their organization
and storage structure.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.6
Generation Date: 08-Nov-2025
"""

from __future__ import annotations
from typing import Any
from pathlib import Path
from datetime import datetime
from exonware.xwsystem import get_logger
from .base import AGroup
from exonware.xwsystem.shared import XWObject
from .contracts import ICollection
from .collection import XWModelCollection
from .defs import EntityType
from .errors import XWEntityError
from .storage.contracts import IGroupStorage
from .auth.contracts import IGroupAuth
logger = get_logger(__name__)


class XWModelGroup(AGroup, XWObject):
    """
    Group of collections with file-based persistence.
    A group contains multiple collections and manages their organization
    and storage structure:
    - base_path/group_id.xwjson (single file containing all collections)
        Example:
        >>> group = XWModelGroup("my_group", base_path=Path("./data"))
        >>> group = XWModelGroup("my_group", title="My Group", description="...", storage=s, auth=a)
        >>> users_collection = group.create_collection("users", User)
        >>> posts_collection = group.create_collection("posts", Post)
        >>> group.save_all()
    """

    def __init__(
        self,
        id: str,  # noqa: A002  # mandatory
        base_path: Path | None = None,
        title: str | None = None,
        description: str | None = None,
        storage: IGroupStorage | None = None,
        auth: IGroupAuth | None = None,
        group: "XWGroup" | None = None,
    ):
        """
        Initialize group.
        Reuses XWObject init for identity (id → object_id).
        Args:
            id: Unique identifier for this group (mandatory)
            base_path: Base path for storage (defaults to current directory)
            title: Optional display title
            description: Optional description
            storage: Optional storage provider (IGroupStorage contract)
            auth: Optional authentication provider (IGroupAuth contract)
            group: Optional parent group (for nested groups)
        """
        if group is not None and base_path is None and hasattr(group, "_base_path"):
            base_path = group._base_path
        if group is not None and storage is None and hasattr(group, "_storage_provider"):
            storage = group._storage_provider
        if group is not None and auth is None and hasattr(group, "_auth_provider"):
            auth = group._auth_provider
        AGroup.__init__(self, id, base_path)
        XWObject.__init__(self, object_id=id)
        self._created_at = datetime.now()
        self._updated_at = self._created_at
        if title:
            self._title = title
        if description:
            self._description = description
        self._storage_provider = storage
        self._auth_provider = auth
        self._subgroups: dict[str, "XWModelGroup"] = {}  # Track subgroups
        self._parent_group = group  # Track parent group
        # Register this group with parent if parent exists
        if group is not None and hasattr(group, "_subgroups"):
            group._subgroups[id] = self
        if storage:
            logger.debug(f"Group '{id}' initialized with storage provider")
        if auth:
            logger.debug(f"Group '{id}' initialized with auth provider")
    @property

    def id(self) -> str:
        """Get the group identifier (XWObject interface)."""
        return self._group_id
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

    def create_collection(
        self,
        id: str,  # noqa: A002  # mandatory
        entity_type: EntityType,
    ) -> XWModelCollection:
        """
        Create a new collection in this group.
        Args:
            id: Unique identifier for the collection (mandatory)
            entity_type: Type of entities in this collection
        Returns:
            XWModelCollection instance
        Raises:
            XWEntityError: If collection already exists
        """
        if id in self._collections:
            raise XWEntityError(f"Collection '{id}' already exists in group '{self._group_id}'")
        collection = XWModelCollection(
            id=id,
            entity_type=entity_type,
            group_id=self._group_id,
            base_path=self._base_path,
        )
        self._collections[id] = collection
        self._update_timestamp()
        logger.info(f"Created collection '{id}' in group '{self._group_id}'")
        return collection

    def create_subgroup(
        self,
        id: str,  # noqa: A002  # mandatory
        title: str | None = None,
        description: str | None = None,
    ) -> "XWModelGroup":
        """
        Create a subgroup within this group.
        Args:
            id: Unique identifier for the subgroup (mandatory)
            title: Optional display title
            description: Optional description
        Returns:
            XWModelGroup instance for the subgroup
        """
        subgroup = XWModelGroup(
            id=id,
            base_path=self._base_path,
            title=title,
            description=description,
            group=self,
            storage=getattr(self, "_storage_provider", None),
            auth=getattr(self, "_auth_provider", None),
        )
        # Track the subgroup
        self._subgroups[id] = subgroup
        logger.info(f"Created subgroup '{id}' in group '{self._group_id}'")
        return subgroup

    def create_group(
        self,
        id: str,  # noqa: A002  # mandatory
        title: str | None = None,
        description: str | None = None,
    ) -> "XWModelGroup":
        """Alias for create_subgroup (API compatibility)."""
        return self.create_subgroup(id=id, title=title, description=description)

    def save_all(self, storage: IGroupStorage | None = None) -> None:
        """
        Save all collections and subgroups recursively.
        Requires IGroupStorage implementation. Uses _storage_provider if storage not passed.
        Args:
            storage: IGroupStorage implementation (uses self._storage_provider if None)
        """
        provider = storage or getattr(self, "_storage_provider", None)
        if provider is None:
            raise XWEntityError(
                "XWGroup.save_all() requires IGroupStorage implementation. "
                "Pass storage= or set group with storage provider."
            )
        provider.save_group(self)

    def load_all(self, storage: IGroupStorage | None = None) -> None:
        """
        Load all collections in this group from storage.
        Requires IGroupStorage implementation. Uses _storage_provider if storage not passed.
        Args:
            storage: IGroupStorage implementation (uses self._storage_provider if None)
        """
        provider = storage or getattr(self, "_storage_provider", None)
        if provider is None:
            raise XWEntityError(
                "XWGroup.load_all() requires IGroupStorage implementation. "
                "Pass storage= or set group with storage provider."
            )
        provider.load_group(self)

    def to_dict(self) -> dict[str, Any]:
        """Export group as dictionary."""
        result: dict[str, Any] = {
            "group_id": self._group_id,
            "base_path": str(self._base_path) if self._base_path else None,
            "collection_count": self.collection_count,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "collections": {
                cid: collection.to_dict() if hasattr(collection, "to_dict") else {"id": cid}
                for cid, collection in self._collections.items()
            },
        }
        if hasattr(self, "_title") and self._title:
            result["title"] = self._title
        if hasattr(self, "_description") and self._description:
            result["description"] = self._description
        return result

    def to_native(self) -> Any:
        """Get group as native representation (XWObject interface)."""
        return self.to_dict()

    def save(self, *args, storage: IGroupStorage | None = None, **kwargs) -> None:
        """Save group to storage (XWObject interface)."""
        self.save_all(storage=storage)

    def load(self, *args, storage: IGroupStorage | None = None, **kwargs) -> None:
        """Load group from storage (XWObject interface)."""
        self.load_all(storage=storage)
# ==============================================================================
# EXPORTS
# ==============================================================================
XWGroup = XWModelGroup
__all__ = [
    "XWModelGroup",
    "XWGroup",
]
