# xwmodels

Entity collections and groups on top of [xwentity](https://github.com/exonware/xwentity), wired for the rest of the eXonware stack. Details live in per-project REF docs.

**Company:** eXonware.com · **Author:** eXonware Backend Team · **Email:** connect@exonware.com  

[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://exonware.com)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## 📦 Install

```bash
pip install exonware-xwmodels
pip install exonware-xwmodels[lazy]
pip install exonware-xwmodels[full]
```

---

## 🚀 Quick start

```python
from exonware.xwmodels import *
# Or: import xwmodels
# Collections and groups of entities - see docs for patterns
```

See [docs/](docs/) for REF_* files and examples.

---

## ✨ What you get

| Area | Contents |
|------|----------|
| **Models** | Entity collections and groups built on xwentity. |
| **Integration** | Hooks for xwentity, xwstorage, xwaction. |
| **Tooling** | Utilities aimed at larger, consistent model graphs. |

## 🧱 Core model roles

- **XWModelEntity** (`entity_compat.py`) is the xwmodels compatibility facade over `exonware.xwentity.XWEntity` (data-first ergonomics + model-facing helpers).
- **XWModelCollection** (`collection.py`) manages many entities of one type and adds persistence-aware collection behavior via storage contracts.
- **XWModelGroup** (`group.py`) manages multiple collections, supports nested subgroups (tree hierarchy), and coordinates group-level save/load through providers.
- **Shared foundation:** model collection and model group inherit `XWObject` from `xwsystem` for lightweight identity/object semantics; entity behavior is inherited from core `xwentity`.
- **Compatibility alias:** `XWEntity` remains exported as an alias to `XWModelEntity` for backward compatibility.

## 📊 Model management layer in practice

- **Base systems:** use one `XWModelGroup` per bounded system (for example `auth`, `catalog`, `billing`, `content`) and keep each system's collections under that group.
- **Domain partitioning:** map each aggregate/root model to one `XWModelCollection` (users, roles, invoices, products), with one schema contract and many entities.
- **Nested environments:** create subgroups for `dev` / `staging` / `prod`, tenant spaces, or regional shards while preserving one management API.
- **Provider orchestration:** plug storage/auth providers at group level so save/load and access control policies are consistent across all collections in that system.
- **App composition:** xwbase-style systems can compose multiple groups to build complete application backbones while reusing the same entity/collection/group semantics.

---

## 🌐 Ecosystem functional contributions

`xwmodels` is the management layer over entity collections/groups; sibling libraries provide the contracts that make model systems production-capable.
You can adopt `xwmodels` standalone as a model-organization layer on top of your existing domain code.
Connecting to more XW modules is optional and primarily useful for enterprise and mission-critical model infrastructure that needs consistent self-hosted contracts.

| Supporting XW lib | What it provides to xwmodels | Functional requirement it satisfies |
|------|----------------|----------------|
| **XWEntity** | Core entity/collection/group semantics and compatibility facade targets. | Stable domain model foundation for model graphs. |
| **XWStorage** | Provider contracts and persistence paths for model save/load operations. | Durable model state and environment/tenant partition persistence. |
| **XWAction** | Action integration for model-level workflows and operations. | Workflow and automation on top of model collections/groups. |
| **XWSystem** | Base object/runtime contracts reused by model types. | Consistent object lifecycle and shared infrastructure behavior. |
| **XWSchema** | Validation rules for model payloads and evolution. | Controlled schema integrity for large model graphs. |
| **XWBase** | Higher-level composition layer that consumes model systems. | End-to-end application assembly from reusable model primitives. |

This positions `xwmodels` as orchestration for large domain graphs, not just a thin alias package.

---

## 📖 Docs and tests

- **Start:** [docs/INDEX.md](docs/INDEX.md) or [docs/](docs/).
- **Tests:** From repo root, e.g. `python tests/runner.py`, per project layout.

---

## 📜 License and links

Apache-2.0 - see [LICENSE](LICENSE). **Homepage:** https://exonware.com · **Repository:** https://github.com/exonware/xwmodels  


## ⏱️ Async Support

<!-- async-support:start -->
- xwmodels includes asynchronous execution paths in production code.
- Source validation: 9 async def definitions and 2 await usages under src/.
- Use async APIs for I/O-heavy or concurrent workloads to improve throughput and responsiveness.
<!-- async-support:end -->
Version: 0.6.0.11 | Updated: 10-Apr-2026

*Built with ❤️ by eXonware.com - Revolutionizing Python Development Since 2025*
