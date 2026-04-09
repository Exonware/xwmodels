#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/storage/contracts.py
Storage Contracts for XWEntity
Defines interfaces for entity, collection, and group storage operations.
Implementations are provided by external storage providers that satisfy these contracts.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.9
Generation Date: 27-Jan-2026
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Literal
from pathlib import Path
# Use protocols/interfaces to avoid circular imports
# These will be type hints only - actual XWEntity types imported at runtime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from exonware.xwentity import XWEntity
    from ..collection import XWModelCollection
    from ..group import XWGroup


class IEntityStorage(ABC):
    """
    Storage contract for XWEntity persistence.
    Implementations are provided by external storage providers that satisfy this contract.
    """
    @abstractmethod

    def save_entity(
        self,
        entity: "XWEntity",
        *,
        scope: str | Path | None = None,
        component: Literal["schema", "actions", "data", "full"] = "full"
    ) -> None:
        """
        Save entity to storage.
        Args:
            entity: Entity instance to save
            scope: Optional storage scope/path
            component: Which component to save (schema, actions, data, or full)
        """
        pass
    @abstractmethod

    def load_entity(
        self,
        entity: "XWEntity",
        *,
        scope: str | Path | None = None,
        component: Literal["schema", "actions", "data", "full"] = "full"
    ) -> None:
        """
        Load entity from storage.
        Args:
            entity: Entity instance to load into
            scope: Optional storage scope/path
            component: Which component to load (schema, actions, data, or full)
        """
        pass
    @abstractmethod

    def from_file(
        self,
        path: Path,
        *,
        component: Literal["schema", "actions", "data", "full"] = "full"
    ) -> "XWEntity":
        """
        Create entity from file.
        Args:
            path: File path to load from
            component: Which component to load (schema, actions, data, or full)
        Returns:
            XWEntity instance
        """
        pass
    @abstractmethod

    def from_format(
        self,
        content: str | bytes,
        *,
        component: Literal["schema", "actions", "data", "full"] = "full",
        input_format: str = "json"
    ) -> "XWEntity":
        """
        Create entity from serialized content.
        Args:
            content: Serialized content (str or bytes)
            component: Which component to load (schema, actions, data, or full)
            input_format: Serialization format (json, yaml, etc.)
        Returns:
            XWEntity instance
        """
        pass
    @abstractmethod

    def to_format(
        self,
        entity: "XWEntity",
        *,
        component: Literal["schema", "actions", "data", "full"] = "full",
        output_format: str = "json"
    ) -> str | bytes:
        """
        Serialize entity component to specified format.
        Args:
            entity: Entity instance to serialize
            component: Which component to serialize (schema, actions, data, or full)
            output_format: Serialization format (json, yaml, etc.)
        Returns:
            Serialized entity component (str for text formats, bytes for binary)
        """
        pass


class ICollectionStorage(ABC):
    """
    Storage contract for XWModelCollection persistence.
    Implementations are provided by external storage providers that satisfy this contract.
    """
    @abstractmethod

    def save_collection(
        self,
        collection: "XWModelCollection",
        *,
        base_path: Path | None = None
    ) -> None:
        """
        Save collection to storage.
        Args:
            collection: Collection instance to save
            base_path: Optional base path override
        """
        pass
    @abstractmethod

    def load_collection(
        self,
        collection: "XWModelCollection",
        *,
        base_path: Path | None = None
    ) -> None:
        """
        Load collection from storage.
        Args:
            collection: Collection instance to load into
            base_path: Optional base path override
        """
        pass


class IGroupStorage(ABC):
    """
    Storage contract for XWGroup persistence.
    Implementations are provided by external storage providers that satisfy this contract.
    """
    @abstractmethod

    def save_group(
        self,
        group: "XWGroup"
    ) -> None:
        """
        Save group to storage.
        Args:
            group: Group instance to save
        """
        pass
    @abstractmethod

    def load_group(
        self,
        group: "XWGroup"
    ) -> None:
        """
        Load group from storage.
        Args:
            group: Group instance to load into
        """
        pass
__all__ = [
    "IEntityStorage",
    "ICollectionStorage",
    "IGroupStorage",
]
