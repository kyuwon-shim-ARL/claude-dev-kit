# claude-dev-kit: Complete Development Kit for Claude Code

## Project Overview
A comprehensive toolkit that provides one-click installation of project structure, slash commands, ZEDS documentation system, and workflow automation for Claude Code projects.

## Current Status
- ✅ **Phase 1**: Core installation scripts completed
- ✅ **Phase 2**: ZEDS implementation completed  
- ✅ **Phase 3**: Unified initialization system completed
- ✅ **Phase 4**: Universal init.sh for all users (v4.0)
- ✅ **Phase 5**: Smart Documentation System v2.0 (스마트 아카이빙, 규모별 차별화)
- 📋 **Next**: Continuous improvement based on user feedback

## Development Environment Setup

### Prerequisites
- Claude Code CLI installed
- Bash shell (Linux/Mac/WSL)
- Git (optional, for version control)
- curl (for downloading commands)

### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/kyuwon-shim-ARL/claude-dev-kit.git
cd claude-dev-kit

# 2. Universal installation (recommended for ALL users)
./init.sh "project_name" "Project description"
# Works for both new and existing projects
# Automatically detects Git and adapts features
# Then follow prompts to run complete installation

# 4. Verify installation
ls -la .claude/commands/  # Should show 10 commands
```

## Key Commands

### Development
```bash
make setup          # Full development setup
make test           # Run tests
make lint           # Code linting
make format         # Code formatting
make clean          # Clean generated files
```

## Project Structure
```
claude-dev-kit/           # Claude Code Development Kit
├── CLAUDE.md            # Main project documentation
├── install.sh           # Core installation script
├── install-web.sh       # Web development extension
├── init.sh              # 🆕 Universal installer (v4.0) - USE THIS!
├── init-complete.sh     # (Deprecated) Use init.sh instead
├── safe-init-claude-repo.sh  # (Deprecated) Use init.sh instead
└── init-claude-repo.sh  # (Legacy) Original script

docs/                    # Documentation
├── guides/              # Development guides and settings
│   ├── claude-code-best-practices.md  # Best practices
│   ├── claude-me-settings-minimal.md  # 🔧 백업 옵션 (웹 전용)
│   └── distribute.md    # Distribution guide
└── templates/           # Document templates
    └── README-TEMPLATE.md  # README template

scripts/                 # Development tools
├── setup_claude_code_structure.py  # Structure generator
└── test_comprehensive.py           # Test suite

# Generated in target projects:
src/[project]/          # Core implementation
├── core/               # Shared components
├── models/             # Data schemas
├── services/           # Business logic
└── web/               # Web extension (optional)
    ├── backend/       # FastAPI server
    ├── frontend/      # Frontend code
    └── tests/         # E2E tests

examples/              # Usage examples
tests/                # Test suites
tools/                # Utilities
project_rules.md      # Project constitution (manual)
.claudeignore         # Context exclusions
```

## 개발 워크플로우

이 프로젝트는 4단계 키워드 기반 개발을 사용합니다:
- **"기획"** → Structured Discovery & Planning Loop:
  - 탐색: 전체 구조 파악, As-Is/To-Be/Gap 분석
  - 계획: MECE 기반 작업분해, 우선순위 설정
  - 수렴: 탐색↔계획 반복 until PRD 완성
- **"구현"** → Implementation with DRY:
  - 기존 코드 검색 → 재사용 → 없으면 생성
  - TodoWrite 기반 체계적 진행
  - 단위 테스트 & 기본 검증
- **"안정화"** → Structural Sustainability Protocol v2.0:
  - 구조 스캔: 전체 파일 분석, 중복/임시 파일 식별
  - 구조 최적화: 디렉토리 정리, 파일 분류, 네이밍 표준화
  - 의존성 해결: Import 수정, 참조 오류 해결
  - 통합 테스트: 모듈 검증, API 테스트, 시스템 무결성
  - 문서 동기화: CLAUDE.md 반영, README 업데이트
  - 품질 검증: MECE 분석, 성능 벤치마크 (ZERO 이슈까지)
- **"배포"** → Deployment: 최종검증 + 구조화커밋 + 푸시 + 태깅

## @배포 전: Claude 컨텍스트 관리 시스템

프로젝트의 안정성과 AI 협업 효율을 극대화하기 위해, Claude의 컨텍스트를 **전략**과 **실행**으로 나누어 체계적으로 관리한다.

### **1. 전략 (Strategy): 역할 분리를 통한 안정성 확보**

#### **1.1. 핵심 원칙: '불변'과 '가변'의 분리**

* **불변(Immutable) 컨텍스트**: 프로젝트의 핵심 규칙과 철학. **수동**으로 관리하여 안정성을 보장한다.
* **가변(Mutable) 컨텍스트**: 코드의 현재 상태와 구조. **자동**으로 관리하여 최신성을 보장한다.

#### **1.2. `project_rules.md`: 프로젝트의 '헌법' 📜**

* **역할**: 프로젝트의 목표, 아키텍처 원칙, 코딩 스타일, DevOps 규칙 등 **사람의 의사결정이 담긴 최상위 지침**을 정의한다.
* **관리**: **수동 관리(Manual)**. 전략적 변경이 있을 때만 신중하게 수정한다. `claude init`의 영향을 받지 않는다.

#### **1.3. `claude.md`: 프로젝트의 '실시간 지도' 🗺️**

* **역할**: `claude init`을 통해 생성된, 현재 코드베이스의 구조와 관계를 요약한 **기술적 현황 보고서**이다.
* **관리**: **자동 관리(Automatic)**. Git Hook을 통해 커밋 시마다 자동으로 갱신되어 항상 최신 상태를 유지한다.

### **2. 실행 (Implementation): 3단계 워크플로우**

#### **2.1. 1단계: 초기 설정 (Set-up)**

* **a. `project_rules.md` 파일 생성**: 프로젝트 최상단에 핵심 규칙을 담은 `project_rules.md` 파일을 작성한다.
* **b. `.claudeignore` 파일 설정**: `node_modules`, `dist`, 빌드 결과물, 로그 등 AI 컨텍스트에 불필요한 자원을 명시하여 `claude.md`의 품질과 효율을 높인다.

#### **2.2. 2단계: 자동화 (Automation)**

* **a. Git `pre-commit` Hook 설정**: `git commit` 시 `claude init` 명령어가 자동으로 실행되도록 설정한다.
  * **목표**: `claude.md` 파일이 항상 최신 코드 상태를 반영하도록 강제한다.
  * **스크립트 예시**:
    ```bash
    #!/bin/sh
    claude init --silent
    git add claude.md
    ```

#### **2.3. 3단계: 활용 (Execution)**

* **a. 컨텍스트 통합 호출**: Claude에게 질문 시, '헌법'과 '지도'를 함께 제공하여 가장 정확한 답변을 유도한다.
  * **목표**: 안정적인 상위 규칙(헌법) 하에 최신 코드 구조(지도)를 분석하도록 지시한다.
  * **명령어 예시**:
    ```bash
    cat project_rules.md claude.md | claude ask "질문 내용"
    ```

📝 **상세 가이드**: `docs/development/guides/claude-code-workflow.md` 참조

## 구조적 지속가능성 원칙

### 📁 Repository 구조 관리
- **Root 정리**: 필수 진입점만 유지 (main_app.py, CLAUDE.md), 도구는 scripts/
- **계층구조**: src/{project}/core/, services/, models/ 체계 준수
- **파일 분류**: 기능별 적절한 디렉토리 배치
- **임시 파일 관리**: *.tmp, *.bak 등 정기적 정리

### 🔄 예방적 관리 시스템
**자동 트리거 조건:**
- 루트 디렉토리 파일 20개 이상
- 임시 파일 5개 이상
- Import 오류 3개 이상
- 매 5번째 커밋마다

### 📊 품질 메트릭스
- **구조적 복잡도**: 디렉토리 깊이, 파일 분산도
- **의존성 건전성**: 순환참조, 결합도
- **문서 동기화율**: 코드-문서 일치 정도
- **테스트 커버리지**: 전체 시스템 검증률

## 구현 체크리스트

### 구현 전 확인사항
- ☐ **기존 코드 검색**: 비슷한 기능이 이미 있는가?
- ☐ **재사용성 검토**: 이 기능을 다른 곳에서도 사용할 수 있는가?
- ☐ **중앙화 고려**: `core/` 디렉토리에 공통 모듈로 배치할가?
- ☐ **인터페이스 설계**: 모듈 간 명확한 계약이 있는가?
- ☐ **테스트 가능성**: 단위 테스트하기 쉬운 구조인가?

### 코드 품질 체크
- ☐ **DRY 원칙**: 코드 중복이 없는가?
- ☐ **Single Source of Truth**: 동일 기능이 여러 곳에 있지 않는가?
- ☐ **의존성 최소화**: 불필요한 결합이 없는가?
- ☐ **명확한 네이밍**: 기능을 잘 나타내는 이름인가?

## Contributing Guidelines

### Code Style
- Use consistent formatting
- Type hints required
- Docstrings for public methods

### Testing Requirements
- All new features need tests
- Integration tests for system components

### Documentation
- Update CLAUDE.md for architectural changes
- Include usage examples for new features

## Development Process
See `docs/development/guides/` for:
- Session management workflows  
- Documentation standards
- Testing strategies
- Deployment procedures