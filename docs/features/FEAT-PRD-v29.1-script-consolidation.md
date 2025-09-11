<!--
@meta
id: feature_20250905_1110_FEAT-PRD-v29.1-script-consolidation
type: feature
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: v29.1, PRD, consolidation, script, FEAT
related: 
-->

# PRD: 설치 스크립트 통합 전략 (v29.1)

## 1. 현재 상황 분석

### 기존 스크립트들의 역할
| 스크립트 | 현재 역할 | 사용 시점 | 타겟 |
|----------|----------|----------|-------|
| `init.sh` | 신규 프로젝트 초기화 | 프로젝트 생성 시 | 새 프로젝트 |
| `update.sh` | 슬래시 명령어만 업데이트 | 기존 프로젝트 업데이트 | 기존 프로젝트 |
| `tadd-enforce-installer.sh` | TADD만 설치 | TADD 추가 시 | 모든 프로젝트 |

### 문제점
- **3개 스크립트로 분산**: 사용자 혼란
- **기능 중복**: 모두 GitHub에서 파일 다운로드
- **불완전한 업데이트**: update.sh는 슬래시 명령어만 업데이트

## 2. 통합 전략

### Option A: update.sh 완전 제거 (추천)
```bash
# Before (3개)
./init.sh my_project              # 신규
./update.sh                       # 기존 업데이트  
./tadd-enforce-installer.sh       # TADD 추가

# After (1개 + 옵션)
./init.sh my_project              # 신규 설치
./init.sh --upgrade               # 기존 업데이트
./init.sh --tadd-only            # TADD만 추가
```

### Option B: update.sh 유지하되 심링크로 통합
```bash
# update.sh → init.sh --upgrade 심링크
ln -s init.sh update.sh

# 사용자는 기존대로 사용 가능
./update.sh  # 실제로는 ./init.sh --upgrade 실행
```

## 3. 새로운 init.sh 통합 설계

### 3.1. 명령어 옵션 체계
```bash
#!/bin/bash
# Enhanced init.sh v29.1

# 사용법
show_usage() {
    echo "🚀 Claude Dev Kit Universal Installer v29.1"
    echo ""
    echo "Usage:"
    echo "  $0 [PROJECT_NAME] [DESCRIPTION]     # 신규 프로젝트 생성"
    echo "  $0 --upgrade                        # 기존 프로젝트 업그레이드"
    echo "  $0 --tadd-only                     # TADD Enforcement만 설치"
    echo "  $0 --reinstall                     # 완전 재설치"
    echo "  $0 --check                         # 설치 상태 확인"
    echo ""
    echo "Options:"
    echo "  --force         # 확인 없이 강제 실행"
    echo "  --no-github     # GitHub 연동 비활성화"
    echo "  --offline       # 오프라인 모드 (로컬 파일 사용)"
    echo ""
}
```

### 3.2. 모드별 동작

#### 신규 설치 모드
```bash
if [ $# -ge 1 ] && [[ "$1" != --* ]]; then
    MODE="install"
    PROJECT_NAME="$1"
    PROJECT_DESC="${2:-A new Claude Code project}"
fi
```

#### 업그레이드 모드 (기존 update.sh 기능 통합)
```bash
if [ "$1" = "--upgrade" ]; then
    MODE="upgrade"
    
    # 기존 프로젝트 확인
    if [ ! -d ".claude/commands" ]; then
        echo "❌ 기존 설치가 없습니다. 먼저 ./init.sh를 실행하세요."
        exit 1
    fi
    
    # 백업 생성 (기존 update.sh 로직)
    create_backup
    
    # 선택적 업데이트
    echo "🔄 업데이트할 항목을 선택하세요:"
    echo "1. 슬래시 명령어만"
    echo "2. TADD Enforcement 포함"
    echo "3. 모든 구성요소"
    
    read -p "선택 (1/2/3): " UPDATE_SCOPE
fi
```

#### TADD 전용 모드
```bash
if [ "$1" = "--tadd-only" ]; then
    MODE="tadd_only"
    
    # 기존 tadd-enforce-installer.sh 로직 통합
    install_tadd_enforcement
fi
```

### 3.3. 백워드 호환성

#### update.sh를 심링크로 유지
```bash
# 설치 시 자동 생성
create_symlinks() {
    if [ ! -f "update.sh" ]; then
        ln -s init.sh update.sh
        echo "📎 update.sh → init.sh 심링크 생성"
    fi
}
```

#### 기존 update.sh 사용자 자동 마이그레이션
```bash
# update.sh가 실행되면 안내 메시지
if [ "$(basename "$0")" = "update.sh" ]; then
    echo "📢 update.sh는 곧 deprecated됩니다."
    echo "대신 './init.sh --upgrade'를 사용해주세요."
    echo ""
    echo "3초 후 자동으로 업그레이드를 진행합니다..."
    sleep 3
    
    # init.sh --upgrade 실행
    exec "./init.sh" --upgrade "$@"
fi
```

## 4. 마이그레이션 계획

### Phase 1: 통합 구현 (1일)
- init.sh에 --upgrade, --tadd-only 옵션 추가
- 기존 update.sh 로직 통합
- 기존 tadd-enforce-installer.sh 로직 통합

### Phase 2: 호환성 보장 (반나절)
- update.sh를 init.sh 심링크로 변경
- 실행 시 deprecation 경고 표시
- 기존 사용자 가이드 업데이트

### Phase 3: 정리 (v30.0에서)
- update.sh 파일 완전 제거
- tadd-enforce-installer.sh 제거
- README에서 관련 내용 정리

## 5. URL 기반 설치 전략

### 현재 문제
```bash
# 복잡한 다중 URL
curl -sSL https://raw.../init.sh | bash -s "project" "desc"
curl -sSL https://raw.../tadd-enforce-installer.sh | bash
```

### 개선된 단일 URL
```bash
# 모든 기능을 하나로
curl -sSL https://raw.../init.sh | bash -s "project" "desc"

# 기존 프로젝트 업그레이드
curl -sSL https://raw.../init.sh | bash -s -- --upgrade

# TADD만 추가
curl -sSL https://raw.../init.sh | bash -s -- --tadd-only
```

### 단축 URL 서비스 (선택사항)
```bash
# 더 간단한 설치
curl -sSL bit.ly/claude-dev-kit | bash -s "project" "desc"
```

## 6. 사용자별 마이그레이션 가이드

### 신규 사용자
**변화 없음** - 계속 `./init.sh project_name` 사용

### 기존 update.sh 사용자
```bash
# 기존
./update.sh

# 새로운 방법 (권장)
./init.sh --upgrade

# 당분간 기존 방법도 작동 (자동 리디렉션)
./update.sh  # → ./init.sh --upgrade로 자동 실행
```

### TADD 별도 설치 사용자
```bash
# 기존
curl ... tadd-enforce-installer.sh | bash

# 새로운 방법
./init.sh --tadd-only
```

## 7. 최종 파일 구조

### v29.1 (전환기)
```
claude-dev-kit/
├── init.sh           # 통합 설치 스크립트
├── update.sh         # → init.sh 심링크 (deprecated)
├── tadd-enforce-installer.sh  # (deprecated, 기능은 init.sh에 통합)
```

### v30.0 (최종)
```
claude-dev-kit/
├── init.sh           # 모든 기능 통합
└── (기타 스크립트 제거)
```

## 8. 이점

### 개발자 관점
- **유지보수 간소화**: 1개 파일만 관리
- **기능 중복 제거**: 공통 로직 통합
- **테스트 용이성**: 단일 엔트리포인트

### 사용자 관점
- **인지 부하 감소**: 하나의 명령어만 기억
- **일관된 경험**: 모든 기능이 동일한 인터페이스
- **실수 방지**: 잘못된 스크립트 실행 방지

## 9. 위험 요소 및 대응

### Risk 1: 기존 문서/튜토리얼에서 update.sh 언급
**대응**: 심링크로 당분간 호환성 유지

### Risk 2: 사용자가 혼란스러워할 수 있음
**대응**: 명확한 마이그레이션 가이드 제공

### Risk 3: init.sh가 너무 복잡해질 수 있음
**대응**: 모듈화된 함수 구조로 설계

## 10. 결론

**추천 방향: update.sh 점진적 제거**

1. **v29.1**: init.sh에 모든 기능 통합, update.sh는 심링크로 유지
2. **v29.5**: update.sh 사용 시 deprecation 경고
3. **v30.0**: update.sh 완전 제거

**사용자에게는 하나의 명령어로 모든 것을 해결할 수 있는 편리함을 제공!**

---

**작성일**: 2025-09-02
**상태**: Strategic Planning Complete