#!/usr/bin/env python3
"""
Enhanced Entity Creation Methods for XWEntity
Provides 4 alternative ways to define entities:
1. @xwentity decorator for dataclass-style definitions
2. Pydantic model support
3. XWEntity.create() factory method for dynamic creation
4. TypedDict/dataclass field definitions
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.8
Generation Date: 27-Jan-2026
"""

from __future__ import annotations
from typing import Any, get_type_hints, get_origin, get_args
from dataclasses import dataclass, fields, is_dataclass, asdict
from functools import wraps
import inspect
# Import XWEntity from unified xwentity package
from exonware.xwmodels import XWEntity
from .errors import XWEntityError
from pydantic import BaseModel
# ==============================================================================
# 1. @xwentity DECORATOR FOR DATACLASS
# ==============================================================================


def xwentity(cls: type | None = None, *, entity_type: str | None = None):
    """
    Decorator to convert a dataclass into an XWEntity class.
    Usage:
        @xwentity
        @dataclass
        class Sword:
            name: str
            sharpness: float
            price: int
        sword = Sword(name="Excalibur", sharpness=100.0, price=10000)
        # sword is now an XWEntity instance
    Args:
        cls: The class to decorate (if None, returns a decorator function)
        entity_type: Optional entity type name
    Returns:
        XWEntity subclass
    """
    def decorator(class_to_decorate: Type) -> type[XWEntity]:
        # Ensure it's a dataclass
        if not is_dataclass(class_to_decorate):
            raise XWEntityError(
                f"@xwentity decorator requires a dataclass. "
                f"Use @dataclass before @xwentity on {class_to_decorate.__name__}"
            )
        # Get dataclass fields
        dataclass_fields = fields(class_to_decorate)
        # Create a new class that inherits from XWEntity
        class_name = class_to_decorate.__name__
        entity_type_name = entity_type or class_name.lower()
        # Build annotations dict from dataclass fields
        annotations = {}
        for field in dataclass_fields:
            annotations[field.name] = field.type
        # Create the new class
        class EnhancedEntity(XWEntity):
            __annotations__ = annotations
            def __init__(self, data: dict[str, Any] | None = None, **kwargs):
                # If data is None but kwargs provided, use kwargs
                if data is None and kwargs:
                    data = kwargs
                # If data is a dataclass instance, convert to dict
                elif data is not None and is_dataclass(data):
                    data = asdict(data)
                # If no data provided, create empty dict
                elif data is None:
                    data = {}
                # Initialize XWEntity with the data
                super().__init__(data=data, entity_type=entity_type_name)
                # Store original dataclass for reference
                self._dataclass_type = class_to_decorate
        # Copy class attributes
        EnhancedEntity.__name__ = class_name
        EnhancedEntity.__qualname__ = class_to_decorate.__qualname__
        EnhancedEntity.__module__ = class_to_decorate.__module__
        EnhancedEntity.__doc__ = class_to_decorate.__doc__
        # Copy methods from original class (except __init__)
        for name, value in class_to_decorate.__dict__.items():
            if name not in ('__init__', '__dict__', '__weakref__', '__module__', '__annotations__'):
                if callable(value) and not isinstance(value, (classmethod, staticmethod, property)):
                    setattr(EnhancedEntity, name, value)
        return EnhancedEntity
    # Support both @xwentity and @xwentity()
    if cls is None:
        return decorator
    else:
        return decorator(cls)
# ==============================================================================
# 2. PYDANTIC MODEL SUPPORT
# ==============================================================================


def create_entity_from_pydantic(pydantic_model: type[BaseModel], entity_type: str | None = None) -> type[XWEntity]:
    """
    Create an XWEntity class from a Pydantic model.
    Usage:
        from pydantic import BaseModel
        class SwordModel(BaseModel):
            name: str
            sharpness: float
            price: int
        Sword = create_entity_from_pydantic(SwordModel)
        sword = Sword(data={"name": "Excalibur", "sharpness": 100.0, "price": 10000})
    Args:
        pydantic_model: Pydantic BaseModel subclass
        entity_type: Optional entity type name
    Returns:
        XWEntity subclass
    """
    if not issubclass(pydantic_model, BaseModel):
        raise XWEntityError(f"{pydantic_model.__name__} must be a subclass of pydantic.BaseModel")
    class_name = pydantic_model.__name__
    entity_type_name = entity_type or class_name.lower()
    # Get field annotations from Pydantic model
    annotations = {}
    if hasattr(pydantic_model, '__annotations__'):
        annotations = pydantic_model.__annotations__.copy()
    elif hasattr(pydantic_model, 'model_fields'):
        # Pydantic v2
        for field_name, field_info in pydantic_model.model_fields.items():
            annotations[field_name] = field_info.annotation
    # Create the new class
    class PydanticEntity(XWEntity):
        __annotations__ = annotations
        def __init__(self, data: dict[str, Any] | None = None, **kwargs):
            # If data is a Pydantic model instance, convert to dict
            if isinstance(data, pydantic_model):
                data = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
            # If data is None but kwargs provided, validate with Pydantic first
            elif data is None and kwargs:
                # Validate with Pydantic model
                validated = pydantic_model(**kwargs)
                data = validated.model_dump() if hasattr(validated, 'model_dump') else validated.dict()
            # If data is dict, validate it
            elif isinstance(data, dict):
                validated = pydantic_model(**data)
                data = validated.model_dump() if hasattr(validated, 'model_dump') else validated.dict()
            # If no data provided, create empty dict
            elif data is None:
                data = {}
            # Initialize XWEntity with the validated data
            super().__init__(data=data, entity_type=entity_type_name)
            # Store original Pydantic model for reference
            self._pydantic_model = pydantic_model
        def to_pydantic(self) -> BaseModel:
            """Convert entity back to Pydantic model instance."""
            return self._pydantic_model(**self.to_dict())
    # Copy class attributes
    PydanticEntity.__name__ = class_name
    PydanticEntity.__qualname__ = pydantic_model.__qualname__
    PydanticEntity.__module__ = pydantic_model.__module__
    PydanticEntity.__doc__ = pydantic_model.__doc__
    return PydanticEntity
# ==============================================================================
# 3. XWEntity.create() FACTORY METHOD
# ==============================================================================


def _create_entity_class(
    name: str,
    fields: dict[str, Any],
    base_class: type[XWEntity] = XWEntity,
    entity_type: str | None = None,
    module: str | None = None
) -> type[XWEntity]:
    """
    Dynamically create an XWEntity class.
    Args:
        name: Class name
        fields: Dictionary mapping field names to type annotations
        base_class: Base class to inherit from (default: XWEntity)
        entity_type: Optional entity type name
        module: Optional module name
    Returns:
        XWEntity subclass
    """
    entity_type_name = entity_type or name.lower()
    # Create annotations dict
    annotations = fields.copy()
    # Create the new class dynamically
    class_dict = {
        '__annotations__': annotations,
        '__module__': module or '__main__',
        '__doc__': f"Dynamically created entity class: {name}",
    }
    DynamicEntity = type(name, (base_class,), class_dict)
    DynamicEntity._entity_type = entity_type_name
    return DynamicEntity
# Add create() method to XWEntity class
@classmethod

def create_entity(
    cls,
    name: str,
    fields: dict[str, Any],
    entity_type: str | None = None,
    **kwargs
) -> type[XWEntity]:
    """
    Factory method to dynamically create an XWEntity class.
    Usage:
        Sword = XWEntity.create(
            "Sword",
            {
                "name": str,
                "sharpness": float,
                "price": int,
            }
        )
        sword = Sword(data={"name": "Excalibur", "sharpness": 100.0, "price": 10000})
    Args:
        name: Class name
        fields: Dictionary mapping field names to type annotations
        entity_type: Optional entity type name
        **kwargs: Additional options for entity initialization
    Returns:
        XWEntity subclass
    """
    return _create_entity_class(name, fields, cls, entity_type, **kwargs)
# Monkey-patch XWEntity with create method
XWEntity.create = create_entity
# ==============================================================================
# 4. TYPEDDICT/DATACLASS FIELD DEFINITIONS
# ==============================================================================


def create_entity_from_typeddict(typed_dict_class: Type, entity_type: str | None = None) -> type[XWEntity]:
    """
    Create an XWEntity class from a TypedDict.
    Usage:
        from typing import TypedDict
        class SwordDict(TypedDict):
            name: str
            sharpness: float
            price: int
        Sword = create_entity_from_typeddict(SwordDict)
        sword = Sword(data={"name": "Excalibur", "sharpness": 100.0, "price": 10000})
    Args:
        typed_dict_class: TypedDict class
        entity_type: Optional entity type name
    Returns:
        XWEntity subclass
    """
    from typing import TypedDict
    # Check if it's a TypedDict
    if not hasattr(typed_dict_class, '__annotations__'):
        raise XWEntityError(f"{typed_dict_class.__name__} must be a TypedDict")
    class_name = typed_dict_class.__name__
    entity_type_name = entity_type or class_name.lower()
    # Get annotations from TypedDict
    annotations = typed_dict_class.__annotations__.copy()
    # Create the new class
    class TypedDictEntity(XWEntity):
        __annotations__ = annotations
        def __init__(self, data: dict[str, Any] | None = None, **kwargs):
            # If data is None but kwargs provided, use kwargs
            if data is None and kwargs:
                data = kwargs
            # If no data provided, create empty dict
            elif data is None:
                data = {}
            # Initialize XWEntity with the data
            super().__init__(data=data, entity_type=entity_type_name)
            # Store original TypedDict for reference
            self._typed_dict_type = typed_dict_class
    # Copy class attributes
    TypedDictEntity.__name__ = class_name
    TypedDictEntity.__qualname__ = typed_dict_class.__qualname__
    TypedDictEntity.__module__ = typed_dict_class.__module__
    TypedDictEntity.__doc__ = typed_dict_class.__doc__
    return TypedDictEntity
# ==============================================================================
# EXPORTS
# ==============================================================================
__all__ = [
    "xwentity",
    "create_entity_from_pydantic",
    "create_entity_from_typeddict",
]
