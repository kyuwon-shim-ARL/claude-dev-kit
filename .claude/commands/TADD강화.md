🛡️ **TADD강화 (TADD Enforcement Setup)**

**🎯 목적**: TADD (Test-Driven AI Development) 강제 시스템을 3단계로 완벽 구축

**📚 컨텍스트 자동 로딩:**
- .github/workflows/tadd-enforcement.yml 확인
- scripts/verify_tadd_order.py 확인
- project_rules.md 확인

**📋 사용법:**
```
/TADD강화 [레벨]
```
- 레벨: local | github | full (기본값: full)

**🚀 즉시 실행할 명령어들 (순서대로 실행):**

```bash
# 1. 현재 TADD 설정 상태 확인
echo "🔍 현재 TADD Enforcement 상태 확인중..."

# GitHub Branch Protection 확인
if command -v gh &> /dev/null; then
    PROTECTION_STATUS=$(gh api repos/${GITHUB_REPOSITORY:-$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')} /branches/main/protection 2>&1)
    if [[ "$PROTECTION_STATUS" == *"404"* ]]; then
        echo "⚠️ Branch Protection: 미설정"
        NEED_PROTECTION=true
    else
        echo "✅ Branch Protection: 설정됨"
        NEED_PROTECTION=false
    fi
else
    echo "⚠️ GitHub CLI 미설치 - Branch Protection 확인 불가"
fi

# Local Git Hook 확인
if [ -f .git/hooks/pre-push ]; then
    echo "✅ Local pre-push hook: 설치됨"
    NEED_HOOK=false
else
    echo "⚠️ Local pre-push hook: 미설치"
    NEED_HOOK=true
fi

# GitHub Actions 확인
if [ -f .github/workflows/tadd-enforcement.yml ]; then
    echo "✅ GitHub Actions: 설정됨"
else
    echo "❌ GitHub Actions: 미설정"
fi

# 2. Local Git Hook 설치 (레벨: local 또는 full)
if [ "$1" = "local" ] || [ "$1" = "full" ] || [ -z "$1" ]; then
    if [ "$NEED_HOOK" = true ]; then
        echo "📦 Local pre-push hook 설치중..."
        
        cat > .git/hooks/pre-push << 'HOOK'
#!/bin/bash
# Pre-push hook for TADD enforcement

echo "🔍 Running TADD pre-push checks..."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check protected branches
protected_branches="main develop"
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [[ " $protected_branches " =~ " $current_branch " ]]; then
    echo "📋 Checking TADD compliance for: $current_branch"
    
    # Quick TADD check
    if [ -f scripts/quick_tadd_check.sh ]; then
        bash scripts/quick_tadd_check.sh
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ TADD check failed!${NC}"
            echo -e "${YELLOW}💡 Use --no-verify to bypass (not recommended)${NC}"
            exit 1
        fi
    fi
    
    # Python TADD verification
    if [ -f scripts/verify_tadd_order.py ]; then
        python scripts/verify_tadd_order.py
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Test-first order violation!${NC}"
            exit 1
        fi
    fi
    
    # Mock usage check
    if [ -f scripts/detect_mock_usage.py ]; then
        python scripts/detect_mock_usage.py
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Mock usage exceeds 20%!${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✅ All TADD checks passed!${NC}"
fi

exit 0
HOOK
        chmod +x .git/hooks/pre-push
        echo "✅ Local pre-push hook 설치 완료!"
    fi
fi

# 3. GitHub Branch Protection 설정 (레벨: github 또는 full)
if [ "$1" = "github" ] || [ "$1" = "full" ] || [ -z "$1" ]; then
    if [ "$NEED_PROTECTION" = true ] && command -v gh &> /dev/null; then
        echo "🔐 GitHub Branch Protection 설정중..."
        
        REPO=$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
        
        gh api -X PUT repos/$REPO/branches/main/protection \
          --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["TADD Enforcement", "TADD Quality Gate"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "required_approving_review_count": 0
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
        
        if [ $? -eq 0 ]; then
            echo "✅ Branch Protection 설정 완료!"
        else
            echo "❌ Branch Protection 설정 실패 (권한 확인 필요)"
        fi
    fi
fi

# 4. 최종 상태 리포트
echo ""
echo "📊 TADD Enforcement 설정 완료"
echo "=============================="
echo "1️⃣ Local Hook: $([ -f .git/hooks/pre-push ] && echo '✅ Active' || echo '❌ Missing')"
echo "2️⃣ GitHub Actions: $([ -f .github/workflows/tadd-enforcement.yml ] && echo '✅ Active' || echo '❌ Missing')"
echo "3️⃣ Branch Protection: $([ "$NEED_PROTECTION" = false ] && echo '✅ Active' || echo '⚠️ Check GitHub')"
echo ""
echo "💡 Tips:"
echo "  - Local: 즉시 피드백 (push 전 체크)"
echo "  - Actions: 자동 CI/CD 체크"
echo "  - Protection: 최종 머지 게이트"
```

**⚡ 3단계 방어 시스템:**

## **1. 🏠 Local 단계 (즉시 피드백)**
- Git pre-push hook 자동 설치
- Push 전에 TADD 체크 실행
- 실패 시 push 차단

## **2. ☁️ CI/CD 단계 (자동 검증)**
- GitHub Actions workflow 확인
- 모든 push/PR에서 자동 실행
- Test-first, Mock usage, Coverage 체크

## **3. 🔐 Branch Protection (최종 방어)**
- GitHub Branch Protection rules 설정
- Strict mode: 최신 상태 유지 필수
- Admin 포함 모든 사용자에게 적용
- TADD 체크 통과 필수

## **📋 슬래시 커맨드 예시**

### 예시 1: 전체 설정 (권장)
```
/TADD강화

→ 출력:
🔍 현재 TADD Enforcement 상태 확인중...
⚠️ Branch Protection: 미설정
⚠️ Local pre-push hook: 미설치
✅ GitHub Actions: 설정됨

📦 Local pre-push hook 설치중...
✅ Local pre-push hook 설치 완료!

🔐 GitHub Branch Protection 설정중...
✅ Branch Protection 설정 완료!

📊 TADD Enforcement 설정 완료
==============================
1️⃣ Local Hook: ✅ Active
2️⃣ GitHub Actions: ✅ Active
3️⃣ Branch Protection: ✅ Active
```

### 예시 2: 로컬만 설정
```
/TADD강화 local

→ Local hook만 설치 (개인 프로젝트용)
```

### 예시 3: GitHub만 설정
```
/TADD강화 github

→ Branch Protection만 설정 (팀 프로젝트용)
```

## **⚙️ 옵션**
```
--check-only    : 현재 상태만 확인
--force         : 기존 설정 덮어쓰기
--branch NAME   : main 대신 다른 브랜치 보호
```

## **🎯 성공 기준**
- Local hook 설치율: 100%
- Actions 정상 동작: 95%+
- Protection 적용: 90%+
- TADD 준수율: 80%+

ARGUMENTS: "${args}"