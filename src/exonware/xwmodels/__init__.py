"""
exonware.xwmodels
XWModelEntity is the composition layer that ties together:
- XWData (data storage + formats + lazy/atomic where supported)
- XWSchema (validation)
- XWAction (actions/services with contracts)
This package follows the facade pattern (see `entity.py`).
"""
# =============================================================================
# XWLAZY — GUIDE_00_MASTER: config_package_lazy_install_enabled (EARLY)
# =============================================================================
# Optional exonware-xwlazy: lite install skips lazy hook (same pattern as xwnode).
try:
    from exonware.xwlazy import config_package_lazy_install_enabled

    config_package_lazy_install_enabled(
        __package__ or "exonware.xwmodels",
        enabled=True,
        mode="smart",
    )
except ImportError:
    # xwlazy not installed — use pip install exonware-xwmodels[lazy] or exonware-xwlazy.
    pass
from .version import (
    __version__,
    get_version,
    get_version_info,
)
from .defs import (
    EntityState,
    PerformanceMode,
    EntityType,
    EntityID,
    EntityData,
    EntityMetadata,
    DEFAULT_ENTITY_TYPE,
    DEFAULT_STATE,
    DEFAULT_VERSION,
    STATE_TRANSITIONS,
    DEFAULT_CACHE_SIZE,
    DEFAULT_THREAD_SAFETY,
    DEFAULT_PERFORMANCE_MODE,
)
from .errors import (
    XWEntityError,
    XWEntityValidationError,
    XWEntityStateError,
    XWEntityActionError,
    XWEntityNotFoundError,
)
from exonware.xwsystem.shared import IObject, AObject, XWObject
from .contracts import (
    IEntity,
    IEntityActions,
    IEntityState,
    IEntitySerialization,
    IEntityProtocol,
    ICollection,
    IGroup,
    # Provider interfaces (from xwsystem)
    IBasicProviderAuth,
    IBasicProviderStorage,
)
from .config import (
    XWEntityConfig,
    get_config,
    set_config,
)
from .base import (
    ACollection,
    AGroup,
)
# Import base metadata/abstracts from xwentity, and expose xwmodels compatibility facade.
from exonware.xwentity import (
    XWEntityMetadata,
    AEntity,
)
from .entity_compat import XWModelEntity, XWEntity
from .collection import XWModelCollection
from .group import XWGroup
from .cache import (
    XWEntityCache,
    get_entity_cache,
    clear_entity_cache,
)
from .metaclass import (
    PropertyInfo,
    ActionInfo,
    DecoratorScanner,
)
# Enhanced entity creation methods
from .enhanced import (
    xwentity,
    create_entity_from_pydantic,
    create_entity_from_typeddict,
)
# Storage contracts and base classes
from .storage import (
    IEntityStorage,
    ICollectionStorage,
    IGroupStorage,
    AEntityStorage,
    ACollectionStorage,
    AGroupStorage,
    # Entity-specific storage operations
    XWEntityStorageGroup,
    create_entity_storage_group,
    create_entity_storage_collection,
    # Simple file-based storage (for development/testing)
    SimpleFileCollectionStorage,
    SimpleFileGroupStorage,
)
# Auth contracts and base classes
from .auth import (
    IEntityAuth,
    ICollectionAuth,
    IGroupAuth,
    AEntityAuth,
    ACollectionAuth,
    AGroupAuth,
)
__author__ = "eXonware Backend Team"
__email__ = "connect@exonware.com"
__company__ = "eXonware.com"
__description__ = "Entity management and relationship modeling library"
__all__ = [
    # facade
    "XWObject",
    "XWModelEntity",
    "XWEntity",
    "XWModelCollection",
    "XWGroup",
    # base
    "AObject",
    "AEntity",
    "ACollection",
    "AGroup",
    "XWEntityMetadata",
    # contracts
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
    # config
    "XWEntityConfig",
    "get_config",
    "set_config",
    # defs
    "EntityState",
    "PerformanceMode",
    "EntityType",
    "EntityID",
    "EntityData",
    "EntityMetadata",
    "DEFAULT_ENTITY_TYPE",
    "DEFAULT_STATE",
    "DEFAULT_VERSION",
    "STATE_TRANSITIONS",
    "DEFAULT_CACHE_SIZE",
    "DEFAULT_THREAD_SAFETY",
    "DEFAULT_PERFORMANCE_MODE",
    # errors
    "XWEntityError",
    "XWEntityValidationError",
    "XWEntityStateError",
    "XWEntityActionError",
    "XWEntityNotFoundError",
    # version
    "__version__",
    "get_version",
    "get_version_info",
    # cache
    "XWEntityCache",
    "get_entity_cache",
    "clear_entity_cache",
    # metaclass
    "PropertyInfo",
    "ActionInfo",
    "DecoratorScanner",
    # enhanced
    "xwentity",
    "create_entity_from_pydantic",
    "create_entity_from_typeddict",
    # storage contracts
    "IEntityStorage",
    "ICollectionStorage",
    "IGroupStorage",
    "AEntityStorage",
    "ACollectionStorage",
    "AGroupStorage",
    # storage integration (entity-specific operations)
    "XWEntityStorageGroup",
    "create_entity_storage_group",
    "create_entity_storage_collection",
    "SimpleFileCollectionStorage",
    "SimpleFileGroupStorage",
    # auth contracts
    "IEntityAuth",
    "ICollectionAuth",
    "IGroupAuth",
    "AEntityAuth",
    "ACollectionAuth",
    "AGroupAuth",
]
