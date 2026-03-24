#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/common/lifecycle/contracts.py
Lifecycle Management Contracts (Optional BaaS Feature)
Defines interfaces for entity lifecycle management.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.5
Generation Date: 26-Jan-2026
NOTE: This is an OPTIONAL module for BaaS platform integration.
"""

from typing import Any, Protocol, runtime_checkable
from ...defs import EntityState
@runtime_checkable

class ILifecycleManager(Protocol):
    """
    Interface for lifecycle manager.
    Provides entity lifecycle state management.
    This is an optional BaaS feature.
    """

    async def transition_state(
        self,
        entity: Any,  # XWEntity type, avoiding circular import
        new_state: EntityState,
        **opts
    ) -> None:
        """
        Transition entity to new state.
        Args:
            entity: Entity instance
            new_state: Target state
            **opts: Additional transition options
        """
        ...

    async def get_state_history(
        self,
        entity: Any,  # XWEntity type
        **opts
    ) -> list[dict[str, Any]]:
        """
        Get state transition history for entity.
        Args:
            entity: Entity instance
            **opts: Additional options
        Returns:
            List of state transition records
        """
        ...

    async def validate_transition(
        self,
        entity: Any,  # XWEntity type
        from_state: EntityState,
        to_state: EntityState,
        **opts
    ) -> bool:
        """
        Validate if state transition is allowed.
        Args:
            entity: Entity instance
            from_state: Current state
            to_state: Target state
            **opts: Additional validation options
        Returns:
            True if transition is valid, False otherwise
        """
        ...
@runtime_checkable

class ILifecycleWorkflow(Protocol):
    """
    Interface for lifecycle workflow.
    Provides workflow-based lifecycle management using xwaction.
    This is an optional BaaS feature.
    """

    async def execute_workflow(
        self,
        entity: Any,  # XWEntity type
        workflow_name: str,
        **opts
    ) -> Any:
        """
        Execute lifecycle workflow.
        Args:
            entity: Entity instance
            workflow_name: Name of workflow to execute
            **opts: Additional workflow options
        Returns:
            Workflow execution result
        """
        ...

    async def define_workflow(
        self,
        workflow_name: str,
        states: list[EntityState],
        transitions: dict[EntityState, list[EntityState]],
        **opts
    ) -> None:
        """
        Define a lifecycle workflow.
        Args:
            workflow_name: Name of workflow
            states: List of states in workflow
            transitions: Dictionary mapping states to allowed transitions
            **opts: Additional workflow definition options
        """
        ...
__all__ = [
    'ILifecycleManager',
    'ILifecycleWorkflow',
]
