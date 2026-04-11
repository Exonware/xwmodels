#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/auth/base.py
Auth Abstract Base Classes for XWEntity
Provides abstract base classes with common helpers for auth implementations.
Implementations are provided by external auth providers that satisfy the contracts.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.12
Generation Date: 27-Jan-2026
"""

from __future__ import annotations
from typing import Any
from exonware.xwsystem import get_logger
from .contracts import (
    IEntityAuth,
    ICollectionAuth,
    IGroupAuth,
)
logger = get_logger(__name__)


class AEntityAuth(IEntityAuth):
    """
    Abstract base class for entity auth implementations.
    Provides common helpers for permission checking patterns,
    role validation, and logging hooks.
    """

    def __init__(self):
        """Initialize abstract entity auth."""
        pass

    def _normalize_permission(self, permission: str) -> str:
        """
        Normalize permission string (helper method).
        Args:
            permission: Permission string
        Returns:
            Normalized permission string
        """
        return permission.lower().strip()

    def _has_role(self, user: Any, role: str) -> bool:
        """
        Check if user has role (helper method).
        Args:
            user: User object/identifier
            role: Role name to check
        Returns:
            True if user has role, False otherwise
        """
        roles = self.get_user_roles(user)
        return role.lower() in [r.lower() for r in roles]


class ACollectionAuth(ICollectionAuth):
    """
    Abstract base class for collection auth implementations.
    Provides common helpers for collection-level permission composition
    and entity auth delegation.
    """

    def __init__(self, entity_auth: IEntityAuth | None = None):
        """
        Initialize abstract collection auth.
        Args:
            entity_auth: Optional entity auth for per-entity operations
        """
        self._entity_auth = entity_auth

    def _check_entity_permissions(
        self,
        collection: Any,
        permission: str,
        user: Any
    ) -> bool:
        """
        Check permissions on all entities in collection (helper method).
        Args:
            collection: Collection instance
            permission: Permission to check
            user: User object/identifier
        Returns:
            True if user has permission on all entities, False otherwise
        """
        if not self._entity_auth:
            return True  # No entity auth means no restriction
        if hasattr(collection, 'list_all'):
            entities = collection.list_all()
        elif hasattr(collection, '_entities'):
            entities = list(collection._entities.values())
        else:
            return True
        return all(
            self._entity_auth.check_permission(entity, permission, user)
            for entity in entities
        )


class AGroupAuth(IGroupAuth):
    """
    Abstract base class for group auth implementations.
    Provides common helpers for group-level permission composition
    and collection/entity auth delegation.
    """

    def __init__(
        self,
        collection_auth: ICollectionAuth | None = None,
        entity_auth: IEntityAuth | None = None
    ):
        """
        Initialize abstract group auth.
        Args:
            collection_auth: Optional collection auth for per-collection operations
            entity_auth: Optional entity auth for per-entity operations
        """
        self._collection_auth = collection_auth
        self._entity_auth = entity_auth

    def _check_collection_permissions(
        self,
        group: Any,
        permission: str,
        user: Any
    ) -> bool:
        """
        Check permissions on all collections in group (helper method).
        Args:
            group: Group instance
            permission: Permission to check
            user: User object/identifier
        Returns:
            True if user has permission on all collections, False otherwise
        """
        if not self._collection_auth:
            return True  # No collection auth means no restriction
        if hasattr(group, 'list_collections'):
            collection_ids = group.list_collections()
            collections = [group.get_collection(cid) for cid in collection_ids if group.get_collection(cid)]
        elif hasattr(group, '_collections'):
            collections = list(group._collections.values())
        else:
            return True
        return all(
            self._collection_auth.check_collection_permission(collection, permission, user)
            for collection in collections
        )
__all__ = [
    "AEntityAuth",
    "ACollectionAuth",
    "AGroupAuth",
]
