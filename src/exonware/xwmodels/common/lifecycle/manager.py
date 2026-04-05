#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/common/lifecycle/manager.py
Lifecycle Manager (Optional BaaS Feature)
Provides entity lifecycle state management using xwaction workflows.
Reuses xwaction for workflow execution.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.7
Generation Date: 26-Jan-2026
NOTE: This is an OPTIONAL module for BaaS platform integration.
"""

from typing import Any
from datetime import datetime
from exonware.xwsystem import get_logger
from exonware.xwaction import XWAction, ActionRegistry, action_executor
from exonware.xwaction.context import ActionContext
from .contracts import ILifecycleManager
from ...defs import EntityState, STATE_TRANSITIONS
from ...errors import XWEntityError, XWEntityStateError
logger = get_logger(__name__)


class LifecycleManager(ILifecycleManager):
    """
    Lifecycle manager using xwaction workflows.
    Provides entity lifecycle state management.
    Reuses xwaction for workflow execution.
    This is an optional BaaS feature.
    """

    def __init__(self):
        """Initialize lifecycle manager."""
        self._state_history: dict[str, list[dict[str, Any]]] = {}
        # Register lifecycle actions using xwaction
        self._register_lifecycle_actions()
        logger.debug("LifecycleManager initialized")

    def _register_lifecycle_actions(self):
        """Register lifecycle transition actions using xwaction."""
        # Register state transition actions
        @XWAction(name="transition_entity_state", profile="workflow")
        async def transition_state_action(
            entity_id: str,
            entity_type: str,
            from_state: str,
            to_state: str,
            context: ActionContext
        ):
            """State transition action using xwaction."""
            # Record transition
            history_key = f"{entity_type}:{entity_id}"
            if history_key not in self._state_history:
                self._state_history[history_key] = []
            self._state_history[history_key].append({
                'from_state': from_state,
                'to_state': to_state,
                'timestamp': datetime.now().isoformat(),
                'context': context.to_dict() if hasattr(context, 'to_dict') else {}
            })
            return {'success': True, 'new_state': to_state}
        logger.debug("Lifecycle actions registered with xwaction")

    async def transition_state(
        self,
        entity: Any,  # XWEntity type, avoiding circular import
        new_state: EntityState,
        **opts
    ) -> None:
        """
        Transition entity to new state using xwaction workflow.
        Reuses xwaction action_executor for workflow execution.
        Args:
            entity: Entity instance
            new_state: Target state
            **opts: Additional transition options
        """
        try:
            entity_id = getattr(entity, 'id', None)
            entity_type = getattr(entity, 'type', getattr(entity, '__class__', {}).__name__)
            current_state = getattr(entity, 'state', EntityState.DRAFT)
            if not entity_id:
                raise XWEntityError("Entity must have an 'id' attribute")
            # Validate transition
            is_valid = await self.validate_transition(
                entity, current_state, new_state, **opts
            )
            if not is_valid:
                raise XWEntityStateError(
                    f"Invalid state transition: {current_state} -> {new_state}"
                )
            # Use xwaction workflow
            try:
                # Execute transition using xwaction
                context = ActionContext(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    from_state=str(current_state),
                    to_state=str(new_state)
                )
                result = await action_executor.execute(
                    action_name="transition_entity_state",
                    entity_id=entity_id,
                    entity_type=entity_type,
                    from_state=str(current_state),
                    to_state=str(new_state),
                    context=context
                )
                if result and result.get('success'):
                    # Update entity state
                    if hasattr(entity, 'state'):
                        entity.state = new_state
                    logger.debug(
                        f"State transition executed via xwaction: "
                        f"{entity_type}:{entity_id} {current_state} -> {new_state}"
                    )
                    return
            except Exception as e:
                logger.warning(f"xwaction workflow failed, using direct transition: {e}")
            # Fallback: Direct transition
            history_key = f"{entity_type}:{entity_id}"
            if history_key not in self._state_history:
                self._state_history[history_key] = []
            self._state_history[history_key].append({
                'from_state': str(current_state),
                'to_state': str(new_state),
                'timestamp': datetime.now().isoformat()
            })
            # Update entity state
            if hasattr(entity, 'state'):
                entity.state = new_state
            logger.debug(
                f"State transition: {entity_type}:{entity_id} {current_state} -> {new_state}"
            )
        except (XWEntityError, XWEntityStateError):
            raise
        except Exception as e:
            logger.error(f"Error transitioning state: {e}")
            raise XWEntityError(f"Failed to transition state: {e}") from e

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
        try:
            entity_id = getattr(entity, 'id', None)
            entity_type = getattr(entity, 'type', getattr(entity, '__class__', {}).__name__)
            if not entity_id:
                return []
            history_key = f"{entity_type}:{entity_id}"
            return self._state_history.get(history_key, [])
        except Exception as e:
            logger.error(f"Error getting state history: {e}")
            return []

    async def validate_transition(
        self,
        entity: Any,  # XWEntity type
        from_state: EntityState,
        to_state: EntityState,
        **opts
    ) -> bool:
        """
        Validate if state transition is allowed.
        Uses STATE_TRANSITIONS from defs.
        Args:
            entity: Entity instance
            from_state: Current state
            to_state: Target state
            **opts: Additional validation options
        Returns:
            True if transition is valid, False otherwise
        """
        try:
            # Check if transition is allowed in STATE_TRANSITIONS
            allowed_transitions = STATE_TRANSITIONS.get(from_state, [])
            return to_state in allowed_transitions
        except Exception as e:
            logger.error(f"Error validating transition: {e}")
            return False
__all__ = ['LifecycleManager']
