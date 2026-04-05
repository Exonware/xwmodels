# Idea Reference — exonware-xwmodels (REF_12_IDEA)

**Company:** eXonware.com  
**Author:** eXonware Backend Team  
**Email:** connect@exonware.com  
**Version:** 0.0.1  
**Last Updated:** 08-Mar-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md)  
**Producing guide:** [GUIDE_12_IDEA.md](../../docs/guides/GUIDE_12_IDEA.md)

---

## Overview

xwmodels provides **entity models** (BaaS-style): entities, collections, groups, auth, cache, lifecycle, relationships, storage integration. It **extends xwentity** with generic types and higher-level document/collection models for Firebase Firestore parity. This document captures ideas and strategic direction; approved ideas graduate to [REF_22_PROJECT.md](REF_22_PROJECT.md) and [REF_13_ARCH.md](REF_13_ARCH.md).

### Alignment with eXonware Five Priorities

- **Security:** Auth and storage provider contracts; path/scope checks.
- **Usability:** Simple hierarchy: group → collections → entities; generic types for type safety (per REF_01).
- **Maintainability:** Contracts, base, facade; link to xwentity/xwstorage in REF_22.
- **Performance:** Cache (XWEntityCache); storage delegation.
- **Extensibility:** Storage/auth providers; BaaS entities (Project, App, Invoice, etc.).

**Related Documents:**
- [REF_01_REQ.md](REF_01_REQ.md) — Requirements source (vision: entities, collections, groups, generic types)
- [REF_22_PROJECT.md](REF_22_PROJECT.md) — Requirements and status
- [REF_13_ARCH.md](REF_13_ARCH.md) — Architecture
- [GUIDE_12_IDEA.md](../../docs/guides/GUIDE_12_IDEA.md) — Idea process

---

## Active Ideas

### ✅ [IDEA-001] xwentity Link and REF_13

**Status:** ✅ Approved → Done  
**Date:** 11-Feb-2026  
**Champion:** eXonware

**Problem:** REF_12 and REF_13 were missing; traceability to xwentity and xwstorage should be explicit in REF_22 and architecture.

**Proposed Solution:** Add REF_12_IDEA (this document); add REF_13_ARCH with module breakdown (group, collection, entity, storage, auth, lifecycle, relationships, cache, BaaS entities); document xwentity/xwstorage linkage in REF_22.

**Next Steps:** Done. REF_13_ARCH added; REF_22 updated.

---

### ✅ [IDEA-002] Generic Types and xwentity Injection

**Status:** ✅ Approved → Implemented  
**Date:** 08-Mar-2026  
**Champion:** eXonware

**Problem:** xwentity is finished; xwmodels must clearly document how it injects xwentity into the model hierarchy and uses generic types for type safety.

**Proposed Solution:**

1. **Entity model = XWModelEntity** — xwmodels exposes `XWModelEntity` (compatibility facade over `exonware.xwentity.XWEntity`); no core re-implementation.

2. **Generic collection** — `XWModelCollection[TEntity: XWModelEntity]` extends `ACollection[TEntity]`; bounds ensure type-safe add/find/remove.

3. **Model group = XWGroup** — `XWGroup` (alias for `XWModelGroup`) extends `AGroup`; `create_collection` returns `XWModelCollection`.

4. **Mapping:**
   - Entity model → XWModelEntity (facade over xwentity core)
   - Collection model → XWModelCollection[TEntity: XWModelEntity]
   - Group model → XWGroup (XWModelGroup)

**Why generic types:** Type-safe collections; IDE autocomplete; refactoring safety.

**Implemented:** 08-Mar-2026 and refined naming on 30-Mar-2026. `collection.py` defines `XWModelCollection[TEntity: XWModelEntity]`; `group.py` defines `XWModelGroup` with `XWGroup = XWModelGroup` alias.

---

## Idea Archive

*(Completed or rejected ideas with rationale.)*

---

*Output of GUIDE_12_IDEA. For requirements see REF_22_PROJECT.md; for architecture see REF_13_ARCH.md.*
