<!--
@meta
id: document_20250905_1110_project_rules
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: project, project_rules.md, rules
related: 
-->

# Project Rules - Claude Dev Kit

## 🎯 목표 (Goals)
**Primary Mission**: 모든 Claude Code 프로젝트에서 즉시 사용 가능한 포괄적 개발 도구킷 제공
- 30초 내 완전한 개발환경 구축
- TADD(Test-AI-Driven Development) 방법론 자동 강제
- 문서화 및 컨텍스트 관리 자동화
- 코드 품질 및 테스트 품질 보증

## 📜 원칙 (Principles)  
1. **Zero Configuration**: 사용자 설정 없이 즉시 작동
2. **System Enforcement**: 프롬프트가 아닌 시스템이 품질 강제
3. **Comprehensive Coverage**: 개발 전 과정을 하나의 도구킷으로 해결
4. **AI-Human Collaboration**: AI 개발 워크플로우 최적화

## 🔧 규칙 (Rules)

### 필수 준수사항
1. **TADD 방법론 강제**: 테스트 우선 작성, Mock 20% 이하 유지
2. **Quality Gate 통과**: 모든 PR은 자동 품질 검증 통과 필수
3. **Documentation Sync**: 코드 변경 시 문서 자동 동기화
4. **컨텍스트 관리**: 3층 컨텍스트 시스템 유지 (Strategic/Tactical/Operational)

### 코딩 스타일
- Type hints 필수
- 함수별 docstring 작성
- Clean Code 원칙 준수

## 📋 가이드라인 (Guidelines)

### 개발 워크플로우
1. **기획** → 구조적 발견 및 계획 루프
2. **구현** → DRY 원칙 기반 체계적 개발
3. **안정화** → ZEDS 2.0 통합 구조적 지속가능성 프로토콜
4. **배포** → 최종검증 후 구조화 커밋

### 슬래시 명령어 활용
- `/비전수립`, `/전략기획`, `/로드맵관리` 등 10개 명령어 활용
- 메타데이터 기반 문서 관리 시스템 활용

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