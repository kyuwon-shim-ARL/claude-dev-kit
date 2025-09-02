#!/bin/bash
# TADD Enforcement Universal Installer
# One-click installation for any repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TADD_VERSION="1.0.0"
GITHUB_RAW_BASE="https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main"

echo -e "${BLUE}🚀 TADD Enforcement Universal Installer v${TADD_VERSION}${NC}"
echo "================================================"

# Detect project type
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "javascript"
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "python"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "java"
    else
        echo "unknown"
    fi
}

# Detect test framework
detect_test_framework() {
    local project_type=$1
    
    case $project_type in
        javascript)
            if grep -q "jest" package.json 2>/dev/null; then
                echo "jest"
            elif grep -q "mocha" package.json 2>/dev/null; then
                echo "mocha"
            elif grep -q "vitest" package.json 2>/dev/null; then
                echo "vitest"
            else
                echo "npm test"
            fi
            ;;
        python)
            if [ -f "pytest.ini" ] || grep -q "pytest" requirements.txt 2>/dev/null; then
                echo "pytest"
            else
                echo "python -m unittest"
            fi
            ;;
        go)
            echo "go test"
            ;;
        rust)
            echo "cargo test"
            ;;
        java)
            if [ -f "pom.xml" ]; then
                echo "mvn test"
            else
                echo "gradle test"
            fi
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git is not installed${NC}"
        exit 1
    fi
    
    # Check if it's a git repository
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}⚠️  Not a git repository. Initializing...${NC}"
        git init
    fi
    
    # Check Python (for TADD scripts)
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}⚠️  Python not found (optional for advanced features)${NC}"
    fi
    
    echo -e "${GREEN}✅ Prerequisites satisfied${NC}"
}

# Install Git hooks
install_git_hooks() {
    echo -e "${YELLOW}🔧 Installing Git hooks...${NC}"
    
    mkdir -p .git/hooks
    
    # Download pre-push hook
    curl -sSL "${GITHUB_RAW_BASE}/scripts/setup_tadd_hooks.sh" | bash
    
    echo -e "${GREEN}✅ Git hooks installed${NC}"
}

# Install TADD scripts
install_tadd_scripts() {
    echo -e "${YELLOW}📦 Installing TADD verification scripts...${NC}"
    
    mkdir -p scripts
    
    # Download core scripts
    curl -sSL "${GITHUB_RAW_BASE}/scripts/verify_tadd_order.py" \
         -o scripts/verify_tadd_order.py
    curl -sSL "${GITHUB_RAW_BASE}/scripts/detect_mock_usage.py" \
         -o scripts/detect_mock_usage.py
    
    # Create quick check script based on project type
    local project_type=$(detect_project_type)
    local test_framework=$(detect_test_framework $project_type)
    
    cat > scripts/quick_tadd_check.sh << EOF
#!/bin/bash
# Quick TADD validation for ${project_type} project

echo "🧪 Running quick TADD check (${test_framework})..."

case "${test_framework}" in
    jest|mocha|vitest)
        npm test --silent 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
        ;;
    pytest)
        python -m pytest -x --tb=short --quiet 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
        ;;
    "go test")
        go test ./... -short 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
        ;;
    "cargo test")
        cargo test --quiet 2>/dev/null || { echo "❌ Tests failed"; exit 1; }
        ;;
    *)
        echo "⚠️  Test framework not detected, skipping tests"
        ;;
esac

echo "✅ Quick check passed!"
EOF
    
    chmod +x scripts/quick_tadd_check.sh
    chmod +x scripts/*.py 2>/dev/null || true
    
    echo -e "${GREEN}✅ TADD scripts installed${NC}"
}

# Setup GitHub Actions
setup_github_actions() {
    echo -e "${YELLOW}🎬 Setting up GitHub Actions...${NC}"
    
    mkdir -p .github/workflows
    
    # Check if workflow already exists
    if [ -f ".github/workflows/tadd-enforcement.yml" ]; then
        echo -e "${YELLOW}⚠️  Existing TADD workflow found. Backing up...${NC}"
        mv .github/workflows/tadd-enforcement.yml .github/workflows/tadd-enforcement.yml.bak
    fi
    
    # Download workflow template
    curl -sSL "${GITHUB_RAW_BASE}/.github/workflows/tadd-enforcement.yml" \
         -o .github/workflows/tadd-enforcement.yml
    
    echo -e "${GREEN}✅ GitHub Actions workflow created${NC}"
}

# Create TADD configuration
create_tadd_config() {
    echo -e "${YELLOW}⚙️  Creating TADD configuration...${NC}"
    
    mkdir -p .tadd
    
    cat > .tadd/config.yml << EOF
# TADD Enforcement Configuration
version: ${TADD_VERSION}
created: $(date +%Y-%m-%d)
project_type: $(detect_project_type)
test_framework: $(detect_test_framework $(detect_project_type))

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
    
    echo -e "${GREEN}✅ Configuration created at .tadd/config.yml${NC}"
}

# Update .gitignore
update_gitignore() {
    echo -e "${YELLOW}📝 Updating .gitignore...${NC}"
    
    # Check if .gitignore exists
    if [ ! -f ".gitignore" ]; then
        touch .gitignore
    fi
    
    # Add TADD-specific ignores if not present
    if ! grep -q ".tadd/version.lock" .gitignore 2>/dev/null; then
        echo "" >> .gitignore
        echo "# TADD Enforcement" >> .gitignore
        echo ".tadd/version.lock" >> .gitignore
        echo "mock-report.json" >> .gitignore
        echo "mock-violations.txt" >> .gitignore
    fi
    
    echo -e "${GREEN}✅ .gitignore updated${NC}"
}

# Show next steps
show_next_steps() {
    echo ""
    echo -e "${GREEN}🎉 TADD Enforcement installed successfully!${NC}"
    echo ""
    echo -e "${BLUE}📋 Installation Summary:${NC}"
    echo "  • Git hooks: ✅ Installed"
    echo "  • TADD scripts: ✅ Installed"
    echo "  • GitHub Actions: ✅ Configured"
    echo "  • Configuration: ✅ Created"
    echo ""
    echo -e "${YELLOW}🔧 Next Steps:${NC}"
    echo ""
    echo "1. Test local hooks:"
    echo -e "   ${BLUE}git commit -m 'test: initial test'${NC}"
    echo ""
    echo "2. Push to trigger GitHub Actions:"
    echo -e "   ${BLUE}git push origin main${NC}"
    echo ""
    echo "3. Enable Branch Protection (REQUIRED for enforcement):"
    echo -e "   ${BLUE}Visit: https://github.com/[owner]/[repo]/settings/branches${NC}"
    echo "   • Add rule for 'main' branch"
    echo "   • Enable 'Require status checks'"
    echo "   • Select: TADD Enforcement checks"
    echo "   • Enable 'Include administrators'"
    echo ""
    echo "4. Customize configuration:"
    echo -e "   ${BLUE}Edit: .tadd/config.yml${NC}"
    echo ""
    echo -e "${GREEN}💡 Tips:${NC}"
    echo "  • Run './scripts/quick_tadd_check.sh' for local validation"
    echo "  • Use 'git push --no-verify' to bypass (emergency only)"
    echo "  • See docs at: https://github.com/kyuwon-shim-ARL/claude-dev-kit"
}

# Main installation flow
main() {
    check_prerequisites
    
    echo ""
    echo -e "${YELLOW}This will install TADD Enforcement in your repository.${NC}"
    echo "Components to install:"
    echo "  • Git hooks (pre-push, pre-commit)"
    echo "  • TADD verification scripts"
    echo "  • GitHub Actions workflow"
    echo "  • Configuration files"
    echo ""
    read -p "Continue? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation cancelled${NC}"
        exit 1
    fi
    
    install_git_hooks
    install_tadd_scripts
    setup_github_actions
    create_tadd_config
    update_gitignore
    show_next_steps
}

# Run main function
main "$@"