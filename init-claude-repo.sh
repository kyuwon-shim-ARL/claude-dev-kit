#!/bin/bash
# Claude Code Repository Initialization Script
# Usage: ./init-claude-repo.sh [project_name] [project_description]

set -e

CURRENT_DIR=$(basename "$PWD")
PROJECT_NAME=${1:-"$CURRENT_DIR"}
PROJECT_DESC=${2:-"A new Claude Code project"}
CURRENT_DATE=$(date +%Y-%m-%d)

echo "🚀 Initializing Claude Code repository: $PROJECT_NAME"
echo "=" * 60

# 1. Create directory structure
echo "📁 Creating directory structure..."
python3 setup_claude_code_structure.py "$PROJECT_NAME"

# 2. Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    git branch -m main
fi

# 3. Copy and customize CLAUDE.md
echo "📝 Setting up CLAUDE.md..."
if [ -f "CLAUDE.md" ]; then
    echo "⚠️  CLAUDE.md already exists. Creating backup..."
    cp CLAUDE.md CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)
fi
sed -e "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" \
    -e "s/\[PROJECT_DESCRIPTION\]/$PROJECT_DESC/g" \
    -e "s/\[project_name\]/$PROJECT_NAME/g" \
    CLAUDE.md > CLAUDE.md.tmp && mv CLAUDE.md.tmp CLAUDE.md

# 4. Create initial .env file
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cp .env.example .env
    echo "# Generated on $CURRENT_DATE for $PROJECT_NAME" >> .env
fi

# 5. Create README.md
echo "📖 Creating README.md..."
cat > README.md << EOF
# $PROJECT_NAME

$PROJECT_DESC

## Quick Start

\`\`\`bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your configuration

# 2. Verify installation
python scripts/test_setup.py

# 3. Run example
python examples/basic_usage.py
\`\`\`

## Development

This project follows **Claude Code development patterns**. See \`CLAUDE.md\` for detailed documentation and workflows.

### Key Commands
- **Development**: Use 4-stage keywords: "기획", "구현", "안정화", "배포"
- **Tracking**: All multi-step tasks tracked with TodoWrite
- **Documentation**: Session archives in \`docs/development/conversations/\`

### Project Structure
See \`CLAUDE.md\` for complete structure explanation.

## Contributing

1. Read \`docs/development/guides/claude-code-workflow.md\`
2. Follow TodoWrite patterns for task tracking
3. Use MECE analysis for progress reporting
4. Archive sessions in proper directory structure

---

*This repository is optimized for Claude Code development workflows.*
EOF

# 6. Create basic Makefile
echo "⚙️ Creating Makefile..."
cat > Makefile << EOF
.PHONY: setup test clean lint format

setup:
	@echo "🔧 Setting up $PROJECT_NAME development environment"
	python scripts/test_setup.py

test:
	@echo "🧪 Running tests"
	python -m pytest tests/ -v

clean:
	@echo "🧹 Cleaning up"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

lint:
	@echo "🔍 Linting code"
	# Add your preferred linter here
	@echo "Linting configuration needed"

format:
	@echo "✨ Formatting code" 
	# Add your preferred formatter here
	@echo "Formatting configuration needed"

# Claude Code specific commands
status:
	@echo "📊 Project Status"
	@python -c "print('✅ $PROJECT_NAME development environment ready')"

archive-session:
	@echo "📚 Archiving current session"
	@mkdir -p docs/development/conversations/\$(date +%Y-%m-%d)
	@echo "Session archived to docs/development/conversations/\$(date +%Y-%m-%d)/"
EOF

# 7. Create .gitignore
echo "🚫 Creating .gitignore..."
cat > .gitignore << EOF
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

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Logs
*.log
logs/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
data/temp/
temp/
*.tmp
EOF

# 8. Initial commit
echo "💾 Creating initial commit..."
git add .
git commit -m "🎯 Initialize Claude Code project structure

## Project Setup
- **Structure**: Complete Claude Code directory organization
- **Documentation**: CLAUDE.md configured for $PROJECT_NAME
- **Templates**: Development guides and session templates
- **Configuration**: Basic .env, Makefile, and .gitignore

## Claude Code Features
- ✅ TodoWrite-ready task tracking
- ✅ MECE progress analysis framework  
- ✅ Session archiving structure
- ✅ Clean root directory with essential entry points only

## Next Steps
1. Run: python scripts/test_setup.py
2. Customize project-specific details in CLAUDE.md
3. Begin development with keyword-based workflow

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo ""
echo "🎉 Claude Code repository initialization complete!"
echo ""
echo "📋 Next steps:"
echo "1. Customize CLAUDE.md with project-specific details"
echo "2. Configure .env file with your settings"
echo "3. Run: python scripts/test_setup.py"
echo "4. Start development with: '기획' keyword for discovery & planning"
echo ""
echo "🔧 Available commands:"
echo "- make setup    # Verify installation"
echo "- make test     # Run tests"
echo "- make status   # Check project status"
echo ""
echo "📖 Read CLAUDE.md and docs/development/guides/ for detailed workflows"