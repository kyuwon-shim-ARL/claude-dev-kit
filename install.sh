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

# Check if this is an existing project
if [ -f "CLAUDE.md" ]; then
    echo "  📋 Existing CLAUDE.md detected - creating append template"
    # Create append template for existing projects
    cat > CLAUDE-APPEND-TEMPLATE.md << 'TEMPLATE_EOF'
# Claude Code 4단계 개발 워크플로우

## 개발 워크플로우

이 프로젝트는 4단계 키워드 기반 개발을 사용합니다:
- **"기획"** → Structured Discovery & Planning Loop:
  - 탐색: 전체 구조 파악, As-Is/To-Be/Gap 분석
  - 계획: MECE 기반 작업분해, 우선순위 설정
  - 수렴: 탐색↔계획 반복 until PRD 완성
- **"구현"** → Implementation with DRY:
  - 기존 코드 검색 → 재사용 → 없으면 생성
  - TodoWrite 기반 체계적 진행
  - 단위 테스트 & 기본 검증
- **"안정화"** → **Structural Sustainability Protocol v2.0**:
  - 구조 스캔: 전체 파일 분석, 중복/임시 파일 식별
  - 구조 최적화: 디렉토리 정리, 파일 분류, 네이밍 표준화
  - 의존성 해결: Import 수정, 참조 오류 해결
  - 통합 테스트: 모듈 검증, API 테스트, 시스템 무결성
  - 문서 동기화: CLAUDE.md 반영, README 업데이트
  - 품질 검증: MECE 분석, 성능 벤치마크 (ZERO 이슈까지)
- **"배포"** → Deployment: 최종검증 + 구조화커밋 + 푸시 + 태깅

## 구현 체크리스트

### 구현 전 확인사항
- ☐ **기존 코드 검색**: 비슷한 기능이 이미 있는가?
- ☐ **재사용성 검토**: 이 기능을 다른 곳에서도 사용할 수 있는가?
- ☐ **중앙화 고려**: 공통 모듈로 배치할가?
- ☐ **인터페이스 설계**: 모듈 간 명확한 계약이 있는가?
- ☐ **테스트 가능성**: 단위 테스트하기 쉬운 구조인가?

### 코드 품질 체크
- ☐ **DRY 원칙**: 코드 중복이 없는가?
- ☐ **Single Source of Truth**: 동일 기능이 여러 곳에 있지 않는가?
- ☐ **의존성 최소화**: 불필요한 결합이 없는가?
- ☐ **명확한 네이밍**: 기능을 잘 나타내는 이름인가?

## 구조적 지속가능성 원칙

### 📁 Repository 구조 관리
- **Root 정리**: 필수 진입점만 유지, 도구는 scripts/
- **계층구조**: 기능별 적절한 디렉토리 배치
- **임시 파일 관리**: *.tmp, *.bak 등 정기적 정리

### 🔄 예방적 관리 시스템
**자동 트리거 조건:**
- 루트 디렉토리 파일 20개 이상
- 임시 파일 5개 이상
- Import 오류 3개 이상
- 매 5번째 커밋마다

## important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
TEMPLATE_EOF
    echo "  ✅ Created: CLAUDE-APPEND-TEMPLATE.md (for existing project)"
else
    echo "  📋 Creating new CLAUDE.md"
    # 1. CLAUDE.md for new projects
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
fi

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

# 8. Setup Claude context management (Git hooks + project files)
echo ""
echo "🤖 Setting up Claude context management..."

# Create hooks directory if it doesn't exist (for git repos)
if [ -d ".git" ]; then
    mkdir -p .git/hooks
    
    # Create pre-commit hook
    cat > .git/hooks/pre-commit << 'HOOK_EOF'
#!/bin/sh
# Claude Dev Kit: Auto-update claude.md before commit

echo "🤖 Auto-updating claude.md..."

# Check if claude command is available
if command -v claude &> /dev/null; then
    # Run claude init silently
    claude init --silent
    
    # Add claude.md to staging if it exists and was modified
    if [ -f "claude.md" ]; then
        git add claude.md
        echo "✅ claude.md updated and staged"
    fi
else
    echo "⚠️  Warning: claude command not found, skipping auto-update"
    echo "💡 Install Claude Code: https://docs.anthropic.com/claude/docs/claude-code"
fi

echo "🎯 Proceeding with commit..."
HOOK_EOF
    
    # Make the hook executable
    chmod +x .git/hooks/pre-commit
    echo "  ✅ Git pre-commit hook installed"
fi

# Create project_rules.md template
cat > project_rules.md << 'RULES_EOF'
# Project Rules (프로젝트 헌법)

## 프로젝트 목표
[이 프로젝트의 핵심 목적과 비전을 명시]

## 아키텍처 원칙
- **단일 진실 공급원**: 동일한 기능은 한 곳에만 구현
- **모듈 분리**: 명확한 인터페이스로 모듈 간 결합도 최소화
- **확장성 우선**: 새로운 기능 추가가 용이한 구조
- **테스트 가능성**: 모든 핵심 기능은 테스트 가능하도록 설계

## 코딩 스타일 (변경 금지)
- **Python**: PEP 8 준수, type hints 필수
- **명명 규칙**: snake_case (함수/변수), PascalCase (클래스)
- **문서화**: 모든 public 함수에 docstring 필수
- **Import 순서**: standard library → third-party → local imports

## DevOps 규칙
- **브랜치 전략**: main 브랜치 직접 push 금지, PR 필수
- **커밋 메시지**: [타입] 제목 (예: [feat] 사용자 인증 추가)
- **테스트**: 모든 PR은 테스트 통과 필수
- **문서**: README.md와 API 문서 항상 최신 유지

## 보안 정책
- **환경 변수**: .env 파일 사용, .gitignore에 포함
- **API 키**: 코드에 하드코딩 금지
- **의존성**: 정기적 보안 업데이트 확인

## 성능 기준
- **응답 시간**: API 엔드포인트 500ms 이하
- **메모리 사용량**: 프로덕션 환경에서 1GB 이하
- **코드 복잡도**: Cyclomatic complexity 10 이하

---
⚠️ **중요**: 이 파일은 프로젝트의 핵심 규칙을 담고 있습니다.
수정 시에는 팀 전체의 합의가 필요하며, claude init의 영향을 받지 않습니다.
RULES_EOF
echo "  ✅ Created: project_rules.md (project constitution)"

# Create .claudeignore
cat > .claudeignore << 'IGNORE_EOF'
# Claude Context Ignore File
# Files and directories listed here will be excluded from claude.md generation

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/
env/

# Build outputs
dist/
build/
*.egg-info/
.coverage
htmlcov/

# Logs and temporary files
*.log
logs/
tmp/
temp/
.tmp/
*.tmp
*.bak

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Database files
*.db
*.sqlite
*.sqlite3

# Large binary files
*.pdf
*.jpg
*.jpeg
*.png
*.gif
*.mp4
*.avi
*.zip
*.tar.gz

# Generated documentation
_build/
site/
IGNORE_EOF
echo "  ✅ Created: .claudeignore (context quality control)"

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
    if [ -f "CLAUDE.md" ] && [ ! -f "CLAUDE-APPEND-TEMPLATE.md" ]; then
        # New installation
        echo "  1. Configure Custom Instructions in Claude.ai (see claude-me-settings-minimal.md)"
        echo "  2. Start development with keywords: @기획, @구현, @안정화, @배포"
    else
        # Existing project
        echo "  1. Existing CLAUDE.md detected - append workflow from CLAUDE-APPEND-TEMPLATE.md"
        echo "  2. Configure Custom Instructions in Claude.ai (see claude-me-settings-minimal.md)"
        echo "  3. Start development with keywords: @기획, @구현, @안정화, @배포"
    fi
    echo ""
    echo "📚 Key files created:"
    if [ -f "CLAUDE-APPEND-TEMPLATE.md" ]; then
        echo "  - CLAUDE-APPEND-TEMPLATE.md (append to existing CLAUDE.md)"
        echo "  - main_app.py (application entry point)"
    else
        echo "  - CLAUDE.md (project documentation)"
        echo "  - main_app.py (application entry point)"
    fi
    echo "  - examples/basic_usage.py (usage example)"
    echo "  - docs/development/guides/ (workflow guides)"
    echo "  - project_rules.md (project constitution - edit this!)"
    echo "  - .claudeignore (context quality control)"
    echo "  - claude-me-settings-minimal.md (Custom Instructions template)"
    if [ -d ".git" ]; then
        echo "  - .git/hooks/pre-commit (auto-updates claude.md)"
    fi
    echo ""
    echo "🤖 Claude context management ready!"
    echo "  Edit project_rules.md with your specific project rules"
    echo "  Run 'claude init' to generate initial claude.md"
    echo "  Commit will auto-update claude.md from now on"
    echo ""
    echo "⚡ Setting up Claude Code slash commands..."
    
    # Download and install Claude Code commands
    if command -v curl &> /dev/null; then
        mkdir -p .claude/commands
        curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts/claude-commands/기획.md -o .claude/commands/기획.md
        curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts/claude-commands/구현.md -o .claude/commands/구현.md
        curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts/claude-commands/안정화.md -o .claude/commands/안정화.md
        curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/prompts/claude-commands/배포.md -o .claude/commands/배포.md
        echo "  ✅ Claude Code slash commands installed"
        echo "  💡 Use: /기획, /구현, /안정화, /배포"
    else
        echo "  ⚠️  curl not found - slash commands not installed"
    fi
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