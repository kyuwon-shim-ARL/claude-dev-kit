#!/bin/bash
# Claude Dev Kit: Ultimate Unified Installer v29.0
# One script to rule them all - Complete project setup with TADD enforcement
# Usage: ./init.sh [PROJECT_NAME] [DESCRIPTION] or ./init.sh [--option]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables
PROJECT_NAME=""
PROJECT_DESC=""
MODE=""
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURRENT_DATE=$(date +%Y-%m-%d)

# Environment detection variables
HAS_GIT=false
IS_GIT_REPO=false
NEW_REPO=false
GITHUB_REMOTE=""
HAS_GITHUB_CLI=false
GITHUB_SETUP_AVAILABLE=false
HAS_PYTHON=false

# Show usage information
show_usage() {
    echo -e "${BLUE}🚀 Claude Dev Kit Ultimate Unified Installer v29.0${NC}"
    echo ""
    echo "Usage:"
    echo -e "  ${GREEN}$0 PROJECT_NAME [DESCRIPTION]${NC}     # Create new project with full setup"
    echo -e "  ${GREEN}$0 --upgrade${NC}                      # Upgrade existing project"
    echo -e "  ${GREEN}$0 --tadd-only${NC}                   # Install TADD Enforcement only"
    echo -e "  ${GREEN}$0 --reinstall${NC}                   # Complete reinstallation"
    echo -e "  ${GREEN}$0 --check${NC}                       # Check installation status"
    echo -e "  ${GREEN}$0 --github-setup${NC}               # Setup GitHub integration"
    echo ""
    echo "Options:"
    echo "  --force         # Skip confirmations"
    echo "  --no-github     # Skip GitHub integration"
    echo "  --offline       # Use local files only"
    echo ""
    echo "Examples:"
    echo -e "  ${CYAN}$0 my_project \"My awesome AI project\"${NC}"
    echo -e "  ${CYAN}$0 --upgrade${NC}"
    echo -e "  ${CYAN}curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh | bash -s \"project\" \"desc\"${NC}"
    echo ""
}

# Detect environment capabilities
detect_environment() {
    echo -e "${YELLOW}🔍 Detecting environment...${NC}"
    
    # Git detection
    if command -v git >/dev/null 2>&1; then
        HAS_GIT=true
        if [ -d ".git" ] || git rev-parse --git-dir >/dev/null 2>&1; then
            IS_GIT_REPO=true
        else
            NEW_REPO=true
        fi
    fi
    
    # GitHub integration detection
    if [ "$HAS_GIT" = true ]; then
        GITHUB_REMOTE=$(git remote -v 2>/dev/null | grep github.com | head -1 | cut -f2 | cut -d' ' -f1 || echo "")
        
        if command -v gh >/dev/null 2>&1; then
            HAS_GITHUB_CLI=true
            if gh auth status >/dev/null 2>&1; then
                GITHUB_SETUP_AVAILABLE=true
            fi
        fi
    fi
    
    # Python detection
    if command -v python3 >/dev/null 2>&1; then
        HAS_PYTHON=true
    fi
    
    echo -e "   Git: ${HAS_GIT} | Repo: ${IS_GIT_REPO} | GitHub CLI: ${HAS_GITHUB_CLI} | GitHub Auth: ${GITHUB_SETUP_AVAILABLE} | Python: ${HAS_PYTHON}"
}

# Show progress with visual progress bar
show_progress() {
    local current=$1
    local total=$2
    local description=$3
    
    local progress=$((current * 50 / total))
    local percent=$((current * 100 / total))
    
    echo -ne "\r${BLUE}🚀 Progress: [$current/$total] $description${NC}"
    printf "\n["
    for ((i=0; i<progress; i++)); do printf "="; done
    for ((i=progress; i<50; i++)); do printf " "; done
    printf "] %d%%\n" $percent
}

# Create project directory structure
install_project_structure() {
    echo -e "${YELLOW}📁 Creating project structure...${NC}"
    
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
}

# Install slash commands
install_slash_commands() {
    echo -e "${YELLOW}⚡ Installing slash commands...${NC}"
    
    BASE_URL="https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.claude/commands"
    
    # Command mapping (Korean -> English for GitHub)
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
        ["주간보고"]="주간보고"
        ["문서정리"]="docsorg"
        ["레포정리"]="repoclean"
        ["세션마감"]="세션마감"
        ["실험시작"]="실험시작"
        ["실험완료"]="실험완료"
        ["보고서작업"]="보고서작업"
        ["TADD강화"]="TADD강화"
    )
    
    local success_count=0
    local total_commands=${#commands[@]}
    
    for korean_cmd in "${!commands[@]}"; do
        echo "  📥 Downloading /$korean_cmd command..."
        
        # URL encode Korean filename for GitHub Raw access
        encoded_filename=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$korean_cmd.md'))" 2>/dev/null)
        
        if [ -n "$encoded_filename" ]; then
            # Try URL-encoded download first (GitHub Raw)
            if curl -sSL "$BASE_URL/$encoded_filename" -o ".claude/commands/$korean_cmd.md" 2>/dev/null && 
               [ -s ".claude/commands/$korean_cmd.md" ] && 
               ! grep -q "html" ".claude/commands/$korean_cmd.md"; then
                success_count=$((success_count + 1))
                echo "    ✅ $korean_cmd.md ($(stat -c%s ".claude/commands/$korean_cmd.md") bytes)"
            else
                # Fallback to English mapping for backward compatibility
                english_cmd="${commands[$korean_cmd]}"
                if curl -sSL "$BASE_URL/$english_cmd.md" -o ".claude/commands/$korean_cmd.md" 2>/dev/null; then
                    success_count=$((success_count + 1))
                    echo "    ✅ $korean_cmd.md (fallback)"
                else
                    echo "    ⚠️ Failed to download $korean_cmd (skipping)"
                    # Create empty file to prevent errors
                    echo "# $korean_cmd - 다운로드 실패" > ".claude/commands/$korean_cmd.md"
                fi
            fi
        else
            echo "    ⚠️ URL encoding failed for $korean_cmd (skipping)"
        fi
    done
    
    echo "  📊 Downloaded $success_count/$total_commands commands successfully"
}

# Setup Git repository
setup_git_repository() {
    if [ "$NEW_REPO" = true ]; then
        echo -e "${YELLOW}🔧 Initializing Git repository...${NC}"
        git init
        echo "  ✅ Git repository initialized"
    fi
    
    # Create/update .gitignore
    if [ ! -f ".gitignore" ]; then
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
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Claude Dev Kit
.backups/
.tadd/version.lock
mock-report.json
mock-violations.txt

# Logs
*.log
logs/

# Temporary files
*.tmp
*.bak
*~
EOF
        echo "  ✅ .gitignore created"
    fi
}

# Install TADD Enforcement (integrated from tadd-enforce-installer.sh)
install_tadd_enforcement() {
    if [ "$HAS_GIT" != true ]; then
        echo -e "${RED}❌ Git is required for TADD Enforcement${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}🛡️ Installing TADD Enforcement...${NC}"
    
    # 1. Install Git hooks
    setup_git_hooks
    
    # 2. Install TADD scripts
    install_tadd_scripts
    
    # 3. Setup GitHub Actions
    setup_github_actions
    
    # 4. Create TADD configuration
    create_tadd_config
    
    # 5. Setup Branch Protection (if GitHub CLI available)
    if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
        setup_branch_protection
    else
        echo -e "  ${YELLOW}⚠️ GitHub CLI not available - Branch Protection setup will be manual${NC}"
        show_manual_branch_protection_guide
    fi
}

# Setup Git hooks
setup_git_hooks() {
    echo "  🔧 Installing Git hooks..."
    mkdir -p .git/hooks
    
    # Pre-push hook
    cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# TADD Enforcement: Pre-push validation hook

echo "🔍 TADD Enforcement: Pre-push validation..."

PROJECT_ROOT="$(git rev-parse --show-toplevel)"

# Check if TADD scripts exist
if [ ! -f "$PROJECT_ROOT/scripts/verify_tadd_order.py" ]; then
    echo "⚠️ TADD verification scripts not found - downloading..."
    mkdir -p "$PROJECT_ROOT/scripts"
    curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/verify_tadd_order.py \
         -o "$PROJECT_ROOT/scripts/verify_tadd_order.py" 2>/dev/null
    curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/detect_mock_usage.py \
         -o "$PROJECT_ROOT/scripts/detect_mock_usage.py" 2>/dev/null
fi

# Run TADD validation
if [ -f "$PROJECT_ROOT/scripts/verify_tadd_order.py" ]; then
    python3 "$PROJECT_ROOT/scripts/verify_tadd_order.py" || {
        echo ""
        echo "❌ TADD Violation: Tests must be written before implementation"
        echo "To bypass (NOT recommended): git push --no-verify"
        exit 1
    }
fi

if [ -f "$PROJECT_ROOT/scripts/detect_mock_usage.py" ]; then
    python3 "$PROJECT_ROOT/scripts/detect_mock_usage.py" || {
        echo ""
        echo "❌ Mock usage exceeds 20% limit"
        echo "To bypass (NOT recommended): git push --no-verify"
        exit 1
    }
fi

echo "✅ TADD validation passed!"
EOF
    
    # Pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# TADD Enforcement: Pre-commit validation hook

# Check commit message format
if echo "$1" | grep -qE "^(test|feat|fix):"; then
    echo "✅ TADD-compliant commit message"
fi
EOF
    
    chmod +x .git/hooks/pre-push
    chmod +x .git/hooks/pre-commit
    echo "    ✅ Git hooks installed"
}

# Install TADD verification scripts
install_tadd_scripts() {
    echo "  📦 Installing TADD verification scripts..."
    mkdir -p scripts
    
    # Download comprehensive verification scripts
    curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/verify_tadd_order.py" \
         -o scripts/verify_tadd_order.py 2>/dev/null && echo "    ✅ verify_tadd_order.py"
    curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/detect_mock_usage.py" \
         -o scripts/detect_mock_usage.py 2>/dev/null && echo "    ✅ detect_mock_usage.py"
    curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/comprehensive_test_validator.py" \
         -o scripts/comprehensive_test_validator.py 2>/dev/null && echo "    ✅ comprehensive_test_validator.py"
    
    # Download auto report generator for /보고 command
    curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/auto_report_generator.py" \
         -o scripts/auto_report_generator.py 2>/dev/null && echo "    ✅ auto_report_generator.py"
    
    # Create quick check script
    cat > scripts/quick_tadd_check.sh << 'EOF'
#!/bin/bash
# Quick TADD validation check

echo "🧪 Quick TADD Check"
echo "==================="

# Detect and run tests based on project type
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    echo "Running pytest..."
    python3 -m pytest -x --tb=short --quiet 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
elif [ -f "package.json" ] && grep -q '"test"' package.json; then
    echo "Running npm test..."
    npm test --silent 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
elif [ -f "go.mod" ]; then
    echo "Running go test..."
    go test ./... -short 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
else
    echo "⚠️ No test framework detected"
fi

echo "✅ Quick check passed!"
EOF
    
    chmod +x scripts/*.py 2>/dev/null || true
    chmod +x scripts/quick_tadd_check.sh
}

# Setup GitHub Actions
setup_github_actions() {
    echo "  🎬 Setting up GitHub Actions..."
    mkdir -p .github/workflows
    
    # Download TADD enforcement workflow
    if curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.github/workflows/tadd-enforcement.yml" \
       -o .github/workflows/tadd-enforcement.yml 2>/dev/null; then
        echo "    ✅ TADD enforcement workflow created"
    else
        echo "    ⚠️ Failed to download GitHub Actions workflow"
    fi
}

# Create TADD configuration
create_tadd_config() {
    echo "  ⚙️ Creating TADD configuration..."
    mkdir -p .tadd
    
    cat > .tadd/config.yml << EOF
# TADD Enforcement Configuration
version: 29.0
created: $CURRENT_DATE
project: $PROJECT_NAME

rules:
  test_first: true
  mock_limit: 20  # Maximum 20% mock usage
  coverage_min: 80  # Minimum 80% coverage
  
exceptions:
  - path: "legacy/*"
    reason: "Legacy code - gradual improvement"
  - path: "vendor/*"
    reason: "Third-party code"
  - path: "node_modules/*"
    reason: "Dependencies"

notifications:
  enabled: false
  # slack: "https://hooks.slack.com/..."
  # email: "team@example.com"
EOF
    echo "    ✅ Configuration created"
}

# Setup Branch Protection (automatic)
setup_branch_protection() {
    if [ "$GITHUB_SETUP_AVAILABLE" != true ]; then
        return 1
    fi
    
    echo "  🔒 Setting up Branch Protection automatically..."
    
    REPO_INFO=$(gh repo view --json owner,name 2>/dev/null)
    if [ $? -eq 0 ]; then
        OWNER=$(echo "$REPO_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['owner']['login'])" 2>/dev/null)
        REPO=$(echo "$REPO_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])" 2>/dev/null)
        
        if [ -n "$OWNER" ] && [ -n "$REPO" ]; then
            # Try to create Branch Protection rule
            ERROR_MSG=$(gh api "repos/$OWNER/$REPO/branches/main/protection" \
                --method PUT \
                --field required_status_checks='{"strict":true,"contexts":["TADD Enforcement / verify-test-first","TADD Enforcement / check-mock-usage","TADD Enforcement / quality-gate"]}' \
                --field enforce_admins=true \
                --field required_pull_request_reviews=null \
                --field restrictions=null \
                2>&1)
            
            if [ $? -eq 0 ]; then
                echo -e "    ${GREEN}✅ Branch Protection configured automatically!${NC}"
                return 0
            elif echo "$ERROR_MSG" | grep -q "Resource not accessible by personal access token"; then
                echo -e "    ${YELLOW}⚠️ GitHub token lacks admin:repo permission${NC}"
                echo ""
                echo "    To enable automatic Branch Protection setup:"
                echo "    1. For Classic tokens: Add 'admin:repo' scope"
                echo "    2. For Fine-grained tokens: Add 'Administration: write' permission"
                echo ""
                echo "    Or manually configure Branch Protection in GitHub settings"
                show_minimal_branch_protection_guide
                return 1
            elif echo "$ERROR_MSG" | grep -q "Upgrade to GitHub Pro"; then
                echo -e "    ${YELLOW}ℹ️ Branch Protection requires GitHub Pro for private repositories${NC}"
                echo ""
                echo "    Options:"
                echo "    1. Make repository public: gh repo edit --visibility public"
                echo "    2. Upgrade to GitHub Pro ($4/month)"
                echo "    3. Continue with local TADD enforcement only (Git hooks)"
                echo ""
                echo "    ${GREEN}✅ Local TADD enforcement is still active via Git hooks${NC}"
                return 1
            else
                echo -e "    ${YELLOW}⚠️ Branch Protection setup failed${NC}"
                echo "    Error: $ERROR_MSG"
                show_manual_branch_protection_guide
                return 1
            fi
        fi
    fi
    
    echo -e "    ${YELLOW}⚠️ Could not retrieve repository information${NC}"
    show_manual_branch_protection_guide
}

# Show minimal Branch Protection setup guide (for permission issues)
show_minimal_branch_protection_guide() {
    echo ""
    echo "    Quick manual setup:"
    echo "    1. Go to Settings → Branches in your GitHub repository"
    echo "    2. Add rule → Branch name pattern: main"
    echo "    3. Enable 'Require status checks' and select TADD checks"
    echo "    4. Save changes"
}


# Show manual Branch Protection setup guide
show_manual_branch_protection_guide() {
    echo -e "${YELLOW}"
    echo "📋 Manual Branch Protection Setup Required:"
    echo "  1. Visit: https://github.com/[OWNER]/[REPO]/settings/branches"
    echo "  2. Add protection rule for 'main' branch"
    echo "  3. Enable: ✅ Require status checks to pass"
    echo "  4. Select: TADD Enforcement checks"
    echo "  5. Enable: ✅ Include administrators"
    echo -e "${NC}"
}

# Create initial project files
create_initial_files() {
    echo -e "${YELLOW}📝 Creating initial project files...${NC}"
    
    # Create CLAUDE.md
    cat > CLAUDE.md << EOF
# $PROJECT_NAME

## Project Overview
$PROJECT_DESC

## Current Status (v1.0)
- ✅ **Project Structure**: Initialized with Claude Dev Kit v29.0
- ✅ **TADD Enforcement**: Fully configured and active
- ✅ **Slash Commands**: All development commands available
- 🚀 **Ready for Development**: Use /기획 to start planning

## Development Environment Setup

### Quick Start
\`\`\`bash
# Start planning your first feature
/기획 "describe your feature"

# Or run the complete development cycle
/전체사이클 "implement feature X"
\`\`\`

## Key Features
- **TADD Enforcement**: Test-driven development automatically enforced
- **Slash Commands**: Korean/English development commands
- **Quality Assurance**: Automated code quality checks
- **Git Integration**: Pre-configured hooks and workflows

## Project Structure
\`\`\`
$PROJECT_NAME/
├── src/$PROJECT_NAME/     # Core implementation
│   ├── core/             # Shared components
│   ├── models/           # Data models
│   └── services/         # Business logic
├── tests/               # Test suites
├── docs/               # Documentation
├── scripts/            # Utility scripts
└── .claude/commands/   # Development commands
\`\`\`

## Contributing
This project follows TADD (Test-Aware Development Discipline):
1. Write tests first
2. Implement functionality 
3. Maintain < 20% mock usage
4. Achieve 80%+ test coverage

---
Created with Claude Dev Kit v29.0 on $CURRENT_DATE
EOF

    # Create README.md
    cat > README.md << EOF
# $PROJECT_NAME

$PROJECT_DESC

## Quick Start

\`\`\`bash
# Install dependencies (if any)
# pip install -r requirements.txt

# Run tests
pytest

# Start development
# Your implementation here
\`\`\`

## Development

This project uses [Claude Dev Kit](https://github.com/kyuwon-shim-ARL/claude-dev-kit) for development workflow:

- \`/기획\` - Plan new features
- \`/구현\` - Implement features  
- \`/검증\` - Test and validate
- \`/배포\` - Deploy changes

## Testing

Tests are automatically enforced through TADD (Test-Aware Development Discipline):
- Tests must be written before implementation
- Mock usage limited to 20%
- Minimum 80% test coverage required

## Contributing

1. Plan your changes with \`/기획\`
2. Implement with \`/구현\`
3. Test with \`/검증\`
4. Deploy with \`/배포\`

All pull requests are automatically checked for TADD compliance.

---
Built with ❤️ using Claude Dev Kit
EOF

    echo "  ✅ CLAUDE.md and README.md created"
}

# Execute install mode (new project)
execute_install() {
    local steps=("Environment" "Structure" "Commands" "Git" "TADD" "Files" "Complete")
    local current=0
    local total=${#steps[@]}
    
    echo -e "${BLUE}🚀 Starting complete installation...${NC}"
    echo ""
    
    for step in "${steps[@]}"; do
        current=$((current + 1))
        show_progress $current $total "$step"
        
        case $step in
            "Environment")
                detect_environment
                ;;
            "Structure") 
                install_project_structure
                ;;
            "Commands")
                install_slash_commands
                ;;
            "Git")
                if [ "$HAS_GIT" = true ]; then
                    setup_git_repository
                fi
                ;;
            "TADD")
                if [ "$HAS_GIT" = true ]; then
                    install_tadd_enforcement
                fi
                ;;
            "Files")
                create_initial_files
                ;;
            "Complete")
                install_test_integrity
                show_completion_message
                ;;
        esac
        
        sleep 0.3  # Visual feedback
    done
}

# Execute upgrade mode
execute_upgrade() {
    echo -e "${BLUE}🔄 Starting upgrade process...${NC}"
    
    # Check existing installation
    if [ ! -d ".claude/commands" ]; then
        echo -e "${RED}❌ No existing installation found. Run './init.sh project_name' first.${NC}"
        exit 1
    fi
    
    # Create backup
    BACKUP_DIR=".claude/commands.backup.$(date +%Y%m%d_%H%M%S)"
    cp -r .claude/commands "$BACKUP_DIR"
    echo -e "${GREEN}📦 Backup created: $BACKUP_DIR${NC}"
    
    detect_environment
    
    echo ""
    echo "🔄 What to upgrade?"
    echo "1. Slash commands only"
    echo "2. TADD Enforcement only" 
    echo "3. Everything (smart upgrade)"
    echo "4. Complete reinstall"
    echo ""
    read -p "Choose (1/2/3/4) [3]: " UPGRADE_CHOICE
    UPGRADE_CHOICE=${UPGRADE_CHOICE:-3}
    
    case $UPGRADE_CHOICE in
        1) 
            install_slash_commands
            ;;
        2) 
            if [ "$HAS_GIT" = true ]; then
                install_tadd_enforcement
            else
                echo -e "${RED}❌ Git is required for TADD Enforcement${NC}"
                exit 1
            fi
            ;;
        3)
            # Smart upgrade - detect what needs updating
            install_slash_commands
            
            if [ "$HAS_GIT" = true ]; then
                # Check if TADD files exist, if so update them
                if [ -f ".git/hooks/pre-push" ] || [ -f ".github/workflows/tadd-enforcement.yml" ]; then
                    echo -e "${YELLOW}🛡️ Updating existing TADD installation...${NC}"
                    install_tadd_enforcement
                fi
                
                # Setup Branch Protection if GitHub CLI is available
                if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
                    setup_branch_protection
                fi
            fi
            ;;
        4)
            echo -e "${YELLOW}🔄 Complete reinstallation...${NC}"
            PROJECT_NAME=$(basename "$PWD")
            execute_install
            ;;
    esac
    
    echo -e "${GREEN}✅ Upgrade completed successfully!${NC}"
}

# Execute TADD-only installation
execute_tadd_only() {
    echo -e "${BLUE}🛡️ Installing TADD Enforcement only...${NC}"
    
    detect_environment
    
    if [ "$HAS_GIT" != true ]; then
        echo -e "${RED}❌ Git is required for TADD Enforcement${NC}"
        exit 1
    fi
    
    install_tadd_enforcement
    
    echo -e "${GREEN}✅ TADD Enforcement installed successfully!${NC}"
}

# Execute installation check
execute_check() {
    echo -e "${BLUE}🔍 Checking installation status...${NC}"
    echo ""
    
    detect_environment
    
    # Check Claude Dev Kit components
    echo "📦 Claude Dev Kit Components:"
    if [ -d ".claude/commands" ]; then
        local cmd_count=$(ls -1 .claude/commands/ | wc -l)
        echo "  ✅ Slash commands: $cmd_count installed"
    else
        echo "  ❌ Slash commands: Not installed"
    fi
    
    if [ -f "CLAUDE.md" ]; then
        echo "  ✅ CLAUDE.md: Present"
    else
        echo "  ❌ CLAUDE.md: Missing"
    fi
    
    # Check TADD components
    echo ""
    echo "🛡️ TADD Enforcement Status:"
    if [ -f ".git/hooks/pre-push" ]; then
        echo "  ✅ Git hooks: Installed"
    else
        echo "  ❌ Git hooks: Missing"
    fi
    
    if [ -f ".github/workflows/tadd-enforcement.yml" ]; then
        echo "  ✅ GitHub Actions: Configured"
    else
        echo "  ❌ GitHub Actions: Missing"
    fi
    
    if [ -f ".tadd/config.yml" ]; then
        echo "  ✅ TADD config: Present"
    else
        echo "  ❌ TADD config: Missing"
    fi
    
    # Check Branch Protection (if GitHub CLI available)
    if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
        echo ""
        echo "🔒 GitHub Branch Protection:"
        REPO_INFO=$(gh repo view --json owner,name 2>/dev/null)
        if [ $? -eq 0 ]; then
            OWNER=$(echo "$REPO_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['owner']['login'])" 2>/dev/null)
            REPO=$(echo "$REPO_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])" 2>/dev/null)
            
            if gh api "repos/$OWNER/$REPO/branches/main/protection" >/dev/null 2>&1; then
                echo "  ✅ Branch Protection: Enabled"
            else
                echo "  ⚠️ Branch Protection: Not configured"
            fi
        fi
    fi
    
    echo ""
    echo -e "${GREEN}📊 Installation check completed${NC}"
}

# Install Test Integrity System (optional)
install_test_integrity() {
    echo ""
    echo -e "${YELLOW}🛡️ Test Integrity System (AI 테스트 우회 방지)${NC}"
    echo "  이 시스템은 AI가 테스트를 조작하거나 우회하는 것을 방지합니다:"
    echo "  • 테스트 삭제 차단"
    echo "  • Theater Testing 패턴 감지"
    echo "  • Mock 사용률 제한"
    echo "  • GitHub Actions 강제 검증"
    echo ""
    read -p "설치하시겠습니까? [Y/n]: " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo -e "${BLUE}📦 Test Integrity System 설치 중...${NC}"
        
        # 로컬 스크립트가 있으면 사용, 없으면 원격에서 다운로드
        if [ -f "$SCRIPT_DIR/install-test-integrity.sh" ]; then
            bash "$SCRIPT_DIR/install-test-integrity.sh"
        else
            curl -fsSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install-test-integrity.sh | bash
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✅ Test Integrity System 설치 완료${NC}"
            TEST_INTEGRITY_INSTALLED=true
        else
            echo -e "  ${YELLOW}⚠️ Test Integrity System 설치 실패 (나중에 수동 설치 가능)${NC}"
            TEST_INTEGRITY_INSTALLED=false
        fi
    else
        echo "  ⏭️ Test Integrity System 설치 건너뜀"
        TEST_INTEGRITY_INSTALLED=false
    fi
}

# Show completion message
show_completion_message() {
    echo ""
    echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}📋 Installation Summary:${NC}"
    echo "  • Project structure: ✅ Created"
    echo "  • Slash commands: ✅ Installed" 
    if [ "$HAS_GIT" = true ]; then
        echo "  • Git integration: ✅ Configured"
        echo "  • TADD enforcement: ✅ Active"
        echo "  • GitHub Actions: ✅ Ready"
        if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
            echo "  • Branch protection: ✅ Configured"
        else
            echo "  • Branch protection: ⚠️ Manual setup needed"
        fi
        if [ "$TEST_INTEGRITY_INSTALLED" = true ]; then
            echo "  • Test Integrity: ✅ AI 우회 방지 활성화"
        fi
    fi
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Open Claude Code in this directory"
    if [ "$NEW_REPO" = true ] && [ -n "$PROJECT_NAME" ]; then
        echo "2. Create GitHub repository and connect:"
        echo -e "   ${CYAN}gh repo create $PROJECT_NAME --public${NC}"
        echo -e "   ${CYAN}git remote add origin https://github.com/$(whoami)/$PROJECT_NAME.git${NC}"
        echo -e "   ${CYAN}git add . && git commit -m \"Initial commit\" && git push -u origin main${NC}"
    fi
    echo "3. Start development:"
    echo -e "   ${CYAN}/기획 \"your first feature\"${NC}"
    echo -e "   ${CYAN}/전체사이클 \"complete development workflow\"${NC}"
    echo ""
    echo -e "${GREEN}💡 Tips:${NC}"
    echo "  • All development commands are available as slash commands"
    echo "  • TADD automatically enforces test-first development"
    echo "  • Use './init.sh --check' to verify installation anytime"
    echo ""
}

# Main execution logic
main() {
    # Handle help flag
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_usage
        exit 0
    fi
    
    # No arguments: use defaults based on current directory
    if [ $# -eq 0 ]; then
        MODE="install"
        PROJECT_NAME=$(basename "$PWD")
        PROJECT_DESC="Claude Code project"
        
        echo -e "${BLUE}🚀 Claude Dev Kit Installation${NC}"
        echo "========================================"
        echo "Project: $PROJECT_NAME (auto-detected)"
        echo "Description: $PROJECT_DESC"
        echo ""
        echo "Tip: Use './init.sh \"project-name\" \"description\"' for custom values"
        echo ""
        
        execute_install
    # Options mode (--upgrade, --check, etc.)
    elif [[ "$1" == --* ]]; then
        MODE="${1#--}"  # Remove -- prefix
        case "$MODE" in
            upgrade)
                execute_upgrade
                ;;
            tadd-only)
                execute_tadd_only
                ;;
            reinstall)
                PROJECT_NAME=$(basename "$PWD")
                PROJECT_DESC="Reinstalled project"
                execute_install
                ;;
            check)
                execute_check
                ;;
            github-setup)
                detect_environment
                if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
                    setup_branch_protection
                else
                    show_manual_branch_protection_guide
                fi
                ;;
            *)
                echo -e "${RED}❌ Unknown option: $1${NC}"
                show_usage
                exit 1
                ;;
        esac
    else
        # Install mode with custom values
        MODE="install"
        PROJECT_NAME="$1"
        PROJECT_DESC="${2:-Claude Code project}"
        
        echo -e "${BLUE}🚀 Claude Dev Kit Installation${NC}"
        echo "========================================"
        echo "Project: $PROJECT_NAME"
        echo "Description: $PROJECT_DESC"
        echo ""
        
        execute_install
    fi
}

# Run main function
main "$@"