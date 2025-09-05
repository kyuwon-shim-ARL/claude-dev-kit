# 🚀 외부 레포 배포 가이드

## Quick Start - 외부 프로젝트에 재구조화 커맨드 적용

### 1. 기본 배포 (권장)
```bash
# 대상 프로젝트 디렉토리에서 실행
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/scripts/deploy_to_external_repo.sh | bash -s -- . --with-tadd --legacy-redirect
```

### 2. 로컬에서 배포
```bash
git clone https://github.com/kyuwon-shim-ARL/claude-dev-kit.git
cd claude-dev-kit

# 대상 프로젝트로 배포
./scripts/deploy_to_external_repo.sh /path/to/your/project --with-tadd --legacy-redirect
```

### 3. 배포 옵션

| 옵션 | 설명 | 권장 |
|------|------|------|
| `--with-tadd` | TADD 검증 시스템 포함 | ✅ 권장 |
| `--legacy-redirect` | 기존 25개 커맨드 자동 매핑 | ✅ 권장 |
| `--dry-run` | 시뮬레이션만 (실제 변경 없음) | 테스트시 |

## 배포 후 즉시 사용 가능

### 🔍 탐색 트랙
```bash
/분석 "현재 프로젝트 상태 파악"     # 5단계 완전 분석
/찾기 "특정 기능 구현 방법"        # 문서+코드 통합 검색  
/보고 "주간 진행 상황"            # 주간보고+보고서 통합
```

### 🛠️ TADD 실행 트랙  
```bash
/기획 "새 기능 개발 계획"          # LLM 지능형 라우팅
/테스트 "실패 테스트 우선 작성"    # TADD 강제
/구현 "테스트 통과 구현"          # Real Testing  
/배포 "검증 및 배포"              # 6단계 통합 프로세스
```

### 🎯 특수 트랙
```bash
/전체사이클 "완전한 개발 사이클"   # 자동화된 전체 워크플로우
/문서정리 "문서 자동 정리"        # 3-Layer 문서화 시스템
```

## 주요 혁신 사항

### ✨ 60% 효율성 향상 (25→9)
- 기존 25개 중복 커맨드를 9개 핵심 커맨드로 재구조화
- LLM 지능형 라우팅으로 자동 모드 선택
- 기존 커맨드는 자동 리다이렉트로 호환성 유지

### 🎯 TADD 품질 보증
- Theater Testing 자동 차단 (Python AST 기반)
- Real Testing 강제 (구체적 값 검증)
- Mock 사용률 20% 제한
- GitHub Actions 자동 품질 검증

### 📚 3-Layer 문서화 시스템
- **실시간**: 개발 중 자동 메타데이터 추가
- **주기적**: 세션별 자동 정리 및 분류
- **마감**: 완성된 문서 아카이빙

## 트러블슈팅

### Q: 기존 커맨드가 작동하지 않음
A: `--legacy-redirect` 옵션으로 배포했는지 확인하세요.

### Q: TADD 검증 실패
A: `scripts/check_theater_testing.py` 실행하여 Theater Testing 패턴을 확인하세요.

### Q: 문서가 자동 생성되지 않음  
A: `.claude/commands/문서정리.md` 커맨드를 확인하고 메타데이터 시스템이 활성화되어 있는지 확인하세요.

## 지원

- **Issues**: https://github.com/kyuwon-shim-ARL/claude-dev-kit/issues
- **Discussions**: GitHub Discussions
- **Documentation**: 프로젝트 `CLAUDE.md` 참조

---

**주의**: 이 시스템은 Claude Code와 함께 사용하도록 설계되었습니다. 일반 프로젝트에서는 일부 기능이 제한될 수 있습니다.