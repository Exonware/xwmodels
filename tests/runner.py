#!/usr/bin/env python3
"""
#exonware/xwmodels/tests/runner.py
Main test runner for xwmodels.
Usage:
  python tests/runner.py
  python tests/runner.py --core
  python tests/runner.py --unit
  python tests/runner.py --integration
"""

import sys
from pathlib import Path

import pytest


def main() -> int:
    """Main test runner function."""
    workspace_root = Path(__file__).parent.parent.parent
    src_paths = [
        Path(__file__).parent.parent / "src",
        workspace_root / "xwdata" / "src",
        workspace_root / "xwaction" / "src",
        workspace_root / "xwentity" / "src",
        workspace_root / "xwschema" / "src",
        workspace_root / "xwsystem" / "src",
        workspace_root / "xwlazy" / "src",
    ]
    for src_path in src_paths:
        if src_path.exists() and str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
    tests_root = Path(__file__).parent
    args = sys.argv[1:]
    if "--core" in args:
        exit_code = pytest.main(["-v", str(tests_root / "0.core")])
    elif "--unit" in args:
        exit_code = pytest.main(["-v", str(tests_root / "1.unit")])
    elif "--integration" in args:
        exit_code = pytest.main(["-v", str(tests_root / "2.integration")])
    else:
        exit_code = pytest.main(
            [
                "-v",
                str(tests_root / "0.core"),
                str(tests_root / "1.unit"),
                str(tests_root / "2.integration"),
            ]
        )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
