# API Reference — xwmodels

**Library:** exonware-xwmodels  
**Version:** 0.0.1  
**Last Updated:** 08-Mar-2026

Canonical API reference (output of GUIDE_15_API). Complete, stable, navigable, example-driven.

---

## Overview

- **Provides:** Entity models (BaaS-style): XWGroup/XWModelGroup, XWModelCollection[TEntity: XWModelEntity], XWModelEntity (compat facade over xwentity). Storage/auth provider contracts.
- **For:** Downstream libs (xwbase, xwapi, xwauth, xwstorage) and app developers.
- **Modes:** lite (default), `[lazy]`, `[full]` per pyproject.toml.

---

## Quick Start

```python
from exonware.xwmodels import XWGroup, XWModelCollection, XWModelEntity
from pathlib import Path

group = XWGroup("my_group", base_path=Path("./data"))
coll = group.create_collection("users", entity_type="user")
entity = XWModelEntity(schema={...}, data={"name": "Alice"})
coll.add(entity)
group.save_all()
```

---

## Public Facades

### XWGroup (alias XWModelGroup)

- **Purpose:** Group of collections; optional parent; subgroups.
- **Constructor:** `XWGroup(id, base_path=None, title=None, description=None, storage=None, auth=None, group=None)`
- **Key methods:** `create_collection(id, entity_type)`, `create_subgroup(id, ...)`, `save_all()`, `load_all()`
- **Storage:** Requires IGroupStorage for save_all/load_all.

### XWModelCollection[TEntity: XWModelEntity]

- **Purpose:** Collection of entities with generic type; one schema, multiple data.
- **Constructor:** `XWModelCollection(id, entity_type, group_id=None, base_path=None)`
- **Key methods:** `add(entity: TEntity)`, `remove(entity_id)`, `find(predicate)`, `save()`, `load()`
- **Generic:** `TEntity` must be `XWModelEntity` (or compatible subclass); type-safe add/find.

### XWModelEntity

- **Purpose:** xwmodels compatibility facade built over `exonware.xwentity.XWEntity` (schema + actions + data with model-friendly constructors/helpers).
- **Compatibility alias:** `XWEntity` remains available as an alias to `XWModelEntity`.
- **Core behavior:** [xwentity REF_15_API](../../xwentity/docs/REF_15_API.md)

---

## Model management layer usage

- **Base system modeling:** create one group per bounded system (`auth`, `billing`, `catalog`, `content`), then map one collection per aggregate/model type.
- **Environment partitioning:** use nested groups for `dev/staging/prod` or tenant segmentation while keeping the same API surface.
- **Provider-driven orchestration:** wire storage/auth providers at group level so policy and persistence behavior is enforced consistently across collections.
- **Operational consistency:** keep schema contracts per collection and action/data semantics per entity model, enabling safe scaling of base systems.

---

## Storage Contracts

| Interface | Purpose |
|-----------|---------|
| IEntityStorage | Save/load entity |
| ICollectionStorage | Save/load collection |
| IGroupStorage | Save/load group |

**Helpers:** `create_entity_storage_group(group=None, storage=...)`, `create_entity_storage_collection(group, collection_id, entity_type, storage=...)`

---

## Auth Contracts

| Interface | Purpose |
|-----------|---------|
| IEntityAuth | Entity auth checks |
| ICollectionAuth | Collection auth checks |
| IGroupAuth | Group auth checks |

---

## Data Models & Contracts

- **IEntity, ICollection, IGroup** — contracts (contracts.py)
- **ACollection[TEntity], AGroup** — abstract bases (base.py)
- **EntityType, EntityID, EntityData** — defs (defs.py)

---

## Errors

| Exception | Meaning | Next step |
|-----------|---------|-----------|
| XWEntityError | Base for all entity errors | Check subclass message |
| XWEntityValidationError | Schema/data validation failed | Fix input or schema |
| XWEntityStateError | Invalid state transition | Ensure valid state flow |
| XWEntityActionError | Action execution failed | Check action logic/inputs |
| XWEntityNotFoundError | Entity/item not found | Check id/path |

---

## Compatibility & Deprecations

- **Version:** 0.0.1.x — Alpha; API may evolve before 1.0.
- **Python:** >=3.12.

---

## Links

- [REF_14_DX.md](REF_14_DX.md) — DX contract  
- [REF_13_ARCH.md](REF_13_ARCH.md) — Architecture  
- [GUIDE_41_DOCS.md](../../docs/guides/GUIDE_41_DOCS.md) — Doc standards  
- [xwentity REF_15_API](../../xwentity/docs/REF_15_API.md) — Core entity engine API
