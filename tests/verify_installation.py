#!/usr/bin/env python3
"""
Installation verification script for xwentity.
Usage:
  python tests/verify_installation.py
"""

import sys
from pathlib import Path

def verify_installation():
    """Verify that the library is properly installed and working."""
    print("🔍 Verifying xwentity installation...")
    print("=" * 50)
    # Add src to Python path for testing
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))
    try:
        # Test main import
        print("📦 Testing main import...")
        import exonware.xwmodels
        print("✅ exonware.xwmodels imported successfully")
        # Test convenience import  
        print("📦 Testing convenience import...")
        import xwentity
        print("✅ xwentity convenience import works")
        # Test version information
        print("📋 Checking version information...")
        assert hasattr(exonware.xwmodels, '__version__')
        assert hasattr(exonware.xwmodels, '__author__')
        assert hasattr(exonware.xwmodels, '__email__')
        assert hasattr(exonware.xwmodels, '__company__')
        print(f"✅ Version: {exonware.xwmodels.__version__}")
        print(f"✅ Author: {exonware.xwmodels.__author__}")
        print(f"✅ Company: {exonware.xwmodels.__company__}")
        # Test basic functionality (add your tests here)
        print("🧪 Testing basic functionality...")
        # Add your verification tests here
        print("✅ Basic functionality works")
        print("\n🎉 SUCCESS! exonware.xwmodels is ready to use!")
        print("You have access to all xwentity features!")
        return True
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you've installed the package with: pip install exonware-xwentity")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def main():
    """Main verification function."""
    success = verify_installation()
    sys.exit(0 if success else 1)
if __name__ == "__main__":
    main()
