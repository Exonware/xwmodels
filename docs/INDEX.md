# Documentation index — xwmodels

**Last Updated:** 08-Mar-2026

Navigation hub for xwmodels docs. Per GUIDE_41_DOCS and GUIDE_00_MASTER.

---

## Document Types: Ref vs Log

| Type | Purpose | Location |
|------|---------|----------|
| **REF_*** | Authoritative current state (WHAT). Output of GUIDE_*. | `docs/REF_*.md` |
| **Log docs** | Evidence, time-ordered. CHANGE_*, PROJECT_*, TEST_*, etc. | `docs/logs/`, `docs/changes/` |

**Ref docs** = single source of truth. **Log docs** = historical evidence of changes, milestones, test runs.

---

## References (REF_*)

| Document | Purpose | Producing guide |
|----------|---------|------------------|
| [REF_01_REQ.md](REF_01_REQ.md) | Requirements from sponsor (vision, generic types, xwentity injection) | GUIDE_01_REQ |
| [REF_12_IDEA.md](REF_12_IDEA.md) | Active ideas (generic types, xwentity injection) | GUIDE_12_IDEA |
| [REF_13_ARCH.md](REF_13_ARCH.md) | Architecture (entity model, collection, group; generic types) | GUIDE_13_ARCH |
| [REF_14_DX.md](REF_14_DX.md) | DX contract (happy paths, errors, key code) | GUIDE_14_DX |
| [REF_15_API.md](REF_15_API.md) | API reference (XWGroup, XWModelCollection, XWEntity) | GUIDE_15_API |
| [REF_21_PLAN.md](REF_21_PLAN.md) | Lifecycle and planning templates | GUIDE_21_PLAN |
| [REF_22_PROJECT.md](REF_22_PROJECT.md) | Vision, requirements, status, milestones | GUIDE_22_PROJECT |
| [REF_35_REVIEW.md](REF_35_REVIEW.md) | Review summary and status | GUIDE_35_REVIEW |
| [REF_51_TEST.md](REF_51_TEST.md) | Test status and coverage | GUIDE_51_TEST |

---

## Usage

| Document | Purpose |
|----------|---------|
| [GUIDE_01_USAGE.md](GUIDE_01_USAGE.md) | How to use xwmodels (GUIDE_41_DOCS) |

---

## Logs and Changes

| Path | Purpose |
|------|---------|
| [logs/reviews/](logs/reviews/) | REVIEW_* (GUIDE_35_REVIEW) |
| [logs/project/](logs/project/) | PROJECT_* milestone evidence |
| [logs/plans/](logs/plans/) | PLAN_* (additional plans) |
| [changes/](changes/) | CHANGE_* implementation notes |

---

## Other

| Path | Purpose |
|------|---------|
| [_archive/](_archive/) | PROJECT_PHASES, BEAUTIFUL_USER_ENTITY, STANDALONE_REFACTOR, XWENTITY_STORAGE_*, etc. |

---

*Per GUIDE_00_MASTER and GUIDE_41_DOCS.*
