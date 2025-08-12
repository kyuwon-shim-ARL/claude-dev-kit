#!/bin/bash
# Safe Claude Code Repository Initialization Script
# Preserves existing files and structure

set -e

PROJECT_NAME=${1:-"my_project"}
PROJECT_DESC=${2:-"A new Claude Code project"}
CURRENT_DATE=$(date +%Y-%m-%d)

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
- **"분석"** → Analyze current state + requirements planning
- **"시작"** → Create TodoWrite plan, begin implementation
- **"정리"** → Refactor, organize files
- **"검증"** → Test and validate
- **"커밋"** → Create meaningful commits

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
echo "  1. Review CLAUDE.md for any needed updates"
echo "  2. Start with: '현재 상태 분석해줘'"
echo "  3. Use keywords: 분석, 시작, 정리, 검증, 커밋"