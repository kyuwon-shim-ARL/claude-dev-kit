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

**특징:**
- ✅ Git 있으면: 전체 기능 (hooks, push, tag)
- ✅ Git 없어도: 완벽 작동 (로컬 백업)
- ✅ 비개발자 친화적: 에러 없이 자동 설치

### 웹 개발 확장 (선택사항)
```bash
# 기본 설치 후 웹 스택 추가 (Playwright + FastAPI + uv)
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install-web.sh | bash
```

## 🔥 핵심 기능

### ✅ 슬래시 명령어 워크플로우 (10개)
- **/기획**: 구조화된 탐색-계획 루프
- **/구현**: DRY 원칙 기반 구현
- **/안정화**: 구조적 지속가능성 프로토콜 v2.0
- **/검증**: 🆕 심화 테스트 및 품질 보증
- **/배포**: 최종 검증 + 자동 배포
- **/전체사이클**: 기획→구현→안정화→배포 완전 자동화
- **/개발완료**: 구현→안정화→배포
- **/품질보증**: 안정화→배포
- **/기획구현**: 기획→구현
- **/극한검증**: 🆕 자동 반복 개선 until 수렴

### 🌐 웹 개발 확장
- **Playwright**: E2E 테스트 + 웹 자동화
- **FastAPI**: 고성능 웹 API 프레임워크  
- **uv**: 초고속 Python 패키지 관리
- **웹 기반 프레젠테이션**: reveal.js 통합

### 🤖 Claude 컨텍스트 관리
- **project_rules.md**: 프로젝트 헌법 (수동 관리)
- **claude.md**: 실시간 코드 지도 (자동 업데이트)
- **Git Hook**: 커밋시 자동 컨텍스트 갱신

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

### 개발 시작
```bash
# 1. 설치 완료 후
"@기획해줘" # → 요구사항 분석 + 작업 계획

# 2. 구현
"@구현해줘" # → DRY 원칙 기반 코딩

# 3. 품질 보증  
"@안정화해줘" # → 6단계 구조적 검증

# 4. 배포
"@배포해줜" # → 최종 검증 + Git Push
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

## 📚 문서

- [개발 가이드](docs/guides/claude-code-best-practices.md)
- [README 템플릿](docs/templates/README-TEMPLATE.md)

## 🎯 특징

- **즉시 사용**: 설치 후 바로 개발 시작
- **검증된 워크플로우**: 실제 프로젝트에서 테스트됨
- **확장 가능**: 웹 개발부터 일반 프로젝트까지
- **자동화**: Git Hook으로 컨텍스트 자동 관리

---

**이제 어떤 프로젝트든 Claude Code와 함께 효율적으로 개발하세요!** 🚀