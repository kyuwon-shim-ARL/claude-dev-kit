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
python test_setup.py

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
├── test_setup.py   # System validation script
└── CLAUDE.md       # This file - system documentation
```

## 개발 워크플로우

이 프로젝트는 4단계 키워드 기반 개발을 사용합니다:
- **"기획"** → 요구사항 분석 및 PRD 작성
- **"구현"** → DRY 원칙 기반 코딩 (기존 코드 확인 후 재사용)
- **"안정화"** → MECE 검증 및 리팩토링 순환
- **"배포"** → 최종 검증 및 커밋&푸시

📝 **상세 가이드**: `docs/development/guides/claude-code-workflow.md` 참조

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