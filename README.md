# 🎯 Claude Code Development Kit

효율적인 Claude Code 개발 워크플로우를 위한 템플릿과 도구 모음입니다.

## ⚡ 30초 설치

### 🚀 Universal 설치 (Git 유무 자동 감지)
```bash
# 새 프로젝트 또는 기존 프로젝트 모두 지원
cd my-project
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh | bash

# 또는 직접 다운로드 후 실행
wget https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh
chmod +x init.sh
./init.sh "프로젝트명" "프로젝트 설명"
```

**🌟 스마트 설치 특징:**
- ✅ **Git 자동 감지**: 있으면 전체 기능 (hooks, push, tag)
- ✅ **Git 없어도 OK**: 완벽 작동 (로컬 백업)
- ✅ **제로 에러**: 비개발자도 에러 없이 자동 설치
- ✅ **30초 완료**: 복잡한 설정 없이 바로 사용 가능

### 웹 개발 확장 (선택사항)
```bash
# 기본 설치 후 웹 스택 추가 (Playwright + FastAPI + uv)
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install-web.sh | bash
```

## 🔥 핵심 기능

### ✅ 4단계 핵심 워크플로우 (ZEDS 2.0 통합)
- **/기획**: 구조화된 탐색-계획 루프 + 요구사항 분석
- **/구현**: DRY 원칙 기반 구현 + 단위 테스트
- **/안정화**: 구조적 지속가능성 + **ZEDS 2.0 문서 자동 정리**
- **/배포**: 최종 검증 + 자동 배포 + 버전 태깅

### 🛠️ 보조 명령어 (필요시 개별 사용)
- **/분석**: 분석 수행 및 자동 저장 (docs/analysis/)
- **/문서정리**: 프로젝트 문서 수동 정리 (안정화에 통합)
- **/주간보고**: 전체 프로젝트 진행 상황 종합 보고
- **/검증**: 심화 테스트 및 품질 보증
- **/전체사이클**: 기획→구현→안정화→배포 완전 자동화
- **/개발완료**: 구현→안정화→배포
- **/품질보증**: 안정화→배포
- **/기획구현**: 기획→구현
- **/극한검증**: 자동 반복 개선 until 수렴

### 🌐 웹 개발 확장
- **Playwright**: E2E 테스트 + 웹 자동화
- **FastAPI**: 고성능 웹 API 프레임워크  
- **uv**: 초고속 Python 패키지 관리
- **웹 기반 프레젠테이션**: reveal.js 통합

### 🤖 ZEDS 2.0 통합 문서 관리 시스템
- **project_rules.md**: 프로젝트 헌법 (수동 관리)
- **CLAUDE.md**: 실시간 코드 지도 (자동 업데이트)
- **Git Hook**: 커밋시 자동 컨텍스트 갱신
- **자동 문서 정리**: `/안정화` 실행 시 프로젝트 문서 자동 분류
- **6단계 로드맵**: 01-hypothesis → 06-documentation 체계적 관리
- **버전 스냅샷**: 개발 버전과 문서 버전 동기화

## 📁 프로젝트 구조

```
claude-dev-kit/
├── init.sh                 # 🆕 Universal 설치 (권장)
├── install.sh              # 슬래시 명령어만 설치
├── install-web.sh          # 웹 확장 설치
├── docs/
│   ├── guides/             # 개발 가이드
│   └── templates/          # 문서 템플릿
└── scripts/               # 개발 도구
```

설치 후 생성되는 구조:
```
your-project/
├── CLAUDE.md              # 프로젝트 문서
├── project_rules.md       # 프로젝트 헌법
├── main_app.py           # 메인 애플리케이션
├── src/your-project/     # 핵심 구현
├── examples/             # 사용 예제
├── tests/               # 테스트
└── scripts/             # 개발 스크립트
```

## 🚀 사용법

### 🎯 핵심 4단계 워크플로우 (권장)
```bash
# 1. 기획 단계
/기획 "프로젝트 요구사항"
# → 구조화된 탐색-계획 루프
# → 요구사항 분석 및 작업 계획 수립
# → docs/CURRENT/에 기획 문서 자동 생성

# 2. 구현 단계
/구현
# → DRY 원칙 기반 체계적 구현
# → 기존 코드 재사용 최우선
# → 단위 테스트 및 기본 검증

# 3. 안정화 단계 (ZEDS 2.0 통합!)
/안정화
# → 구조적 지속가능성 프로토콜
# → 📚 자동 문서 정리 (프로젝트 로드맵 기반 분류)
# → 📊 버전 스냅샷 생성
# → ✅ 종합 품질 검증

# 4. 배포 단계
/배포
# → 최종 검증 + Git Push
# → 자동 버전 태깅
# → 배포 완료 보고
```

### ⚡ 단축 명령어 (고급 사용자)
```bash
/전체사이클 "요구사항"  # 1~4단계 완전 자동화
/개발완료              # 2~4단계 (구현부터)
/품질보증              # 3~4단계 (안정화부터)
```

### 📊 보조 도구
```bash
/분석 "주제"           # 분석 + 자동 저장
/문서정리              # 수동 문서 정리 (안정화에 통합됨)
/주간보고              # 프로젝트 현황 종합 보고
```

### 🎯 ZEDS 2.0 문서 관리 시스템 (신규!)

**핵심 특징**: `/안정화` 실행 시 문서가 자동으로 프로젝트 구조로 정리됨

```
docs/
├── CURRENT/           # 현재 작업 중인 문서들
├── projects/          # 프로젝트별 체계적 정리
│   └── project-name/
│       ├── 01-hypothesis/     # 기획 및 요구사항
│       ├── 02-design/         # 설계 및 아키텍처
│       ├── 03-implementation/ # 구현 및 코딩
│       ├── 04-analysis/       # 분석 및 최적화
│       ├── 05-validation/     # 테스트 및 검증
│       └── 06-documentation/  # 문서화 및 가이드
└── archives/          # 완료된 프로젝트 보관
```

**자동화 예시**:
```bash
# /안정화 실행 시 자동으로:
1. docs/CURRENT/planning.md → projects/my-project/01-hypothesis/
2. docs/CURRENT/architecture.md → projects/my-project/02-design/
3. docs/CURRENT/test-results.md → projects/my-project/05-validation/
4. README.md 자동 생성 및 인덱스 업데이트
5. roadmap.md 진행률 자동 반영
```

### 웹 개발 (확장 설치시)
```bash
# 개발 서버 시작
./scripts/run-web.sh

# E2E 테스트 실행  
./scripts/test-web.sh

# 브라우저에서 확인
open http://localhost:8000
```

## 📚 문서 및 가이드

### 🎓 시작하기
- [설치 가이드](#-30초-설치): 30초 만에 설치 완료
- [기본 사용법](#-사용법): 4단계 워크플로우 가이드
- [ZEDS 2.0 문서 시스템](#-zeds-20-문서-관리-시스템-신규): 자동 문서 정리

### 📋 개발 가이드
- [Claude Code 개발 모범 사례](docs/guides/claude-code-best-practices.md)
- [파일 명명 규칙](docs/guides/file-naming-standards.md)
- [배포 가이드](docs/guides/distribute.md)

### 📝 템플릿 및 예제
- [README 템플릿](docs/templates/README-TEMPLATE.md)
- [프로젝트 구조 예제](docs/projects/claude-dev-kit-v10/)

### 🔧 고급 설정
- [Claude.me 웹 설정](docs/guides/claude-me-settings-minimal.md) (웹 전용 사용자)

### 📊 프로젝트 문서
- [전체 문서 구조](docs/README.md)
- [개발 세션 로그](docs/development/sessions/)
- [분석 결과](docs/analysis/)

## 🆘 자주 묻는 질문 (FAQ)

### Q: 기존 프로젝트에 설치해도 안전한가요?
✅ **완전 안전합니다.** 기존 파일은 건드리지 않고 `.claude/` 폴더만 추가합니다.

### Q: Git이 없어도 사용할 수 있나요?
✅ **완벽하게 작동합니다.** Git 없으면 로컬 백업 시스템으로 동작합니다.

### Q: 다른 프로젝트에서도 명령어를 쓸 수 있나요?
📝 **프로젝트별 설치가 필요합니다.** 각 프로젝트마다 `init.sh` 실행 필요합니다.

### Q: ZEDS 2.0 문서 정리는 언제 동작하나요?
🎯 **`/안정화` 실행 시 자동으로 동작합니다.** 별도 명령어 불필요입니다.

### Q: 웹 확장을 설치해야 하나요?
🔧 **선택사항입니다.** 웹 개발을 하는 경우에만 설치하세요.

## 🔧 특수 상황 대응

**⚠️ 특수 상황에서만 사용:**
- [Claude.me 웹 설정](docs/guides/claude-me-settings-minimal.md) - claude.ai 웹 전용 사용자
- [수동 업데이트](docs/UPDATE_GUIDE.md) - 자동 업데이트가 안 되는 경우
- [문제 해결](docs/development/testing-reality-check.md) - 일반적인 문제 해결

## 🎯 핵심 특징

### 💡 개발 효율성
- **즉시 사용**: 설치 후 바로 개발 시작 (30초 설치)
- **검증된 워크플로우**: 실제 프로젝트에서 테스트된 4단계 개발 프로세스
- **DRY 원칙**: 기존 코드 재사용 우선, 중복 제거

### 📚 혁신적 문서 관리 (ZEDS 2.0)
- **제로 에포트**: 개발하면 문서가 자동으로 정리됨
- **로드맵 기반**: 6단계 개발 로드맵에 따른 체계적 분류
- **버전 동기화**: 개발 버전과 문서 버전 완전 일치
- **지식 보존**: 모든 개발 과정과 의사결정 자동 보관

### 🚀 확장성 및 적응성
- **프로젝트 무관**: 웹 개발부터 연구 프로젝트까지 모든 영역 지원
- **Git 적응**: Git 있으면 풀 기능, 없어도 완벽 작동
- **사용자 친화**: 비개발자도 쉽게 사용 가능
- **점진적 도입**: 필요한 기능만 선택적으로 사용

### 🤖 AI 협업 최적화
- **컨텍스트 관리**: project_rules.md + CLAUDE.md 이중 구조
- **Git Hook 자동화**: 커밋할 때마다 문서 자동 동기화
- **지능형 프롬프트**: 각 단계별 최적화된 Claude 상호작용

## 🔥 ZEDS 2.0 혁신 포인트

### 📈 Before vs After
```
📋 기존 방식:
개발 → 별도 문서화 → 수동 정리 → 버전 관리 → 보관
(시간: 30분, 놓치는 정보: 70%)

🚀 ZEDS 2.0:
개발 → /안정화 → 모든 것이 자동으로 완료!
(시간: 3초, 정보 보존율: 100%)
```

### 🎯 실제 효과
- **개발 집중도 향상**: 문서 걱정 없이 개발에만 집중
- **지식 손실 방지**: 모든 의사결정과 과정 자동 보존
- **팀 협업 강화**: 체계적으로 정리된 프로젝트 히스토리
- **학습 효과**: 과거 프로젝트 패턴 분석으로 더 나은 개발

---

**🎉 이제 어떤 프로젝트든 Claude Code와 ZEDS 2.0으로 효율적이고 체계적으로 개발하세요!**

💫 **개발은 코딩만, 문서는 자동으로!** 🚀