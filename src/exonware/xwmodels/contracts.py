#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/contracts.py
XWEntity Interfaces and Contracts
This module defines all interfaces for the xwentity library following
GUIDE_DEV.md standards. All interfaces use 'I' prefix.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.9
Generation Date: 08-Nov-2025
"""

from typing import Any, Protocol, runtime_checkable, TYPE_CHECKING
from pathlib import Path
from datetime import datetime
from exonware.xwsystem.shared import IObject
from .defs import EntityState, EntityType, EntityID, EntityData, EntityMetadata
from .errors import (
    XWEntityError,
    XWEntityValidationError,
    XWEntityStateError,
    XWEntityActionError,
)
if TYPE_CHECKING:
    from typing import Any as EntityTypeHint
else:
    EntityTypeHint = Any
# ==============================================================================
# CORE OBJECT INTERFACE
# ==============================================================================
# IObject is now imported from exonware.xwsystem.shared
# This ensures consistency across xwentity and other libraries that use XWObject
# ==============================================================================
# CORE ENTITY INTERFACE
# ==============================================================================
@runtime_checkable

class IEntity(IObject, Protocol):
    """
    Core interface for all entities in the XWEntity system.
    This interface defines the fundamental operations that all entities
    must support, ensuring consistency across different entity types.
    These methods are considered internal-facing, to be called by the
    public facade, hence the underscore prefix.
    """
    @property

    def id(self) -> EntityID:
        """Get the unique entity identifier."""
        ...
    @property

    def type(self) -> EntityType:
        """Get the entity type name."""
        ...
    @property

    def schema(self) -> Any | None:  # XWSchema type
        """Get the entity schema."""
        ...
    @property

    def data(self) -> Any:  # XWData type
        """Get the entity data."""
        ...
    @property

    def state(self) -> EntityState:
        """Get the current entity state."""
        ...
    @property

    def version(self) -> int:
        """Get the entity version number."""
        ...
    @property

    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        ...
    @property

    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        ...

    def _update(self, updates: EntityData) -> None:
        """Update multiple values."""
        ...

    def _validate(self) -> bool:
        """Validate data against schema."""
        ...

    def _to_dict(self) -> EntityData:
        """Export entity as dictionary."""
        ...

    def _from_dict(self, data: EntityData) -> None:
        """Import entity from dictionary."""
        ...
# ==============================================================================
# ACTION INTERFACE
# ==============================================================================
@runtime_checkable

class IEntityActions(Protocol):
    """
    Interface for entities that support actions.
    This interface extends IEntity with action-related capabilities.
    """

    def _execute_action(self, action_name: str, **kwargs) -> Any:
        """Execute a registered action."""
        ...

    def _list_actions(self) -> list[str]:
        """List available action names."""
        ...

    def _export_actions(self) -> dict[str, dict[str, Any]]:
        """Export action metadata."""
        ...

    def _register_action(self, action: Any) -> None:  # XWAction type
        """Register an action for this entity."""
        ...
# ==============================================================================
# STATE INTERFACE
# ==============================================================================
@runtime_checkable

class IEntityState(Protocol):
    """
    Interface for entities that support state management.
    This interface extends IEntity with state transition capabilities.
    """

    def _transition_to(self, target_state: EntityState) -> None:
        """Transition to a new state."""
        ...

    def _can_transition_to(self, target_state: EntityState) -> bool:
        """Check if state transition is allowed."""
        ...

    def _update_version(self) -> None:
        """Update the entity version."""
        ...
# ==============================================================================
# SERIALIZATION INTERFACE
# ==============================================================================
@runtime_checkable

class IEntitySerialization(Protocol):
    """
    Interface for entities that support serialization.
    This interface extends IEntity with serialization capabilities.
    """

    def _to_file(self, path: str | Path, format: str | None = None) -> bool:
        """Save entity to file."""
        ...

    def _from_file(self, path: str | Path, format: str | None = None) -> None:
        """Load entity from file."""
        ...

    def _to_native(self) -> EntityData:
        """Get entity as native dictionary."""
        ...

    def _from_native(self, data: EntityData) -> None:
        """Create entity from native dictionary."""
        ...
# ==============================================================================
# PROTOCOL INTERFACES (for runtime checking)
# ==============================================================================
# ==============================================================================
# COLLECTION INTERFACE
# ==============================================================================
@runtime_checkable

class ICollection[TEntity](Protocol):
    """
    Interface for collections of entities.
    A collection is a container that holds multiple entities of the same type,
    providing operations for managing and querying entities.
    """
    @property

    def collection_id(self) -> str:
        """Get the collection identifier."""
        ...
    @property

    def group_id(self) -> str | None:
        """Get the group identifier this collection belongs to."""
        ...
    @property

    def entity_type(self) -> EntityType:
        """Get the type of entities in this collection."""
        ...
    @property

    def size(self) -> int:
        """Get the number of entities in the collection."""
        ...

    def add(self, entity: TEntity) -> None:
        """Add an entity to the collection."""
        ...

    def remove(self, entity_id: EntityID) -> bool:
        """Remove an entity from the collection by ID."""
        ...

    def get(self, entity_id: EntityID) -> TEntity | None:
        """Get an entity by ID."""
        ...

    def find(self, predicate: Any) -> list[TEntity]:
        """Find entities matching a predicate."""
        ...

    def list_all(self) -> list[TEntity]:
        """Get all entities in the collection."""
        ...

    def clear(self) -> None:
        """Clear all entities from the collection."""
        ...

    def save(self, base_path: Any | None = None) -> None:  # Path type
        """Save collection to storage."""
        ...

    def load(self, base_path: Any | None = None) -> None:  # Path type
        """Load collection from storage."""
        ...
# ==============================================================================
# GROUP INTERFACE
# ==============================================================================
@runtime_checkable

class IGroup(Protocol):
    """
    Interface for groups of collections.
    A group contains multiple collections and manages their organization
    and storage structure.
    """
    @property

    def group_id(self) -> str:
        """Get the group identifier."""
        ...
    @property

    def base_path(self) -> Any | None:  # Path type
        """Get the base storage path for this group."""
        ...
    @property

    def collections(self) -> dict[str, Any]:  # ICollection type
        """Get all collections in this group."""
        ...
    @property

    def collection_count(self) -> int:
        """Get the number of collections in this group."""
        ...

    def create_collection(self, id: str, entity_type: EntityType) -> Any:  # noqa: A002  # ICollection type
        """Create a new collection in this group. id is mandatory."""
        ...

    def get_collection(self, id: str) -> Any | None:  # noqa: A002  # ICollection type
        """Get a collection by ID."""
        ...

    def remove_collection(self, id: str) -> bool:  # noqa: A002
        """Remove a collection from this group."""
        ...

    def list_collections(self) -> list[str]:
        """List all collection IDs in this group."""
        ...

    def save_all(self) -> None:
        """Save all collections in this group."""
        ...

    def load_all(self) -> None:
        """Load all collections in this group."""
        ...
# ==============================================================================
# PROTOCOL INTERFACE (for runtime checking)
# ==============================================================================
@runtime_checkable

class IEntityProtocol(Protocol):
    """
    Protocol for internal entities that can be checked at runtime.
    This allows for duck typing and runtime type checking of entity implementations
    without requiring explicit inheritance from IEntity.
    """
    id: EntityID
    type: EntityType
    state: EntityState
    version: int
    created_at: datetime
    updated_at: datetime

    def _update(self, updates: EntityData) -> None: ...

    def _validate(self) -> bool: ...

    def _to_dict(self) -> EntityData: ...

    def _from_dict(self, data: EntityData) -> None: ...
# ==============================================================================
# PROVIDER INTERFACES (Optional Dependencies)
# ==============================================================================
# xwentity reuses provider interfaces from xwsystem (single source of truth)
from exonware.xwsystem.shared.contracts import (
    IBasicProviderAuth,
    IBasicProviderStorage,
)
# ==============================================================================
# EXPORTS
# ==============================================================================
__all__ = [
    "IObject",
    "IEntity",
    "IEntityActions",
    "IEntityState",
    "IEntitySerialization",
    "IEntityProtocol",
    "ICollection",
    "IGroup",
    # Provider interfaces (from xwsystem)
    "IBasicProviderAuth",
    "IBasicProviderStorage",
]
