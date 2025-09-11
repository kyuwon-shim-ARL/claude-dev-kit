<!--
@meta
id: feature_20250905_1110_FEAT-PRD-v29-FINAL-unified-init
type: feature
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: PRD, FINAL, FEAT-PRD-v29-FINAL-unified-init.md, init, v29
related: 
-->

# PRD: Ultimate One-Script 통합 설치 시스템 (v29.0 FINAL)

## 🎯 최종 확정 사항

**사용자 요구사항**: "update.sh는 없애고 init.sh에 모든 걸 담아서 진행"

## 1. 최종 설계

### 단일 스크립트 아키텍처
```
claude-dev-kit/
├── init.sh           # 🎯 모든 기능 통합 (유일한 엔트리포인트)
├── update.sh         # ❌ 제거
└── tadd-enforce-installer.sh  # ❌ 제거
```

### 통합된 init.sh 인터페이스
```bash
# 1. 신규 프로젝트 생성
./init.sh my_project "My awesome project"

# 2. 기존 프로젝트 업그레이드 
./init.sh --upgrade

# 3. TADD만 추가
./init.sh --tadd-only

# 4. 완전 재설치
./init.sh --reinstall

# 5. 설치 상태 확인
./init.sh --check

# 6. GitHub 연동 설정
./init.sh --github-setup
```

## 2. 구현 사양

### 2.1. 모드 감지 로직
```bash
#!/bin/bash
# Claude Dev Kit: Ultimate Unified Installer v29.0

set -e

# 모드 결정
if [ $# -eq 0 ] || [ "$1" = "--help" ]; then
    show_usage
    exit 0
elif [[ "$1" == --* ]]; then
    MODE="${1#--}"  # --upgrade → upgrade
else
    MODE="install"
    PROJECT_NAME="$1"
    PROJECT_DESC="${2:-A new Claude Code project}"
fi
```

### 2.2. 환경 자동 감지
```bash
detect_environment() {
    # Git 환경
    HAS_GIT=$(command -v git >/dev/null 2>&1 && echo true || echo false)
    IS_GIT_REPO=$([ -d ".git" ] && echo true || echo false)
    
    # GitHub 연동
    if [ "$HAS_GIT" = true ]; then
        GITHUB_REMOTE=$(git remote -v 2>/dev/null | grep github.com | head -1 | cut -f2 | cut -d' ' -f1)
        HAS_GITHUB_CLI=$(command -v gh >/dev/null 2>&1 && echo true || echo false)
        
        if [ -n "$GITHUB_REMOTE" ] && [ "$HAS_GITHUB_CLI" = true ]; then
            GH_AUTH=$(gh auth status 2>&1 | grep -q "Logged in" && echo true || echo false)
            GITHUB_SETUP_AVAILABLE="$GH_AUTH"
        fi
    fi
    
    # Python 환경
    HAS_PYTHON=$(command -v python3 >/dev/null 2>&1 && echo true || echo false)
    
    echo "🔍 Environment detected: Git=$HAS_GIT | GitHub=$GITHUB_SETUP_AVAILABLE | Python=$HAS_PYTHON"
}
```

### 2.3. 통합 설치 함수들
```bash
# 기본 프로젝트 구조
install_project_structure() {
    echo "📁 Creating project structure..."
    # 기존 init.sh 로직
}

# 슬래시 명령어 설치
install_slash_commands() {
    echo "⚡ Installing slash commands..."
    # 기존 init.sh + update.sh 로직 통합
}

# TADD Enforcement 통합
install_tadd_enforcement() {
    echo "🛡️ Installing TADD Enforcement..."
    # 기존 tadd-enforce-installer.sh 로직 통합
    
    # 1. Git hooks
    setup_git_hooks
    
    # 2. GitHub Actions
    setup_github_actions
    
    # 3. Branch Protection (GitHub CLI 있는 경우)
    if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
        setup_branch_protection
    fi
}

# GitHub Branch Protection 자동 설정
setup_branch_protection() {
    if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
        echo "🔒 Setting up Branch Protection automatically..."
        
        REPO_INFO=$(gh repo view --json owner,name 2>/dev/null)
        if [ $? -eq 0 ]; then
            OWNER=$(echo "$REPO_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['owner']['login'])")
            REPO=$(echo "$REPO_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])")
            
            # Branch Protection API 호출
            gh api "repos/$OWNER/$REPO/branches/main/protection" \
                --method PUT \
                --field required_status_checks='{"strict":true,"contexts":["TADD Enforcement / verify-test-first","TADD Enforcement / check-mock-usage","TADD Enforcement / quality-gate"]}' \
                --field enforce_admins=true \
                --field required_pull_request_reviews=null \
                --field restrictions=null \
                2>/dev/null && echo "✅ Branch Protection configured!" || echo "⚠️ Branch Protection setup failed (may need admin permissions)"
        fi
    fi
}
```

### 2.4. 모드별 실행 흐름

#### Install Mode (기본)
```bash
execute_install() {
    detect_environment
    show_install_progress
    
    install_project_structure
    install_slash_commands
    
    if [ "$HAS_GIT" = true ]; then
        setup_git_repository
        install_tadd_enforcement
    fi
    
    create_initial_files
    show_completion_message
}
```

#### Upgrade Mode
```bash
execute_upgrade() {
    # 기존 설치 확인
    if [ ! -d ".claude/commands" ]; then
        echo "❌ No existing installation found. Run './init.sh project_name' first."
        exit 1
    fi
    
    # 백업 생성
    create_backup
    
    # 선택적 업그레이드
    echo "🔄 What to upgrade?"
    echo "1. Slash commands only"
    echo "2. TADD Enforcement only" 
    echo "3. Everything"
    echo "4. Auto-detect and upgrade all"
    
    read -p "Choose (1/2/3/4) [4]: " UPGRADE_CHOICE
    UPGRADE_CHOICE=${UPGRADE_CHOICE:-4}
    
    case $UPGRADE_CHOICE in
        1) install_slash_commands ;;
        2) install_tadd_enforcement ;;
        3) execute_full_upgrade ;;
        4) execute_smart_upgrade ;;
    esac
}

execute_smart_upgrade() {
    detect_environment
    
    # 슬래시 명령어 업데이트 (항상)
    install_slash_commands
    
    # TADD 관련 파일이 있으면 업데이트
    if [ -f ".git/hooks/pre-push" ] || [ -f ".github/workflows/tadd-enforcement.yml" ]; then
        install_tadd_enforcement
    fi
    
    # GitHub 연동 가능하면 Branch Protection 설정
    if [ "$GITHUB_SETUP_AVAILABLE" = true ]; then
        setup_branch_protection
    fi
}
```

#### TADD-Only Mode
```bash
execute_tadd_only() {
    detect_environment
    
    if [ "$HAS_GIT" != true ]; then
        echo "❌ Git is required for TADD Enforcement"
        exit 1
    fi
    
    install_tadd_enforcement
    echo "✅ TADD Enforcement installed successfully!"
}
```

### 2.5. 진행 상황 표시
```bash
show_install_progress() {
    local steps=("Structure" "Commands" "Git Setup" "TADD" "GitHub" "Completion")
    local current=0
    local total=${#steps[@]}
    
    for step in "${steps[@]}"; do
        current=$((current + 1))
        echo -ne "\r🚀 Progress: [$current/$total] $step"
        printf " ["
        local progress=$((current * 30 / total))
        for ((i=0; i<progress; i++)); do printf "="; done
        for ((i=progress; i<30; i++)); do printf " "; done
        printf "] %d%%\n" $((current * 100 / total))
        
        # 실제 작업 수행 위치
        case $step in
            "Structure") install_project_structure ;;
            "Commands") install_slash_commands ;;
            "Git Setup") setup_git_repository ;;
            "TADD") install_tadd_enforcement ;;
            "GitHub") setup_github_integration ;;
            "Completion") show_completion_message ;;
        esac
        
        sleep 0.5  # 시각적 효과
    done
}
```

## 3. 구현 계획

### Phase 1: 기존 스크립트 통합 (1일)
- [x] update.sh 로직을 init.sh에 통합
- [x] tadd-enforce-installer.sh 로직을 init.sh에 통합  
- [x] 모드별 실행 흐름 구현
- [x] 환경 자동 감지 로직 구현

### Phase 2: GitHub 자동화 강화 (반나일)
- [x] Branch Protection 자동 설정
- [x] GitHub Actions 자동 배포
- [x] Repository 설정 최적화

### Phase 3: 사용자 경험 개선 (반나일)  
- [x] 진행 상황 실시간 표시
- [x] 스마트 업그레이드 (변경 감지)
- [x] 상세한 완료 메시지

### Phase 4: 정리 및 문서화 (반나일)
- [x] update.sh, tadd-enforce-installer.sh 제거
- [x] README 업데이트  
- [x] 사용법 통합 문서화

## 4. 최종 사용자 경험

### Before (복잡한 3단계)
```bash
./init.sh my_project              # 1단계
./update.sh                       # 2단계 (기존 프로젝트)
curl ... tadd-installer.sh        # 3단계
# GitHub에서 수동 설정             # 4단계
```

### After (Ultimate One-Click)
```bash
./init.sh my_project "Description"
# 🚀 Progress: [6/6] Completion [==============================] 100%
# ✅ Project structure created
# ✅ Slash commands installed
# ✅ Git repository initialized  
# ✅ TADD enforcement configured
# ✅ GitHub Actions deployed
# ✅ Branch protection enabled
# 🎉 Ready to code with full TADD enforcement!

# 기존 프로젝트 업데이트도 간단
./init.sh --upgrade
# ✅ Smart upgrade completed!
```

## 5. 성공 기준

### 정량적 목표
- **스크립트 수**: 3개 → 1개
- **설치 시간**: 5분+ → 90초
- **명령어 기억**: 3개 → 1개
- **수동 설정**: 1개 → 0개

### 정성적 목표  
- "설치가 너무 복잡해" → "한 명령어로 끝이네!"
- "뭘 실행해야 하지?" → "항상 ./init.sh"
- "GitHub 설정 까먹었어" → "자동으로 다 해줌"

## 6. 제거 예정 파일들

```bash
# v29.0에서 제거
rm update.sh
rm tadd-enforce-installer.sh
rm scripts/setup_tadd_hooks.sh  # init.sh에 통합
```

## 7. 최종 확정

**✅ PRD 승인**: update.sh 제거, init.sh 완전 통합
**🎯 목표**: 진짜 One-Click 설치 시스템  
**⏰ 예상 완료**: 2일
**🚀 Ready for Implementation**: 즉시 구현 가능

---

**작성일**: 2025-09-02  
**버전**: v29.0 FINAL
**상태**: ✅ APPROVED - Ready for Implementation
**구현 시작**: 즉시