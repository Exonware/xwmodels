# Project Reference — xwmodels

**Library:** exonware-xwmodels  
**Last Updated:** 08-Mar-2026

Per REF_35_REVIEW.

---

## Vision

xwmodels provides **entity models** (BaaS-style): entities, collections, groups, auth, cache, lifecycle, relationships, storage integration. It **extends xwentity** with generic types (XWModelCollection[TEntity: XWModelEntity]) and higher-level document/collection models for Firebase Firestore parity.

---

## Goals

1. **Entity models:** BaaS entities, collections, groups; generic types for type safety.
2. **xwentity integration:** Entity model = XWModelEntity; collection = XWModelCollection; group = XWModelGroup (exported as XWGroup). xwentity is finished; xwmodels uses it.
3. **Auth and storage integration:** Link to xwentity and xwstorage; document model parity.
4. **Traceability:** REF_22_PROJECT, REF_35_REVIEW, logs; relationship to xwentity documented.

---

## Functional Requirements (Summary)

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | Entity and collection models | High | Done |
| FR-002 | Generic types (XWModelCollection[TEntity: XWModelEntity]) | High | Done |
| FR-003 | Auth and storage integration | High | Done |
| FR-004 | Base, contracts, facade; entities/baas | High | Done |
| FR-005 | 4-layer tests | High | Done |
| FR-006 | REF_* docs (REQ, IDEA, ARCH, DX, API, PLAN) | High | Done |

---

## Project Status Overview

- **Current phase:** Alpha (Medium). xwentity is finished; xwmodels uses XWModelEntity for the entity model, XWModelCollection for the collection model, and XWModelGroup/XWGroup for the group model. Generic types documented.
- **Docs:** REF_01_REQ, REF_12_IDEA, REF_13_ARCH, REF_14_DX, REF_15_API, REF_21_PLAN, REF_22_PROJECT (this file), REF_35_REVIEW; logs/reviews/.

---

## Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| M1 — Core entities and integration | v0.x | Done |
| M2 — REF_* and xwentity linkage | v0.x | Done |
| M3 — Generic types and docs completion | v0.x | Done (08-Mar-2026) |

---

*See GUIDE_22_PROJECT.md. Review: REF_35_REVIEW.md.*
