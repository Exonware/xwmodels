"""
Pytest configuration for xwmodels tests.
Ensures project src is on sys.path first so exonware.xwmodels resolves to this package.
"""
from pathlib import Path
import sys

# Prepend project src so exonware.xwmodels is found from this repo when multiple exonware packages exist
_root = Path(__file__).resolve().parent.parent
_src = _root / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))
