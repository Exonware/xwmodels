#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwentity/entities/baas/billing.py
BaaS Billing Entities (Optional BaaS Feature)
Provides billing-related entity classes (Invoice, Payment, Subscription, Plan).
This is an optional BaaS feature.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.6
Generation Date: 26-Jan-2026
NOTE: This is an OPTIONAL module for BaaS platform integration.
"""

from typing import Any
from datetime import datetime
from exonware.xwschema import XWSchema
from exonware.xwsystem import get_logger
from ...entity import XWEntity
logger = get_logger(__name__)


class Invoice(XWEntity):
    """
    Invoice entity for billing capability.
    Represents an invoice with line items, taxes, and payment tracking.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize Invoice entity."""
        # Reuse XWSchema for comprehensive validation
        schema_dict = {
            "type": "object",
            "properties": {
                "invoice_id": {"type": "string"},
                "customer_id": {"type": "string"},
                "amount": {"type": "number", "minimum": 0},
                "currency": {"type": "string", "default": "USD", "pattern": "^[A-Z]{3}$"},
                "status": {
                    "type": "string",
                    "enum": ["draft", "sent", "paid", "cancelled"],
                    "default": "draft"
                },
                "line_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "quantity": {"type": "number", "minimum": 0},
                            "unit_price": {"type": "number", "minimum": 0},
                            "total": {"type": "number", "minimum": 0}
                        },
                        "required": ["description", "quantity", "unit_price"]
                    }
                },
                "due_date": {"type": "string", "format": "date"},
                "paid_at": {"type": ["string", "null"], "format": "date-time"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["invoice_id", "customer_id", "amount", "currency", "status"]
        }
        # Create XWSchema instance for validation
        schema = XWSchema(schema_dict)
        # Validate initial data if provided using XWSchema
        if kwargs.get('data'):
            try:
                schema.validate(kwargs['data'])
            except Exception as e:
                logger.warning(f"Initial data validation warning: {e}")
        super().__init__(
            schema=schema,
            entity_type="invoice",
            **kwargs
        )


class Payment(XWEntity):
    """
    Payment entity for billing capability.
    Represents a payment transaction.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize Payment entity."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "payment_id": {"type": "string"},
                "invoice_id": {"type": "string"},
                "amount": {"type": "number"},
                "currency": {"type": "string", "default": "USD"},
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed", "failed", "refunded"],
                    "default": "pending"
                },
                "payment_method": {"type": "string"},
                "transaction_id": {"type": ["string", "null"]},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["payment_id", "invoice_id", "amount", "currency", "status"]
        })
        super().__init__(
            schema=schema,
            entity_type="payment",
            **kwargs
        )


class Subscription(XWEntity):
    """
    Subscription entity for billing capability.
    Represents a subscription to a billing plan.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize Subscription entity."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "subscription_id": {"type": "string"},
                "customer_id": {"type": "string"},
                "plan_id": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["active", "cancelled", "expired", "suspended"],
                    "default": "active"
                },
                "start_date": {"type": "string", "format": "date-time"},
                "end_date": {"type": ["string", "null"], "format": "date-time"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["subscription_id", "customer_id", "plan_id", "status"]
        })
        super().__init__(
            schema=schema,
            entity_type="subscription",
            **kwargs
        )


class Plan(XWEntity):
    """
    Billing plan entity for billing capability.
    Represents a billing plan definition with pricing.
    This is an optional BaaS entity.
    """

    def __init__(self, **kwargs):
        """Initialize Plan entity."""
        schema = XWSchema({
            "type": "object",
            "properties": {
                "plan_id": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": ["string", "null"]},
                "price": {"type": "number"},
                "currency": {"type": "string", "default": "USD"},
                "billing_interval": {
                    "type": "string",
                    "enum": ["monthly", "yearly", "one-time"],
                    "default": "monthly"
                },
                "features": {"type": "array", "items": {"type": "string"}},
                "is_active": {"type": "boolean", "default": True},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["plan_id", "name", "price", "currency", "billing_interval"]
        })
        super().__init__(
            schema=schema,
            entity_type="plan",
            **kwargs
        )
__all__ = ['Invoice', 'Payment', 'Subscription', 'Plan']
