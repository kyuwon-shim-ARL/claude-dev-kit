#!/bin/bash
# TADD Enforcement: Git Hooks Auto-installer
# Ensures TADD compliance at the local level

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

echo "🔧 TADD Enforcement: Installing Git Hooks"
echo "=========================================="

# Check if git repository exists
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo "❌ Error: Not a git repository"
    echo "Please run 'git init' first"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Create pre-push hook
cat > "$HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# TADD Enforcement: Pre-push validation hook
# Prevents pushing code that violates TADD principles

echo "🔍 TADD Enforcement: Pre-push validation..."

PROJECT_ROOT="$(git rev-parse --show-toplevel)"

# Check if TADD scripts exist
if [ ! -f "$PROJECT_ROOT/scripts/verify_tadd_order.py" ]; then
    echo "⚠️  Warning: TADD verification scripts not found"
    echo "Installing from claude-dev-kit..."
    
    # Download verification scripts
    mkdir -p "$PROJECT_ROOT/scripts"
    curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/verify_tadd_order.py \
         -o "$PROJECT_ROOT/scripts/verify_tadd_order.py"
    curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/detect_mock_usage.py \
         -o "$PROJECT_ROOT/scripts/detect_mock_usage.py"
fi

# 1. Verify test-first development order
if [ -f "$PROJECT_ROOT/scripts/verify_tadd_order.py" ]; then
    echo "📊 Checking test-first development order..."
    python "$PROJECT_ROOT/scripts/verify_tadd_order.py" || {
        echo ""
        echo "❌ TADD Violation: Tests must be written before implementation"
        echo ""
        echo "Please ensure:"
        echo "  1. Write failing tests first (commit with 'test:' prefix)"
        echo "  2. Then implement the feature (commit with 'feat:' or 'fix:' prefix)"
        echo "  3. Tests should fail initially and pass after implementation"
        echo ""
        echo "To bypass (NOT recommended): git push --no-verify"
        exit 1
    }
fi

# 2. Check mock usage limits
if [ -f "$PROJECT_ROOT/scripts/detect_mock_usage.py" ]; then
    echo "📊 Checking mock usage (limit: 20%)..."
    python "$PROJECT_ROOT/scripts/detect_mock_usage.py" || {
        echo ""
        echo "❌ Mock Usage Violation: Exceeds 20% limit"
        echo ""
        echo "Please reduce mock usage by:"
        echo "  1. Using real implementations where possible"
        echo "  2. Creating test fixtures with real data"
        echo "  3. Using integration tests instead of unit tests with mocks"
        echo ""
        echo "To bypass (NOT recommended): git push --no-verify"
        exit 1
    }
fi

# 3. Run quick local tests
if [ -f "$PROJECT_ROOT/scripts/quick_tadd_check.sh" ]; then
    echo "🧪 Running quick local tests..."
    bash "$PROJECT_ROOT/scripts/quick_tadd_check.sh" || {
        echo ""
        echo "❌ Local tests failed"
        echo ""
        echo "Please fix failing tests before pushing"
        echo "Run './scripts/quick_tadd_check.sh' to see details"
        echo ""
        echo "To bypass (NOT recommended): git push --no-verify"
        exit 1
    }
fi

echo "✅ All TADD checks passed locally!"
echo "📤 Proceeding with push..."
EOF

# Create pre-commit hook
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# TADD Enforcement: Pre-commit validation hook
# Ensures commit messages follow TADD conventions

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Check for test commits
if echo "$COMMIT_MSG" | grep -qE "^test:"; then
    echo "✅ Test commit detected - good TADD practice!"
fi

# Warn about implementation without tests
if echo "$COMMIT_MSG" | grep -qE "^(feat|fix):"; then
    # Check if there are test files in the staged changes
    if ! git diff --cached --name-only | grep -qE "(test_|_test\.py|\.test\.|spec\.)"; then
        echo "⚠️  Warning: Implementation commit without test files"
        echo "Remember: Write tests first (TADD principle)"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi
EOF

# Make hooks executable
chmod +x "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-commit"

# Create quick check script if it doesn't exist
if [ ! -f "$PROJECT_ROOT/scripts/quick_tadd_check.sh" ]; then
    cat > "$PROJECT_ROOT/scripts/quick_tadd_check.sh" << 'EOF'
#!/bin/bash
# Quick TADD validation check
# Runs essential tests without full test suite

echo "🧪 Quick TADD Check"
echo "==================="

# Detect test framework
if [ -f "pytest.ini" ] || [ -f "setup.cfg" ] || [ -f "pyproject.toml" ]; then
    echo "Running pytest (fast mode)..."
    python -m pytest -x --tb=short --quiet 2>/dev/null || {
        echo "❌ Tests failed"
        exit 1
    }
elif [ -f "package.json" ]; then
    if grep -q '"test"' package.json; then
        echo "Running npm test..."
        npm test --silent 2>/dev/null || {
            echo "❌ Tests failed"
            exit 1
        }
    fi
elif [ -f "go.mod" ]; then
    echo "Running go test..."
    go test ./... -short 2>/dev/null || {
        echo "❌ Tests failed"
        exit 1
    }
else
    echo "⚠️  No test framework detected"
    echo "Skipping test execution"
fi

echo "✅ Quick check passed!"
EOF
    chmod +x "$PROJECT_ROOT/scripts/quick_tadd_check.sh"
fi

echo ""
echo "✅ Git hooks installed successfully!"
echo ""
echo "📋 Installed hooks:"
echo "  • pre-push: Validates TADD compliance before push"
echo "  • pre-commit: Checks commit message conventions"
echo ""
echo "🔧 Next steps:"
echo "  1. Test the hooks: git commit -m 'test: sample test'"
echo "  2. Configure GitHub Actions: See .github/workflows/tadd-enforcement.yml"
echo "  3. Enable Branch Protection: Settings → Branches → main"
echo ""
echo "💡 To bypass hooks (emergency only): git push --no-verify"