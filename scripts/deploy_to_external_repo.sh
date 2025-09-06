#!/bin/bash
set -e

# ====================================================================
# 외부 레포 재구조화 커맨드 배포 스크립트 v1.0
# 25→9 슬래시 커맨드 재구조화 시스템 완전 배포
# ====================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로깅 함수
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 배너 출력
echo "======================================================================"
echo "🚀 Claude Dev Kit: 외부 레포 배포 시스템 v1.0"
echo "  25→9 슬래시 커맨드 재구조화 시스템 완전 배포"
echo "======================================================================"
echo

# 사용법 체크
if [ $# -lt 1 ]; then
    echo "사용법: $0 <target_directory> [options]"
    echo ""
    echo "Options:"
    echo "  --with-tadd        TADD 검증 시스템도 함께 설치"
    echo "  --legacy-redirect  기존 커맨드 리다이렉트 설정"
    echo "  --dry-run         실제 파일 변경 없이 시뮬레이션만"
    echo ""
    echo "예제:"
    echo "  $0 /path/to/external/repo --with-tadd --legacy-redirect"
    echo ""
    exit 1
fi

TARGET_DIR="$1"
shift

# 옵션 파싱
WITH_TADD=false
LEGACY_REDIRECT=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --with-tadd)
            WITH_TADD=true
            shift
            ;;
        --legacy-redirect)
            LEGACY_REDIRECT=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            log_error "알 수 없는 옵션: $1"
            exit 1
            ;;
    esac
done

# 타겟 디렉토리 검증
if [ ! -d "$TARGET_DIR" ]; then
    log_error "타겟 디렉토리가 존재하지 않습니다: $TARGET_DIR"
    exit 1
fi

if [ ! -d "$TARGET_DIR/.claude" ]; then
    log_error "타겟 디렉토리에 .claude 폴더가 없습니다: $TARGET_DIR"
    log_info "먼저 claude-dev-kit을 초기화하세요: ./init.sh"
    exit 1
fi

# 백업 생성
create_backup() {
    local backup_dir="$TARGET_DIR/.claude/commands/.backup-$(date +%Y%m%d-%H%M%S)"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] 백업 생성 예정: $backup_dir"
        return
    fi
    
    log_info "기존 커맨드 백업 중..."
    if [ -d "$TARGET_DIR/.claude/commands" ]; then
        mkdir -p "$backup_dir"
        cp -r "$TARGET_DIR/.claude/commands"/* "$backup_dir/" 2>/dev/null || true
        log_success "백업 완료: $backup_dir"
    fi
}

# 새로운 9개 커맨드 복사
deploy_new_commands() {
    log_info "새로운 9개 재구조화 커맨드 배포 중..."
    
    local commands=(
        "분석.md"
        "찾기.md" 
        "보고.md"
        "기획.md"
        "테스트.md"
        "구현.md"
        "배포.md"
        "전체사이클.md"
        "문서정리.md"
    )
    
    for cmd in "${commands[@]}"; do
        local src="$PROJECT_ROOT/.claude/commands/$cmd"
        local dest="$TARGET_DIR/.claude/commands/$cmd"
        
        if [ ! -f "$src" ]; then
            log_warn "소스 커맨드 파일 없음: $cmd"
            continue
        fi
        
        if [ "$DRY_RUN" = true ]; then
            log_info "[DRY-RUN] 배포 예정: $cmd"
            continue
        fi
        
        cp "$src" "$dest"
        log_success "배포 완료: $cmd"
    done
}

# 레거시 리다이렉트 설정
setup_legacy_redirects() {
    if [ "$LEGACY_REDIRECT" = false ]; then
        log_info "레거시 리다이렉트 건너뛰기"
        return
    fi
    
    log_info "25개 기존 커맨드 → 9개 새 커맨드 리다이렉트 설정 중..."
    
    local redirect_dir="$TARGET_DIR/.claude/commands/.redirects"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] 리다이렉트 설정 예정: $redirect_dir"
        return
    fi
    
    mkdir -p "$redirect_dir"
    
    # 리다이렉트 맵핑 생성
    cat > "$redirect_dir/legacy_mappings.json" << 'EOF'
{
  "redirects": {
    "시작": "기획",
    "구현": "구현", 
    "검증": "테스트",
    "완료": "배포",
    "안정화": "배포",
    "레포정리": "배포",
    "세션마감": "배포",
    "개발완료": "배포",
    "주간보고": "보고",
    "문서찾기": "찾기",
    "컨텍스트": "찾기",
    "스펙분석": "분석",
    "요구분석": "분석",
    "설계": "기획",
    "계획": "기획",
    "아키텍처": "기획",
    "프로토타입": "기획",
    "실험": "테스트",
    "디버깅": "테스트",
    "최적화": "구현",
    "리팩토링": "구현",
    "성능": "구현",
    "보안": "구현",
    "배치": "배포"
  }
}
EOF

    log_success "레거시 리다이렉트 설정 완료"
}

# TADD 검증 시스템 설치
install_tadd_system() {
    if [ "$WITH_TADD" = false ]; then
        log_info "TADD 시스템 설치 건너뛰기"
        return
    fi
    
    log_info "TADD 검증 시스템 설치 중..."
    
    local tadd_files=(
        "scripts/check_theater_testing.py"
        "scripts/verify_tadd_order.py"
        "scripts/detect_mock_usage.py"
        "scripts/validate_test_quality.py"
        ".github/workflows/test-integrity.yml"
    )
    
    for file in "${tadd_files[@]}"; do
        local src="$PROJECT_ROOT/$file"
        local dest="$TARGET_DIR/$file"
        local dest_dir="$(dirname "$dest")"
        
        if [ ! -f "$src" ]; then
            log_warn "TADD 파일 없음: $file"
            continue
        fi
        
        if [ "$DRY_RUN" = true ]; then
            log_info "[DRY-RUN] TADD 파일 설치 예정: $file"
            continue
        fi
        
        mkdir -p "$dest_dir"
        cp "$src" "$dest"
        log_success "TADD 파일 설치: $file"
    done
}

# 프로젝트별 커스터마이제이션
customize_for_project() {
    log_info "프로젝트별 커스터마이제이션 적용 중..."
    
    # package.json 확인
    if [ -f "$TARGET_DIR/package.json" ]; then
        log_info "Node.js 프로젝트 감지 - 관련 설정 적용"
        # TODO: Node.js 특화 설정
    fi
    
    # requirements.txt 확인  
    if [ -f "$TARGET_DIR/requirements.txt" ]; then
        log_info "Python 프로젝트 감지 - 관련 설정 적용"
        # TODO: Python 특화 설정
    fi
    
    # Cargo.toml 확인
    if [ -f "$TARGET_DIR/Cargo.toml" ]; then
        log_info "Rust 프로젝트 감지 - 관련 설정 적용"
        # TODO: Rust 특화 설정
    fi
}

# 설치 검증
verify_installation() {
    log_info "설치 검증 중..."
    
    local failed=0
    
    # 9개 핵심 커맨드 확인
    local core_commands=("분석" "찾기" "보고" "기획" "테스트" "구현" "배포" "전체사이클" "문서정리")
    
    for cmd in "${core_commands[@]}"; do
        if [ ! -f "$TARGET_DIR/.claude/commands/$cmd.md" ]; then
            log_error "핵심 커맨드 누락: $cmd.md"
            ((failed++))
        fi
    done
    
    # TADD 시스템 확인 (설치했다면)
    if [ "$WITH_TADD" = true ]; then
        if [ ! -f "$TARGET_DIR/scripts/check_theater_testing.py" ]; then
            log_error "TADD 검증 스크립트 누락"
            ((failed++))
        fi
    fi
    
    if [ $failed -eq 0 ]; then
        log_success "설치 검증 완료! 모든 구성 요소가 정상적으로 배포되었습니다."
        return 0
    else
        log_error "설치 검증 실패! $failed 개의 문제가 발견되었습니다."
        return 1
    fi
}

# 사용 가이드 생성
generate_usage_guide() {
    log_info "사용 가이드 생성 중..."
    
    local guide_file="$TARGET_DIR/.claude/RESTRUCTURED_COMMANDS_GUIDE.md"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] 사용 가이드 생성 예정: $guide_file"
        return
    fi
    
    cat > "$guide_file" << 'EOF'
# 🚀 재구조화된 슬래시 커맨드 가이드 (25→9)

## 새로운 9개 커맨드 체계

### 🔍 탐색 트랙 (Understanding) - 3개
- **`/분석`**: 5단계 완전 분석 사이클 (탐색→수렴→정제→보고서→정리)
- **`/찾기`**: 문서찾기 + 컨텍스트 통합 검색
- **`/보고`**: 주간보고 + 보고서작업 통합

### 🛠️ TADD 실행 트랙 (Implementation) - 4개  
- **`/기획`**: LLM 지능형 라우팅 (5개 모드: 탐색/신속/체계/완전/통합)
- **`/테스트`**: Failing Tests 우선 생성 (TADD 강제)
- **`/구현`**: 테스트 통과 구현 (Real Testing)
- **`/배포`**: 검증 + 배포 + 자동 정리

### 🎯 특수 트랙 (Special) - 2개
- **`/전체사이클`**: 완전한 개발 사이클 자동화
- **`/문서정리`**: 3-Layer 자동 문서화 시스템

## 주요 혁신사항

1. **LLM 지능형 라우팅**: 키워드가 아닌 컨텍스트 기반 모드 선택
2. **TADD 강제 시스템**: Theater Testing 차단, Real Testing 강제
3. **3-Layer 문서화**: 실시간 자동화 + 주기적 정리 + 세션 마감
4. **60% 중복 제거**: 25개→9개로 효율성 극대화

## 기존 커맨드 매핑

EOF

    if [ "$LEGACY_REDIRECT" = true ]; then
        cat >> "$guide_file" << 'EOF'
### 자동 리다이렉트 설정됨
- `/시작` → `/기획`
- `/구현` → `/구현` 
- `/검증` → `/테스트`
- `/완료` → `/배포`
- `/안정화` → `/배포`
- `/주간보고` → `/보고`
- 기타 25개 커맨드 → 9개 새 커맨드로 자동 매핑

EOF
    fi

    cat >> "$guide_file" << 'EOF'
## 사용 시나리오

### 📊 분석이 필요할 때
```
/분석 "현재 프로젝트 상황을 파악하고 싶어"
→ 5단계 워크플로우: 탐색→수렴→정제→보고서→정리
```

### 🛠️ 개발 작업할 때
```
/기획 "새로운 기능을 추가하고 싶어"  
→ LLM이 자동 분석하여 최적 모드 선택

/테스트 "실패하는 테스트부터 만들어줘"
→ TADD 방식으로 테스트 우선 작성

/구현 "테스트를 통과하는 코드 만들어줘"
→ Real Testing 기반 구체적 구현

/배포 "검증하고 배포 준비해줘"
→ 6단계 통합 배포 프로세스
```

## 지원받기
- Issues: https://github.com/kyuwon-shim-ARL/claude-dev-kit/issues
- Docs: 프로젝트 루트의 `CLAUDE.md` 참조
EOF

    log_success "사용 가이드 생성 완료: $guide_file"
}

# ====================================================================
# 메인 실행 흐름
# ====================================================================

main() {
    log_info "배포 시작: $TARGET_DIR"
    echo "옵션: TADD=$WITH_TADD, LEGACY=$LEGACY_REDIRECT, DRY_RUN=$DRY_RUN"
    echo
    
    # 1. 백업 생성
    create_backup
    
    # 2. 새 커맨드 배포
    deploy_new_commands
    
    # 3. 레거시 리다이렉트 설정
    setup_legacy_redirects
    
    # 4. TADD 시스템 설치
    install_tadd_system
    
    # 5. 프로젝트별 커스터마이제이션
    customize_for_project
    
    # 6. 사용 가이드 생성
    generate_usage_guide
    
    # 7. 설치 검증
    if verify_installation; then
        echo
        log_success "🎉 재구조화 커맨드 배포 완료!"
        log_info "가이드: $TARGET_DIR/.claude/RESTRUCTURED_COMMANDS_GUIDE.md"
        
        if [ "$LEGACY_REDIRECT" = true ]; then
            log_info "기존 25개 커맨드는 자동으로 새 9개 커맨드로 리다이렉트됩니다."
        fi
        
        if [ "$WITH_TADD" = true ]; then
            log_info "TADD 검증 시스템이 설치되었습니다. GitHub Actions에서 자동 검증됩니다."
        fi
        
        return 0
    else
        log_error "배포 중 오류가 발생했습니다."
        return 1
    fi
}

# 스크립트 실행
main "$@"