#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/storage/file_storage.py
Simple file-based storage implementations for collections and groups.
Provides ICollectionStorage and IGroupStorage for development and testing.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.13
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from exonware.xwsystem import get_logger

from .contracts import ICollectionStorage, IGroupStorage

logger = get_logger(__name__)


class SimpleFileCollectionStorage(ICollectionStorage):
    """
    Simple file-based collection storage.
    Saves to {base_path}/{group_id}/{collection_id}.data.xwjson (or .json if no group_id).
    """

    def save_collection(
        self,
        collection: Any,
        *,
        base_path: Path | None = None,
    ) -> None:
        """Save collection entities to JSON file."""
        path = base_path or getattr(collection, "_base_path", None) or Path.cwd()
        path = Path(path)
        group_id = getattr(collection, "_group_id", None) or getattr(collection, "group_id", None)
        coll_id = getattr(collection, "_collection_id", None) or getattr(collection, "id", None)
        if group_id:
            path = path / str(group_id)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{coll_id}.data.xwjson"
        entities = []
        for entity in (collection.list_all() if hasattr(collection, "list_all") else list(getattr(collection, "_entities", {}).values())):
            if hasattr(entity, "to_native"):
                entities.append(entity.to_native())
            elif hasattr(entity, "to_dict"):
                entities.append(entity.to_dict())
            else:
                entities.append(entity)
        data = {"entities": entities, "collection_id": coll_id, "group_id": group_id}
        file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.debug(f"Saved collection {coll_id} to {file_path}")

    def load_collection(
        self,
        collection: Any,
        *,
        base_path: Path | None = None,
    ) -> None:
        """Load collection entities from JSON file."""
        path = base_path or getattr(collection, "_base_path", None) or Path.cwd()
        path = Path(path)
        group_id = getattr(collection, "_group_id", None) or getattr(collection, "group_id", None)
        coll_id = getattr(collection, "_collection_id", None) or getattr(collection, "id", None)
        if group_id:
            path = path / str(group_id)
        file_path = path / f"{coll_id}.data.xwjson"
        if not file_path.exists():
            logger.debug(f"No file at {file_path}, collection remains empty")
            return
        data = json.loads(file_path.read_text(encoding="utf-8"))
        entities_data = data.get("entities", [])
        _entities = getattr(collection, "_entities", None)
        if _entities is not None:
            _entities.clear()
            for i, ent in enumerate(entities_data):
                if isinstance(ent, dict):
                    eid = ent.get("_metadata", {}).get("id") or ent.get("id") or str(i)
                    _entities[eid] = ent
                else:
                    _entities[str(i)] = ent
        logger.debug(f"Loaded collection {coll_id} from {file_path}")


class SimpleFileGroupStorage(IGroupStorage):
    """
    Simple file-based group storage.
    Saves group metadata and collection refs to {base_path}/{group_id}.xwjson.
    """

    def __init__(self, collection_storage: ICollectionStorage | None = None):
        self._collection_storage = collection_storage or SimpleFileCollectionStorage()

    def save_group(self, group: Any) -> None:
        """Save group and its collections to files."""
        base_path = getattr(group, "_base_path", None) or Path.cwd()
        base_path = Path(base_path)
        group_id = getattr(group, "_group_id", None) or getattr(group, "id", None)
        base_path.mkdir(parents=True, exist_ok=True)
        group_file = base_path / f"{group_id}.xwjson"
        group_dict = group.to_dict() if hasattr(group, "to_dict") else {}
        group_file.write_text(json.dumps(group_dict, indent=2), encoding="utf-8")
        for coll in getattr(group, "_collections", {}).values():
            self._collection_storage.save_collection(coll, base_path=base_path)
        for sub in getattr(group, "_subgroups", {}).values():
            self.save_group(sub)
        logger.debug(f"Saved group {group_id} to {group_file}")

    def load_group(self, group: Any) -> None:
        """Load group from file. Collections are loaded as dicts into _collections."""
        base_path = getattr(group, "_base_path", None) or Path.cwd()
        base_path = Path(base_path)
        group_id = getattr(group, "_group_id", None) or getattr(group, "id", None)
        group_file = base_path / f"{group_id}.xwjson"
        if not group_file.exists():
            logger.debug(f"No file at {group_file}, group remains empty")
            return
        data = json.loads(group_file.read_text(encoding="utf-8"))
        if hasattr(group, "from_dict") and data:
            group.from_dict(data)
        logger.debug(f"Loaded group {group_id} from {group_file}")


__all__ = ["SimpleFileCollectionStorage", "SimpleFileGroupStorage"]
