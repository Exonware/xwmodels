#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/base.py
XWEntity Abstract Base Classes
This module defines abstract base classes that extend interfaces from contracts.py.
Following GUIDE_DEV.md: All abstract classes start with 'A' and extend 'I' interfaces.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.12
Generation Date: 08-Nov-2025
"""

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
from pathlib import Path
import threading
import uuid
from exonware.xwsystem import get_logger
from exonware.xwdata import XWData
# Import XWAction for type checking and validation
from exonware.xwaction import XWAction
from exonware.xwsystem.shared import IObject, AObject
from collections.abc import Callable
from .contracts import (
    IEntity,
    IEntityActions,
    IEntityState,
    IEntitySerialization,
    ICollection,
    IGroup,
)
from .defs import (
    EntityState,
    EntityID,
    EntityType,
    EntityData,
    DEFAULT_ENTITY_TYPE,
    DEFAULT_STATE,
    DEFAULT_VERSION,
    STATE_TRANSITIONS,
    DEFAULT_CACHE_SIZE,
)
from .errors import (
    XWEntityError,
    XWEntityValidationError,
    XWEntityStateError,
    XWEntityActionError,
)
from .config import get_config
from .cache import get_entity_cache
logger = get_logger(__name__)
# ==============================================================================
# ABSTRACT OBJECT BASE
# ==============================================================================
# AObject is now imported from exonware.xwsystem.shared
# This ensures consistency across xwentity and other libraries that use XWObject
# ==============================================================================
# ENTITY METADATA
# ==============================================================================


class XWEntityMetadata:
    """
    Internal metadata management for entities.
    Manages entity identity, state, versioning, and timestamps.
    """

    def __init__(self, entity_type: str | None = None):
        """Initialize entity metadata."""
        self._id: EntityID = str(uuid.uuid4())
        self._type: EntityType = entity_type or DEFAULT_ENTITY_TYPE
        self._state: EntityState = DEFAULT_STATE
        self._version: int = DEFAULT_VERSION
        self._created_at: datetime = datetime.now()
        self._updated_at: datetime = self._created_at
        self._deleted_at: datetime | None = None
    @property

    def id(self) -> EntityID:
        """Get entity ID."""
        return self._id
    @property

    def type(self) -> EntityType:
        """Get entity type."""
        return self._type
    @property

    def state(self) -> EntityState:
        """Get entity state."""
        return self._state
    @state.setter

    def state(self, value: EntityState) -> None:
        """Set entity state."""
        self._state = value
        self._updated_at = datetime.now()
    @property

    def version(self) -> int:
        """Get entity version."""
        return self._version

    def update_version(self) -> None:
        """Increment entity version."""
        self._version += 1
        self._updated_at = datetime.now()
    @property

    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at
    @property

    def updated_at(self) -> datetime:
        """Get last update timestamp."""
        return self._updated_at
    @property

    def deleted_at(self) -> datetime | None:
        """Get deletion timestamp (None if not deleted)."""
        return self._deleted_at
    @deleted_at.setter

    def deleted_at(self, value: datetime | None) -> None:
        """Set deletion timestamp."""
        self._deleted_at = value
        if value is not None:
            self._updated_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to dictionary."""
        result = {
            "id": self._id,
            "type": self._type,
            "state": str(self._state),
            "version": self._version,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }
        if self._deleted_at is not None:
            result["deleted_at"] = self._deleted_at.isoformat()
        return result

    def from_dict(self, data: dict[str, Any]) -> None:
        """Load metadata from dictionary."""
        self._id = data.get("id", str(uuid.uuid4()))
        self._type = data.get("type", DEFAULT_ENTITY_TYPE)
        self._state = EntityState(data.get("state", DEFAULT_STATE.value))
        self._version = data.get("version", DEFAULT_VERSION)
        if "created_at" in data:
            self._created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            self._updated_at = datetime.fromisoformat(data["updated_at"])
        if "deleted_at" in data:
            self._deleted_at = datetime.fromisoformat(data["deleted_at"])
# ==============================================================================
# ABSTRACT ENTITY
# ==============================================================================


class AEntity(AObject, IEntity, IEntityActions, IEntityState, IEntitySerialization):
    """
    Abstract base class for all entity implementations.
    Provides default implementations for common functionality while requiring
    subclasses to implement core data operations. Manages metadata, caching,
    performance stats, and state transitions.
    """

    def __init__(
        self,
        schema: Any | None = None,  # XWSchema type
        data: Any | None = None,  # XWData type or dict
        entity_type: str | None = None,
        config: Any | None = None,  # XWEntityConfig type
    ):
        """
        Initialize abstract entity.
        Args:
            schema: Optional entity schema
            data: Optional initial data (dict or XWData)
            entity_type: Optional entity type name
            config: Optional entity configuration
        """
        # Initialize AObject parent (required for IObject interface)
        AObject.__init__(self, object_id=None)  # ID will be set by metadata
        # Core components
        self._metadata = XWEntityMetadata(entity_type)
        self._schema = schema
        self._config = config or get_config()
        # Data will be initialized by subclass
        self._data: Any | None = None  # XWData type
        # Actions storage
        self._actions: dict[str, Any] = {}
        # Performance optimizations
        self._cache: dict[str, Any] = {}
        self._cache_size = self._config.cache_size if hasattr(self._config, 'cache_size') else DEFAULT_CACHE_SIZE
        self._global_cache = get_entity_cache()
        self._schema_cache: dict[str, Any] | None = None
        self._performance_stats: dict[str, Any] = {
            "access_count": 0,
            "validation_count": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        # Extensibility
        self._extensions: dict[str, Any] = {}
        # Thread safety
        enable_thread_safety = (
            self._config.enable_thread_safety
            if hasattr(self._config, 'enable_thread_safety')
            else False
        )
        self._lock = threading.RLock() if enable_thread_safety else None
    # ==========================================================================
    # CORE PROPERTIES (IEntity)
    # ==========================================================================
    @property

    def id(self) -> EntityID:
        """Get the unique entity identifier."""
        return self._metadata.id
    @property

    def type(self) -> EntityType:
        """Get the entity type name."""
        return self._metadata.type
    @property

    def schema(self) -> Any | None:  # XWSchema type
        """Get the entity schema."""
        return self._schema
    @property
    @abstractmethod

    def data(self) -> Any:  # XWData type
        """Get the entity data. Must be implemented by subclass."""
        pass
    @property

    def state(self) -> EntityState:
        """Get the current entity state."""
        return self._metadata.state
    @property

    def version(self) -> int:
        """Get the entity version number."""
        return self._metadata.version
    @property

    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._metadata.created_at
    @property

    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        return self._metadata.updated_at
    # ==========================================================================
    # DATA OPERATIONS (IEntity)
    # ==========================================================================

    def _get(self, path: str, default: Any = None) -> Any:
        """Get value at path."""
        self._performance_stats["access_count"] += 1
        # Check cache first (both local and global)
        cache_key = f"get:{self._metadata.id}:{path}"
        cached = self._global_cache.get(cache_key)
        if cached is not None:
            self._performance_stats["cache_hits"] += 1
            return cached
        # Also check local cache
        if cache_key in self._cache:
            self._performance_stats["cache_hits"] += 1
            return self._cache[cache_key]
        self._performance_stats["cache_misses"] += 1
        # Delegate to data
        if self._data is None:
            return default
        result = self._data_get_sync(path, default)
        # Cache result (both local and global)
        if len(self._cache) < self._cache_size:
            self._cache[cache_key] = result
        self._global_cache.put(cache_key, result)
        return result

    def _data_get_sync(self, path: str, default: Any = None) -> Any:
        """
        Synchronous get over XWData - FULLY DELEGATES to XWData.
        Uses XWData.get() which provides:
        - Path-based access (e.g., "user.profile.name")
        - Query support via xwquery
        - Format-agnostic data access
        - Caching and performance optimizations
        Uses XWDataNode's sync methods first, then falls back to XWData's async methods.
        NO manual dict navigation - always uses XWData capabilities.
        """
        # Prefer XWDataNode sync navigation (fast path) - DELEGATE to XWData
        node = getattr(self._data, "_node", None)
        if node is not None and hasattr(node, "get_value_at_path"):
            return node.get_value_at_path(path, default)
        # Fallback: Use XWData's async get() method via sync bridge
        if isinstance(self._data, XWData) and hasattr(self._data, "get"):
            try:
                import asyncio
                # Try to get running event loop
                try:
                    loop = asyncio.get_running_loop()
                    # If we're in an async context, we can't use asyncio.run()
                    # Return default for now (caller should use async API)
                    logger.debug(f"Cannot use async get() in sync context with running loop")
                    return default
                except RuntimeError:
                    # No running loop - safe to use asyncio.run()
                    return asyncio.run(self._data.get(path, default))
            except Exception as e:
                logger.debug(f"Failed to use XWData.get(): {e}")
        # Last resort: if data is a plain dict, use simple access
        if isinstance(self._data, dict):
            # Use XWDataNode's navigation logic (reuse, don't duplicate)
            from exonware.xwdata.data.node import XWDataNode
            temp_node = XWDataNode(data=self._data)
            return temp_node.get_value_at_path(path, default)
        return default

    def _set(self, path: str, value: Any) -> None:
        """Set value at path."""
        if self._lock:
            with self._lock:
                self._set_impl(path, value)
        else:
            self._set_impl(path, value)

    def _set_impl(self, path: str, value: Any) -> None:
        """
        Internal set implementation - FULLY DELEGATES to XWData.
        Uses XWData.set() which provides:
        - Path-based updates (e.g., "user.profile.name")
        - Immutability support via XWNode
        - Automatic cache invalidation
        - Format-agnostic data updates
        Uses XWDataNode's sync methods first, then falls back to XWData's async methods.
        NO manual dict updates - always uses XWData capabilities.
        """
        if self._data is None:
            raise XWEntityError("Data not initialized")
        # Prefer XWDataNode sync mutation (COW) - DELEGATE to XWData
        node = getattr(self._data, "_node", None)
        if node is not None and hasattr(node, "set_value_at_path"):
            new_node = node.set_value_at_path(path, value)
            self._data = self._rebuild_xwdata_from_node(new_node)
        elif isinstance(self._data, XWData) and hasattr(self._data, "set"):
            # Fallback: Use XWData's async set() method via sync bridge
            try:
                import asyncio
                try:
                    loop = asyncio.get_running_loop()
                    logger.debug(f"Cannot use async set() in sync context with running loop")
                    raise XWEntityError("Cannot set value: async context required. Use async API.")
                except RuntimeError:
                    # No running loop - safe to use asyncio.run()
                    asyncio.run(self._data.set(path, value))
                    # Rebuild from updated node
                    node = getattr(self._data, "_node", None)
                    if node:
                        self._data = self._rebuild_xwdata_from_node(node)
            except Exception as e:
                logger.error(f"Failed to use XWData.set(): {e}")
                raise XWEntityError(f"Failed to set value: {e}", cause=e)
        elif isinstance(self._data, dict):
            # Last resort: if data is a plain dict, use XWDataNode's logic (reuse, don't duplicate)
            from exonware.xwdata.data.node import XWDataNode
            temp_node = XWDataNode(data=self._data)
            new_node = temp_node.set_value_at_path(path, value)
            self._data = new_node.to_native()
        else:
            raise XWEntityError("Cannot set value: data does not support mutation")
        self._metadata.update_version()
        self._clear_cache()  # Invalidate cache on data change

    def _rebuild_xwdata_from_node(self, new_node: Any) -> Any:
        """
        Rebuild an XWData instance from a new XWDataNode without using async APIs.
        This keeps XWEntity's sync API usable while preserving XWData's COW behavior.
        """
        old = self._data
        if old is None or not isinstance(old, XWData):
            return XWData(new_node)  # type: ignore[arg-type]
        instance = XWData.__new__(XWData)
        instance._config = old._config
        instance._engine = old._engine
        instance._node = new_node
        instance._metadata = getattr(new_node, "metadata", {})
        return instance

    def _delete(self, path: str) -> None:
        """Delete value at path."""
        if self._lock:
            with self._lock:
                self._delete_impl(path)
        else:
            self._delete_impl(path)

    def _delete_impl(self, path: str) -> None:
        """
        Internal delete implementation - FULLY DELEGATES to XWData.
        Uses XWData.delete() which provides:
        - Path-based deletion (e.g., "user.profile.name")
        - Immutability support via XWNode
        - Automatic cache invalidation
        - Format-agnostic data deletion
        Uses XWDataNode's sync methods first, then falls back to XWData's async methods.
        NO manual dict deletion - always uses XWData capabilities.
        """
        if self._data is None:
            raise XWEntityError("Data not initialized")
        # Prefer XWDataNode sync deletion - DELEGATE to XWData
        node = getattr(self._data, "_node", None)
        if node is not None and hasattr(node, "delete_at_path"):
            new_node = node.delete_at_path(path)
            self._data = self._rebuild_xwdata_from_node(new_node)
        elif isinstance(self._data, XWData) and hasattr(self._data, "delete"):
            # Fallback: Use XWData's async delete() method via sync bridge
            try:
                import asyncio
                try:
                    loop = asyncio.get_running_loop()
                    logger.debug(f"Cannot use async delete() in sync context with running loop")
                    raise XWEntityError("Cannot delete value: async context required. Use async API.")
                except RuntimeError:
                    # No running loop - safe to use asyncio.run()
                    asyncio.run(self._data.delete(path))
                    # Rebuild from updated node
                    node = getattr(self._data, "_node", None)
                    if node:
                        self._data = self._rebuild_xwdata_from_node(node)
            except Exception as e:
                logger.error(f"Failed to use XWData.delete(): {e}")
                raise XWEntityError(f"Failed to delete value: {e}", cause=e)
        elif isinstance(self._data, dict):
            # Last resort: if data is a plain dict, use XWDataNode's logic (reuse, don't duplicate)
            from exonware.xwdata.data.node import XWDataNode
            temp_node = XWDataNode(data=self._data)
            new_node = temp_node.delete_at_path(path)
            self._data = new_node.to_native()
        else:
            raise XWEntityError("Cannot delete value: data does not support mutation")
        self._metadata.update_version()
        self._clear_cache()  # Invalidate cache on data change

    def _update(self, updates: EntityData) -> None:
        """Update multiple values."""
        for path, value in updates.items():
            self._set(path, value)

    def _validate(self) -> bool:
        """
        Validate data against schema using XWSchema.
        Uses XWSchema.validate_sync() which supports XWData directly.
        This ensures full reuse of xwschema validation capabilities.
        """
        self._performance_stats["validation_count"] += 1
        if not self._schema:
            return True  # No schema means no validation
        if self._data is None:
            return False
        # Use XWSchema.validate_sync() - fully reuses xwschema validation
        # This method supports XWData directly, so no conversion needed
        if hasattr(self._schema, "validate_sync"):
            is_valid, _errors = self._schema.validate_sync(self._data)
            return bool(is_valid)
        if hasattr(self._schema, "validate"):
            # Async validate() is not supported from sync entity API.
            raise XWEntityValidationError(
                "Schema validation requires async context. Use XWSchema.validate_sync() or validate via XWEntity.validate_issues()."
            )
        logger.warning("Schema does not support validation")
        return True

    def _to_dict(self) -> EntityData:
        """Export entity as dictionary."""
        result: EntityData = {
            "_metadata": self._metadata.to_dict(),
        }
        if self._data and hasattr(self._data, 'to_native'):
            result["_data"] = self._data.to_native()
        else:
            result["_data"] = {}
        if self._schema:
            # Schema serialization depends on implementation
            if hasattr(self._schema, 'to_dict'):
                result["_schema"] = self._schema.to_dict()
            elif hasattr(self._schema, 'to_native'):
                result["_schema"] = self._schema.to_native()
        if self._actions:
            result["_actions"] = {
                name: self._export_action(action)
                for name, action in self._actions.items()
            }
        return result

    def _export_action(self, action: Any) -> dict[str, Any]:
        """Export action metadata."""
        if hasattr(action, 'to_dict'):
            return action.to_dict()
        elif hasattr(action, 'to_native'):
            return action.to_native()
        elif hasattr(action, 'api_name'):
            return {"api_name": action.api_name}
        else:
            return {"type": type(action).__name__}

    def _from_dict(self, data: EntityData) -> None:
        """Import entity from dictionary."""
        if "_metadata" in data:
            self._metadata.from_dict(data["_metadata"])
        if "_data" in data:
            # Data initialization depends on subclass
            self._init_data_from_dict(data["_data"])
        # Optional schema restore
        if "_schema" in data and data["_schema"] is not None:
            from exonware.xwschema import XWSchema
            try:
                if isinstance(data["_schema"], dict):
                    self._schema = XWSchema(data["_schema"])
            except Exception as e:
                raise XWEntityError(f"Failed to restore schema from dict: {e}", cause=e)
        # Optional actions restore
        if "_actions" in data and isinstance(data["_actions"], dict):
            from exonware.xwaction import XWAction
            try:
                for _name, action_payload in data["_actions"].items():
                    if isinstance(action_payload, dict):
                        try:
                            action = XWAction.from_native(action_payload)
                            self._register_action(action)
                        except (ValueError, AttributeError) as action_error:
                            # Actions with local/closure function references may not be restorable
                            # This is expected behavior - log warning but continue
                            logger.warning(
                                f"Failed to restore action '{_name}' from dict: {action_error}. "
                                f"This is expected for actions with local function references."
                            )
            except Exception as e:
                # Only raise error if it's not a function resolution issue
                if "Cannot resolve function" not in str(e):
                    raise XWEntityError(f"Failed to restore actions from dict: {e}", cause=e)
                else:
                    # Function resolution failures are expected for local functions
                    logger.warning(f"Some actions could not be restored due to function resolution: {e}")
    @abstractmethod

    def _init_data_from_dict(self, data: EntityData) -> None:
        """Initialize data from dictionary. Must be implemented by subclass."""
        pass
    # ==========================================================================
    # ACTIONS (IEntityActions)
    # ==========================================================================

    def _execute_action(self, action_name: str, *args, **kwargs) -> Any:
        """
        Execute a registered action with parameter validation.
        Args:
            action_name: Name of the action to execute
            *args: Positional arguments (will be converted to kwargs based on function signature)
            **kwargs: Keyword arguments
        Returns:
            Action result
        Raises:
            XWEntityActionError: If action not found or execution fails
            XWEntityValidationError: If parameter validation fails
        """
        if action_name not in self._actions:
            raise XWEntityActionError(
                f"Action '{action_name}' not found",
                action_name=action_name
            )
        action = self._actions[action_name]
        # Extract XWAction object if action is a decorated method
        xwaction_obj = None
        if callable(action) and hasattr(action, 'xwaction'):
            xwaction_obj = getattr(action, 'xwaction', None)
        elif XWAction and isinstance(action, XWAction):
            xwaction_obj = action
        # Note: Parameter conversion and validation is handled by XWAction wrapper
        # We don't need to duplicate that logic here - just pass args/kwargs through
        # Handle different action types
        # CRITICAL: Always use XWAction.execute() if available (has validation built-in)
        from exonware.xwaction import ActionContext
        ctx = ActionContext(
            actor="entity",
            source="xwentity",
            metadata={"action_name": action_name}
        )
        # PRIORITY 1: Use XWAction.execute() - fully reuses xwaction execution pipeline
        # This uses action_executor internally which provides:
        # - Input validation via action_validator
        # - Permission checking
        # - Engine selection and execution
        # - Handler pipeline (BEFORE, AFTER, ERROR)
        # - Result wrapping in ActionResult
        if xwaction_obj and hasattr(xwaction_obj, 'execute'):
            # We have an XWAction object extracted from a decorated method
            # Use XWAction.execute() which internally uses action_executor
            # This ensures full reuse of xwaction capabilities
            return xwaction_obj.execute(context=ctx, instance=self, **kwargs)
        # PRIORITY 2: Action itself is XWAction (has execute method)
        elif XWAction and isinstance(action, XWAction) and hasattr(action, 'execute'):
            # Use XWAction.execute() - fully reuses xwaction execution pipeline
            return action.execute(context=ctx, instance=self, **kwargs)
        # PRIORITY 3: Action has execute method (might be XWAction but not isinstance check)
        elif hasattr(action, 'execute') and callable(getattr(action, 'execute', None)):
            # Try to use execute method
            return action.execute(context=ctx, instance=self, **kwargs)
        # PRIORITY 4: Regular callable - validate manually if we have XWAction object
        elif callable(action):
            # If we have XWAction object with validation schemas, validate before calling
            if xwaction_obj and hasattr(xwaction_obj, 'in_types') and xwaction_obj.in_types:
                # Validate inputs before calling
                from exonware.xwaction.core.validation import action_validator
                validation_result = action_validator.validate_inputs(xwaction_obj, kwargs)
                if not validation_result.valid:
                    raise XWEntityValidationError(
                        f"Action parameter validation failed: {', '.join(validation_result.errors)}",
                        cause=None
                    )
            # Execute the callable
            return action(self, *args, **kwargs)
        else:
            raise XWEntityActionError(
                f"Action '{action_name}' is not callable",
                action_name=action_name
            )

    def _list_actions(self) -> list[str]:
        """List available action names."""
        return list(self._actions.keys())

    def _export_actions(self) -> dict[str, dict[str, Any]]:
        """Export action metadata."""
        return {
            name: self._export_action(action)
            for name, action in self._actions.items()
        }

    def _register_action(self, action: Any) -> None:  # XWAction type
        """
        Register an action for this entity.
        Normalizes actions at registration time:
        - Decorated methods (wrapper.xwaction) -> extracts XWAction instance
        - XWAction instances -> stores directly
        - Other callables -> stores as-is
        """
        # Normalize: Extract XWAction object if it's a decorated method
        # For decorated methods: wrapper.xwaction -> XWAction instance
        # For XWAction from JSON/direct: already an XWAction instance
        if callable(action) and hasattr(action, 'xwaction') and XWAction is not None:
            xwaction_obj = getattr(action, 'xwaction', None)
            if isinstance(xwaction_obj, XWAction):
                action = xwaction_obj  # Store XWAction instance directly
        # Get action name
        if hasattr(action, 'api_name'):
            name = action.api_name
        elif hasattr(action, 'name'):
            name = action.name
        elif hasattr(action, '__name__'):
            name = action.__name__
        else:
            name = f"action_{len(self._actions)}"
        self._actions[name] = action
        logger.debug(f"Registered action: {name}")
    # ==========================================================================
    # STATE (IEntityState)
    # ==========================================================================

    def _transition_to(self, target_state: EntityState) -> None:
        """Transition to a new state."""
        if not self._can_transition_to(target_state):
            raise XWEntityStateError(
                f"Cannot transition from {self._metadata.state} to {target_state}",
                current_state=str(self._metadata.state),
                target_state=str(target_state)
            )
        self._metadata.state = target_state
        self._metadata.update_version()
        logger.debug(f"Entity {self._metadata.id} transitioned to {target_state}")

    def _can_transition_to(self, target_state: EntityState) -> bool:
        """Check if state transition is allowed."""
        current_state = self._metadata.state
        allowed_transitions = STATE_TRANSITIONS.get(current_state, [])
        return target_state in allowed_transitions

    def _update_version(self) -> None:
        """Update the entity version."""
        self._metadata.update_version()
    # ==========================================================================
    # SERIALIZATION (IEntitySerialization)
    # ==========================================================================

    def _to_native(self) -> EntityData:
        """Get entity as native dictionary."""
        return self._to_dict()

    def _from_native(self, data: EntityData) -> None:
        """Create entity from native dictionary."""
        self._from_dict(data)
    # ==========================================================================
    # AOBJECT INTERFACE IMPLEMENTATION
    # ==========================================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Export entity as dictionary (AObject interface).
        Delegates to _to_dict() and adds IObject required fields.
        """
        result = self._to_dict()
        # Ensure IObject required fields are present
        if "_metadata" in result:
            metadata = result["_metadata"]
            # Add uid if not present (AObject requirement)
            if "uid" not in metadata:
                metadata["uid"] = self.uid
            # Add title and description if available
            if hasattr(self, 'title') and self.title:
                metadata["title"] = self.title
            if hasattr(self, 'description') and self.description:
                metadata["description"] = self.description
        return result

    def to_native(self) -> Any:
        """
        Get entity as native representation (AObject interface).
        Delegates to _to_native().
        """
        return self._to_native()

    def from_native(self, data: dict[str, Any]) -> "IObject":
        """
        Create entity from native dictionary (AObject interface).
        Delegates to _from_native().
        """
        self._from_native(data)
        return self
    @abstractmethod

    def save(self, *args, **kwargs) -> None:
        """
        Save entity to storage (AObject interface).
        Must be implemented by subclass.
        """
        pass
    @abstractmethod

    def load(self, *args, **kwargs) -> None:
        """
        Load entity from storage (AObject interface).
        Must be implemented by subclass.
        """
        pass
    # ==========================================================================
    # PERFORMANCE OPTIMIZATION
    # ==========================================================================

    def _optimize_for_access(self) -> None:
        """Optimize the entity for fast access operations."""
        # Pre-cache frequently accessed paths
        self._cache_schema()

    def _optimize_for_validation(self) -> None:
        """Optimize the entity for fast validation operations."""
        self._cache_schema()

    def _cache_schema(self) -> None:
        """Cache the schema for faster validation."""
        if self._schema and not self._schema_cache:
            if hasattr(self._schema, 'to_native'):
                self._schema_cache = self._schema.to_native()
            elif hasattr(self._schema, 'to_dict'):
                self._schema_cache = self._schema.to_dict()

    def _clear_cache(self) -> None:
        """Clear performance cache (both local and global entries for this entity)."""
        self._cache.clear()
        self._schema_cache = None
        # Clear global cache entries for this entity only (not all entities)
        # Cache keys are in format "get:{entity_id}:{path}"
        entity_prefix = f"get:{self._metadata.id}:"
        if self._global_cache and hasattr(self._global_cache, 'clear_by_prefix'):
            self._global_cache.clear_by_prefix(entity_prefix)

    def _get_memory_usage(self) -> int:
        """
        Get the memory usage in bytes.
        Returns:
            Estimated memory usage in bytes
        """
        import sys
        size = 0
        size += sys.getsizeof(self._metadata)
        if self._data:
            size += sys.getsizeof(self._data)
        size += sys.getsizeof(self._actions)
        size += sys.getsizeof(self._cache)
        size += sys.getsizeof(self._extensions)
        return size

    def _optimize_memory(self) -> None:
        """Optimize memory usage."""
        # Clear unnecessary caches
        self._clear_cache()
        # Compact data if possible
        if self._data and hasattr(self._data, 'compact'):
            self._data.compact()

    def get_performance_stats(self) -> dict[str, Any]:
        """
        Get performance statistics.
        Returns:
            Dictionary with performance statistics
        """
        stats = self._performance_stats.copy()
        stats['cache_stats'] = self._global_cache.stats()
        return stats
    # ==========================================================================
    # EXTENSIBILITY
    # ==========================================================================

    def register_extension(self, name: str, extension: Any) -> None:
        """
        Register an extension with the entity.
        Args:
            name: Extension name
            extension: Extension object
        """
        self._extensions[name] = extension
        logger.debug(f"Registered extension: {name}")

    def get_extension(self, name: str) -> Any | None:
        """
        Get an extension by name.
        Args:
            name: Extension name
        Returns:
            Extension object or None if not found
        """
        return self._extensions.get(name)

    def has_extension(self, name: str) -> bool:
        """
        Check if an extension exists.
        Args:
            name: Extension name
        Returns:
            True if extension exists
        """
        return name in self._extensions

    def list_extensions(self) -> list[str]:
        """
        List all registered extensions.
        Returns:
            List of extension names
        """
        return list(self._extensions.keys())

    def remove_extension(self, name: str) -> bool:
        """
        Remove an extension by name.
        Args:
            name: Extension name
        Returns:
            True if extension was removed, False if not found
        """
        if name in self._extensions:
            del self._extensions[name]
            logger.debug(f"Removed extension: {name}")
            return True
        return False

    def has_extension_type(self, extension_type: str) -> bool:
        """
        Check if an extension of a specific type exists.
        Args:
            extension_type: Extension type name to search for
        Returns:
            True if extension of type exists
        """
        return any(
            hasattr(ext, '__class__') and extension_type.lower() in ext.__class__.__name__.lower()
            for ext in self._extensions.values()
        )
# ==============================================================================
# EXPORTS
# ==============================================================================
# ==============================================================================
# ABSTRACT COLLECTION
# ==============================================================================


class ACollection[TEntity](ICollection[TEntity]):
    """
    Abstract base class for collections of entities.
    Provides common functionality for XWCollection implementations.
    Extends ICollection interface.
    """

    def __init__(
        self,
        id: str,  # noqa: A002
        entity_type: EntityType,
        group_id: str | None = None,
    ):
        """Initialize abstract collection. id is mandatory."""
        self._collection_id = id
        self._entity_type = entity_type
        self._group_id = group_id
        self._entities: dict[EntityID, TEntity] = {}
    @property

    def collection_id(self) -> str:
        """Get the collection identifier."""
        return self._collection_id
    @property

    def group_id(self) -> str | None:
        """Get the group identifier this collection belongs to."""
        return self._group_id
    @property

    def entity_type(self) -> EntityType:
        """Get the type of entities in this collection."""
        return self._entity_type
    @property

    def size(self) -> int:
        """Get the number of entities in the collection."""
        return len(self._entities)

    def add(self, entity: TEntity) -> None:
        """Add an entity to the collection."""
        # Type checking: ensure entity has required IEntity attributes
        if not hasattr(entity, 'id') or not hasattr(entity, 'type'):
            raise XWEntityError(f"Entity must have 'id' and 'type' attributes (must implement IEntity)")
        # Type checking with runtime protocol check if available
        from .contracts import IEntityProtocol
        if not isinstance(entity, IEntityProtocol):
            # Fallback: check for required attributes
            if not (hasattr(entity, 'id') and hasattr(entity, 'type') and hasattr(entity, 'state')):
                raise XWEntityError(f"Entity must implement IEntity interface")
        # Support both class-based and string-based entity_type (GUIDE_DEV: fix root cause)
        if isinstance(self._entity_type, type):
            if not isinstance(entity, self._entity_type):
                raise XWEntityError(
                    f"Entity type mismatch: expected {self._entity_type.__name__}, "
                    f"got {type(entity).__name__}"
                )
        else:
            entity_type = getattr(entity, 'type')
            if entity_type != self._entity_type:
                raise XWEntityError(
                    f"Entity type mismatch: expected {self._entity_type}, got {entity_type}"
                )
        entity_id = getattr(entity, 'id')
        self._entities[entity_id] = entity

    def remove(self, entity_id: EntityID) -> bool:
        """Remove an entity from the collection by ID."""
        if entity_id in self._entities:
            del self._entities[entity_id]
            return True
        return False

    def get(self, entity_id: EntityID) -> TEntity | None:
        """Get an entity by ID."""
        return self._entities.get(entity_id)

    def find(self, predicate: Callable[[TEntity], bool]) -> list[TEntity]:
        """Find entities matching a predicate."""
        return [entity for entity in self._entities.values() if predicate(entity)]

    def list_all(self) -> list[TEntity]:
        """Get all entities in the collection."""
        return list(self._entities.values())

    def clear(self) -> None:
        """Clear all entities from the collection."""
        self._entities.clear()
    @abstractmethod

    def save(self, base_path: Path | None = None) -> None:
        """Save collection to storage."""
        pass
    @abstractmethod

    def load(self, base_path: Path | None = None) -> None:
        """Load collection from storage."""
        pass
# ==============================================================================
# ABSTRACT GROUP
# ==============================================================================


class AGroup(IGroup, ABC):
    """
    Abstract base class for groups of collections.
    Provides common functionality for XWGroup implementations.
    Extends IGroup interface.
    """

    def __init__(
        self,
        id: str,  # noqa: A002
        base_path: Path | None = None,
    ):
        """Initialize abstract group. id is mandatory."""
        self._group_id = id
        # Normalize base_path to relative if it's absolute
        if base_path is None:
            # Default to current directory, but keep it relative
            self._base_path = Path(".")
        elif base_path.is_absolute():
            try:
                self._base_path = base_path.relative_to(Path.cwd())
            except ValueError:
                # Can't make relative, store as-is but this may cause issues
                from exonware.xwsystem import get_logger
                logger = get_logger(__name__)
                logger.warning(
                    f"Base path {base_path} is absolute and cannot be made relative to cwd. "
                    f"This may cause path validation errors."
                )
                self._base_path = base_path
        else:
            # Already relative, store as-is
            self._base_path = base_path
        self._collections: dict[str, Any] = {}  # ICollection type
    @property

    def group_id(self) -> str:
        """Get the group identifier."""
        return self._group_id
    @property

    def base_path(self) -> Path | None:
        """Get the base storage path for this group."""
        return self._base_path
    @property

    def collections(self) -> dict[str, Any]:  # ICollection type
        """Get all collections in this group."""
        return self._collections.copy()
    @property

    def collection_count(self) -> int:
        """Get the number of collections in this group."""
        return len(self._collections)
    @abstractmethod

    def create_collection(self, id: str, entity_type: EntityType) -> Any:  # noqa: A002  # ICollection type
        """Create a new collection in this group. id is mandatory."""
        pass

    def get_collection(self, id: str) -> Any | None:  # noqa: A002  # ICollection type
        """Get a collection by ID."""
        return self._collections.get(id)

    def remove_collection(self, id: str) -> bool:  # noqa: A002
        """Remove a collection from this group."""
        if id in self._collections:
            del self._collections[id]
            return True
        return False

    def list_collections(self) -> list[str]:
        """List all collection IDs in this group."""
        return list(self._collections.keys())
    @abstractmethod

    def save_all(self) -> None:
        """Save all collections in this group."""
        pass
    @abstractmethod

    def load_all(self) -> None:
        """Load all collections in this group."""
        pass
# ==============================================================================
# EXPORTS
# ==============================================================================
__all__ = [
    "AObject",
    "XWEntityMetadata",
    "AEntity",
    "ACollection",
    "AGroup",
]
