#!/bin/bash
#
# TADD Quick Check Script
# 빠른 로컬 검증을 위한 간단한 스크립트
#

set -e

echo "🔍 TADD Quick Check"
echo "=================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check for test commits
echo "📊 Checking commit order..."
TEST_COMMITS=$(git log --grep="^test:" --oneline 2>/dev/null | head -5)
FEAT_COMMITS=$(git log --grep="^feat:\|^fix:" --oneline 2>/dev/null | head -5)

if [ -z "$TEST_COMMITS" ]; then
    echo -e "${RED}❌ No test commits found${NC}"
    echo "   Use 'test: description' for test commits"
    EXIT_CODE=1
else
    echo -e "${GREEN}✅ Found test commits${NC}"
fi

# 2. Check most recent test/feature pair
LAST_TEST=$(git log --grep="^test:" -1 --format="%H %s" 2>/dev/null)
LAST_FEAT=$(git log --grep="^feat:\|^fix:" -1 --format="%H %s" 2>/dev/null)

if [ -n "$LAST_TEST" ] && [ -n "$LAST_FEAT" ]; then
    TEST_HASH=$(echo $LAST_TEST | cut -d' ' -f1)
    FEAT_HASH=$(echo $LAST_FEAT | cut -d' ' -f1)
    
    # Check if test comes before feature
    if git merge-base --is-ancestor $TEST_HASH $FEAT_HASH 2>/dev/null; then
        echo -e "${GREEN}✅ Test was committed before implementation${NC}"
    else
        echo -e "${YELLOW}⚠️  Latest implementation might be before test${NC}"
    fi
fi

echo ""
echo "📊 Checking mock usage..."

# 3. Quick mock check
if [ -d "tests" ] || [ -d "test" ]; then
    MOCK_COUNT=$(grep -r "Mock\|mock\|@patch" tests test 2>/dev/null | wc -l || echo 0)
    TEST_COUNT=$(grep -r "def test_" tests test 2>/dev/null | wc -l || echo 0)
    
    if [ "$TEST_COUNT" -gt 0 ]; then
        MOCK_PERCENTAGE=$((MOCK_COUNT * 100 / TEST_COUNT))
        
        if [ "$MOCK_PERCENTAGE" -gt 20 ]; then
            echo -e "${RED}❌ Mock usage too high: ${MOCK_PERCENTAGE}%${NC}"
            echo "   Limit: 20%"
            EXIT_CODE=1
        else
            echo -e "${GREEN}✅ Mock usage acceptable: ${MOCK_PERCENTAGE}%${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  No test methods found${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No test directory found${NC}"
fi

echo ""
echo "📊 Running Python verification scripts..."

# 4. Run Python scripts if they exist
if [ -f "scripts/verify_tadd_order.py" ]; then
    echo "Running TADD order verification..."
    python scripts/verify_tadd_order.py || EXIT_CODE=$?
fi

echo ""

if [ -f "scripts/detect_mock_usage.py" ]; then
    echo "Running mock usage analysis..."
    python scripts/detect_mock_usage.py || EXIT_CODE=$?
fi

echo ""
echo "=================="

# Summary
if [ "${EXIT_CODE:-0}" -eq 0 ]; then
    echo -e "${GREEN}✅ TADD Quick Check: PASSED${NC}"
    echo ""
    echo "Ready for PR! 🚀"
else
    echo -e "${RED}❌ TADD Quick Check: FAILED${NC}"
    echo ""
    echo "Please fix the issues above before creating a PR"
    exit 1
fi