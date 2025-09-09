<!--
@meta
id: document_20250905_1110_claude-me-settings-minimal
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-09
tags: claude-me-settings-minimal.md, settings, guides, claude, minimal
related: 
-->

# Claude.me 설정 (백업/고급 옵션)

> ⚠️ **주의**: 이 설정은 Claude Code를 사용할 수 없는 특수 상황에서만 사용하세요.
> 
> 🎯 **권장**: Claude Code + 슬래시 명령어 (/.전체사이클, /기획, /구현, /안정화, /배포)

## 🔧 언제 이 설정을 사용하나요?

**✅ 다음 상황에서만 사용:**
- 웹 claude.ai에서만 작업 가능한 경우
- Claude Code 설치가 불가능한 환경
- 프로젝트 외부에서 간단한 컨설팅/조언 시
- 키워드 기반 자연어 접근을 선호하는 경우

**❌ 다음 상황에서는 사용하지 마세요:**
- Claude Code가 설치 가능한 경우 → 슬래시 명령어 사용
- 정식 프로젝트 개발 시 → /전체사이클 사용
- 체계적 워크플로우가 필요한 경우 → Claude Code 우선

## ⚙️ 웹사이트에서 설정하는 방법:

1. https://claude.ai 접속
2. 우측 상단 프로필 → Settings
3. "Custom Instructions" 섹션
4. 아래 내용을 복사해서 붙여넣기

---

## 📝 Claude.me에 추가할 내용:

### Claude Code Workflow (Korean Keywords)
When user uses these keywords, IMMEDIATELY apply corresponding workflows:

- **"기획"** → **STRUCTURED DISCOVERY-PLANNING LOOP with Intelligent Context Management**:
  1. **Context Auto-Loading**: project_rules.md, PRD-v*.md, status.md, previous TODOs
  2. **Intelligent Context Management**: Roadmap transition detection, impact-based classification (Strategic/Tactical/Operational)
  3. **Discovery Phase**: Full structure analysis, As-Is/To-Be/Gap identification, stakeholder requirements
  4. **Planning Phase**: MECE work breakdown, priority matrix, resource planning
  5. **Convergence Phase**: Discovery↔Planning iteration until PRD complete
  6. **Documentation Strategy**: Auto-generate specs, differentiated documentation by scale

- **"구현"** → **IMPLEMENTATION WITH DRY & Context Loading**:
  1. **Context Loading**: project_rules.md, active-todos.md
  2. **DRY Application**: Grep/Glob extensive search for existing functionality
  3. **Reuse Priority**: Leverage existing libraries/modules before creating new
  4. **Systematic Progress**: TodoWrite-based step-by-step implementation
  5. **Quality Assurance**: Unit testing, syntax check, type check, lint
  6. **Auto Documentation**: Record progress in implementation.md

- **"안정화"** → **STRUCTURE-COUPLED DOCUMENTATION + SUSTAINABILITY v3.0**:
  1. **Context Loading**: project_rules.md, test-report.md
  2. **Repository Structure Scan**: Full file analysis, duplicate/temp file identification
  3. **Structural Optimization**: Directory cleanup, logical grouping, naming standardization
  4. **Dependency Resolution**: Import fixes, circular reference resolution
  5. **TADD-Integrated Testing + GitHub Actions Integration**: 
     - Pre-Push GitHub Actions compatibility check
     - Real scenario testing (NO MOCKS)
     - TADD validation with CI/CD integration
  6. **Structure-Document Sync**: CLAUDE.md, README auto-update with code structure
  7. **Quality Assurance**: MECE analysis, performance benchmarks with specific metrics

- **"배포"** → **DEPLOYMENT WITH GITHUB ACTIONS REAL-TIME MONITORING**:
  1. **Context Loading**: project_rules.md, all CURRENT/ status
  2. **Auto Completion Checklist**: 20-item verification (code quality, documentation, structure, deployment readiness)
  3. **Structured Commit**: Meaningful messages, atomic changes, issue linking
  4. **Remote Deployment**: MANDATORY git push + GitHub Actions monitoring
  5. **Real-time CI/CD Verification**: Wait for GitHub Actions "All Pass" before success declaration
  6. **Post-deployment Verification**: Remote repository reflection, endpoint functionality
  7. **Intelligent Session Closure**: Auto-archive completed documents when 5+ completion documents detected

### Mock Test Prohibition
NEVER use mock data or fake testing. Always use real data and actual user scenarios.

### Python Package Management
**ALWAYS use UV instead of pip for Python projects:**
- Use `uv pip install` instead of `pip install`
- Use `uv venv` instead of `python -m venv` 
- Use `uv add` to add dependencies
- Use `uv sync` to sync dependencies
Why: UV is 10-100x faster than pip and provides better dependency resolution.

### DRY Principle
Before creating new code, always search for existing similar functionality first.

### Quantitative Verification
Never say "passed" - always provide specific metrics and measurements.

---

## 💡 참고 사항

**이 설정은 Claude Code의 완전한 대체품이 아닙니다.**
- 슬래시 명령어만큼 정확하지 않음
- 프로젝트 컨텍스트 자동 로딩 없음
- 버전 관리 및 동기화 기능 없음

**최상의 경험을 위해서는 Claude Code를 설치하세요:**
```bash
# Claude Code 설치 후
curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/init.sh | bash
```