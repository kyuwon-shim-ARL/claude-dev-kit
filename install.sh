#!/bin/bash
# Claude Dev Kit: One-Click Installation Script
# Usage: curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install.sh | bash -s project_name

set -e

PROJECT_NAME=${1:-"my_project"}
PROJECT_DESC=${2:-"A new Claude Code project"}
CURRENT_DATE=$(date +%Y-%m-%d)

echo "🚀 Installing Claude Dev Kit for: $PROJECT_NAME"
echo "==============================================="
echo ""

# Create directory structure
echo "📁 Creating project structure..."
for dir in "src/$PROJECT_NAME" "src/$PROJECT_NAME/core" "src/$PROJECT_NAME/models" \
           "src/$PROJECT_NAME/services" "core_features" "docs/CURRENT" \
           "docs/development/conversations" "docs/development/guides" \
           "docs/development/templates" "docs/specs" "examples" "tests" \
           "tools" "scripts" "archive"; do
    mkdir -p "$dir"
    echo "  ✅ Created: $dir"
done

# Create essential files
echo ""
echo "📝 Creating essential files..."

# 1. CLAUDE.md
cat > CLAUDE.md << EOF
# $PROJECT_NAME: Claude Code Project

## Project Overview
$PROJECT_DESC

## Development Environment Setup

### Quick Start
\`\`\`bash
# 1. Set up environment
echo "# Add your environment variables here" > .env

# 2. Install dependencies and test
python scripts/scripts/test_setup.py

# 3. Run main application
python main_app.py
\`\`\`

## Development Workflow (Claude Code)

### Keyword Commands
- **"분석"** → Analyze current state + requirements planning
- **"시작"** → Create TodoWrite plan, begin implementation
- **"정리"** → Refactor, organize files
- **"검증"** → Test and validate
- **"커밋"** → Create meaningful commits

### Project Structure Guidelines
Keep root clean with only essential files.
See \`docs/development/guides/\` for detailed workflows.

## Key Commands

### Development
\`\`\`bash
python scripts/scripts/test_setup.py    # Verify system setup
python main_app.py      # Run main application
\`\`\`

## Testing Strategy

### Setup Verification
- \`scripts/test_setup.py\`: Complete system verification
- Tests core functionality and component integration

## Project Structure
\`\`\`
src/$PROJECT_NAME/       # Core implementation
├── core/               # Core components
├── models/             # Data schemas  
└── services/           # Service layer

core_features/          # Verified standalone features
docs/                   # Documentation
├── CURRENT/            # Current project status
├── development/        # Development process records
│   ├── conversations/  # Development session archives
│   ├── templates/      # Documentation templates
│   └── guides/         # Development guides
└── specs/              # Project specifications

examples/               # Usage examples and tutorials
tests/                  # Unit and integration tests
tools/                  # Development and utility scripts
scripts/                # Automation scripts
archive/                # Organized legacy code
\`\`\`

## Contributing Guidelines

### Code Style
- Type hints required for all functions
- Docstrings for all public methods
- Follow clean code principles

### Testing Requirements
- All new features need tests
- Integration tests for system components
- Examples should demonstrate real usage

### Documentation
- Update CLAUDE.md for architectural changes
- Add docstrings for new classes/methods
- Include usage examples for new features
EOF

# 2. main_app.py
cat > main_app.py << 'EOF'
#!/usr/bin/env python3
"""
Main application entry point for Claude Code project.
This is the primary interface for running the application.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main application function."""
    print("🚀 Starting application...")
    print(f"📁 Project root: {Path(__file__).parent}")
    print("✅ Application started successfully")
    
    # TODO: Add your main application logic here
    # Example:
    # from src.your_project.core.app import App
    # app = App()
    # app.run()

if __name__ == "__main__":
    main()
EOF

# 3. scripts/test_setup.py
cat > scripts/test_setup.py << 'EOF'
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
    root = Path(__file__).parent
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
EOF

# 4. .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Temporary files
tmp/
temp/
.tmp/

# Documentation builds
_build/
.doctrees/

# Jupyter Notebook
.ipynb_checkpoints

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json
EOF

# 5. Create example files
cat > "examples/basic_usage.py" << 'EOF'
#!/usr/bin/env python3
"""
Basic usage example for the Claude Code project.
This demonstrates the fundamental functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def run_basic_example():
    """Run a basic usage example."""
    print("🎯 Running basic usage example...")
    
    # TODO: Add your basic usage example here
    # Example:
    # from your_project.core.service import YourService
    # service = YourService()
    # result = service.process()
    # print(f"Result: {result}")
    
    print("✅ Basic example completed successfully")

if __name__ == "__main__":
    run_basic_example()
EOF

# 6. Create workflow guide
cat > "docs/development/guides/claude-code-workflow.md" << 'EOF'
# Claude Code Development Workflow

## Keyword-Based Development

### 1. 기획 (Structured Discovery & Planning Loop)
- **탐색**: 전체 구조 파악, As-Is/To-Be/Gap 분석
- **계획**: MECE 기반 작업분해(WBS), 우선순위 매트릭스
- **수렴**: 탐색↔계획 반복 until PRD 완성 & TodoWrite 구조화

### 2. 구현 (Implementation with DRY)  
- **DRY 원칙**: 기존 코드 검색 → 재사용 → 없으면 생성
- **체계적 진행**: TodoWrite 기반 단계별 구현
- **품질 보증**: 단위 테스트 + 기본 검증

### 3. 안정화 (Structural Sustainability Protocol v2.0)
**패러다임 전환**: 기능 중심 → **구조적 지속가능성** 중심

**6단계 통합 검증 루프:**
1. **Repository Structure Scan**: 전체 파일 분석, 중복/임시 파일 식별
2. **Structural Optimization**: 디렉토리 정리, 파일 분류, 네이밍 표준화  
3. **Dependency Resolution**: Import 수정, 참조 오류 해결, 환경 동기화
4. **Comprehensive Testing**: 모듈 검증, API 테스트, 시스템 무결성 확인
5. **Documentation Sync**: CLAUDE.md 반영, README 업데이트, .gitignore 정리
6. **Quality Assurance**: MECE 분석, 성능 벤치마크, 정량 평가

**예방적 관리**: 루트 20개 파일, 임시 파일 5개, Import 오류 3개 이상 시 자동 실행

### 4. 배포 (Deployment)
- **최종 검증**: 체크리스트 완료 확인
- **구조화 커밋**: 의미있는 커밋 메시지 생성
- **원격 배포**: 푸시 + 버전 태깅

## TodoWrite Usage

Always use TodoWrite for tasks with 3+ steps:

```python
todos = [
    {"content": "분석: 현황 파악 + 요구사항 정리", "status": "in_progress", "id": "001"},
    {"content": "시작: 핵심 기능 구현", "status": "pending", "id": "002"},
    {"content": "검증: 테스트 및 문서화", "status": "pending", "id": "003"}
]
```

## MECE Progress Tracking

Provide quantitative, specific progress updates:
- ❌ "거의 다 됐어요"
- ✅ "3/4 주요 기능 완료, 1개 DB 연결 이슈 남음"
EOF

# 7. Create session template
cat > "docs/development/templates/session-template.md" << 'EOF'
# Development Session: [Date] - [Topic]

## 목표 (Objective)
[Clear session goal]

## 현황 분석 (Current State)
[Current project status and context]

## 작업 계획 (Work Plan)
[TodoWrite task breakdown]

## 진행 과정 (Progress)
[Real-time updates and decisions made]

## 결과 (Results)
[What was accomplished]

## 학습 (Learnings)
[Key insights and lessons learned]

## 다음 단계 (Next Steps)
[Follow-up actions needed]

---
Session archived: [timestamp]
EOF

# Make scripts executable
chmod +x main_app.py
chmod +x scripts/test_setup.py
chmod +x examples/basic_usage.py

echo ""
echo "🎉 Claude Dev Kit installation complete!"
echo ""
echo "📋 Summary:"
echo "  ✅ Created project structure for '$PROJECT_NAME'"
echo "  ✅ Generated essential files and templates"
echo "  ✅ Set up development workflow guides"
echo ""
echo "🔍 Running system validation..."

# Automatic validation and cleanup
if python scripts/test_setup.py; then
    echo ""
    echo "✅ Validation successful - cleaning up..."
    rm scripts/test_setup.py
    echo "🎉 Claude Code installation complete!"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Configure Custom Instructions in Claude.ai (see claude-me-settings-minimal.md)"
    echo "  2. Start development with keywords: @기획, @구현, @안정화, @배포"
    echo ""
    echo "📚 Key files created:"
    echo "  - CLAUDE.md (project documentation)"
    echo "  - main_app.py (application entry point)"
    echo "  - examples/basic_usage.py (usage example)"
    echo "  - docs/development/guides/ (workflow guides)"
    echo "  - claude-me-settings-minimal.md (Custom Instructions template)"
else
    echo ""
    echo "❌ Validation failed"
    echo "🔧 Debugging: Check scripts/test_setup.py for details"
    echo "💡 Common issues:"
    echo "  - Missing Python 3.x"
    echo "  - Virtual environment not activated"
    echo "  - Dependency installation problems"
    echo ""
    echo "🔄 To retry validation: python scripts/test_setup.py"
    exit 1
fi