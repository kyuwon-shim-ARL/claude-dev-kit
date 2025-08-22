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

# 다운로드할 명령어 목록 (v8.0 기준)
COMMANDS=(
    "기획.md"
    "구현.md"
    "안정화.md"
    "배포.md"
    "전체사이클.md"
    "문서화.md"
    "배포문서.md"
    "분석.md"
)

# 명령어 다운로드
for cmd in "${COMMANDS[@]}"; do
    echo -n "  $cmd ... "
    if curl -s -o ".claude/commands/$cmd" "$BASE_URL/$cmd"; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
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

# 5. 선택적 업데이트
echo ""
echo -e "${YELLOW}📌 선택적 업데이트 항목:${NC}"
echo ""
echo "다음 파일들도 업데이트하시겠습니까? (y/n)"
echo "  - project_rules.md (프로젝트 규칙)"
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
    # project_rules.md 업데이트 (템플릿만 제공)
    if [ ! -f "project_rules.md" ]; then
        echo "📝 project_rules.md 템플릿 생성 중..."
        curl -s -o "project_rules.template.md" \
            "https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/project_rules.md"
        echo -e "${GREEN}✅ 템플릿 생성됨: project_rules.template.md${NC}"
        echo "   필요에 따라 수정 후 project_rules.md로 저장하세요."
    else
        echo "⚠️  project_rules.md가 이미 존재합니다. 수동 업데이트를 권장합니다."
    fi
fi

# 6. 버전 정보 저장
echo "v9.0.0 - $(date)" > .claude/.version

# 7. 완료 메시지
echo ""
echo "========================================="
echo -e "${GREEN}✅ 업데이트 완료!${NC}"
echo "========================================="
echo ""
echo "📋 다음 기능이 추가되었습니다:"
echo "  1. 동적 컨텍스트 가이드 생성 (v9.0)"
echo "  2. Claude가 실시간 작업 분석"
echo "  3. 템플릿 제약 제거, 85-95% 압축률"
echo ""
echo "💡 사용 예시:"
echo '  배포 후: /compact "v1.0.0 배포 완료. ZEDS 문서 보존됨. 구현 과정 제거"'
echo ""
echo "🔄 롤백이 필요한 경우:"
echo "  cp -r $BACKUP_DIR/* .claude/commands/"
echo ""
echo "📖 자세한 내용:"
echo "  https://github.com/kyuwon-shim-ARL/claude-dev-kit/releases/tag/v9.0.0"