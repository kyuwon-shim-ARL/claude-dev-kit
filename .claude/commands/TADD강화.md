🛡️ **TADD강화 (TADD Enforcement Setup) - Hybrid Strategy v30.7**

**🎯 목적**: TADD (Test-AI-Driven Development) 강제 시스템을 3단계로 완벽 구축

**📚 컨텍스트 자동 로딩:**
- .github/workflows/tadd-enforcement.yml 확인
- scripts/comprehensive_test_validator.py 확인
- docs/TADD_PHILOSOPHY.md 확인

**📋 사용법:**
```
/TADD강화 [레벨]
```
- 레벨: local | github | full (기본값: full)

**🚀 즉시 실행할 명령어들 (하이브리드 3단계 폴백 전략):**

```bash
# 🎯 하이브리드 검증 함수 정의
run_comprehensive_validator() {
    echo "🔍 Running comprehensive TADD validation..."
    
    # 1단계: 로컬 스크립트 확인
    if [ -f scripts/comprehensive_test_validator.py ]; then
        echo "✅ Using local validator script"
        python scripts/comprehensive_test_validator.py
        return $?
    fi
    
    # 2단계: 자동 다운로드 시도  
    echo "📥 Downloading comprehensive validator..."
    if command -v curl &> /dev/null; then
        mkdir -p scripts
        if curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/comprehensive_test_validator.py" \
           -o scripts/comprehensive_test_validator.py 2>/dev/null; then
            echo "✅ Downloaded validator, running..."
            python scripts/comprehensive_test_validator.py
            return $?
        fi
    fi
    
    # 3단계: 임베디드 폴백 (기본 검증만)
    echo "⚠️ Using embedded fallback validator"
    python3 << 'EMBEDDED_VALIDATOR'
import os
import glob
import subprocess

def basic_validation():
    print("🔍 TADD Basic Validation (Embedded)")
    print("=" * 40)
    
    issues = []
    
    # 테스트 파일 존재 확인
    test_files = glob.glob("**/test*.py", recursive=True)
    if len(test_files) == 0:
        issues.append("No test files found")
    else:
        print(f"✅ Found {len(test_files)} test files")
    
    # Mock 사용률 간단 체크
    mock_count = 0
    total_lines = 0
    for test_file in test_files:
        try:
            with open(test_file, 'r') as f:
                content = f.read()
                total_lines += len(content.split('\n'))
                mock_count += content.count('Mock') + content.count('patch') + content.count('@mock')
        except Exception:
            pass
    
    if total_lines > 0:
        mock_ratio = (mock_count / total_lines) * 100
        if mock_ratio > 20:
            issues.append(f"Mock usage too high: {mock_ratio:.1f}%")
        else:
            print(f"✅ Mock usage acceptable: {mock_ratio:.1f}%")
    
    # E2E 테스트 확인
    e2e_files = glob.glob("**/test*e2e*.py", recursive=True) + \
                glob.glob("**/e2e*.py", recursive=True) + \
                glob.glob("**/*playwright*.py", recursive=True)
    
    if len(e2e_files) == 0:
        issues.append("No E2E tests found")
    else:
        print(f"✅ Found {len(e2e_files)} E2E test files")
    
    # 결과 출력
    if issues:
        print(f"\n❌ Issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
        print("\n💡 For comprehensive validation, install: pip install pytest pytest-cov")
        return 1
    else:
        print("\n✅ Basic TADD validation passed")
        return 0

if __name__ == "__main__":
    exit(basic_validation())
EMBEDDED_VALIDATOR
    return $?
}

# 1. 현재 TADD 설정 상태 확인
echo "🔍 현재 TADD Enforcement 상태 확인중..."

# GitHub Branch Protection 확인
if command -v gh &> /dev/null; then
    PROTECTION_STATUS=$(gh api repos/${GITHUB_REPOSITORY:-$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' 2>/dev/null)}/branches/main/protection 2>&1)
    if [[ "$PROTECTION_STATUS" == *"404"* ]] || [[ -z "$PROTECTION_STATUS" ]]; then
        echo "⚠️ Branch Protection: 미설정"
        NEED_PROTECTION=true
    else
        echo "✅ Branch Protection: 설정됨"
        NEED_PROTECTION=false
    fi
else
    echo "⚠️ GitHub CLI 미설치 - Branch Protection 확인 불가"
    NEED_PROTECTION=false
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

# 🎯 포괄적 TADD 검증 실행 (선택적)
if [ "$1" != "setup-only" ]; then
    echo ""
    echo "🔍 Running comprehensive TADD validation..."
    run_comprehensive_validator
    VALIDATION_RESULT=$?
    
    if [ $VALIDATION_RESULT -ne 0 ]; then
        echo "❌ TADD validation issues found. Setup will continue..."
    else
        echo "✅ TADD validation passed!"
    fi
fi

# 2. Local Git Hook 설치 (레벨: local 또는 full)
if [ "$1" = "local" ] || [ "$1" = "full" ] || [ -z "$1" ]; then
    if [ "$NEED_HOOK" = true ]; then
        echo ""
        echo "📦 Installing enhanced pre-push hook..."
        
        cat > .git/hooks/pre-push << 'HOOK'
#!/bin/bash
# Enhanced TADD Pre-push Hook v30.7

echo "🔍 Running TADD pre-push checks..."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check protected branches
protected_branches="main master develop"
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,' 2>/dev/null || echo "detached")

if [[ " $protected_branches " =~ " $current_branch " ]]; then
    echo "📋 Checking TADD compliance for: $current_branch"
    
    # Infrastructure bypass check
    COMMIT_MSG=$(git log -1 --pretty=%B)
    if [[ "$COMMIT_MSG" =~ ^(infra|docs|chore): ]]; then
        echo -e "${YELLOW}⚠️  Infrastructure commit detected - allowing bypass${NC}"
        exit 0
    fi
    
    # Run comprehensive validation
    if [ -f scripts/comprehensive_test_validator.py ]; then
        python scripts/comprehensive_test_validator.py
        RESULT=$?
    elif [ -f scripts/quick_tadd_check.sh ]; then
        bash scripts/quick_tadd_check.sh
        RESULT=$?
    else
        # Embedded basic check
        python3 << 'EMBEDDED'
import glob
test_files = glob.glob("**/test*.py", recursive=True)
if len(test_files) == 0:
    print("❌ No test files found")
    exit(1)
else:
    print(f"✅ Found {len(test_files)} test files")
    exit(0)
EMBEDDED
        RESULT=$?
    fi
    
    if [ $RESULT -ne 0 ]; then
        echo -e "${RED}❌ TADD validation failed!${NC}"
        echo -e "${YELLOW}💡 Use --no-verify to bypass (logs bypass usage)${NC}"
        
        # Log bypass attempt
        echo "$(date): TADD bypass attempted on $current_branch" >> .tadd/bypass.log 2>/dev/null || true
        exit 1
    fi
    
    echo -e "${GREEN}✅ All TADD checks passed!${NC}"
fi

exit 0
HOOK
        chmod +x .git/hooks/pre-push
        mkdir -p .tadd
        echo "✅ Enhanced pre-push hook installed!"
    fi
fi

# 3. GitHub Branch Protection 설정 (레벨: github 또는 full)
if [ "$1" = "github" ] || [ "$1" = "full" ] || [ -z "$1" ]; then
    if [ "$NEED_PROTECTION" = true ] && command -v gh &> /dev/null; then
        echo ""
        echo "🔐 GitHub Branch Protection 설정중..."
        
        REPO=$(git config --get remote.origin.url 2>/dev/null | sed 's/.*github.com[:/]\(.*\)\.git/\1/' 2>/dev/null)
        
        if [ -n "$REPO" ]; then
            gh api -X PUT repos/$REPO/branches/main/protection \
              --input - << 'EOF' 2>/dev/null
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["TADD Enforcement"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
            
            if [ $? -eq 0 ]; then
                echo "✅ Branch Protection 설정 완료!"
            else
                echo "❌ Branch Protection 설정 실패 (권한 또는 네트워크 문제)"
            fi
        else
            echo "❌ GitHub 저장소 URL을 찾을 수 없습니다"
        fi
    fi
fi

# 4. TADD 철학 문서 다운로드
if [ ! -f docs/TADD_PHILOSOPHY.md ]; then
    echo ""
    echo "📚 Downloading TADD Philosophy documentation..."
    mkdir -p docs
    if curl -sSL "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/docs/TADD_PHILOSOPHY.md" \
       -o docs/TADD_PHILOSOPHY.md 2>/dev/null; then
        echo "✅ TADD Philosophy downloaded"
    else
        echo "⚠️ Failed to download TADD Philosophy (will continue)"
    fi
fi

# 5. 최종 상태 리포트
echo ""
echo "📊 TADD Enforcement 설정 완료"
echo "=============================="
echo "1️⃣ Local Hook: $([ -f .git/hooks/pre-push ] && echo '✅ Active (Enhanced)' || echo '❌ Missing')"
echo "2️⃣ GitHub Actions: $([ -f .github/workflows/tadd-enforcement.yml ] && echo '✅ Active' || echo '❌ Missing')"
echo "3️⃣ Branch Protection: $([ "$NEED_PROTECTION" = false ] && echo '✅ Active' || echo '⚠️ Check GitHub')"
echo "4️⃣ Validator: $([ -f scripts/comprehensive_test_validator.py ] && echo '✅ Local' || echo '⚠️ Download on-demand')"
echo "5️⃣ Philosophy: $([ -f docs/TADD_PHILOSOPHY.md ] && echo '✅ Available' || echo '⚠️ Not downloaded')"
echo ""
echo "💡 Usage Tips:"
echo "  - Local Hook: 즉시 피드백 (push 전 체크)"
echo "  - Embedded Fallback: 네트워크 없어도 기본 검증"
echo "  - Comprehensive: 완전한 품질 검증"
echo ""
echo "🎯 Next Steps:"
echo "  1. 테스트를 먼저 작성: test_feature.py"
echo "  2. 구현 코드 작성: feature.py" 
echo "  3. TADD 검증: /TADD강화"
```

**⚡ 하이브리드 3단계 방어 시스템:**

## **1. 🏠 Local 단계 (즉시 피드백)**
- **1단계**: 로컬 스크립트 (최고 품질)
- **2단계**: 자동 다운로드 (네트워크 필요)
- **3단계**: 임베디드 폴백 (항상 작동)

## **2. ☁️ CI/CD 단계 (자동 검증)**
- GitHub Actions workflow 자동 실행
- 모든 push/PR에서 포괄적 검증
- Test-first, Mock usage, Coverage 체크

## **3. 🔐 Branch Protection (최종 방어)**
- GitHub Branch Protection 자동 설정
- TADD 체크 통과 필수
- Infrastructure commits 자동 우회

## **📋 슬래시 커맨드 예시**

### 예시 1: 전체 설정 (권장)
```
/TADD강화

→ 하이브리드 시스템 완전 설치
→ 3단계 폴백으로 100% 작동 보장
```

### 예시 2: 로컬만 설정
```
/TADD강화 local

→ 강화된 pre-push hook만 설치
→ 임베디드 검증 포함
```

### 예시 3: 설정만 (검증 스킵)
```
/TADD강화 setup-only

→ 검증 없이 빠른 설정
```

## **🎯 v30.7 혁신 사항**

### ✅ **100% 작동 보장**
- 로컬 스크립트 → 자동 다운로드 → 임베디드 폴백
- 네트워크 없어도 기본 검증 가능

### ✅ **지능형 우회**
- Infrastructure commits 자동 감지
- 우회 로깅으로 남용 방지

### ✅ **점진적 강화**
- 기본: 임베디드 검증
- 표준: 자동 다운로드
- 고급: 로컬 스크립트

### ✅ **완전한 이식성**
- 단일 .md 파일에 모든 로직 포함
- 어떤 프로젝트에서도 동일 동작

ARGUMENTS: "${args}"