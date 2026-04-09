# DX Reference — xwmodels

**Library:** exonware-xwmodels  
**Last Updated:** 08-Mar-2026

Developer experience contract: happy paths, errors, ergonomics (output of GUIDE_14_DX).

---

## Happy Paths (1–3 lines)

**Create group and collection with entities:**

```python
from exonware.xwmodels import XWGroup, XWModelCollection, XWModelEntity
from pathlib import Path

group = XWGroup("my_group", base_path=Path("./data"))
coll = group.create_collection("users", entity_type="user")
entity = XWModelEntity(schema={...}, data={"name": "Alice"})
coll.add(entity)
group.save_all()
```

**Type-safe collection with generic:**

```python
from exonware.xwmodels import XWModelCollection, XWModelEntity

# XWModelCollection[TEntity: XWModelEntity] — add/find return typed entities
coll: XWModelCollection[XWModelEntity] = XWModelCollection("users", entity_type="user")
coll.add(entity)  # entity must be XWModelEntity-compatible
found = coll.find(lambda e: e.get("status") == "active")  # list[XWModelEntity]
```

**Nested groups:**

```python
parent = XWGroup("parent", base_path=Path("./data"))
child = parent.create_subgroup("child")
users = child.create_collection("users", entity_type="user")
```

---

## Defaults

- Safe by default: validation via xwentity; storage/auth optional (no-op without providers).
- Sane defaults: base_path defaults to cwd; entity_type required for collections.

---

## Errors

- `XWEntityError` — base for xwmodels/xwentity errors  
- `XWEntityValidationError` — validation failures (from xwentity)  
- `XWEntityStateError` — invalid state transitions  
- `XWEntityActionError` — action execution errors  
- `XWEntityNotFoundError` — missing entity/item  

Storage/auth providers may raise their own errors when save/load fails.

---

## Entry Points

- `from exonware.xwmodels import XWGroup, XWModelCollection, XWModelEntity, ...` (primary)
- `from exonware.xwmodels.facade import XWGroup, XWModelCollection, ...` (explicit facade)

---

## Key Code (per REF_01)

| Task | Code |
|------|------|
| Create group | `XWGroup("id", base_path=Path("./data"))` |
| Create collection | `group.create_collection("users", entity_type="user")` |
| Add entity | `coll.add(entity)` |
| Find entities | `coll.find(lambda e: e.get("status") == "active")` |
| Save/load | `group.save_all()` / `group.load_all()` (requires IGroupStorage) |

---

*See GUIDE_14_DX.md for DX standards.*
