# Architecture Reference — exonware-xwmodels

**Library:** exonware-xwmodels  
**Version:** 0.0.1  
**Last Updated:** 08-Mar-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md) sec. 7, 6, 5

---

## Overview

xwmodels provides **entity models** (BaaS-style): **groups** (optional parent, subgroups), **collections** (one schema, multiple entities), and **entities** (from xwentity). It **extends xwentity** with generic types and adds storage/auth provider contracts, lifecycle, relationships, cache, and BaaS entities (Project, App, Invoice, etc.) for Firebase Firestore parity. Design: simple hierarchy and contracts; logic delegates to xwentity and optional xwstorage/xwauth.

**Design philosophy:** Contract-first; generic types for type safety; group → collection → entity; storage and auth via provider interfaces.

---

## Generic Types and xwentity Injection

| Model concept | xwmodels type | Source | Notes |
|---------------|---------------|-------|-------|
| **Entity model** | `XWModelEntity` | `entity_compat.py` + `exonware.xwentity` | Compatibility facade over core xwentity engine |
| **Collection model** | `XWModelCollection[TEntity: XWModelEntity]` | `collection.py` | Generic over entity type; extends `ACollection[TEntity]` |
| **Group model** | `XWGroup` (alias `XWModelGroup`) | `group.py` | Extends `AGroup`; `create_collection` returns `XWModelCollection` |

**Why generic types:** Type-safe `add(entity: TEntity)`, `find(...) -> list[TEntity]`; IDE autocomplete; refactoring safety.

---

## High-Level Structure

```
xwmodels/
+-- contracts.py      # IEntity, ICollection, IGroup
+-- base.py           # ACollection[TEntity], AGroup; XWObject
+-- facade.py         # Public API
+-- group.py          # XWGroup (XWModelGroup, AGroup); parent, subgroups, create_collection
+-- collection.py     # XWModelCollection[TEntity: XWModelEntity] (ACollection[TEntity]); add, find, save
+-- cache.py          # XWEntityCache
+-- auth/             # IEntityAuth, ICollectionAuth, IGroupAuth; A* bases
+-- storage/          # IEntityStorage, ICollectionStorage, IGroupStorage; integration
+-- common/
|   +-- lifecycle/    # LifecycleManager, ILifecycleManager, ILifecycleWorkflow
|   +-- relationships.py, enhanced.py  # EntityRelationship, RelationshipManager
+-- entities/baas/    # Project, App, Deployment; Invoice, Payment, Subscription, Plan
+-- config.py, defs.py, errors.py, version.py
```

**Entry points:** `exonware.xwmodels` (facade, XWGroup, XWModelCollection, XWModelEntity; `XWEntity` kept as compatibility alias).

---

## Module Breakdown

### Group (`group.py`)

**Purpose:** Hierarchy root; optional parent group; subgroups; create_collection, create_subgroup.

**Key types:** XWGroup (alias XWModelGroup; AGroup, XWObject); optional IGroupStorage, IGroupAuth; save_all/load_all delegate to storage. `create_collection(id, entity_type)` returns `XWModelCollection`.

### Collection (`collection.py`)

**Purpose:** One schema, multiple entities; generic over entity type; file layout group_id/collection_id.*.xwjson.

**Key types:** `XWModelCollection[TEntity: XWModelEntity]` (ACollection[TEntity], XWObject); add(entity: TEntity), find, save.

### Entity

**Purpose:** `XWModelEntity` compatibility facade over **xwentity** core (`exonware.xwentity.XWEntity`). Schema + list of actions + data; actions per entity.

### Storage (`storage/`)

**Purpose:** IEntityStorage, ICollectionStorage, IGroupStorage; A* bases; XWEntityStorageGroup wraps XWGroup with IGroupStorage.

### Auth (`auth/`)

**Purpose:** IEntityAuth, ICollectionAuth, IGroupAuth; A* bases.

### Lifecycle (`common/lifecycle/`)

**Purpose:** LifecycleManager, ILifecycleManager, ILifecycleWorkflow; state transitions for entities.

### Relationships (`common/relationships*.py`)

**Purpose:** EntityRelationship, RelationshipManager, GraphRelationshipManager.

### Cache (`cache.py`)

**Purpose:** XWEntityCache.

### BaaS entities (`entities/baas/`)

**Purpose:** Project, App, Deployment; Invoice, Payment, Subscription, Plan.

---

## Dependencies

- **xwentity** — Unified core entity engine; xwmodels wraps it as `XWModelEntity` and does not re-implement it.

---

## Practical model-management usage

- Build **base systems** by allocating one root group per bounded context (`auth`, `billing`, `catalog`).
- Under each group, keep one collection per aggregate type (`users`, `roles`, `invoices`, `products`).
- Use subgroups for environment and tenant partitioning without changing APIs.
- Attach storage/auth providers at group boundaries so persistence and policy behavior are applied consistently across all collections in that system.
- **xwsystem, xwschema, xwdata, xwnode, xwaction** — Core stack.
- **xwauth, xwstorage** — Optional providers.

---

## Layering (eXonware)

xwmodels sits in **Domain Models**: consumes xwentity (Domain Entities); consumed by xwbase, xwapi, xwauth, xwstorage.

---

## Related Documents

- [REF_01_REQ.md](REF_01_REQ.md) — Requirements (vision: entities, collections, groups, generic types)
- [REF_12_IDEA.md](REF_12_IDEA.md) — Ideas (generic types, xwentity injection)
- [REF_22_PROJECT.md](REF_22_PROJECT.md) — Requirements and status
- [GUIDE_13_ARCH.md](../../docs/guides/GUIDE_13_ARCH.md) — Architecture guide
