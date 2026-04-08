#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/common/relationships/enhanced.py
Enhanced Relationship Management using XWNode Graphs (Optional BaaS Feature)
Provides graph-based relationship management using xwnode.
Reuses xwnode for graph operations.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.8
Generation Date: 26-Jan-2026
NOTE: This is an OPTIONAL module for BaaS platform integration.
"""

from typing import Any
from exonware.xwsystem import get_logger
from exonware.xwnode import XWNode
from exonware.xwnode.defs import EdgeMode
from .relationships import RelationshipManager, EntityRelationship, RelationshipType
logger = get_logger(__name__)


class GraphRelationshipManager(RelationshipManager):
    """
    Enhanced relationship manager using xwnode graphs.
    Extends RelationshipManager with graph-based relationship operations
    using xwnode for efficient graph traversal and relationship queries.
    This is an optional BaaS feature.
    Reuses xwnode for graph operations.
    """

    def __init__(self):
        """Initialize graph relationship manager."""
        super().__init__()
        # Initialize xwnode graph for relationship storage
        # Reuse xwnode for graph-based relationships
        self._graph = XWNode(edge_mode=EdgeMode.MULTIPLEX, immutable=False)
        logger.debug("GraphRelationshipManager initialized with xwnode graph")

    def add_relationship(
        self,
        source_entity: Any,  # XWEntity type, avoiding circular import
        target_entity: Any,  # XWEntity type
        relationship_type: str,
        properties: dict[str, Any] | None = None
    ) -> None:
        """
        Add relationship using xwnode graph.
        Args:
            source_entity: Source entity instance
            target_entity: Target entity instance
            relationship_type: Type of relationship
            properties: Optional relationship properties
        """
        try:
            source_id = getattr(source_entity, 'id', str(id(source_entity)))
            target_id = getattr(target_entity, 'id', str(id(target_entity)))
            # Add relationship to base manager
            relationship = EntityRelationship(
                source_entity=getattr(source_entity, 'type', type(source_entity).__name__),
                target_entity=getattr(target_entity, 'type', type(target_entity).__name__),
                relationship_type=RelationshipType(relationship_type) if isinstance(relationship_type, str) else relationship_type,
                field_name=relationship_type,
                metadata=properties or {}
            )
            super().add_relationship(relationship)
            # Add edge to xwnode graph
            # Reuse xwnode edge operations
            edge_properties = properties or {}
            edge_properties['relationship_type'] = relationship_type
            self._graph.add_edge(
                source_id,
                target_id,
                layer=relationship_type,
                properties=edge_properties
            )
            logger.debug(
                f"Added relationship: {source_id} --[{relationship_type}]--> {target_id}"
            )
        except Exception as e:
            logger.error(f"Error adding relationship: {e}")
            raise

    def get_related_entities(
        self,
        entity: Any,  # XWEntity type
        relationship_type: str | None = None,
        depth: int = 1
    ) -> list[Any]:
        """
        Get related entities via graph traversal.
        Args:
            entity: Entity instance
            relationship_type: Optional relationship type filter
            depth: Traversal depth (1 = direct relationships)
        Returns:
            List of related entity instances
        """
        try:
            entity_id = getattr(entity, 'id', str(id(entity)))
            # Use xwnode graph traversal
            # Reuse xwnode traversal capabilities
            related_ids = []
            if depth == 1:
                # Direct relationships
                if relationship_type:
                    # Filter by relationship type (layer)
                    neighbors = self._graph.get_neighbors(entity_id, layer=relationship_type)
                else:
                    # All relationships
                    neighbors = self._graph.get_neighbors(entity_id)
                related_ids = list(neighbors) if neighbors else []
            else:
                # Multi-depth traversal
                # Use xwnode's BFS/DFS capabilities
                visited = {entity_id}
                current_level = {entity_id}
                for _ in range(depth):
                    next_level = set()
                    for node_id in current_level:
                        if relationship_type:
                            neighbors = self._graph.get_neighbors(node_id, layer=relationship_type)
                        else:
                            neighbors = self._graph.get_neighbors(node_id)
                        if neighbors:
                            for neighbor_id in neighbors:
                                if neighbor_id not in visited:
                                    visited.add(neighbor_id)
                                    next_level.add(neighbor_id)
                                    related_ids.append(neighbor_id)
                    current_level = next_level
            logger.debug(
                f"Found {len(related_ids)} related entities for {entity_id} "
                f"(type: {relationship_type}, depth: {depth})"
            )
            # Return IDs (caller can resolve to entity instances)
            return related_ids
        except Exception as e:
            logger.error(f"Error getting related entities: {e}")
            return []

    def remove_relationship(
        self,
        source_entity: Any,  # XWEntity type
        target_entity: Any,  # XWEntity type
        relationship_type: str | None = None
    ) -> None:
        """
        Remove relationship from graph.
        Args:
            source_entity: Source entity instance
            target_entity: Target entity instance
            relationship_type: Optional relationship type filter
        """
        try:
            source_id = getattr(source_entity, 'id', str(id(source_entity)))
            target_id = getattr(target_entity, 'id', str(id(target_entity)))
            # Remove edge from xwnode graph
            # Reuse xwnode edge removal
            if relationship_type:
                self._graph.remove_edge(source_id, target_id, layer=relationship_type)
            else:
                # Remove all relationship types
                self._graph.remove_edge(source_id, target_id)
            logger.debug(
                f"Removed relationship: {source_id} --[{relationship_type or 'all'}]--> {target_id}"
            )
        except Exception as e:
            logger.error(f"Error removing relationship: {e}")
            raise
__all__ = ['GraphRelationshipManager']
