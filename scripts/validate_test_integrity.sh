#!/bin/bash
# Test Integrity Validator
# 테스트 무결성을 검증합니다

echo "🔍 테스트 무결성 검증 시작..."

# 검증 항목들
CHECKS_PASSED=0
CHECKS_FAILED=0

# 1. Pre-commit hook 확인
if [ -f .git/hooks/pre-commit ] && [ -x .git/hooks/pre-commit ]; then
    echo "✅ Pre-commit hook 설치됨"
    ((CHECKS_PASSED++))
else
    echo "❌ Pre-commit hook 미설치"
    ((CHECKS_FAILED++))
fi

# 2. GitHub Actions 확인
if [ -f .github/workflows/test-integrity.yml ]; then
    echo "✅ GitHub Actions workflow 설치됨"
    ((CHECKS_PASSED++))
else
    echo "❌ GitHub Actions workflow 미설치"
    ((CHECKS_FAILED++))
fi

# 3. 테스트 디렉토리 확인
if [ -d tests ]; then
    TEST_COUNT=$(find tests/ -name "test*.py" -exec grep -c "def test_" {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}')
    echo "✅ 테스트 디렉토리 존재 ($TEST_COUNT개 테스트)"
    ((CHECKS_PASSED++))
else
    echo "⚠️ 테스트 디렉토리 없음"
fi

# 4. Python 환경 확인
if command -v python3 &> /dev/null && command -v pytest &> /dev/null; then
    echo "✅ Python 테스트 환경 준비됨"
    ((CHECKS_PASSED++))
else
    echo "⚠️ pytest 미설치"
fi

# 결과 출력
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "검증 결과: $CHECKS_PASSED/$((CHECKS_PASSED + CHECKS_FAILED)) 통과"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $CHECKS_FAILED -eq 0 ]; then
    echo "🎉 테스트 무결성 시스템 준비 완료!"
    exit 0
else
    echo "⚠️ 일부 구성요소가 누락되었습니다"
    exit 1
fi
