# claude-dev-kit Project Rules

## 🎯 Core Philosophy
- **중앙화된 프롬프트 관리**: prompts/api.json이 Single Source of Truth
- **Mock 테스트 금지**: 실제 사용자 시나리오 검증 필수
- **워크플로우 기반 개발**: /전체사이클 중심의 체계적 진행
- **Zero-Effort Documentation**: 슬래시 커맨드 사용만으로 자동 문서화

## 📐 Architecture Principles
- **프롬프트 동기화**: prompts/api.json → 모든 플랫폼 자동 동기화
- **4단계 워크플로우**: 기획 → 구현 → 안정화 → 배포
- **글로벌 슬래시 명령어**: 10개 명령어 표준화 (개별 5개 + 조합 5개)
- **3층 문서화 구조**: project_rules.md / docs/CURRENT/ / sessions/

## 🔧 Development Standards
- **배포 정의**: 배포 = 커밋 + 푸시 + 태깅 + 검증
- **DRY 원칙**: 코드 중복 절대 금지, 재사용 우선
- **구조적 지속가능성**: 6단계 검증 루프 필수 적용
- **정량적 검증**: "통과했습니다" 금지, 구체적 수치 제시

## 📚 Documentation Workflow
- **세션 시작**: project_rules.md + docs/CURRENT/status.md 자동 로드
- **작업 진행**: 각 단계별 자동 문서화 (planning.md, implementation.md, test-report.md)
- **세션 종료**: /배포 시 자동으로 sessions/에 아카이브
- **토큰 효율**: 현재 컨텍스트만 로드 (< 1000 tokens)

## 🚀 Deployment Protocol
- **필수 푸시**: 커밋만 하고 끝내지 말고 반드시 원격 저장소에 푸시
- **버전 태깅**: semantic versioning 준수 (major.minor.patch)
- **세션 아카이빙**: 배포 시 자동으로 현재 세션을 아카이브
- **GitHub Raw URL**: 모든 프롬프트는 GitHub에서 직접 접근 가능

## ⚙️ Technical Stack
- **Python**: 3.8+ 필수, uv 패키지 매니저 권장
- **Git**: pre-commit hooks 자동 설정
- **Playwright**: 웹 프로젝트 E2E 테스트 필수
- **Claude Code**: 슬래시 명령어 기반 워크플로우

## 📊 Success Metrics
- **문서화 추가 시간**: 0분 (완전 자동)
- **컨텍스트 로드**: < 1000 tokens
- **세션 연속성**: 100% 유지
- **배포 성공률**: push까지 완료 100%

---
*이 문서는 claude-dev-kit의 헌법입니다. 수동으로만 수정하세요.*