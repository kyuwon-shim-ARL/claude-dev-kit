#!/usr/bin/env python3
"""
System validation and setup verification script.
Run this to ensure your development environment is properly configured.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_project_structure():
    """Verify project directory structure."""
    root = Path.cwd()
    
    # 안전장치: 올바른 프로젝트 루트인지 확인
    if not (root / "CLAUDE.md").exists():
        print("❌ Error: Not in a Claude Code project directory")
        print("💡 Run this script from the project root directory")
        return False
    
    required_dirs = [
        "src", "core_features", "docs", "examples", 
        "tests", "tools", "scripts", "archive"
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not (root / directory).exists():
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("✅ Project structure complete")
    return True

def check_essential_files():
    """Check for essential project files."""
    root = Path.cwd()
    
    # 안전장치: 올바른 프로젝트 루트인지 확인
    if not (root / "CLAUDE.md").exists():
        print("❌ Error: Not in a Claude Code project directory")
        print("💡 Run this script from the project root directory")
        return False
    
    essential_files = ["CLAUDE.md", "main_app.py"]
    
    missing_files = []
    for file_name in essential_files:
        if not (root / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ Essential files present")
    return True

def main():
    """Run complete system validation."""
    print("🔍 Running Claude Code setup validation...")
    print("=" * 45)
    
    checks = [
        check_python_version,
        check_project_structure, 
        check_essential_files
    ]
    
    results = []
    for check in checks:
        try:
            results.append(check())
        except Exception as e:
            print(f"❌ Check failed: {e}")
            results.append(False)
    
    print("=" * 45)
    if all(results):
        print("🎉 Setup validation passed!")
        print("")
        print("🔧 Next steps:")
        print("  1. Start with: '현재 상태 분석해줘'")
        print("  2. Use keywords: 분석, 시작, 정리, 검증, 커밋")
        print("  3. Run: python main_app.py")
        return True
    else:
        print("💥 Setup validation failed!")
        print("Please fix the issues above and run again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
