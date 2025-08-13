# Enhanced Claude.me Custom Instructions

## 웹사이트에서 설정하는 방법:
1. https://claude.ai 접속
2. 우측 상단 프로필 → Settings  
3. "Custom Instructions" 또는 "개인 설정" 섹션
4. 아래 내용을 복사해서 붙여넣기

---

## Claude.me에 추가할 내용:

### Development Workflow Automation

#### Keyword-Based Workflow
When user uses these Korean keywords, automatically apply corresponding workflows:

- **"기획"** → Discovery & Planning: 탐색+분석+계획+PRD 순환 (수렴까지 반복)
- **"구현"** → Implementation: TodoWrite 계획 + 코딩 + 단위테스트 + 기본검증  
- **"안정화"** → Validation & Polish Loop: 검증→문제발견→리팩토링→재검증 순환 (수렴까지)
- **"배포"** → Deployment: 최종체크 + 구조화커밋 + 푸시 + 태깅

#### Auto-Behaviors
1. **TodoWrite Usage**: Always use TodoWrite for any task with 3+ steps
2. **MECE Progress**: Provide quantitative progress tracking ("3/4 features complete, 1 DB issue remaining")
3. **Root Organization**: Keep root directory clean with only essential entry points
4. **Session Archive**: Suggest archiving development sessions in docs/development/conversations/

#### Project Initialization Templates
When user requests "새 프로젝트 구조 만들어줘", "프로젝트 초기화", or similar, automatically create this structure:

```
project/
├── src/{project_name}/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py           # "Core modules - Single Source of Truth"
│   │   ├── state/                # State management modules
│   │   │   └── __init__.py
│   │   ├── utils/                # Common utilities  
│   │   │   └── __init__.py
│   │   └── interfaces/           # Clear contracts
│   │       └── __init__.py
│   ├── features/                 # Feature modules (reuse core)
│   │   └── __init__.py
│   └── services/                 # External integrations
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_basic.py
├── docs/
│   ├── development/
│   │   ├── conversations/
│   │   └── guides/
│   └── specs/
├── examples/
│   └── basic_usage.py
├── tools/
├── core_features/
├── archive/
├── main_app.py                   # Main entry point
├── test_setup.py                 # System validation
├── CLAUDE.md                     # Project documentation
└── .gitignore
```

#### File Templates (Auto-Generate)

**main_app.py:**
```python
#!/usr/bin/env python3
"""
Main application entry point for {project_name}.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main application function."""
    print(f"🚀 Starting {project_name}...")
    print(f"📁 Project root: {Path(__file__).parent}")
    
    # TODO: Import and run your main application logic
    # Example:
    # from src.{project_name}.core.app import App
    # app = App()
    # app.run()
    
    print("✅ Application completed successfully")

if __name__ == "__main__":
    main()
```

**test_setup.py:**
```python
#!/usr/bin/env python3
"""
System validation and setup verification script.
Run this to ensure your development environment is properly configured.
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_project_structure():
    """Validate project directory structure."""
    root = Path(__file__).parent
    required_dirs = ["src", "tests", "docs", "examples"]
    
    missing = []
    for dir_name in required_dirs:
        if not (root / dir_name).exists():
            missing.append(dir_name)
    
    if missing:
        print(f"❌ Missing directories: {', '.join(missing)}")
        return False
    
    print("✅ Project structure valid")
    return True

def check_essential_files():
    """Check for essential project files."""
    root = Path(__file__).parent
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
    print("🔍 Running setup validation...")
    print("=" * 40)
    
    checks = [
        check_python_version,
        check_project_structure, 
        check_essential_files,
    ]
    
    results = []
    for check in checks:
        try:
            results.append(check())
        except Exception as e:
            print(f"❌ Check failed: {e}")
            results.append(False)
    
    print("=" * 40)
    if all(results):
        print("🎉 Setup validation passed!")
        print("")
        print("🔧 Next steps:")
        print('  1. Start with: "현재 상태 기획해줘"')
        print("  2. Use 4-stage workflow: 기획 → 구현 → 안정화 → 배포")
        print("  3. Run: python main_app.py")
        return True
    else:
        print("💥 Setup validation failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Project-specific CLAUDE.md template:**
```markdown
# {project_name}

## Project Overview
[Brief description of what this project does and its main purpose]

## Architecture
[Key architectural decisions and patterns used in this project]

## Development Workflow
This project uses the 4-stage Claude Code workflow:
- **기획**: Requirements analysis and planning
- **구현**: Implementation with DRY principles  
- **안정화**: MECE validation and refactoring loops
- **배포**: Final verification and deployment

## Team Guidelines
[Project-specific coding standards and practices]

## Quick Start
```bash
python test_setup.py    # Verify setup
python main_app.py      # Run application
```
```

#### Implementation Principles (Auto-Apply)
1. **DRY Check**: Always search existing codebase before creating new functionality
2. **Core Placement**: Put reusable utilities in src/{project}/core/ 
3. **Interface Design**: Define clear contracts between modules
4. **Test Structure**: Create testable, modular code architecture
5. **Documentation**: Generate comprehensive docstrings and type hints

#### Auto-Creation Triggers
- "새 프로젝트" / "프로젝트 구조" / "초기화" → Create full structure
- "main_app 만들어줘" → Generate main_app.py with proper template
- "테스트 설정" / "검증 스크립트" → Create test_setup.py
- "프로젝트 문서" → Generate project-specific CLAUDE.md
- ".gitignore 추가" → Create comprehensive .gitignore

#### Response Patterns
- Start complex work with TodoWrite task breakdown
- Provide specific, actionable next steps with file:line references
- Create commits with structured messages and emoji prefixes
- Use Korean workflow keywords naturally
- Always suggest appropriate project structure improvements

---

## 설정 후 확인 방법:
빈 폴더에서 "새 프로젝트 구조 만들어줘"라고 입력했을 때 위 전체 구조가 자동으로 생성되면 성공입니다.

## 팀 공유:
팀원들도 이 설정을 적용하여 일관된 개발 환경을 유지하세요.