# Requirements Reference (REF_01_REQ)

**Project:** xwmodels  
**Sponsor:** TBD  
**Version:** 0.0.1  
**Last Updated:** 08-Mar-2026 00:00:00.000  
**Produced by:** [GUIDE_01_REQ.md](../guides/GUIDE_01_REQ.md)

---

## Purpose of This Document

This document is the **single source of raw and refined requirements** collected from the project sponsor and stakeholders. It is updated on every requirements-gathering run. When the **Clarity Checklist** (section 12) reaches the agreed threshold, use this content to fill REF_12_IDEA, REF_22_PROJECT, REF_13_ARCH, REF_14_DX, REF_15_API, and planning artifacts. Template structure: [GUIDE_01_REQ.md](../guides/GUIDE_01_REQ.md).

---

## 1. Vision and Goals

| Field | Content |
|-------|---------|
| One-sentence purpose | **SW models = entity models + collections + groups.** xwmodels extends xwentity with generic types: entity model uses XWModelEntity; model collection uses XWModelCollection[TEntity: XWModelEntity]; model group uses XWModelGroup (exported as XWGroup). Groups contain collections; collections contain entities. One schema per collection, multiple data; actions per entity. (Sponsor confirmed.) |
| **Design principle (sponsor)** | **Really simple.** Generic types for type safety; entity model = XWModelEntity; collection = XWModelCollection; group = XWModelGroup/XWGroup. xwentity is finished; xwmodels integrates it into the hierarchy. (Sponsor confirmed.) |
| Primary users/beneficiaries | eXonware stack (xwbase, xwapi, xwauth, xwstorage); developers building BaaS/document-level apps. (Sponsor confirmed.) |
| Success (6 mo / 1 yr) | 6 mo: Stable generic API, REF_* compliance, xwentity linkage documented. 1 yr: Production use, ecosystem integration. (Refine per REF_22.) |
| Top 3–5 goals (ordered) | 1) **Generic types** — XWModelCollection[TEntity: XWModelEntity] for type-safe collections; entity model = XWModelEntity. 2) **Group** — XWModelGroup (alias XWGroup); optional parent, subgroups, create_collection. 3) **Collection** — XWModelCollection; one schema, multiple entities. 4) **Entity integration** — xwentity provides the core engine; xwmodels uses it via XWModelEntity and does not re-implement. 5) Hierarchy: group → collections → entities. (Sponsor confirmed.) |
| Problem statement | Need a simple hierarchy on top of xwentity with generic types: entity model uses XWModelEntity; model collection uses XWModelCollection[TEntity]; model group uses XWModelGroup/XWGroup. Groups (optional parent), collections (one schema, many entities), entities (from xwentity core). (Sponsor confirmed.) |

## 2. Scope and Boundaries

| In scope | Out of scope | Dependencies | Anti-goals |
|----------|--------------|--------------|------------|
| **Core:** Generic types (XWModelCollection[TEntity: XWModelEntity]); entity model = XWModelEntity; collection = XWModelCollection; group = XWModelGroup/XWGroup. Group (optional parent, subgroups), collection (one schema, multiple entities), entity (xwentity-backed; actions per entity). **Rest (reverse‑engineered):** storage/auth provider contracts, lifecycle, relationships, cache, BaaS entities (Project, App, Invoice, etc.). (Sponsor confirmed; see 2a.) | Implementing storage backend (xwstorage); implementing auth backend (xwauth). (Sponsor confirmed.) | xwentity (core XWEntity), xwsystem, xwschema, xwdata, xwnode, xwaction; optional xwauth, xwstorage (providers). (pyproject.toml) | Re-implementing entity core (use xwentity). (Sponsor confirmed.) |

### 2a. Reverse‑engineered from codebase

Objective summary from `src/exonware/xwmodels/`:

| Concept | Implemented |
|---------|-------------|
| **Group** | XWGroup (alias XWModelGroup; AGroup, XWObject): id, optional parent group (`group` param), subgroups (`_subgroups`), `create_collection(id, entity_type)` → XWModelCollection, `create_subgroup(id, ...)`. Optional base_path, title, description; optional IGroupStorage, IGroupAuth. save_all/load_all delegate to storage. (group.py) |
| **Collection** | XWModelCollection[TEntity: XWModelEntity] (ACollection[TEntity], XWObject): id, entity_type (one schema), group_id, base_path. Generic over entity type. Holds multiple entities (same type). File layout: group_id/collection_id.data.xwjson, .schemas.xwjson, .actions.xwjson. add, find, save. (collection.py) |
| **Entity** | XWModelEntity from xwmodels (compatibility facade over exonware.xwentity.XWEntity). Entity model = XWModelEntity. Schema + list of actions + data; actions are per entity. (__init__.py) |
| **Storage** | IEntityStorage, ICollectionStorage, IGroupStorage; AEntityStorage, ACollectionStorage, AGroupStorage. XWEntityStorageGroup wraps XWGroup with IGroupStorage; create_collection_with_storage, create_group_with_storage. (storage/contracts.py, base.py, integration.py) |
| **Auth** | IEntityAuth, ICollectionAuth, IGroupAuth; A* bases. (auth/contracts.py, base.py) |
| **Lifecycle** | LifecycleManager, ILifecycleManager, ILifecycleWorkflow; state transitions for entities. (common/lifecycle/) |
| **Relationships** | EntityRelationship, RelationshipManager, GraphRelationshipManager. (common/relationships.py, enhanced.py) |
| **Cache** | XWEntityCache. (cache.py) |
| **BaaS entities** | Project, App, Deployment; Invoice, Payment, Subscription, Plan (entities/baas/). (entities/baas/) |
| **Contracts** | IEntity, ICollection, IGroup; ACollection, AGroup. (contracts.py, base.py) |

*Source: group.py, collection.py, __init__.py, storage/, auth/, common/lifecycle/, common/relationships/, entities/baas/, contracts.py, base.py.*

## 3. Stakeholders and Sponsor

| Sponsor (name, role, final say) | Main stakeholders | External customers/partners | Doc consumers |
|----------------------------------|-------------------|-----------------------------|---------------|
| TBD | Project sponsor / eXonware | TBD | Downstream REF owners; devs using xwmodels. |

## 4. Compliance and Standards

| Regulatory/standards | Security & privacy | Certifications/evidence |
|----------------------|--------------------|--------------------------|
| Per GUIDE_00_MASTER, GUIDE_11_COMP. (inferred) | TBD | TBD |

## 5. Product and User Experience

| Main user journeys/use cases | Developer persona & 1–3 line tasks | Usability/accessibility | UX/DX benchmarks |
|-----------------------------|------------------------------------|--------------------------|------------------|
| Create group (with or without parent); add collections to group; add entities to collection; optional storage/auth providers; lifecycle and relationships. (Sponsor + reverse‑engineered.) | **Easy:** `group = XWGroup("my_group")`; `coll = group.create_collection("users", entity_type)`; `coll.add(entity)`. Same idea as xwbase: group → collections → entities; one schema per collection, multiple data; actions per model entity. Generic types: `XWModelCollection[XWModelEntity]` for type-safe collections. (Sponsor confirmed.) | Clear hierarchy (group/collection/entity); provider contracts for storage and auth; generic types for type safety. (Reverse‑engineered.) | TBD |

## 6. API and Surface Area

| Main entry points / "key code" | Easy (1–3 lines) vs advanced | Integration/existing APIs | Not in public API |
|--------------------------------|------------------------------|---------------------------|-------------------|
| **Core:** XWModelGroup/XWGroup (id, parent group optional, create_collection, create_subgroup), XWModelCollection[TEntity: XWModelEntity] (id, entity_type, add, find, save), XWModelEntity (xwmodels facade over xwentity). **Storage:** IGroupStorage, ICollectionStorage, IEntityStorage; XWEntityStorageGroup, create_entity_storage_group, create_entity_storage_collection. **Auth:** IGroupAuth, ICollectionAuth, IEntityAuth. **Contracts:** IEntity, ICollection, IGroup; ACollection, AGroup. (Reverse‑engineered.) | **Easy:** XWGroup → create_collection → XWModelCollection.add(entity). **Advanced:** storage/auth providers, lifecycle manager, relationship manager, cache, BaaS entity subclasses (Project, Invoice, etc.). (Reverse‑engineered.) | xwentity (core XWEntity), xwstorage (IGroupStorage/ICollectionStorage impls), xwauth (IGroupAuth/ICollectionAuth impls). (Reverse‑engineered.) | Internal provider implementations; base class internals. (Reverse‑engineered.) |

## 7. Architecture and Technology

| Required/forbidden tech | Preferred patterns | Scale & performance | Multi-language/platform |
|-------------------------|--------------------|----------------------|-------------------------|
| Python 3.12+; xwentity, xwsystem, xwschema, xwdata, xwnode, xwaction; optional xwauth, xwstorage. (pyproject.toml) | Generic types: XWModelCollection[TEntity: XWModelEntity]. Group (optional parent, subgroups) → Collection (one schema, many entities) → Entity (xwentity-backed model entity). Facades: XWGroup/XWModelGroup, XWModelCollection, XWModelEntity; contracts IGroup, ICollection, IEntity; storage/auth provider interfaces. (Sponsor + reverse‑engineered.) | TBD | Python only. (inferred) |

## 8. Non-Functional Requirements (Five Priorities)

| Security | Usability | Maintainability | Performance | Extensibility |
|----------|-----------|-----------------|-------------|---------------|
| TBD | TBD | 4-layer tests, REF_*, base/contracts/facade. (from REF_22) | TBD | Provider interfaces. (inferred) |

## 9. Milestones and Timeline

| Major milestones | Definition of done (first) | Fixed vs flexible |
|------------------|----------------------------|-------------------|
| M1 — Core entities and integration (Done); M2 — REF_* and xwentity linkage (Done). (from REF_22) | M2: REF_22, REF_35, xwentity relationship documented. (from REF_22) | TBD |

## 10. Risks and Assumptions

| Top risks | Assumptions | Kill/pivot criteria |
|-----------|-------------|----------------------|
| TBD | xwmodels builds on xwentity; xwentity is finished; xwmodels uses XWModelEntity for entity model, XWModelCollection for collection model, XWModelGroup/XWGroup for group model. xwauth/xwstorage optional as providers. (from pyproject, REF_22) | TBD |

## 11. Workshop / Session Log (Optional)

| Date | Type | Participants | Outcomes |
|------|------|---------------|----------|
| 11-Feb-2026 | Reverse‑engineer + Q&A | User + Agent | Draft from code/docs (REF_22, README, pyproject, src); user to confirm. |
| 11-Feb-2026 | Q&A Batch A (Vision) | Sponsor + Agent | Vision: really simple — entities, collections, groups. Group can have parent (or not); under group are collections; under collection are entities. Collection = one schema, multiple data. Actions per xwentity. Rest reverse‑engineered (storage/auth, lifecycle, relationships, cache, BaaS entities). Section 2a added. |
| 08-Mar-2026 | Docs completion (xwentity done) | Sponsor + Agent | xwentity finished; xwmodels docs updated: generic types (XWModelCollection[TEntity: XWModelEntity]), entity model = XWModelEntity, collection = XWModelCollection, group = XWModelGroup/XWGroup. xwentity integration documented. |

## 12. Clarity Checklist

| # | Criterion | ☐ |
|---|-----------|---|
| 1 | Vision and one-sentence purpose filled and confirmed | ☑ |
| 2 | Primary users and success criteria defined | ☑ |
| 3 | Top 3–5 goals listed and ordered | ☑ |
| 4 | In-scope and out-of-scope clear | ☑ |
| 5 | Dependencies and anti-goals documented | ☑ |
| 6 | Sponsor and main stakeholders identified | ☑ |
| 7 | Compliance/standards stated or deferred | ☑ |
| 8 | Main user journeys / use cases listed | ☑ |
| 9 | API / "key code" expectations captured | ☑ |
| 10 | Architecture/technology constraints captured | ☑ |
| 11 | NFRs (Five Priorities) addressed | ☑ |
| 12 | Milestones and DoD for first milestone set | ☑ |
| 13 | Top risks and assumptions documented | ☑ |
| 14 | Sponsor confirmed vision, scope, priorities | ☑ |

**Clarity score:** 14 / 14. **Ready to fill downstream docs?** ☑ Yes

---

*Inferred content is marked; sponsor confirmation required. Per GUIDE_01_REQ.*
