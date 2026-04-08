<!-- docs/GUIDE_01_USAGE.md (project usage, GUIDE_41_DOCS) -->
# xwmodels — Usage Guide

**Last Updated:** 30-Mar-2026

How to use xwmodels (output of GUIDE_41_DOCS). See [REF_15_API.md](REF_15_API.md) and [REF_22_PROJECT.md](REF_22_PROJECT.md).

---

## Core classes

- `XWModelEntity` — model-facing entity facade built on `exonware.xwentity.XWEntity`.
- `XWModelCollection[TEntity]` — same-type entity container with collection-level management.
- `XWModelGroup` (exported as `XWGroup`) — group of collections with optional nested subgroups.

`XWEntity` is still exported as a compatibility alias to `XWModelEntity`.

---

## Practical setup pattern (base systems)

Use xwmodels as the **model management layer** for base systems:

1. Create one top-level group per system (for example: `auth`, `catalog`, `billing`).
2. Create one collection per aggregate/model type inside each group (users, roles, sessions, invoices).
3. Store typed model entities in each collection.
4. Attach storage/auth providers at group level so persistence and policy are consistent.

---

## Quick example

```python
from pathlib import Path
from exonware.xwmodels import XWGroup, XWModelEntity

auth_group = XWGroup("auth", base_path=Path("./data"))
users = auth_group.create_collection("users", entity_type="user")

user = XWModelEntity(
    schema={"type": "object", "properties": {"name": {"type": "string"}}},
    data={"name": "Alice"},
    entity_type="user",
)
users.add(user)
```

---

## Nested group usage

Use subgroups for environment/tenant partitioning:

- `root` -> `prod` -> `billing`
- `root` -> `staging` -> `billing`
- `root` -> `tenant-acme` -> `auth`

This keeps one mental model while scaling across environments and tenants.

---

*Per GUIDE_00_MASTER and GUIDE_41_DOCS.*
