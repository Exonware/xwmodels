#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/auth/contracts.py
Auth Contracts for XWEntity
Defines interfaces for entity, collection, and group authorization operations.
Implementations are provided by external auth providers that satisfy these contracts.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.6
Generation Date: 27-Jan-2026
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
# Use protocols/interfaces to avoid circular imports
# These will be type hints only - actual XWEntity types imported at runtime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from exonware.xwentity import XWEntity
    from ..collection import XWModelCollection
    from ..group import XWGroup


class IEntityAuth(ABC):
    """
    Auth contract for XWEntity authorization.
    Implementations are provided by external auth providers that satisfy this contract.
    """
    @abstractmethod

    def check_permission(
        self,
        entity: "XWEntity",
        permission: str,
        user: Any
    ) -> bool:
        """
        Check if user has permission on entity.
        Args:
            entity: Entity instance
            permission: Permission to check (e.g., "read", "write", "delete")
            user: User object/identifier
        Returns:
            True if user has permission, False otherwise
        """
        pass
    @abstractmethod

    def validate_access(
        self,
        entity: "XWEntity",
        user: Any
    ) -> bool:
        """
        Validate if user has access to entity.
        Args:
            entity: Entity instance
            user: User object/identifier
        Returns:
            True if user has access, False otherwise
        """
        pass
    @abstractmethod

    def get_user_roles(
        self,
        user: Any
    ) -> list[str]:
        """
        Get roles for user.
        Args:
            user: User object/identifier
        Returns:
            List of role names
        """
        pass


class ICollectionAuth(ABC):
    """
    Auth contract for XWModelCollection authorization.
    Implementations are provided by external auth providers that satisfy this contract.
    """
    @abstractmethod

    def check_collection_permission(
        self,
        collection: "XWModelCollection",
        permission: str,
        user: Any
    ) -> bool:
        """
        Check if user has permission on collection.
        Args:
            collection: Collection instance
            permission: Permission to check (e.g., "read", "write", "delete")
            user: User object/identifier
        Returns:
            True if user has permission, False otherwise
        """
        pass
    @abstractmethod

    def validate_collection_access(
        self,
        collection: "XWModelCollection",
        user: Any
    ) -> bool:
        """
        Validate if user has access to collection.
        Args:
            collection: Collection instance
            user: User object/identifier
        Returns:
            True if user has access, False otherwise
        """
        pass


class IGroupAuth(ABC):
    """
    Auth contract for XWGroup authorization.
    Implementations are provided by external auth providers that satisfy this contract.
    """
    @abstractmethod

    def check_group_permission(
        self,
        group: "XWGroup",
        permission: str,
        user: Any
    ) -> bool:
        """
        Check if user has permission on group.
        Args:
            group: Group instance
            permission: Permission to check (e.g., "read", "write", "delete")
            user: User object/identifier
        Returns:
            True if user has permission, False otherwise
        """
        pass
    @abstractmethod

    def validate_group_access(
        self,
        group: "XWGroup",
        user: Any
    ) -> bool:
        """
        Validate if user has access to group.
        Args:
            group: Group instance
            user: User object/identifier
        Returns:
            True if user has access, False otherwise
        """
        pass
__all__ = [
    "IEntityAuth",
    "ICollectionAuth",
    "IGroupAuth",
]
