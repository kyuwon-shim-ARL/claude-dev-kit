#!/bin/bash
# Claude Dev Kit: Complete Initialization Script
# One command to set up everything for claude-dev-kit
# Usage: ./init-complete.sh [project_name] [project_description]

set -e

PROJECT_NAME=${1:-"my_project"}
PROJECT_DESC=${2:-"A new Claude Code project"}
CURRENT_DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🚀 Claude Dev Kit Complete Installation"
echo "========================================"
echo "Project: $PROJECT_NAME"
echo "Description: $PROJECT_DESC"
echo ""

# Step 1: Create directory structure
echo "📁 Step 1/5: Creating project structure..."
for dir in "src/$PROJECT_NAME" "src/$PROJECT_NAME/core" "src/$PROJECT_NAME/models" \
           "src/$PROJECT_NAME/services" "core_features" "docs/CURRENT" \
           "docs/development/sessions" "docs/development/guides" \
           "docs/development/templates" "docs/specs" "examples" "tests" \
           "tools" "scripts" "archive" ".claude/commands"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "  ✅ Created: $dir"
    else
        echo "  ⏭️  Exists: $dir"
    fi
done

# Step 2: Install slash commands
echo ""
echo "⚡ Step 2/5: Installing slash commands..."
BASE_URL="https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.claude/commands"

# URL encode Korean characters properly
declare -A commands=(
    ["기획"]="%EA%B8%B0%ED%9A%8D"
    ["구현"]="%EA%B5%AC%ED%98%84"
    ["안정화"]="%EC%95%88%EC%A0%95%ED%99%94"
    ["배포"]="%EB%B0%B0%ED%8F%AC"
    ["전체사이클"]="%EC%A0%84%EC%B2%B4%EC%82%AC%EC%9D%B4%ED%81%B4"
    ["개발완료"]="%EA%B0%9C%EB%B0%9C%EC%99%84%EB%A3%8C"
    ["품질보증"]="%ED%92%88%EC%A7%88%EB%B3%B4%EC%A6%9D"
    ["기획구현"]="%EA%B8%B0%ED%9A%8D%EA%B5%AC%ED%98%84"
)

# Download each command
for cmd in "${!commands[@]}"; do
    encoded="${commands[$cmd]}"
    echo "  📥 Downloading /$cmd command..."
    curl -sSL "$BASE_URL/$encoded.md" -o ".claude/commands/$cmd.md" 2>/dev/null || {
        echo "  ⚠️  Failed to download $cmd.md from GitHub"
        echo "     Copying from local source..."
        if [ -f "$SCRIPT_DIR/.claude/commands/$cmd.md" ]; then
            cp "$SCRIPT_DIR/.claude/commands/$cmd.md" ".claude/commands/$cmd.md"
            echo "     ✅ Copied from local"
        else
            echo "     ❌ Local file not found either"
        fi
    }
done

echo "  ✅ All 8 slash commands installed"

# Step 3: Create project_rules.md if missing
echo ""
echo "📜 Step 3/5: Creating project_rules.md..."
if [ ! -f "project_rules.md" ]; then
    cat > project_rules.md << 'EOF'
# PROJECT_NAME Project Rules

## 🎯 Core Philosophy
- **중앙화된 프롬프트 관리**: prompts/api.json이 Single Source of Truth
- **Mock 테스트 금지**: 실제 사용자 시나리오 검증 필수
- **워크플로우 기반 개발**: /전체사이클 중심의 체계적 진행
- **Zero-Effort Documentation**: 슬래시 커맨드 사용만으로 자동 문서화

## 📐 Architecture Principles
- **프롬프트 동기화**: prompts/api.json → 모든 플랫폼 자동 동기화
- **4단계 워크플로우**: 기획 → 구현 → 안정화 → 배포
- **글로벌 슬래시 명령어**: 8개 명령어 표준화 (개별 4개 + 조합 4개)
- **3층 문서화 구조**: project_rules.md / docs/CURRENT/ / sessions/

## 🔧 Development Standards
- **배포 정의**: 배포 = 커밋 + 푸시 + 태깅 + 검증
- **DRY 원칙**: 코드 중복 절대 금지, 재사용 우선
- **구조적 지속가능성**: 6단계 검증 루프 필수 적용
- **정량적 검증**: "통과했습니다" 금지, 구체적 수치 제시

## 📚 Documentation Workflow
- **세션 시작**: project_rules.md + docs/CURRENT/status.md 자동 로드
- **작업 진행**: 각 단계별 자동 문서화
- **세션 종료**: /배포 시 자동으로 sessions/에 아카이브
- **토큰 효율**: 현재 컨텍스트만 로드 (< 1000 tokens)

## 🚀 Deployment Protocol
- **필수 푸시**: 커밋만 하고 끝내지 말고 반드시 원격 저장소에 푸시
- **버전 태깅**: semantic versioning 준수 (major.minor.patch)
- **세션 아카이빙**: 배포 시 자동으로 현재 세션을 아카이브
- **GitHub Raw URL**: 모든 프롬프트는 GitHub에서 직접 접근 가능

## ⚙️ Technical Stack
- **Python**: 3.8+ 필수, uv 패키지 매니저 권장
- **Git**: pre-commit hooks 자동 설정
- **Playwright**: 웹 프로젝트 E2E 테스트 필수
- **Claude Code**: 슬래시 명령어 기반 워크플로우

## 📊 Success Metrics
- **문서화 추가 시간**: 0분 (완전 자동)
- **컨텍스트 로드**: < 1000 tokens
- **세션 연속성**: 100% 유지
- **배포 성공률**: push까지 완료 100%

---
*이 문서는 PROJECT_NAME의 헌법입니다. 수동으로만 수정하세요.*
EOF
    sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" project_rules.md
    echo "  ✅ Created project_rules.md"
else
    echo "  ⏭️  project_rules.md already exists"
fi

# Step 4: Initialize ZEDS structure
echo ""
echo "📚 Step 4/5: Initializing ZEDS (Zero-Effort Documentation System)..."

# Create initial status.md
if [ ! -f "docs/CURRENT/status.md" ]; then
    cat > docs/CURRENT/status.md << EOF
# Current Project Status

## 📅 Last Updated: $CURRENT_DATE

## 🎯 Current Phase: Initial Setup
- Project initialized with claude-dev-kit
- Ready to start development

## ✅ Recently Completed
- Project structure created
- Slash commands installed
- ZEDS initialized

## 🔄 Active Work
- Waiting for first development task

## 📋 Next Steps
- Use /기획 to plan your first feature
- Or use /전체사이클 for complete workflow

## 💡 Notes
- All slash commands are ready to use
- Documentation will be automatic
EOF
    echo "  ✅ Created docs/CURRENT/status.md"
else
    echo "  ⏭️  status.md already exists"
fi

# Create initial active-todos.md
if [ ! -f "docs/CURRENT/active-todos.md" ]; then
    cat > docs/CURRENT/active-todos.md << EOF
# Active TODOs

## 🚀 Current Sprint
- [ ] Start first development task

## 📝 Backlog
- [ ] Define project requirements
- [ ] Set up development environment

## 💭 Ideas
- Add your project ideas here
EOF
    echo "  ✅ Created docs/CURRENT/active-todos.md"
else
    echo "  ⏭️  active-todos.md already exists"
fi

# Step 5: Set up Git hooks (if git repo exists)
echo ""
echo "🔗 Step 5/5: Setting up Git hooks..."
if [ -d ".git" ]; then
    # Create pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Auto-update claude.md on commit
if command -v claude >/dev/null 2>&1; then
    claude init --silent 2>/dev/null || true
    git add claude.md 2>/dev/null || true
fi
EOF
    chmod +x .git/hooks/pre-commit
    echo "  ✅ Git pre-commit hook installed"
else
    echo "  ⏭️  Not a git repository (hooks skipped)"
fi

# Create CLAUDE.md if missing
if [ ! -f "CLAUDE.md" ]; then
    echo ""
    echo "📝 Creating CLAUDE.md..."
    cat > CLAUDE.md << EOF
# $PROJECT_NAME: $PROJECT_DESC

## Project Overview
$PROJECT_DESC

## Current Status
- ✅ **Phase 1**: Project initialized with claude-dev-kit
- 📋 **Next**: Start development with /기획 or /전체사이클

## Development Environment Setup

### Prerequisites
- Claude Code CLI installed
- Python 3.8+ (with uv package manager recommended)
- Git

### Quick Start
\`\`\`bash
# Project already initialized!
# Start developing with slash commands:
# Use /기획 to plan features
# Use /구현 to implement
# Use /안정화 to test and optimize
# Use /배포 to deploy

# Or use workflow commands:
# /전체사이클 - Complete development cycle
# /개발완료 - Implementation to deployment
# /품질보증 - Testing and deployment
# /기획구현 - Planning and implementation
\`\`\`

## Key Commands

### Slash Commands Available
- **/기획** - Structured discovery and planning
- **/구현** - Implementation with DRY principles
- **/안정화** - Comprehensive validation and testing
- **/배포** - Deployment with push and tagging
- **/전체사이클** - Complete workflow (기획→구현→안정화→배포)
- **/개발완료** - From implementation to deployment
- **/품질보증** - Testing and deployment
- **/기획구현** - Planning and implementation

## Project Structure
\`\`\`
$PROJECT_NAME/
├── CLAUDE.md            # This file
├── project_rules.md     # Project constitution
├── .claude/
│   └── commands/        # 8 slash commands installed
├── src/$PROJECT_NAME/   # Main source code
│   ├── core/           # Core functionality
│   ├── models/         # Data models
│   └── services/       # Business logic
├── docs/
│   ├── CURRENT/        # Active session docs
│   └── development/    # Development history
├── tests/              # Test suites
└── scripts/            # Utility scripts
\`\`\`

## Development Workflow

이 프로젝트는 4단계 키워드 기반 개발을 사용합니다:
- **"기획"** → Structured Discovery & Planning Loop
- **"구현"** → Implementation with DRY
- **"안정화"** → Structural Sustainability Protocol v2.0
- **"배포"** → Deployment with push and tagging

## Contributing Guidelines

### Code Style
- Follow existing patterns in the codebase
- Use type hints in Python
- Write tests for new features

### Documentation
- Automatic via ZEDS (Zero-Effort Documentation System)
- Just use slash commands, documentation happens automatically

---
*Generated with claude-dev-kit v3.0*
EOF
    echo "  ✅ Created CLAUDE.md"
else
    echo "  ⏭️  CLAUDE.md already exists"
fi

# Create .claudeignore if missing
if [ ! -f ".claudeignore" ]; then
    cat > .claudeignore << 'EOF'
# Build artifacts
dist/
build/
*.egg-info/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Dependencies
node_modules/
.venv/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local
.env.*.local

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Documentation builds
docs/_build/
docs/.doctrees/

# Temporary
*.tmp
*.bak
*.backup
tmp/
temp/
EOF
    echo "  ✅ Created .claudeignore"
fi

# Summary
echo ""
echo "=========================================="
echo "🎉 Claude Dev Kit Installation Complete!"
echo "=========================================="
echo ""
echo "✅ Installed Components:"
echo "  • Project structure created"
echo "  • 8 slash commands installed"
echo "  • project_rules.md created"
echo "  • ZEDS initialized"
if [ -d ".git" ]; then
    echo "  • Git hooks configured"
fi
echo ""
echo "📚 Available Slash Commands:"
echo "  Individual: /기획, /구현, /안정화, /배포"
echo "  Workflows: /전체사이클, /개발완료, /품질보증, /기획구현"
echo ""
echo "🚀 Next Steps:"
echo "  1. Open Claude Code in this directory"
echo "  2. Use /기획 to plan your first feature"
echo "  3. Or use /전체사이클 for complete workflow"
echo ""
echo "💡 Tips:"
echo "  • project_rules.md is your project constitution"
echo "  • Documentation happens automatically via ZEDS"
echo "  • Always use slash commands for consistency"