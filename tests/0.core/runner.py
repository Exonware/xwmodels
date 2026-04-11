#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/0.core/runner.py
Core test runner for xwmodels.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import pytest


def main() -> int:
    """Run core tests."""
    tests_root = Path(__file__).parent
    return pytest.main(["-v", str(tests_root)])


if __name__ == "__main__":
    sys.exit(main())
