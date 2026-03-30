#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/common/relationships.py
Entity Relationship Management
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.6
Generation Date: 15-Nov-2025
"""

from typing import Any
from dataclasses import dataclass
from enum import Enum
from exonware.xwsystem import get_logger
logger = get_logger(__name__)


class RelationshipType(Enum):
    """Types of entity relationships."""
    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"
    COMPOSITION = "composition"
    AGGREGATION = "aggregation"
@dataclass

class EntityRelationship:
    """Represents a relationship between entities."""
    source_entity: str
    target_entity: str
    relationship_type: RelationshipType
    field_name: str
    cascade_delete: bool = False
    cascade_update: bool = False
    metadata: dict[str, Any] | None = None


class RelationshipManager:
    """Manages entity relationships."""

    def __init__(self):
        """Initialize relationship manager."""
        self._relationships: dict[str, list[EntityRelationship]] = {}
        self._inverse_relationships: dict[str, list[EntityRelationship]] = {}

    def add_relationship(self, relationship: EntityRelationship) -> None:
        """
        Add a relationship.
        Args:
            relationship: Relationship to add
        """
        if relationship.source_entity not in self._relationships:
            self._relationships[relationship.source_entity] = []
        self._relationships[relationship.source_entity].append(relationship)
        # Add inverse relationship
        if relationship.target_entity not in self._inverse_relationships:
            self._inverse_relationships[relationship.target_entity] = []
        inverse = EntityRelationship(
            source_entity=relationship.target_entity,
            target_entity=relationship.source_entity,
            relationship_type=relationship.relationship_type,
            field_name=relationship.field_name,
            cascade_delete=relationship.cascade_delete,
            cascade_update=relationship.cascade_update,
            metadata=relationship.metadata
        )
        self._inverse_relationships[relationship.target_entity].append(inverse)

    def get_relationships(self, entity_name: str) -> list[EntityRelationship]:
        """
        Get all relationships for an entity.
        Args:
            entity_name: Name of the entity
        Returns:
            List of relationships
        """
        return self._relationships.get(entity_name, [])

    def get_inverse_relationships(self, entity_name: str) -> list[EntityRelationship]:
        """
        Get all inverse relationships for an entity.
        Args:
            entity_name: Name of the entity
        Returns:
            List of inverse relationships
        """
        return self._inverse_relationships.get(entity_name, [])

    def validate_relationship(
        self,
        source_entity: Any,
        target_entity: Any,
        relationship: EntityRelationship
    ) -> tuple[bool, str | None]:
        """
        Validate a relationship between entities.
        Args:
            source_entity: Source entity instance
            target_entity: Target entity instance
            relationship: Relationship definition
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if entities are of correct types
        source_type = getattr(source_entity, '__class__', {}).__name__
        target_type = getattr(target_entity, '__class__', {}).__name__
        if source_type != relationship.source_entity:
            return False, f"Source entity type mismatch: expected {relationship.source_entity}, got {source_type}"
        if target_type != relationship.target_entity:
            return False, f"Target entity type mismatch: expected {relationship.target_entity}, got {target_type}"
        # Validate relationship type constraints
        if relationship.relationship_type == RelationshipType.ONE_TO_ONE:
            # Check if target is already related to another source
            pass  # Implementation would check uniqueness
        return True, None
# Global relationship manager instance
_relationship_manager: RelationshipManager | None = None


def get_relationship_manager() -> RelationshipManager:
    """
    Get global relationship manager instance.
    Returns:
        RelationshipManager instance
    """
    global _relationship_manager
    if _relationship_manager is None:
        _relationship_manager = RelationshipManager()
    return _relationship_manager
