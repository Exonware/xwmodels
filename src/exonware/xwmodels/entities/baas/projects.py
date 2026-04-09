#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/entities/baas/projects.py
BaaS Project Entities (Optional BaaS Feature)
Provides project/app management entity classes (Project, App, Deployment).
This is an optional BaaS feature.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.10
Generation Date: 26-Jan-2026
NOTE: This is an OPTIONAL module for BaaS platform integration.
"""

from typing import Any
from exonware.xwschema import XWSchema
from ...entity_compat import XWModelEntity


class Project(XWModelEntity):
    """
    Project entity for BaaS capability.
    Represents a project definition and configuration.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize Project entity."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "project_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": ["string", "null"]},
                "organization_id": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["active", "archived", "deleted"],
                    "default": "active"
                },
                "settings": {"type": "object"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["project_id", "name", "organization_id"]
        })
        super().__init__(
            schema=schema,
            entity_type="project",
            **kwargs
        )


class App(XWModelEntity):
    """
    App entity for BaaS capability.
    Represents an application definition within a project.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize App entity."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "app_id": {"type": "string"},
                "project_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": ["string", "null"]},
                "type": {
                    "type": "string",
                    "enum": ["web", "api", "mobile", "desktop"],
                    "default": "web"
                },
                "status": {
                    "type": "string",
                    "enum": ["active", "inactive", "archived"],
                    "default": "active"
                },
                "configuration": {"type": "object"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["app_id", "project_id", "name"]
        })
        super().__init__(
            schema=schema,
            entity_type="app",
            **kwargs
        )


class Deployment(XWModelEntity):
    """
    Deployment entity for BaaS capability.
    Represents a deployment record and history.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize Deployment entity."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "deployment_id": {"type": "string"},
                "app_id": {"type": "string"},
                "environment": {
                    "type": "string",
                    "enum": ["development", "staging", "production"],
                    "default": "development"
                },
                "version": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "completed", "failed", "rolled_back"],
                    "default": "pending"
                },
                "deployed_at": {"type": ["string", "null"], "format": "date-time"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["deployment_id", "app_id", "environment", "version", "status"]
        })
        super().__init__(
            schema=schema,
            entity_type="deployment",
            **kwargs
        )
__all__ = ['Project', 'App', 'Deployment']
