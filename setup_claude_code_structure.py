#!/usr/bin/env python3
"""
Claude Code Project Structure Setup Script
Creates the optimal directory structure for Claude Code development
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def create_directory_structure(project_name: str, base_path: str = "."):
    """Create the complete Claude Code project structure"""
    
    base = Path(base_path)
    
    # Check if this is an existing project
    is_existing_project = any([
        (base / "src").exists(),
        (base / "app.py").exists(),
        (base / "main.py").exists(),
        (base / "package.json").exists(),
        (base / "pyproject.toml").exists(),
        (base / "Cargo.toml").exists(),
        (base / "requirements.txt").exists(),
        (base / "setup.py").exists(),
    ])
    
    # Core directories
    directories = []
    
    # Only create src/{project_name} for new projects
    if not is_existing_project:
        directories.extend([
            f"src/{project_name}",
            f"src/{project_name}/core",
            f"src/{project_name}/models", 
            f"src/{project_name}/services",
        ])
    
    # Always create these Claude Code specific directories
    directories.extend([
        # Active components
        "core_features",
        
        # Documentation & examples
        "docs/CURRENT",
        "docs/development/conversations",
        "docs/development/guides", 
        "docs/development/templates",
        "docs/specs",
        
        "examples",
        
        # Testing & infrastructure
        "tests",
        "tools",
        "scripts",
        
        # Organized archive
        "archive/legacy_code",
        "archive/experiments", 
        "archive/old_docs",
    ])
    
    if is_existing_project:
        print(f"🔄 Adding Claude Code structure to existing project: {project_name}")
        print("📌 Note: Not creating src/{project_name} as project already exists")
    else:
        print(f"🏗️ Creating Claude Code structure for new project: {project_name}")
    print("=" * 60)
    
    for directory in directories:
        dir_path = base / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")
        else:
            print(f"⏭️  Skipped (exists): {directory}")
    
    # Create essential files
    essential_files = {}
    
    # Only create main entry points for new projects
    if not is_existing_project:
        essential_files.update({
            "main_app.py": "# Main application entry point\npass\n",
            f"src/{project_name}/__init__.py": f'"""\n{project_name}: [Project description]\n"""\n\n__version__ = "0.1.0"\n',
        })
    
    # Always create these files
    essential_files.update({
        "test_setup.py": "#!/usr/bin/env python3\n# System validation script\nprint('✅ Setup validation passed')\n",
        
        # Configuration (only if not exists)
        ".env.example": "# Example environment configuration\n# Copy to .env and configure\n",
        
        # Documentation templates
        "docs/development/templates/session-template.md": """# Session: [DATE] - [TOPIC]

## Objective
[What we're trying to accomplish]

## Tasks Completed
- [ ] Task 1
- [ ] Task 2

## Key Decisions
- Decision 1: Rationale
- Decision 2: Rationale

## Next Steps
1. Next action
2. Following action

## Files Changed
- file1.py: Description of changes
- file2.py: Description of changes
""",
        
        "docs/development/guides/claude-code-workflow.md": """# Claude Code Workflow Guide

## Key Principles
1. **TodoWrite Usage**: Track all multi-step tasks
2. **MECE Analysis**: Mutually Exclusive, Collectively Exhaustive progress tracking
3. **Session Archiving**: Document all development sessions
4. **Clean Commits**: Meaningful commit messages with context

## Command Patterns
- "탐색" → Analyze codebase, identify issues
- "시작" → Plan with TodoWrite, begin execution  
- "정리" → Refactor, organize, cleanup
- "검증" → Test, validate, document
- "커밋" → Create meaningful commits with full context

## File Organization
Keep root directory clean with only essential entry points.
""",
        
        # Basic test
        "tests/test_basic.py": """#!/usr/bin/env python3
import pytest

def test_basic_functionality():
    \"\"\"Test that basic imports work\"\"\"
    assert True
    
def test_setup_validation():
    \"\"\"Validate project setup\"\"\"
    from pathlib import Path
    assert Path('CLAUDE.md').exists()
""",
        
        # Example usage
        "examples/basic_usage.py": f"""#!/usr/bin/env python3
\"\"\"
Basic usage example for {project_name}
\"\"\"

import sys
sys.path.append('src')

# import {project_name}

def main():
    print(f"✅ {project_name} basic usage example")
    
if __name__ == "__main__":
    main()
""",
    })
    
    # Don't overwrite .gitignore if it exists
    if not (base / ".gitignore").exists():
        essential_files[".gitignore"] = """# Claude Code .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv/
venv/
.pytest_cache/
.coverage
*.log
"""
    
    print("\n📄 Creating essential files...")
    for file_path, content in essential_files.items():
        full_path = base / file_path
        if not full_path.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"✅ Created: {file_path}")
        else:
            print(f"⏭️  Skipped (exists): {file_path}")
    
    print("\n🎯 Claude Code project structure setup complete!")
    
    if is_existing_project:
        print("\n📊 Added Claude Code structure to existing project")
        print("Next steps:")
        print("1. Review and merge CLAUDE.md with existing documentation")
        print("2. Move legacy code to archive/ if needed")
        print("3. Run: python test_setup.py")
    else:
        print("\nNext steps:")
        print("1. Copy CLAUDE.md template and customize")
        print("2. Update project-specific details")
        print("3. Run: python test_setup.py")
    
    print("4. Start development with TodoWrite for task tracking")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        project_name = input("Enter project name (lowercase, no spaces): ")
    else:
        project_name = sys.argv[1]
    
    if not project_name.replace('_', '').isalnum():
        print("❌ Project name should be alphanumeric with underscores only")
        sys.exit(1)
        
    create_directory_structure(project_name)