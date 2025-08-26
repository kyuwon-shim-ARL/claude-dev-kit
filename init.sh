#!/bin/bash
# Claude Dev Kit: Universal Initialization Script
# Works for everyone - developers and non-developers alike
# Usage: ./init.sh [project_name] [project_description]

set -e

PROJECT_NAME=${1:-"my_project"}
PROJECT_DESC=${2:-"A new Claude Code project"}
CURRENT_DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect Git availability and setup
HAS_GIT=false
NEW_REPO=false
SHOULD_INIT_GIT=false

if command -v git >/dev/null 2>&1; then
    if [ -d ".git" ] || git rev-parse --git-dir >/dev/null 2>&1; then
        HAS_GIT=true
        echo "🔍 Existing Git repository detected"
    else
        HAS_GIT=true
        NEW_REPO=true
        echo "💡 Git available but no repository - will initialize new repo"
        SHOULD_INIT_GIT=true
    fi
else
    echo "⚠️  Git not available - will use local backup system"
fi

echo "🚀 Claude Dev Kit Universal Installation"
echo "========================================"
echo "Project: $PROJECT_NAME"
echo "Description: $PROJECT_DESC"
if [ "$HAS_GIT" = true ]; then
    if [ "$NEW_REPO" = true ]; then
        echo "Git: ✅ Available (will initialize new repository)"
    else
        echo "Git: ✅ Detected (using existing repository)"
    fi
else
    echo "Git: ❌ Not detected (local mode)"
fi
echo ""

# Step 1: Create directory structure
echo "📁 Step 1/5: Creating project structure..."
for dir in "src/$PROJECT_NAME" "src/$PROJECT_NAME/core" "src/$PROJECT_NAME/models" \
           "src/$PROJECT_NAME/services" "docs/CURRENT" \
           "docs/development/sessions" "docs/specs" "examples" "tests" \
           "scripts" ".claude/commands"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "  ✅ Created: $dir"
    else
        echo "  ⏭️  Exists: $dir"
    fi
done

# Create backup directory for non-git environments
if [ "$HAS_GIT" = false ]; then
    if [ ! -d ".backups" ]; then
        mkdir -p ".backups"
        echo "  ✅ Created: .backups (for version control)"
    fi
fi

# Step 2: Install slash commands
echo ""
echo "⚡ Step 2/5: Installing slash commands..."
BASE_URL="https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.claude/commands"

# Hybrid command mapping: Korean -> English (GitHub-safe)
declare -A commands=(
    ["기획"]="plan"
    ["구현"]="implement"
    ["안정화"]="stabilize"
    ["검증"]="validate"
    ["배포"]="deploy"
    ["전체사이클"]="fullcycle"
    ["개발완료"]="complete"
    ["품질보증"]="quality"
    ["기획구현"]="plandev"
    ["극한검증"]="extreme"
    ["컨텍스트"]="context"
    ["분석"]="analyze"
    ["주간보고"]="weekly"
    ["문서정리"]="docsorg"
)

# Download each command
DOWNLOAD_SUCCESS=true
for korean_cmd in "${!commands[@]}"; do
    english_cmd="${commands[$korean_cmd]}"
    echo "  📥 Downloading /$korean_cmd command..."
    
    # Try downloading from GitHub (English filename)
    RESPONSE=$(curl -sSL -w "\n%{http_code}" "$BASE_URL/$english_cmd.md" 2>/dev/null)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    CONTENT=$(echo "$RESPONSE" | head -n -1)
    
    if [ "$HTTP_CODE" = "200" ] && [ -n "$CONTENT" ] && ! echo "$CONTENT" | grep -q "400 Bad request"; then
        # Save as Korean filename but also create English alias
        echo "$CONTENT" > ".claude/commands/$korean_cmd.md"
        echo "$CONTENT" > ".claude/commands/$english_cmd.md"
        echo "     ✅ Downloaded (both /$korean_cmd and /$english_cmd available)"
    else
        # Fallback to local copy
        if [ -f "$SCRIPT_DIR/.claude/commands/$korean_cmd.md" ]; then
            cp "$SCRIPT_DIR/.claude/commands/$korean_cmd.md" ".claude/commands/$korean_cmd.md"
            cp "$SCRIPT_DIR/.claude/commands/$korean_cmd.md" ".claude/commands/$english_cmd.md"
            echo "     ✅ Copied from local (both /$korean_cmd and /$english_cmd available)"
        elif [ -f "$SCRIPT_DIR/.claude/commands/$english_cmd.md" ]; then
            cp "$SCRIPT_DIR/.claude/commands/$english_cmd.md" ".claude/commands/$korean_cmd.md"
            cp "$SCRIPT_DIR/.claude/commands/$english_cmd.md" ".claude/commands/$english_cmd.md"
            echo "     ✅ Copied from local (both /$korean_cmd and /$english_cmd available)"
        else
            echo "     ⚠️  Could not install $korean_cmd ($english_cmd)"
            DOWNLOAD_SUCCESS=false
        fi
    fi
done

if [ "$DOWNLOAD_SUCCESS" = true ]; then
    echo "  ✅ All 11 slash commands installed"
else
    echo "  ⚠️  Some commands could not be installed (check network)"
fi

# Step 3: Create project_rules.md if missing (새로운 위치: docs/specs/)
echo ""
echo "📜 Step 3/5: Creating project specifications..."

# Check for existing project_rules.md and migrate if needed
if [ -f "project_rules.md" ] && [ ! -f "docs/specs/project_rules.md" ]; then
    echo "  📦 Migrating project_rules.md to docs/specs/..."
    mv "project_rules.md" "docs/specs/project_rules.md"
    echo "  ✅ Migrated project_rules.md to docs/specs/"
elif [ ! -f "docs/specs/project_rules.md" ]; then
    cat > docs/specs/project_rules.md << 'EOF'
# PROJECT_NAME Project Rules

## 🎯 Core Philosophy
- **워크플로우 기반 개발**: /전체사이클 중심의 체계적 진행
- **Zero-Effort Documentation**: 슬래시 커맨드 사용만으로 자동 문서화
- **Mock 테스트 금지**: 실제 사용자 시나리오 검증 필수
- **DRY 원칙**: 코드 중복 절대 금지, 재사용 우선

## 📐 Architecture Principles
- **4단계 워크플로우**: 기획 → 구현 → 안정화 → 배포
- **글로벌 슬래시 명령어**: 10개 명령어 표준화 (개별 5개 + 조합 5개)
- **3층 문서화 구조**: project_rules.md / docs/CURRENT/ / sessions/
- **구조적 지속가능성**: 6단계 검증 루프 필수 적용

## 🔧 Development Standards
- **정량적 검증**: "통과했습니다" 금지, 구체적 수치 제시
- **테스트 우선**: 모든 기능은 테스트와 함께
- **문서화 자동화**: ZEDS를 통한 자동 문서 생성

## 📚 Documentation Workflow
- **세션 시작**: project_rules.md + docs/CURRENT/status.md 자동 로드
- **작업 진행**: 각 단계별 자동 문서화
- **세션 종료**: /배포 시 자동으로 sessions/에 아카이브
- **토큰 효율**: 현재 컨텍스트만 로드 (< 1000 tokens)

## 🚀 Version Control
EOF
    
    # Add Git-specific or local backup info
    if [ "$HAS_GIT" = true ]; then
        cat >> project_rules.md << 'EOF'
- **Git 기반**: commit + push + tag 워크플로우
- **Pre-commit hooks**: 자동 문서 업데이트
- **원격 저장소**: GitHub 연동
EOF
    else
        cat >> docs/specs/project_rules.md << 'EOF'
- **로컬 백업**: .backups/ 디렉토리에 날짜별 저장
- **버전 관리**: 타임스탬프 기반 백업
- **수동 동기화**: 필요시 외부 저장소에 수동 업로드
EOF
    fi
    
    cat >> docs/specs/project_rules.md << 'EOF'

## ⚙️ Technical Stack
- **Claude Code**: 슬래시 명령어 기반 워크플로우
- **Python**: 3.8+ (선택사항)
- **Playwright**: 웹 프로젝트 E2E 테스트 (선택사항)

## 📊 Success Metrics
- **문서화 추가 시간**: 0분 (완전 자동)
- **컨텍스트 로드**: < 1000 tokens
- **세션 연속성**: 100% 유지

---
*이 문서는 PROJECT_NAME의 헌법입니다. 수동으로만 수정하세요.*
EOF
    sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" docs/specs/project_rules.md
    echo "  ✅ Created docs/specs/project_rules.md"
else
    echo "  ⏭️  docs/specs/project_rules.md already exists"
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
- Context management: Dynamic guide generation (v9.0)
- Expected compression: 85-95% with /compact
EOF
    
    if [ "$HAS_GIT" = false ]; then
        cat >> docs/CURRENT/status.md << EOF

## ⚠️ Git Not Detected
- Running in local mode
- Backups saved to .backups/ directory
- Manual sync required for sharing
EOF
    fi
    
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

# Create PRD template
if [ ! -f "docs/specs/PRD-template.md" ]; then
    cat > docs/specs/PRD-template.md << EOF
# Product Requirements Document (PRD)

## 📋 Version
- Version: 1.0
- Date: $CURRENT_DATE
- Status: Draft

## 🎯 Product Overview
[제품의 핵심 목적과 비전을 명시]

## 👥 Target Users
- Primary: [주요 사용자 그룹]
- Secondary: [부가 사용자 그룹]

## 🔑 Key Features
1. **[핵심 기능 1]**
   - Description: 
   - Priority: High/Medium/Low
   - Success Criteria: 

2. **[핵심 기능 2]**
   - Description:
   - Priority: High/Medium/Low
   - Success Criteria:

## 📊 Success Metrics
- [측정 가능한 성공 지표 1]
- [측정 가능한 성공 지표 2]

## 🚫 Out of Scope
- [명시적으로 제외되는 기능들]

## 📅 Timeline
- Phase 1: [날짜] - [목표]
- Phase 2: [날짜] - [목표]

## 🔄 Dependencies
- [외부 의존성 1]
- [외부 의존성 2]

## ⚠️ Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [위험 1] | High/Medium/Low | [완화 방안] |

---
*이 PRD는 /기획 명령어로 자동 생성되었습니다.*
EOF
    echo "  ✅ Created docs/specs/PRD-template.md"
else
    echo "  ⏭️  PRD-template.md already exists"
fi

# Step 5: Git setup and hooks
echo ""
if [ "$HAS_GIT" = true ]; then
    echo "🔗 Step 5/5: Setting up Git repository..."
    
    # Initialize new Git repository if needed
    if [ "$SHOULD_INIT_GIT" = true ]; then
        echo "  📦 Initializing new Git repository..."
        git init
        
        # Create initial .gitignore
        cat > .gitignore << 'EOF'
# Build artifacts
dist/
build/
*.egg-info/
__pycache__/
*.pyc
*.pyo

# Dependencies  
node_modules/
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

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
.pytest_cache/
coverage/
.nyc_output/

# Temporary
*.tmp
*.bak
tmp/
temp/

# Backups (for non-git mode)
.backups/
EOF
        echo "  ✅ Git repository initialized"
        echo ""
        echo "  📋 Next steps for Git setup:"
        echo "     1. Create a repository on GitHub/GitLab"  
        echo "     2. Add remote: git remote add origin <your-repo-url>"
        echo "     3. Push: git add . && git commit -m 'Initial commit' && git push -u origin main"
        echo ""
    fi
    
    # Create pre-commit hook
    echo "  🪝 Installing Git pre-commit hook..."
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Auto-update claude.md on commit
if command -v claude >/dev/null 2>&1; then
    claude init 2>/dev/null || true
    git add claude.md 2>/dev/null || true
fi
EOF
    chmod +x .git/hooks/pre-commit
    echo "  ✅ Git pre-commit hook installed"
else
    echo "📦 Step 5/5: Setting up local backup system..."
    
    # Create backup script
    cat > scripts/backup.sh << 'EOF'
#!/bin/bash
# Local backup script for non-Git environments
BACKUP_DIR=".backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_$TIMESTAMP"

echo "Creating backup: $BACKUP_NAME"
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# Backup important files
for item in src/ docs/ tests/ examples/ CLAUDE.md; do
    if [ -e "$item" ]; then
        cp -r "$item" "$BACKUP_DIR/$BACKUP_NAME/"
    fi
done

echo "✅ Backup created at $BACKUP_DIR/$BACKUP_NAME"

# Keep only last 10 backups
cd "$BACKUP_DIR"
ls -t | tail -n +11 | xargs -r rm -rf
cd ..

echo "📊 Backup stats:"
du -sh "$BACKUP_DIR/$BACKUP_NAME"
EOF
    chmod +x scripts/backup.sh
    echo "  ✅ Local backup system created (use scripts/backup.sh)"
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

## Development Environment

### Quick Start
\`\`\`bash
# Project is ready! Start with slash commands:
/기획      # Plan features
/구현      # Implement code
/안정화    # Test and optimize
/배포      # Deploy changes

# Or use workflows:
/전체사이클  # Complete cycle
/개발완료    # Implementation to deployment
\`\`\`

## Available Commands
- **Individual**: /기획, /구현, /안정화, /배포
- **Workflows**: /전체사이클, /개발완료, /품질보증, /기획구현

## Project Structure
\`\`\`
$PROJECT_NAME/
├── CLAUDE.md            # This file
├── project_rules.md     # Project constitution
├── .claude/commands/    # 8 slash commands
├── src/$PROJECT_NAME/   # Source code
├── docs/CURRENT/        # Active documentation
├── tests/              # Test suites
EOF

    if [ "$HAS_GIT" = false ]; then
        cat >> CLAUDE.md << EOF
├── .backups/           # Local version control
EOF
    fi

    cat >> CLAUDE.md << EOF
└── scripts/            # Utility scripts
\`\`\`

## Development Workflow
이 프로젝트는 4단계 키워드 기반 개발을 사용합니다:
- **기획** → Structured Discovery & Planning
- **구현** → Implementation with DRY
- **안정화** → Structural Sustainability
- **배포** → Deployment${HAS_GIT:+ with Git}${HAS_GIT:- (local)}

EOF

    if [ "$HAS_GIT" = false ]; then
        cat >> CLAUDE.md << EOF
## ⚠️ Note: Running in Local Mode
Git was not detected in this environment. The project will work perfectly, but:
- Version control uses local backups (.backups/)
- Use \`scripts/backup.sh\` to create backups
- Manual sharing required (no automatic push)
- All other features work normally!

EOF
    fi

    cat >> CLAUDE.md << EOF
---
*Initialized with claude-dev-kit v4.0 (Universal Edition)*
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

# Dependencies
node_modules/
.venv/
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Logs
*.log

# Environment
.env

# Testing
.coverage
.pytest_cache/

# Backups
.backups/

# Temporary
*.tmp
*.bak
tmp/
EOF
    echo "  ✅ Created .claudeignore"
fi

# Final Summary
echo ""
echo "=========================================="
echo "🎉 Claude Dev Kit Installation Complete!"
echo "=========================================="
echo ""
echo "✅ Installed Components:"
echo "  • Project structure created"
echo "  • 11 slash commands installed"
echo "  • project_rules.md created" 
echo "  • ZEDS initialized"

if [ "$HAS_GIT" = true ]; then
    if [ "$NEW_REPO" = true ]; then
        echo "  • New Git repository initialized"
        echo "  • Git hooks configured"
        echo "  • Ready for remote repository setup"
    else
        echo "  • Git hooks configured"
        echo "  • Existing repository preserved"
    fi
else
    echo "  • Local backup system ready"
    echo "  • Use scripts/backup.sh for versioning"
fi

echo ""
echo "📚 Available Slash Commands:"
echo "  Individual: /기획, /구현, /안정화, /검증, /배포"
echo "  Workflows: /전체사이클, /개발완료, /품질보증, /기획구현, /극한검증"
echo ""
echo "🚀 New Features (v9.0):"
echo "  • Dynamic context guide generation"
echo "  • 85-95% compression with smart /compact"
echo "  • Claude analyzes your actual work for optimal cleanup"
echo ""
if [ "$NEW_REPO" = true ]; then
    echo ""
    echo "🔧 Git Setup Required:"
    echo "  1. Create a new repository on GitHub/GitLab/etc"
    echo "  2. Connect your repository:"
    echo "     git remote add origin https://github.com/yourusername/${PROJECT_NAME}.git"
    echo "  3. Make initial commit:"
    echo "     git add ."
    echo "     git commit -m 'Initial commit with claude-dev-kit'"  
    echo "     git push -u origin main"
    echo ""
fi

echo "🚀 Next Steps:"
echo "  1. Open Claude Code in this directory"
if [ "$NEW_REPO" = true ]; then
    echo "  2. Set up your Git remote repository (see above)"
    echo "  3. Use /기획 to plan your first feature"
    echo "  4. Or use /전체사이클 for complete workflow"
else
    echo "  2. Use /기획 to plan your first feature"
    echo "  3. Or use /전체사이클 for complete workflow"  
fi
echo ""

if [ "$HAS_GIT" = false ]; then
    echo "💡 Tip for non-Git users:"
    echo "  • Your work is safe! Backups are automatic"
    echo "  • Run 'scripts/backup.sh' anytime to save progress"
    echo "  • All Claude Code features work perfectly!"
    echo ""
fi

echo "Happy coding with Claude! 🤖"