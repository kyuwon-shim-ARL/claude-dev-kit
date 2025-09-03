# Project Rules - Claude Dev Kit

## 🚀 Core Principles
This document defines the immutable rules and principles for the Claude Dev Kit project.
These rules override any auto-generated documentation and must be followed at all times.

## 📦 Python Package Management

### MANDATORY: Use UV for Python Projects
When working with Python projects that use this toolkit:

**Always use UV (Astral's package manager) instead of pip:**
```bash
# CORRECT ✅
uv pip install package_name
uv pip install -r requirements.txt
uv venv
uv add package_name

# WRONG ❌
pip install package_name
pip3 install package_name
python -m pip install
```

**Why UV?**
- 10-100x faster than pip
- Better dependency resolution
- Modern Python packaging
- Integrated virtual environment management

**Note**: This is a recommendation enforced through documentation.
Actual system-level enforcement requires individual local configuration.

## 🏗️ Development Principles

### 1. Simplicity First
- Prefer simple, working solutions over complex theoretical ones
- If something doesn't actually work, remove it

### 2. User-Friendly Defaults
- Scripts should work with minimal or no arguments
- Use sensible defaults based on context (e.g., folder name as project name)
- Provide helpful tips rather than errors when possible

### 3. Honest Documentation
- Document what actually works, not what theoretically could work
- Be clear about limitations
- Distinguish between "recommended" and "enforced"

### 4. Clean Repository
- Remove non-functional code promptly
- Don't keep "example" code that doesn't actually work
- Maintain clear separation between distributed tools and local configurations

## 📝 Documentation Hierarchy

1. **project_rules.md** (this file) - Immutable project constitution
2. **CLAUDE.md** - Auto-generated project overview (may be overwritten)
3. **README.md** - User-facing documentation

## 🎯 Version Philosophy

- Increment versions for significant changes
- Document breaking changes clearly
- Maintain backward compatibility when possible

---
*This document is manually maintained and should not be auto-generated or modified by scripts.*