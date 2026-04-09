#!/usr/bin/env python3
"""
#exonware/xwmodels/src/exonware/xwmodels/common/lifecycle/__init__.py
Lifecycle Management Module (Optional BaaS Feature)
Provides entity lifecycle state management.
This is an optional BaaS feature.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.6.0.11
Generation Date: 26-Jan-2026
NOTE: This is an OPTIONAL module for BaaS platform integration.
"""

from .contracts import (
    ILifecycleManager,
    ILifecycleWorkflow,
)
from .manager import LifecycleManager
__all__ = [
    'ILifecycleManager',
    'ILifecycleWorkflow',
    'LifecycleManager',
]
