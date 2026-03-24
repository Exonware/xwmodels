# XWEntity Standalone Refactoring

**Date:** 2026-01-26  
**Status:** ✅ Complete

## Summary

XWEntity has been refactored to be a **standalone library** that does not require `xwauth`, `xwstorage`, or `xwapi` as hard dependencies. The core functionality (Groups, Collections, Entities) works independently using only:

- `exonware-xwsystem` - Foundation library
- `exonware-xwschema` - Schema validation
- `exonware-xwdata` - Data manipulation (file-based persistence)
- `exonware-xwnode` - Graph engine
- `exonware-xwaction` - Action/workflow orchestration

## Changes Made

### 1. Provider Interfaces - Using Existing XW Interfaces

Updated `contracts.py` to use existing provider interfaces from xwstorage and xwauth when available:

- **`IStorageProvider`** - Aliases to `xwstorage.contracts.IStorageConnection` when available, fallback interface otherwise
- **`ITabularStorageProvider`** - Aliases to `xwstorage.contracts.ITabularDataConnection` when available, fallback interface otherwise
- **`IAuthProvider`** - Aliases to `xwauth.contracts.IAuthorizer` when available (has both `check_permission` and `get_user_roles`), fallback interface otherwise
- **`IAPIProvider`** - Custom interface for API generation (no existing equivalent found)

**Key Benefits:**
- ✅ Reuses existing, well-tested interfaces from xwstorage and xwauth
- ✅ No duplicate interface definitions
- ✅ Automatic compatibility with xwstorage/xwauth implementations
- ✅ Fallback interfaces when libraries not installed (standalone mode)

### 2. Integration Modules Updated

All integration modules in `integrations/` now use:

- **Conditional imports** - Only import `xwauth`/`xwstorage` if available
- **Provider interfaces** - Use `IStorageProvider`/`IAuthProvider` instead of direct dependencies
- **Adapter classes** - Wrap legacy `xwstorage`/`xwauth` connections as providers for backward compatibility

**Files Updated:**
- `integrations/storage/adapter.py` - Uses `IStorageProvider` interface
- `integrations/auth/authorization.py` - Uses `IAuthProvider` interface
- `integrations/auth/access_control.py` - Uses `IAuthProvider` interface

### 3. Dependencies Made Optional

**`pyproject.toml`:**
- Removed `exonware-xwauth` and `exonware-xwstorage` from required dependencies
- Added new optional dependency group: `baas` (for BaaS platform integration)
- Updated `lazy` and `full` optional dependencies

**`requirements.txt`:**
- Commented out `exonware-xwauth` and `exonware-xwstorage` as optional
- Added notes explaining they're only needed for BaaS integration features

### 4. Core Functionality Verified

✅ **Core classes are standalone:**
- `XWEntity` - Uses only `xwdata`, `xwschema`, `xwaction`, `xwnode`
- `XWCollection` - Uses only `xwdata` for file-based persistence
- `XWGroup` - Uses only `xwdata` for file-based persistence

✅ **No hard dependencies:**
- Core classes don't import from `integrations/` directory
- `__init__.py` doesn't export integration modules
- Integration modules are completely isolated

## Usage

### Core Functionality (No Optional Dependencies)

```python
from exonware.xwentity import XWEntity, XWCollection, XWGroup

# Works without xwauth, xwstorage, or xwapi
group = XWGroup("my_group", base_path=Path("./data"))
collection = group.create_collection("users", "user")
entity = XWEntity(...)
collection.add(entity)
group.save_all()
```

### With Optional BaaS Features

```python
# Install optional dependencies
# pip install exonware-xwentity[baas]

from exonware.xwentity import XWEntity, IStorageProvider, IAuthProvider
from exonware.xwentity.integrations.storage import EntityStorageAdapter
from exonware.xwentity.integrations.auth import EntityAuthorization

# Use with xwstorage (via adapter)
from exonware.xwstorage import create_connection
storage_conn = await create_connection(...)
adapter = EntityStorageAdapter(storage_connection=storage_conn)

# Use with xwauth (via adapter)
from exonware.xwauth import create_authorizer
auth = await create_authorizer(...)
authorization = EntityAuthorization(authorizer=auth)

# Or use custom providers implementing interfaces
class MyStorageProvider(IStorageProvider):
    async def save(self, data, path): ...
    async def load(self, path): ...
    # ... implement interface

my_provider = MyStorageProvider()
adapter = EntityStorageAdapter(storage_provider=my_provider)
```

## Architecture

### Provider Pattern

The refactoring follows a **provider pattern** where:

1. **Interfaces define contracts** - `IStorageProvider`, `IAuthProvider`, etc.
2. **Implementations are swappable** - Can use `xwstorage`/`xwauth` or custom implementations
3. **Backward compatibility maintained** - Legacy `xwstorage`/`xwauth` connections are wrapped as providers
4. **No hard dependencies** - Core library works without optional dependencies

### Integration Isolation

Integration modules are completely isolated:

- Located in `integrations/` directory
- Not imported by core classes
- Not exported in main `__init__.py`
- Use conditional imports to avoid import errors
- Can be used optionally when needed

## Benefits

1. ✅ **Standalone core** - Groups, Collections, Entities work independently
2. ✅ **Flexible providers** - Can swap storage/auth implementations
3. ✅ **Backward compatible** - Existing code using `xwstorage`/`xwauth` still works
4. ✅ **Future-proof** - Easy to add new providers or replace existing ones
5. ✅ **Cleaner dependencies** - Only install what you need

## Migration Guide

### For Core Users (No Changes Needed)

If you only use `XWEntity`, `XWCollection`, and `XWGroup`:
- ✅ **No changes required** - Everything works as before
- ✅ **No new dependencies** - Core dependencies unchanged

### For BaaS Integration Users

If you use integration modules:

**Before:**
```python
# Required xwauth and xwstorage to be installed
from exonware.xwentity.integrations.storage import EntityStorageAdapter
```

**After:**
```python
# Option 1: Install optional dependencies
# pip install exonware-xwentity[baas]

# Option 2: Use custom providers
from exonware.xwentity import IStorageProvider
class MyProvider(IStorageProvider): ...
adapter = EntityStorageAdapter(storage_provider=MyProvider())
```

## Testing

To verify standalone functionality:

```bash
# Install without optional dependencies
pip install exonware-xwentity

# Test core functionality
python -c "from exonware.xwentity import XWEntity, XWCollection, XWGroup; print('✅ Core works!')"
```

## Files Modified

- `src/exonware/xwentity/contracts.py` - Added provider interfaces
- `src/exonware/xwentity/__init__.py` - Export provider interfaces
- `src/exonware/xwentity/integrations/storage/adapter.py` - Use provider interface
- `src/exonware/xwentity/integrations/auth/authorization.py` - Use provider interface
- `src/exonware/xwentity/integrations/auth/access_control.py` - Use provider interface
- `pyproject.toml` - Made dependencies optional
- `requirements.txt` - Marked dependencies as optional

## Notes

- Integration modules remain in `integrations/` directory for BaaS platform features
- Provider interfaces reuse existing interfaces from xwstorage/xwauth when available
- Fallback interfaces provided when xwstorage/xwauth not installed (standalone mode)
- Adapter classes provide backward compatibility with existing `xwstorage`/`xwauth` code
- Core library is now truly standalone and can be used independently
- **No duplicate interfaces** - reuses existing work from xwstorage and xwauth libraries
