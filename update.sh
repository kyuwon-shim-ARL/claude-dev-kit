#!/bin/bash
# claude-dev-kit 업데이트 스크립트 v1.0
# 기존 설치된 프로젝트의 슬래시 명령어만 업데이트

set -e

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔄 Claude Dev Kit 업데이트 시작..."

# 1. 현재 디렉토리 확인
if [ ! -d ".claude/commands" ]; then
    echo -e "${RED}❌ 오류: .claude/commands 디렉토리가 없습니다.${NC}"
    echo "먼저 init.sh를 실행하여 초기 설치를 진행하세요."
    exit 1
fi

# 2. 백업 생성
echo "📦 기존 명령어 백업 중..."
BACKUP_DIR=".claude/commands.backup.$(date +%Y%m%d_%H%M%S)"
cp -r .claude/commands "$BACKUP_DIR"
echo -e "${GREEN}✅ 백업 완료: $BACKUP_DIR${NC}"

# 3. GitHub에서 최신 명령어 다운로드
echo "⬇️ 최신 명령어 다운로드 중..."

# GitHub Raw URL 기본 경로
BASE_URL="https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.claude/commands"

# Hybrid command mapping (GitHub uses English filenames)
declare -A COMMAND_MAPPING=(
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
    ["주간보고"]="weekly-report"
    ["문서정리"]="docsorg"
    ["레포정리"]="repoclean"
    ["세션마감"]="session-closure"
)

# 명령어 다운로드 (하이브리드 방식)
echo "Downloading commands with hybrid Korean/English support..."
for korean_cmd in "${!COMMAND_MAPPING[@]}"; do
    english_cmd="${COMMAND_MAPPING[$korean_cmd]}"
    echo -n "  $korean_cmd ($english_cmd) ... "
    
    # Download from GitHub (English filename)
    if curl -s -o ".tmp_download" "$BASE_URL/$english_cmd.md"; then
        # Check if it's a valid file (not error page)
        if ! grep -q "400 Bad request" ".tmp_download" && ! grep -q "404: Not Found" ".tmp_download" && [ -s ".tmp_download" ]; then
            # Force update: always overwrite existing files
            cp ".tmp_download" ".claude/commands/$korean_cmd.md"
            cp ".tmp_download" ".claude/commands/$english_cmd.md"
            rm -f ".tmp_download"
            echo -e "${GREEN}✓ (updated /$korean_cmd and /$english_cmd)${NC}"
        else
            rm -f ".tmp_download"
            echo -e "${RED}✗ (file not found or corrupted)${NC}"
        fi
    else
        echo -e "${RED}✗ (network error)${NC}"
    fi
done

# 4. 변경사항 확인
echo ""
echo "📋 업데이트된 항목:"
echo "-------------------"

# 주요 변경사항 하이라이트
if grep -q "compact" .claude/commands/배포.md 2>/dev/null; then
    echo -e "${GREEN}✅ 컨텍스트 관리 시스템 v8.0 적용됨${NC}"
    echo "   - /compact 템플릿 가이드 추가"
    echo "   - ZEDS와 시너지 효과 극대화"
    echo "   - 예상 감소율: 75-85%"
fi

# 5. 문서 구조 마이그레이션 (v13.0.0 신규)
echo ""
echo "📁 문서 구조 업데이트 확인 중..."

# project_rules.md 마이그레이션 (docs/specs/로 이동)
if [ -f "project_rules.md" ] && [ ! -f "docs/specs/project_rules.md" ]; then
    echo "📦 project_rules.md를 docs/specs/로 이동합니다..."
    mkdir -p docs/specs
    mv "project_rules.md" "docs/specs/project_rules.md"
    echo -e "${GREEN}✅ project_rules.md가 docs/specs/로 이동되었습니다${NC}"
elif [ -f "docs/specs/project_rules.md" ]; then
    echo -e "${GREEN}✓ project_rules.md가 이미 docs/specs/에 있습니다${NC}"
fi

# 6. GitHub Actions 업데이트 확인 (v25.3.0 신규)
echo ""
echo "🔍 GitHub Actions TADD 강제 시스템 확인 중..."

GITHUB_ACTIONS_UPDATED=false
TADD_SCRIPTS_UPDATED=false

if [ -d ".github/workflows" ]; then
    echo -e "${GREEN}✓ .github/workflows 디렉토리 발견${NC}"
    
    # TADD enforcement workflow 확인
    if [ -f ".github/workflows/tadd-enforcement.yml" ]; then
        echo "  📊 기존 TADD enforcement 워크플로우 발견"
        echo "  ⚡ 최신 버전으로 업데이트하시겠습니까? (기존 파일은 백업됩니다)"
        
        if [ -t 0 ]; then
            read -p "  GitHub Actions 업데이트? (y/n): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # 백업 생성
                cp ".github/workflows/tadd-enforcement.yml" ".github/workflows/tadd-enforcement.yml.backup.$(date +%Y%m%d_%H%M%S)"
                echo "  📦 백업 완료"
                
                # 최신 버전 다운로드
                curl -s -o ".github/workflows/tadd-enforcement.yml" \
                    "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.github/workflows/tadd-enforcement.yml"
                echo -e "  ${GREEN}✅ GitHub Actions 업데이트 완료${NC}"
                GITHUB_ACTIONS_UPDATED=true
            fi
        fi
    else
        echo "  ⚠️  TADD enforcement 워크플로우가 없습니다"
        echo "  💡 새로 설치하시겠습니까?"
        
        if [ -t 0 ]; then
            read -p "  TADD 강제 시스템 설치? (y/n): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                curl -s -o ".github/workflows/tadd-enforcement.yml" \
                    "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/.github/workflows/tadd-enforcement.yml"
                echo -e "  ${GREEN}✅ TADD 강제 시스템 설치 완료${NC}"
                GITHUB_ACTIONS_UPDATED=true
            fi
        fi
    fi
else
    echo "  ℹ️  .github/workflows 디렉토리가 없습니다"
    echo "  💡 GitHub Actions를 사용하려면 GitHub에 푸시 후 자동 활성화됩니다"
fi

# TADD 검증 스크립트 업데이트
echo ""
echo "📋 TADD 검증 스크립트 확인 중..."

# 스크립트 디렉토리 생성
mkdir -p scripts

# 각 스크립트 업데이트 또는 설치
for script in "verify_tadd_order.py" "detect_mock_usage.py" "quick_tadd_check.sh"; do
    if [ -f "scripts/$script" ]; then
        echo "  ✓ scripts/$script 발견 - 최신 버전으로 업데이트"
        cp "scripts/$script" "scripts/$script.backup.$(date +%Y%m%d_%H%M%S)"
    else
        echo "  + scripts/$script 새로 설치"
    fi
    
    curl -s -o "scripts/$script" \
        "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/$script"
    
    if [ "$script" = "quick_tadd_check.sh" ]; then
        chmod +x "scripts/$script"
    fi
done

echo -e "${GREEN}✅ TADD 검증 스크립트 업데이트 완료${NC}"
TADD_SCRIPTS_UPDATED=true

# 7. 선택적 업데이트
echo ""
echo -e "${YELLOW}📌 선택적 업데이트 항목:${NC}"
echo ""
echo "다음 파일들도 업데이트하시겠습니까? (y/n)"
echo "  - docs/specs/PRD-template.md (PRD 템플릿)"
echo "  - CLAUDE.md (프로젝트 설명서)"
echo ""

# stdin이 파이프인 경우 기본값 사용
if [ -t 0 ]; then
    read -p "업데이트 하시겠습니까? (y/n): " -n 1 -r
    echo ""
else
    echo "자동 모드: 명령어만 업데이트합니다."
    REPLY="n"
fi

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # PRD 템플릿 업데이트
    if [ ! -f "docs/specs/PRD-template.md" ]; then
        echo "📝 PRD 템플릿 생성 중..."
        mkdir -p docs/specs
        curl -s -o "docs/specs/PRD-template.md" \
            "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/docs/specs/PRD-template.md"
        echo -e "${GREEN}✅ 템플릿 생성됨: docs/specs/PRD-template.md${NC}"
    else
        echo "⚠️  PRD-template.md가 이미 존재합니다."
    fi
fi

# 7. 버전 정보 저장
echo "v13.0.0 - $(date)" > .claude/.version

# 8. 완료 메시지
echo ""
echo "========================================="
echo -e "${GREEN}✅ 업데이트 완료!${NC}"
echo "========================================="
echo ""
echo "📋 업데이트된 항목:"

# 슬래시 명령어 업데이트 표시
echo "  ✓ 슬래시 명령어 최신화"

# GitHub Actions 업데이트 표시
if [ "$GITHUB_ACTIONS_UPDATED" = true ]; then
    echo "  ✓ GitHub Actions TADD 강제 시스템 업데이트"
fi

# TADD 스크립트 업데이트 표시
if [ "$TADD_SCRIPTS_UPDATED" = true ]; then
    echo "  ✓ TADD 검증 스크립트 최신화"
fi

# PRD 관련 기능
echo "  ✓ PRD 자동 분해 시스템 (v13.0)"
echo "  ✓ docs/specs/ 통합 사양서 관리"
echo ""
echo "💡 새로운 사용법:"

# GitHub Actions 관련 안내
if [ "$GITHUB_ACTIONS_UPDATED" = true ]; then
    echo "  🚀 TADD 강제 시스템:"
    echo "     - GitHub에 푸시하면 자동으로 모든 PR 검증"
    echo "     - 테스트 우선 작성 강제 (AI도 회피 불가)"
    echo "     - Mock 사용률 20% 이하 자동 강제"
    echo ""
fi

# TADD 스크립트 관련 안내
if [ "$TADD_SCRIPTS_UPDATED" = true ]; then
    echo "  📊 로컬 TADD 검증:"
    echo "     - ./scripts/quick_tadd_check.sh (빠른 체크)"
    echo "     - python scripts/verify_tadd_order.py (순서 검증)"
    echo "     - python scripts/detect_mock_usage.py (Mock 분석)"
    echo ""
fi

echo '  📝 PRD 기반 개발:'
echo '     1. PRD를 docs/specs/PRD-v1.0.md에 작성'
echo '     2. /기획 실행 시 자동으로 requirements.md, architecture.md 생성'
echo ""
echo "🔄 롤백이 필요한 경우:"
echo "  - 슬래시 명령어: cp -r $BACKUP_DIR/* .claude/commands/"
if [ "$GITHUB_ACTIONS_UPDATED" = true ]; then
    echo "  - GitHub Actions: .github/workflows/*.backup.* 파일 복원"
fi
if [ "$TADD_SCRIPTS_UPDATED" = true ]; then
    echo "  - TADD 스크립트: scripts/*.backup.* 파일 복원"
fi
echo ""
echo "📖 자세한 내용:"
echo "  https://github.com/kyuwon-shim-ARL/claude-dev-kit/releases/latest"