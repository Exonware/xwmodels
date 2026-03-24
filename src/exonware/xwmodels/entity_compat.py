#!/usr/bin/env python3
"""
Compatibility facade for xwmodels XWEntity.

This wrapper preserves legacy xwmodels ergonomics (data-first construction and
file/factory helpers) while delegating core behavior to exonware.xwentity.XWEntity.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from exonware.xwaction import XWAction
from exonware.xwdata import XWData
from exonware.xwschema import XWSchema
from exonware.xwentity import XWEntity as CoreXWEntity

from .errors import XWEntityError


class XWEntity(CoreXWEntity):
    """xwmodels-compatible entity facade."""

    _SENSITIVE_FIELDS = {
        "password",
        "passphrase",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "api_key",
        "private_key",
    }

    @staticmethod
    def _looks_like_schema_dict(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        schema_markers = {"type", "properties", "$schema", "$id", "required", "allOf", "anyOf", "oneOf"}
        return bool(schema_markers.intersection(value.keys()))

    @staticmethod
    def _resolve_format(explicit_format: str | None, file_path: Path) -> str:
        if explicit_format:
            return explicit_format.lower()
        suffix = file_path.suffix.lower().lstrip(".")
        if suffix in {"yml", "yaml"}:
            return "yaml"
        if suffix in {"json", "xml", "toml"}:
            return suffix
        return "json"

    @classmethod
    def _decode_payload(cls, raw_text: str, input_format: str) -> Any:
        fmt = input_format.lower()
        if fmt == "json":
            return json.loads(raw_text)
        if fmt == "yaml":
            import yaml

            return yaml.safe_load(raw_text)
        if fmt == "toml":
            try:
                import tomllib

                return tomllib.loads(raw_text)
            except ModuleNotFoundError:
                import toml

                return toml.loads(raw_text)
        if fmt == "xml":
            probe = cls()
            probe.from_xml(raw_text)
            return probe.to_dict()
        raise XWEntityError(f"Unsupported input format: {input_format}")

    @classmethod
    def _encode_payload(cls, payload: Any, output_format: str) -> str:
        fmt = output_format.lower()
        if fmt == "json":
            return json.dumps(payload, indent=2, ensure_ascii=False)
        if fmt == "yaml":
            import yaml

            return yaml.safe_dump(payload, sort_keys=False)
        if fmt == "toml":
            try:
                import tomli_w

                return tomli_w.dumps(payload)
            except ModuleNotFoundError:
                import toml

                return toml.dumps(payload)
        if fmt == "xml":
            probe = cls.from_dict(payload if isinstance(payload, dict) else {"_data": payload})
            return probe.to_xml()
        raise XWEntityError(f"Unsupported output format: {output_format}")

    @staticmethod
    def _redact_sensitive(value: Any) -> Any:
        if isinstance(value, dict):
            redacted: dict[str, Any] = {}
            for key, child in value.items():
                if key.lower() in XWEntity._SENSITIVE_FIELDS:
                    redacted[key] = "***REDACTED***"
                else:
                    redacted[key] = XWEntity._redact_sensitive(child)
            return redacted
        if isinstance(value, list):
            return [XWEntity._redact_sensitive(item) for item in value]
        return value

    def __init__(
        self,
        schema: XWSchema | dict[str, Any] | str | None = None,
        data: XWData | dict[str, Any] | list[Any] | None = None,
        actions: list[XWAction] | dict[str, Any] | None = None,
        entity_type: str | None = None,
        config: Any | None = None,
        node_mode: str | None = None,
        edge_mode: str | None = None,
        graph_manager_enabled: bool | None = None,
        **node_options: Any,
    ):
        # Backward compatibility: treat first positional dict/list/XWData as data.
        if data is None and schema is not None:
            if isinstance(schema, (XWData, list)):
                data = schema
                schema = None
            elif isinstance(schema, dict) and not self._looks_like_schema_dict(schema):
                data = schema
                schema = None

        resolved_entity_type = entity_type
        if resolved_entity_type is None and config is not None:
            resolved_entity_type = getattr(config, "default_entity_type", None)
        if resolved_entity_type is None:
            resolved_entity_type = "entity"

        super().__init__(
            schema=schema,
            data=data,
            actions=actions,
            entity_type=resolved_entity_type,
            config=config,
            node_mode=node_mode,
            edge_mode=edge_mode,
            graph_manager_enabled=graph_manager_enabled,
            **node_options,
        )

    @classmethod
    def from_data(
        cls,
        data: XWData | dict[str, Any] | list[Any],
        schema: XWSchema | dict[str, Any] | str | None = None,
        **kwargs: Any,
    ) -> XWEntity:
        """Legacy factory that creates an entity from data-first input."""
        return cls(schema=schema, data=data, **kwargs)

    @classmethod
    def from_schema(
        cls,
        schema: XWSchema | dict[str, Any] | str,
        initial_data: XWData | dict[str, Any] | list[Any] | None = None,
        **kwargs: Any,
    ) -> XWEntity:
        """Legacy factory that creates an entity from schema + optional data."""
        return cls(schema=schema, data=initial_data or {}, **kwargs)

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        format: str = "data",
        input_format: str | None = None,
        schema: XWSchema | dict[str, Any] | str | None = None,
        **kwargs: Any,
    ) -> XWEntity:
        """Load an entity facet from a file."""
        file_path = Path(path)
        if not file_path.exists():
            raise XWEntityError(f"File not found: {file_path}")

        component = (format or "data").lower()
        # Legacy behavior: format may specify the file serialization format directly.
        if component in {"json", "yaml", "xml", "toml"}:
            input_format = component
            component = "data"
        if component not in {"data", "schema", "actions"}:
            raise XWEntityError(f"Invalid format: {format}")

        resolved_format = cls._resolve_format(input_format, file_path)
        payload = cls._decode_payload(file_path.read_text(encoding="utf-8"), resolved_format)

        if component == "schema":
            schema_obj = payload if isinstance(payload, XWSchema) else XWSchema(payload)
            return cls(schema=schema_obj, data={}, **kwargs)

        if component == "actions":
            entity = cls(schema=schema, data={}, **kwargs)
            action_payloads = payload.values() if isinstance(payload, dict) else payload
            for action_payload in action_payloads or []:
                if isinstance(action_payload, dict):
                    entity.register_action(XWAction.from_native(action_payload))
            return entity

        if isinstance(payload, dict) and "_data" in payload:
            payload = payload.get("_data") or {}
        return cls(schema=schema, data=payload, **kwargs)

    def to_file(
        self,
        path: str | Path,
        format: str = "data",
        output_format: str = "json",
        **_: Any,
    ) -> str:
        """Save a selected entity facet to disk."""
        component = (format or "data").lower()
        if component not in {"data", "schema", "actions"}:
            raise XWEntityError(f"Invalid format: {format}")

        if component == "schema":
            if self.schema is None:
                raise XWEntityError("Schema is not available")
            payload = self.schema.to_native() if hasattr(self.schema, "to_native") else self.schema
        elif component == "actions":
            payload = list((self.to_dict().get("_actions") or {}).values())
        else:
            payload = self.to_dict().get("_data") or {}

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(self._encode_payload(payload, output_format), encoding="utf-8")
        return str(file_path)

    def load_from_file(
        self,
        path: str | Path,
        format: str = "data",
        input_format: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Load a selected entity facet into the current instance."""
        loaded = self.__class__.from_file(path, format=format, input_format=input_format, schema=self.schema, **kwargs)
        component = (format or "data").lower()

        if component == "schema":
            self._schema = loaded.schema
            return
        if component == "actions":
            for action in loaded.actions:
                self.register_action(action)
            return
        self._from_dict({"_data": loaded.to_dict().get("_data") or {}})

    def __str__(self) -> str:
        """Redact sensitive fields in string rendering."""
        try:
            payload = self.to_dict()
            safe_payload = self._redact_sensitive(payload)
            return json.dumps(safe_payload, indent=2, ensure_ascii=False, default=str)
        except Exception:
            return super().__str__()
