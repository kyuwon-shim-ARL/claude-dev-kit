#!/bin/bash
#
# Test Integrity System Installer
# AI 테스트 우회/조작 방지 시스템 원클릭 설치
#

set -e  # 오류 시 즉시 중단

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════╗
║   TEST INTEGRITY ENFORCEMENT SYSTEM    ║
║         AI 우회 방지 시스템            ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 진행 상태 표시 함수
progress() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 1. 환경 검사
progress "시스템 환경 검사 중..."

# Python 확인
if ! command -v python3 &> /dev/null; then
    error "Python3가 설치되어 있지 않습니다"
    exit 1
fi

# Git 확인
if ! git rev-parse --git-dir &> /dev/null; then
    error "Git 저장소가 아닙니다"
    exit 1
fi

# GitHub CLI 확인 (선택적)
if command -v gh &> /dev/null; then
    progress "GitHub CLI 감지됨 - 고급 기능 활성화"
    HAS_GH=true
else
    warning "GitHub CLI 미설치 - 일부 기능 제한"
    HAS_GH=false
fi

# 2. 필요한 디렉토리 생성
progress "디렉토리 구조 생성 중..."
mkdir -p .github/workflows
mkdir -p scripts
mkdir -p tests
mkdir -p .claude/commands

# 3. Pre-commit Hook 설치
progress "Git Pre-commit Hook 설치 중..."

cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# Test Integrity Pre-commit Hook
# AI의 테스트 조작 시도를 차단합니다

echo "🔍 테스트 무결성 검사 시작..."

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 테스트 개수 감소 방지
if [ -d "tests" ]; then
    BEFORE=$(git show HEAD:tests/ 2>/dev/null | grep -c "def test_" || echo 0)
    CURRENT=$(find tests/ -name "*.py" -exec grep -c "def test_" {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}')
    
    if [ "$CURRENT" -lt "$BEFORE" ]; then
        echo -e "${RED}❌ 테스트 감소 감지!${NC}"
        echo -e "  이전: $BEFORE개 → 현재: $CURRENT개"
        echo -e "${YELLOW}💡 테스트를 삭제하지 말고 수정하세요${NC}"
        exit 1
    fi
fi

# 2. Theater Testing 패턴 감지
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts)$' || true)

if [ -n "$STAGED_FILES" ]; then
    for file in $STAGED_FILES; do
        # Theater Testing 패턴 검사
        if git diff --cached "$file" | grep -E "(assert.*is\s+not\s+None$|assert\s+True$|pass\s*#.*test)" > /dev/null; then
            echo -e "${RED}❌ Theater Testing 패턴 감지: $file${NC}"
            echo -e "${YELLOW}💡 구체적인 값을 검증하는 assertion을 사용하세요${NC}"
            exit 1
        fi
        
        # 과도한 Mock 사용 검사
        MOCK_COUNT=$(git diff --cached "$file" | grep -c "mock\|Mock" || true)
        if [ "$MOCK_COUNT" -gt 5 ]; then
            echo -e "${YELLOW}⚠️ Mock 과다 사용 의심: $file (${MOCK_COUNT}회)${NC}"
        fi
    done
fi

# 3. 테스트 실행 (pytest가 있는 경우)
if command -v pytest &> /dev/null && [ -d "tests" ]; then
    echo "🧪 테스트 실행 중..."
    if ! pytest --tb=short --quiet; then
        echo -e "${RED}❌ 테스트 실패! 모든 테스트가 통과해야 커밋할 수 있습니다${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ 테스트 무결성 검사 통과${NC}"
HOOK

chmod +x .git/hooks/pre-commit
progress "✅ Pre-commit Hook 설치 완료"

# 4. GitHub Actions Workflow 설치
progress "GitHub Actions Workflow 설치 중..."

cat > .github/workflows/test-integrity.yml << 'WORKFLOW'
name: Test Integrity Enforcement
on:
  push:
    branches: [ main, develop ]
  pull_request:
    types: [ opened, synchronize, reopened ]

jobs:
  enforce-test-integrity:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout Code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # 전체 히스토리 필요
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install Dependencies
      run: |
        pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
    
    - name: Count and Verify Tests
      id: test_count
      run: |
        TOTAL=$(find . -name 'test*.py' -exec grep -c 'def test_' {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}')
        echo "total_tests=$TOTAL" >> $GITHUB_OUTPUT
        echo "📊 총 테스트 개수: $TOTAL"
        
        # 이전 커밋과 비교
        if [ "${{ github.event_name }}" = "pull_request" ]; then
          BASE_COUNT=$(git show ${{ github.event.pull_request.base.sha }}:tests/ 2>/dev/null | grep -c 'def test_' || echo 0)
          if [ "$TOTAL" -lt "$BASE_COUNT" ]; then
            echo "::error::테스트 감소 감지! $BASE_COUNT → $TOTAL"
            exit 1
          fi
        fi
    
    - name: Run All Tests (No Skip Allowed)
      run: |
        pytest --strict-markers --tb=short -v
    
    - name: Check Test Quality
      run: |
        # Theater Testing 패턴 검사
        if find . -name "test*.py" -exec grep -l "assert.*is not None$\|assert True$" {} \; | head -1; then
          echo "::error::Theater Testing 패턴 감지!"
          exit 1
        fi
    
    - name: Analyze Mock Usage
      run: |
        # Mock 사용률 계산
        MOCK_COUNT=$(find . -name "*.py" -exec grep -c "mock\|Mock" {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}')
        TOTAL_LINES=$(find . -name "test*.py" -exec wc -l {} \; | awk '{sum+=$1} END {print sum}')
        
        if [ "$TOTAL_LINES" -gt 0 ]; then
          MOCK_PERCENTAGE=$((MOCK_COUNT * 100 / TOTAL_LINES))
          echo "📊 Mock 사용률: ${MOCK_PERCENTAGE}%"
          
          if [ "$MOCK_PERCENTAGE" -gt 20 ]; then
            echo "::warning::Mock 사용률이 20%를 초과합니다 (${MOCK_PERCENTAGE}%)"
          fi
        fi
    
    - name: Generate Test Report
      if: always()
      run: |
        echo "## 📋 Test Integrity Report" >> $GITHUB_STEP_SUMMARY
        echo "- 총 테스트: ${{ steps.test_count.outputs.total_tests }}개" >> $GITHUB_STEP_SUMMARY
        echo "- 상태: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
        echo "- 시간: $(date)" >> $GITHUB_STEP_SUMMARY
WORKFLOW

progress "✅ GitHub Actions Workflow 설치 완료"

# 5. 검증 스크립트 설치
progress "검증 스크립트 설치 중..."

cat > scripts/validate_test_integrity.sh << 'VALIDATOR'
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
VALIDATOR

chmod +x scripts/validate_test_integrity.sh

# 6. 설치 검증
progress "설치 검증 중..."
./scripts/validate_test_integrity.sh

# 7. 완료 메시지
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     🎉 설치 완료!                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo "다음 기능들이 활성화되었습니다:"
echo "  ✅ 커밋 시 테스트 무결성 자동 검사"
echo "  ✅ GitHub Actions CI/CD 파이프라인"
echo "  ✅ Theater Testing 패턴 차단"
echo "  ✅ 테스트 개수 감소 방지"
echo "  ✅ Mock 사용률 모니터링"
echo ""
echo "사용 방법:"
echo "  1. 코드 변경 후 git commit 시 자동 검사"
echo "  2. PR 생성 시 GitHub Actions 자동 실행"
echo "  3. scripts/validate_test_integrity.sh로 수동 검증"
echo ""
echo -e "${YELLOW}💡 팁: '/테스트강화' 슬래시 커맨드로 Claude에서 직접 사용 가능${NC}"