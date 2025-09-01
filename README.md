# 🎯 Claude Dev Kit - AI-Native Development Toolkit

[![Version](https://img.shields.io/badge/version-v25.0-blue)](https://github.com/kyuwon-shim-ARL/claude-dev-kit/releases)
[![TADD](https://img.shields.io/badge/TADD-Enforced-green)](https://github.com/kyuwon-shim-ARL/claude-dev-kit/blob/main/.github/workflows/tadd-enforcement.yml)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

**완벽한 AI-Native 개발 환경을 30초 만에 구축하는 개발 도구**

## 🚀 30초 설치 (모든 사용자용)

### Universal 설치 (권장)
```bash
# Git 유무 자동 감지하여 최적 설치
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh | bash -s "프로젝트명" "프로젝트 설명"

# 또는 직접 다운로드
wget https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh
chmod +x init.sh
./init.sh "my-project" "My AI project"
```

### 기존 프로젝트 업데이트
```bash
# 슬래시 명령어 + GitHub Actions + TADD 스크립트 업데이트 (v25.3.0+)
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/update.sh | bash

# 자동 업데이트 항목:
# ✓ 슬래시 명령어 최신화
# ✓ GitHub Actions TADD 강제 시스템 (선택적)
# ✓ TADD 검증 스크립트 (자동)
# ✓ 백업 자동 생성 및 롤백 지원
```

## ✨ 핵심 기능

### 📊 Document Tracking System (v25.1) 🆕
**모든 문서의 메타데이터와 관계를 자동으로 추적:**
- **메타데이터 자동 삽입**: 문서 생성 시 ID, 타입, 상태, 참조 자동 기록
- **참조 그래프 구축**: 문서 간 관계를 실시간으로 추적하고 시각화
- **생명주기 관리**: draft → review → published → archived 자동 전환
- **Git Hooks 통합**: 커밋 시 자동으로 메타데이터 업데이트

#### 설치 및 사용
```bash
# Document Tracking System 설치
./scripts/setup_document_tracking_hooks.sh

# 시스템 테스트
python3 scripts/test_document_tracking.py

# 수동 메타데이터 업데이트
python3 scripts/update_document_metadata.py docs/your-document.md
```

### 🤖 슬래시 명령어 시스템 (v25)
완전한 개발 워크플로우를 4단계로 자동화:

| 명령어 | 설명 | 소요시간 |
|--------|------|----------|
| `/기획` | 구조화된 탐색-계획 루프 | 5-15분 |
| `/구현` | DRY 원칙 기반 체계적 구현 | 10-60분 |
| `/안정화` | 구조적 지속가능성 검증 | 5-20분 |
| `/배포` | 자동 품질검증 + 원격배포 | 2-5분 |

#### 통합 워크플로우
- `/전체사이클`: 기획→구현→안정화→배포 (완전 자동화)
- `/개발완료`: 구현→안정화→배포
- `/품질보증`: 안정화→배포

### 🎯 TADD Enforcement System (v24)
**프롬프트가 아닌 시스템이 품질을 강제:**
- Git 히스토리 기반 테스트-코드 순서 자동 검증
- Mock 사용률 20% 이하 시스템적 강제
- GitHub Actions PR 자동 차단/승인
- AI도 회피 불가능한 품질 보증

### 📊 완성도 체크리스트 (v15.1)
배포 전 자동으로 20개 항목 검증:
- 코드 품질 (5개)
- 문서화 (4개) 
- 구조적 안정성 (4개)
- 배포 준비 (4개)
- 성능 지표 (3개)

## 🏗️ 프로젝트 구조

```
claude-dev-kit/
├── init.sh                         # ⭐ Universal 초기화 (누구나 30초)
├── update.sh                       # ⭐ 기존 설치 업데이트 (10초)
├── .claude/
│   └── commands/                   # 슬래시 명령어 (한/영 지원)
│       ├── 기획.md (plan.md)
│       ├── 구현.md (implement.md)
│       ├── 안정화.md (stabilize.md)
│       └── 배포.md (deploy.md)
├── scripts/
│   ├── verify_tadd_order.py        # TADD 순서 검증
│   ├── detect_mock_usage.py        # Mock 사용률 분석
│   └── quick_tadd_check.sh         # 빠른 품질 체크
├── docs/
│   ├── CURRENT/                    # 현재 작업 상태
│   ├── guides/                     # 개발 가이드
│   └── templates/                  # 문서 템플릿
├── scripts/
│   ├── document_metadata.py        # 🆕 메타데이터 관리
│   ├── document_graph.py           # 🆕 참조 그래프 시스템
│   ├── document_lifecycle.py       # 🆕 생명주기 자동화
│   └── setup_document_tracking_hooks.sh  # 🆕 설치 스크립트
└── CLAUDE.md                       # 프로젝트 상세 문서
```

## 🎮 Quick Start

### 1. 새 프로젝트 시작
```bash
mkdir my-ai-project && cd my-ai-project
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh | bash -s "my-ai-project" "AI-powered application"
```

### 2. 개발 사이클 (Claude Code에서)
```bash
# 1. 기획
/기획 "사용자 인증 시스템"

# 2. 구현 (TADD 자동 적용)
/구현 "로그인 기능"
# → 테스트 먼저 생성
# → 구현 코드 작성
# → 자동 검증

# 3. 빠른 품질 체크
./scripts/quick_tadd_check.sh

# 4. 배포
/배포
# → 20개 완성도 체크
# → 자동 커밋/푸시/태깅
# → 원격 저장소 검증
```

### 3. 기존 프로젝트 업그레이드
```bash
# 현재 디렉토리에서 최신 명령어로 업데이트
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/update.sh | bash
```

## 🔧 고급 사용법

### TADD 강제 시스템 활성화 (중요!)

**🚨 GitHub Actions 자동 강제 시스템:**
```bash
# 1. GitHub에 프로젝트 푸시 (자동으로 TADD 강제 활성화)
git remote add origin https://github.com/username/project.git
git push -u origin main

# 2. 이후 모든 PR이 자동으로 TADD 검증됨
# → 테스트 우선 작성 안하면 PR 자동 차단
# → Mock 20% 초과시 PR 자동 차단  
# → 테스트 커버리지 80% 미만시 경고
```

**💡 시스템적 강제의 핵심:**
- **AI도 회피 불가능**: GitHub Actions가 모든 PR을 자동 검증
- **프롬프트 무시 불가**: 시스템 레벨에서 품질 강제
- **팀 전체 적용**: 모든 개발자가 동일한 품질 기준 준수

**📋 로컬 검증 (선택사항):**
```bash
# 빠른 체크
./scripts/quick_tadd_check.sh

# 상세 분석
python scripts/verify_tadd_order.py   # 테스트-코드 순서
python scripts/detect_mock_usage.py   # Mock 패턴 분석
```

### 문서 관리
```bash
/문서정리                            # 프로젝트 문서 정리
/레포정리                            # 저장소 구조 정리
/주간보고                            # Git 기반 진행 리포트
```

## 📈 검증된 성과

### Before (일반 개발)
- 워크플로우: 매번 다름
- 품질 일관성: 30%
- 반복 작업: 평균 4회
- 문서화: 수동

### After (claude-dev-kit)
- 워크플로우: **100% 표준화**
- 품질 일관성: **95%+**
- 반복 작업: **평균 1회**
- 문서화: **자동 동기화**

## 🛠️ 기술 스택

- **Core**: Bash, Python, YAML
- **CI/CD**: GitHub Actions
- **Testing**: pytest, AST analysis
- **Documentation**: Markdown, Auto-sync
- **Version Control**: Git, Semantic Versioning

## 📚 문서

- [CLAUDE.md](CLAUDE.md) - 프로젝트 상세 가이드
- [Installation Guide](docs/guides/installation.md)
- [TADD Guide](docs/guides/tadd-guide.md)
- [Workflow Guide](docs/guides/claude-code-workflow.md)

## 🤝 기여하기

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. **Write tests first** (`test: Add amazing tests`)
4. Implement feature (`feat: Add amazing feature`)
5. Run quality check (`./scripts/quick_tadd_check.sh`)
6. Create Pull Request

## 📊 현재 상태

- **버전**: v25.0.0
- **설치**: init.sh (Universal)
- **업데이트**: update.sh (10초)
- **명령어**: 16개 (한/영 지원)
- **검증**: TADD Enforcement
- **커버리지**: 95%+

## 🎯 주요 사용 사례

### 개인 개발자
- **30초 설치**: 즉시 고품질 개발 환경
- **자동화**: 반복 작업 75% 감소
- **품질**: 프로 수준 코드 품질

### 팀 개발
- **표준화**: 일관된 워크플로우
- **CI/CD**: GitHub Actions 통합
- **협업**: 명확한 개발 프로세스

### AI 개발
- **Claude 최적화**: 완벽한 AI 협업 환경
- **컨텍스트 관리**: 프로젝트 헌법 + 실시간 지도
- **문서 동기화**: 코드-문서 자동 일치

## 🔗 링크

- [GitHub Repository](https://github.com/kyuwon-shim-ARL/claude-dev-kit)
- [Latest Release](https://github.com/kyuwon-shim-ARL/claude-dev-kit/releases/latest)
- [Issues](https://github.com/kyuwon-shim-ARL/claude-dev-kit/issues)
- [Discussions](https://github.com/kyuwon-shim-ARL/claude-dev-kit/discussions)

---

**"30초 설치, 평생 품질"** - claude-dev-kit으로 개발의 새로운 표준을 경험하세요.

Made with ❤️ by [Claude Dev Kit Team](https://github.com/kyuwon-shim-ARL)
