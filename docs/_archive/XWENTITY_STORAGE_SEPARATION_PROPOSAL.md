## XWEntity → XWStorage Separation Proposal

### Goals (Aligned with GUIDE_DEV.md)

- **Make `xwentity` purely about entities**: metadata, state, actions, relationships, lifecycle, and in‑memory collections/groups.
- **Move storage & serialization concerns** into:
  - **`xwstorage`**: persistence of entities/collections/groups (paths, files, xwjson, manifests, providers).
  - **`xwsystem`**: shared low‑level serialization/IO utilities only.

This proposal is explicitly aligned with:

- **`GUIDE_DEV.md`**: contracts/base/facade patterns, layering rules, error‑fixing philosophy, "never reinvent the wheel", and **no duplication**.
- **`GUIDE_TEST.md`**: hierarchical test layers, markers, test runners, and **root‑cause‑oriented** testing.

Wherever there is conflict, **GUIDE_DEV.md and GUIDE_TEST.md take precedence** over this document.

---

## 1. Storage Abstractions in `xwentity.storage`

**Storage contracts and base classes are owned by `xwentity`**, not `xwstorage`. This ensures `xwentity` defines its own storage interface, and `xwstorage` provides implementations that satisfy those contracts.

Following **GUIDE_DEV.md layering**:

- **Contracts** in `xwentity/src/exonware/xwentity/storage/contracts.py` (`I*` types only).
- **Abstract base classes** in `xwentity/src/exonware/xwentity/storage/base.py` (`A*` types only).
- **Concrete implementations** provided by `xwstorage` library (no concrete classes with specific names like `LocalEntityFileStorage` – this is a design defect).

### 1.1 Contracts (in `xwentity.storage.contracts`)

Define new interfaces (names are indicative and must follow GUIDE_DEV naming: `I*` in contracts):

- **`IEntityStorage`** (storage contract for `XWEntity`)
  - `save_entity(entity: XWEntity, *, scope: str | Path | None = None, component: Literal["schema","actions","data","full"]="full") -> None`
  - `load_entity(entity: XWEntity, *, scope: str | Path | None = None, component: Literal["schema","actions","data","full"]="full") -> None`
  - `from_file(path: Path, *, component: Literal["schema","actions","data","full"]="full") -> XWEntity`
  - `from_format(content: str | bytes, *, component: Literal["schema","actions","data","full"]="full", input_format: str = "json") -> XWEntity`
  - `to_format(entity: XWEntity, *, component: Literal["schema","actions","data","full"]="full", output_format: str = "json") -> str | bytes`

- **`ICollectionStorage`** (storage contract for `XWCollection`)
  - `save_collection(collection: XWCollection, *, base_path: Path | None = None) -> None`
  - `load_collection(collection: XWCollection, *, base_path: Path | None = None) -> None`

- **`IGroupStorage`** (storage contract for `XWGroup`)
  - `save_group(group: XWGroup) -> None`
  - `load_group(group: XWGroup) -> None`

These contracts live in `xwentity` because **`xwentity` owns its storage interface**. Implementations in `xwstorage` must satisfy these contracts.

### 1.2 Abstract Base Classes (in `xwentity.storage.base`)

Add abstract base classes that implement cross‑cutting behaviour but no IO:

- **`AEntityStorage(IEntityStorage)`**
  - Common helpers: converting entities to dicts/native, shared error handling, logging hooks.

- **`ACollectionStorage(ICollectionStorage)`**
  - Common helpers: iterating collections, composing entity storage for per‑entity operations.

- **`AGroupStorage(IGroupStorage)`**
  - Common helpers: traversing group/collection hierarchies, composing collection/entity storage.

These follow the same **A*/I* pattern used in `xwentity` (`AEntity`, `ACollection`, `AGroup`). All storage implementations (from `xwstorage` or elsewhere) can extend these base classes.

### 1.3 Implementations from `xwstorage` (No Named Concrete Classes)

**Important Design Principle**: Concrete storage implementations like `LocalEntityFileStorage`, `LocalCollectionFileStorage`, or `XWStorageManifestGroupStorage` **should NOT exist as named classes**. This is a design defect.

Instead:

- **`xwstorage`** provides implementations that satisfy `IEntityStorage`, `ICollectionStorage`, and `IGroupStorage` contracts.
- These implementations are accessed through **factory functions or registry patterns** in `xwstorage`, not as concrete class names.
- The logic currently in `XWEntity.from_file/save/to_file/from_format/to_format`, `AEntity._to_file/_from_file`, `XWCollection._get_storage_path/save/load`, and `XWGroup.save_all/load_all` moves into `xwstorage` implementations.
- `xwstorage` implementations must respect **GUIDE_DEV "no duplication"** by reusing existing utilities in `xwsystem` and `xwdata` instead of re‑implementing serialization or path logic.

**Example pattern** (not prescriptive, but illustrates the principle):

```python
# In xwstorage - factory/registry approach, not concrete classes
from exonware.xwentity.storage.contracts import IEntityStorage

def create_entity_storage(backend: str = "local", **opts) -> IEntityStorage:
    """Factory that returns an IEntityStorage implementation."""
    if backend == "local":
        return _LocalFileEntityStorage(**opts)  # Internal implementation
    # ... other backends
```

This keeps `xwentity` decoupled from `xwstorage` implementation details while `xwstorage` provides the actual persistence logic.

---

## 1A. Auth Abstractions in `xwentity.auth`

**Auth contracts and base classes are owned by `xwentity`**, not `xwauth`. This ensures `xwentity` defines its own auth interface, and `xwauth` provides implementations that satisfy those contracts.

Following **GUIDE_DEV.md layering**:

- **Contracts** in `xwentity/src/exonware/xwentity/auth/contracts.py` (`I*` types only).
- **Abstract base classes** in `xwentity/src/exonware/xwentity/auth/base.py` (`A*` types only).
- **Concrete implementations** provided by `xwauth` library (no concrete classes with specific names – this is a design defect).

### 1A.1 Contracts (in `xwentity.auth.contracts`)

Define auth interfaces that `xwentity` requires, following GUIDE_DEV naming: `I*` in contracts:

- **`IEntityAuth`** (auth contract for `XWEntity`)
  - `check_permission(entity: XWEntity, permission: str, user: Any) -> bool`
  - `validate_access(entity: XWEntity, user: Any) -> bool`
  - `get_user_roles(user: Any) -> list[str]`

- **`ICollectionAuth`** (auth contract for `XWCollection`)
  - `check_collection_permission(collection: XWCollection, permission: str, user: Any) -> bool`
  - `validate_collection_access(collection: XWCollection, user: Any) -> bool`

- **`IGroupAuth`** (auth contract for `XWGroup`)
  - `check_group_permission(group: XWGroup, permission: str, user: Any) -> bool`
  - `validate_group_access(group: XWGroup, user: Any) -> bool`

These contracts live in `xwentity` because **`xwentity` owns its auth interface**. Implementations in `xwauth` must satisfy these contracts.

### 1A.2 Abstract Base Classes (in `xwentity.auth.base`)

Add abstract base classes that provide common behaviour but no auth logic:

- **`AEntityAuth(IEntityAuth)`**
  - Common helpers: permission checking patterns, role validation, logging hooks.

- **`ACollectionAuth(ICollectionAuth)`**
  - Common helpers: collection-level permission composition, entity auth delegation.

- **`AGroupAuth(IGroupAuth)`**
  - Common helpers: group-level permission composition, collection/entity auth delegation.

These follow the same **A*/I* pattern used in `xwentity` (`AEntity`, `ACollection`, `AGroup`). All auth implementations (from `xwauth` or elsewhere) can extend these base classes.

### 1A.3 Implementations from `xwauth` (No Named Concrete Classes)

**Important Design Principle**: Concrete auth implementations with specific names **should NOT exist as named classes**. This is a design defect.

Instead:

- **`xwauth`** provides implementations that satisfy `IEntityAuth`, `ICollectionAuth`, and `IGroupAuth` contracts.
- These implementations are accessed through **factory functions or registry patterns** in `xwauth`, not as concrete class names.
- The logic currently in `XWGroup._auth_provider` and any auth-related code in entities/collections/groups moves into `xwauth` implementations.
- `xwauth` implementations must respect **GUIDE_DEV "no duplication"** by reusing existing utilities.

**Example pattern** (not prescriptive, but illustrates the principle):

```python
# In xwauth - factory/registry approach, not concrete classes
from exonware.xwentity.auth.contracts import IEntityAuth

def create_entity_auth(backend: str = "local", **opts) -> IEntityAuth:
    """Factory that returns an IEntityAuth implementation."""
    if backend == "local":
        return _LocalEntityAuth(**opts)  # Internal implementation
    # ... other backends
```

This keeps `xwentity` decoupled from `xwauth` implementation details while `xwauth` provides the actual auth logic.

---

## 2. XWEntity (`entity.py`) – Make It Storage‑Agnostic

### 2.1 What Stays in `XWEntity`

Keep all **entity‑centric** responsibilities:

- Metadata and state: `XWEntityMetadata`, `id`, `type`, `state`, `version`, timestamps.
- Data access and mutation: `get`, `set`, `delete`, `update`, internal `_data_*` helpers.
- Validation: `validate`, `validate_issues`, `_validate`.
- Actions: registration, execution, listing, integration with `xwaction`.
- Performance and extensions: caching, optimization methods, extension registry.

### 2.2 What Moves to `xwstorage` (GUIDE_DEV Layering)

Move the following methods out of `XWEntity` into `xwstorage` implementations (via `IEntityStorage` contract):

- `XWEntity.from_file(...)`
- `XWEntity.save(...)` / `load(...)`
- `XWEntity.to_file(...)` / `load_from_file(...)`
- `XWEntity.from_format(...)` / `to_format(...)`

All file paths, format detection, and low‑level serialization live in `xwstorage`, not inside `xwentity`, to respect **GUIDE_DEV.md** layering:

- `xwsystem` / `xwdata` – platform & data infrastructure.
- `xwstorage` – storage orchestration + manifests.
- `xwentity` – entity modelling & behaviour only.

### 2.3 Optional Thin Delegation API (Facade‑Friendly)

If we want to keep a façade‑style experience for consumers (see `facade.py` and GUIDE_DEV), we can keep **thin helper methods** in `XWEntity` that delegate to a configured storage provider:

- Example:

```python
from exonware.xwentity.storage.contracts import IEntityStorage
from exonware.xwstorage import get_default_entity_storage  # factory function

def save_with(self, storage: IEntityStorage | None = None, **opts) -> None:
    (storage or get_default_entity_storage()).save_entity(self, **opts)

@classmethod
def from_file_with(cls, storage: IEntityStorage | None, path: Path, **opts) -> "XWEntity":
    return (storage or get_default_entity_storage()).from_file(path, **opts)
```

This keeps the convenience while enforcing that **all real storage logic** is implemented in `xwstorage` and governed by the contracts in `xwentity.storage.contracts`.

---

## 3. AEntity (`base.py`) – Remove Direct File IO

`AEntity` should focus on:

- Entity metadata.
- In‑memory data representation and access.
- State transitions and actions.
- Converting to/from native dictionaries.

### 3.1 Methods to Move (to `xwstorage`)

Move these into `xwstorage` implementations (that satisfy `IEntityStorage` and may extend `AEntityStorage`):

- `AEntity._to_file(...)`
- `AEntity._from_file(...)`

Today these call `get_serialization_registry()` and read/write files directly. After refactor:

At the end of the refactor:

- `AEntity` only exposes `_to_dict`, `_from_dict`, `_to_native`, `_from_native` (pure in‑memory transforms).
- Storage providers in `xwstorage` use those methods plus `xwsystem` serializers to perform persistence.
- `AEntity` never references filesystem paths or formats directly, consistent with **GUIDE_DEV "single responsibility per layer"**.

---

## 4. XWCollection (`collection.py`) – Pure Collection Logic

`XWCollection` should only describe **collections of entities**, not where/how they are stored.

### 4.1 What Stays

- Constructor identity:
  - `id`, `entity_type`, `group_id`.
- Collection operations (via `ACollection`):
  - `add`, `remove`, `clear`, `find`, `list_all`, `size`.
- In‑memory representation:
  - `to_dict`, `to_native`.

### 4.2 What Moves to `xwstorage`

Move all path and file handling into `xwstorage` implementations (that satisfy `ICollectionStorage` and may extend `ACollectionStorage`):

- `_get_storage_path(...)`
- `save(self, base_path: Optional[Path] = None)`
- `load(self, base_path: Optional[Path] = None)`

These methods currently:

- Resolve `base_path`, enforce relative paths, and construct on‑disk layout.
- Write and read `.data.xwjson`, `.schemas.xwjson`, `.actions.xwjson`.
- Use `XWData.from_native(...).to_format("xwjson", ...)` and direct file writes.

After refactor:

- `xwstorage` implementations (satisfying `ICollectionStorage`) take a `XWCollection` and are responsible for all of that.
- `XWCollection` is purely in‑memory and testable without touching the filesystem (makes unit tests easier per **GUIDE_TEST.md**).

### 4.3 Optional Delegation Methods (Facade‑Friendly)

If we want to keep the current API surface, `XWCollection.save/load` can become delegates:

```python
from exonware.xwstorage import get_default_collection_storage  # factory function

def save(self, base_path: Optional[Path] = None) -> None:
    get_default_collection_storage().save_collection(self, base_path=base_path)

def load(self, base_path: Optional[Path] = None) -> None:
    get_default_collection_storage().load_collection(self, base_path=base_path)
```

But the implementation details live in `xwstorage`.

---

## 5. XWGroup (`group.py`) – Group Semantics Only

`XWGroup` should manage **collections and sub‑groups**, not storage manifests or auth providers.

### 5.1 What Stays

- Group identity and hierarchy:
  - `_group_id`, `_collections`, `_subgroups`, `_parent_group`.
  - `group_id`, `collection_count`, `collections`, `list_collections`.
  - `create_collection`, `create_group`.
- In‑memory representation:
  - `to_dict`, `to_native`.

### 5.2 What Moves to `xwstorage`

#### Storage/auth providers

- `_storage_provider`, `_auth_provider` fields and constructor parameters:
  - These should reference `IGroupStorage` and `IGroupAuth` contracts (from `xwentity.storage.contracts` and `xwentity.auth.contracts`), not concrete implementations.
  - Implementations are provided by `xwstorage` / `xwauth` via factory functions, not as named classes.
  - These should either:
    - be injected by `xwstorage` / `xwauth` layers, or
    - live on storage/auth‑side façade objects instead of in the core group.

#### Group persistence

Move the following into `xwstorage` implementations (that satisfy `IGroupStorage` and may extend `AGroupStorage`):

- `save_all(...)`
  - `_sanitize_data(...)`.
  - `_collect_group_data(...)`.
  - `_save_to_storage_async(...)` that builds and writes the `xwstorage.xwjson` manifest:
    - `{"source": "xwstorage", "address": "data/xwstorage.xwjson", "backend": "local", "format": "xwjson", "groups": ...}`.
- `load_all(...)`
  - Everything related to `group_file = base_path / f"{self._group_id}.xwjson"` and reconstructing collections/entities.

`XWGroup.save/load` wrappers should either:

- Delegate to `IGroupStorage`, or
- Be removed, with callers going through `xwstorage` explicitly.

In both cases, **XWGroup remains a pure group façade**, consistent with `facade.py` and GUIDE_DEV's façade guidance.

---

## 6. xwsystem – Shared Serialization Layer

Most low‑level serialization is already correctly placed in `xwsystem` / `xwdata`:

- `get_serialization_registry()`
- `XWData`, `XWSchema`, and related IO utilities.

The key rule after refactor:

- **`xwentity` never directly calls `get_serialization_registry()` or manipulates filesystem paths.**
- The flow becomes:
  - `xwentity` ⇄ `xwstorage` ⇄ `xwsystem` serializers / `xwdata`.

If any generic serialization helpers remain in `xwentity`, they should be moved to:

- `xwstorage` (if they depend on entity/collection/group concepts), or
- `xwsystem.io.serialization` (if they are generic).

This respects **GUIDE_DEV "never reinvent the wheel"** by always going through `xwsystem` for core serialization behaviour.

---

## 7. Testing Strategy (GUIDE_TEST.md Compliance)

All changes in this proposal must be validated using the **standard eXonware testing hierarchy** from `GUIDE_TEST.md` (`0.core`, `1.unit`, `2.integration`, `3.advance`) and xwentity‑specific markers.

### 7.1 Test Layers to Update

- **Core tests (`xwentity/tests/0.core/`)**
  - Ensure **end‑to‑end flows** using entities, collections, and groups still work when routed through `xwstorage` (local file backend).
  - Add/adjust `@pytest.mark.xwentity_core` tests that:
    - Create entities and collections.
    - Persist them using the new storage layer.
    - Reload and validate equality (schema, data, actions, metadata).

- **Unit tests (`xwentity/tests/1.unit/`)**
  - Focus on **in‑memory behaviour** only (no filesystem):
    - `AEntity`, `XWEntity`: metadata, caching, actions, validation.
    - `ACollection`, `XWCollection`: add/remove/find/list logic.
    - `AGroup`, `XWGroup`: group and subgroup management without IO.
  - For storage‑specific behaviour, add unit tests under **`xwstorage/tests/1.unit/`**, mirroring `xwstorage` source modules.

- **Integration tests (`xwentity/tests/2.integration/` and `xwstorage/tests/2.integration/`)**
  - Cross‑module tests that verify **`xwentity` + `xwstorage` + `xwsystem`** integration:
    - End‑to‑end flows that persist entities using actual `xwstorage.xwjson` manifests.
    - Tests should be marked `@pytest.mark.xwentity_integration` or `@pytest.mark.xwstorage_integration` as appropriate.

- **Advance tests (`xwentity/tests/3.advance/`, `xwstorage/tests/3.advance/`)**
  - Optional until v1.0.0, but recommended for:
    - **Performance**: ensure moving IO to `xwstorage` does not regress entity performance (or clearly isolates it).
    - **Security**: path validation and serialization remain safe when centralized.

### 7.2 Runners & Reports

- Keep the **hierarchical runners** exactly as defined in `GUIDE_TEST.md`:
  - `tests/runner.py` (orchestrator) – only here we persist Markdown summaries under `docs/tests/`.
  - Layer runners (`tests/0.core/runner.py`, `tests/1.unit/runner.py`, etc.) – no file writes, just stdout.

- Ensure new tests for `xwstorage` and updated `xwentity` tests:
  - Use **library‑specific markers** (`xwentity_core`, `xwentity_unit`, `xwstorage_core`, etc.).
  - Are runnable via existing runners without adding forbidden pytest flags (no `--disable-warnings`, no `--maxfail=10`, etc., as per GUIDE_TEST).

### 7.3 Error‑Fixing & Regression Policy

Any failures introduced by this refactor must follow **GUIDE_DEV / GUIDE_TEST error‑fixing philosophy**:

- Never hide or skip failing tests – fix root causes.
- Add **regression tests** in the appropriate layer (usually `1.unit` + `0.core` or `2.integration`).
- Do not lower performance or quality thresholds to "make tests pass"; optimize or correct design instead.

---

## 8. Migration Plan

### Step 1 – Introduce Storage and Auth Interfaces and Implementations

- Add `IEntityStorage`, `ICollectionStorage`, and `IGroupStorage` to `xwentity.storage.contracts`.
- Add `AEntityStorage`, `ACollectionStorage`, and `AGroupStorage` to `xwentity.storage.base`.
- Add `IEntityAuth`, `ICollectionAuth`, and `IGroupAuth` to `xwentity.auth.contracts`.
- Add `AEntityAuth`, `ACollectionAuth`, and `AGroupAuth` to `xwentity.auth.base`.
- Implement storage providers in `xwstorage` (via factory/registry patterns, not named concrete classes) by **copying** logic from `xwentity` (without changing behaviour).
- Implement auth providers in `xwauth` (via factory/registry patterns, not named concrete classes) to satisfy `xwentity.auth` contracts.

### Step 2 – Wire Delegation from xwentity

- Update `XWEntity`, `XWCollection`, and `XWGroup` to:
  - Either provide **delegation helpers** (e.g. `save_with`, `load_with`).
  - Or drop direct file/format methods entirely in favour of `xwstorage` APIs.

### Step 3 – Update Call Sites (Examples & Tests – GUIDE_TEST)

- Update all examples and tests (e.g. `xwentity/examples`, `xwentity/tests`) that use:
  - `XWEntity.from_file`, `.save`, `.to_file`, `.from_format`, `.to_format`.
  - `XWCollection.save/load`.
  - `XWGroup.save_all/load_all`.
- Replace them with calls through:
  - `xwstorage` storage providers, or
  - New thin delegation methods if we keep them.

### Step 4 – Tighten Boundaries

- Once all call sites are migrated and tests pass:
  - Deprecate, then remove any remaining direct file/format methods from `xwentity` that bypass `xwstorage`.
  - Ensure new storage‑related features are added only to `xwstorage` and not back into `xwentity`.

---

## 9. End State

After this refactor:

- **`xwentity`**: focused, purely responsible for entity modelling, state, actions, validation, collections, and groups as in‑memory constructs.
- **`xwstorage`**: the single place for persistence concerns of entities/collections/groups, including local files and `xwstorage.xwjson` manifests.
- **`xwsystem`**: shared serialization + plumbing used by `xwstorage`, but never called directly from `xwentity` for IO.

This separation makes it easier to:

- Swap or extend storage backends without touching entity logic.
- Reuse `xwentity` in contexts where persistence is not file‑based (in‑memory, remote, database, etc.).
- Keep security and path validation logic centralized in `xwstorage` rather than spread around entity code.
