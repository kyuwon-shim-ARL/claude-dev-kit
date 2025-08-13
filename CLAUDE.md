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

## Claude Code 워크플로우

### 개발 키워드 체계
개발 과정을 4단계 키워드로 체계화:

#### 🔍 **"기획"** - Discovery & Planning
- 탐색 + 분석 + 계획 + PRD 작성 순환
- 수렴까지 반복하여 완전한 요구사항 정의

#### ⚡ **"구현"** - Implementation  
- TodoWrite 계획 + 코딩 + 단위테스트
- 핵심 기능 동작까지 완료

#### 🔄 **"안정화"** - Validation & Polish
- MECE 방식 철저한 검증 자동 실행
- 성능측정, 에지케이스, 품질점검 포함

#### 🚀 **"배포"** - Deployment
- 최종 검증 + 구조화된 커밋 + 푸시

### 사용법
```bash
# 단계별 진행
"새 기능 기획해줘"
"로그인 기능 구현해줘" 
"안정화해줘"
"배포해줘"
```

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