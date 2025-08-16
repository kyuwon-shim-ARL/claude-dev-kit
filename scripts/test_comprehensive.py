#!/usr/bin/env python3
"""
Comprehensive test suite for claude-dev-kit
"""

import subprocess
import sys
from pathlib import Path

def test_installation_scripts():
    """Test that installation scripts work correctly"""
    print('🧪 Testing installation scripts...')
    
    # Test basic syntax
    scripts = ['install.sh', 'install-web.sh', 'init-claude-repo.sh', 'safe-init-claude-repo.sh']
    for script in scripts:
        result = subprocess.run(['bash', '-n', script], capture_output=True)
        if result.returncode != 0:
            print(f'❌ {script} syntax error')
            return False
        print(f'  ✅ {script} syntax OK')
    
    return True

def test_python_modules():
    """Test Python module imports"""
    print('🧪 Testing Python modules...')
    
    py_files = list(Path('.').rglob('*.py'))
    if not py_files:
        print('  ✅ No Python modules to test')
        return True
    
    for py_file in py_files:
        result = subprocess.run([sys.executable, '-m', 'py_compile', str(py_file)], 
                              capture_output=True)
        if result.returncode != 0:
            print(f'❌ {py_file} compilation failed')
            return False
        print(f'  ✅ {py_file} compiled successfully')
    
    return True

def test_file_structure():
    """Test required file structure"""
    print('🧪 Testing file structure...')
    
    required_files = ['CLAUDE.md', 'install.sh', 'install-web.sh']
    required_dirs = ['docs', 'scripts']
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f'❌ Missing required file: {file_path}')
            return False
        print(f'  ✅ {file_path} exists')
    
    for dir_path in required_dirs:
        if not Path(dir_path).is_dir():
            print(f'❌ Missing required directory: {dir_path}')
            return False
        print(f'  ✅ {dir_path}/ exists')
    
    return True

def main():
    """Run all tests"""
    print('🔬 Running comprehensive test suite...')
    print('=' * 50)
    
    tests = [
        test_installation_scripts,
        test_python_modules,
        test_file_structure
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f'❌ Test failed with exception: {e}')
            results.append(False)
        print()
    
    print('=' * 50)
    if all(results):
        print('🎉 All tests passed!')
        return True
    else:
        print('💥 Some tests failed!')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

