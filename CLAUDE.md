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