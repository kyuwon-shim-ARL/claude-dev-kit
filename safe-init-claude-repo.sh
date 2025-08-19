#!/bin/bash
# [DEPRECATED] Safe Claude Code Repository Initialization Script
# ⚠️  DEPRECATED: Use init.sh instead - it includes all safety features
# This script is kept for backward compatibility only
# Preserves existing files and structure

set -e

PROJECT_NAME=${1:-"my_project"}
PROJECT_DESC=${2:-"A new Claude Code project"}
CURRENT_DATE=$(date +%Y-%m-%d)

echo "⚠️  WARNING: This script is DEPRECATED!"
echo "Please use ./init.sh instead - it has all the same safety features plus more."
echo ""
read -p "Do you want to use the new init.sh instead? [Y/n]: " use_new
case $use_new in
    [Nn]* )
        echo "Continuing with deprecated script..."
        ;;
    * )
        echo "🚀 Switching to init.sh..."
        exec bash "$(dirname "$0")/init.sh" "$PROJECT_NAME" "$PROJECT_DESC"
        ;;
esac

echo "🚀 Safely initializing Claude Code structure for: $PROJECT_NAME"
echo "=" 
echo ""

# Check for existing files
if [ -f "CLAUDE.md" ]; then
    echo "⚠️  CLAUDE.md already exists"
    read -p "Do you want to: [B]ackup and update, [S]kip, or [M]erge? (B/S/M): " choice
    case $choice in
        [Bb]* )
            cp CLAUDE.md "CLAUDE.md.backup.$CURRENT_DATE"
            echo "✅ Backed up to CLAUDE.md.backup.$CURRENT_DATE"
            # Update only missing sections
            ;;
        [Ss]* )
            echo "⏭️  Skipping CLAUDE.md update"
            SKIP_CLAUDE=true
            ;;
        [Mm]* )
            echo "📝 Will merge with existing CLAUDE.md"
            MERGE_CLAUDE=true
            ;;
        * )
            echo "❌ Invalid choice. Exiting."
            exit 1
            ;;
    esac
fi

# Create only missing directories
echo "📁 Creating missing directories..."
for dir in "src/$PROJECT_NAME" "src/$PROJECT_NAME/core" "src/$PROJECT_NAME/models" \
           "src/$PROJECT_NAME/services" "core_features" "docs/CURRENT" \
           "docs/development/conversations" "docs/development/guides" \
           "docs/development/templates" "docs/specs" "examples" "tests" \
           "tools" "scripts" "archive"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "  ✅ Created: $dir"
    else
        echo "  ⏭️  Exists: $dir"
    fi
done

# Merge or append to CLAUDE.md if requested
if [ "$MERGE_CLAUDE" = true ] && [ -f "CLAUDE.md" ]; then
    echo ""
    echo "📝 Adding Claude Code workflow section to existing CLAUDE.md..."
    
    # Check if workflow section already exists
    if ! grep -q "## Development Workflow" CLAUDE.md; then
        cat >> CLAUDE.md << 'EOF'

## Development Workflow (Claude Code)

### Keyword Commands
- **"기획"** → Structured Discovery & Planning Loop:
  - 탐색: 전체 구조 파악, As-Is/To-Be/Gap 분석
  - 계획: MECE 기반 작업분해, 우선순위 설정
  - 수렴: 탐색↔계획 반복 until PRD 완성
- **"구현"** → Implementation with DRY:
  - 기존 코드 검색 → 재사용 → 없으면 생성
  - TodoWrite 기반 체계적 진행
  - 단위 테스트 & 기본 검증
- **"안정화"** → Comprehensive Validation Loop:
  - 일관성: 키워드/문서/코드 동기화 검증
  - MECE: 구조적 완전성 분석
  - 리팩토링: 문제→수정→재검증 (ZERO 이슈까지)
- **"배포"** → Deployment: 최종검증 + 구조화커밋 + 푸시 + 태깅

### Project Structure Guidelines
Keep root clean with only essential files.
See `docs/development/guides/` for detailed workflows.
EOF
        echo "  ✅ Added workflow section to CLAUDE.md"
    else
        echo "  ⏭️  Workflow section already exists"
    fi
fi

# Create .gitignore only if missing
if [ ! -f ".gitignore" ]; then
    echo "🚫 Creating .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
.venv/
*.log
.DS_Store
EOF
    echo "  ✅ Created .gitignore"
else
    echo "  ⏭️  .gitignore already exists"
fi

# Check if init-complete.sh exists and offer to run it
if [ -f "$(dirname "$0")/init-complete.sh" ]; then
    echo ""
    echo "🔔 Complete installation available!"
    read -p "Do you want to run the complete installation? (includes slash commands, ZEDS, etc.) [Y/n]: " complete_choice
    case $complete_choice in
        [Nn]* )
            echo "⏭️  Skipping complete installation"
            ;;
        * )
            echo "🚀 Running complete installation..."
            bash "$(dirname "$0")/init-complete.sh" "$PROJECT_NAME" "$PROJECT_DESC"
            exit 0
            ;;
    esac
fi

# Summary
echo ""
echo "🎉 Safe initialization complete!"
echo ""
echo "📋 Summary:"
echo "  - Preserved existing files"
echo "  - Created missing directories"
echo "  - Ready for Claude Code workflows"
echo ""
echo "🔧 Next steps:"
echo "  1. Run ./init-complete.sh for full installation (slash commands, ZEDS, etc.)"
echo "  2. Or manually run install.sh for slash commands only"
echo "  3. Review CLAUDE.md for any needed updates"