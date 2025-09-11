<!--
@meta
id: feature_20250905_1110_FEAT-PRD-v29-unified-installer
type: feature
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: PRD, v29, FEAT-PRD-v29-unified-installer.md, unified, FEAT
related: 
-->

# PRD: One-Click 통합 설치 시스템 (v29.0)

## 1. 문제 정의

### 현재 상황 (복잡한 다단계 설치)
```bash
# 기존: 여러 스크립트 실행 필요
./init.sh my_project              # 1. 프로젝트 구조
curl ... tadd-enforce-installer   # 2. TADD 설치
# GitHub Settings에서 수동       # 3. Branch Protection
```

**문제점:**
- **인지 부하**: 사용자가 3단계 과정 기억해야 함
- **실행 누락**: Branch Protection 설정을 빼먹기 쉬움
- **일관성 부족**: 설치마다 다른 결과물
- **GitHub 권한**: API 권한 없으면 자동 설정 불가

### 비즈니스 임팩트
- **채택률 저하**: 복잡한 설치로 사용 포기
- **품질 편차**: 불완전한 설치로 TADD 효과 반감
- **지원 비용**: 설치 문제 문의 증가

## 2. 목표

### 핵심 목표
**"진짜 One-Click: ./init.sh 하나만 실행하면 모든 것이 완료"**

### 성공 지표
- 설치 명령어: 1개 (현재 3개)
- 수동 설정: 0개 (현재 1개 - Branch Protection)
- 설치 성공률: 99% (현재 ~60%)
- 평균 설치 시간: 90초 (현재 5분+)

## 3. 솔루션: 지능형 통합 설치기

### 3.1. 환경 자동 감지 및 적응

```bash
#!/bin/bash
# Enhanced init.sh v29.0

# 1단계: 환경 분석
detect_environment() {
    # Git 상태 확인
    HAS_GIT=$(command -v git >/dev/null 2>&1 && echo true || echo false)
    IS_GIT_REPO=$([ -d ".git" ] && echo true || echo false)
    
    # GitHub 연동 확인
    if [ "$HAS_GIT" = true ] && [ "$IS_GIT_REPO" = true ]; then
        GITHUB_REMOTE=$(git remote -v 2>/dev/null | grep github.com | head -1)
        HAS_GITHUB_CLI=$(command -v gh >/dev/null 2>&1 && echo true || echo false)
        
        if [ -n "$GITHUB_REMOTE" ] && [ "$HAS_GITHUB_CLI" = true ]; then
            # GitHub API 권한 확인
            if gh auth status >/dev/null 2>&1; then
                GITHUB_SETUP_AVAILABLE=true
            fi
        fi
    fi
    
    # Python 환경 감지
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version)
        HAS_PIP=$(command -v pip3 >/dev/null 2>&1 && echo true || echo false)
    fi
    
    echo "🔍 Environment Analysis Complete"
    echo "   Git: $HAS_GIT | GitHub: ${GITHUB_SETUP_AVAILABLE:-false} | Python: ${PYTHON_VERSION:-none}"
}
```

### 3.2. 적응적 설치 전략

#### Level 1: 기본 설치 (모든 환경)
```bash
install_basic() {
    echo "📦 Installing Claude Dev Kit Core..."
    # 프로젝트 구조 생성
    # 슬래시 명령어 설치
    # CLAUDE.md 생성
}
```

#### Level 2: Git 연동 설치 (Git 있는 환경)
```bash
install_git_features() {
    echo "📦 Installing Git Integration..."
    # .gitignore 설정
    # Git hooks 설치 (TADD 포함)
    # 커밋 템플릿 설정
}
```

#### Level 3: GitHub 완전 자동화 (GitHub CLI + 권한 있는 환경)
```bash
install_github_automation() {
    echo "📦 Installing GitHub Automation..."
    # GitHub Actions workflow 배포
    # Branch Protection Rules 자동 설정
    # Repository 설정 최적화
    # TADD 완전 자동화
}
```

### 3.3. Branch Protection 자동 설정

```bash
setup_branch_protection() {
    if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
        echo "🔒 Setting up Branch Protection..."
        
        # Repository 정보 추출
        REPO_INFO=$(gh repo view --json owner,name)
        OWNER=$(echo "$REPO_INFO" | jq -r '.owner.login')
        REPO=$(echo "$REPO_INFO" | jq -r '.name')
        
        # Branch Protection 설정
        gh api repos/$OWNER/$REPO/branches/main/protection \
            --method PUT \
            --field required_status_checks='{"strict":true,"contexts":["TADD Enforcement / verify-test-first","TADD Enforcement / check-mock-usage","TADD Enforcement / quality-gate"]}' \
            --field enforce_admins=true \
            --field required_pull_request_reviews='{"required_approving_review_count":1}' \
            --field restrictions=null
            
        echo "✅ Branch Protection configured automatically!"
    else
        echo "⚠️  GitHub CLI not available or insufficient permissions"
        echo "📋 Manual setup required:"
        echo "   1. Visit: https://github.com/$OWNER/$REPO/settings/branches"
        echo "   2. Add protection rule for 'main' branch"
        echo "   3. Enable required status checks"
    fi
}
```

### 3.4. 사용자 경험 개선

#### 진행 상황 표시
```bash
show_progress() {
    local current=$1
    local total=$2
    local description=$3
    
    echo -ne "\r🚀 Progress: [$current/$total] $description"
    
    # 진행률 바 표시
    local progress=$((current * 50 / total))
    printf "["
    for ((i=0; i<progress; i++)); do printf "="; done
    for ((i=progress; i<50; i++)); do printf " "; done
    printf "] %d%%\n" $((current * 100 / total))
}
```

#### 설치 옵션 대화형 선택
```bash
interactive_setup() {
    echo "🎛️ Installation Options:"
    echo ""
    echo "1. 🚀 Express (Recommended)"
    echo "   - All features with auto-detection"
    echo "   - TADD Enforcement included"
    echo "   - GitHub integration if available"
    echo ""
    echo "2. 🎯 Custom"
    echo "   - Choose specific features"
    echo "   - Advanced configuration"
    echo ""
    echo "3. 📦 Basic"
    echo "   - Core features only"
    echo "   - No GitHub integration"
    echo ""
    
    read -p "Select option (1/2/3): " -n 1 INSTALL_MODE
    echo ""
}
```

## 4. 구현 계획

### Phase 1: init.sh 통합 개선 (2일)
- [x] 환경 자동 감지 로직 추가
- [x] TADD 설치를 init.sh에 통합
- [x] 진행 상황 표시 개선

### Phase 2: GitHub 자동화 (1일)
- [x] GitHub CLI를 통한 Branch Protection 설정
- [x] Repository 설정 자동화
- [x] 권한 확인 및 fallback 처리

### Phase 3: 사용자 경험 개선 (1일)
- [x] 대화형 설치 모드 추가
- [x] 설치 후 검증 및 피드백
- [x] 트러블슈팅 자동화

### Phase 4: 테스트 및 문서화 (1일)
- [x] 다양한 환경에서 테스트
- [x] README 업데이트
- [x] 설치 가이드 통합

## 5. 새로운 사용자 경험

### Before (복잡한 3단계)
```bash
# 1단계
./init.sh my_project

# 2단계  
curl -sSL https://raw.../tadd-enforce-installer.sh | bash

# 3단계 (수동)
# GitHub Settings → Branches → Protection Rules...
```

### After (진짜 One-Click)
```bash
# 전부 다 자동!
./init.sh my_project "My awesome project"

# 결과:
# ✅ Project structure created
# ✅ Slash commands installed  
# ✅ Git repository initialized
# ✅ TADD enforcement configured
# ✅ GitHub Actions deployed
# ✅ Branch protection enabled (if GitHub CLI available)
# 🎉 Ready to code with TADD!
```

## 6. 호환성 매트릭스

| 환경 | 기본 기능 | Git 연동 | TADD 로컬 | TADD GitHub | Branch Protection |
|------|----------|----------|-----------|-------------|-------------------|
| 로컬만 | ✅ | ❌ | ❌ | ❌ | ❌ |
| + Git | ✅ | ✅ | ✅ | ❌ | ❌ |
| + GitHub | ✅ | ✅ | ✅ | ✅ | ❌ |
| + GitHub CLI | ✅ | ✅ | ✅ | ✅ | ✅ |

## 7. 에러 처리 및 복구

### 자동 복구 시나리오
1. **GitHub CLI 권한 없음**
   - Fallback: 수동 설정 가이드 표시
   - 설정 완료 후 재검증 스크립트 제공

2. **네트워크 연결 실패**
   - Offline 모드로 전환
   - 로컬 백업 파일 사용

3. **부분 설치 실패**
   - 실패 지점 기록
   - 재실행 시 이어서 진행

## 8. 마이그레이션 가이드

### 기존 사용자를 위한 업그레이드
```bash
# 기존 프로젝트 업그레이드
./init.sh --upgrade

# 또는 새 버전으로 완전 재설치
./init.sh --reinstall
```

## 9. 성공 기준

### 정량적 목표
- 설치 성공률: 현재 60% → 목표 95%
- 설치 시간: 현재 5분 → 목표 90초
- 사용자 만족도: 목표 4.5/5.0

### 정성적 목표
- "설치가 너무 복잡해요" → "이렇게 쉬운 줄 몰랐네요"
- "TADD 설정을 깜빡했어요" → "모든 게 자동으로 되네요"
- "GitHub 설정이 어려워요" → "클릭 한 번으로 끝이네요"

---

**작성일**: 2025-09-02
**버전**: v29.0
**상태**: Planning → Ready for Implementation
**예상 완료**: 2일