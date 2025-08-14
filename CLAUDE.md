# [PROJECT_NAME]: [PROJECT_DESCRIPTION]

## Project Overview
[Brief description of what this project does and its main purpose]

## Current Status
- ✅ **Phase 1**: [Completed milestone]
- 🔄 **Phase 2**: [Current focus]
- 📋 **Next**: [Planned next steps]

## Development Environment Setup

### Prerequisites
- [List key dependencies]
- [Development tools needed]

### Quick Start
```bash
# 1. Clone and setup
git clone [repo-url]
cd [project-name]

# 2. Install dependencies
[installation commands]

# 3. Verify setup
python scripts/test_setup.py

# 4. Run examples
[example commands]
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
src/[project_name]/
├── core/           # Core components
├── models/         # Data schemas
├── services/       # Service layer
└── main.py         # Main interface

docs/
├── CURRENT/        # Latest project status
├── development/    # Development process records
│   ├── conversations/  # Session archives
│   ├── templates/     # Documentation templates
│   └── guides/        # Development guides
└── specs/          # Project specifications

core_features/      # Validated functionality
tests/             # Unit and integration tests
examples/          # Usage examples
tools/             # Standalone utilities
scripts/           # Development scripts
archive/           # Legacy code (organized)

# Entry Points  
├── main_app.py     # Main application entry
├── CLAUDE.md       # This file - system documentation
└── scripts/        # Development and validation tools
    └── test_setup.py   # System validation script
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